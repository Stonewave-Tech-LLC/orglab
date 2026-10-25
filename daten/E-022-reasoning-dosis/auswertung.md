# E-022 Ergebnis (automatisch erzeugt)

Vollständige Stapel: 24 von 24. Urteile: 3456, gültig: 3456

- Arm low: 864 Urteile, fehlend 0.000
- Arm medium: 864 Urteile, fehlend 0.000
- Arm high: 864 Urteile, fehlend 0.000
- Arm ohne: 864 Urteile, fehlend 0.000

## Manipulationscheck (Bedingung, Regel 10)

Median Completion-Tokens je Aufruf: low 257, medium 257, high 896, ohne 903
Kriterium low < medium < high und high ≥ 1.5 × low → **NICHT bestanden**

## Primär (Cluster-Bootstrap über Stapel, einseitig 95 %)

- **P1** Δ Fehlalarm (low − high) = **+0.044**, untere Grenze +0.025 → erfüllt (Relevanz ≥ +0.05: nein; ok-Belege 144)
- **P2** Δ Übersehen (high − low) = **-0.019**, obere Grenze -0.000 (Grenze +0.03) → erfüllt
- **H-037: Kontrast erfüllt, aber Manipulationscheck gescheitert → H-037 NICHT bestätigt; Befund gilt nur unter der tatsächlichen Manipulation** (P1, P2 und Manipulationscheck gemeinsam)

## Sekundär (vorab festgelegt, nicht konfirmatorisch)

S1 Dosis: Raten je Arm (Mittel über Belege, zweiseitiges 95-%-KI über Stapel)

| Arm | Median-Tokens | Fehlalarm | Übersehen | PPV bei 50 % | PPV bei 5 % |
|---|---|---|---|---|---|
| low | 257 | 0.067 [0.044; 0.094] | 0.062 [0.040; 0.085] | 0.93 | 0.42 |
| medium | 257 | 0.062 [0.039; 0.089] | 0.056 [0.037; 0.073] | 0.94 | 0.44 |
| high | 896 | 0.023 [0.011; 0.038] | 0.044 [0.025; 0.064] | 0.98 | 0.68 |
| ohne | 903 | 0.023 [0.009; 0.040] | 0.051 [0.031; 0.073] | 0.98 | 0.68 |

Erwartung FA(low) > FA(medium) ≥ FA(high): ja

S2 Δ Fehlalarm (ohne − high) = +0.000 [-0.007; +0.007] (E-021-Probe: gleich)

S3 Eskalation bei Konfidenz < 0.80

| Arm | eskaliert | gefangene Fehler |
|---|---|---|
| low | 0.12 | 0.55 |
| medium | 0.14 | 0.41 |
| high | 0.12 | 0.31 |
| ohne | 0.10 | 0.38 |

S4 Fehlalarm je Domäne

| Domäne | low | medium | high | ohne |
|---|---|---|---|---|
| business | 0.118 | 0.104 | 0.049 | 0.049 |
| coding | 0.028 | 0.035 | 0.007 | 0.007 |
| research | 0.056 | 0.049 | 0.014 | 0.014 |

Generatorfehler-Regel: ok-Belege in allen Armen und Kanälen als kaputt beurteilt: keine
Kosten: 6.18 $