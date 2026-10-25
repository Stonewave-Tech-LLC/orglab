# E-003: Regime-Vergleich unter knapper Aufmerksamkeit, Präregistrierung

- **Datum:** 2026-10-21, ~01:45 · **Status:** registriert, Start sofort (parallel zu E-012)
- **Anlass:**
  - E-001 und E-002 lagen an der Decke.
  - Die Kalibrierung in E-012 zeigt: Unter 4 Calls / 8 Ticks auf `phantom_stress` liegt B_minimal bei 0,88. Das ist informativ.
- **Hypothesen:** H-003, H-007, H-014, H-015, H-016 (neu, siehe unten).

## Konkrete Vorhersagen
Vorhersagen 1 und 2 stützen sich auf die explorative Tendenz aus E-002:
1. D_constitution_tight hat die höchste `true_completion`.
2. C_stigmergy_tight hat die meisten Inspektionen pro Run, aber unter Knappheit **keine** höhere `true_completion` als B (redundante Prüfung kostet Aufmerksamkeit, H-016).
3. A_contracts_tight hat die niedrigste `true_completion` (der Hub-Engpass kostet unter Knappheit Ticks).
4. Die Regime unterscheiden sich in `true_completion` um mindestens 0,05 zwischen bestem und schlechtestem.

**Widerlegt, wenn:** alle Regime innerhalb von 0,03 liegen (Organisation egal, auch unter Last) oder B am besten abschneidet (Struktur schadet nur).

## Design
- **Szenario:** `phantom_stress` (16 Pakete, 4 Phantome, 5 Regressionen)
- **Domänen:** coding, business (research bleibt Holdout)
- **Regime:** `configs/regimes_tight/` A/B/C/D_tight (identisch mit A–D, aber 4 Calls / 8 Ticks)
- **Seeds:** 0–4 → 4 × 2 × 5 = **40 Runs**, Concurrency 2
- **Modell:** Sonnet 5.5, effort medium

## Auswertung
- **Primär:** `true_completion`
- **Sekundär:** `success`, `regressions_repaired`, `false_done_rate`, `inspections`, `messages`, `output_tokens`
- **Statistik:** Permutationstests paarweise, Bonferroni p < 0,0083
- **Emergenz-Analyse** (`orglab.emergence`) als explorativer Teil: Spezialisierung, Rollen

## Abbruch
- Gehäufte Backend-Ausfälle, oder Laufzeit über 4 h.

## Abweichungen
-
