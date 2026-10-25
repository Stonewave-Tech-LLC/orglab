# E-017 Kalibrierung, Iteration 3 (anthropic/claude-sonnet-5.5)

Urteile: 360, gültig: 360, unparsbar/Fehler: 0

**Einzelfehlerrate gesamt: 0.031** (Ziel 0,10–0,40)

## Nach Kanal

| Domäne | Kanal | n | Fehlerrate |
|---|---|---|---|
| coding | deploy | 40 | 0.150 |
| coding | probe | 40 | 0.025 |
| coding | sockets | 40 | 0.025 |
| business | smtp | 40 | 0.000 |
| business | delivery | 40 | 0.000 |
| business | ledger | 40 | 0.000 |
| research | joblog | 40 | 0.050 |
| research | output | 40 | 0.025 |
| research | validation | 40 | 0.000 |

Kanalbalance (Position = Kanalindex, über Domänen): 0.033, 0.025, 0.033 → Spanne 0.008 (Ziel ≤ 0,20, also ±0,10)
Spanne über alle 9 Kanäle: 0.150 (nur deskriptiv)

## Nach Art und Subtilität

| Art | subtlety | n | Fehlerrate |
|---|---|---|---|
| fail_moderate | 1 | 90 | 0.011 |
| fail_subtle | 2 | 51 | 0.098 |
| fail_subtle | 3 | 39 | 0.026 |
| ok_clear | 1 | 90 | 0.011 |
| ok_noisy | 2 | 57 | 0.018 |
| ok_noisy | 3 | 33 | 0.061 |

Ok-Belege (Fehlalarm): 0.022 · Fail-Belege (übersehen): 0.039 (beide Ziel ≥ 0,03)

## Nach Fehlerart

- bounced: 0.000
- db_down: 0.389
- none: 0.022
- row_loss: 0.000
- stale_process: 0.000
- weights_broken: 0.000
- wrong_recipient: 0.000

Kosten: 1.04 $

## Falsch beurteilte Urteile (für die Stichprobenprüfung, Kriterium 4)

- coding-ok_noisy-1006 · probe · Wahrheit ok · Konf. 0.6 · 'features\' count on every call (52, 40, 9, 54, 24, 12), which suggests inconsistent behavior, possibly multiple differing instances or nondeterministic config."}'
- coding-fail_moderate-1002 · deploy · Wahrheit kaputt · Konf. 0.8 · 'e, and the app log shows config loaded, db pool ready, and listening on :5000; the main gap is that uptime was only 6s and no external health check was shown."}'
- coding-fail_subtle-1000 · deploy · Wahrheit kaputt · Konf. 0.8 · 'e directory matches v2.3.6-c5768a7, pm2 reports billing-api online, and the app log shows config loaded, db pool ready, and listening on :3000 with no errors."}'
- coding-fail_subtle-1002 · deploy · Wahrheit kaputt · Konf. 0.8 · 's the process online, and the app log shows it listening on :5000 (matching the configured port) with a ready DB pool and Redis connected after one reconnect."}'
- coding-fail_subtle-1002 · sockets · Wahrheit kaputt · Konf. 0.8 · 'rt 5000, with many established client connections and Redis connections, indicating it is serving traffic; the single SYN-SENT to Postgres is a minor concern."}'
- coding-fail_subtle-1003 · deploy · Wahrheit kaputt · Konf. 0.85 · 'assed, release 3.9.7-1b1aad5 deployed, pm2 shows the process online, and the app log shows it listening on :3000 with the db pool ready and redis reconnected."}'
- coding-fail_subtle-1005 · deploy · Wahrheit kaputt · Konf. 0.85 · 'og shows config loaded, db pool ready, and listening on :8080 matching the release PORT=8080; only minor unrelated warnings (slow query, deprecations) appear."}'
- coding-fail_subtle-1006 · deploy · Wahrheit kaputt · Konf. 0.8 · 'ild passed, pm2 shows auth-service online, and the app log shows it listening on :8080 with caches warmed and redis reconnected, matching the configured port."}'
- research-ok_clear-1008 · output · Wahrheit ok · Konf. 0.5 · 'oved 292 rows from 10,009, but the evidence doesn\'t show these were only duplicates, and the weight mean of exactly 1.00 after removal is slightly suspicious."}'
- research-ok_noisy-1001 · joblog · Wahrheit ok · Konf. 0.4 · '.4, "reason": "The chunk rows sum to 33,060 rather than 33,062, so 2 rows appear to be silently lost before dedup, and the output row count is never reported."}'
- research-ok_noisy-1007 · joblog · Wahrheit ok · Konf. 0.6 · ', "reason": "The 20 chunks of 692 rows total 13,840, not 13,846, so 6 rows were apparently never read, and no final row count is logged to confirm the output."}'