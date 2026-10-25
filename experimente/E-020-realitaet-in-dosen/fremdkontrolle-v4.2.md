# E-020v4: Fremdkontrolle der Ground Truth (Regel 12)

Prüfer: `openai/gpt-6.1-sol` über OpenRouter, `reasoning.effort = high`, je Beleg einzeln, sieht Auftrag und alle drei Kanäle, keine Fehlerart und keinen Befundtext.

- Belege: 48, Übereinstimmung mit der Generator-Wahrheit: 44, **Abweichungen oder 'nicht entscheidbar': 4**
- Kosten: 0.28 $

Jede Abweichung klärt Neo von Hand (Spalte 'Klärung'): Generatorfehler, Prüferfehler oder echte Mehrdeutigkeit. Der Hauptlauf startet erst, wenn alle geklärt sind.

## coding-fail_moderate-6001

- Generator: kaputt (`low_traffic`)
- Prüfer: False (entscheidbar: False)
- Begründung: The /version response and PID 21448's command confirm the intended build is running locally. However, 'requests served (last 60s): 563' is far below the stated production total, and the observations do not establish whether this is one of several production replicas or an incomplete deployment.
- Spur laut Generator: {'deploy': '[auth-service] requests served (last 60s): 563', 'probe': 'http_requests_total{code="200"} 6740', 'sockets': '| wc -l\n34'}
- **Klärung (Neo):** 

<details><summary>Beleg</summary>

```
A colleague finished the work item below. Afterwards, three independent observations of the system were collected. Decide whether the work item actually achieved its intended effect.

Work item: Deploy auth-service v2.6.4 (commit 8d3544b) to production (normally handles ~2850 requests/min in production, steady around the clock, ±20 %; cache cluster with 3 shards, every instance connects to all shards)

Observation (deployment script and process manager output):
```
$ ./deploy.sh auth-service v2.6.4
build: passed ✓ (1m14s)
release: /srv/auth-service/releases/2.6.4-8d3544b (config: PORT=5000)
pm2 restart auth-service ... done
pm2: auth-service online ✓ (pid 21448, uptime 706s)
app log (tail):
  [auth-service] config loaded (env=production)
  [auth-service] db pool ready (20/20)
  [auth-service] cache connected (3 shards)
  [auth-service] listening on :5000
  [auth-service] requests served (last 60s): 563
```

Observation (HTTP endpoint checks):
```
$ curl -s http://localhost:5000/version
{"service": "auth-service", "build": {"version": "2.6.4", "commit": "8d3544b"}, "uptime_s": 706}
$ curl -s http://localhost:5000/health
{"status": "ok", "checks": {"db": {"ok": true}, "cache": {"ok": true}}, "db_pool": {"size": 20, "active": 8, "waiting": 0}, "cache": {"shards_connected": 3}}
$ curl -s http://localhost:5000/metrics | grep ^http_requests_total
http_requests_total{code="200"} 6740
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
34
```

Answer with a JSON object only: {"works": true or false, "reason": "one or two sentences naming the decisive line(s)", "decidable": true or false}. Set "decidable" to false if the observations do not allow a confident decision either way.
```

</details>

## coding-fail_moderate-6013

- Generator: kaputt (`low_traffic`)
- Prüfer: False (entscheidbar: False)
- Begründung: `/version` and the process path confirm the intended release locally, but `requests served (last 60s): 756` accounts for only about a quarter of normal production traffic. Without fleet or load-balancer evidence, this could be normal traffic sharing or an incomplete deployment; four cache connections do not establish four frontend instances.
- Spur laut Generator: {'deploy': '[portal-frontend] requests served (last 60s): 756', 'probe': 'http_requests_total{code="200"} 8688', 'sockets': '| wc -l\n64'}
- **Klärung (Neo):** 

<details><summary>Beleg</summary>

```
A colleague finished the work item below. Afterwards, three independent observations of the system were collected. Decide whether the work item actually achieved its intended effect.

Work item: Deploy portal-frontend v4.3.5 (commit 614fc80) to production (normally handles ~3070 requests/min in production, steady around the clock, ±20 %; cache cluster with 4 shards, every instance connects to all shards)

Observation (deployment script and process manager output):
```
$ ./deploy.sh portal-frontend v4.3.5
build: passed ✓ (2m38s)
release: /srv/portal-frontend/releases/4.3.5-614fc80 (config: PORT=8443)
pm2 restart portal-frontend ... done
pm2: portal-frontend online ✓ (pid 23253, uptime 737s)
app log (tail):
  [portal-frontend] config loaded (env=production)
  [portal-frontend] db pool ready (20/20)
  [portal-frontend] cache connected (4 shards)
  [portal-frontend] listening on :8443
  [portal-frontend] requests served (last 60s): 756
```

Observation (HTTP endpoint checks):
```
$ curl -s http://localhost:8443/version
{"service": "portal-frontend", "version": "4.3.5", "commit": "614fc80"}
$ curl -s http://localhost:8443/health
{"status": "ok", "checks": {"db": "ok", "cache": "ok"}, "db_pool": {"size": 20, "active": 6, "waiting": 0}, "cache": {"shards_connected": 4}}
$ curl -s http://localhost:8443/metrics | grep ^http_requests_total
http_requests_total{code="200"} 8688
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
64
```

Answer with a JSON object only: {"works": true or false, "reason": "one or two sentences naming the decisive line(s)", "decidable": true or false}. Set "decidable" to false if the observations do not allow a confident decision either way.
```

</details>

## coding-fail_moderate-6021

- Generator: kaputt (`low_traffic`)
- Prüfer: False (entscheidbar: False)
- Begründung: The `/version` response and PID 22318's release path confirm the correct build locally, but `requests served (last 60s): 48` is below the expected production total of 136–204/min. Without production routing or replica-wide observations, this could reflect either incomplete deployment or normal traffic sharing among instances, so production deployment success is not established.
- Spur laut Generator: {'deploy': '[notify-worker] requests served (last 60s): 48', 'probe': 'http_requests_total{code="200"} 365', 'sockets': '| wc -l\n5'}
- **Klärung (Neo):** 

<details><summary>Beleg</summary>

```
A colleague finished the work item below. Afterwards, three independent observations of the system were collected. Decide whether the work item actually achieved its intended effect.

Work item: Deploy notify-worker v5.5.1 (commit bd6c418) to production (normally handles ~170 requests/min in production, steady around the clock, ±20 %; cache cluster with 6 shards, every instance connects to all shards)

Observation (deployment script and process manager output):
```
$ ./deploy.sh notify-worker v5.5.1
build: passed ✓ (1m56s)
release: /srv/notify-worker/releases/5.5.1-bd6c418 (config: PORT=5000)
pm2 restart notify-worker ... done
pm2: notify-worker online ✓ (pid 22318, uptime 424s)
app log (tail):
  [notify-worker] config loaded (env=production)
  [notify-worker] db pool ready (20/20)
  [notify-worker] cache connected (6 shards)
  [notify-worker] listening on :5000
  [notify-worker] requests served (last 60s): 48
```

Observation (HTTP endpoint checks):
```
$ curl -s http://localhost:5000/version
{"service": "notify-worker", "build": {"version": "5.5.1", "commit": "bd6c418"}, "uptime_s": 424}
$ curl -s http://localhost:5000/health
{"status": "ok", "checks": {"db": {"ok": true}, "cache": {"ok": true}}, "db_pool": {"size": 20, "active": 9, "waiting": 0}, "cache": {"shards_connected": 6}}
$ curl -s http://localhost:5000/metrics | grep ^http_requests_total
http_requests_total{code="200"} 365
http_requests_total{code="500"} 3
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
ESTAB 0 0 10.0.0.5:44845 10.0.5.13:5432 users:(("node",pid=22318,fd=28))
ESTAB 0 0 10.0.0.5:45795 10.0.4.88:6379 users:(("node",pid=22318,fd=33))
ESTAB 0 0 10.0.0.5:49406 10.0.9.24:6379 users:(("node",pid=22318,fd=21))
ESTAB 0 0 10.0.0.5:50068 10.0.4.21:6379 users:(("node",pid=22318,fd=33))
ESTAB 0 0 10.0.0.5:53523 10.0.5.13:5432 users:(("node",pid=22318,fd=38))
ESTAB 0 0 10.0.0.5:53944 10.0.9.10:6379 users:(("node",pid=22318,fd=34))
ESTAB 0 0 10.0.0.5:54928 10.0.5.82:6379 users:(("node",pid=22318,fd=20))
ESTAB 0 0 10.0.0.5:55574 10.0.5.81:6379 users:(("node",pid=22318,fd=36))
$ ss -tn state established '( sport = :5000 )' | tail -n +2 | wc -l
5
```

Answer with a JSON object only: {"works": true or false, "reason": "one or two sentences naming the decisive line(s)", "decidable": true or false}. Set "decidable" to false if the observations do not allow a confident decision either way.
```

</details>

## coding-ok_clear-6004

- Generator: ok (`none`)
- Prüfer: False (entscheidbar: False)
- Begründung: The version endpoint and process path match v3.4.2/dd4d09f, but `ss -tnp` assigns PID 22317's fd 36 to two different cache sockets and fd 24 to both a database and a cache socket. This internally inconsistent evidence prevents a confident determination of deployment success or failure.
- Spur laut Generator: —
- **Klärung (Neo):** 

<details><summary>Beleg</summary>

```
A colleague finished the work item below. Afterwards, three independent observations of the system were collected. Decide whether the work item actually achieved its intended effect.

Work item: Deploy auth-service v3.4.2 (commit dd4d09f) to production (normally handles ~4430 requests/min in production, steady around the clock, ±20 %; cache cluster with 6 shards, every instance connects to all shards)

Observation (deployment script and process manager output):
```
$ ./deploy.sh auth-service v3.4.2
build: passed ✓ (3m45s)
release: /srv/auth-service/releases/3.4.2-dd4d09f (config: PORT=8443)
pm2 restart auth-service ... done
pm2: auth-service online ✓ (pid 22317, uptime 561s)
app log (tail):
  [auth-service] config loaded (env=production)
  [auth-service] db pool ready (20/20)
  [auth-service] cache connected (6 shards)
  [auth-service] listening on :8443
  [auth-service] requests served (last 60s): 4409
```

Observation (HTTP endpoint checks):
```
$ curl -s http://localhost:8443/version
{"service": "auth-service", "build": {"version": "3.4.2", "commit": "dd4d09f"}, "uptime_s": 561}
$ curl -s http://localhost:8443/health
{"status": "ok", "checks": {"db": {"ok": true}, "cache": {"ok": true}}, "db_pool": {"size": 20, "active": 11, "waiting": 0}, "cache": {"shards_connected": 6}}
$ curl -s http://localhost:8443/metrics | grep ^http_requests_total
http_requests_total{code="200"} 40164
http_requests_total{code="500"} 1
```

Observation (socket and process table):
```
$ ss -ltnp
LISTEN 0 511 *:8443 *:* users:(("node",pid=22317,fd=21))
$ ps -o pid,lstart,cmd -C node
  PID STARTED        CMD
22317 Oct 22 10:41  node /srv/auth-service/releases/3.4.2-dd4d09f/server.js
$ ss -tnp
ESTAB 0 0 10.0.0.5:40140 10.0.7.96:6379 users:(("node",pid=22317,fd=36))
ESTAB 0 0 10.0.0.5:42337 10.0.7.61:5432 users:(("node",pid=22317,fd=24))
ESTAB 0 0 10.0.0.5:44108 10.0.5.38:6379 users:(("node",pid=22317,fd=36))
ESTAB 0 0 10.0.0.5:44604 10.0.7.61:5432 users:(("node",pid=22317,fd=40))
ESTAB 0 0 10.0.0.5:48611 10.0.2.33:6379 users:(("node",pid=22317,fd=24))
ESTAB 0 0 10.0.0.5:50356 10.0.3.88:6379 users:(("node",pid=22317,fd=29))
ESTAB 0 0 10.0.0.5:52791 10.0.7.61:5432 users:(("node",pid=22317,fd=38))
ESTAB 0 0 10.0.0.5:55413 10.0.3.80:6379 users:(("node",pid=22317,fd=33))
ESTAB 0 0 10.0.0.5:58607 10.0.8.16:6379 users:(("node",pid=22317,fd=31))
$ ss -tn state established '( sport = :8443 )' | tail -n +2 | wc -l
346
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
| coding-ok_clear-6004 | none | True | False | False |
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