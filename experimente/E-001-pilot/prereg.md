# E-001: Pilot "Phantom-Fertig" × vier Regime, Präregistrierung

- **Datum:** 2026-10-21 · **Status:** registriert, noch nicht gestartet (wartet auf Neos Login im Agent SDK)
- **Hypothese(n):** primär Messbarkeit, kein Hypothesentest. Explorativ: H-003, H-008.
- **Zweck:**
  1. Trägt die Messung mit echten LLM-Agenten?
  2. Wie groß ist die Varianz pro Zelle?
  3. Welchen Durchsatz erlaubt die Subscription?
  4. Gibt es Bugs im Testbed?
- **Konkrete Erwartungen** (explorativ, nicht als Test gedacht):
  - Die Varianz von `true_completion` zwischen Seeds ist deutlich > 0. Daraus planen wir die Seed-Zahl für E-002.
  - Regime mit Board (C) zeigen weniger `orphans_end` als A und B.
  - Kein Regime erreicht systematisch `phantoms_diagnosed` = 1, denn keines verlangt explizit Wirkungsprüfung.

## Design
- **Szenario:** `phantom_done` (8 Pakete, 2 Phantome)
- **Domänen:** coding, business
- **Unabhängige Variable:** Regime A_contracts, B_minimal, C_stigmergy, D_constitution (`configs/regimes/`)
- **Konstant gehalten:** 4 Agenten, max. 10 Ticks, max. 8 Werkzeugaufrufe pro Tick, Agenten-Prompts englisch
- **Modell:** `claude-sonnet-5-5`, effort `medium`, über das Claude Agent SDK (Subscription)
- **Seeds:** 0–2 pro Zelle → 4 × 2 × 3 = **24 Runs**, Concurrency 2

## Metriken
- **Primär:** `true_completion`
- **Sekundär:** `false_done_rate`, `phantoms_diagnosed`, `built_on_phantom`, `orphans_end`, `messages`, `repeated_messages`, `escalations`, `comm_degree_gini`
- **Kosten/Durchsatz:** `output_tokens`, `wall_s` pro Run, Backend-Ausfälle (`backend_failures.log`)

## Auswertungsplan
- `python -m orglab.analyze daten/E-001-pilot`: Mittelwerte mit Bootstrap-95%-CI je Zelle, paarweise Permutationstests.
- **Alle Vergleiche gelten als explorativ** (n=3 pro Zelle ist zu klein für Inferenz).
- Qualitativ: je Regime zwei Verläufe mit `orglab.digest` lesen und auf Testbed-Artefakte prüfen. Gesucht wird etwa, ob Agenten Werkzeuge missverstehen oder Prompts mehrdeutig sind.
- **Ausschluss:** Runs mit `turn_errors` > 0 werden gesondert berichtet.

## Abbruchkriterien
- Mehr als 3 Backend-Ausfälle hintereinander, ein offensichtlicher Testbed-Bug, oder mehr als 6 h Laufzeit.

## Abweichungen (nach Start)
-
