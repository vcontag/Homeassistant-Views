# Home Assistant Views

Handyfreundliche Steuerseiten für Home Assistant – als Integration über HACS installierbar.
Jede Ansicht erscheint **automatisch** in der Seitenleiste, sobald die passende Integration
eingerichtet ist, und verschwindet wieder, wenn du sie entfernst.

| Ansicht | Erscheint, wenn … |
|---|---|
| Smart Home (Übersicht) | immer – zeigt Kacheln zu allen verfügbaren Ansichten |
| Saugroboter | Roborock eingerichtet ist oder ein Saugroboter (`vacuum.*`) existiert |
| Wäsche | Electrolux Status (AEG/Electrolux) eingerichtet ist |
| Fernseher | Samsung Smart TV eingerichtet ist |
| Receiver | Denon AVR eingerichtet ist |
| Echo | Alexa Devices oder Alexa Media Player eingerichtet ist |
| Transit | FordPass eingerichtet ist |
| Zigbee | ZHA eingerichtet ist oder Zigbee2MQTT-Geräte vorhanden sind |

Die Seiten passen sich hellem und dunklem Design an, sind für das Handy optimiert und
lassen sich auf Android als eigene App installieren.

## Installation über HACS

1. HACS öffnen → Menü (⋮) → **Benutzerdefinierte Repositories**.
2. Repository `https://github.com/vcontag/Homeassistant-Views`, Typ **Integration**, hinzufügen.
3. **Home Assistant Views** in HACS suchen und herunterladen.
4. Home Assistant neu starten.
5. Einstellungen → Geräte & Dienste → **Integration hinzufügen** → **Home Assistant Views**.

Fertig – die passenden Ansichten stehen danach in der Seitenleiste.

## Einstellungen

Über **Konfigurieren** bei der Integration:

- **In der Seitenleiste anzeigen** – welche Ansichten einen eigenen Eintrag bekommen.
  Es erscheinen trotzdem nur die, deren Integration vorhanden ist. Abgewählte Ansichten
  bleiben über die Übersicht „Smart Home“ erreichbar.
- **Festes Zugriffstoken (optional)** – nur nötig für Handy-Verknüpfungen außerhalb der
  HA-Oberfläche (z. B. angeheftete Verknüpfungen der Companion-App oder als Chrome-App).
  In der Seitenleiste nutzen die Seiten automatisch deine normale Anmeldung.
  ⚠️ Das Token ist im lokalen Netz ohne Anmeldung abrufbar – nur verwenden, wenn
  Home Assistant nicht aus dem Internet erreichbar ist.

## Direkt aufrufen / als App installieren

Die Seiten liegen unter `http://<deine-ha-adresse>:8123/ha_views/`, z. B.
`/ha_views/start.html` oder `/ha_views/saugroboter.html`.

- **Companion-App:** Einstellungen → Companion-App → Verknüpfungen verwalten →
  angeheftete Verknüpfung mit Pfad `/ha_views/start.html` (öffnet ohne Adressleiste).
- **Chrome auf Android:** Seite öffnen → Menü → „App installieren“
  (ohne HTTPS mit Adressleiste).

## Umstieg von den Dateien im `www`-Ordner

Wer die Seiten bisher unter `/local/` genutzt hat, kann die alten Dateien aus `config/www`
löschen und Verknüpfungen von `/local/…` auf `/ha_views/…` ändern.

## Updates

HACS meldet neue Versionen. Nach dem Update Home Assistant neu starten.
Die Seiten werden ohne langes Caching ausgeliefert, Änderungen sind also sofort sichtbar.
