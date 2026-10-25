# E-002: Regime-Vergleich auf `phantom_hard` – Ergebnis

- **Zeitraum:** 2026-10-21, 00:45–~01:40
- **Code:** `3d7ce9c` (Prozessstart) · **Rohdaten:** `daten/E-002-regime-hard/` (40 Runs, 0 Abstürze, 0 Backend-Ausfälle)
- **Auswertung:** `daten/E-002-regime-hard/auswertung.md`

## Ergebnis zu den Vorhersagen

| Vorhersage | Ergebnis |
|---|---|
| 1. `true_completion` liegt unter E-001 | Knapp eingetreten: 0,97–1,00 statt 1,00 |
| 2. `regressions_repaired` streut stärker als `phantoms_diagnosed` | **Eingetreten.** Phantome werden immer erkannt (1,0), Regressionen zu 0,80–1,00 repariert |
| 3. C hat die höchste `regressions_repaired` | **Nicht eingetreten.** Am höchsten liegt D mit 1,00, C mit 0,90 auf Platz zwei |
| Widerlegungskriterium: alle Regime ≥ 0,95 | **Erfüllt, also Decke.** Kein Paarvergleich ist signifikant (alle p ≥ 0,47) |

## Explorative Befunde (n=10 pro Regime, nicht signifikant)

| Regime | true_compl. | Erfolg (alles wahr) | Ticks | Inspektionen | Nachrichten | Output-Tokens |
|---|---|---|---|---|---|---|
| A_contracts | 0,971 | 8/10 | 6,0 | **37,5** (am wenigsten) | 10,8 | 9.827 |
| B_minimal | 0,971 | 8/10 | 5,8 | 52,3 | 17,5 | 10.836 |
| C_stigmergy | 0,979 | 9/10 | 6,2 | **75,4** (am meisten) | 7,8 | 13.698 |
| D_constitution | **1,000** | **10/10** | **4,5** (am schnellsten) | 48,7 | 15,6 | **9.409** (am wenigsten) |

**Lesarten (Hypothesen):**
- **D (Selbstverfassung mit wählbarer Reviewer-Rolle)** ist zugleich das zuverlässigste, schnellste und günstigste Regime. Eine Rolle, die sich ausdrücklich ums Prüfen kümmert, scheint Prüfarbeit effizient zu bündeln (vgl. E-001: Reviewer-Rolle entsteht spontan).
- **C prüft am meisten:** Alle sehen alles und prüfen alles. Das ist teuer, aber nicht besser als D. Geteilte Sichtbarkeit führt eher zu redundanter Prüfung.
- **A prüft am wenigsten** und hat die meisten Falsch-"fertig"-Meldungen (2,9 %). Der Vertrag ("execute, report, message coordinator") lenkt die Aufmerksamkeit aufs Melden, nicht aufs Prüfen.

## Grenzen
- Deckeneffekt, alle Unterschiede liegen innerhalb der Konfidenzintervalle.
- Ohne Last sagt dieses Experiment wenig über Organisationsqualität. Das ist der Anlass für E-003.

## Konsequenzen
- **E-003:** derselbe Vergleich unter knapper Aufmerksamkeit (`phantom_stress`, 4 Calls / 8 Ticks), also dort, wo die Kalibrierung (E-012) einen informativen Bereich gezeigt hat.
