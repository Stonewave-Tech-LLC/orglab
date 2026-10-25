# E-017 Stufe 0 (Kalibrierung): nicht erfüllt, kein Hauptlauf

- **Datum:** 2026-10-22
- **Rohdaten:** `daten/E-017-faktorielles-panel/kalibrierung-{1,2,3}*.jsonl`, Berichte `kalibrierung-*-bericht.md`
- **Kosten:** 2,37 $ (Sonnet 0,59 + 0,66 + 1,04; Haiku 0,08)
- **Material:** Seeds 1000–1009 × 3 Domänen × 4 Arten = 120 Belege. Jeder Kanal wurde einzeln beurteilt, also 360 Urteile pro Iteration.

## Ergebnis je Iteration

| Iteration | Änderung am Generator | Sonnet-Fehlerrate | Kanalbalance (Spanne) | Fehlalarm / Übersehen |
|---|---|---|---|---|
| 1 | Ausgangsversion | 0,094 | 0,017 | 0,078 / 0,111 |
| 2 | Rauschen bereinigt (siehe unten), Coding- und Business-Spuren subtiler, Research-Auftrag nennt die Gewichtsnorm | 0,031 | 0,017 | 0,006 / 0,056 |
| 3 | 20–40 Routinezeilen pro Kanal (realistische Loglänge), `fail_moderate` ohne explizite Fehlermeldungen | 0,031 | 0,008 | 0,022 / 0,039 |
| 3 (Haiku 5.5) | wie 3 | 0,075 | 0,017 | 0,117 / 0,033 |

**Kriterium 1 (Fehlerrate 0,10–0,40) wurde in keiner Iteration erreicht.** Kanalbalance und Parsebarkeit (0 Ausfälle) waren immer erfüllt. Laut Präregistrierung heißt das: **kein Hauptlauf, neu planen.**

## Stichprobenprüfung (Kriterium 4): drei Generatorfehler gefunden
1. **Iteration 1:** Das "harmlose" Research-Rauschen veränderte tatsächlich Daten ("212 values set to NaN", "set to NaT"). Bei einem Auftrag "remove duplicates only" hatte Sonnet recht, das als Fehler zu werten. 17 von 34 Fehlern waren also keine.
2. **Iteration 1:** Die Prozentzahl im Output-Rauschen war falsch berechnet (212 Nullwerte ≠ 0,9 %).
3. **Iteration 3:** Die Chunk-Zeilen summierten sich nicht zur Rohzeilenzahl (Rundung). Sonnet bemerkte die 2–6 fehlenden Zeilen. Behoben, mit Regressionstest.

Die Modelle lagen in diesen Fällen richtig, der Generator falsch. Das ist dieselbe Lehre wie aus dem E-016-Pilot.

## Was trotzdem interpretierbar ist (explorativ)
- **Sonnet 5.5 liest synthetische Betriebslogs fast fehlerfrei.** Das gilt auch für einen einzelnen Kanal, 40 Routinezeilen Rauschen und Spuren, die nur im Abgleich mit dem Auftrag sichtbar sind (Commit-Hash, ein fehlender Buchstabe in der Adresse, Zeilenzahl).
- **Die verbleibenden echten Fehler konzentrieren sich auf eine einzige Spurart:** "db pool ready (0/20)" bzw. Pool aktiv 0 bei "status ok", mit 39 % Fehlerrate in Iteration 3. Alle anderen Fehlerarten liegen bei 0 %. Das passt zu HK-A4 (Fehler und damit auch gemeinsame Fehler sitzen auf wenigen bestimmten Items) und zu Chen 2606.27288 (β wird von wenigen Items bestimmt).
- **Haiku irrt anders als Sonnet:** vor allem Fehlalarme bei harmlosem Rauschen (23 % bei `ok_noisy`), kaum übersehene Fehler.

## Konsequenz
Ein Panel-Experiment zur Fehlerkorrelation braucht einen Fehler*mechanismus*, den starke Modelle tatsächlich haben. Mehr Text allein reicht nicht. Optionen siehe Laborbuch 22.10. Entscheidung durch Neo, danach neue Präregistrierung bzw. dokumentierte Neuplanung.
