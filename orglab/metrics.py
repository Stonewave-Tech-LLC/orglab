"""Generische Metriken über alle Szenarien, berechnet aus Event-Log und Endzustand.

Sie messen Neos Symptome direkt (notizen/02): liegengebliebene Arbeit, Doppelfragen,
Schweigen, Machtkonzentration in der Kommunikation, Kosten.
"""

from __future__ import annotations

import re
from collections import Counter
from typing import Any

from .world import World


def gini(values: list[float]) -> float:
    vals = sorted(v for v in values if v >= 0)
    n, total = len(vals), sum(vals)
    if n == 0 or total == 0:
        return 0.0
    cum = sum((i + 1) * v for i, v in enumerate(vals))
    return (2 * cum) / (n * total) - (n + 1) / n


def _norm(text: str) -> str:
    return re.sub(r"\W+", " ", text.lower()).strip()


def generic_metrics(world: World) -> dict[str, Any]:
    ev = world.log.events
    msgs = [e for e in ev if e["type"] == "message"]
    seen: Counter[tuple[str, str, str]] = Counter()
    repeated = 0
    for m in msgs:
        key = (m["actor"], m["to"], _norm(m["text"]))
        repeated += seen[key] > 0
        seen[key] += 1
    degree = {a: 0 for a in world.agents}
    sent = {a: 0 for a in world.agents}
    for m in msgs:
        degree[m["actor"]] += 1
        degree[m["to"]] += 1
        sent[m["actor"]] += 1
    turns = [e for e in ev if e["type"] == "agent_turn_end"]
    items = list(world.items.values())
    return {
        "ticks_used": world.tick,
        "messages": len(msgs),
        "repeated_messages": repeated,
        "escalations": sum(e["type"] == "escalation" for e in ev),
        "tool_calls": sum(e["type"] == "tool_call" for e in ev),
        "rejected_actions": sum(e["type"] == "action_rejected" for e in ev),
        "idle_turn_rate": (sum(t["tool_calls"] == 0 for t in turns) / len(turns)) if turns else 0.0,
        "open_claims_end": sum(it.status == "claimed" for it in items),
        "orphans_end": sum(it.owner is None and not it.true_done for it in items),
        "comm_degree_gini": gini(list(degree.values())),
        "max_talk_share": (max(sent.values()) / len(msgs)) if msgs else 0.0,
        "silent_agents": sum(1 for a in world.agents if degree[a] == 0 and not any(
            e["actor"] == a and e["type"] == "tool_call" for e in ev)),
        "turn_errors": sum(1 for t in turns if t.get("error")),
        "input_tokens": sum(t.get("input_tokens", 0) for t in turns),
        "output_tokens": sum(t.get("output_tokens", 0) for t in turns),
        "cache_read_tokens": sum(t.get("cache_read_tokens", 0) for t in turns),
        "cost_usd_est": round(sum(t.get("cost_usd", 0.0) for t in turns), 4),
    }
