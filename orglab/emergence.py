"""Emergenz-Analyse: Welche Organisation ist in einem Run entstanden?

Post-hoc aus events.jsonl, ohne laufende Experimente zu berühren. Misst:
  - Aktionsprofil je Agent (ausführen, prüfen, koordinieren, kommunizieren, dokumentieren)
  - emergente Rolle je Agent (dominante Aktivität, nur wenn deutlich dominant)
  - Spezialisierung des Teams: 1 − mittlere normierte Entropie der Agentenprofile
    (0 = alle tun alles gleich verteilt, 1 = jeder tut genau eine Art von Arbeit)
  - Konzentration: Anteil des aktivsten Agenten an Prüfungen bzw. Nachrichten
  - Rollenstabilität: Überschneidung der dominanten Rolle zwischen erster und zweiter Run-Hälfte

  python -m orglab.emergence daten/E-001-pilot
"""

from __future__ import annotations

import math
import statistics
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from .analyze import collect, summarize, write_csv
from .events import load_events

ACTIVITY = {
    "execute_item": "execute", "claim_item": "execute", "release_item": "execute", "report_done": "execute",
    "inspect_item": "verify",
    "send_message": "communicate", "contact_human": "communicate",
    "list_items": "coordinate", "declare_role": "coordinate",
    "add_note": "document", "read_notes": "document",
}
KINDS = ("execute", "verify", "communicate", "coordinate", "document")
ROLE_NAME = {"execute": "executor", "verify": "verifier", "communicate": "communicator",
             "coordinate": "coordinator", "document": "archivist"}


def _norm_entropy(counts: Counter) -> float:
    total = sum(counts.values())
    if total == 0:
        return 0.0
    ps = [c / total for c in counts.values() if c]
    return -sum(p * math.log(p) for p in ps) / math.log(len(KINDS))


def _dominant(counts: Counter, threshold: float = 0.45) -> str:
    total = sum(counts.values())
    if not total:
        return "silent"
    kind, n = counts.most_common(1)[0]
    return ROLE_NAME[kind] if n / total >= threshold else "generalist"


def analyze_run(run_dir: Path) -> dict[str, Any]:
    ev = load_events(run_dir / "events.jsonl")
    calls = [e for e in ev if e["type"] == "tool_call" and not e["result"].startswith("ERROR")]
    agents = sorted({e["actor"] for e in ev if e["type"] == "agent_turn_end"})
    last_tick = max((e["tick"] for e in ev), default=1)
    profile: dict[str, Counter] = defaultdict(Counter)
    halves: dict[str, list[Counter]] = defaultdict(lambda: [Counter(), Counter()])
    for e in calls:
        kind = ACTIVITY.get(e["tool"])
        if kind:
            profile[e["actor"]][kind] += 1
            halves[e["actor"]][0 if e["tick"] <= last_tick / 2 else 1][kind] += 1
    roles = {a: _dominant(profile[a]) for a in agents}
    stable = [a for a in agents if sum(halves[a][0].values()) and sum(halves[a][1].values())]
    verify = [profile[a]["verify"] for a in agents]
    comm = [profile[a]["communicate"] for a in agents]
    declared = {e["actor"]: e["role"] for e in ev if e["type"] == "role_declared"}
    return {
        "specialization": round(1 - statistics.fmean(_norm_entropy(profile[a]) for a in agents), 3) if agents else 0.0,
        "verifier_concentration": round(max(verify) / sum(verify), 3) if sum(verify) else 0.0,
        "communication_concentration": round(max(comm) / sum(comm), 3) if sum(comm) else 0.0,
        "role_stability": round(statistics.fmean(_dominant(halves[a][0]) == _dominant(halves[a][1]) for a in stable), 3)
        if stable else None,
        "n_distinct_roles": len(set(roles.values()) - {"silent"}),
        "emergent_roles": ",".join(f"{a}:{roles[a]}" for a in agents),
        "declared_roles": ",".join(f"{a}:{r}" for a, r in sorted(declared.items())),
        "notes_written": sum(e["type"] == "note_added" for e in ev),
    }


def analyze_experiment(exp_dir: Path) -> str:
    rows = []
    for r in collect(exp_dir):
        rd = exp_dir / r["run_dir"]
        if (rd / "events.jsonl").exists():
            rows.append({**{k: r[k] for k in ("config_name", "domain", "seed", "true_completion")}, **analyze_run(rd)})
    write_csv(rows, exp_dir / "emergenz.csv")
    metrics = ["specialization", "verifier_concentration", "communication_concentration", "n_distinct_roles"]
    roles = defaultdict(Counter)
    for r in rows:
        for pair in r["emergent_roles"].split(","):
            roles[r["config_name"]][pair.split(":")[1]] += 1
    role_lines = [f"- **{c}:** " + ", ".join(f"{k} {v}" for k, v in cnt.most_common()) for c, cnt in sorted(roles.items())]
    text = "\n\n".join([f"# Emergenz-Analyse {exp_dir.name}", f"Runs: {len(rows)}",
                        summarize(rows, metrics, by=("config_name",)),
                        "## Emergente Rollen (Anzahl Agenten über alle Runs)", "\n".join(role_lines)])
    (exp_dir / "emergenz.md").write_text(text, encoding="utf-8")
    return text


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    print(analyze_experiment(Path(sys.argv[1])))
