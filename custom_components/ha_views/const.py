"""Konstanten für Home Assistant Views."""

from __future__ import annotations

from dataclasses import dataclass

DOMAIN = "ha_views"
URL_BASE = "/ha_views"

CONF_SIDEBAR = "sidebar"
CONF_TOKEN = "token"


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
