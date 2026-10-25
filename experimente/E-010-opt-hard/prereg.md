# E-010: Erster Optimierungslauf (Nacht), Präregistrierung

- **Datum:** 2026-10-21, ca. 00:40 · **Status:** registriert, Start sofort (parallel zu E-002)
- **Frage:** Findet der Optimierer (Opus 5.5 als Editor, ohne Werkzeuge) ausgehend von einem minimalen Gerüst Organisationsänderungen, die
  1. auf den Trainingsdomänen signifikant helfen und
  2. auf eine ungesehene Domäne übertragbar sind?
- **Hypothesen:** H-005 (Transfer), explorativ H-014.

## Konkrete Vorhersagen
1. Mindestens eine Änderung wird übernommen. Inhaltlich erwartet: ein Mechanismus zur **erneuten Prüfung bereits erledigter Arbeit** (Regressionen), z. B. eine Norm, eine Reviewer-Rolle oder ein Board-Audit.
2. Der Holdout-Δ (research) ist > 0.

**Widerlegt / Nullbefund, wenn:** keine Übernahme stattfindet oder der Holdout-Δ ≤ 0 ist. Beides wird genauso berichtet.

## Design
- **Szenario:** `phantom_hard`
- **Start-Config:** `configs/regimes/B_minimal.yaml`
- **Training:** coding, business, je 5 frische Seeds pro Iteration (gepaarter Vergleich, 10 Paare)
- **Holdout:** research, 5 feste Seeds (900000–900004), alle 2 Iterationen und am Ende
- **Gate:** Δ`true_completion` ≥ 0,02, gepaarter Vorzeichen-Permutationstest p < 0,1, Tokenfaktor ≤ 3
- **Agenten:** Sonnet 5.5, effort medium · **Editor:** Opus 5.5, effort high
- **Concurrency:** 4 · **Dauer:** bis ca. 08:30 (7,75 h), patience 6

## Vorab festgelegte Abbruchregel (Kalibrierung nach D-010)
Liegt die Baseline von B_minimal in Iteration 1 bei einem Mittelwert ≥ 0,95, wird der Lauf abgebrochen und als **E-011 auf `phantom_stress`** neu gestartet (gleiche Einstellungen). Die abgebrochene Iteration bleibt als Kalibrierungsdatum erhalten.

## Grenzen (vorab bekannt)
- Wenige Iterationen in einer Nacht.
- p < 0,1 bei mehreren Kandidaten pro Iteration bedeutet eine erhöhte Falsch-Positiv-Rate. Deshalb ist der Holdout-Test die eigentliche Prüfung.
- Der Editor sieht Ground-Truth-Annotationen in den Traces. Das ist bewusst so (wir haben Verifier, Harness² nicht), muss aber beim Vergleich mit Harness² genannt werden.

## Abweichungen
- **2026-10-21 00:47, Abbruch nach der vorab festgelegten Regel.**
  - Die Baseline von B_minimal in Iteration 1 lag bei `true_completion` 0,986 (10 Runs, 9 × 1,0, 1 × 0,857), also ≥ 0,95. Die Iteration wurde während der Kandidaten-Probes beendet.
  - Erhalten bleiben: Baseline-Runs, Editor-Prompt, Editor-Antwort, Diagnose und beide Kandidaten-Configs (`daten/E-010-opt-hard/iter-001/`).
  - Neustart als E-011 auf `phantom_stress`.
- **Diagnose des Editors** (lohnt die Aufbewahrung, deckt sich mit H-013): *"Each agent confirms an item once, right after executing it. Nobody owns the question of whether the whole set still works once all execution has stopped."* Der einzige Fehlermodus in der Baseline: Die Agenten hören auf ("quiescent"), obwohl noch Falsch-"fertig"-Meldungen offen sind.
