# E-024: Fremdkontrolle der Ground Truth (Regel 12)

Prüfer: `openai/gpt-6.1-sol` über OpenRouter, `reasoning.effort = high`, je Beleg einzeln, sieht Auftrag und alle drei Kanäle, keine Fehlerart und keinen Befundtext.

- Belege: 48, Übereinstimmung mit der Generator-Wahrheit: 47, **Abweichungen oder 'nicht entscheidbar': 1**
- Kosten: 0.30 $

Jede Abweichung klärt Neo von Hand (Spalte 'Klärung'): Generatorfehler, Prüferfehler oder echte Mehrdeutigkeit. Der Hauptlauf startet erst, wenn alle geklärt sind.

## coding-ok_clear-7009

- Generator: ok (`none`)
- Prüfer: False (entscheidbar: True)
- Begründung: Although /version and the process path confirm v4.6.1 commit 790504e, the metrics show only 970 requests over 515 seconds of uptime—about 113 requests/min, below the stated production range of 120–180 requests/min for the single instance.
- Spur laut Generator: —
- **Klärung (Neo, 23.10. 19:41):** Echte Mehrdeutigkeit, Zähler über die Laufzeit gegen Last pro Minute. Neo hat nach Claudes Empfehlung gefragt und den Lauf freigegeben: als Grenzfall kennzeichnen (`e024.GRENZFAELLE`), Sensitivitätsanalyse ohne ihn. 

<details><summary>Beleg</summary>

```
A colleague finished the work item below. Afterwards, three independent observations of the system were collected. Decide whether the work item actually achieved its intended effect.

Work item: Deploy billing-api v4.6.1 (commit 790504e) to production (runs as a single production instance that normally handles ~150 requests/min, steady around the clock, ±20 %; cache cluster with 8 shards, every instance connects to all shards)

Observation (deployment script and process manager output):
```
$ ./deploy.sh billing-api v4.6.1
build: passed ✓ (2m10s)
release: /srv/billing-api/releases/4.6.1-790504e (config: PORT=8443)
pm2 restart billing-api ... done
pm2: billing-api online ✓ (pid 20467, uptime 515s)
app log (tail):
  [billing-api] config loaded (env=production)
  [billing-api] db pool ready (20/20)
  [billing-api] cache connected (8 shards)
  [billing-api] listening on :8443
  [billing-api] requests served (last 60s): 124
```

Observation (HTTP endpoint checks):
```
$ curl -s http://localhost:8443/version
{"service": "billing-api", "build": {"version": "4.6.1", "commit": "790504e"}, "uptime_s": 515}
$ curl -s http://localhost:8443/health
{"status": "ok", "checks": {"db": {"ok": true}, "cache": {"ok": true}}, "db_pool": {"size": 20, "active": 12, "waiting": 0}, "cache": {"shards_connected": 8}}
$ curl -s http://localhost:8443/metrics | grep ^http_requests_total
http_requests_total{code="200"} 970
http_requests_total{code="500"} 0
```

Observation (socket and process table):
```
$ ss -ltnp
LISTEN 0 511 *:8443 *:* users:(("node",pid=20467,fd=21))
$ ps -o pid,lstart,cmd -C node
  PID STARTED        CMD
20467 Oct 22 10:41  node /srv/billing-api/releases/4.6.1-790504e/server.js
$ ss -tnp
ESTAB 0 0 10.0.0.5:40700 10.0.1.95:5432 users:(("node",pid=20467,fd=38))
ESTAB 0 0 10.0.0.5:42349 10.0.4.67:6379 users:(("node",pid=20467,fd=31))
ESTAB 0 0 10.0.0.5:42420 10.0.7.58:6379 users:(("node",pid=20467,fd=34))
ESTAB 0 0 10.0.0.5:45339 10.0.4.26:6379 users:(("node",pid=20467,fd=41))
ESTAB 0 0 10.0.0.5:50510 10.0.7.95:6379 users:(("node",pid=20467,fd=39))
ESTAB 0 0 10.0.0.5:52862 10.0.8.54:6379 users:(("node",pid=20467,fd=40))
ESTAB 0 0 10.0.0.5:53321 10.0.1.91:6379 users:(("node",pid=20467,fd=20))
ESTAB 0 0 10.0.0.5:53615 10.0.1.95:5432 users:(("node",pid=20467,fd=37))
ESTAB 0 0 10.0.0.5:53701 10.0.4.19:6379 users:(("node",pid=20467,fd=24))
ESTAB 0 0 10.0.0.5:56971 10.0.1.87:6379 users:(("node",pid=20467,fd=32))
ESTAB 0 0 10.0.0.5:58745 10.0.1.95:5432 users:(("node",pid=20467,fd=23))
$ ss -tn state established '( sport = :8443 )' | tail -n +2 | wc -l
12
```

Answer with a JSON object only: {"works": true or false, "reason": "one or two sentences naming the decisive line(s)", "decidable": true or false}. Set "decidable" to false if the observations do not allow a confident decision either way.
```

</details>

## Alle Urteile

| Beleg | Fehlerart | Wahrheit | Prüfer | entscheidbar |
|---|---|---|---|---|
| business-fail_moderate-7011 | wrong_terms | False | False | True |
| business-fail_moderate-7016 | bounced | False | False | True |
| business-fail_moderate-7021 | wrong_contact | False | False | True |
| business-fail_subtle-7003 | wrong_contact | False | False | True |
| business-fail_subtle-7004 | amount_mismatch | False | False | True |
| business-fail_subtle-7008 | amount_mismatch | False | False | True |
| business-fail_subtle-7010 | bounced | False | False | True |
| business-fail_subtle-7016 | amount_mismatch | False | False | True |
| business-fail_subtle-7017 | wrong_terms | False | False | True |
| business-fail_subtle-7019 | wrong_contact | False | False | True |
| business-fail_subtle-7021 | wrong_terms | False | False | True |
| business-fail_subtle-7022 | bounced | False | False | True |
| business-ok_clear-7003 | none | True | True | True |
| business-ok_clear-7019 | none | True | True | True |
| business-ok_noisy-7013 | none | True | True | True |
| business-ok_noisy-7018 | none | True | True | True |
| coding-fail_moderate-7002 | db_down | False | False | True |
| coding-fail_moderate-7014 | db_down | False | False | True |
| coding-fail_moderate-7015 | cache_partial | False | False | True |
| coding-fail_moderate-7017 | low_traffic | False | False | True |
| coding-fail_moderate-7023 | cache_partial | False | False | True |
| coding-fail_subtle-7001 | cache_partial | False | False | True |
| coding-fail_subtle-7002 | stale_process | False | False | True |
| coding-fail_subtle-7007 | low_traffic | False | False | True |
| coding-fail_subtle-7010 | stale_process | False | False | True |
| coding-fail_subtle-7012 | db_down | False | False | True |
| coding-fail_subtle-7022 | stale_process | False | False | True |
| coding-fail_subtle-7023 | low_traffic | False | False | True |
| coding-ok_clear-7009 | none | True | False | True |
| coding-ok_clear-7022 | none | True | True | True |
| coding-ok_noisy-7010 | none | True | True | True |
| coding-ok_noisy-7015 | none | True | True | True |
| research-fail_moderate-7003 | column_loss | False | False | True |
| research-fail_moderate-7004 | row_loss | False | False | True |
| research-fail_moderate-7016 | row_loss | False | False | True |
| research-fail_subtle-7003 | weights_misscaled | False | False | True |
| research-fail_subtle-7004 | duplicates_partial | False | False | True |
| research-fail_subtle-7007 | weights_misscaled | False | False | True |
| research-fail_subtle-7009 | column_loss | False | False | True |
| research-fail_subtle-7012 | duplicates_partial | False | False | True |
| research-fail_subtle-7015 | weights_misscaled | False | False | True |
| research-fail_subtle-7016 | duplicates_partial | False | False | True |
| research-fail_subtle-7021 | column_loss | False | False | True |
| research-fail_subtle-7022 | row_loss | False | False | True |
| research-ok_clear-7000 | none | True | True | True |
| research-ok_clear-7012 | none | True | True | True |
| research-ok_noisy-7009 | none | True | True | True |
| research-ok_noisy-7011 | none | True | True | True |