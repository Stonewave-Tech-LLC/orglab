# E-002: Regime-Vergleich auf "Phantom-Fertig, schwer" (Regressionen), Präregistrierung

- **Datum:** 2026-10-21, ca. 00:30 · **Status:** registriert, Start nach E-001
- **Anlass:**
  - Der Smoke-Test und die ersten Pilot-Runs zeigen einen Deckeneffekt auf `phantom_done`: Sonnet 5.5 prüft die Wirkung spontan und erreicht 100 % in 2–3 Ticks.
  - `phantom_hard` setzt Last und eine neue Anforderung dazu: 14 Pakete, 3 Phantome, 3 Regressionen. Ein Paket muss nach dem "Fertig" erneut geprüft werden.
- **Hypothesen:**
  - **H-014 (neu):** Organisationsunterschiede zeigen sich bei starken Modellen erst unter Last bzw. bei Anforderungen, die über den einzelnen Agenten hinausgehen, etwa Regressionen in fremder Arbeit. Ohne Last sind alle Regime nahe der Decke.
  - **H-003 (explorativ):** Selbstregulierende Regime (B, C, D) schneiden nicht schlechter ab als explizite Verträge (A).
  - **H-007:** Regime mit gemeinsamem Zustand (C: Board und Notizbuch) reparieren mehr Regressionen.

## Konkrete Vorhersagen
1. Die mittlere `true_completion` über alle Regime liegt unter der von E-001 (Last wirkt).
2. `regressions_repaired` streut zwischen Regimen stärker als `phantoms_diagnosed`.
3. C_stigmergy hat die höchste `regressions_repaired`.

**Widerlegt, wenn:** alle Regime ≥ 0,95 `true_completion` erreichen. Dann gilt die Decke auch hier, und das Szenario muss weiter verschärft werden.

## Design
- **Szenario:** `phantom_hard`
- **Domänen:** coding, business. `research` bleibt als Holdout für E-010 ungesehen.
- **Regime:** A_contracts, B_minimal, C_stigmergy, D_constitution
- **Konstant:** 4 Agenten, 10 Ticks, 8 Werkzeugaufrufe pro Tick, Sonnet 5.5, effort medium
- **Seeds:** 0–4 pro Zelle → 4 × 2 × 5 = **40 Runs**, Concurrency 2

## Metriken
- **Primär:** `true_completion`
- **Sekundär:** `regressions_repaired`, `false_done_rate`, `phantoms_diagnosed`, `inspections`, `messages`, `output_tokens`, `ticks_used`

## Auswertung
- `orglab.analyze` liefert Bootstrap-CIs und paarweise Permutationstests.
- Bei 6 Vergleichen gilt eine Bonferroni-Schwelle von p < 0,0083 für "signifikant". Alles andere wird als Tendenz berichtet.
- Qualitativ: je Regime einen Verlauf mit Regression lesen.

## Abbruch
- Backend-Ausfälle häufen sich, oder die Laufzeit liegt über 3 h.

## Abweichungen
-
