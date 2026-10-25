# E-012: Optimierungslauf auf `phantom_stress` mit knapper Aufmerksamkeit, Präregistrierung

- **Datum:** 2026-10-21, ~01:00 · **Status:** registriert, Start sofort
- **Herkunft:** Folge-Regel aus E-011 (Baseline 0,994 ≥ 0,95)
- **Fragen und Vorhersagen:** wie E-010/E-011.
  - Zusätzlich H-014: Unter knapper Aufmerksamkeit (4 Werkzeugaufrufe pro Tick, 8 Ticks) fällt die Baseline in den informativen Bereich, und organisatorische Änderungen werden messbar.
  - Erwartete Art der Änderungen: Verifikationsarbeit wird **gezielt verteilt** (wer prüft was wann), statt dass alle alles prüfen. Möglich sind auch Rollen (Prüfer, Abschluss-Verantwortlicher) oder ein geteilter Zustand (Board), der doppelte Prüfungen spart.

## Design
Wie E-011, außer:
- **Start-Config:** `configs/regimes/B_minimal_tight.yaml` (`max_tool_calls` 4, `max_ticks` 8, beide für den Editor gesperrt)
- **Dauer:** bis ca. 08:30 (7,4 h)

## Vorab festgelegte Folge-Regel
Ist die Baseline in Iteration 1 erneut ≥ 0,95, wird abgebrochen und mit `max_tool_calls` 3 / `max_ticks` 6 als E-013 neu gestartet. Liegt sie < 0,3 (Bodeneffekt), wird mit `max_tool_calls` 6 / `max_ticks` 8 als E-013 neu gestartet.

## Abweichungen
- **02:23–06:10:** Das Session-Limit hat Iteration 4 unterbrochen (keine gültigen Probes). Um 05:29 ist der Prozess an einem Windows-Temp-Ordner-Bug abgestürzt, behoben in `38c5858`.
- **Ab 07:23 (Zeitstempel verlauf.log):** Fortsetzung mit Neos Zustimmung ("kannst durchziehen").
  - Concurrency 2 statt 4, damit das Abo geschont wird und E-005 parallel läuft.
  - Neue Laufzeit 8 h ab Fortsetzung.
  - Iteration 4 wird komplett neu gemessen. Bereits fertige Runs auf denselben Seeds werden wiederverwendet, abgebrochene neu gestartet.
  - Iterationen ohne gültige Daten zählen ab jetzt nicht mehr als "keine Verbesserung".
