# E-005: A/A-Test und Positivkontrolle – Ergebnis

- **Zeitraum:** 2026-10-21, ~07:20–08:43 (laut Zeitstempeln)
- **Code:** `d8737c8`
- **Rohdaten:** `daten/E-005-aa-positivkontrolle/`, 60 Runs, 0 Abstürze, 20 Paare je Vergleich

## Ergebnis (vorab festgelegt)

| Prüfung | Kriterium | Ergebnis | Bestanden |
|---|---|---|---|
| A/A `true_completion` | p ≥ 0,05 und \|Δ\| < 0,03 | Δ +0,006 (CI −0,041 bis +0,053), p = 0,90 | ✓ |
| A/A `inspections` | – | Δ +0,5 (CI −3,4 bis +4,6), p = 0,83 | ✓ (keine Verhaltensdrift) |
| Positivkontrolle `true_completion` | einseitig p < 0,01 | 0,903 → 0,378, Δ −0,525 (CI −0,58 bis −0,47), p < 0,001 | ✓ |
| Positivkontrolle `false_done_rate` | steigt | 0,066 → 0,621 | ✓ |
| Manipulationscheck Positivkontrolle | Prüfungen sinken deutlich | 43,9 → 0,85 | ✓ |

**Die Pipeline gilt damit als vertrauenswürdig:** keine Scheineffekte bei identischen Configs, große bekannte Effekte werden sicher erkannt. Eine Nebenbeobachtung ist, dass die Agenten die schädliche Norm fast vollständig befolgen (0,85 Prüfungen statt 44).

## Wichtigster Nebenbefund: das LLM-Rauschen und was es für die Teststärke heißt

Die Standardabweichung der Paar-Differenzen im A/A-Test liegt bei **sd(Δ) = 0,111** (`true_completion`, `phantom_stress`, 4 Calls / 8 Ticks). Daraus ergibt sich der minimal nachweisbare Effekt (MDE, 80 % Power):

| Paare | MDE zweiseitig α = 0,05 | MDE Optimierer-Gate (zweiseitig p < 0,1 und Δ > 0, also einseitig α = 0,05) |
|---|---|---|
| 10 (E-012-Gate) | ±0,098 | **±0,087** |
| 30 (E-004) | ±0,057 | ±0,050 |
| 40 | ±0,049 | ±0,044 |
| 80 | ±0,035 | ±0,031 |

**Konsequenzen:**
1. **Das Gate des Optimierers in E-010 bis E-012 war praktisch blind.**
   - Bei einer Baseline von ~0,88–0,94 ist die maximal mögliche Verbesserung ~0,06–0,12.
   - Das Gate hätte nur Verbesserungen ≳ 0,09 zuverlässig erkannt.
   - Die 4 Iterationen ohne Übernahme in E-012 heißen also **nicht** "es gibt nichts Besseres". Sie heißen "wenn es etwas Besseres gibt, ist es kleiner als ~0,09".
   - Die beobachteten Deltas waren allerdings überwiegend negativ (Mittel aller 8 Kandidaten ≈ −0,03). Das spricht eher gegen große versteckte Gewinne.
2. **E-004 (30 Paare) konnte −0,033 nicht zuverlässig nachweisen** (MDE einseitig ±0,050). Die Nicht-Bestätigung von H-017 ist also auch eine Frage der Teststärke: Der wahre Effekt ist vermutlich kleiner als in der Entdeckung, −0,075 liegt genau am Rand des 95%-CI von E-004, oder er ist null.
3. **Für künftige Bestätigungen:** Effekte um 0,03–0,05 brauchen 40–90 Paare.

## Grenzen
- Rauschschätzung aus einem Szenario und einer Budget-Stufe. In anderen Szenarien kann die Streuung anders sein.

## Konsequenzen
- **D-011:** Das Optimierer-Gate wird adaptiv (sequenzielles Nachmessen vielversprechender Kandidaten).
- E-012 wurde gestoppt, Neustart als E-013 mit dem adaptiven Gate.
- Meine Formulierung im Laborbuch und im Briefing an Ace, "keine Handregel schlägt die ungeregelte Organisation", ist zu stark. Korrekt ist: "keine Handregel mit Effekt ≳ 0,09".
