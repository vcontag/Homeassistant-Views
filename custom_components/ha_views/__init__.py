"""Home Assistant Views.

Liefert die Steuerseiten (Saugroboter, Wäsche, Fernseher, …) unter /ha_views aus
und trägt sie in die Seitenleiste ein. Jede Ansicht erscheint nur, wenn die
zugehörige Integration in Home Assistant eingerichtet ist, und verschwindet
wieder, wenn sie entfernt wird.
"""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any

from homeassistant.components import frontend
from homeassistant.components.http import StaticPathConfig
from homeassistant.config_entries import SIGNAL_CONFIG_ENTRY_CHANGED, ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers import device_registry as dr, entity_registry as er
from homeassistant.helpers.debounce import Debouncer
from homeassistant.helpers.dispatcher import async_dispatcher_connect
from homeassistant.loader import async_get_integration

from .const import (
    CONF_KNOWN,
    CONF_SIDEBAR,
    CONF_TOKEN,
    DEFAULT_SIDEBAR,
    DOMAIN,
    URL_BASE,
    VIEWS,
    VIEWS_V1,
    View,
)

_LOGGER = logging.getLogger(__name__)

WWW = Path(__file__).parent / "www"


def _write_file(path: Path, content: str) -> None:
    """Datei schreiben, nur wenn sich der Inhalt geändert hat."""
    try:
        if path.exists() and path.read_text(encoding="utf-8") == content:
            return
    except OSError:
        pass
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(content, encoding="utf-8")
    tmp.replace(path)


def _is_available(hass: HomeAssistant, view: View) -> bool:
    """Prüfen, ob die Integration bzw. Geräte für eine Ansicht vorhanden sind."""
    if view.always:
        return True
    for domain in view.domains:
        if hass.config_entries.async_entries(domain, include_ignore=False, include_disabled=False):
            return True
    if view.entity_domains:
        prefixes = tuple(f"{d}." for d in view.entity_domains)
        for entry in er.async_get(hass).entities.values():
            if entry.disabled_by is None and entry.entity_id.startswith(prefixes):
                return True
    if view.zigbee2mqtt:
        for device in dr.async_get(hass).devices.values():
            if device.disabled_by is None and any(
                dom == "mqtt" and str(ident).startswith("zigbee2mqtt_")
                for dom, ident in device.identifiers
            ):
                return True
    return False


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Integration einrichten."""
    data: dict[str, Any] = hass.data.setdefault(DOMAIN, {})

    # Statische Dateien nur einmal registrieren (bleibt auch beim Neuladen bestehen).
    # cache_headers=False, damit nach Updates nicht wochenlang alte Seiten aus dem Cache kommen.
    if not data.get("static_registered"):
        await hass.http.async_register_static_paths(
            [StaticPathConfig(URL_BASE, str(WWW), cache_headers=False)]
        )
        data["static_registered"] = True

    integration = await async_get_integration(hass, DOMAIN)
    version = str(integration.version or "0")

    # Optionales festes Token für Handy-Verknüpfungen außerhalb der HA-Oberfläche.
    token = (entry.options.get(CONF_TOKEN) or "").strip()
    await hass.async_add_executor_job(
        _write_file,
        WWW / "ha-token.js",
        "// Wird von der Integration geschrieben – nicht von Hand ändern.\n"
        f"window.HA_FIXED_TOKEN = {json.dumps(token)};\n",
    )

    state: dict[str, Any] = {"panels": set(), "available": None, "version": version}
    data[entry.entry_id] = state

    async def _async_sync() -> None:
        """Seitenleiste und views.json an die vorhandenen Integrationen anpassen."""
        available = [v.key for v in VIEWS if _is_available(hass, v)]
        sidebar = set(entry.options.get(CONF_SIDEBAR, DEFAULT_SIDEBAR))
        # Neue Ansichten (beim Speichern der Optionen noch unbekannt) standardmäßig einblenden
        if CONF_SIDEBAR in entry.options:
            known = set(entry.options.get(CONF_KNOWN, VIEWS_V1))
            sidebar |= {v.key for v in VIEWS if v.key not in known and v.key in DEFAULT_SIDEBAR}
        wanted = {v.key for v in VIEWS if v.key in available and v.key in sidebar}

        for view in VIEWS:
            if view.key in state["panels"] and view.key not in wanted:
                frontend.async_remove_panel(hass, view.panel_url, warn_if_unknown=False)
                state["panels"].discard(view.key)
                _LOGGER.debug("Ansicht %s ausgeblendet", view.key)
            elif view.key in wanted and view.key not in state["panels"]:
                frontend.async_register_built_in_panel(
                    hass,
                    component_name="iframe",
                    sidebar_title=view.title,
                    sidebar_icon=view.icon,
                    frontend_url_path=view.panel_url,
                    config={"url": f"{URL_BASE}/{view.file}?v={version}"},
                    require_admin=False,
                    update=True,
                )
                state["panels"].add(view.key)
                _LOGGER.debug("Ansicht %s eingeblendet", view.key)

        if available != state["available"]:
            state["available"] = available
            await hass.async_add_executor_job(
                _write_file,
                WWW / "views.json",
                json.dumps({"available": available, "version": version}) + "\n",
            )

    debouncer = Debouncer(
        hass, _LOGGER, cooldown=2, immediate=False, function=_async_sync
    )
    entry.async_on_unload(debouncer.async_shutdown)

    @callback
    def _async_schedule(*_: Any) -> None:
        hass.async_create_task(debouncer.async_call())

    # Neu prüfen, wenn Integrationen hinzukommen/verschwinden oder Geräte sich ändern.
    entry.async_on_unload(
        async_dispatcher_connect(hass, SIGNAL_CONFIG_ENTRY_CHANGED, _async_schedule)
    )
    entry.async_on_unload(
        hass.bus.async_listen(dr.EVENT_DEVICE_REGISTRY_UPDATED, _async_schedule)
    )
    entry.async_on_unload(
        hass.bus.async_listen(er.EVENT_ENTITY_REGISTRY_UPDATED, _async_schedule)
    )
    entry.async_on_unload(entry.add_update_listener(_async_options_updated))

    await _async_sync()
    return True


async def _async_options_updated(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Nach Änderung der Optionen neu laden."""
    await hass.config_entries.async_reload(entry.entry_id)


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Integration entladen und Seitenleisten-Einträge entfernen."""
    state = hass.data.get(DOMAIN, {}).pop(entry.entry_id, None)
    if state:
        for view in VIEWS:
            if view.key in state["panels"]:
                frontend.async_remove_panel(hass, view.panel_url, warn_if_unknown=False)
    return True
