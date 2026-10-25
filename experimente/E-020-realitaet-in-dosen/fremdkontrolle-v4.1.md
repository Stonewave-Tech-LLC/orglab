# E-020v4: Fremdkontrolle der Ground Truth (Regel 12)

Prüfer: `openai/gpt-6.1-sol` über OpenRouter, `reasoning.effort = high`, je Beleg einzeln, sieht Auftrag und alle drei Kanäle, keine Fehlerart und keinen Befundtext.

- Belege: 48, Übereinstimmung mit der Generator-Wahrheit: 47, **Abweichungen oder 'nicht entscheidbar': 1**
- Kosten: 0.26 $

Jede Abweichung klärt Neo von Hand (Spalte 'Klärung'): Generatorfehler, Prüferfehler oder echte Mehrdeutigkeit. Der Hauptlauf startet erst, wenn alle geklärt sind.

## coding-fail_moderate-6021

- Generator: kaputt (`low_traffic`)
- Prüfer: False (entscheidbar: False)
- Begründung: The release path and `/version` confirm that v5.5.1 (bd6c418) is running, but `requests served (last 60s): 2` is far below the normal ~20/min and could reflect only local checks. Without production-routing evidence, these observations cannot establish whether the new build is serving production traffic.
- Spur laut Generator: {'deploy': '[notify-worker] requests served (last 60s): 2', 'probe': 'http_requests_total{code="200"} 2', 'sockets': '| wc -l\n1'}
- **Klärung (Neo):** 

<details><summary>Beleg</summary>

```
A colleague finished the work item below. Afterwards, three independent observations of the system were collected. Decide whether the work item actually achieved its intended effect.

Work item: Deploy notify-worker v5.5.1 (commit bd6c418) to production (normally handles ~20 requests/min, steady around the clock; cache cluster with 6 shards)

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

## Alle Urteile

| Beleg | Fehlerart | Wahrheit | Prüfer | entscheidbar |
|---|---|---|---|---|
| business-fail_moderate-6006 | amount_mismatch | False | False | True |
| business-fail_moderate-6009 | wrong_contact | False | False | True |
| business-fail_moderate-6011 | wrong_terms | False | False | True |
| business-fail_moderate-6015 | wrong_terms | False | False | True |
| business-fail_moderate-6018 | amount_mismatch | False | False | True |
| business-fail_moderate-6021 | wrong_contact | False | False | True |
| business-fail_subtle-6001 | wrong_terms | False | False | True |
| business-fail_subtle-6002 | bounced | False | False | True |
| business-fail_subtle-6003 | wrong_contact | False | False | True |
| business-fail_subtle-6006 | bounced | False | False | True |
| business-fail_subtle-6008 | amount_mismatch | False | False | True |
| business-fail_subtle-6010 | bounced | False | False | True |
| business-ok_clear-6001 | none | True | True | True |
| business-ok_clear-6008 | none | True | True | True |
| business-ok_noisy-6003 | none | True | True | True |
| business-ok_noisy-6008 | none | True | True | True |
| coding-fail_moderate-6001 | low_traffic | False | False | True |
| coding-fail_moderate-6003 | cache_partial | False | False | True |
| coding-fail_moderate-6013 | low_traffic | False | False | True |
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
| research-ok_clear-6004 | none | True | True | True |
| research-ok_clear-6010 | none | True | True | True |
| research-ok_noisy-6002 | none | True | True | True |
| research-ok_noisy-6016 | none | True | True | True |