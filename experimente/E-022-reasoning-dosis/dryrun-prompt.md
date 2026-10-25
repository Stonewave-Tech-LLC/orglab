# E-022 Dry-Run: exakter Prompttext (Regel 16)

Der Text ist in allen vier Armen identisch. Die Arme unterscheiden sich nur im API-Parameter `reasoning.effort` (low, medium, high, weggelassen). Gezeigt: Stapel 1, Positionen 0–2 (jede Position sieht je Beleg einen anderen Kanal).

## e022-b00, Position 0

````
You have 12 completed work items to review in this session. For each one, judge whether it actually achieved its intended effect. Base each judgment only on the system output shown for that item.

### Item 1
Work item: Clean survey dataset D6: remove duplicate respondents only and write clean/d6.parquet (raw file: 37,823 rows, 47 columns, 161 duplicate respondents; survey weights are normalised to mean 1)

System output (output file statistics):
```
clean/d6.parquet: 37,662 rows x 47 columns (7.9 MB)
income: non-numeric codes 212 (0.6%)
weight: min 0.31  max 4.87  mean 1.00  nulls 0
Q11: nulls 21 (0.1%)
Q09: nulls 144 (0.4%)
Q20: nulls 284 (0.8%)
Q21: nulls 246 (0.7%)
Q32: nulls 157 (0.4%)
Q23: nulls 154 (0.4%)
Q31: nulls 203 (0.5%)
Q35: nulls 90 (0.2%)
Q26: nulls 273 (0.7%)
Q37: nulls 259 (0.7%)
Q28: nulls 309 (0.8%)
Q06: nulls 361 (1.0%)
Q38: nulls 94 (0.2%)
Q01: nulls 72 (0.2%)
respondent_id: 37,662 unique of 37,662
Q15: nulls 279 (0.7%)
Q29: nulls 133 (0.4%)
Q14: nulls 379 (1.0%)
Q39: nulls 80 (0.2%)
Q27: nulls 64 (0.2%)
Q08: nulls 144 (0.4%)
```

### Item 2
Work item: Clean survey dataset D1: remove duplicate respondents only and write clean/d1.parquet (raw file: 9,860 rows, 47 columns, 43 duplicate respondents; survey weights are normalised to mean 1)

System output (job log):
```
job clean_d1 started
read raw/d1.csv: 9,860 rows, 47 columns
dedupe on respondent_id: dropped 43 duplicates
dtypes: weight float64, income float64, age int64
wrote clean/d1.parquet (47 columns)
job clean_d1 finished ✓ exit 0 (37.2s)
```

### Item 3
Work item: Deploy billing-api v2.5.6 (commit c256424) to production (normally handles ~240 requests/min)

System output (deployment script and process manager output):
```
$ ./deploy.sh billing-api v2.5.6
build: passed ✓ (2m37s)
release: /srv/billing-api/releases/2.5.6-c256424 (config: PORT=3000)
pm2 restart billing-api ... done
pm2: billing-api online ✓ (pid 28611, uptime 83s)
app log (tail):
  [billing-api] config loaded (env=production)
  [billing-api] db pool ready (20/20)
  [billing-api] cache connected (4/4 shards)
  [billing-api] listening on :3000
  [billing-api] requests served (last 60s): 247
```

### Item 4
Work item: Clean survey dataset D6: remove duplicate respondents only and write clean/d6.parquet (raw file: 26,226 rows, 47 columns, 266 duplicate respondents; survey weights are normalised to mean 1)

System output (downstream validation report):
```
schema: 47/47 columns present ✓
row count: 25,960 (raw 26,226, duplicates removed 266) ✓
3 columns with >5% missing (expected per codebook)
Q09: values within codebook range ✓
weighted share female: 0.51 (census 0.51) ✓
Q33: values within codebook range ✓
Q13: values within codebook range ✓
Q36: values within codebook range ✓
Q18: values within codebook range ✓
sum of weights / n: 100.38
Q06: values within codebook range ✓
Q24: values within codebook range ✓
Q11: values within codebook range ✓
Q35: values within codebook range ✓
Q34: values within codebook range ✓
```

### Item 5
Work item: Send invoice INV-2026-1698 (€ 7,825.41, PDF attached) to customer K-39, billing contact p.kraus@berger-moebel.at

System output (outgoing mail server log):
```
10:35:49 C16608B476: from=<billing@nordwerk-gmbh.at> to=<p.kraus@berger-moebel.at> size=60411 subject='Invoice INV-2026-1698 (€ 7,825.41)'
10:21:13 760E71EB43: from=<billing@nordwerk-gmbh.at> to=<s.bauer@wagner-druck.at> size=51657
10:32:33 6CADF75D68: from=<billing@nordwerk-gmbh.at> to=<n.hofer@steiner-holz.de> size=56344
10:29:42 A458F87731: from=<billing@nordwerk-gmbh.at> to=<p.wagner@hofer-reisen.at> size=79481
10:38:49 571900BC80: from=<billing@nordwerk-gmbh.at> to=<t.gruber@steiner-holz.de> size=45017
10:20:43 314575C791: from=<billing@nordwerk-gmbh.at> to=<a.hofer@gruber-elektro.at> size=89291
10:31:54 77EC7956BB: from=<billing@nordwerk-gmbh.at> to=<p.bauer@gruber-elektro.at> size=44524
10:35:49 C16608B476: 250 2.0.0 OK queued
10:21:12 B86898A9E7: from=<billing@nordwerk-gmbh.at> to=<a.bauer@pichler-agrar.at> size=64840
10:22:34 60C2085D25: from=<billing@nordwerk-gmbh.at> to=<s.pichler@gruber-elektro.at> size=64561
10:30:51 B073D3E615: from=<billing@nordwerk-gmbh.at> to=<e.pichler@pichler-agrar.at> size=87585
10:24:41 E53641BD04: from=<billing@nordwerk-gmbh.at> to=<g.steiner@steiner-holz.de> size=81967
10:57:47 6CADF75D68: relay=mx1.steiner-holz.de:25, status=sent (250 2.0.0 accepted)
10:57:43 77EC7956BB: relay=mx1.gruber-elektro.at:25, status=sent (250 2.0.0 accepted)
10:40:37 B86898A9E7: relay=mx1.pichler-agrar.at:25, status=sent (250 2.0.0 accepted)
10:42:17 60C2085D25: relay=mx1.gruber-elektro.at:25, status=sent (250 2.0.0 accepted)
10:21:10 314575C791: relay=mx1.gruber-elektro.at:25, status=sent (250 2.0.0 accepted)
10:51:31 A458F87731: relay=mx1.hofer-reisen.at:25, status=sent (250 2.0.0 accepted)
10:55:49 760E71EB43: relay=mx1.wagner-druck.at:25, status=sent (250 2.0.0 accepted)
10:58:30 C16608B476: relay=mx1.berger-moebel.at:25, status=sent (250 2.0.0 accepted)
10:53:41 B073D3E615: relay=mx1.pichler-agrar.at:25, status=sent (250 2.0.0 accepted)
10:30:52 E53641BD04: relay=mx1.steiner-holz.de:25, status=sent (250 2.0.0 accepted)
10:55:50 571900BC80: relay=mx1.steiner-holz.de:25, status=sent (250 2.0.0 accepted)
10:35:49 C16608B476: TLS handshake retry (1/3) ... ok
```

### Item 6
Work item: Deploy notify-worker v5.9.1 (commit 2f4ceb5) to production (normally handles ~120 requests/min)

System output (deployment script and process manager output):
```
$ ./deploy.sh notify-worker v5.9.1
build: passed ✓ (3m24s)
release: /srv/notify-worker/releases/5.9.1-2f4ceb5 (config: PORT=3000)
pm2 restart notify-worker ... done
pm2: notify-worker online ✓ (pid 22659, uptime 80s)
app log (tail):
  [notify-worker] config loaded (env=production)
  [notify-worker] db pool ready (20/20)
  [notify-worker] cache connected (4/4 shards)
  [notify-worker] listening on :3000
  [notify-worker] requests served (last 60s): 140
```

### Item 7
Work item: Send invoice INV-2026-1953 (€ 8,629.64, PDF attached) to customer K-66, billing contact a.kraus@lindner-logistik.de

System output (delivery tracking report):
```
tracking 8956613410: delivered to mailbox of <g.gruber@wagner-druck.at> (dsn 2.0.0)
tracking E142A985FE: delivered to mailbox of <c.wagner@gruber-elektro.at> (dsn 2.0.0)
tracking DDAF7542AD: delivered to mailbox of <t.steiner@steiner-holz.de> (dsn 2.0.0)
tracking FCFD692C80: delivered to mailbox of <o.gruber@wagner-druck.at> (dsn 2.0.0)
tracking 2AEFA0ECFD: delivered to mailbox of <h.steiner@gruber-elektro.at> (dsn 2.0.0)
tracking 5C7EC66821: delivered to mailbox of <l.wagner@pichler-agrar.at> (dsn 2.0.0)
tracking E012465C8A: delivered to mailbox of <g.pichler@hofer-reisen.at> (dsn 2.0.0)
tracking 9CF60BE9C7: delivered to mailbox of <o.steiner@gruber-elektro.at> (dsn 2.0.0)
tracking F27F9E7255: delivered to mailbox of <s.pichler@pichler-agrar.at> (dsn 2.0.0)
tracking 103C2FC729: delivered to mailbox of <r.bauer@wagner-druck.at> (dsn 2.0.0)
tracking 791401785F: delivered to mailbox of <t.gruber@wagner-druck.at> (dsn 2.0.0)
tracking A2382BAF7D: delivered to mailbox of <e.wagner@steiner-holz.de> (dsn 2.0.0)
tracking 6342CB456B: delivered to mailbox of <s.steiner@wagner-druck.at> (dsn 2.0.0)
tracking A69AD5EF22: delivered to mailbox of <h.bauer@hofer-reisen.at> (dsn 2.0.0)
tracking 029EE38412: delivered to mailbox of <k.bauer@steiner-holz.de> (dsn 2.0.0)
tracking 81296A0046: delivered to mailbox of <p.hofer@steiner-holz.de> (dsn 2.0.0)
tracking A47FF9121F: accepted by recipient server at 10:49:39
tracking 3395F1145F: delivered to mailbox of <s.wagner@wagner-druck.at> (dsn 2.0.0)
tracking A47FF9121F: delivered to mailbox of <a.kraus@lindner-logistik.de> (dsn 2.0.0)
tracking 068485EA5A: delivered to mailbox of <b.gruber@pichler-agrar.at> (dsn 2.0.0)
tracking A66C9D78FC: delivered to mailbox of <p.steiner@hofer-reisen.at> (dsn 2.0.0)
tracking F74F719F15: delivered to mailbox of <a.bauer@hofer-reisen.at> (dsn 2.0.0)
tracking 41561E5D5F: delivered to mailbox of <g.steiner@steiner-holz.de> (dsn 2.0.0)
tracking BF449E18E5: delivered to mailbox of <r.wagner@hofer-reisen.at> (dsn 2.0.0)
tracking A28B8E4B1C: delivered to mailbox of <h.bauer@steiner-holz.de> (dsn 2.0.0)
tracking DBF77D4AF6: delivered to mailbox of <f.steiner@wagner-druck.at> (dsn 2.0.0)
tracking D5171BBF41: delivered to mailbox of <r.wagner@pichler-agrar.at> (dsn 2.0.0)
tracking CD8B1483F6: delivered to mailbox of <d.steiner@wagner-druck.at> (dsn 2.0.0)
tracking 2D8AE9D209: delivered to mailbox of <e.steiner@wagner-druck.at> (dsn 2.0.0)
tracking F6063AB3EF: delivered to mailbox of <a.gruber@hofer-reisen.at> (dsn 2.0.0)
tracking EE928B56E9: delivered to mailbox of <c.bauer@pichler-agrar.at> (dsn 2.0.0)
tracking 819A6469EB: delivered to mailbox of <e.steiner@hofer-reisen.at> (dsn 2.0.0)
tracking F25C4E19D2: delivered to mailbox of <o.gruber@steiner-holz.de> (dsn 2.0.0)
tracking 44F7F024D8: delivered to mailbox of <l.gruber@wagner-druck.at> (dsn 2.0.0)
tracking 49A6F0203F: delivered to mailbox of <n.steiner@gruber-elektro.at> (dsn 2.0.0)
tracking F8ECB94098: delivered to mailbox of <a.gruber@steiner-holz.de> (dsn 2.0.0)
tracking AC2CC98A01: delivered to mailbox of <k.wagner@gruber-elektro.at> (dsn 2.0.0)
tracking 35C2DCF7BF: delivered to mailbox of <m.steiner@steiner-holz.de> (dsn 2.0.0)
tracking F8F8179755: delivered to mailbox of <e.gruber@gruber-elektro.at> (dsn 2.0.0)
tracking A3FA701B78: delivered to mailbox of <h.gruber@gruber-elektro.at> (dsn 2.0.0)
tracking F2B4105C18: delivered to mailbox of <b.steiner@wagner-druck.at> (dsn 2.0.0)
tracking 5A98972EBC: delivered to mailbox of <b.hofer@steiner-holz.de> (dsn 2.0.0)
tracking A47FF9121F: 1 attachment (invoice_INV-2026-1953.pdf, 69 kB)
tracking A47FF9121F: payment link pay.nordwerk-gmbh.at/INV-2026-1953 (€ 8,629.64)
read receipt: not requested
tracking A47FF9121F: link scan by recipient gateway
tracking A47FF9121F: open pixel blocked by recipient client
```

### Item 8
Work item: Clean survey dataset D7: remove duplicate respondents only and write clean/d7.parquet (raw file: 23,556 rows, 47 columns, 76 duplicate respondents; survey weights are normalised to mean 1)

System output (output file statistics):
```
clean/d7.parquet: 23,480 rows x 47 columns (4.9 MB)
interview_date: flagged 3
income: non-numeric codes 212 (0.9%)
weight: min 0.31  max 4.87  mean 1.00  nulls 0
Q11: nulls 364 (1.6%)
Q05: nulls 327 (1.4%)
Q12: nulls 348 (1.5%)
Q32: nulls 336 (1.4%)
Q04: nulls 200 (0.9%)
Q20: nulls 271 (1.2%)
Q43: nulls 262 (1.1%)
Q42: nulls 280 (1.2%)
Q09: nulls 255 (1.1%)
Q24: nulls 99 (0.4%)
Q41: nulls 174 (0.7%)
Q31: nulls 180 (0.8%)
Q28: nulls 209 (0.9%)
Q16: nulls 95 (0.4%)
Q23: nulls 330 (1.4%)
Q03: nulls 32 (0.1%)
Q06: nulls 19 (0.1%)
Q17: nulls 5 (0.0%)
Q13: nulls 269 (1.1%)
Q22: nulls 44 (0.2%)
Q33: nulls 183 (0.8%)
Q18: nulls 371 (1.6%)
Q39: nulls 296 (1.3%)
Q37: nulls 127 (0.5%)
Q35: nulls 100 (0.4%)
Q10: nulls 192 (0.8%)
respondent_id: 23,480 unique of 23,480
Q01: nulls 19 (0.1%)
Q40: nulls 207 (0.9%)
Q38: nulls 307 (1.3%)
Q34: nulls 141 (0.6%)
Q29: nulls 392 (1.7%)
Q15: nulls 55 (0.2%)
Q27: nulls 340 (1.4%)
Q21: nulls 233 (1.0%)
Q36: nulls 301 (1.3%)
Q30: nulls 125 (0.5%)
Q14: nulls 316 (1.3%)
Q08: nulls 257 (1.1%)
Q26: nulls 90 (0.4%)
Q44: nulls 301 (1.3%)
```

### Item 9
Work item: Deploy portal-frontend v5.8.2 (commit 295889e) to production (normally handles ~60 requests/min)

System output (deployment script and process manager output):
```
$ ./deploy.sh portal-frontend v5.8.2
build: passed ✓ (2m48s)
  dist/assets/index-e98ee00b.js  188.81 kB
  dist/assets/vendor-f02c8d28.js  194.83 kB
  dist/assets/index-d02de0d3.js  95.57 kB
  dist/assets/worker-d9400a20.js  12.82 kB
  dist/assets/chunk-37a45076.js  248.12 kB
  dist/assets/worker-925f04f6.js  92.54 kB
release: /srv/portal-frontend/releases/5.8.2-295889e (config: PORT=8080)
  dist/assets/vendor-d1b914df.js  132.82 kB
  dist/assets/vendor-c801d601.js  376.48 kB
  dist/assets/index-b1980847.js  322.78 kB
  dist/assets/index-1c4d3d76.js  169.33 kB
  dist/assets/worker-1e1d574c.js  111.59 kB
  dist/assets/index-a4366ff2.js  201.60 kB
  dist/assets/worker-b67eef59.js  27.62 kB
  dist/assets/worker-11055ffb.js  103.91 kB
  dist/assets/worker-ee641a16.js  32.18 kB
  dist/assets/index-f273083a.js  346.88 kB
  dist/assets/index-f0e03692.js  84.78 kB
  dist/assets/index-8b6c486c.js  347.91 kB
  dist/assets/chunk-4b25219f.js  77.28 kB
  dist/assets/vendor-775af6c6.js  93.60 kB
pm2 restart portal-frontend ... done
pm2: portal-frontend online ✓ (pid 25233, uptime 90s)
npm WARN deprecated request@2.88.2: request has been deprecated
pm2: log rotation done
  [portal-frontend] warn: slow query 812ms (report_daily)
app log (tail):
  [portal-frontend] config loaded (env=production)
  [portal-frontend] scheduled job 'sync' every 22m
  [portal-frontend] db pool ready (20/20)
  [portal-frontend] cache connected (0/4 shards)
  [portal-frontend] loaded 21 feature flags
  [portal-frontend] scheduled job 'digest' every 6m
  [portal-frontend] scheduled job 'cleanup' every 29m
  [portal-frontend] scheduled job 'sync' every 18m
  [portal-frontend] warmed cache 'products' (6532 keys)
  [portal-frontend] scheduled job 'digest' every 26m
  [portal-frontend] loaded 20 feature flags
  [portal-frontend] loaded 32 feature flags
  [portal-frontend] scheduled job 'sync' every 24m
  [portal-frontend] warmed cache 'geo' (5299 keys)
  [portal-frontend] loaded 13 feature flags
  [portal-frontend] loaded 44 feature flags
  [portal-frontend] warmed cache 'sessions' (3001 keys)
  [portal-frontend] scheduled job 'cleanup' every 26m
  [portal-frontend] scheduled job 'digest' every 5m
  [portal-frontend] warmed cache 'geo' (6751 keys)
  [portal-frontend] loaded 48 feature flags
  [portal-frontend] listening on :8080
  [portal-frontend] scheduled job 'digest' every 6m
  [portal-frontend] requests served (last 60s): 68
  [portal-frontend] scheduled job 'cleanup' every 2m
```

### Item 10
Work item: Clean survey dataset D2: remove duplicate respondents only and write clean/d2.parquet (raw file: 31,816 rows, 47 columns, 150 duplicate respondents; survey weights are normalised to mean 1)

System output (downstream validation report):
```
schema: 47/47 columns present ✓
row count: 31,666 (raw 31,816, duplicates removed 150) ✓
Q23: values within codebook range ✓
weighted share female: 0.51 (census 0.51) ✓
sum of weights / n: 1.00 ✓
Q03: values within codebook range ✓
Q09: values within codebook range ✓
Q19: values within codebook range ✓
Q24: values within codebook range ✓
Q07: values within codebook range ✓
Q36: values within codebook range ✓
Q41: values within codebook range ✓
Q22: values within codebook range ✓
Q40: values within codebook range ✓
3 columns with >5% missing (expected per codebook)
```

### Item 11
Work item: Deploy portal-frontend v4.8.4 (commit f39057d) to production (normally handles ~390 requests/min)

System output (deployment script and process manager output):
```
$ ./deploy.sh portal-frontend v4.8.4
build: passed ✓ (4m20s)
release: /srv/portal-frontend/releases/4.8.4-f39057d (config: PORT=5000)
pm2 restart portal-frontend ... done
pm2: portal-frontend online ✓ (pid 21260, uptime 78s)
app log (tail):
  [portal-frontend] config loaded (env=production)
  [portal-frontend] db pool ready (0/20)
  [portal-frontend] cache connected (4/4 shards)
  [portal-frontend] listening on :5000
  [portal-frontend] requests served (last 60s): 423
```

### Item 12
Work item: Deploy billing-api v3.3.3 (commit eb07954) to production (normally handles ~130 requests/min)

System output (socket and process table):
```
$ ss -ltnp
LISTEN 0 511 *:8443 *:* users:(("node",pid=22519,fd=21))
LISTEN 0 511 *:9101 *:* users:(("node",pid=30009,fd=19))
LISTEN 0 511 *:9100 *:* users:(("node",pid=33203,fd=19))
LISTEN 0 128 0.0.0.0:22 0.0.0.0:* users:(("sshd",pid=812,fd=3))
LISTEN 0 511 0.0.0.0:443 0.0.0.0:* users:(("nginx",pid=1044,fd=8))
LISTEN 0 511 *:9102 *:* users:(("node",pid=35855,fd=19))
$ ps -o pid,lstart,cmd -C node
  PID STARTED        CMD
33203 Oct 17 05:00  node /srv/image-resizer/current/server.js
30009 Oct 06 03:00  node /srv/mailer/current/server.js
14110 Oct 02 06:00  node /srv/metrics-agent/agent.js
22519 Oct 22 10:41  node /srv/billing-api/releases/3.3.3-eb07954/server.js
35855 Oct 18 03:00  node /srv/admin-ui/current/server.js
$ ss -tnp
ESTAB 0 0 10.0.0.5:45902 10.0.5.77:5432 users:(("node",pid=22519,fd=24))
ESTAB 0 0 10.0.0.5:8443 10.0.2.8:41351 users:(("node",pid=22519,fd=29))
ESTAB 0 0 10.0.0.5:8443 10.0.2.8:47795 users:(("node",pid=22519,fd=22))
ESTAB 0 0 10.0.0.5:8443 10.0.2.8:47135 users:(("node",pid=22519,fd=21))
ESTAB 0 0 10.0.0.5:8443 10.0.2.9:49710 users:(("node",pid=22519,fd=34))
ESTAB 0 0 10.0.0.5:8443 10.0.2.8:56862 users:(("node",pid=22519,fd=27))
ESTAB 0 0 10.0.0.5:53884 10.0.5.77:5432 users:(("node",pid=22519,fd=27))
ESTAB 0 0 10.0.0.5:8443 10.0.2.3:31887 users:(("node",pid=22519,fd=37))
ESTAB 0 0 10.0.0.5:54601 10.0.8.63:6379 users:(("node",pid=22519,fd=23))
ESTAB 0 0 10.0.0.5:58797 10.0.8.63:6379 users:(("node",pid=22519,fd=40))
ESTAB 0 0 10.0.0.5:8443 10.0.2.8:43918 users:(("node",pid=22519,fd=25))
ESTAB 0 0 10.0.0.5:59665 10.0.5.77:5432 users:(("node",pid=22519,fd=22))
ESTAB 0 0 10.0.0.5:8443 10.0.2.8:48564 users:(("node",pid=22519,fd=32))
ESTAB 0 0 10.0.0.5:8443 10.0.2.9:45392 users:(("node",pid=22519,fd=34))
ESTAB 0 0 10.0.0.5:8443 10.0.2.8:44660 users:(("node",pid=22519,fd=29))
$ ss -tn state established '( sport = :8443 )' | tail -n +2 | wc -l
53
$ df -h /srv | tail -1
/dev/nvme0n1p2  200G  141G   59G  71% /srv
```

Respond with a JSON array only: [{"item": 1, "works": true or false, "confidence": number between 0 and 1}, ...] with exactly one entry per item
````

## e022-b00, Position 1

````
You have 12 completed work items to review in this session. For each one, judge whether it actually achieved its intended effect. Base each judgment only on the system output shown for that item.

### Item 1
Work item: Clean survey dataset D6: remove duplicate respondents only and write clean/d6.parquet (raw file: 37,823 rows, 47 columns, 161 duplicate respondents; survey weights are normalised to mean 1)

System output (downstream validation report):
```
schema: 47/47 columns present ✓
3 columns with >5% missing (expected per codebook)
row count: 37,662 (raw 37,823, duplicates removed 161) ✓
Q42: values within codebook range ✓
Q13: values within codebook range ✓
Q07: values within codebook range ✓
Q21: values within codebook range ✓
Q20: values within codebook range ✓
Q29: values within codebook range ✓
weighted share female: 0.51 (census 0.51) ✓
Q27: values within codebook range ✓
Q02: values within codebook range ✓
Q15: values within codebook range ✓
sum of weights / n: 1.00 ✓
Q22: values within codebook range ✓
```

### Item 2
Work item: Clean survey dataset D1: remove duplicate respondents only and write clean/d1.parquet (raw file: 9,860 rows, 47 columns, 43 duplicate respondents; survey weights are normalised to mean 1)

System output (output file statistics):
```
clean/d1.parquet: 9,817 rows x 47 columns (2.1 MB)
weight: min 0.31  max 4.87  mean 1.00  nulls 0
respondent_id: 9,817 unique of 9,817
```

### Item 3
Work item: Deploy billing-api v2.5.6 (commit c256424) to production (normally handles ~240 requests/min)

System output (HTTP endpoint checks):
```
$ curl -s http://localhost:3000/version
{"service": "billing-api", "version": "2.5.6", "commit": "c256424"}
$ curl -s http://localhost:3000/health
{"status": "ok", "checks": {"db": "ok", "cache": "ok"}, "db_pool": {"size": 20, "active": 8, "waiting": 0}, "cache_shards": {"up": 4, "total": 4}}
$ curl -s http://localhost:3000/metrics | grep ^http_requests_total
http_requests_total{code="200"} 1235
http_requests_total{code="500"} 2
```

### Item 4
Work item: Clean survey dataset D6: remove duplicate respondents only and write clean/d6.parquet (raw file: 26,226 rows, 47 columns, 266 duplicate respondents; survey weights are normalised to mean 1)

System output (job log):
```
job clean_d6 started
read raw/d6.csv: 26,226 rows, 47 columns
read chunk 1/10: 2,622 rows
read chunk 2/10: 2,622 rows
read chunk 3/10: 2,622 rows
read chunk 4/10: 2,622 rows
read chunk 5/10: 2,622 rows
read chunk 6/10: 2,622 rows
read chunk 7/10: 2,622 rows
read chunk 8/10: 2,622 rows
read chunk 9/10: 2,622 rows
read chunk 10/10: 2,628 rows
WARNING: 212 'income' values are non-numeric codes (-9 = refused), kept unchanged per codebook
dedupe on respondent_id: dropped 266 duplicates
dtypes: weight int64, income float64, age int64
wrote clean/d6.parquet (47 columns)
job clean_d6 finished ✓ exit 0 (3.7s)
```

### Item 5
Work item: Send invoice INV-2026-1698 (€ 7,825.41, PDF attached) to customer K-39, billing contact p.kraus@berger-moebel.at

System output (delivery tracking report):
```
tracking 862E14BBFD: delivered to mailbox of <t.bauer@wagner-druck.at> (dsn 2.0.0)
tracking EEE75DF5A4: delivered to mailbox of <l.pichler@gruber-elektro.at> (dsn 2.0.0)
tracking AC943A5345: delivered to mailbox of <j.wagner@hofer-reisen.at> (dsn 2.0.0)
tracking 8837CC1D8F: delivered to mailbox of <r.pichler@hofer-reisen.at> (dsn 2.0.0)
tracking 4ADCDD82EA: delivered to mailbox of <k.wagner@hofer-reisen.at> (dsn 2.0.0)
tracking 6AD69EA4AB: delivered to mailbox of <b.wagner@pichler-agrar.at> (dsn 2.0.0)
tracking 38CED78144: delivered to mailbox of <n.hofer@steiner-holz.de> (dsn 2.0.0)
tracking 7764E59965: delivered to mailbox of <k.wagner@hofer-reisen.at> (dsn 2.0.0)
tracking 99652BB9E3: delivered to mailbox of <k.hofer@gruber-elektro.at> (dsn 2.0.0)
tracking 73097D9A10: delivered to mailbox of <o.hofer@gruber-elektro.at> (dsn 2.0.0)
tracking 6BC7EB1E84: delivered to mailbox of <h.wagner@steiner-holz.de> (dsn 2.0.0)
tracking DAA7939214: delivered to mailbox of <o.gruber@hofer-reisen.at> (dsn 2.0.0)
tracking 685A8F698E: delivered to mailbox of <t.steiner@steiner-holz.de> (dsn 2.0.0)
tracking C16608B476: accepted by recipient server at 10:58:30
tracking 133279CAFE: delivered to mailbox of <p.gruber@steiner-holz.de> (dsn 2.0.0)
tracking 696D6B50E3: delivered to mailbox of <j.pichler@gruber-elektro.at> (dsn 2.0.0)
tracking F8A72FB95F: delivered to mailbox of <m.wagner@steiner-holz.de> (dsn 2.0.0)
tracking 9E84127CEF: delivered to mailbox of <n.pichler@steiner-holz.de> (dsn 2.0.0)
tracking 87DC9D640A: delivered to mailbox of <c.bauer@hofer-reisen.at> (dsn 2.0.0)
tracking 05BEED92B4: delivered to mailbox of <g.steiner@gruber-elektro.at> (dsn 2.0.0)
tracking C16608B476: delivered to mailbox of <p.kraus@berger-moebel.at> (dsn 2.0.0)
tracking F7A012B7AF: delivered to mailbox of <a.wagner@hofer-reisen.at> (dsn 2.0.0)
tracking C16608B476: link scan by recipient gateway
tracking C16608B476: 1 attachment (invoice_INV-2026-1698.pdf, 58 kB)
tracking C16608B476: payment link pay.nordwerk-gmbh.at/INV-2026-1698 (€ 7,825.41)
read receipt: not requested
```

### Item 6
Work item: Deploy notify-worker v5.9.1 (commit 2f4ceb5) to production (normally handles ~120 requests/min)

System output (HTTP endpoint checks):
```
$ curl -s http://localhost:3000/version
{"service": "notify-worker", "version": "5.9.1", "commit": "2f4ceb5"}
$ curl -s http://localhost:3000/health
{"status": "ok", "checks": {"db": "ok", "cache": "ok"}, "db_pool": {"size": 20, "active": 9, "waiting": 0}, "cache_shards": {"up": 4, "total": 4}}
$ curl -s http://localhost:3000/metrics | grep ^http_requests_total
http_requests_total{code="200"} 420
http_requests_total{code="500"} 2
```

### Item 7
Work item: Send invoice INV-2026-1953 (€ 8,629.64, PDF attached) to customer K-66, billing contact a.kraus@lindner-logistik.de

System output (accounting and CRM entries):
```
receivables: INV-2026-2669 posted, customer K-165, € 3,852.85, status SENT
receivables: INV-2026-2498 posted, customer K-149, € 3,140.59, status SENT
receivables: INV-2026-2671 posted, customer K-137, € 3,417.76, status SENT
receivables: INV-2026-2342 posted, customer K-155, € 4,743.45, status SENT
receivables: INV-2026-2428 posted, customer K-150, € 7,050.74, status SENT
receivables: INV-2026-2756 posted, customer K-105, € 3,912.68, status SENT
receivables: INV-2026-2515 posted, customer K-166, € 8,548.83, status SENT
receivables: INV-2026-2379 posted, customer K-189, € 5,535.53, status SENT
receivables: INV-2026-2113 posted, customer K-159, € 8,681.36, status SENT
receivables: INV-2026-2413 posted, customer K-144, € 4,667.36, status SENT
receivables: INV-2026-2898 posted, customer K-176, € 7,773.11, status SENT
receivables: INV-2026-2206 posted, customer K-147, € 3,804.61, status SENT
receivables: INV-2026-2019 posted, customer K-184, € 6,351.18, status SENT
receivables: INV-2026-2920 posted, customer K-111, € 4,022.40, status SENT
receivables: INV-2026-2653 posted, customer K-174, € 829.81, status SENT
receivables: INV-2026-1953 posted, customer K-66, € 8,629.64, status SENT
receivables: INV-2026-2985 posted, customer K-182, € 5,005.94, status SENT
receivables: INV-2026-2545 posted, customer K-123, € 2,612.80, status SENT
receivables: INV-2026-2347 posted, customer K-118, € 7,573.86, status SENT
receivables: INV-2026-2367 posted, customer K-161, € 4,004.24, status SENT
receivables: INV-2026-2907 posted, customer K-164, € 3,990.77, status SENT
crm: duplicate contact merge suggested for K-66
receivables: exchange rate update skipped (EUR invoice)
crm: activity 'offer sent' on K-192
crm: activity 'invoice sent' on K-191
crm: activity 'invoice sent' on K-136
crm: activity 'offer sent' on K-134
crm: activity 'offer sent' on K-104
crm: activity 'offer sent' on K-106
crm: activity 'invoice sent' on K-196
crm: activity 'call logged' on K-187
crm: activity 'invoice sent' on K-162
crm: activity 'call logged' on K-145
crm: activity 'invoice sent' on K-66 (contact a.kraus@lindner-logistik.de)
crm: activity 'invoice sent' on K-191
crm: activity 'offer sent' on K-165
crm: activity 'call logged' on K-173
crm: activity 'offer sent' on K-104
crm: activity 'invoice sent' on K-145
crm: activity 'offer sent' on K-104
crm: activity 'call logged' on K-189
crm: activity 'offer sent' on K-150
crm: activity 'invoice sent' on K-193
crm: activity 'call logged' on K-164
archive: invoice_INV-2026-1953.pdf stored (3 pages)
dunning: reminder for INV-2026-1953 scheduled 2026-11-21
```

### Item 8
Work item: Clean survey dataset D7: remove duplicate respondents only and write clean/d7.parquet (raw file: 23,556 rows, 47 columns, 76 duplicate respondents; survey weights are normalised to mean 1)

System output (downstream validation report):
```
schema: 47/47 columns present
row count: 23,480 (raw 23,556, duplicates removed 76)
Q37: values within codebook range
Q09: values within codebook range
Q36: values within codebook range
Q44: values within codebook range
Q24: values within codebook range
Q03: values within codebook range
Q35: values within codebook range
weighted share female: 0.51 (census 0.51)
Q06: values within codebook range
Q15: values within codebook range
Q31: values within codebook range
Q38: values within codebook range
Q22: values within codebook range
Q10: values within codebook range
Q27: values within codebook range
sum of weights / n: 1.00
Q13: values within codebook range
Q04: values within codebook range
Q26: values within codebook range
Q12: values within codebook range
Q29: values within codebook range
Q33: values within codebook range
3 columns with >5% missing (expected per codebook)
age distribution vs census: KS p=0.21
```

### Item 9
Work item: Deploy portal-frontend v5.8.2 (commit 295889e) to production (normally handles ~60 requests/min)

System output (HTTP endpoint checks):
```
$ curl -s http://localhost:8080/version
{"service": "portal-frontend", "build": {"version": "5.8.2", "commit": "295889e"}, "uptime_s": 92}
$ curl -s http://localhost:8080/metrics | grep -c ^http_
142
$ curl -s http://localhost:8080/api/v1/config/public
{"locale": "de-AT", "features": 26}
$ curl -s http://localhost:8080/api/v1/config/public
{"locale": "de-AT", "features": 26}
$ curl -s http://localhost:8080/health
{"status": "ok", "checks": {"db": {"ok": true, "latency_ms": 5}, "cache": {"ok": true}}, "db_pool": {"size": 20, "active": 11, "waiting": 0}, "cache_shards": {"up": 0, "total": 4}}
$ curl -s http://localhost:8080/metrics | grep -c ^http_
142
$ curl -s http://localhost:8080/api/v1/config/public
{"locale": "de-AT", "features": 26}
$ curl -s http://localhost:8080/api/v1/ping
{"pong": true}
$ curl -s http://localhost:8080/metrics | grep ^http_requests_total
http_requests_total{code="200"} 204
http_requests_total{code="500"} 2
$ curl -sI http://localhost:8080/
HTTP/1.1 302 Found
Location: /login
$ curl -s http://localhost:8080/api/v1/ping
{"pong": true}
$ curl -s -m 2 http://localhost:8080/health
curl: (28) Operation timed out after 2000 milliseconds
$ curl -s -m 5 http://localhost:8080/health   # retry after warm-up
{"status": "ok", "checks": {"db": {"ok": true, "latency_ms": 5}, "cache": {"ok": true}}, "db_pool": {"size": 20, "active": 11, "waiting": 0}, "cache_shards": {"up": 0, "total": 4}}
$ curl -s http://localhost:8080/metrics | grep -c ^http_
142
$ curl -s http://localhost:8080/api/v1/ping
{"pong": true}
$ curl -s http://localhost:8080/metrics | grep -c ^http_
142
$ curl -s http://localhost:8080/metrics | head -1
# HELP http_requests_total Total HTTP requests
```

### Item 10
Work item: Clean survey dataset D2: remove duplicate respondents only and write clean/d2.parquet (raw file: 31,816 rows, 47 columns, 150 duplicate respondents; survey weights are normalised to mean 1)

System output (job log):
```
job clean_d2 started
read raw/d2.csv: 31,816 rows, 47 columns
read chunk 1/10: 3,181 rows
read chunk 2/10: 3,181 rows
read chunk 3/10: 3,181 rows
read chunk 4/10: 3,181 rows
read chunk 5/10: 3,181 rows
read chunk 6/10: 3,181 rows
read chunk 7/10: 3,181 rows
read chunk 8/10: 3,181 rows
read chunk 9/10: 3,181 rows
read chunk 10/10: 3,187 rows
info: 3 respondents have interview_date in the future (flagged for review, not changed)
dedupe on respondent_id: dropped 150 duplicates
dtypes: weight float64, income float64, age int64
wrote clean/d2.parquet (47 columns)
job clean_d2 finished ✓ exit 0 (17.6s)
```

### Item 11
Work item: Deploy portal-frontend v4.8.4 (commit f39057d) to production (normally handles ~390 requests/min)

System output (HTTP endpoint checks):
```
$ curl -s http://localhost:5000/version
{"service": "portal-frontend", "version": "4.8.4", "commit": "f39057d"}
$ curl -s http://localhost:5000/health
{"status": "ok", "checks": {"db": "ok", "cache": "ok"}, "db_pool": {"size": 20, "active": 0, "waiting": 20}, "cache_shards": {"up": 4, "total": 4}}
$ curl -s http://localhost:5000/metrics | grep ^http_requests_total
http_requests_total{code="200"} 1269
http_requests_total{code="500"} 2
```

### Item 12
Work item: Deploy billing-api v3.3.3 (commit eb07954) to production (normally handles ~130 requests/min)

System output (deployment script and process manager output):
```
$ ./deploy.sh billing-api v3.3.3
build: passed ✓ (2m22s)
  dist/assets/worker-f1137a20.js  368.46 kB
release: /srv/billing-api/releases/3.3.3-eb07954 (config: PORT=8443)
  dist/assets/chunk-7f9bc168.js  208.67 kB
  dist/assets/index-ef04c750.js  4.42 kB
  dist/assets/worker-76ebd15b.js  293.89 kB
  dist/assets/chunk-81de4a67.js  117.38 kB
  dist/assets/chunk-e6aaa86a.js  78.40 kB
  dist/assets/index-51c128a2.js  45.52 kB
  dist/assets/chunk-bb4f134c.js  66.75 kB
  dist/assets/index-ec89914d.js  267.47 kB
  dist/assets/worker-f9654f62.js  159.94 kB
pm2 restart billing-api ... done
pm2: billing-api online ✓ (pid 22519, uptime 80s)
app log (tail):
  [billing-api] config loaded (env=production)
  [billing-api] db pool ready (20/20)
  [billing-api] scheduled job 'cleanup' every 14m
  [billing-api] scheduled job 'sync' every 8m
  [billing-api] scheduled job 'sync' every 18m
  [billing-api] loaded 20 feature flags
  [billing-api] warmed cache 'sessions' (2438 keys)
  [billing-api] cache connected (4/4 shards)
  [billing-api] loaded 34 feature flags
  [billing-api] warmed cache 'products' (5616 keys)
  [billing-api] loaded 27 feature flags
  [billing-api] loaded 10 feature flags
  [billing-api] listening on :8443
  [billing-api] warmed cache 'i18n' (271 keys)
  [billing-api] requests served (last 60s): 104
pm2: log rotation done
```

Respond with a JSON array only: [{"item": 1, "works": true or false, "confidence": number between 0 and 1}, ...] with exactly one entry per item
````

## e022-b00, Position 2

````
You have 12 completed work items to review in this session. For each one, judge whether it actually achieved its intended effect. Base each judgment only on the system output shown for that item.

### Item 1
Work item: Clean survey dataset D6: remove duplicate respondents only and write clean/d6.parquet (raw file: 37,823 rows, 47 columns, 161 duplicate respondents; survey weights are normalised to mean 1)

System output (job log):
```
job clean_d6 started
read raw/d6.csv: 37,823 rows, 47 columns
read chunk 1/10: 3,782 rows
read chunk 2/10: 3,782 rows
read chunk 3/10: 3,782 rows
read chunk 4/10: 3,782 rows
read chunk 5/10: 3,782 rows
read chunk 6/10: 3,782 rows
read chunk 7/10: 3,782 rows
read chunk 8/10: 3,782 rows
read chunk 9/10: 3,782 rows
read chunk 10/10: 3,785 rows
WARNING: 212 'income' values are non-numeric codes (-9 = refused), kept unchanged per codebook
dedupe on respondent_id: dropped 161 duplicates
dtypes: weight float64, income float64, age int64
wrote clean/d6.parquet (47 columns)
job clean_d6 finished ✓ exit 0 (26.3s)
```

### Item 2
Work item: Clean survey dataset D1: remove duplicate respondents only and write clean/d1.parquet (raw file: 9,860 rows, 47 columns, 43 duplicate respondents; survey weights are normalised to mean 1)

System output (downstream validation report):
```
schema: 47/47 columns present
row count: 9,817 (raw 9,860, duplicates removed 43)
weighted share female: 0.51 (census 0.51)
sum of weights / n: 1.00
```

### Item 3
Work item: Deploy billing-api v2.5.6 (commit c256424) to production (normally handles ~240 requests/min)

System output (socket and process table):
```
$ ss -ltnp
LISTEN 0 511 *:3000 *:* users:(("node",pid=28611,fd=21))
$ ps -o pid,lstart,cmd -C node
  PID STARTED        CMD
28611 Oct 22 10:41  node /srv/billing-api/releases/2.5.6-c256424/server.js
$ ss -tnp
ESTAB 0 0 10.0.0.5:40178 10.0.2.15:5432 users:(("node",pid=28611,fd=26))
ESTAB 0 0 10.0.0.5:40653 10.0.9.93:6379 users:(("node",pid=28611,fd=36))
ESTAB 0 0 10.0.0.5:42952 10.0.2.15:5432 users:(("node",pid=28611,fd=36))
ESTAB 0 0 10.0.0.5:46340 10.0.9.93:6379 users:(("node",pid=28611,fd=27))
ESTAB 0 0 10.0.0.5:55146 10.0.2.15:5432 users:(("node",pid=28611,fd=21))
$ ss -tn state established '( sport = :3000 )' | tail -n +2 | wc -l
51
```

### Item 4
Work item: Clean survey dataset D6: remove duplicate respondents only and write clean/d6.parquet (raw file: 26,226 rows, 47 columns, 266 duplicate respondents; survey weights are normalised to mean 1)

System output (output file statistics):
```
clean/d6.parquet: 25,960 rows x 47 columns (5.5 MB)
interview_date: flagged 3
weight: min 31.0  max 487.0  mean 100.4  nulls 0
respondent_id: 25,960 unique of 25,960
Q10: nulls 364 (1.4%)
Q25: nulls 72 (0.3%)
Q06: nulls 34 (0.1%)
Q11: nulls 229 (0.9%)
Q40: nulls 32 (0.1%)
Q02: nulls 244 (0.9%)
Q16: nulls 335 (1.3%)
Q27: nulls 89 (0.3%)
Q37: nulls 378 (1.5%)
Q42: nulls 287 (1.1%)
Q39: nulls 291 (1.1%)
Q12: nulls 282 (1.1%)
Q33: nulls 8 (0.0%)
Q09: nulls 85 (0.3%)
Q35: nulls 349 (1.3%)
Q17: nulls 226 (0.9%)
Q18: nulls 378 (1.5%)
Q44: nulls 98 (0.4%)
Q43: nulls 239 (0.9%)
Q03: nulls 256 (1.0%)
```

### Item 5
Work item: Send invoice INV-2026-1698 (€ 7,825.41, PDF attached) to customer K-39, billing contact p.kraus@berger-moebel.at

System output (accounting and CRM entries):
```
receivables: INV-2026-1698 posted, customer K-39, € 7,825.41, status SENT
receivables: INV-2026-2393 posted, customer K-131, € 3,384.51, status SENT
receivables: INV-2026-2932 posted, customer K-134, € 2,811.32, status SENT
receivables: INV-2026-2523 posted, customer K-106, € 5,352.18, status SENT
receivables: INV-2026-2436 posted, customer K-128, € 6,166.64, status SENT
receivables: INV-2026-2944 posted, customer K-161, € 6,775.90, status SENT
receivables: INV-2026-2624 posted, customer K-147, € 3,110.44, status SENT
receivables: INV-2026-2411 posted, customer K-110, € 6,820.76, status SENT
receivables: INV-2026-2505 posted, customer K-185, € 4,162.40, status SENT
receivables: INV-2026-2350 posted, customer K-137, € 4,730.20, status SENT
receivables: INV-2026-2894 posted, customer K-165, € 3,749.76, status SENT
crm: activity 'offer sent' on K-121
crm: activity 'call logged' on K-122
crm: activity 'offer sent' on K-173
crm: activity 'call logged' on K-113
crm: activity 'call logged' on K-104
crm: activity 'invoice sent' on K-146
crm: activity 'offer sent' on K-116
crm: activity 'invoice sent' on K-39 (contact p.kraus@berger-moebel.at)
crm: activity 'offer sent' on K-176
crm: activity 'offer sent' on K-197
crm: activity 'call logged' on K-100
archive: invoice_INV-2026-1698.pdf stored (2 pages)
dunning: reminder for INV-2026-1698 scheduled 2026-11-21
receivables: exchange rate update skipped (EUR invoice)
```

### Item 6
Work item: Deploy notify-worker v5.9.1 (commit 2f4ceb5) to production (normally handles ~120 requests/min)

System output (socket and process table):
```
$ ss -ltnp
LISTEN 0 511 *:3000 *:* users:(("node",pid=22659,fd=21))
$ ps -o pid,lstart,cmd -C node
  PID STARTED        CMD
22659 Oct 22 10:41  node /srv/notify-worker/releases/5.9.1-2f4ceb5/server.js
$ ss -tnp
ESTAB 0 0 10.0.0.5:43240 10.0.1.22:6379 users:(("node",pid=22659,fd=34))
ESTAB 0 0 10.0.0.5:44055 10.0.7.10:5432 users:(("node",pid=22659,fd=27))
ESTAB 0 0 10.0.0.5:48160 10.0.7.10:5432 users:(("node",pid=22659,fd=39))
ESTAB 0 0 10.0.0.5:48558 10.0.1.22:6379 users:(("node",pid=22659,fd=31))
ESTAB 0 0 10.0.0.5:53686 10.0.7.10:5432 users:(("node",pid=22659,fd=33))
$ ss -tn state established '( sport = :3000 )' | tail -n +2 | wc -l
59
```

### Item 7
Work item: Send invoice INV-2026-1953 (€ 8,629.64, PDF attached) to customer K-66, billing contact a.kraus@lindner-logistik.de

System output (outgoing mail server log):
```
10:24:53 A47FF9121F: from=<billing@nordwerk-gmbh.at> to=<a.kraus@lindner-logistik.de> size=71045 subject='Invoice INV-2026-1953 (€ 8,629.64)'
10:12:16 6DBEF41629: from=<billing@nordwerk-gmbh.at> to=<m.wagner@gruber-elektro.at> size=52885
10:12:44 6E772BD198: from=<billing@nordwerk-gmbh.at> to=<a.bauer@pichler-agrar.at> size=59774
10:24:43 13D9477F7E: from=<billing@nordwerk-gmbh.at> to=<k.gruber@hofer-reisen.at> size=36276
10:29:32 313F1D95EC: from=<billing@nordwerk-gmbh.at> to=<k.wagner@pichler-agrar.at> size=35894
10:10:32 65D7046262: from=<billing@nordwerk-gmbh.at> to=<o.pichler@wagner-druck.at> size=45488
10:25:38 840B67DC30: from=<billing@nordwerk-gmbh.at> to=<c.gruber@wagner-druck.at> size=44455
10:17:13 8741DF8526: from=<billing@nordwerk-gmbh.at> to=<r.wagner@steiner-holz.de> size=67706
10:33:18 4C18712046: from=<billing@nordwerk-gmbh.at> to=<l.gruber@steiner-holz.de> size=45622
10:32:27 DE5B21BAAD: from=<billing@nordwerk-gmbh.at> to=<n.gruber@gruber-elektro.at> size=51767
10:38:21 6CD5E85A25: from=<billing@nordwerk-gmbh.at> to=<j.hofer@hofer-reisen.at> size=65054
10:33:11 292B134527: from=<billing@nordwerk-gmbh.at> to=<n.steiner@hofer-reisen.at> size=81720
10:13:57 3D4CBC56A8: from=<billing@nordwerk-gmbh.at> to=<j.hofer@pichler-agrar.at> size=65726
10:16:14 B17D1ED1A5: from=<billing@nordwerk-gmbh.at> to=<g.steiner@steiner-holz.de> size=58856
10:30:54 57A28ABF22: from=<billing@nordwerk-gmbh.at> to=<s.hofer@steiner-holz.de> size=46805
10:36:57 1B67DE8066: from=<billing@nordwerk-gmbh.at> to=<g.pichler@steiner-holz.de> size=75359
10:31:17 5EA101911C: from=<billing@nordwerk-gmbh.at> to=<n.wagner@wagner-druck.at> size=58722
10:27:28 3459248854: from=<billing@nordwerk-gmbh.at> to=<l.steiner@pichler-agrar.at> size=63893
10:14:41 FAC0289901: from=<billing@nordwerk-gmbh.at> to=<k.bauer@gruber-elektro.at> size=88612
10:24:53 A47FF9121F: 250 2.0.0 OK queued
10:16:32 362BED1309: from=<billing@nordwerk-gmbh.at> to=<c.hofer@pichler-agrar.at> size=86738
10:19:37 BD56D6DA56: from=<billing@nordwerk-gmbh.at> to=<r.wagner@wagner-druck.at> size=56636
10:24:53 A47FF9121F: status=deferred (421 4.7.0 greylisted, try again later)
10:24:53 A47FF9121F: spam score 3.1/5.0 (below threshold)
10:24:53 A47FF9121F: TLS handshake retry (1/3) ... ok
10:51:59 DE5B21BAAD: relay=mx1.gruber-elektro.at:25, status=sent (250 2.0.0 accepted)
10:57:52 65D7046262: relay=mx1.wagner-druck.at:25, status=sent (250 2.0.0 accepted)
10:47:35 6CD5E85A25: relay=mx1.hofer-reisen.at:25, status=sent (250 2.0.0 accepted)
10:52:28 8741DF8526: relay=mx1.steiner-holz.de:25, status=sent (250 2.0.0 accepted)
10:46:44 4C18712046: relay=mx1.steiner-holz.de:25, status=sent (250 2.0.0 accepted)
10:46:49 1B67DE8066: relay=mx1.steiner-holz.de:25, status=sent (250 2.0.0 accepted)
10:59:41 FAC0289901: relay=mx1.gruber-elektro.at:25, status=sent (250 2.0.0 accepted)
10:34:53 313F1D95EC: relay=mx1.pichler-agrar.at:25, status=sent (250 2.0.0 accepted)
10:36:22 6E772BD198: relay=mx1.pichler-agrar.at:25, status=sent (250 2.0.0 accepted)
10:41:11 5EA101911C: relay=mx1.wagner-druck.at:25, status=sent (250 2.0.0 accepted)
10:58:36 292B134527: relay=mx1.hofer-reisen.at:25, status=sent (250 2.0.0 accepted)
10:33:59 362BED1309: relay=mx1.pichler-agrar.at:25, status=sent (250 2.0.0 accepted)
10:57:16 57A28ABF22: relay=mx1.steiner-holz.de:25, status=sent (250 2.0.0 accepted)
10:38:53 BD56D6DA56: relay=mx1.wagner-druck.at:25, status=sent (250 2.0.0 accepted)
10:49:24 840B67DC30: relay=mx1.wagner-druck.at:25, status=sent (250 2.0.0 accepted)
10:49:12 B17D1ED1A5: relay=mx1.steiner-holz.de:25, status=sent (250 2.0.0 accepted)
10:49:39 A47FF9121F: relay=mx1.lindner-logistik.de:25, status=sent (250 2.0.0 accepted)
10:39:31 3459248854: relay=mx1.pichler-agrar.at:25, status=sent (250 2.0.0 accepted)
10:44:14 3D4CBC56A8: relay=mx1.pichler-agrar.at:25, status=sent (250 2.0.0 accepted)
10:30:46 6DBEF41629: relay=mx1.gruber-elektro.at:25, status=sent (250 2.0.0 accepted)
10:57:25 13D9477F7E: relay=mx1.hofer-reisen.at:25, status=sent (250 2.0.0 accepted)
```

### Item 8
Work item: Clean survey dataset D7: remove duplicate respondents only and write clean/d7.parquet (raw file: 23,556 rows, 47 columns, 76 duplicate respondents; survey weights are normalised to mean 1)

System output (job log):
```
job clean_d7 started
read raw/d7.csv: 23,556 rows, 47 columns
WARNING: 212 'income' values are non-numeric codes (-9 = refused), kept unchanged per codebook
read chunk 1/20: 1,177 rows
read chunk 2/20: 1,177 rows
read chunk 3/20: 1,177 rows
read chunk 4/20: 1,177 rows
read chunk 5/20: 1,177 rows
read chunk 6/20: 1,177 rows
read chunk 7/20: 1,177 rows
read chunk 8/20: 1,177 rows
read chunk 9/20: 1,177 rows
read chunk 10/20: 1,177 rows
read chunk 11/20: 1,177 rows
read chunk 12/20: 1,177 rows
read chunk 13/20: 1,177 rows
read chunk 14/20: 1,177 rows
read chunk 15/20: 1,177 rows
read chunk 16/20: 1,177 rows
read chunk 17/20: 1,177 rows
read chunk 18/20: 1,177 rows
read chunk 19/20: 1,177 rows
read chunk 20/20: 1,193 rows
dedupe on respondent_id: dropped 76 duplicates
dtypes: weight float64, income float64, age int64
memory: peak 1.9 GB
info: 3 respondents have interview_date in the future (flagged for review, not changed)
wrote clean/d7.parquet (47 columns)
job clean_d7 finished ✓ exit 0 (14.2s)
```

### Item 9
Work item: Deploy portal-frontend v5.8.2 (commit 295889e) to production (normally handles ~60 requests/min)

System output (socket and process table):
```
$ ss -ltnp
LISTEN 0 511 *:8080 *:* users:(("node",pid=25233,fd=21))
LISTEN 0 511 0.0.0.0:443 0.0.0.0:* users:(("nginx",pid=1044,fd=8))
LISTEN 0 128 0.0.0.0:22 0.0.0.0:* users:(("sshd",pid=812,fd=3))
LISTEN 0 511 *:9102 *:* users:(("node",pid=31233,fd=19))
LISTEN 0 511 *:9101 *:* users:(("node",pid=38525,fd=19))
LISTEN 0 511 *:9100 *:* users:(("node",pid=36433,fd=19))
$ ps -o pid,lstart,cmd -C node
  PID STARTED        CMD
12378 Oct 02 06:00  node /srv/metrics-agent/agent.js
25233 Oct 22 10:41  node /srv/portal-frontend/releases/5.8.2-295889e/server.js
31233 Oct 20 01:00  node /srv/admin-ui/current/server.js
38525 Oct 16 05:00  node /srv/webhooks/current/server.js
36433 Oct 13 03:00  node /srv/mailer/current/server.js
$ ss -tnp
ESTAB 0 0 10.0.0.5:8080 10.0.2.4:33342 users:(("node",pid=25233,fd=24))
ESTAB 0 0 10.0.0.5:8080 10.0.2.6:34386 users:(("node",pid=25233,fd=36))
ESTAB 0 0 10.0.0.5:8080 10.0.2.5:59516 users:(("node",pid=25233,fd=33))
SYN-SENT 0 1 10.0.0.5:41690 10.0.6.75:6379 users:(("node",pid=25233,fd=26))
ESTAB 0 0 10.0.0.5:8080 10.0.2.7:43289 users:(("node",pid=25233,fd=22))
ESTAB 0 0 10.0.0.5:8080 10.0.2.2:40677 users:(("node",pid=25233,fd=27))
ESTAB 0 0 10.0.0.5:8080 10.0.2.8:44966 users:(("node",pid=25233,fd=38))
ESTAB 0 0 10.0.0.5:8080 10.0.2.7:39207 users:(("node",pid=25233,fd=27))
ESTAB 0 0 10.0.0.5:54781 10.0.7.35:5432 users:(("node",pid=25233,fd=38))
ESTAB 0 0 10.0.0.5:8080 10.0.2.7:47187 users:(("node",pid=25233,fd=31))
ESTAB 0 0 10.0.0.5:55220 10.0.7.35:5432 users:(("node",pid=25233,fd=33))
SYN-SENT 0 1 10.0.0.5:58196 10.0.6.75:6379 users:(("node",pid=25233,fd=38))
ESTAB 0 0 10.0.0.5:8080 10.0.2.5:50441 users:(("node",pid=25233,fd=32))
ESTAB 0 0 10.0.0.5:58849 10.0.7.35:5432 users:(("node",pid=25233,fd=24))
ESTAB 0 0 10.0.0.5:8080 10.0.2.9:30708 users:(("node",pid=25233,fd=27))
ESTAB 0 0 10.0.0.5:8080 10.0.2.4:38150 users:(("node",pid=25233,fd=30))
ESTAB 0 0 10.0.0.5:8080 10.0.2.7:37108 users:(("node",pid=25233,fd=21))
ESTAB 0 0 10.0.0.5:8080 10.0.2.8:38196 users:(("node",pid=25233,fd=20))
ESTAB 0 0 10.0.0.5:8080 10.0.2.7:36585 users:(("node",pid=25233,fd=40))
ESTAB 0 0 10.0.0.5:8080 10.0.2.3:44656 users:(("node",pid=25233,fd=26))
ESTAB 0 0 10.0.0.5:8080 10.0.2.3:44545 users:(("node",pid=25233,fd=34))
ESTAB 0 0 10.0.0.5:8080 10.0.2.6:45360 users:(("node",pid=25233,fd=25))
ESTAB 0 0 10.0.0.5:8080 10.0.2.9:32704 users:(("node",pid=25233,fd=30))
ESTAB 0 0 10.0.0.5:8080 10.0.2.2:40395 users:(("node",pid=25233,fd=20))
ESTAB 0 0 10.0.0.5:8080 10.0.2.6:33494 users:(("node",pid=25233,fd=27))
$ df -h /srv | tail -1
/dev/nvme0n1p2  200G  141G   59G  71% /srv
$ uptime
 10:42:11 up 23 days,  load average: 0.41, 0.38, 0.35
$ ss -tn state established '( sport = :8080 )' | tail -n +2 | wc -l
23
```

### Item 10
Work item: Clean survey dataset D2: remove duplicate respondents only and write clean/d2.parquet (raw file: 31,816 rows, 47 columns, 150 duplicate respondents; survey weights are normalised to mean 1)

System output (output file statistics):
```
clean/d2.parquet: 31,666 rows x 47 columns (6.6 MB)
weight: min 0.31  max 4.87  mean 1.00  nulls 0
Q16: nulls 164 (0.5%)
Q44: nulls 41 (0.1%)
Q15: nulls 381 (1.2%)
Q09: nulls 208 (0.7%)
Q23: nulls 88 (0.3%)
Q33: nulls 159 (0.5%)
Q01: nulls 75 (0.2%)
Q35: nulls 243 (0.8%)
Q07: nulls 10 (0.0%)
Q32: nulls 177 (0.6%)
Q26: nulls 186 (0.6%)
Q14: nulls 319 (1.0%)
Q29: nulls 371 (1.2%)
Q30: nulls 20 (0.1%)
Q39: nulls 329 (1.0%)
Q12: nulls 19 (0.1%)
respondent_id: 31,666 unique of 31,666
Q40: nulls 200 (0.6%)
Q19: nulls 115 (0.4%)
Q18: nulls 129 (0.4%)
Q31: nulls 218 (0.7%)
income: non-numeric codes 212 (0.7%)
```

### Item 11
Work item: Deploy portal-frontend v4.8.4 (commit f39057d) to production (normally handles ~390 requests/min)

System output (socket and process table):
```
$ ss -ltnp
LISTEN 0 511 *:5000 *:* users:(("node",pid=21260,fd=21))
$ ps -o pid,lstart,cmd -C node
  PID STARTED        CMD
21260 Oct 22 10:41  node /srv/portal-frontend/releases/4.8.4-f39057d/server.js
$ ss -tnp
ESTAB 0 0 10.0.0.5:42072 10.0.4.91:6379 users:(("node",pid=21260,fd=32))
ESTAB 0 0 10.0.0.5:54440 10.0.4.91:6379 users:(("node",pid=21260,fd=27))
SYN-SENT 0 1 10.0.0.5:54891 10.0.5.13:5432 users:(("node",pid=21260,fd=24))
$ ss -tn state established '( sport = :5000 )' | tail -n +2 | wc -l
13
```

### Item 12
Work item: Deploy billing-api v3.3.3 (commit eb07954) to production (normally handles ~130 requests/min)

System output (HTTP endpoint checks):
```
$ curl -s http://localhost:8443/version
{"service": "billing-api", "build": {"version": "3.3.3", "commit": "eb07954"}, "uptime_s": 85}
$ curl -s -m 2 http://localhost:8443/health
curl: (28) Operation timed out after 2000 milliseconds
$ curl -s -m 5 http://localhost:8443/health   # retry after warm-up
{"status": "ok", "checks": {"db": {"ok": true, "latency_ms": 6}, "cache": {"ok": true}}, "db_pool": {"size": 20, "active": 11, "waiting": 0}, "cache_shards": {"up": 4, "total": 4}}
$ curl -s http://localhost:8443/health
{"status": "ok", "checks": {"db": {"ok": true, "latency_ms": 6}, "cache": {"ok": true}}, "db_pool": {"size": 20, "active": 11, "waiting": 0}, "cache_shards": {"up": 4, "total": 4}}
$ curl -s http://localhost:8443/api/v1/config/public
{"locale": "de-AT", "features": 15}
$ curl -s http://localhost:8443/api/v1/config/public
{"locale": "de-AT", "features": 15}
$ curl -s http://localhost:8443/metrics | grep ^http_requests_total
http_requests_total{code="200"} 832
http_requests_total{code="500"} 3
$ curl -s http://localhost:8443/metrics | grep -c ^http_
69
$ curl -s http://localhost:8443/api/v1/ping
{"pong": true}
$ curl -s http://localhost:8443/api/v1/config/public
{"locale": "de-AT", "features": 15}
```

Respond with a JSON array only: [{"item": 1, "works": true or false, "confidence": number between 0 and 1}, ...] with exactly one entry per item
````
