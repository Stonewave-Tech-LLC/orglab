"""Limit-Wächter für das Claude-Abo (Subscription-Login der Agent SDK).

Die SDK meldet über `RateLimitEvent`, wie voll das 5-Stunden-Fenster und das Wochenlimit sind und wann sie
zurückgesetzt werden. Das Backend schreibt jede Meldung nach `daten/limits.json`. Vor jedem Run fragt
`wait_for_budget()` dort nach und wartet, statt Runs in ein Limit laufen zu lassen.

Regeln (änderbar zur Laufzeit in `daten/limit_policy.json`, ohne Neustart):
- `five_hour_max` (Standard 0,95): Ab dieser Auslastung oder bei "rejected" wird bis zum Reset gewartet.
- `weekly_max` (Standard 0,75): Ab dieser Wochenauslastung starten keine neuen Runs mehr, damit Neo für die
  eigene Arbeit genug Kontingent bleibt. Gewartet wird bis zum Wochen-Reset.
- Liegt `daten/PAUSE` vor, wartet jeder neue Run, bis die Datei entfernt ist (Not-Aus von Hand).
Laufende Runs werden nie abgebrochen, die Prüfung greift nur vor dem Start.
"""

from __future__ import annotations

import asyncio
import json
import os
import time
from pathlib import Path
from typing import Any, Callable

ROOT = Path(__file__).resolve().parent.parent
STATE = ROOT / "daten" / "limits.json"
POLICY = ROOT / "daten" / "limit_policy.json"
PAUSE = ROOT / "daten" / "PAUSE"
DEFAULTS = {"five_hour_max": 0.95, "weekly_max": 0.75}
WEEKLY_TYPES = ("seven_day", "seven_day_sonnet", "seven_day_opus")


def _read(path: Path) -> dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}


def policy() -> dict[str, float]:
    return {**DEFAULTS, **{k: float(v) for k, v in _read(POLICY).items() if k in DEFAULTS}}


def record(info: Any) -> None:
    """Eine RateLimitInfo der SDK festhalten (letzter Stand je Limit-Typ)."""
    kind = getattr(info, "rate_limit_type", None) or "unknown"
    state = _read(STATE)
    state[kind] = {"status": info.status, "utilization": info.utilization, "resets_at": info.resets_at,
                   "seen": time.time(), "seen_local": time.strftime("%Y-%m-%dT%H:%M:%S")}
    STATE.parent.mkdir(parents=True, exist_ok=True)
    tmp = STATE.with_name(f"limits.{os.getpid()}.tmp")
    tmp.write_text(json.dumps(state, indent=2), encoding="utf-8")
    os.replace(tmp, STATE)


def blocked_until(now: float | None = None) -> tuple[float, str]:
    """(Zeitpunkt, Grund), bis zu dem keine neuen Runs starten sollen. (0, "") = freie Fahrt."""
    now = now or time.time()
    if PAUSE.exists():
        return now + 60, "daten/PAUSE vorhanden"
    pol, state, until, why = policy(), _read(STATE), 0.0, ""
    for kind, s in state.items():
        reset = float(s.get("resets_at") or 0)
        if reset <= now:
            continue   # Fenster ist inzwischen zurückgesetzt, der alte Stand gilt nicht mehr
        util = s.get("utilization")
        limit = pol["weekly_max"] if kind in WEEKLY_TYPES else pol["five_hour_max"]
        if s.get("status") == "rejected" or (util is not None and util >= limit):
            if reset + 120 > until:
                until, why = reset + 120, f"{kind}: {s.get('status')}, Auslastung {util}, Grenze {limit}"
    return until, why


async def wait_for_budget(log: Callable[[str], None] = print) -> None:
    announced = ""
    while True:
        until, why = blocked_until()
        if not until:
            return
        if why != announced:
            log(f"[limits] warte bis {time.strftime('%H:%M', time.localtime(until))} ({why})")
            announced = why
        await asyncio.sleep(min(600.0, max(30.0, until - time.time())))
