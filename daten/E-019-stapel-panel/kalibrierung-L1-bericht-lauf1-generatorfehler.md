# E-019 Kalibrierung L1 (B=8, Reasoning=low, anthropic/claude-sonnet-5.5)

Aufrufe: 54, Urteile: 432, gültig: 432 (Parse-Ausfall 0.000)

**Einzelfehlerrate: 0.104** · Fehlalarm 0.162 · Übersehen 0.046

Kanalpositionen: 0.090, 0.125, 0.097
Position im Stapel (V8-Vorschau): vordere Hälfte 0.111, hintere Hälfte 0.097

Übersehensrate je Fehlerart: bounced 0.000, db_down 0.273, row_loss 0.056, stale_process 0.000, weights_broken 0.000, wrong_recipient 0.000
Größter Anteil eines einzelnen Belegs an allen Fehlern: 0.067

## Kriterien

- ✔ 1 Fehlerrate 0,10–0,40
- ✔ 2 Kanalbalance ≤ 0,20
- ✔ 3 Fehlalarm und Übersehen ≥ 0,03
- ✘ 4 ≥ 4/6 Fehlerarten ≥ 0,05 und kein Beleg > 5 % der Fehler
- ✔ 6 Parse-Ausfall ≤ 5 %
- (5 Stichprobe: von Hand, siehe unten)

**Alle automatischen Kriterien erfüllt: NEIN**

## Fehlerrate je Art und Subtilität

- fail_moderate: 0.046
- fail_subtle: 0.046
- ok_clear: 0.157
- ok_noisy: 0.167

Kosten: 0.62 $

## Falsch beurteilte Belege (für die Stichprobe)

- business-ok_noisy-1105 · smtp · Slot 1 · Wahrheit ok · Konf. 0.6
- business-ok_clear-1110 · ledger · Slot 2 · Wahrheit ok · Konf. 0.6
- business-ok_noisy-1102 · smtp · Slot 7 · Wahrheit ok · Konf. 0.85
- business-ok_noisy-1107 · delivery · Slot 2 · Wahrheit ok · Konf. 0.5
- business-ok_clear-1100 · ledger · Slot 1 · Wahrheit ok · Konf. 0.6
- business-ok_noisy-1107 · smtp · Slot 2 · Wahrheit ok · Konf. 0.6
- research-ok_noisy-1111 · output · Slot 4 · Wahrheit ok · Konf. 0.5
- coding-ok_noisy-1106 · probe · Slot 7 · Wahrheit ok · Konf. 0.6
- coding-ok_noisy-1101 · probe · Slot 7 · Wahrheit ok · Konf. 0.6
- business-ok_noisy-1111 · smtp · Slot 1 · Wahrheit ok · Konf. 0.9
- research-ok_clear-1102 · joblog · Slot 4 · Wahrheit ok · Konf. 0.6
- research-ok_noisy-1106 · joblog · Slot 6 · Wahrheit ok · Konf. 0.6
- research-ok_noisy-1106 · validation · Slot 6 · Wahrheit ok · Konf. 0.6
- business-ok_clear-1101 · ledger · Slot 2 · Wahrheit ok · Konf. 0.6
- coding-ok_clear-1105 · sockets · Slot 5 · Wahrheit ok · Konf. 0.8
- coding-ok_clear-1100 · deploy · Slot 6 · Wahrheit ok · Konf. 0.6
- research-ok_noisy-1110 · joblog · Slot 7 · Wahrheit ok · Konf. 0.8
- coding-fail_moderate-1106 · deploy · Slot 5 · Wahrheit kaputt · Konf. 0.8
- research-ok_noisy-1110 · output · Slot 7 · Wahrheit ok · Konf. 0.8
- research-ok_noisy-1102 · output · Slot 6 · Wahrheit ok · Konf. 0.85
- coding-fail_subtle-1100 · deploy · Slot 2 · Wahrheit kaputt · Konf. 0.8
- coding-ok_noisy-1103 · probe · Slot 1 · Wahrheit ok · Konf. 0.5
- research-fail_subtle-1111 · output · Slot 5 · Wahrheit kaputt · Konf. 0.7
- business-ok_noisy-1100 · smtp · Slot 1 · Wahrheit ok · Konf. 0.85
- business-ok_noisy-1104 · smtp · Slot 3 · Wahrheit ok · Konf. 0.85
- research-ok_noisy-1108 · output · Slot 7 · Wahrheit ok · Konf. 0.6
- coding-fail_moderate-1100 · deploy · Slot 2 · Wahrheit kaputt · Konf. 0.6
- business-ok_clear-1111 · ledger · Slot 4 · Wahrheit ok · Konf. 0.6
- research-ok_clear-1103 · joblog · Slot 8 · Wahrheit ok · Konf. 0.6
- research-ok_clear-1104 · joblog · Slot 2 · Wahrheit ok · Konf. 0.6
- coding-fail_subtle-1106 · deploy · Slot 3 · Wahrheit kaputt · Konf. 0.8
- business-ok_clear-1105 · ledger · Slot 7 · Wahrheit ok · Konf. 0.6
- coding-fail_subtle-1109 · deploy · Slot 2 · Wahrheit kaputt · Konf. 0.8
- research-ok_clear-1106 · joblog · Slot 6 · Wahrheit ok · Konf. 0.8
- research-ok_clear-1106 · validation · Slot 6 · Wahrheit ok · Konf. 0.8
- business-ok_clear-1106 · ledger · Slot 8 · Wahrheit ok · Konf. 0.6
- coding-ok_clear-1107 · sockets · Slot 1 · Wahrheit ok · Konf. 0.6
- research-ok_clear-1106 · output · Slot 6 · Wahrheit ok · Konf. 0.85
- coding-fail_moderate-1102 · deploy · Slot 7 · Wahrheit kaputt · Konf. 0.8
- coding-ok_clear-1108 · sockets · Slot 4 · Wahrheit ok · Konf. 0.6