# Änderungen

Neue Einträge oben. Die Überschrift `## <Version>` muss zu `version` in
`custom_components/ha_views/manifest.json` passen – der Abschnitt wird beim Release
automatisch als Beschreibung übernommen.

## 1.5.0
- Neue Ansicht **Wetter** für [Wetter & Warnungen](https://github.com/SH1FT-W/wetter-warnungen): amtliche Warnungen
  (DWD und NINA) nach Schwere mit Beschreibung und Handlungsempfehlung, aktuelles Wetter, „Regen in X Minuten“,
  48-Stunden-Verlauf mit Temperaturkurve und Niederschlag, 8-Tage-Vorhersage, Pollenflug und UV-Index.

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
