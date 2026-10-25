# E-004: Replikation "Nur der Eigentümer prüft" – Ergebnis (konfirmatorisch)

- **Zeitraum:** 2026-10-21, 02:05–07:21 (laut Dateizeitstempeln)
- **Unterbrechung:** Session-Limit von 02:23 bis 06:10. Dabei sind 2 Runs nach allen Wiederholungsversuchen gescheitert, sie wurden um ~07:10 mit demselben Befehl nachgeholt. Abweichung vom Plan: nur zeitlich, nicht im Design.
- **Code:** Prozessstart `ebb86a5`, Nachholläufe `6b289d3`. Die Änderungen dazwischen betreffen nicht den Pfad dieses Szenarios bzw. dieser Configs. `item_inspected` loggt seit `ec113a1` zusätzlich `owner`, das ist für die Metriken hier irrelevant.
- **Rohdaten:** `daten/E-004-owner-only-replikation/`, 60 Runs, 30 Paare (Domäne × Seed)

## Ergebnis zu den Vorhersagen (vorab festgelegt, einseitig α = 0,05)

| Vorhersage | Baseline | owner_only | Δ (95%-CI) | p einseitig | Ergebnis |
|---|---|---|---|---|---|
| 1. `true_completion` sinkt | 0,898 | 0,865 | −0,033 (−0,075 bis +0,004) | **0,076** | **nicht bestätigt** |
| 2. `regressions_repaired` sinkt | 0,398 | 0,342 | −0,056 (−0,22 bis +0,12) | 0,27 | nicht bestätigt |
| 3. `inspections` sinkt (Manipulationscheck) | 39,9 | 24,5 | −15,4 (−18,8 bis −11,9) | < 0,001 | bestätigt |

**Nach dem vorab festgelegten Kriterium** ("widerlegt, wenn Vorhersage 1 nicht signifikant") gilt **H-017 als nicht bestätigt**. Der Befund aus E-012 Iteration 2 (Δ −0,075, p = 0,015) hat sich auf frischen Seeds nicht in dieser Stärke gezeigt.

## Einordnung
- **Die Richtung stimmt, die Größe halbiert sich.** Das ist das typische Muster eines überschätzten Entdeckungsbefunds: In E-012 wurde aus mehreren Kandidaten selektiert, und das Paar mit dem stärksten Ausschlag fällt auf. Das ist die Regression zur Mitte, oder der "Fluch des Gewinners".
- **Die Norm wirkt auf das Verhalten** (−39 % Prüfungen), **kaum aber auf das Ergebnis.** Plausibel ist, dass die Hälfte der Prüfungen in der Baseline tatsächlich redundant ist. Die Kreuzprüfung, die wirklich Regressionen fängt, ist ein kleiner Teil davon.
- **Explorativ, je Domäne:** business Δ −0,069 (p = 0,03), coding −0,025, research −0,006. Ein domänenspezifischer Effekt ist möglich, aber nicht vorab festgelegt. Er zählt nur als Kandidat.
- **Aces Einwand passt dazu (H-018):** Im Testbed ist `inspect` immer wahrheitsgemäß, hier sind Redundanz und Pfad-Diversität also dasselbe. Aces Vorschlag ("Prüfpfad-Diversität") würde testen, ob der eigentliche Mechanismus die *andere Beweisart* ist und nicht die zweite Person.

## Grenzen
- n = 30 Paare. Die Teststärke reicht für Effekte ≳ 0,05, kleinere Effekte bleiben unsicher.
- Ein Modell (Sonnet 5.5).
- Kein unabhängiger Kritiker aus einer anderen Modellfamilie. Ace (ebenfalls Claude) hat das Design kommentiert.

## Konsequenzen
- H-017 bekommt den Status **widerlegt (konfirmatorisch nicht repliziert)**, mit Hinweis auf die gleiche Richtung. Eine erneute Prüfung geht nur mit einer neuen, präziseren Hypothese (H-018) und größerem n.
- **Methodische Lehre für den Blog:** Der stärkste Einzelbefund der Nacht ist in der Bestätigungsstufe auf die Hälfte geschrumpft. Ohne die Zwei-Stufen-Regel stünde er jetzt als "Befund" im Laborbuch.

## Nachtrag 2026-10-21 ~17:15: Sensitivitätsanalyse nach Audit
- Der Baseline-Run research/seed-101 hatte 1 fehlerhaften Agenten-Zug (Session-Limit im letzten Tick). Er wurde als ungültig markiert und nachgemessen.
- Neu: Δ −0,035 (CI −0,077 bis +0,002), einseitig **p = 0,061** (vorher 0,076).
- **Die Schlussfolgerung bleibt:** Die Vorhersage ist nicht bestätigt.
