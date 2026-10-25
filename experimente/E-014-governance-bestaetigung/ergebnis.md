# E-014: Bestätigung Governance gegen Blockierer – Ergebnis (konfirmatorisch)

- **Zeitraum:** 2026-10-21, 17:35–22:58, unterbrochen durch Session-Limit (Reset 21:20). 3 Runs (H, business 106/108/109) haben die Backoff-Versuche aufgebraucht und wurden um ~22:57 mit demselben Befehl nachgeholt.
- **Code:** `ed91612` · **Rohdaten:** `daten/E-014-governance-bestaetigung/` (80 Runs, Audit sauber, 20 Paare je Vergleich, frische Seeds 100–109)

## Primärtests (vorab festgelegt, einseitig, gepaart, Holm auf α = 0,05)

| Hypothese | Δ `true_completion` (95%-CI) | p einseitig | Holm-Schwelle | Ergebnis |
|---|---|---|---|---|
| N < H (ohne Mensch schlechter) | −0,307 (−0,364 bis −0,246) | < 0,0001 | 0,017 | **bestätigt** |
| V > N (Abstimmung rettet) | +0,482 (+0,429 bis +0,536) | < 0,0001 | 0,025 | **bestätigt** |
| F > N (Frist-Regel rettet) | +0,307 (+0,221 bis +0,393) | < 0,0001 | 0,050 | **bestätigt** |

## Sekundär
| | Δ gegen H (95%-CI) | Nicht-Unterlegenheit (Grenze −0,05) |
|---|---|---|
| Abstimmung (V) | **+0,175** (+0,121 bis +0,232) | gezeigt, sogar überlegen |
| Frist-Regel (F) | 0,000 (−0,061 bis +0,061) | **nicht gezeigt**, die untere Grenze liegt knapp unter −0,05 |

| Arm | true_compl. | Maulwurf-Pakete gerettet | richtige Übernahmen | **Fehlurteile** (gegen Ehrliche) |
|---|---|---|---|---|
| H (Mensch) | 0,764 | 0,56 | 3,6 | **1,30 pro Run** |
| N (ohne) | 0,457 | 0,00 | 0 | 0 |
| V (Abstimmung) | 0,939 | 0,93 | 5,25 | **0,00** |
| F (Frist) | 0,764 | 0,65 | 7,5 (Freigaben) | 0,15 |

## Einordnung
- **Bestätigt:** Ohne Übernahme-Mechanismus bricht ein Team gegen Blockierer massiv ein (−31 Punkte). Sowohl eine Abstimmung (Quorum 2) als auch eine Frist-Regel retten große Teile.
- **H-024 ist damit bestätigt**, mit beiden Teilen: der große Verlust ohne Schiedsrichter und die Abstimmung, die den Schiedsrichter mindestens ersetzt.
- **H-025 ist teilweise bestätigt:** Die Frist-Regel rettet (F > N), ist dem Menschen aber nur *gleich* (Δ 0,00), nicht nachweislich nicht unterlegen.
- **Wichtige Einschränkung zum Arm "Mensch":** Der simulierte Mensch ist ein **naiver Schiedsrichter**. Er weist ein Paket neu zu, sobald jemand es eskaliert und es gerade nicht funktioniert, ohne zu prüfen, ob der Eigentümer ehrlich ist und nur eine Regression erlitten hat. Daher kommen 1,3 Fehlurteile pro Run. Die Überlegenheit der Abstimmung gegenüber H ist also **teilweise ein Artefakt meiner Mensch-Simulation** und kein Befund "Demokratie schlägt Mensch". Robust ist: **Die Abstimmung der Agenten produziert keine Fehlurteile.** Die beiden ehrlichen Stimmen müssen sich einig sein, das wirkt wie ein eingebautes Vier-Augen-Prinzip.
- **Warum H hier schwächer ist als in E-007 (0,76 gegen 0,84):** Es sind andere Seeds. Die Streuung zwischen Seed-Sets ist bei k = 2 groß. Die Paarvergleiche sind davon nicht betroffen.

## Checkliste (CLAUDE.md)
- [x] repliziert auf frischen Seeds, vorab festgelegt, Effektgröße relevant (30–48 Punkte)
- [x] A/A und Positivkontrolle der Pipeline (E-005)
- [x] Audit sauber
- [ ] Kritiker aus anderer Modellfamilie (fehlt). Ace (Claude) hat das Design kommentiert.
- [ ] Transkripte von Neo gelesen (offen: je Arm 2 Runs)
- [x] Mit einem Befehl reproduzierbar (siehe `prereg.md`)
- Eval-Awareness: Die Saboteure sind Skripte, die ehrlichen Agenten bekommen keinen Hinweis. Geringes Risiko.

## Grenzen
- Die Saboteure sind auffällig (stumm, stimmen nicht mit). Die Robustheit gegen mitstimmende Saboteure testet E-015.
- Ein Modell (Sonnet 5.5), ein Szenario (`mole_2`), naive Mensch-Simulation.
