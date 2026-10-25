# E-011: Optimierungslauf auf `phantom_stress`, Präregistrierung

- **Datum:** 2026-10-21, 00:50 · **Status:** registriert, Start sofort
- **Herkunft:** Neustart von E-010 nach dessen Abbruchregel (Baseline 0,986 ≥ 0,95)
- **Frage, Hypothesen, Vorhersagen:** wie E-010. Zusätzliche Vorhersage aus der Editor-Diagnose von E-010: Eine übernommene Änderung wird eine **Zuständigkeit für den Gesamtzustand am Ende** einführen, etwa eine Abschlussprüfung, eine Reviewer- oder Closer-Rolle oder eine Regel "vor dem Aufhören alles prüfen".

## Design
Wie E-010, außer:
- **Szenario:** `phantom_stress` (16 Pakete, 4 Phantome, 5 Regressionen)
- **Dauer:** bis ca. 08:30 (7,6 h)

## Vorab festgelegte Folge-Regel
Liegt die Baseline von B_minimal in Iteration 1 erneut bei ≥ 0,95, wird abgebrochen und als **E-012** neu gestartet:
- Szenario: `phantom_stress`
- Start-Config: `configs/regimes/B_minimal_tight.yaml` (identisch mit B_minimal, aber `max_tool_calls` 4 statt 8 und `max_ticks` 8 statt 10)
- Begründung: Knappe Aufmerksamkeit ist eine realistische Lastform (H-014). Verifikation hat dann Kosten, und die Organisation muss entscheiden, wer was wann prüft.

## Abweichungen
- **2026-10-21 ~01:00, Abbruch nach der Folge-Regel.**
  - Die Baseline von B_minimal in Iteration 1 lag bei 0,994 (10 Runs, 9 × 1,0, 1 × 0,938). Der eine Fehlschlag endete am Tick-Limit (`max_ticks`), mit 2 von 3 reparierten Regressionen. Mehrere Runs brauchten 8–10 von 10 Ticks.
  - Zeit und Aufmerksamkeit werden also schon knapp, Qualität ist nicht das Problem. Das stützt die Wahl der Folgestufe.
  - Neustart als E-012 mit `B_minimal_tight`.
