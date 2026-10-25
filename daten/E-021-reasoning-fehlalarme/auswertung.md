# E-021 Ergebnis (automatisch erzeugt)

Aufrufe: 144, Urteile: 1728, gültig: 1728

- Arm low: 864 Urteile, fehlend 0.000
- Arm aus: 864 Urteile, fehlend 0.000

## Primär

- **FA(low)** = 0.102, **FA(aus)** = 0.032 (ok-Belege: 144)
- **P1** Δ Fehlalarm (low − aus) = **+0.069**, einseitiges 95-%-KI untere Grenze +0.049, Bootstrap-p = 0.0000 → erfüllt (Relevanz ≥ +0,05: ja)
- **Miss(low)** = 0.074, **Miss(aus)** = 0.067 (kaputte Belege: 144)
- **P2** Δ Übersehen (aus − low) = **-0.007**, obere Grenze des einseitigen 95-%-KI +0.007 (Grenze +0,03) → erfüllt
- **H-036: BESTÄTIGT** (P1 und P2 gemeinsam)

## Sekundär

S1: Eskalation bei Konfidenz < 0.80 (Schwelle vorab festgelegt)

| Arm | eskaliert | gefangene Fehler | PPV der Alarme bei 50 % | PPV bei 5 % |
|---|---|---|---|---|
| low | 0.16 | 0.62 | 0.90 | 0.32 |
| aus | 0.10 | 0.37 | 0.97 | 0.60 |

S3: Fehlalarm je Domäne/Kanal

| Domäne/Kanal | low | aus |
|---|---|---|
| business/delivery | 0.000 | 0.000 |
| business/ledger | 0.188 | 0.042 |
| business/smtp | 0.250 | 0.083 |
| coding/deploy | 0.125 | 0.062 |
| coding/probe | 0.042 | 0.021 |
| coding/sockets | 0.083 | 0.000 |
| research/joblog | 0.125 | 0.083 |
| research/output | 0.062 | 0.000 |
| research/validation | 0.042 | 0.000 |

Manipulationscheck, Completion-Tokens je Aufruf: low 255, aus 832
Kosten: 3.19 $

Generatorfehler-Regel: ok-Belege in beiden Armen in allen 3 Kanälen als kaputt beurteilt: keine