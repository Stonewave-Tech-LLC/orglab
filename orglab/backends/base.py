"""Backend-Schnittstelle: wer spielt die Agenten?

Austauschbar, damit derselbe Run mit dem Claude Agent SDK (Subscription, D-006), später mit
der Messages API (API-Key, für einen öffentlichen Benchmark) oder mit geskripteten Policies
(Tests, Mess-Validierung) laufen kann.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Protocol

from ..tools import ToolSpec


@dataclass
class TurnResult:
    text: str = ""
    input_tokens: int = 0
    output_tokens: int = 0
    cache_read_tokens: int = 0
    cost_usd: float = 0.0
    error: str | None = None
    raw: dict[str, Any] = field(default_factory=dict)


class AgentBackend(Protocol):
    name: str
    model: str

    async def start(self, agent: str, system_prompt: str, tools: list[ToolSpec]) -> None: ...

    async def turn(self, agent: str, prompt: str) -> TurnResult: ...

    async def close(self) -> None: ...
