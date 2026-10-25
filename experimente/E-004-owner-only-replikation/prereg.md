# E-004: Replikation "Nur der Eigentümer prüft", Präregistrierung (konfirmatorisch)

- **Datum:** 2026-10-21, ~02:00 · **Status:** registriert, Start sofort
- **Anlass:**
  - In E-012 Iteration 2 war die Intervention "nur der Eigentümer prüft, gezielte statt Broadcast-Updates" signifikant schlechter als die ungeregelte Baseline: Δ`true_completion` −0,075, p = 0,015, 10 Paare.
  - Der vermutete Mechanismus: Ohne Kreuzprüfung bleiben Regressionen unentdeckt, die *fremde* Arbeit verursacht (`regressions_repaired` 0,55 → 0,22).
  - Ein einzelner Test unter mehreren Kandidaten kann ein Zufallstreffer sein, deshalb die Replikation mit frischen Seeds.
- **Hypothese H-017 (neu):** Emergente, redundante Kreuzprüfung ist funktional. Normen, die die Prüfung strikt dem Eigentümer zuweisen (Effizienz), senken die Robustheit gegen Regressionen aus fremder Arbeit.

## Konfirmatorische Vorhersagen (gerichtet)
1. **Primär:** `true_completion`(owner_only) < `true_completion`(B_minimal_tight), gepaarter Vorzeichen-Permutationstest, **einseitig α = 0,05**.
2. **Mechanismus:** `regressions_repaired`(owner_only) < Baseline, einseitig α = 0,05.
3. `inspections`(owner_only) < Baseline (Manipulationscheck: Die Norm wirkt tatsächlich auf das Verhalten).

**Widerlegt, wenn:** Vorhersage 1 nicht signifikant ist oder das Vorzeichen sich umkehrt. Dann war E-012 It. 2 ein Zufallsbefund.

## Design
- **Szenario:** `phantom_stress`
- **Domänen:** coding, business **und research**. Research ist für den Optimierer Holdout, hier prüft es die Domänen-Generalität des Effekts.
- **Configs:**
  - `configs/regimes_tight/B_minimal_tight.yaml`
  - `configs/interventions/B_tight_owner_only.yaml`
  - Identisch bis auf die 3 Normen. Diese sind wortgleich aus E-012 It. 2 übernommen.
- **Seeds:** 100–109, frisch und weder im Optimierer noch in E-003 benutzt → 2 × 3 × 10 = **60 Runs**, gepaart nach (Domäne, Seed)
- **Modell:** Sonnet 5.5, effort medium · Concurrency 2

## Auswertung
- Gepaarter Vorzeichen-Permutationstest. Für die einseitige Version wird der p-Wert halbiert, wenn das Vorzeichen der Vorhersage entspricht.
- Effektgröße: mittlere Differenz mit Bootstrap-CI.
- Zusätzlich je Domäne getrennt (explorativ).

## Abweichungen
-
