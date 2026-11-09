"""Konstanten für Home Assistant Views."""

from __future__ import annotations

from dataclasses import dataclass

DOMAIN = "ha_views"
URL_BASE = "/ha_views"

CONF_SIDEBAR = "sidebar"
CONF_TOKEN = "token"
# Ansichten, die beim letzten Speichern der Optionen bekannt waren. Neu hinzugekommene
# Ansichten erscheinen dadurch automatisch in der Seitenleiste, bis man sie abwählt.
CONF_KNOWN = "known_views"


@dataclass(frozen=True)
class View:
    """Eine Ansicht und woran erkannt wird, ob sie gebraucht wird."""

    key: str
    file: str
    title: str
    icon: str
    # Ansicht erscheint, wenn eine dieser Integrationen eingerichtet ist …
    domains: tuple[str, ...] = ()
    # … oder eine Entität dieser Art existiert (z. B. irgendein Saugroboter) …
    entity_domains: tuple[str, ...] = ()
    # … oder eine dieser Integrationen per YAML geladen ist …
    components: tuple[str, ...] = ()
    # … oder Zigbee2MQTT-Geräte vorhanden sind.
    zigbee2mqtt: bool = False
    # Immer verfügbar (Übersicht).
    always: bool = False

    @property
    def panel_url(self) -> str:
        """URL-Pfad des Seitenleisten-Eintrags."""
        return f"ha-views-{self.key}"


VIEWS: tuple[View, ...] = (
    View("start", "start.html", "Smart Home", "mdi:home-variant", always=True),
    View(
        "saugroboter",
        "saugroboter.html",
        "Saugroboter",
        "mdi:robot-vacuum",
        domains=("roborock",),
        entity_domains=("vacuum",),
    ),
    View("waesche", "waesche.html", "Wäsche", "mdi:washing-machine", domains=("electrolux_status",)),
    View("fernseher", "fernseher.html", "Fernseher", "mdi:television", domains=("samsungtv",)),
    View("receiver", "receiver.html", "Receiver", "mdi:audio-video", domains=("denonavr",)),
    View(
        "echo",
        "echo.html",
        "Echo",
        "mdi:speaker-wireless",
        domains=("alexa_devices", "alexa_media"),
    ),
    View("ford", "ford-transit.html", "Transit", "mdi:van-utility", domains=("fordpass",)),
    View(
        "gruenbeck",
        "gruenbeck.html",
        "Wasser",
        "mdi:water-opacity",
        domains=("gruenbeck_cloud",),
    ),
    View(
        "abfall",
        "abfall.html",
        "Abfall",
        "mdi:trash-can",
        domains=("waste_collection_schedule",),
        components=("waste_collection_schedule",),
    ),
    View(
        "garten",
        "garten.html",
        "Garten",
        "mdi:sprinkler-variant",
        domains=("garten_bewaesserung",),
    ),
    View(
        "wetter",
        "wetter.html",
        "Wetter",
        "mdi:weather-partly-cloudy",
        domains=("wetter", "dwd_weather_warnings"),
    ),
    View(
        "fritz",
        "fritz.html",
        "FRITZ!Box",
        "mdi:router-wireless",
        domains=("fritz",),
    ),
    View(
        "tanken",
        "tanken.html",
        "Tanken",
        "mdi:gas-station",
        domains=("tankerkoenig",),
    ),
    View(
        "zigbee",
        "zigbee-manager.html",
        "Zigbee",
        "mdi:zigbee",
        domains=("zha",),
        zigbee2mqtt=True,
    ),
)

# Standard: alle Ansichten in der Seitenleiste, außer der Übersicht.
DEFAULT_SIDEBAR: list[str] = [v.key for v in VIEWS if v.key != "start"]

# Ansichten der Version 1.0.0 – für Optionen, die noch ohne CONF_KNOWN gespeichert wurden.
VIEWS_V1: frozenset[str] = frozenset({"start", "saugroboter", "waesche", "fernseher", "receiver", "echo", "ford", "zigbee"})
