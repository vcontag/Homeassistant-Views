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
| Wasser (Grünbeck) | Grünbeck Cloud (`gruenbeck_cloud`) eingerichtet ist |
| Abfall | Waste Collection Schedule (`waste_collection_schedule`) eingerichtet ist – über die Oberfläche oder per YAML |
| Garten | Garten-Bewässerung — Score Irrigation (`garten_bewaesserung`) eingerichtet ist |
| Wetter | Wetter & Warnungen (`wetter`) oder DWD Weather Warnings (`dwd_weather_warnings`) eingerichtet ist |
| FRITZ!Box | FRITZ!Box Tools (`fritz`) eingerichtet ist |
| Tanken | Tankerkönig (`tankerkoenig`) eingerichtet ist |
| Verlauf | es ein Dashboard mit der Adresse `dashboard-verlauf` gibt |
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
  Neu hinzugekommene Ansichten (nach einem Update) werden automatisch eingeblendet und lassen sich hier abwählen.
- **Festes Zugriffstoken (optional)** – nur nötig für Handy-Verknüpfungen außerhalb der
  HA-Oberfläche (z. B. angeheftete Verknüpfungen der Companion-App oder als Chrome-App).
  In der Seitenleiste nutzen die Seiten automatisch deine normale Anmeldung.
  Die Seiten selbst haben keine eigenen Verbindungseinstellungen mehr – Adresse und Anmeldung kommen von Home Assistant.
  ⚠️ Das Token ist im lokalen Netz ohne Anmeldung abrufbar – nur verwenden, wenn
  Home Assistant nicht aus dem Internet erreichbar ist.

## Design und Diagnose

Die Seiten folgen in der Home-Assistant-Oberfläche dem Design von Home Assistant, sonst dem des Geräts. Passt auf
einem Gerät etwas nicht (z. B. dunkel oder keine Mobilansicht in einem App-Browser), die Seite
`/ha_views/diagnose.html` **auf diesem Gerät** öffnen (Link unten auf der Übersicht). Sie zeigt die Ursache, lässt
das Design für dieses Gerät fest auf Hell oder Dunkel stellen und schickt den Bericht auf Wunsch an Home Assistant.
Rechnet der eingebaute Browser einer App mit Desktop-Breite, passen sich die Seiten automatisch an und zeigen trotzdem
die Mobilansicht (abschaltbar auf der Diagnoseseite). In normalen Browsern bleibt „Desktop-Website“ wählbar.

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

Änderungen je Version stehen im [CHANGELOG](CHANGELOG.md). Releases entstehen automatisch, sobald eine neue
Version (`manifest.json`) auf `main` landet.

HACS meldet neue Versionen. Nach dem Update Home Assistant neu starten.
Die Seiten werden ohne langes Caching ausgeliefert, Änderungen sind also sofort sichtbar.

## Wasser (Grünbeck)

Angelehnt an die Grünbeck-App: großer Kreis mit der Restkapazität, Status (betriebsbereit, Regeneration mit
aktuellem Schritt, Störung), Betriebsart (Eco/Comfort/Power/Individuell) und **Regeneration starten**.
Darunter Salzreichweite, Durchfluss, Wasserhärte, Regenerationen, ein Verbrauchsdiagramm für Wasser und Salz
(7 oder 30 Tage), Wartung, Installateur und Meldungen. Alle weiteren Einstellungen der Anlage
(Regenerationszeiten, Härte, Benachrichtigungen …) sind unter „Einstellungen“ eingeklappt.
Voraussetzung ist die Integration [Grünbeck Cloud](https://github.com/p0l0/hagruenbeck_cloud).

## Abfall (Waste Collection Schedule)

Oben die **nächste Abholung** mit Kalenderblatt, Abfallarten als farbige Tonnen und dem Hinweis
„Heute Abend rausstellen“ bzw. „Heute ist Abholung“. Darunter je Abfallart der nächste Termin – ein Tipp
darauf filtert die Terminliste auf diese Art. Die **Termine** gibt es als Liste (nach Monaten) oder als
Monatskalender. Über ↻ werden die Termine bei der Abfallwirtschaft neu abgerufen. Die Sensoren der
Integration sind unter „Sensoren“ eingeklappt.

Die Termine kommen aus den Kalendern der Integration; gibt es keinen, aus den Attributen der Sensoren.
Die Farben werden am Namen erkannt (Restmüll, Bio, Papier, Gelber Sack/Wertstoff, Glas, Grünschnitt,
Sperrmüll, Schadstoffe), alle anderen Arten bekommen eine feste eigene Farbe.
Bei mehreren Adressen lässt sich oben zwischen ihnen umschalten.
Voraussetzung ist die Integration [Waste Collection Schedule](https://github.com/mampfes/hacs_waste_collection_schedule).

## Garten (Score Irrigation)

Für die Integration [Garten-Bewässerung — Score Irrigation](https://github.com/philipp-builder/ha-garten-bewaesserung-integration).
Oben der **nächste Lauf** mit geplanten Minuten je Kreis, Startzeit, „Heute überspringen“, **Jetzt bewässern**
und **Not-Aus**. Ist die Bewässerung pausiert (Urlaub/Winterpause), erscheint ein Hinweis mit **Freigeben**.
Darunter Wetter (Temperatur, Regen, Vorhersage, ET₀) und je Kreis: die Begründung der Engine („Score 76 → 16 min“),
Score, Bodenfeuchte mit Veto-Schwelle bzw. Sollband (Töpfe), Vetos wie „Regen erwartet“, die heutige Dauer
zum Anpassen, Kreis an/aus, bei Töpfen **Dosis jetzt geben** und Dosen/Liter/Kosten. Der **Verlauf** zeigt die
Läufe und Dosen der letzten 14 Tage aus dem Bewässerungskalender. Alle weiteren Regler (Pausen, Bodensensor-Betrieb,
Schwellen, Boost …) sind unter „Einstellungen“ eingeklappt.

## Wetter (Wetter & Warnungen)

Für die Integration [Wetter & Warnungen](https://github.com/SH1FT-W/wetter-warnungen). Ganz oben die **amtlichen Warnungen**
(DWD und NINA), nach Schwere gefärbt; ein Tipp öffnet ein Popup mit Beschreibung, Handlungsempfehlung und Absender. Ohne Warnung
steht „Keine Warnungen“ mit dem Warngebiet. Darunter das aktuelle Wetter mit „Regen in X Minuten“, Wind, Luftfeuchte,
Druck und Sicht, die nächsten 48 Stunden mit Temperaturkurve und Niederschlag, die Vorhersage für 8 Tage sowie
Pollenflug und UV-Index. Die Vorhersage aktualisiert sich live.

Ist zusätzlich die Integration **DWD Weather Warnings** eingerichtet, kommen ihre Warnungen für die eingestellte
Warnregion mit in die Liste (Vorabinformationen gekennzeichnet); auch sie zeigen ihre Details im Popup.
Ist nur DWD Weather Warnings eingerichtet, zeigt die Seite nur die Warnungen.

## FRITZ!Box (FRITZ!Box Tools)

Status der Internetverbindung mit externer IP (antippen kopiert sie), Verbindungsdauer und FRITZ!OS-Version samt
Update-Knopf. Download und Upload live in Mbit/s mit Auslastung und Verlauf der letzten 3 Stunden. WLAN-Netze an/aus,
Gast-WLAN mit QR-Code und „Neues Passwort“. Die Geräte im Netz mit Suche und Filter, IP, LAN/WLAN, Internetzugang je
Gerät (wenn in der Integration Profile aktiv sind) und Wake on LAN. Dazu Portfreigaben, Rufumleitungen, Leitungswerte
und **Neu verbinden** / **Neustart** (jeweils mit Rückfrage). Bei mehreren Boxen (Mesh) lässt sich oben umschalten.

## Tanken (Tankerkönig)

Kraftstoff wählen (E5, E10, Diesel). Oben die **günstigste geöffnete Tankstelle** mit Preis wie an der Säule und
Route, darunter alle Tankstellen nach Preis mit Abstand zur günstigsten in Cent. Der **Preisverlauf** zeigt die letzten
24 Stunden je Tankstelle; aus den letzten 7 Tagen errechnet die Seite, zu welcher Tageszeit es meist am günstigsten war.

## Verlauf (Diagramme aus einem Dashboard)

Zeigt die Diagramme des Dashboards **„Verlauf“** (Adresse `dashboard-verlauf`) seitenfüllend und zoombar. Jede Ansicht
des Dashboards mit einer **ApexCharts-Card** wird ein Diagramm; Serien, Farben, Achsen, Transformationen, Zeitraum
(`graph_span`) und Aktualisierung kommen aus der Karte – Änderungen also einfach in Home Assistant an der Karte machen.
Oben Diagramm und Zeitraum wählen (6 h bis 2 Jahre). Über 10 Tage kommen die Werte aus den Langzeit-Statistiken
von Home Assistant (ab 3 Monaten als Tageswerte); dafür braucht der Sensor eine `state_class` (z. B. `measurement`),
sonst reicht er nur 10 Tage zurück und ist mit „nur 10 Tage“ gekennzeichnet. URL-Parameter: `d=<Ansicht>`, `h=<Stunden>`, `kopf=0` (ohne Kopfzeile, z. B. für eine
Webseiten-Karte), `dash=<anderes Dashboard>`.
