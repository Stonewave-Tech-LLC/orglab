"""Append-only Event-Log. Jede Beobachtung eines Runs landet hier, nichts wird nachträglich geändert."""

from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any


class EventLog:
    def __init__(self, path: Path | None):
        self.path = path
        self.events: list[dict[str, Any]] = []
        self.tick = 0
        self._fh = open(path, "a", encoding="utf-8") if path else None

    def emit(self, type: str, actor: str | None = None, **data: Any) -> dict[str, Any]:
        event = {"seq": len(self.events), "tick": self.tick, "t": round(time.time(), 3),
                 "type": type, "actor": actor, **data}
        self.events.append(event)
        if self._fh:
            self._fh.write(json.dumps(event, ensure_ascii=False, default=str) + "\n")
            self._fh.flush()
        return event

    def of_type(self, *types: str) -> list[dict[str, Any]]:
        return [e for e in self.events if e["type"] in types]

    def close(self) -> None:
        if self._fh:
            self._fh.close()
            self._fh = None


def load_events(path: Path) -> list[dict[str, Any]]:
    with open(path, encoding="utf-8") as fh:
        return [json.loads(line) for line in fh if line.strip()]
