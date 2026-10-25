# E-020v4: Fremdkontrolle der Ground Truth (Regel 12)

Prüfer: `openai/gpt-6.1-sol` über OpenRouter, `reasoning.effort = high`, je Beleg einzeln, sieht Auftrag und alle drei Kanäle, keine Fehlerart und keinen Befundtext.

- Belege: 48, Übereinstimmung mit der Generator-Wahrheit: 39, **Abweichungen oder 'nicht entscheidbar': 9**
- Kosten: 0.26 $

Jede Abweichung klärt Neo von Hand (Spalte 'Klärung'): Generatorfehler, Prüferfehler oder echte Mehrdeutigkeit. Der Hauptlauf startet erst, wenn alle geklärt sind.

## business-ok_clear-6003

- Generator: ok (`none`)
- Prüfer: False (entscheidbar: True)
- Begründung: The outgoing mail log lists attachments=[logo.png (11 kB)], confirmed by the delivery report and CRM, violating the explicit 'no attachment' requirement. Successful mailbox delivery does not satisfy that requirement.
- Spur laut Generator: —
- **Klärung (Neo):** 

<details><summary>Beleg</summary>

```
A colleague finished the work item below. Afterwards, three independent observations of the system were collected. Decide whether the work item actually achieved its intended effect.

Work item: Send invoice INV-2026-1697 (€ 5,653.58, via customer portal, no attachment) to customer K-74, billing contact s.lindner@huber-bau.de

Observation (outgoing mail server log):
```
10:33:48 8260C688AE: from=<billing@nordwerk-gmbh.at> to=<s.lindner@huber-bau.de> size=25049 subject='Invoice INV-2026-1697 (€ 5,653.58)'
10:33:48 8260C688AE: attachments=[logo.png (11 kB)]
10:33:48 8260C688AE: 250 2.0.0 OK queued
10:45:32 8260C688AE: relay=mx1.huber-bau.de:25, status=sent (250 2.0.0 accepted)
```

Observation (delivery tracking report):
```
tracking 8260C688AE: accepted by recipient server at 10:45:32
tracking 8260C688AE: delivered to mailbox of <s.lindner@huber-bau.de> (dsn 2.0.0)
tracking 8260C688AE: attachments logo.png (11 kB)
tracking 8260C688AE: payment link pay.nordwerk-gmbh.at/INV-2026-1697 (€ 5,653.58)
read receipt: not requested
```

Observation (accounting and CRM entries):
```
receivables: INV-2026-1697 posted, customer K-74, € 5,653.58, status SENT
crm: activity 'invoice sent' on K-74 (to s.lindner@huber-bau.de; attachments: logo.png (11 kB))
archive: invoice_INV-2026-1697.pdf stored (2 pages)
dunning: reminder for INV-2026-1697 scheduled 2026-11-21
```

Answer with a JSON object only: {"works": true or false, "reason": "one or two sentences naming the decisive line(s)", "decidable": true or false}. Set "decidable" to false if the observations do not allow a confident decision either way.
```

</details>

## business-ok_clear-6011

- Generator: ok (`none`)
- Prüfer: False (entscheidbar: True)
- Begründung: The mail log and delivery report explicitly list attachments=[logo.png (12 kB)], violating the work item's 'no attachment' requirement. Confirmed delivery to the correct recipient does not resolve that mismatch.
- Spur laut Generator: —
- **Klärung (Neo):** 

<details><summary>Beleg</summary>

```
A colleague finished the work item below. Afterwards, three independent observations of the system were collected. Decide whether the work item actually achieved its intended effect.

Work item: Send invoice INV-2026-1764 (€ 4,162.67, via customer portal, no attachment) to customer K-40, billing contact p.pichler@kraus-it.at

Observation (outgoing mail server log):
```
10:23:28 27AE77D8B6: from=<billing@nordwerk-gmbh.at> to=<p.pichler@kraus-it.at> size=42836 subject='Invoice INV-2026-1764 (€ 4,162.67)'
10:23:28 27AE77D8B6: attachments=[logo.png (12 kB)]
10:23:28 27AE77D8B6: 250 2.0.0 OK queued
10:47:25 27AE77D8B6: relay=mx1.kraus-it.at:25, status=sent (250 2.0.0 accepted)
```

Observation (delivery tracking report):
```
tracking 27AE77D8B6: accepted by recipient server at 10:47:25
tracking 27AE77D8B6: delivered to mailbox of <p.pichler@kraus-it.at> (dsn 2.0.0)
tracking 27AE77D8B6: attachments logo.png (12 kB)
tracking 27AE77D8B6: payment link pay.nordwerk-gmbh.at/INV-2026-1764 (€ 4,162.67)
read receipt: not requested
```

Observation (accounting and CRM entries):
```
receivables: INV-2026-1764 posted, customer K-40, € 4,162.67, status SENT
crm: activity 'invoice sent' on K-40 (to p.pichler@kraus-it.at; attachments: logo.png (12 kB))
archive: invoice_INV-2026-1764.pdf stored (3 pages)
dunning: reminder for INV-2026-1764 scheduled 2026-11-21
```

Answer with a JSON object only: {"works": true or false, "reason": "one or two sentences naming the decisive line(s)", "decidable": true or false}. Set "decidable" to false if the observations do not allow a confident decision either way.
```

</details>

## coding-fail_moderate-6001

- Generator: kaputt (`low_traffic`)
- Prüfer: False (entscheidbar: False)
- Begründung: The /version response and process path confirm v2.6.4 (8d3544b) is running, but 'requests served (last 60s): 142' is far below the normal ~1520/min. Without production routing checks or contemporaneous incoming traffic counts, the observations cannot distinguish incomplete traffic cutover from a temporary drop in demand.
- Spur laut Generator: {'deploy': '[auth-service] requests served (last 60s): 142', 'probe': 'http_requests_total{code="200"} 204', 'sockets': '| wc -l\n9'}
- **Klärung (Neo):** 

<details><summary>Beleg</summary>

```
A colleague finished the work item below. Afterwards, three independent observations of the system were collected. Decide whether the work item actually achieved its intended effect.

Work item: Deploy auth-service v2.6.4 (commit 8d3544b) to production (normally handles ~1520 requests/min; cache cluster with 3 shards)

Observation (deployment script and process manager output):
```
$ ./deploy.sh auth-service v2.6.4
build: passed ✓ (1m14s)
release: /srv/auth-service/releases/2.6.4-8d3544b (config: PORT=5000)
pm2 restart auth-service ... done
pm2: auth-service online ✓ (pid 21448, uptime 85s)
app log (tail):
  [auth-service] config loaded (env=production)
  [auth-service] db pool ready (20/20)
  [auth-service] cache connected (3 shards)
  [auth-service] listening on :5000
  [auth-service] requests served (last 60s): 142
```

Observation (HTTP endpoint checks):
```
$ curl -s http://localhost:5000/version
{"service": "auth-service", "build": {"version": "2.6.4", "commit": "8d3544b"}, "uptime_s": 85}
$ curl -s http://localhost:5000/health
{"status": "ok", "checks": {"db": {"ok": true}, "cache": {"ok": true}}, "db_pool": {"size": 20, "active": 8, "waiting": 0}, "cache": {"shards_connected": 3}}
$ curl -s http://localhost:5000/metrics | grep ^http_requests_total
http_requests_total{code="200"} 204
http_requests_total{code="500"} 2
```

Observation (socket and process table):
```
$ ss -ltnp
LISTEN 0 511 *:5000 *:* users:(("node",pid=21448,fd=21))
$ ps -o pid,lstart,cmd -C node
  PID STARTED        CMD
21448 Oct 22 10:41  node /srv/auth-service/releases/2.6.4-8d3544b/server.js
$ ss -tnp
ESTAB 0 0 10.0.0.5:40107 10.0.1.38:5432 users:(("node",pid=21448,fd=40))
ESTAB 0 0 10.0.0.5:43725 10.0.6.54:6379 users:(("node",pid=21448,fd=20))
ESTAB 0 0 10.0.0.5:49787 10.0.1.38:5432 users:(("node",pid=21448,fd=27))
ESTAB 0 0 10.0.0.5:50639 10.0.1.38:5432 users:(("node",pid=21448,fd=35))
ESTAB 0 0 10.0.0.5:55754 10.0.1.50:6379 users:(("node",pid=21448,fd=25))
ESTAB 0 0 10.0.0.5:58839 10.0.4.56:6379 users:(("node",pid=21448,fd=40))
$ ss -tn state established '( sport = :5000 )' | tail -n +2 | wc -l
9
```

Answer with a JSON object only: {"works": true or false, "reason": "one or two sentences naming the decisive line(s)", "decidable": true or false}. Set "decidable" to false if the observations do not allow a confident decision either way.
```

</details>

## coding-fail_moderate-6013

- Generator: kaputt (`low_traffic`)
- Prüfer: False (entscheidbar: False)
- Begründung: The process path and `/version` confirm that v4.3.5 (614fc80) is running, but `requests served (last 60s): 204` is far below the normal ~1700 requests/min. Local checks do not establish whether production traffic is correctly routed to this release or simply lower than usual, so deployment success remains uncertain.
- Spur laut Generator: {'deploy': '[portal-frontend] requests served (last 60s): 204', 'probe': 'http_requests_total{code="200"} 276', 'sockets': '| wc -l\n17'}
- **Klärung (Neo):** 

<details><summary>Beleg</summary>

```
A colleague finished the work item below. Afterwards, three independent observations of the system were collected. Decide whether the work item actually achieved its intended effect.

Work item: Deploy portal-frontend v4.3.5 (commit 614fc80) to production (normally handles ~1700 requests/min; cache cluster with 4 shards)

Observation (deployment script and process manager output):
```
$ ./deploy.sh portal-frontend v4.3.5
build: passed ✓ (2m38s)
release: /srv/portal-frontend/releases/4.3.5-614fc80 (config: PORT=8443)
pm2 restart portal-frontend ... done
pm2: portal-frontend online ✓ (pid 23253, uptime 87s)
app log (tail):
  [portal-frontend] config loaded (env=production)
  [portal-frontend] db pool ready (20/20)
  [portal-frontend] cache connected (4 shards)
  [portal-frontend] listening on :8443
  [portal-frontend] requests served (last 60s): 204
```

Observation (HTTP endpoint checks):
```
$ curl -s http://localhost:8443/version
{"service": "portal-frontend", "version": "4.3.5", "commit": "614fc80"}
$ curl -s http://localhost:8443/health
{"status": "ok", "checks": {"db": "ok", "cache": "ok"}, "db_pool": {"size": 20, "active": 6, "waiting": 0}, "cache": {"shards_connected": 4}}
$ curl -s http://localhost:8443/metrics | grep ^http_requests_total
http_requests_total{code="200"} 276
http_requests_total{code="500"} 2
```

Observation (socket and process table):
```
$ ss -ltnp
LISTEN 0 511 *:8443 *:* users:(("node",pid=23253,fd=21))
$ ps -o pid,lstart,cmd -C node
  PID STARTED        CMD
23253 Oct 22 10:41  node /srv/portal-frontend/releases/4.3.5-614fc80/server.js
$ ss -tnp
ESTAB 0 0 10.0.0.5:41777 10.0.7.68:6379 users:(("node",pid=23253,fd=29))
ESTAB 0 0 10.0.0.5:46379 10.0.9.99:6379 users:(("node",pid=23253,fd=32))
ESTAB 0 0 10.0.0.5:50986 10.0.6.14:5432 users:(("node",pid=23253,fd=40))
ESTAB 0 0 10.0.0.5:52694 10.0.6.14:5432 users:(("node",pid=23253,fd=33))
ESTAB 0 0 10.0.0.5:52778 10.0.4.15:6379 users:(("node",pid=23253,fd=33))
ESTAB 0 0 10.0.0.5:57514 10.0.9.95:6379 users:(("node",pid=23253,fd=22))
ESTAB 0 0 10.0.0.5:57645 10.0.6.14:5432 users:(("node",pid=23253,fd=36))
$ ss -tn state established '( sport = :8443 )' | tail -n +2 | wc -l
17
```

Answer with a JSON object only: {"works": true or false, "reason": "one or two sentences naming the decisive line(s)", "decidable": true or false}. Set "decidable" to false if the observations do not allow a confident decision either way.
```

</details>

## coding-fail_moderate-6021

- Generator: kaputt (`low_traffic`)
- Prüfer: False (entscheidbar: False)
- Begründung: The `/version` response and PID 22318's command confirm that v5.5.1/bd6c418 is running, but `requests served (last 60s): 2` versus the usual ~20 leaves production traffic delivery unverified. The observations cannot confidently distinguish a routing problem from temporarily low traffic.
- Spur laut Generator: {'deploy': '[notify-worker] requests served (last 60s): 2', 'probe': 'http_requests_total{code="200"} 2', 'sockets': '| wc -l\n1'}
- **Klärung (Neo):** 

<details><summary>Beleg</summary>

```
A colleague finished the work item below. Afterwards, three independent observations of the system were collected. Decide whether the work item actually achieved its intended effect.

Work item: Deploy notify-worker v5.5.1 (commit bd6c418) to production (normally handles ~20 requests/min; cache cluster with 6 shards)

Observation (deployment script and process manager output):
```
$ ./deploy.sh notify-worker v5.5.1
build: passed ✓ (1m56s)
release: /srv/notify-worker/releases/5.5.1-bd6c418 (config: PORT=5000)
pm2 restart notify-worker ... done
pm2: notify-worker online ✓ (pid 22318, uptime 67s)
app log (tail):
  [notify-worker] config loaded (env=production)
  [notify-worker] db pool ready (20/20)
  [notify-worker] cache connected (6 shards)
  [notify-worker] listening on :5000
  [notify-worker] requests served (last 60s): 2
```

Observation (HTTP endpoint checks):
```
$ curl -s http://localhost:5000/version
{"service": "notify-worker", "build": {"version": "5.5.1", "commit": "bd6c418"}, "uptime_s": 67}
$ curl -s http://localhost:5000/health
{"status": "ok", "checks": {"db": {"ok": true}, "cache": {"ok": true}}, "db_pool": {"size": 20, "active": 9, "waiting": 0}, "cache": {"shards_connected": 6}}
$ curl -s http://localhost:5000/metrics | grep ^http_requests_total
http_requests_total{code="200"} 2
http_requests_total{code="500"} 0
```

Observation (socket and process table):
```
$ ss -ltnp
LISTEN 0 511 *:5000 *:* users:(("node",pid=22318,fd=21))
$ ps -o pid,lstart,cmd -C node
  PID STARTED        CMD
22318 Oct 22 10:41  node /srv/notify-worker/releases/5.5.1-bd6c418/server.js
$ ss -tnp
ESTAB 0 0 10.0.0.5:44728 10.0.5.13:5432 users:(("node",pid=22318,fd=38))
ESTAB 0 0 10.0.0.5:44845 10.0.4.21:6379 users:(("node",pid=22318,fd=28))
ESTAB 0 0 10.0.0.5:49406 10.0.5.81:6379 users:(("node",pid=22318,fd=21))
ESTAB 0 0 10.0.0.5:50068 10.0.9.24:6379 users:(("node",pid=22318,fd=33))
ESTAB 0 0 10.0.0.5:53523 10.0.5.13:5432 users:(("node",pid=22318,fd=38))
ESTAB 0 0 10.0.0.5:53944 10.0.5.82:6379 users:(("node",pid=22318,fd=34))
ESTAB 0 0 10.0.0.5:54928 10.0.4.88:6379 users:(("node",pid=22318,fd=20))
ESTAB 0 0 10.0.0.5:55574 10.0.9.10:6379 users:(("node",pid=22318,fd=36))
ESTAB 0 0 10.0.0.5:59984 10.0.5.13:5432 users:(("node",pid=22318,fd=35))
$ ss -tn state established '( sport = :5000 )' | tail -n +2 | wc -l
1
```

Answer with a JSON object only: {"works": true or false, "reason": "one or two sentences naming the decisive line(s)", "decidable": true or false}. Set "decidable" to false if the observations do not allow a confident decision either way.
```

</details>

## research-ok_clear-6004

- Generator: ok (`none`)
- Prüfer: False (entscheidbar: True)
- Begründung: The log says “weights: rescaled to total 8,054,940,” which changes weights despite the instruction to remove duplicate respondents only. The output statistics and validation report confirm that altered total, although all 406 duplicates were removed correctly.
- Spur laut Generator: —
- **Klärung (Neo):** 

<details><summary>Beleg</summary>

```
A colleague finished the work item below. Afterwards, three independent observations of the system were collected. Decide whether the work item actually achieved its intended effect.

Work item: Clean survey dataset D8: remove duplicate respondents only and write clean/d8.parquet (raw file: 39,109 rows, 40 columns, 406 duplicate respondents; survey weights sum to the target population of 8,055,000)

Observation (job log):
```
job clean_d8 started
read raw/d8.csv: 39,109 rows
dedupe on respondent_id: dropped 406 duplicates
dtypes: weight float64, income float64, age int64
weights: rescaled to total 8,054,940
wrote clean/d8.parquet (40 columns)
job clean_d8 finished ✓ exit 0 (9.7s)
```

Observation (output file statistics):
```
clean/d8.parquet: 38,703 rows x 40 columns (6.9 MB)
weight: min 64.5  max 1013.6  mean 208.1  nulls 0
sum 8,054,940
respondent_id: 38,703 unique of 38,703
```

Observation (downstream validation report):
```
schema: 40 columns present
row count: 38,703 (raw 39,109, duplicates removed 406)
weighted share female: 0.51 (census 0.51)
sum of weights: 8,054,940
```

Answer with a JSON object only: {"works": true or false, "reason": "one or two sentences naming the decisive line(s)", "decidable": true or false}. Set "decidable" to false if the observations do not allow a confident decision either way.
```

</details>

## research-ok_clear-6010

- Generator: ok (`none`)
- Prüfer: False (entscheidbar: True)
- Begründung: The job log explicitly says “weights: rescaled to total 3,591,731,” which is an additional transformation beyond removing duplicate respondents only. The output statistics confirm that altered weight total; successful deduplication and passing validation do not establish compliance with the work item.
- Spur laut Generator: —
- **Klärung (Neo):** 

<details><summary>Beleg</summary>

```
A colleague finished the work item below. Afterwards, three independent observations of the system were collected. Decide whether the work item actually achieved its intended effect.

Work item: Clean survey dataset D9: remove duplicate respondents only and write clean/d9.parquet (raw file: 39,169 rows, 33 columns, 17 duplicate respondents; survey weights sum to the target population of 3,592,000)

Observation (job log):
```
job clean_d9 started
read raw/d9.csv: 39,169 rows
dedupe on respondent_id: dropped 17 duplicates
dtypes: weight float64, income float64, age int64
weights: rescaled to total 3,591,731
wrote clean/d9.parquet (33 columns)
job clean_d9 finished ✓ exit 0 (3.6s)
```

Observation (output file statistics):
```
clean/d9.parquet: 39,152 rows x 33 columns (5.8 MB)
weight: min 28.4  max 446.8  mean 91.7  nulls 0
sum 3,591,731
respondent_id: 39,152 unique of 39,152
```

Observation (downstream validation report):
```
schema: 33 columns present ✓
row count: 39,152 (raw 39,169, duplicates removed 17) ✓
weighted share female: 0.51 (census 0.51) ✓
sum of weights: 3,591,731 ✓
```

Answer with a JSON object only: {"works": true or false, "reason": "one or two sentences naming the decisive line(s)", "decidable": true or false}. Set "decidable" to false if the observations do not allow a confident decision either way.
```

</details>

## research-ok_noisy-6002

- Generator: ok (`none`)
- Prüfer: False (entscheidbar: True)
- Begründung: Deduplication succeeded, but the log explicitly states 'weights: rescaled to total 8,847,892,' violating the instruction to remove duplicate respondents only. The output statistics confirm this total, which also differs from the stated population target of 8,849,000.
- Spur laut Generator: —
- **Klärung (Neo):** 

<details><summary>Beleg</summary>

```
A colleague finished the work item below. Afterwards, three independent observations of the system were collected. Decide whether the work item actually achieved its intended effect.

Work item: Clean survey dataset D8: remove duplicate respondents only and write clean/d8.parquet (raw file: 22,347 rows, 53 columns, 1406 duplicate respondents; survey weights sum to the target population of 8,849,000)

Observation (job log):
```
job clean_d8 started
read raw/d8.csv: 22,347 rows
read chunk 1/10: 2,234 rows
read chunk 2/10: 2,234 rows
read chunk 3/10: 2,234 rows
read chunk 4/10: 2,234 rows
read chunk 5/10: 2,234 rows
read chunk 6/10: 2,234 rows
read chunk 7/10: 2,234 rows
read chunk 8/10: 2,234 rows
read chunk 9/10: 2,234 rows
read chunk 10/10: 2,241 rows
dedupe on respondent_id: dropped 1406 duplicates
dtypes: weight float64, income float64, age int64
weights: rescaled to total 8,847,892
wrote clean/d8.parquet (53 columns)
job clean_d8 finished ✓ exit 0 (22.4s)
WARNING: 212 'income' values are non-numeric codes (-9 = refused), kept unchanged per codebook
```

Observation (output file statistics):
```
clean/d8.parquet: 20,941 rows x 53 columns (5.0 MB)
weight: min 131.0  max 2057.6  mean 422.5  nulls 0
Q03: nulls 249 (1.2%)
Q22: nulls 253 (1.2%)
Q17: nulls 42 (0.2%)
Q47: nulls 326 (1.6%)
Q20: nulls 49 (0.2%)
Q01: nulls 61 (0.3%)
Q35: nulls 117 (0.6%)
Q10: nulls 117 (0.6%)
Q36: nulls 368 (1.8%)
Q12: nulls 377 (1.8%)
Q21: nulls 295 (1.4%)
Q45: nulls 209 (1.0%)
Q27: nulls 355 (1.7%)
sum 8,847,892
Q16: nulls 113 (0.5%)
Q37: nulls 325 (1.6%)
Q29: nulls 23 (0.1%)
respondent_id: 20,941 unique of 20,941
Q34: nulls 163 (0.8%)
Q46: nulls 168 (0.8%)
Q15: nulls 342 (1.6%)
Q06: nulls 271 (1.3%)
income: non-numeric codes 212 (1.0%)
```

Observation (downstream validation report):
```
schema: 53 columns present ✓
row count: 20,941 (raw 22,347, duplicates removed 1406) ✓
Q35: values within codebook range ✓
Q11: values within codebook range ✓
weighted share female: 0.51 (census 0.51) ✓
Q23: values within codebook range ✓
sum of weights: 8,847,892 ✓
Q17: values within codebook range ✓
Q27: values within codebook range ✓
Q24: values within codebook range ✓
Q19: values within codebook range ✓
Q34: values within codebook range ✓
Q26: values within codebook range ✓
Q02: values within codebook range ✓
3 columns with >5% missing (expected per codebook)
```

Answer with a JSON object only: {"works": true or false, "reason": "one or two sentences naming the decisive line(s)", "decidable": true or false}. Set "decidable" to false if the observations do not allow a confident decision either way.
```

</details>

## research-ok_noisy-6016

- Generator: ok (`none`)
- Prüfer: False (entscheidbar: True)
- Begründung: The log states 'weights: rescaled to total 2,154,595', which is an additional modification beyond removing duplicate respondents. Output statistics and downstream validation confirm this total, which also differs from the stated population target of 2,155,000.
- Spur laut Generator: —
- **Klärung (Neo):** 

<details><summary>Beleg</summary>

```
A colleague finished the work item below. Afterwards, three independent observations of the system were collected. Decide whether the work item actually achieved its intended effect.

Work item: Clean survey dataset D8: remove duplicate respondents only and write clean/d8.parquet (raw file: 16,683 rows, 41 columns, 124 duplicate respondents; survey weights sum to the target population of 2,155,000)

Observation (job log):
```
job clean_d8 started
read raw/d8.csv: 16,683 rows
read chunk 1/20: 834 rows
read chunk 2/20: 834 rows
read chunk 3/20: 834 rows
read chunk 4/20: 834 rows
read chunk 5/20: 834 rows
read chunk 6/20: 834 rows
read chunk 7/20: 834 rows
read chunk 8/20: 834 rows
read chunk 9/20: 834 rows
read chunk 10/20: 834 rows
read chunk 11/20: 834 rows
read chunk 12/20: 834 rows
read chunk 13/20: 834 rows
read chunk 14/20: 834 rows
read chunk 15/20: 834 rows
read chunk 16/20: 834 rows
read chunk 17/20: 834 rows
read chunk 18/20: 834 rows
read chunk 19/20: 834 rows
read chunk 20/20: 837 rows
info: 3 respondents have interview_date in the future (flagged for review, not changed)
WARNING: 212 'income' values are non-numeric codes (-9 = refused), kept unchanged per codebook
memory: peak 1.9 GB
dedupe on respondent_id: dropped 124 duplicates
dtypes: weight float64, income float64, age int64
weights: rescaled to total 2,154,595
wrote clean/d8.parquet (41 columns)
job clean_d8 finished ✓ exit 0 (11.5s)
```

Observation (output file statistics):
```
clean/d8.parquet: 16,559 rows x 41 columns (3.0 MB)
weight: min 40.3  max 633.7  mean 130.1  nulls 0
Q21: nulls 184 (1.1%)
Q09: nulls 161 (1.0%)
Q11: nulls 380 (2.3%)
Q13: nulls 212 (1.3%)
Q04: nulls 166 (1.0%)
Q29: nulls 11 (0.1%)
Q17: nulls 224 (1.4%)
Q15: nulls 291 (1.8%)
Q28: nulls 28 (0.2%)
Q26: nulls 84 (0.5%)
Q34: nulls 392 (2.4%)
Q10: nulls 388 (2.3%)
Q01: nulls 337 (2.0%)
Q02: nulls 212 (1.3%)
Q27: nulls 156 (0.9%)
Q05: nulls 63 (0.4%)
Q32: nulls 32 (0.2%)
Q24: nulls 102 (0.6%)
Q18: nulls 127 (0.8%)
Q19: nulls 212 (1.3%)
Q12: nulls 211 (1.3%)
sum 2,154,595
Q37: nulls 274 (1.7%)
Q33: nulls 216 (1.3%)
Q06: nulls 294 (1.8%)
Q36: nulls 133 (0.8%)
Q16: nulls 11 (0.1%)
Q08: nulls 107 (0.6%)
Q07: nulls 205 (1.2%)
Q25: nulls 192 (1.2%)
Q31: nulls 276 (1.7%)
Q14: nulls 254 (1.5%)
Q03: nulls 199 (1.2%)
Q30: nulls 61 (0.4%)
respondent_id: 16,559 unique of 16,559
Q22: nulls 163 (1.0%)
Q35: nulls 345 (2.1%)
Q20: nulls 213 (1.3%)
Q23: nulls 31 (0.2%)
income: non-numeric codes 212 (1.3%)
interview_date: flagged 3
```

Observation (downstream validation report):
```
schema: 41 columns present
row count: 16,559 (raw 16,683, duplicates removed 124)
age distribution vs census: KS p=0.21
3 columns with >5% missing (expected per codebook)
Q19: values within codebook range
Q36: values within codebook range
Q32: values within codebook range
Q20: values within codebook range
Q37: values within codebook range
Q06: values within codebook range
Q33: values within codebook range
Q10: values within codebook range
Q22: values within codebook range
weighted share female: 0.51 (census 0.51)
Q07: values within codebook range
Q26: values within codebook range
Q05: values within codebook range
Q35: values within codebook range
Q23: values within codebook range
Q08: values within codebook range
Q14: values within codebook range
Q12: values within codebook range
Q11: values within codebook range
Q01: values within codebook range
sum of weights: 2,154,595
Q09: values within codebook range
```

Answer with a JSON object only: {"works": true or false, "reason": "one or two sentences naming the decisive line(s)", "decidable": true or false}. Set "decidable" to false if the observations do not allow a confident decision either way.
```

</details>

## Alle Urteile

| Beleg | Fehlerart | Wahrheit | Prüfer | entscheidbar |
|---|---|---|---|---|
| business-fail_moderate-6000 | bounced | False | False | True |
| business-fail_moderate-6006 | amount_mismatch | False | False | True |
| business-fail_moderate-6009 | wrong_contact | False | False | True |
| business-fail_moderate-6013 | wrong_contact | False | False | True |
| business-fail_moderate-6016 | bounced | False | False | True |
| business-fail_moderate-6018 | amount_mismatch | False | False | True |
| business-fail_subtle-6001 | attachment_missing | False | False | True |
| business-fail_subtle-6003 | wrong_contact | False | False | True |
| business-fail_subtle-6005 | attachment_missing | False | False | True |
| business-fail_subtle-6008 | amount_mismatch | False | False | True |
| business-fail_subtle-6009 | attachment_missing | False | False | True |
| business-fail_subtle-6018 | bounced | False | False | True |
| business-ok_clear-6003 | none | True | False | True |
| business-ok_clear-6011 | none | True | False | True |
| business-ok_noisy-6005 | none | True | True | True |
| business-ok_noisy-6012 | none | True | True | True |
| coding-fail_moderate-6001 | low_traffic | False | False | False |
| coding-fail_moderate-6003 | cache_partial | False | False | True |
| coding-fail_moderate-6013 | low_traffic | False | False | False |
| coding-fail_moderate-6015 | cache_partial | False | False | True |
| coding-fail_moderate-6021 | low_traffic | False | False | False |
| coding-fail_subtle-6002 | stale_process | False | False | True |
| coding-fail_subtle-6004 | db_down | False | False | True |
| coding-fail_subtle-6008 | db_down | False | False | True |
| coding-fail_subtle-6010 | stale_process | False | False | True |
| coding-fail_subtle-6012 | db_down | False | False | True |
| coding-fail_subtle-6014 | stale_process | False | False | True |
| coding-fail_subtle-6017 | cache_partial | False | False | True |
| coding-ok_clear-6004 | none | True | True | True |
| coding-ok_clear-6021 | none | True | True | True |
| coding-ok_noisy-6004 | none | True | True | True |
| coding-ok_noisy-6023 | none | True | True | True |
| research-fail_moderate-6002 | duplicates_partial | False | False | True |
| research-fail_moderate-6004 | row_loss | False | False | True |
| research-fail_moderate-6007 | column_loss | False | False | True |
| research-fail_moderate-6012 | row_loss | False | False | True |
| research-fail_moderate-6019 | column_loss | False | False | True |
| research-fail_moderate-6020 | row_loss | False | False | True |
| research-fail_subtle-6000 | duplicates_partial | False | False | True |
| research-fail_subtle-6005 | column_loss | False | False | True |
| research-fail_subtle-6007 | weights_misscaled | False | False | True |
| research-fail_subtle-6008 | duplicates_partial | False | False | True |
| research-fail_subtle-6015 | weights_misscaled | False | False | True |
| research-fail_subtle-6023 | weights_misscaled | False | False | True |
| research-ok_clear-6004 | none | True | False | True |
| research-ok_clear-6010 | none | True | False | True |
| research-ok_noisy-6002 | none | True | False | True |
| research-ok_noisy-6016 | none | True | False | True |