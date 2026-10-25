# E-021: Reasoning und Fehlalarme bei der Stapelprüfung – Präregistrierung

- **Datum:** 2026-10-23, ~01:15, vor dem ersten Lauf
- **Stufe:** **Bestätigung**. Frische Seeds 4000–4023, die nie zuvor benutzt wurden. Daten aus der E-019-Kalibrierung werden nicht verwendet.
- **Hypothese:** H-036, "Reasoning erhöht die Fehlalarmrate von Prüfern, ohne ihre Übersehensrate zu senken"
- **Herkunft des Kandidaten:**
  - `notizen/20b` §2: gepaart über identische Belege bei Stapel 12, Δ Fehlalarm (low − aus) +0,12 [0,08; 0,17] auf Material v2 und +0,07 [0,04; 0,12] auf v3. Δ Übersehen −0,01 bzw. +0,03.
  - Grok-Gutachten 2 (`notizen/23b`): der einzige gepaart robuste Befund, er gehört bestätigt.
- **Ausdrücklich:** Dieses Experiment bestätigt den Befund für **Stapelprüfung** (Stapel 12). Über Einzelbelege sagt es nichts (das ist E-020 V6).

## Design
- **Material:** Generator v3.1 (Commit 0328ad3), Seeds 4000–4023 × 3 Domänen × 4 Arten = **288 Belege** (je 72 pro Art, 50 % kaputt)
- **Stapel:** einmal per Seed gemischt (Tag `"e021"`), 24 Stapel zu je 12. Zusammensetzung und Reihenfolge sind in beiden Armen identisch.
- **Zelle:** I1-S0-E0 aus E-019. Drei Prüferpositionen sehen je einen anderen Kanal, also wird jeder Beleg einmal pro Kanal beurteilt, insgesamt 864 Urteile je Arm.
- **Arme (gepaart):**
  - **low:** `reasoning.effort = "low"`
  - **aus:** kein Reasoning-Parameter
- **Prompt, Parser, Wiederholungen:** unverändert aus `orglab/batch.py` (E-019 L2/L3)
- **Modell:** `anthropic/claude-sonnet-5.5` über OpenRouter
- **Umfang:** 24 Stapel × 3 Positionen × 2 Arme = 144 Aufrufe. Kosten ca. 3 $.

## Primärtest (konfirmatorisch)
- **P1:** Δ Fehlalarm = FA(low) − FA(aus) auf Belegebene. Je ok-Beleg wird die Fehlalarmrate über seine 3 Urteile gemittelt, dann die Differenz zwischen den Armen gebildet.
  - **Vorhersage:** Δ > 0
  - **Test:** einseitig, Bootstrap über ok-Belege (10.000 Ziehungen), α = 0,05
  - **Relevanz:** Δ ≥ +0,05
  - **Widerlegt**, wenn die untere Grenze des einseitigen 95-%-KI ≤ 0 ist (kein Effekt nachweisbar) oder die Punktschätzung ≤ 0.
- **P2 (Nicht-Unterlegenheit, gehört zu H-036):** Δ Übersehen = Miss(aus) − Miss(low) auf Belegebene. "Ohne Reasoning übersieht nicht wesentlich mehr" gilt als gezeigt, wenn die obere Grenze des einseitigen 95-%-KI ≤ +0,03 ist.
- **H-036 gilt als bestätigt, wenn P1 und P2 beide erfüllt sind.** Eine Mehrfachkorrektur ist nicht nötig, weil beide Tests gemeinsam Bedingung sind (Intersection-Union-Prinzip).

## Sekundär (vorab festgelegt, nicht konfirmatorisch)
- **S1, Konfidenz-Eskalation mit festgelegter Schwelle 0,80** (gewählt auf E-019 v2 in `notizen/20b` §3):
  - Anteil eskalierter Urteile und Anteil der gefangenen Fehler, je Arm
  - **Erwartung:** Bei höchstens 25 % Eskalation werden mindestens 50 % der Fehler gefangen.
- **S2, Prävalenz 5 %:** PPV der Alarme je Arm, umgewichtet (Methode `notizen/20b` §5). **Erwartung:** PPV(low) < PPV(aus).
- **S3:** Fehlalarm je Domäne und Kanal (wo entsteht der Effekt?)
- **Manipulationscheck:** Completion-Tokens je Aufruf, low > aus
- **Transkripte:** 2 zufällige Stapel-Antworten je Arm in `transkripte.md`, für Neo zum Lesen

## Ausschlüsse und Abbruch
- Aufrufe mit weniger als 95 % geparsten Urteilen werden bis zu zweimal wiederholen (wie E-019). Fehlende Urteile fehlen.
- Fehlen mehr als 5 % der Urteile in einem Arm, wird abgebrochen und die Pipeline repariert.
- Kosten über 8 $ → Abbruch.
- **Generatorfehler-Regel:** Ein ok-Beleg, der in beiden Armen in allen 3 Kanälen als kaputt beurteilt wird, wird von Hand geprüft. Ausgeschlossen wird er nur bei nachweislich falscher Ground Truth. Berichtet wird mit und ohne Ausschluss.

## Auswertung
`python -m orglab.e021 analyze`. Das Skript ist vor dem ersten Lauf committet.

## Offene Schwächen
- Kritiker-Unabhängigkeit: Design, Material und Prüfer sind Claude.
- "Reasoning aus" heißt über OpenRouter, dass kein Parameter gesetzt wird. Was der Anbieter dann genau tut, ist nicht geprüft.
- Die Ground Truth beruht auf der Definition des Generators: "Rauschen ist ok". Ein Teil der Fehlalarme könnte begründete Vorsicht sein (Grok-Gutachten 1, §4b).

## Abweichungen (nach Start)
-
- **23.10., nach dem Lauf:**
  - Die Uhrzeit im Kopf ("~01:15") war geschätzt. Der tatsächliche Commit der Präregistrierung war um 00:43 (a257dbf), also weiterhin vor dem Lauf.
  - **Der Manipulationscheck ist gescheitert:** Ohne Parameter denkt Sonnet adaptiv und mehr als bei `low`. Die Deutung ist in `ergebnis.md` korrigiert, H-036 ist im Wortlaut nicht bestätigt, und H-037 ist neu.
