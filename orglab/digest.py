"""Kompakte, lesbare Zusammenfassung eines Runs aus dem Event-Log (für den Editor und für Menschen)."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .events import load_events

SHOW = {"message", "item_claimed", "item_released", "item_executed", "item_inspected", "item_reported_done",
        "escalation", "human_reply", "note_added", "role_declared", "action_rejected", "phantom_diagnosed"}


def _line(e: dict[str, Any]) -> str:
    a, t = e.get("actor"), e["type"]
    if t == "message":
        return f"{a} → {e['to']}: {e['text'][:160]}"
    if t == "item_executed":
        truth = "WORKS" if e["true_done_after"] else "DOES NOT WORK"
        return f"{a} executes {e['item']} → signal '{e['signal'][:60]}' [ground truth: {truth}]"
    if t == "item_inspected":
        return f"{a} inspects {e['item']} → {e['result'][:120]}"
    if t == "item_reported_done":
        return f"{a} reports {e['item']} done [ground truth: {'works' if e['true_done'] else 'DOES NOT WORK'}]"
    if t == "escalation":
        return f"{a} → HUMAN: {e['text'][:160]}"
    if t == "human_reply":
        return f"HUMAN → {e['to']}: {e['text'][:160]}"
    if t == "note_added":
        return f"{a} notes: {e['text'][:160]}"
    if t == "action_rejected":
        return f"{a} rejected {e['action']}: {e['reason'][:100]}"
    if t == "phantom_diagnosed":
        return f"(diagnosis of {e['item']} via {e['via']})"
    return f"{a} {t} {e.get('item', e.get('role', ''))}"


def digest(run_dir: Path, max_chars: int = 3500) -> str:
    ev = load_events(run_dir / "events.jsonl")
    out: list[str] = []
    tick = -1
    for e in ev:
        if e["type"] not in SHOW:
            continue
        if e["tick"] != tick:
            tick = e["tick"]
            out.append(f"-- tick {tick}")
        out.append(_line(e))
    end = next((e for e in reversed(ev) if e["type"] == "run_end"), None)
    tail = ""
    if end:
        m = end["metrics"]
        tail = (f"\nEND ({end['end_reason']}): true_completion={m.get('true_completion')}, "
                f"false_done={m.get('false_done')}, messages={m.get('messages')}, escalations={m.get('escalations')}")
    text = "\n".join(out)
    if len(text) > max_chars:
        text = text[: max_chars // 2] + "\n[...]\n" + text[-max_chars // 2:]
    return text + tail
