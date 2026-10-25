# E-017 Kalibrierung, Iteration 3 (anthropic/claude-haiku-5.5)

Urteile: 360, gültig: 360, unparsbar/Fehler: 0

**Einzelfehlerrate gesamt: 0.075** (Ziel 0,10–0,40)

## Nach Kanal

| Domäne | Kanal | n | Fehlerrate |
|---|---|---|---|
| coding | deploy | 40 | 0.175 |
| coding | probe | 40 | 0.125 |
| coding | sockets | 40 | 0.000 |
| business | smtp | 40 | 0.000 |
| business | delivery | 40 | 0.125 |
| business | ledger | 40 | 0.000 |
| research | joblog | 40 | 0.250 |
| research | output | 40 | 0.000 |
| research | validation | 40 | 0.000 |

Kanalbalance (Position = Kanalindex, über Domänen): 0.083, 0.067, 0.075 → Spanne 0.017 (Ziel ≤ 0,20, also ±0,10)
Spanne über alle 9 Kanäle: 0.250 (nur deskriptiv)

## Nach Art und Subtilität

| Art | subtlety | n | Fehlerrate |
|---|---|---|---|
| fail_moderate | 1 | 90 | 0.011 |
| fail_subtle | 2 | 51 | 0.059 |
| fail_subtle | 3 | 39 | 0.051 |
| ok_clear | 1 | 90 | 0.000 |
| ok_noisy | 2 | 57 | 0.228 |
| ok_noisy | 3 | 33 | 0.242 |

Ok-Belege (Fehlalarm): 0.117 · Fail-Belege (übersehen): 0.033 (beide Ziel ≥ 0,03)

## Nach Fehlerart

- bounced: 0.000
- db_down: 0.333
- none: 0.117
- row_loss: 0.000
- stale_process: 0.000
- weights_broken: 0.000
- wrong_recipient: 0.000

Kosten: 0.08 $

## Falsch beurteilte Urteile (für die Stichprobenprüfung, Kriterium 4)

- coding-ok_noisy-1001 · deploy · Wahrheit ok · Konf. 0.6 · 'led every 24m and every 2m; i18n cache warmed at 2875 and 8110 keys), which suggests duplicate or mixed-config instances rather than one clean v4.6.5 process."}'
- coding-ok_noisy-1001 · probe · Wahrheit ok · Konf. 0.6 · 'onfig/public calls returned different feature counts (59 vs 18), suggesting mixed or inconsistent instances, so the new version may not be serving everywhere."}'
- coding-ok_noisy-1005 · probe · Wahrheit ok · Konf. 0.6 · 'ealth timeout, fluctuating feature counts (27, 52, 13), and metric totals dropping (384 to 153) suggest restarts or mixed instances, so stability is unproven."}'
- coding-ok_noisy-1006 · probe · Wahrheit ok · Konf. 0.6 · '/api/v1/config/public returns a different feature count on nearly every request (52, 40, 9, 54, 24, 12), indicating inconsistent behavior that is unexplained."}'
- coding-ok_noisy-1008 · probe · Wahrheit ok · Konf. 0.6 · 'that vary between requests (14, 53, 5, 46), suggesting inconsistent or mixed backends, and /version was checked only once, so the full rollout is unconfirmed."}'
- coding-ok_noisy-1009 · deploy · Wahrheit ok · Konf. 0.6 · 'flags loaded four times with different counts, and no version confirmation, which suggests duplicate or conflicting startup rather than a clean v2.8.9 deploy."}'
- coding-fail_moderate-1002 · deploy · Wahrheit kaputt · Konf. 0.85 · 'nline, and the app log confirms config loaded, the DB pool ready, and listening on :5000, though the 6s uptime is short and the log doesn\'t print the version."}'
- coding-fail_subtle-1000 · deploy · Wahrheit kaputt · Konf. 0.8 · 'roduction, and the DB pool and caches initialized, though the repeated feature-flag loads with differing counts and multiple \'sync\' schedules are unexplained."}'
- coding-fail_subtle-1002 · deploy · Wahrheit kaputt · Konf. 0.6 · ' and the app is listening on port 5000, but the log shows conflicting scheduled-job intervals for the same job and a Redis reconnect, which warrant follow-up."}'
- coding-fail_subtle-1005 · deploy · Wahrheit kaputt · Konf. 0.8 · ' logged \'config loaded (env=production)\' and \'listening on :8080\' with no errors, though the only warnings are non-fatal and no explicit health check was run."}'
- coding-fail_subtle-1005 · probe · Wahrheit kaputt · Konf. 0.6 · 'ks pass after warm-up, but the fluctuating feature counts, the initial health timeout, and the db_pool showing 20 waiting with 0 active warrant investigation."}'
- coding-fail_subtle-1006 · deploy · Wahrheit kaputt · Konf. 0.7 · 'ed, though the duplicate \'sync\' job schedules, two \'products\' cache warms, and two feature-flag loads suggest a possible double initialization worth checking."}'
- business-ok_noisy-1003 · delivery · Wahrheit ok · Konf. 0.8 · 'so delivered to about 20 unrelated mailboxes at other domains, so the send was not limited to the intended recipient and exposed the invoice to third parties."}'
- business-ok_noisy-1004 · delivery · Wahrheit ok · Konf. 0.8 · ' about 20 unrelated mailboxes at other companies, so the send was not limited to the intended billing contact and likely exposed the invoice to third parties."}'
- business-ok_noisy-1006 · delivery · Wahrheit ok · Konf. 0.8 · '9), but the same invoice was also delivered to about 20 unrelated mailboxes at other companies, so the send was not properly scoped to the intended recipient."}'
- business-ok_noisy-1008 · delivery · Wahrheit ok · Konf. 0.8 · 'irmed delivered to j.berger@huber-bau.de, but the same send also delivered to about 20 unrelated customer mailboxes, a misdirected disclosure of billing data."}'
- business-ok_noisy-1009 · delivery · Wahrheit ok · Konf. 0.7 · 'k.at received the invoice (tracking 098145B7D0), but the same run also delivered messages to about 20 unrelated external mailboxes, an unintended side effect."}'
- research-ok_noisy-1000 · joblog · Wahrheit ok · Konf. 0.6 · 'he log shows 20 chunks of 1,443 rows (28,860 total), but the raw file has 28,870, so 10 rows are unaccounted for and the output\'s row count is never reported."}'
- research-ok_noisy-1001 · joblog · Wahrheit ok · Konf. 0.35 · 'chunks total 33,060 rows against the 33,062 read, and the job never reports the post-dedupe row count or weight mean, so the output\'s integrity is unverified."}'
- research-ok_noisy-1002 · joblog · Wahrheit ok · Konf. 0.7 · 'ws, not the 18,307 in the raw file, so 7 rows are unaccounted for, and the log never confirms the final row count or that weights remain normalised to mean 1."}'
- research-ok_noisy-1004 · joblog · Wahrheit ok · Konf. 0.75 · '17,310 rows, not the 17,314 in the raw file, so 4 rows are unaccounted for, and the log shows no check that the weights still have mean 1 after deduplication."}'
- research-ok_noisy-1003 · joblog · Wahrheit ok · Konf. 0.7 · 'e ten chunks total 21,750 rows, not the 21,759 in the raw file, so 9 rows appear to have been lost during reading, which goes beyond removing duplicates only."}'
- research-ok_noisy-1005 · joblog · Wahrheit ok · Konf. 0.6 · '2,480, not the 32,489 raw rows, so 9 rows are unaccounted for, and the log never confirms the final row count (expected 32,352 after dropping 137 duplicates)."}'
- research-ok_noisy-1007 · joblog · Wahrheit ok · Konf. 0.6 · 'f 692 rows total 13,840, not the 13,846 raw rows, so 6 rows appear unaccounted for, and the log never reports the final row count written to clean/d9.parquet."}'
- research-ok_noisy-1008 · joblog · Wahrheit ok · Konf. 0.8 · ' rows total 25,700, not the 25,703 raw rows, so 3 rows appear to have been silently lost before deduplication, which violates the duplicates-only requirement."}'
- research-ok_noisy-1006 · joblog · Wahrheit ok · Konf. 0.6 · ' "Ten chunks of 3,701 rows total 37,010, not the 37,015 raw rows, so 5 rows are unaccounted for, which suggests unintended data loss beyond duplicate removal."}'
- research-ok_noisy-1009 · joblog · Wahrheit ok · Konf. 0.6 · 's total 12,080, not the 12,099 raw rows, so 19 rows appear unaccounted for, and the log never confirms the output row count or that weights remain normalised."}'