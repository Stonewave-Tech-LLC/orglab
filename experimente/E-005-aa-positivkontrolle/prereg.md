# E-005: A/A-Test und Positivkontrolle der Pipeline, Präregistrierung

- **Datum:** 2026-10-21, ~07:20
- **Stufe:** Bestätigung (Pipeline-Validierung nach Handoff Teil 3, §3)
- **Frage:** Erzeugt die Pipeline mit echten LLM-Agenten Scheineffekte, und erkennt sie einen bekannten Effekt? Die geskriptete Validierung prüft nur den Auswerter, nicht das LLM-Rauschen.

## Konfirmatorische Vorhersagen
1. **A/A:**
   - `B_minimal_tight` gegen den inhaltsgleichen `B_minimal_tight_AA`, gepaart nach (Domäne, Seed).
   - Zweiseitiger Vorzeichen-Permutationstest auf `true_completion`: **p ≥ 0,05**, und |Δ| < 0,03.
   - Die beobachtete Paar-Streuung dient als Schätzung des LLM-Rauschens für Power-Planung.
2. **Positivkontrolle:**
   - `B_tight_trust_flags` hat Normen, die Prüfen untersagen und sofortiges Melden verlangen.
   - Vorhersage: niedrigere `true_completion` als `B_minimal_tight`, **einseitig p < 0,01**, und höhere `false_done_rate`.
   - Manipulationscheck: `inspections` deutlich niedriger.

**Pipeline gilt als nicht vertrauenswürdig, wenn:** A/A p < 0,05 ergibt oder die Positivkontrolle nicht erkannt wird. Dann werden alle Befunde dieser Nacht zurückgestellt, bis die Ursache gefunden ist.

## Design
- **Szenario:** `phantom_stress`
- **Domänen:** coding, business
- **Configs:** `configs/regimes_tight/B_minimal_tight.yaml`, `configs/controls/B_minimal_tight_AA.yaml`, `configs/controls/B_tight_trust_flags.yaml`
- **Seeds:** 200–209 (frisch) → 3 × 2 × 10 = **60 Runs**
- **Modell:** Sonnet 5.5, effort medium · Concurrency 2

## Abweichungen
-
