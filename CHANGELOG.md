# Änderungen

Neue Einträge oben. Die Überschrift `## <Version>` muss zu `version` in
`custom_components/ha_views/manifest.json` passen – der Abschnitt wird beim Release
automatisch als Beschreibung übernommen.

## 1.7.1
- Verlauf: Zeiträume **3 Monate, 6 Monate, 1 Jahr und 2 Jahre**.
- Die Seite richtet sich nach den tatsächlich gespeicherten Daten – egal ob Standard-Recorder (10 Tage) oder eigene
  Datenbank (z. B. MySQL/MariaDB mit 2 Jahren):
  - bis 30 Tage Rohdaten; reichen sie nicht bis zum Anfang, wird er aus der Langzeit-Statistik ergänzt,
  - darüber Langzeit-Statistik (Stunden-, ab 3 Monaten Tageswerte) für Sensoren mit `state_class`,
    Rohdaten über den ganzen Zeitraum für alle anderen und für Attribut-Serien (bei sehr vielen Punkten verdichtet,
    Spitzen bleiben erhalten),
  - fangen die Werte einer Serie später an als der Zeitraum, steht oben „Daten ab …“.
- `transform` der Karte gilt auch für Statistikwerte. Zeitachse mit Monat/Jahr, lange Zeiträume laden alle 15 Minuten neu.

## 1.7.0
- Neue Ansicht **Verlauf**: zeigt die Diagramme des HA-Dashboards „Verlauf“ (`dashboard-verlauf`, je Ansicht eine
  ApexCharts-Card) groß und zoombar – Achsen, Farben, Transformationen und Zeitraum kommen aus der Karte, Zeitraum
  umschaltbar (6 h bis 30 Tage, ab 10 Tagen aus den Langzeit-Statistiken). Erscheint automatisch, sobald es das
  Dashboard gibt. Anmeldung, hell/dunkel und Mobilansicht wie bei den anderen Seiten.

## 1.6.0
- Neue Ansicht **FRITZ!Box** für die Integration FRITZ!Box Tools: Internetverbindung mit externer IPv4/IPv6 und
  Verbindungsdauer, FRITZ!OS-Version mit Update, Download/Upload live mit Auslastung und Verlauf (3 Stunden),
  WLAN-Netze schaltbar, Gast-WLAN mit QR-Code und neuem Passwort, Geräte im Netz (Suche, online/alle, IP,
  LAN/WLAN, Internetzugang je Gerät, Wake on LAN), Portfreigaben, Rufumleitungen, Leitungswerte (DSL),
  Neu verbinden und Neustart.
- Neue Ansicht **Tanken** für die Integration Tankerkönig: günstigste geöffnete Tankstelle für E5, E10 oder Diesel
  mit Route, alle Tankstellen nach Preis mit Abstand zur günstigsten, Preisverlauf der letzten 24 Stunden und die
  meist günstigste Tageszeit aus den letzten 7 Tagen.

## 1.5.3
- **Mobilansicht in App-Browsern:** Manche Apps ignorieren die Viewport-Angabe, bauen die Seite mit Desktop-Breite auf
  (z. B. 1082 px) und verkleinern sie aufs Display – winzige Desktop-Ansicht. Die Seiten erkennen das jetzt
  (Touch-Gerät, Seite deutlich breiter als das Display), vergrößern sich passend und zeigen die Mobilansicht.
  Das gilt **nur in eingebauten App-Browsern** (Android WebView, iOS-App-Browser): In Chrome, Samsung Internet,
  Firefox und Safari bleibt „Desktop-Website“ eine bewusste Wahl und funktioniert wie gewohnt. Normale Handys,
  Tablets und PCs sind nicht betroffen. Abschaltbar auf der Diagnoseseite („Mobilansicht anpassen“).
- Diagnoseseite zeigt, ob und wie stark angepasst wird.

## 1.5.2
- Neue **Diagnoseseite** (`/ha_views/diagnose.html`, Link unten auf der Übersicht): misst auf dem jeweiligen Gerät Design
  und Mobilansicht (Breite, Zoom, In-App-Browser, Desktop-Modus, System-/HA-Design), erklärt die Ursache im Klartext
  und sendet den Bericht auf Wunsch als Benachrichtigung an Home Assistant.
- **Design je Gerät** wählbar (Automatisch, Hell, Dunkel) – gilt für alle Seiten in diesem Browser bzw. dieser App.
- „Automatisch“ folgt in der Home-Assistant-Oberfläche jetzt dem **Design von Home Assistant** statt dem des Systems.
- Alle Seiten melden ein eigenes dunkles Design an (`color-scheme`), damit App-Browser sie nicht zwangsweise abdunkeln.
- Wetter: Das Warnungs-Popup öffnet sich nicht mehr von selbst, sondern beim Tippen auf eine Warnung oben
  und zeigt dann alle Details (Stufe, Zeitraum, Text, „Was tun?“, Absender, Link). Gilt für alle Warnungen,
  auch die von Wetter & Warnungen.

## 1.5.0
- Neue Ansicht **Wetter** für [Wetter & Warnungen](https://github.com/SH1FT-W/wetter-warnungen): amtliche Warnungen
  (DWD und NINA) nach Schwere mit Beschreibung und Handlungsempfehlung, aktuelles Wetter, „Regen in X Minuten“,
  48-Stunden-Verlauf mit Temperaturkurve und Niederschlag, 8-Tage-Vorhersage, Pollenflug und UV-Index.
- Ist die Integration **DWD Weather Warnings** eingerichtet, erscheinen ihre Warnungen (aktuell und Vorabinformation)
  ebenfalls in der Liste; doppelte Meldungen beider Integrationen werden zusammengefasst. Eine neue aktuelle
  DWD-Warnung öffnet ein **Popup**, bis sie mit „Verstanden“ bestätigt wird. Die Ansicht erscheint auch,
  wenn nur DWD Weather Warnings eingerichtet ist.

## 1.4.0
- Neue Ansicht **Garten** für [Garten-Bewässerung — Score Irrigation](https://github.com/philipp-builder/ha-garten-bewaesserung-integration):
  nächster Lauf mit Minuten je Kreis, Startzeit, „Heute überspringen“, Jetzt bewässern, Not-Aus,
  Pausenhinweis mit Freigabe, Wetter, je Kreis Begründung/Score/Bodenfeuchte, heutige Dauer anpassen,
  Topf-Dosis, Liter/Kosten, Verlauf aus dem Bewässerungskalender und alle weiteren Regler eingeklappt.
- Releases entstehen jetzt automatisch, sobald eine neue Version auf `main` landet.

## 1.3.0
- Die Seiten haben keine eigenen Verbindungseinstellungen mehr (Adresse, Token) – beides kommt von
  Home Assistant. Echo behält „Angezeigte Geräte“, Zigbee seine Schwellwerte und das Zigbee2MQTT-Topic.

## 1.2.0
- Neue Ansicht **Abfall** für Waste Collection Schedule: nächste Abholung, Termine je Abfallart,
  Liste oder Monatskalender.

## 1.1.0
- Neue Ansicht **Wasser** für die Grünbeck-Cloud-Integration.
- Neu hinzugekommene Ansichten erscheinen bei bestehenden Installationen automatisch in der Seitenleiste.

## 1.0.0
- Erste Version: Steuerseiten als HACS-Integration, automatisch in der Seitenleiste.
