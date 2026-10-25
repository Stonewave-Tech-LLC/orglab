# E-xxx: <Name> – Präregistrierung

> **Vor dem ersten Run ausfüllen und committen.** Was danach geändert wird, kommt unten unter "Abweichungen" hinein, mit Datum und Grund. Regeln 10–20 in CLAUDE.md beachten.

- **Datum:** (Uhrzeit aus `date`, nicht schätzen)
- **Stufe:** Entdeckung | Bestätigung (Bestätigung nur auf frischen Seeds, mit gerichteter Vorhersage)
- **Hypothese(n):** H-xxx
- **Konkrete Vorhersage:** Was genau erwarten wir, mit Richtung und grober Größe? Welches Ergebnis würde die Hypothese widerlegen?

## Design
- **Szenario(s) / Material:** inklusive Generator-Commit und Seeds
- **Unabhängige Variable(n)** (Harness/Org-Konfiguration):
- **Konstant gehalten:** Modell, Temperatur, Budget, …
- **Weg, Modell, Einstellung (Regel 11):**
  - Weg: SDK/Abo · OpenRouter/API · Hersteller-CLI
  - Modell: exakte ID
  - Parameter: jeder gesetzte *und* jeder weggelassene, jeweils mit der tatsächlichen Bedeutung beim Anbieter. Beispiel: "ohne `reasoning` = adaptives Reasoning bei Sonnet 5.5 über OpenRouter"
- **Prompts (Regel 16):** exakte Texte aller Zellen als Dry-Run-Anhang, eingefroren
- **Seeds pro Zelle:** · **Gesamtzahl Runs:**

## Manipulationscheck (Pflicht, Regel 10)
- Woran messen wir, dass jede Manipulation das tut, was ihr Name sagt? (Tokens, Werkzeugaufrufe, Promptlänge, …)
- Was gilt, wenn der Check scheitert?

## Material-Leckprüfung (Regel 17)
- Welche Primär-Fehlerarten wären auch *ohne* den manipulierten Faktor entscheidbar? Welcher Test schließt das aus?

## Fremdkontrolle der Ground Truth (Regel 12)
- Wer (Nicht-Claude-Modell oder Neo), welche geschichtete Stichprobe, je Beleg einzeln, blind

## Metriken
- **Primär** (genau eine):
- **Sekundär:**
- **Analyse-Einheit (Regel 13):** Urteil, Beleg, Stapel oder Run? Was hängt zusammen?
- **Prävalenz (Regel 14):** Fehlalarm- und Eskalationszahlen zusätzlich bei 5 % (PPV)
- **Kosten:** Tokens pro Run und pro Erfolg

## Teststärke (Pflicht, D-020)
- Kleinster Effekt, der für Wave/Ace relevant wäre:
- Erwartete Streuung (Quelle, z. B. Vorläufer-Experiment):
- Damit erreichte Power bzw. Breite des Intervalls bei der geplanten Stichprobe (Rechnung oder Simulation, Skript nennen):
- Was ein Null-Ergebnis bei dieser Power aussagt und was nicht:

## Auswertungsplan
- **Statistischer Test / Effektgröße:**
- **Auswerteskript:** Pfad. Vor dem Lauf mit synthetischen Daten getestet und committet (Regel 16).
- **Ausschlusskriterien** (z. B. technisch abgebrochene Runs):
- **Analyse-Freiheitsgrade, vorab festgelegt (Pflicht, D-020).** Jede Zeile beantworten, auch mit "entfällt":
  - Bootstrap: Zahl der Ziehungen, Zufallsstartwert, Quantilmethode (z. B. Perzentil mit linearer Interpolation)
  - Wiederholte Aufrufe: Welcher Versuch zählt (letzter, erster gültiger)?
  - Fehlende Urteile: weglassen, als Fehler zählen oder ganze Einheit ausschließen?
  - Gewichtung: jede Einheit gleich (Beleg, Stapel, Run) oder nach Anzahl?
  - Mindestumfang für eine konfirmatorische Aussage (z. B. vollständige Stapel), sonst nur deskriptiv
  - Ausfälle je Arm berichten (prüfen, ob der Ausfall selbst vom Arm abhängt)
- **Doppelte Buchführung (Regel 19):** Welches Fremdmodell rechnet nach? Was gilt bei Abweichung?
- **Verblindung (Regel 20):** Feld mit dem Arm, Armnamen, und welche Felder den Arm verraten und deshalb aus der verblindeten Kopie entfernt werden. Wie wird der Manipulationscheck gerechnet, ohne zu entblinden?

## Externe Kritik (Regel 18)
- Über 10 $ oder neue Kernthese: Welcher Kritiker (andere Familie) hat Präregistrierung und Code vorher gelesen? Ablage des Gutachtens.

## Abbruchkriterien
- Wann wird abgebrochen (Kosten, offensichtlicher Bug)?
- Was ist bei Abbruch noch berichtbar (vollständige Blöcke)?

## Abweichungen (nach Start)
-
