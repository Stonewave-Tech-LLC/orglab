# E-009: Eigentümerwechsel nach Frist (H-013 als Regel), Präregistrierung

- **Datum:** 2026-10-21, 13:51 · **Stufe:** Entdeckung
- **Anlass:**
  - Aus den Wave-Daten (notizen/06) ergibt sich H-013 (liegen bleibt, was keinen Pull-Mechanismus hat).
  - Ace bestätigt (notizen/11), dass es in Wave keine Stufe "Frist überschritten → Eigentümerwechsel" gibt. Die einzige Eskalation geht an den Menschen.
  - E-008 testet Abstimmung. E-009 testet die **unpersönliche Frist-Regel** als Alternative, ohne Menschen und ohne Abstimmung.
- **Regel:** Ein als erledigt gemeldetes Paket, das bei einer Fremdprüfung nicht funktioniert und vom Eigentümer binnen 2 Ticks nicht erneut ausgeführt wird, wird freigegeben. Alle werden informiert, und jeder kann es übernehmen.

## Vorhersagen (explorativ)
1. `true_completion` (B_no_human_deadline) > B_no_human (aus E-008, gleiche Seeds), bei k = 1 und 2.
2. Die Frist-Regel erreicht mindestens das Niveau der Abstimmung (B_no_human_vote, E-008), mit weniger Kommunikationsaufwand. Begründung: Kein Quorum muss organisiert werden.
3. Fehlurteile (`auto_released_from_honest`) treten auf, wenn ehrliche Pakete durch Regressionen kurzzeitig nicht funktionieren. Sie sind aber seltener als Freigaben von Maulwürfen.

## Design
- **Szenario:** `mole_1`, `mole_2`, geskriptete Maulwürfe
- **Config:** `configs/governance/B_no_human_deadline.yaml` (stale_release_ticks 2)
- **Referenzen aus E-008:** B_no_human, B_no_human_vote. Aus E-007: B_minimal mit Mensch.
- **Domänen:** coding, business · **Seeds:** 0–4 → **20 Runs** in `daten/E-009-frist-regel/k1|k2/`
- Sonnet 5.5 · Concurrency 2 · Start nach E-008

## Abweichungen
-
