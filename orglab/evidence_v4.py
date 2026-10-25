"""Belegmaterial v4 (D-018, für E-020): Fehlerarten, deren Spur nur mit dem Sollwert entscheidbar ist ("spec-rein").

Warum: In v3 verraten sich die Fehlerarten, die SPEC messen sollten, auch ohne Sollwert ("0 kB", "0 pages",
"mean 100", "requests: 0", "0/4 shards"). Dort misst SPEC nichts (Grok-Gutachten 1 und 2, CLAUDE.md Regel 17).

Prinzipien:
  - Spec-reine Spuren sehen ohne Norm plausibel aus: keine Nullen, keine Nenner ("k/N"), keine runden Konventionen
    (Mittelwert 1 oder 100), keine Fehlermeldungen. Ok- und Fehlerwerte stammen aus überlappenden Verteilungen.
  - Die Normen sind je Vorgang verschieden (Last, Shard-Zahl, Kontakt, Zielpopulation, Duplikatzahl, Spaltenzahl),
    damit kein fester Wert gelernt werden kann.
  - Jede Fehlerart hinterlässt in jedem Kanal eine Spur (wie v2/v3), sodass jeder Kanal mit Norm allein entscheidbar ist.
  - Das Runbook ist abschnittsweise: `lookup(ev, topic)` liefert nur passende Abschnitte, sonst "No entry".
  - Fehlerarten werden je Seed deterministisch und balanciert zugewiesen (Grok-Gutachten 2: Primärarten nicht dem
    Zufall überlassen). Mit Kanal = Seed mod 3 (E-020 ZUGANG=0) ist jede Kombination Fehlerart × Kanal alle 12 Seeds
    genau einmal vertreten.

v4.1 (23.10., nach GPT-Lecktest und Fremdkontrolle, `notizen/29`): Research-Auftrag nennt die Neukalibrierung der
Gewichte (sonst widerspricht "rescaled" dem Auftrag), `attachment_missing` ersetzt durch `wrong_terms` (fehlendes PDF ist
auch ohne Norm verdächtig, Konventionsleck), übliche Last mit "steady around the clock" (sonst mehrdeutig).

v3.1 (`orglab.evidence`) bleibt unverändert, weil E-021 und E-022 darauf präregistriert sind.
"""

from __future__ import annotations

import datetime
import json
import math
import random
import re
from dataclasses import asdict, dataclass, field

from .evidence import CHANNEL_DESC, CHANNELS, KINDS_V2, NOISE_BLOCKS, PAD_LINES, _hex, _pad, _render

KINDS = KINDS_V2
SERVICES = ["auth-service", "billing-api", "search-indexer", "notify-worker", "portal-frontend"]
# Je Domäne vier Fehlerarten; spec-rein (Primärmenge für E-020) sind die in PRIMARY.
FAULTS = {"coding": ("stale_process", "low_traffic", "db_down", "cache_partial"),
          "business": ("bounced", "wrong_contact", "amount_mismatch", "wrong_terms"),
          "research": ("row_loss", "weights_misscaled", "duplicates_partial", "column_loss")}
PRIMARY = ("low_traffic", "cache_partial", "wrong_contact", "wrong_terms", "weights_misscaled",
           "duplicates_partial", "column_loss")
FINDINGS = {
    "none": "It worked as intended.",
    "stale_process": "It did not work: the old release kept running and served all traffic.",
    "db_down": "It did not work: the new release ran without a working database connection.",
    "low_traffic": "It did not work: production traffic was still routed to the old release; the new one only got a trickle.",
    "cache_partial": "It did not work: the new release was connected to only part of the cache cluster.",
    "bounced": "It did not work: the invoice never reached the customer.",
    "amount_mismatch": "It did not work: the invoice was sent with the wrong amount.",
    "wrong_contact": "It did not work: the invoice went to the wrong person at the customer.",
    "wrong_terms": "It did not work: the invoice was issued with the wrong payment terms (wrong due date).",
    "row_loss": "It did not work: most respondents were lost during cleaning.",
    "weights_misscaled": "It did not work: the survey weights were scaled to the wrong population total.",
    "duplicates_partial": "It did not work: most duplicate respondents were not removed.",
    "column_loss": "It did not work: several columns were lost in the output.",
}
# Schlüsselwörter je Runbook-Abschnitt (Abfrage per Teilwort im Topic, Kleinschreibung)
TOPIC_KEYS = {
    "traffic": ("traffic", "request", "load", "rate", "throughput", "rpm"),
    "cache": ("cache", "redis", "shard"),
    "database": ("database", "db", "postgres", "pool"),
    "ports": ("port", "listen"),
    "logging": ("log",), "on-call": ("on-call", "oncall", "pager", "incident"), "release": ("release", "deploy", "rollback"),
    "contacts": ("contact", "recipient", "customer", "address", "email address"),
    "attachments": ("attach", "pdf", "document"),
    "dunning": ("dunning", "reminder", "overdue"), "payment": ("payment", "link", "pay"),
    "templates": ("template", "language", "subject"),
    "duplicates": ("duplicate", "dedup", "respondent"),
    "weights": ("weight", "population", "calibrat"),
    "schema": ("schema", "column", "variable"),
    "codes": ("code", "missing", "refused", "-9"), "storage": ("storage", "parquet", "file", "path"),
}


@dataclass
class EvidenceV4:
    id: str
    domain: str
    kind: str
    works: bool
    item: str                    # SPEC=0: Auftrag mit den Hintergrund-Sollwerten
    item_short: str              # SPEC=1: Auftrag ohne sie
    channels: dict[str, str]
    subtlety: int
    fault: str
    finding: str
    signatures: dict[str, str]   # je Kanal die Fehlerspur (nur Tests/Auswertung)
    runbook_sections: dict[str, str]
    norms: dict[str, str]        # Normwerte als Text (nur Tests: dürfen bei spec-reinen Fehlern nicht in den Kanälen stehen)
    primary: bool = False
    version: str = "v4.3"
    runbook: str = field(default="")
    entities: list[str] = field(default_factory=list)   # Einheit des Vorgangs (Dienst, Rechnung, Kunde, Datensatz)

    def __post_init__(self) -> None:
        self.runbook = "\n".join(f"[{k}] {v}" for k, v in self.runbook_sections.items())


LOOKUP_VERSION = "seite-2"   # 23.10.: seitenbasiert (Pilot 1), v4.2 realistische Seiten und Wortgrenzen (Grok-Gutachten 3)


def entities_for(domain: str, item: str) -> list[str]:
    """Wörter, mit denen man im Wiki die Seite dieses Vorgangs findet (aus dem Auftrag, ohne Zufall)."""
    w = item.split()
    if domain == "coding":
        return [w[1].lower()]                                                   # Dienstname
    if domain == "business":
        cust = re.search(r"customer (K-\d+)", item).group(1).lower()
        return ["invoice", w[2].lower(), cust]                                  # "invoice", INV-…, K-…
    return [w[3].rstrip(":").lower(), "survey", "dataset"]                      # D5, survey, dataset


def lookup(ev: EvidenceV4, topic: str) -> str:
    """Seitenbasiert: Nennt das Topic die Einheit, kommt die ganze Seite (alle Abschnitte inklusive Distraktoren),
    sonst nur die per Stichwort passenden Abschnitte, sonst "No entry"."""
    t = (topic or "").lower()
    if any(re.search(rf"(?<![a-z0-9]){re.escape(e)}(?![a-z0-9])", t) for e in ev.entities):
        return "\n".join(f"[{k}] {v}" for k, v in ev.runbook_sections.items())
    hits = [f"[{k}] {v}" for k, v in ev.runbook_sections.items()
            if any(re.search(rf"(?<![a-z0-9]){re.escape(w)}", t) for w in TOPIC_KEYS.get(k, (k,)))]   # Wortanfang
    return "\n".join(hits) if hits else f"No entry for '{topic}'."


def fault_for(domain: str, kind: str, seed: int) -> str:
    if kind.startswith("ok"):
        return "none"
    return FAULTS[domain][(seed + (0 if kind == "fail_moderate" else 2)) % 4]


def _loguniform(rng: random.Random, lo: float, hi: float) -> float:
    return math.exp(rng.uniform(math.log(lo), math.log(hi)))


# --- coding ------------------------------------------------------------------------------------------------------

def _coding(rng: random.Random, fault: str, sub: int) -> tuple:
    svc = rng.choice(SERVICES)
    major, minor, patch = rng.randint(2, 5), rng.randint(3, 9), rng.randint(1, 9)
    new = f"{major}.{minor}.{patch}"
    sha, sha_old = _hex(rng, 7), _hex(rng, 7)
    pid, pid_old, pid_agent = rng.randint(20000, 29999), rng.randint(2000, 9999), rng.randint(10000, 19999)
    port = rng.choice([3000, 8080, 8443, 5000])
    db = f"10.0.{rng.randint(1, 9)}.{rng.randint(10, 99)}:5432"
    nested = rng.random() < 0.5
    # übliche Last, je Dienst verschieden; breit gestreut, damit "wenig" ohne Norm nicht auffällt (Lecktest)
    # v4.2: ab 100 req/min, damit kaputte Last nie im Bereich eigener Sonden liegt (Grok-Gutachten 3)
    rate = int(round(_loguniform(rng, 100, 10000), -1))
    shards = rng.choice([3, 4, 6, 8])                             # Shard-Zahl des Cache-Clusters
    redis = [f"10.0.{rng.randint(1, 9)}.{rng.randint(10, 99)}:6379" for _ in range(shards)]
    item = (f"Deploy {svc} v{new} (commit {sha}) to production "
            f"(runs as a single production instance that normally handles ~{rate} requests/min, steady around the clock, ±20 %; "
            f"cache cluster with {shards} shards, every instance connects to all shards)")
    short = f"Deploy {svc} v{new} (commit {sha}) to production"
    uptime = rng.randint(300, 900)                               # v4.2: deutlich über dem 60-s-Zählerfenster
    reqs = int(rate * rng.uniform(0.8, 1.2))
    if fault == "low_traffic":       # v4.2: 10–30 % der üblichen Last (mind. 10): ohne Norm plausibel, mit Norm (±20 %) klar zu wenig
        reqs = max(10, int(rate * rng.uniform(0.10, 0.30)))
    up = shards if fault != "cache_partial" else rng.randint(max(1, shards // 2 - 1), shards - 1)
    sig: dict[str, str] = {}

    app = {"config": f"  [{svc}] config loaded (env=production)", "db": f"  [{svc}] db pool ready (20/20)",
           "cache": f"  [{svc}] cache connected ({up} shards)", "listen": f"  [{svc}] listening on :{port}",
           "reqs": f"  [{svc}] requests served (last 60s): {reqs}"}
    if fault == "stale_process":
        app["listen"] = f"  [{svc}] listening on :{port + 1}"
        app["reqs"] = f"  [{svc}] requests served (last 60s): 0"
        sig["deploy"] = app["listen"].strip()
    if fault == "db_down":
        app["db"] = f"  [{svc}] db pool ready (0/20)"
        sig["deploy"] = app["db"].strip()
    if fault == "cache_partial":
        sig["deploy"] = app["cache"].strip()
    if fault == "low_traffic":
        sig["deploy"] = app["reqs"].strip()
    deploy = [[f"$ ./deploy.sh {svc} v{new}", f"build: passed ✓ ({rng.randint(1, 4)}m{rng.randint(10, 59)}s)",
               f"release: /srv/{svc}/releases/{new}-{sha} (config: PORT={port})"],
              [f"pm2 restart {svc} ... done", f"pm2: {svc} online ✓ (pid {pid}, uptime {uptime}s)"],
              ["app log (tail):"] + list(app.values())]
    deploy_noise = [["npm WARN deprecated request@2.88.2: request has been deprecated"],
                    [f"  [{svc}] warn: slow query 812ms (report_daily)"], ["pm2: log rotation done"],
                    [f"  [{svc}] DeprecationWarning: url.parse() behavior is not standardized"]]

    serving_ver, serving_sha, serving_up = new, sha, uptime
    if fault == "stale_process":
        serving_ver, serving_sha, serving_up = new, sha_old, rng.randint(200000, 400000)
        sig["probe"] = serving_sha
    ver = ({"service": svc, "build": {"version": serving_ver, "commit": serving_sha}, "uptime_s": serving_up} if nested
           else {"service": svc, "version": serving_ver, "commit": serving_sha})
    pool = {"size": 20, "active": rng.randint(3, 12), "waiting": 0}
    if fault == "db_down":
        pool = {"size": 20, "active": 0, "waiting": 20}
        sig["probe"] = '"active": 0, "waiting": 20'
    health = {"status": "ok", "checks": {"db": {"ok": True} if nested else "ok", "cache": {"ok": True} if nested else "ok"},
              "db_pool": pool, "cache": {"shards_connected": up}}
    if fault == "cache_partial":
        sig["probe"] = f'"shards_connected": {up}'
    served = max(1, int(reqs * uptime / 60 * rng.uniform(0.9, 1.1)))
    metrics = [f"$ curl -s http://localhost:{port}/metrics | grep ^http_requests_total",
               f'http_requests_total{{code="200"}} {served}',
               f'http_requests_total{{code="500"}} {rng.randint(0, 3) if served > 10 else 0}']
    if fault == "low_traffic":
        sig["probe"] = metrics[1]
    probe = [[f"$ curl -s http://localhost:{port}/version", json.dumps(ver)],
             [f"$ curl -s http://localhost:{port}/health", json.dumps(health)], metrics]
    probe_noise = [[f"$ curl -s -m 2 http://localhost:{port}/health", "curl: (28) Operation timed out after 2000 milliseconds",
                    f"$ curl -s -m 5 http://localhost:{port}/health   # retry after warm-up", json.dumps(health)],
                   [f"$ curl -s http://localhost:{port}/metrics | head -1", "# HELP http_requests_total Total HTTP requests"],
                   [f"$ curl -sI http://localhost:{port}/", "HTTP/1.1 302 Found", "Location: /login"]]

    listen_pid = pid_old if fault == "stale_process" else pid
    procs = {pid: ("Oct 22 10:41", f"node /srv/{svc}/releases/{new}-{sha}/server.js")}
    if fault == "stale_process":
        procs[pid_old] = ("Oct 19 08:12", f"node /srv/{svc}/releases/{new}-{sha_old}/server.js")
        sig["sockets"] = f"releases/{new}-{sha_old}/"
    if sub > 1:
        procs[pid_agent] = ("Oct 02 06:00", "node /srv/metrics-agent/agent.js")
    used_fd = {21}                    # v4.3: eindeutige Datei-Deskriptoren je Prozess (GPT-Fremdkontrolle v4.2)

    def fd() -> int:                  # gleiche Zahl an Zufallsaufrufen wie vorher, Kollisionen werden weitergezählt
        x = rng.randint(20, 40)
        while x in used_fd:
            x += 1
        used_fd.add(x)
        return x
    db_conns = [f'ESTAB 0 0 10.0.0.5:{rng.randint(40000, 60000)} {db} users:(("node",pid={listen_pid},fd={fd()}))'
                for _ in range(3)]
    if fault == "db_down":
        db_conns = [f'SYN-SENT 0 1 10.0.0.5:{rng.randint(40000, 60000)} {db} users:(("node",pid={listen_pid},fd={fd()}))']
        sig["sockets"] = "SYN-SENT"
    redis_conns = [f'ESTAB 0 0 10.0.0.5:{rng.randint(40000, 60000)} {r} users:(("node",pid={listen_pid},fd={fd()}))'
                   for r in redis[:up]]
    if fault == "cache_partial":
        sig["sockets"] = f"{up} connections to :6379"
    conns = sorted(db_conns + redis_conns, key=lambda c: c.split()[3])
    clients = 0 if fault == "stale_process" else max(1, round(reqs * rng.uniform(0.05, 0.15)))
    sockets = [[f"$ ss -ltnp | grep :{port}", f'LISTEN 0 511 *:{port} *:* users:(("node",pid={listen_pid},fd=21))'],
               ["$ ps -o pid,lstart,cmd -C node", "  PID STARTED        CMD"]
               + [f"{p:>5} {s}  {c}" for p, (s, c) in sorted(procs.items())],
               ["$ ss -tnp state all '( dport = :5432 or dport = :6379 )'"] + conns,
               [f"$ ss -tn state established '( sport = :{port} )' | tail -n +2 | wc -l", str(clients)]]
    if fault == "low_traffic":
        sig["sockets"] = f"| wc -l\n{clients}"
    sockets_noise = [["$ uptime", f" 10:4{rng.randint(2, 9)}:11 up 23 days,  load average: 0.41, 0.38, 0.35"],
                     ["$ df -h /srv | tail -1", "/dev/nvme0n1p2  200G  141G   59G  71% /srv"]]

    pad = PAD_LINES[sub]
    _pad(rng, deploy[0], [f"  dist/assets/{rng.choice(['index', 'vendor', 'chunk', 'worker'])}-{_hex(rng, 8)}.js  "
                          f"{rng.randint(2, 380)}.{rng.randint(10, 99)} kB" for _ in range(pad // 2)], start=2)
    _pad(rng, deploy[2], [rng.choice([f"  [{svc}] loaded {rng.randint(5, 60)} feature flags",
                                      f"  [{svc}] warmed cache '{rng.choice(['products', 'sessions', 'geo', 'i18n'])}' ({rng.randint(100, 9000)} keys)",
                                      f"  [{svc}] scheduled job '{rng.choice(['cleanup', 'digest', 'sync'])}' every {rng.randint(1, 30)}m"])
                          for _ in range(pad // 2)], start=2)
    features, metric_count = rng.randint(5, 60), rng.randint(40, 400)
    for _ in range(pad // 4):
        probe.insert(rng.randint(1, len(probe)), rng.choice([
            [f"$ curl -s http://localhost:{port}/api/v1/ping", '{"pong": true}'],
            [f"$ curl -s http://localhost:{port}/api/v1/config/public", json.dumps({"locale": "de-AT", "features": features})],
            [f"$ curl -s http://localhost:{port}/metrics | grep -c ^http_", str(metric_count)]]))
    others = {rng.randint(30000, 39999): s2 for s2 in rng.sample(["mailer", "image-resizer", "admin-ui", "webhooks"], 3)}
    sockets[0][0] = "$ ss -ltnp"
    _pad(rng, sockets[0], [f'LISTEN 0 511 *:{9100 + i} *:* users:(("node",pid={p2},fd=19))' for i, p2 in enumerate(others) if pad]
         + ['LISTEN 0 128 0.0.0.0:22 0.0.0.0:* users:(("sshd",pid=812,fd=3))',
            'LISTEN 0 511 0.0.0.0:443 0.0.0.0:* users:(("nginx",pid=1044,fd=8))'][:max(0, pad // 10)], start=2)
    if pad:
        _pad(rng, sockets[1], [f"{p2:>5} Oct {rng.randint(1, 20):02d} 0{rng.randint(1, 9)}:00  node /srv/{s2}/current/server.js"
                               for p2, s2 in others.items()], start=2)
    sockets[2][0] = "$ ss -tnp"
    _pad(rng, sockets[2], [f'ESTAB 0 0 10.0.0.5:{port} 10.0.2.{rng.randint(2, 9)}:{rng.randint(30000, 60000)} '
                           f'users:(("node",pid={listen_pid},fd={fd()}))' for _ in range(min(pad // 2, clients))])
    n = NOISE_BLOCKS[sub]
    channels = {"deploy": _render(rng, deploy, deploy_noise, n), "probe": _render(rng, probe, probe_noise, n),
                "sockets": _render(rng, sockets, sockets_noise, n)}
    # v4.2: realistische Seiten (Grok-Gutachten 3): die Norm steht zwischen gleich aussehenden Werten anderer Dienste
    # und der Staging-Umgebung. Eigener Zufall, damit die Belege selbst unverändert bleiben.
    r2 = random.Random(f"runbook-v4.2:{svc}:{sha}")
    others = r2.sample([s for s in SERVICES if s != svc], 3)
    rates = [int(round(_loguniform(r2, 100, 10000), -1)) for _ in others]
    sh = [r2.choice([n for n in (3, 4, 6, 8, 12) if n != shards]) for _ in others]
    sections = {"traffic": ("Each service runs as a single production instance. Production traffic baselines per instance "
                            "(requests/min, steady around the clock, ±20 %): "
                            + "; ".join([f"{svc} ~{rate}"] + [f"{o} ~{x}" for o, x in zip(others, rates)])
                            + f". Staging: {svc} ~{max(10, int(round(rate * r2.uniform(0.02, 0.1), -1)))}."),
                "cache": ("Cache clusters (every instance connects to all shards of its cluster): "
                          + "; ".join([f"{svc} {shards} shards"] + [f"{o} {n} shards" for o, n in zip(others, sh)])
                          + f". Staging: {svc} 1 shard."),
                "database": f"{svc} uses a database connection pool of 20.",
                "ports": f"{svc} listens on port {port} behind nginx.",
                "logging": f"{svc} logs to stdout; pm2 rotates logs daily.",
                "on-call": "Incidents go to the platform on-call rotation; page only for customer impact.",
                "release": "Releases are deployed with deploy.sh; rollback with deploy.sh --previous."}
    norms = {"rate": f"~{rate} requests/min", "shards": f"{shards} shards"}
    return item, short, channels, sig, sections, norms


# --- business ----------------------------------------------------------------------------------------------------

FIRST = ["Anna", "Jakob", "Lena", "Paul", "Sophie", "Maria", "Felix", "Eva", "Lukas", "Julia"]
LAST = ["Huber", "Lindner", "Kraus", "Berger", "Wagner", "Pichler", "Steiner", "Gruber"]


def _business(rng: random.Random, fault: str, sub: int) -> tuple:
    inv = f"INV-2026-{rng.randint(1000, 1999)}"
    cust = f"K-{rng.randint(10, 99)}"
    dom = rng.choice(["huber-bau", "lindner-logistik", "kraus-it", "berger-moebel", "steiner-holz"]) + rng.choice([".at", ".de"])
    (f1, f2), (l1, l2) = rng.sample(FIRST, 2), rng.sample(LAST, 2)
    contact = f"{f1[0].lower()}.{l1.lower()}@{dom}"            # Rechnungskontakt laut CRM
    sales = f"{f2[0].lower()}.{l2.lower()}@{dom}"              # anderer, echter Kontakt derselben Firma
    euros, cents = rng.randint(400, 9000), rng.randint(10, 99)
    amount = f"€ {euros:,}.{cents}"
    qid = _hex(rng, 10).upper()
    t1, t2 = f"10:{rng.randint(10, 39)}:{rng.randint(10, 59)}", f"10:{rng.randint(40, 59)}:{rng.randint(10, 59)}"
    # Zahlungsziel je Kunde (Norm). Ok- und Fehlerwerte kommen aus derselben Menge, ein Fälligkeitsdatum allein verrät
    # ohne Norm nichts. v4 hatte hier "Portal statt PDF", das war ein Konventionsleck (GPT-Lecktest, notizen/29).
    terms = rng.choice([14, 30, 45, 60])
    used = terms if fault != "wrong_terms" else rng.choice([t for t in (14, 30, 45, 60) if t != terms])
    due = (datetime.date(2026, 10, 23) + datetime.timedelta(days=used)).isoformat()
    remind = (datetime.date(2026, 10, 23) + datetime.timedelta(days=used + 7)).isoformat()
    item = (f"Send invoice {inv} dated 2026-10-23 ({amount}, payment terms {terms} days, PDF attached) "
            f"to customer {cust}, billing contact {contact}")
    short = f"Send invoice {inv} dated 2026-10-23 ({amount}, PDF attached) to customer {cust}"
    sent_amount = amount if fault != "amount_mismatch" else f"€ {(euros * 100 + cents) / 1000:,.2f}"
    rcpt = sales if fault == "wrong_contact" else contact
    pdf_kb, logo_kb, body_kb = rng.randint(38, 85), rng.randint(9, 22), rng.randint(14, 48)
    att_list = f"invoice_{inv}.pdf ({pdf_kb} kB), logo.png ({logo_kb} kB)"
    size = (body_kb + logo_kb + pdf_kb) * 1000 + rng.randint(0, 999)
    sig: dict[str, str] = {}

    mx = rcpt.split("@")[1]
    smtp = [[f"{t1} {qid}: from=<billing@nordwerk-gmbh.at> to=<{rcpt}> size={size} subject='Invoice {inv} ({sent_amount}, due {due})'",
             f"{t1} {qid}: attachments=[{att_list}]", f"{t1} {qid}: 250 2.0.0 OK queued"],
            [f"{t2} {qid}: relay=mx1.{mx}:25, status=sent (250 2.0.0 accepted)"]]
    track = [f"tracking {qid}: accepted by recipient server at {t2}",
             f"tracking {qid}: delivered to mailbox of <{rcpt}> (dsn 2.0.0)"]
    crm = [f"crm: activity 'invoice sent' on {cust} (to {rcpt}; attachments: {att_list})"]
    if fault == "wrong_contact":
        sig["smtp"] = sig["delivery"] = f"<{rcpt}>"
        sig["ledger"] = crm[0]
    if fault == "bounced":
        smtp[1] = [f"{t2} {qid}: relay=mx1.{mx}:25, status=deferred (452 4.2.2 over quota)",
                   f"queue: {qid} still pending, next retry in 4h (attempt 9 of 12)"]
        track = [f"tracking {qid}: queued for retry at {t2}", f"tracking {qid}: last update 71h ago (deferred)"]
        crm.append(f"crm: contact {contact} email status 'soft-bounce' (reported by mail gateway)")
        sig["smtp"], sig["delivery"], sig["ledger"] = smtp[1][-1], track[-1], crm[-1]
    delivery = [track, [f"tracking {qid}: attachments {att_list}",
                        f"tracking {qid}: payment link pay.nordwerk-gmbh.at/{inv} ({sent_amount}, due {due})", "read receipt: not requested"]]
    pages = rng.randint(1, 3)
    ledger = [[f"receivables: {inv} posted, customer {cust}, {sent_amount}, due {due}, status SENT"], crm,
              [f"archive: invoice_{inv}.pdf stored ({pages} pages)", f"dunning: reminder for {inv} scheduled {remind}"]]
    if fault == "amount_mismatch":
        sig["smtp"], sig["delivery"], sig["ledger"] = f"({sent_amount},", delivery[1][1], ledger[0][0]
    if fault == "wrong_terms":
        sig["smtp"], sig["delivery"], sig["ledger"] = f"due {due})'", delivery[1][1], ledger[0][0]
    smtp_noise = [[f"{t1} {qid}: status=deferred (421 4.7.0 greylisted, try again later)"],
                  [f"{t1} {qid}: spam score 3.1/5.0 (below threshold)"], [f"{t1} {qid}: TLS handshake retry (1/3) ... ok"]]
    delivery_noise = [[f"tracking {qid}: open pixel blocked by recipient client"], [f"tracking {qid}: link scan by recipient gateway"]]
    ledger_noise = [[f"crm: duplicate contact merge suggested for {cust}"], ["receivables: exchange rate update skipped (EUR invoice)"]]

    pad = PAD_LINES[sub]

    def stranger() -> str:
        return (f"{rng.choice('abcdefghjklmnoprst')}.{rng.choice(['wagner', 'pichler', 'steiner', 'gruber', 'hofer', 'bauer'])}"
                f"@{rng.choice(['wagner-druck.at', 'pichler-agrar.at', 'steiner-holz.de', 'gruber-elektro.at', 'hofer-reisen.at'])}")
    for _ in range(pad // 2):
        q2, who = _hex(rng, 10).upper(), stranger()
        m1 = rng.randint(10, 39)
        _pad(rng, smtp[0], [f"10:{m1}:{rng.randint(10, 59)} {q2}: from=<billing@nordwerk-gmbh.at> to=<{who}> size={rng.randint(30000, 150000)}"])
        _pad(rng, smtp[1], [f"10:{rng.randint(m1 + 1, 59)}:{rng.randint(10, 59)} {q2}: relay=mx1.{who.split('@')[1]}:25, "
                            "status=sent (250 2.0.0 accepted)"], start=0)
    _pad(rng, delivery[0], [f"tracking {_hex(rng, 10).upper()}: delivered to mailbox of <{stranger()}> (dsn 2.0.0)"
                            for _ in range(pad)], start=0)
    _pad(rng, ledger[0], [f"receivables: INV-2026-{rng.randint(2000, 2999)} posted, customer K-{rng.randint(100, 199)}, "
                          f"€ {rng.randint(100, 9000):,}.{rng.randint(10, 99)}, status SENT" for _ in range(pad // 2)], start=0)
    _pad(rng, ledger[1], [f"crm: activity '{rng.choice(['call logged', 'invoice sent', 'offer sent'])}' on K-{rng.randint(100, 199)}"
                          for _ in range(pad // 2)], start=0)
    n = NOISE_BLOCKS[sub]
    channels = {"smtp": _render(rng, smtp, smtp_noise, n), "delivery": _render(rng, delivery, delivery_noise, n),
                "ledger": _render(rng, ledger, ledger_noise, n)}
    # v4.2: realistische Seiten: Kontakte und Zahlungsziele mehrerer Kunden, eigener Zufall (Belege bleiben gleich)
    r2 = random.Random(f"runbook-v4.2:{inv}:{cust}")
    custs = [f"K-{n}" for n in r2.sample([n for n in range(10, 100) if f"K-{n}" != cust], 3)]
    tech = f"{r2.choice([n for n in FIRST if n not in (f1, f2)])[0].lower()}.{r2.choice(LAST).lower()}@{dom}"

    def person(d: str) -> str:
        return f"{r2.choice(FIRST)[0].lower()}.{r2.choice(LAST).lower()}@{d}"
    other_doms = [r2.choice(["wagner-druck.at", "pichler-agrar.at", "gruber-elektro.at", "hofer-reisen.at", "bauer-metall.de"])
                  for _ in custs]
    sections = {"contacts": (f"Customer {cust}: billing contact {contact}; sales contact {sales}; technical contact {tech}. "
                             + " ".join(f"Customer {c}: billing contact {person(d)}; sales contact {person(d)}."
                                        for c, d in zip(custs, other_doms))
                             + " Invoices go to the billing contact."),
                "attachments": "Every invoice email carries the invoice as a PDF attachment, plus the inline logo.",
                "dunning": "First reminder 7 days after the due date.",
                "payment": ("Payment terms from the invoice date: "
                            + "; ".join([f"{cust} {terms} days"] + [f"{c} {r2.choice([t for t in (14, 30, 45, 60) if t != terms])} days"
                                                                     for c in custs])
                            + "; all other customers 30 days. Every invoice email contains a payment link "
                              "pay.nordwerk-gmbh.at/<invoice number>."),
                "templates": "All invoice emails use the standard English invoice template."}
    norms = {"contact": contact, "terms": f"{terms} days"}
    return item, short, channels, sig, sections, norms


# --- research ----------------------------------------------------------------------------------------------------

def _research(rng: random.Random, fault: str, sub: int) -> tuple:
    ds = f"d{rng.randint(1, 9)}"
    rows = rng.randint(8000, 40000)
    dups = int(_loguniform(rng, 15, 1500))                 # breit gestreut (Lecktest)
    ncols = rng.randint(30, 80)
    pop = rng.randint(800_000, 9_000_000)                   # Zielpopulation, je Datensatz verschieden, nicht rund (sonst Leck)
    marked = rng.random() < 0.5
    ok = " ✓" if marked else ""
    item = (f"Clean survey dataset {ds.upper()}: remove duplicate respondents (nothing else may be dropped), recalibrate "
            f"the survey weights to the target population and write clean/{ds}.parquet "
            f"(raw file: {rows:,} rows, {ncols} columns, {dups} duplicate respondents; "
            f"target population {pop:,})")
    short = (f"Clean survey dataset {ds.upper()}: remove duplicate respondents (nothing else may be dropped), recalibrate "
             f"the survey weights to the target population and write clean/{ds}.parquet "
             f"(raw file: {rows:,} rows)")
    removed, cols = dups, ncols
    if fault == "duplicates_partial":                     # dedupe nur über respondent_id: Wiederbefragte bleiben drin
        removed = max(3, round(dups * rng.uniform(0.2, 0.5)))
    if fault == "column_loss":
        cols = ncols - rng.randint(3, 8)
    out = rows - removed
    wsum = float(pop)                                       # Kalibrierung trifft die Zielsumme exakt
    if fault == "weights_misscaled":
        wsum = pop * (rng.uniform(0.78, 0.92) if rng.random() < 0.5 else rng.uniform(1.08, 1.28))
    sig: dict[str, str] = {}

    mean = wsum / out
    steps = [f"dedupe on respondent_id: dropped {removed} duplicates", "dtypes: weight float64, income float64, age int64",
             f"weights: rescaled to total {wsum:,.0f}"]
    if fault == "row_loss":
        kept = int((rows - dups) * rng.uniform(0.12, 0.2))
        steps.insert(1, f"merge with respondents_meta.csv (inner): {rows - dups:,} -> {kept:,} rows")
        out, mean = kept, wsum / kept
        sig["joblog"] = steps[1]
    weight = f"weight: min {mean * 0.31:.1f}  max {mean * 4.87:.1f}  mean {mean:.1f}  nulls 0"
    wline = f"sum of weights: {wsum:,.0f}{ok}"
    count = f"row count: {out:,} (raw {rows:,}, duplicates removed {removed}){ok}"
    ids = f"respondent_id: {out:,} unique of {out:,}"
    joblog = [[f"job clean_{ds} started", f"read raw/{ds}.csv: {rows:,} rows"], steps,
              [f"wrote clean/{ds}.parquet ({cols} columns)", f"job clean_{ds} finished ✓ exit 0 ({rng.uniform(3, 40):.1f}s)"]]
    output = [[f"clean/{ds}.parquet: {out:,} rows x {cols} columns ({max(out, 1) * 0.21 / 1000 * cols / 47:.1f} MB)"],
              [weight, f"sum {wsum:,.0f}", ids]]
    schema = f"schema: {cols} columns present{ok}"
    validation = [[schema], [count], [f"weighted share female: 0.51 (census 0.51){ok}", wline]]
    if fault == "row_loss":
        sig["output"], sig["validation"] = f"{out:,} rows", count
    if fault == "weights_misscaled":
        sig["joblog"], sig["output"], sig["validation"] = steps[-1], f"sum {wsum:,.0f}", wline
    if fault == "duplicates_partial":
        sig["joblog"], sig["output"], sig["validation"] = steps[0], output[0][0], count
    if fault == "column_loss":
        sig["joblog"], sig["output"], sig["validation"] = joblog[2][0], f"x {cols} columns", schema
    joblog_noise = [["WARNING: 212 'income' values are non-numeric codes (-9 = refused), kept unchanged per codebook"],
                    ["info: 3 respondents have interview_date in the future (flagged for review, not changed)"],
                    ["memory: peak 1.9 GB"]]
    output_noise = [[f"income: non-numeric codes 212 ({212 / max(out, 1) * 100:.1f}%)"], ["interview_date: flagged 3"]]
    validation_noise = [["3 columns with >5% missing (expected per codebook)"], ["age distribution vs census: KS p=0.21"]]

    pad = PAD_LINES[sub]
    if pad:
        k = pad // 2
        joblog.insert(1, [f"read chunk {i}/{k}: {rows // k + (rows % k if i == k else 0):,} rows" for i in range(1, k + 1)])
    qmax = cols - 3
    _pad(rng, output[1], [f"Q{i:02d}: nulls {(m := rng.randint(0, 400))} ({m / max(out, 1) * 100:.1f}%)"
                          for i in rng.sample(range(1, qmax), min(pad, qmax - 1))])
    _pad(rng, validation[2], [f"Q{i:02d}: values within codebook range{ok}" for i in rng.sample(range(1, qmax), min(pad // 2, qmax - 1))],
         start=0)
    n = NOISE_BLOCKS[sub]
    channels = {"joblog": _render(rng, joblog, joblog_noise, n), "output": _render(rng, output, output_noise, n),
                "validation": _render(rng, validation, validation_noise, n)}
    # v4.2: realistische Codebuch-Seite: Werte mehrerer Datensätze nebeneinander, eigener Zufall (Belege bleiben gleich)
    r2 = random.Random(f"runbook-v4.2:{ds}:{rows}")
    dsx = r2.sample([f"D{i}" for i in range(1, 10) if f"d{i}" != ds], 3)
    sections = {"duplicates": ("Known duplicate respondents (re-interviews) in the raw files: "
                               + "; ".join([f"{ds.upper()} {dups}"] + [f"{d} {int(_loguniform(r2, 15, 1500))}" for d in dsx]) + "."),
                "weights": ("Target populations for weighting: "
                            + "; ".join([f"{ds.upper()} {pop:,}"] + [f"{d} {r2.randint(800_000, 9_000_000):,}" for d in dsx]) + "."),
                "schema": ("Column counts: " + "; ".join([f"{ds.upper()} {ncols}"] + [f"{d} {r2.randint(30, 80)}" for d in dsx]) + "."),
                "codes": "Income code -9 means 'refused' and is kept unchanged.",
                "storage": f"Clean files are written to clean/{ds}.parquet."}
    norms = {"dups": f"{dups} duplicate", "pop": f"{pop:,}", "ncols": f"{ncols} columns"}
    return item, short, channels, sig, sections, norms


GEN = {"coding": _coding, "business": _business, "research": _research}


def generate(domain: str, kind: str, seed: int) -> EvidenceV4:
    rng = random.Random(f"evidence-v4:{domain}:{kind}:{seed}")
    sub = 1 if kind in ("ok_clear", "fail_moderate") else rng.choice((2, 3))
    fault = fault_for(domain, kind, seed)
    item, short, channels, sig, sections, norms = GEN[domain](rng, fault, sub)
    return EvidenceV4(f"{domain}-{kind}-{seed:04d}", domain, kind, kind.startswith("ok"), item, short, channels, sub,
                      fault, FINDINGS[fault], sig, sections, norms, fault in PRIMARY,
                      entities=entities_for(domain, item))


def generate_set(seeds, domains=tuple(GEN), kinds=KINDS) -> list[EvidenceV4]:
    return [generate(d, k, s) for d in domains for k in kinds for s in seeds]


def as_dict(e: EvidenceV4) -> dict:
    return asdict(e)
