# E-019 Kalibrierung L1, Material v3 (B=8, Reasoning=low, anthropic/claude-sonnet-5.5)

Aufrufe: 54, Urteile: 432, gültig: 432 (Parse-Ausfall 0.000)

**Einzelfehlerrate: 0.106** · Fehlalarm 0.116 · Übersehen 0.097

Kanalpositionen: 0.125, 0.104, 0.090
Position im Stapel (V8-Vorschau): vordere Hälfte 0.111, hintere Hälfte 0.102

Übersehensrate je Fehlerart: amount_mismatch 0.000, bounced 0.000, cache_down 0.048, column_loss 0.000, db_down 0.200, duplicates_kept 0.000, empty_attachment 0.125, row_loss 0.000, stale_process 0.000, weights_broken 0.083, wrong_recipient 0.000, zero_traffic 0.542
Größter Anteil eines einzelnen Belegs an allen Fehlern: 0.065

## Kriterien

- ✔ 1 Fehlerrate 0,10–0,40
- ✔ 2 Kanalbalance ≤ 0,20
- ✔ 3 Fehlalarm und Übersehen ≥ 0,03
- ✘ 4 ≥ Hälfte der Fehlerarten ≥ 0,05 und kein Beleg > 5 % der Fehler (D-016)
- ✔ 6 Parse-Ausfall ≤ 5 %
- (5 Stichprobe: von Hand, siehe unten)

**Alle automatischen Kriterien erfüllt: NEIN**

## Fehlerrate je Art und Subtilität

- fail_moderate: 0.102
- fail_subtle: 0.093
- ok_clear: 0.130
- ok_noisy: 0.102

Kosten: 0.68 $

## Falsch beurteilte Belege (für die Stichprobe)

- business-ok_noisy-1203 · smtp · Slot 6 · Wahrheit ok · Konf. 0.4
- business-ok_clear-1210 · smtp · Slot 2 · Wahrheit ok · Konf. 0.6
- business-ok_noisy-1203 · ledger · Slot 6 · Wahrheit ok · Konf. 0.6
- business-ok_noisy-1205 · smtp · Slot 1 · Wahrheit ok · Konf. 0.6
- coding-fail_moderate-1201 · sockets · Slot 5 · Wahrheit kaputt · Konf. 0.6
- business-ok_noisy-1202 · smtp · Slot 7 · Wahrheit ok · Konf. 0.5
- business-ok_clear-1200 · ledger · Slot 1 · Wahrheit ok · Konf. 0.6
- business-ok_clear-1209 · ledger · Slot 2 · Wahrheit ok · Konf. 0.55
- coding-fail_moderate-1208 · probe · Slot 5 · Wahrheit kaputt · Konf. 0.6
- business-fail_moderate-1200 · smtp · Slot 3 · Wahrheit kaputt · Konf. 0.8
- coding-fail_moderate-1204 · probe · Slot 1 · Wahrheit kaputt · Konf. 0.8
- coding-ok_noisy-1206 · deploy · Slot 7 · Wahrheit ok · Konf. 0.6
- coding-ok_clear-1209 · deploy · Slot 6 · Wahrheit ok · Konf. 0.55
- business-ok_clear-1207 · smtp · Slot 3 · Wahrheit ok · Konf. 0.6
- business-fail_subtle-1208 · smtp · Slot 1 · Wahrheit kaputt · Konf. 0.9
- business-fail_moderate-1211 · smtp · Slot 5 · Wahrheit kaputt · Konf. 0.9
- coding-fail_subtle-1201 · probe · Slot 7 · Wahrheit kaputt · Konf. 0.88
- coding-fail_subtle-1204 · deploy · Slot 5 · Wahrheit kaputt · Konf. 0.85
- coding-fail_subtle-1203 · deploy · Slot 8 · Wahrheit kaputt · Konf. 0.6
- business-ok_clear-1201 · ledger · Slot 2 · Wahrheit ok · Konf. 0.6
- research-ok_noisy-1206 · output · Slot 6 · Wahrheit ok · Konf. 0.6
- coding-fail_subtle-1203 · probe · Slot 8 · Wahrheit kaputt · Konf. 0.65
- research-ok_noisy-1206 · validation · Slot 6 · Wahrheit ok · Konf. 0.6
- coding-fail_subtle-1203 · sockets · Slot 8 · Wahrheit kaputt · Konf. 0.5
- coding-ok_noisy-1202 · sockets · Slot 3 · Wahrheit ok · Konf. 0.8
- research-fail_subtle-1200 · joblog · Slot 4 · Wahrheit kaputt · Konf. 0.8
- coding-fail_subtle-1211 · deploy · Slot 3 · Wahrheit kaputt · Konf. 0.75
- research-ok_clear-1205 · joblog · Slot 4 · Wahrheit ok · Konf. 0.6
- research-ok_noisy-1202 · joblog · Slot 6 · Wahrheit ok · Konf. 0.55
- coding-fail_subtle-1211 · probe · Slot 3 · Wahrheit kaputt · Konf. 0.8
- coding-fail_subtle-1200 · deploy · Slot 2 · Wahrheit kaputt · Konf. 0.8
- coding-fail_moderate-1200 · deploy · Slot 2 · Wahrheit kaputt · Konf. 0.8
- business-ok_clear-1211 · ledger · Slot 4 · Wahrheit ok · Konf. 0.6
- business-ok_noisy-1206 · smtp · Slot 6 · Wahrheit ok · Konf. 0.6
- business-ok_noisy-1204 · ledger · Slot 3 · Wahrheit ok · Konf. 0.6
- business-ok_clear-1211 · smtp · Slot 4 · Wahrheit ok · Konf. 0.6
- research-ok_clear-1206 · joblog · Slot 6 · Wahrheit ok · Konf. 0.7
- business-ok_clear-1206 · ledger · Slot 8 · Wahrheit ok · Konf. 0.6
- coding-ok_clear-1208 · sockets · Slot 4 · Wahrheit ok · Konf. 0.6
- coding-fail_moderate-1210 · probe · Slot 5 · Wahrheit kaputt · Konf. 0.8