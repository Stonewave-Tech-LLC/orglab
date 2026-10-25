# E-019 Kalibrierung L1, Material v3 (B=8, Reasoning=low, anthropic/claude-sonnet-5.5)

Aufrufe: 54, Urteile: 432, gültig: 432 (Parse-Ausfall 0.000)

**Einzelfehlerrate: 0.081** · Fehlalarm 0.097 · Übersehen 0.065

Kanalpositionen: 0.083, 0.083, 0.076
Position im Stapel (V8-Vorschau): vordere Hälfte 0.079, hintere Hälfte 0.083

Übersehensrate je Fehlerart: amount_mismatch 0.133, bounced 0.000, cache_down 0.048, column_loss 0.000, db_down 0.133, duplicates_kept 0.000, empty_attachment 0.167, row_loss 0.000, stale_process 0.000, weights_broken 0.083, wrong_recipient 0.000, zero_traffic 0.167
Größter Anteil eines einzelnen Belegs an allen Fehlern: 0.086

## Kriterien

- ✘ 1 Fehlerrate 0,10–0,40
- ✔ 2 Kanalbalance ≤ 0,20
- ✔ 3 Fehlalarm und Übersehen ≥ 0,03
- ✘ 4 ≥ Hälfte der Fehlerarten ≥ 0,05 und kein Beleg > 5 % der Fehler (D-016)
- ✔ 6 Parse-Ausfall ≤ 5 %
- (5 Stichprobe: von Hand, siehe unten)

**Alle automatischen Kriterien erfüllt: NEIN**

## Fehlerrate je Art und Subtilität

- fail_moderate: 0.056
- fail_subtle: 0.074
- ok_clear: 0.130
- ok_noisy: 0.065

Kosten: 0.69 $

## Falsch beurteilte Belege (für die Stichprobe)

- business-ok_clear-1200 · ledger · Slot 1 · Wahrheit ok · Konf. 0.6
- business-fail_moderate-1207 · smtp · Slot 3 · Wahrheit kaputt · Konf. 0.8
- business-ok_noisy-1203 · ledger · Slot 6 · Wahrheit ok · Konf. 0.6
- business-fail_moderate-1200 · smtp · Slot 3 · Wahrheit kaputt · Konf. 0.8
- business-fail_subtle-1208 · smtp · Slot 1 · Wahrheit kaputt · Konf. 0.9
- business-fail_moderate-1211 · smtp · Slot 5 · Wahrheit kaputt · Konf. 0.9
- business-ok_clear-1207 · smtp · Slot 3 · Wahrheit ok · Konf. 0.6
- business-ok_noisy-1211 · smtp · Slot 1 · Wahrheit ok · Konf. 0.8
- research-ok_clear-1202 · joblog · Slot 4 · Wahrheit ok · Konf. 0.8
- coding-fail_subtle-1201 · probe · Slot 7 · Wahrheit kaputt · Konf. 0.7
- coding-fail_subtle-1204 · deploy · Slot 5 · Wahrheit kaputt · Konf. 0.85
- research-ok_noisy-1206 · joblog · Slot 6 · Wahrheit ok · Konf. 0.6
- business-ok_clear-1201 · ledger · Slot 2 · Wahrheit ok · Konf. 0.6
- research-ok_noisy-1206 · output · Slot 6 · Wahrheit ok · Konf. 0.6
- business-fail_subtle-1209 · delivery · Slot 7 · Wahrheit kaputt · Konf. 0.8
- coding-fail_subtle-1203 · probe · Slot 8 · Wahrheit kaputt · Konf. 0.6
- research-ok_noisy-1206 · validation · Slot 6 · Wahrheit ok · Konf. 0.6
- research-fail_subtle-1200 · joblog · Slot 4 · Wahrheit kaputt · Konf. 0.8
- business-fail_subtle-1200 · delivery · Slot 6 · Wahrheit kaputt · Konf. 0.85
- research-ok_clear-1205 · joblog · Slot 4 · Wahrheit ok · Konf. 0.6
- coding-ok_clear-1211 · probe · Slot 2 · Wahrheit ok · Konf. 0.6
- coding-fail_subtle-1200 · deploy · Slot 2 · Wahrheit kaputt · Konf. 0.8
- coding-ok_noisy-1207 · sockets · Slot 4 · Wahrheit ok · Konf. 0.8
- business-ok_clear-1211 · ledger · Slot 4 · Wahrheit ok · Konf. 0.6
- business-ok_noisy-1206 · smtp · Slot 6 · Wahrheit ok · Konf. 0.6
- research-ok_clear-1203 · joblog · Slot 8 · Wahrheit ok · Konf. 0.5
- research-ok_clear-1208 · validation · Slot 1 · Wahrheit ok · Konf. 0.7
- research-ok_clear-1206 · joblog · Slot 6 · Wahrheit ok · Konf. 0.6
- research-ok_clear-1206 · validation · Slot 6 · Wahrheit ok · Konf. 0.6
- business-ok_clear-1206 · ledger · Slot 8 · Wahrheit ok · Konf. 0.6
- coding-ok_clear-1208 · deploy · Slot 4 · Wahrheit ok · Konf. 0.6
- coding-fail_moderate-1210 · probe · Slot 5 · Wahrheit kaputt · Konf. 0.75
- coding-fail_moderate-1210 · deploy · Slot 5 · Wahrheit kaputt · Konf. 0.8
- coding-fail_moderate-1203 · deploy · Slot 2 · Wahrheit kaputt · Konf. 0.8
- research-ok_clear-1210 · joblog · Slot 7 · Wahrheit ok · Konf. 0.6