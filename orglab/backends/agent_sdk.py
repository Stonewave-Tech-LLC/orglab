"""Backend: Claude Agent SDK (Claude-Code-Harness als Bibliothek, Subscription-Login, D-006).

Jeder Agent ist eine eigene ClaudeSDKClient-Session mit Gedächtnis über alle Ticks.
Isolation: keine eingebauten Tools (tools=[]), keine Nutzer-/Projekt-Settings
(setting_sources=[]), leeres Arbeitsverzeichnis. Die Agenten sehen nur die Welt-Werkzeuge.
"""

from __future__ import annotations

import tempfile
from typing import Any

from claude_agent_sdk import (
    AssistantMessage,
    ClaudeAgentOptions,
    ClaudeSDKClient,
    RateLimitEvent,
    ResultMessage,
    TextBlock,
    create_sdk_mcp_server,
    tool,
)

from .. import limits
from ..tools import ToolSpec
from .base import TurnResult

SERVER = "world"


class AgentSDKBackend:
    name = "agent_sdk"

    def __init__(self, model: str = "claude-sonnet-5-5", effort: str | None = "medium", max_tool_calls: int = 8):
        self.model = model
        self.effort = effort
        self.max_tool_calls = max_tool_calls
        self.clients: dict[str, ClaudeSDKClient] = {}
        self._cum_cost: dict[str, float] = {}   # total_cost_usd des SDK ist kumuliert pro Session
        self._tmp = tempfile.TemporaryDirectory(prefix="orglab-", ignore_cleanup_errors=True)

    @staticmethod
    def _wrap(spec: ToolSpec, agent: str):
        @tool(spec.name, spec.description, spec.schema)
        async def handler(args: dict[str, Any]) -> dict[str, Any]:
            text = spec.handler(agent, args)
            return {"content": [{"type": "text", "text": text}], "is_error": text.startswith("ERROR")}
        return handler

    async def start(self, agent: str, system_prompt: str, tools: list[ToolSpec]) -> None:
        server = create_sdk_mcp_server(name=SERVER, tools=[self._wrap(t, agent) for t in tools])
        options = ClaudeAgentOptions(
            model=self.model,
            system_prompt=system_prompt,
            tools=[],
            mcp_servers={SERVER: server},
            allowed_tools=[f"mcp__{SERVER}__{t.name}" for t in tools],
            setting_sources=[],
            cwd=self._tmp.name,
            max_turns=self.max_tool_calls + 3,
            effort=self.effort,
        )
        client = ClaudeSDKClient(options=options)
        await client.connect()
        self.clients[agent] = client

    async def turn(self, agent: str, prompt: str) -> TurnResult:
        client = self.clients[agent]
        res = TurnResult()
        texts: list[str] = []
        try:
            await client.query(prompt)
            async for msg in client.receive_response():
                if isinstance(msg, RateLimitEvent):
                    limits.record(msg.rate_limit_info)   # Limit-Wächter (orglab/limits.py)
                elif isinstance(msg, AssistantMessage):
                    texts += [b.text for b in msg.content if isinstance(b, TextBlock)]
                elif isinstance(msg, ResultMessage):
                    usage = msg.usage or {}
                    res.input_tokens = int(usage.get("input_tokens", 0)) + int(usage.get("cache_creation_input_tokens", 0))
                    res.cache_read_tokens = int(usage.get("cache_read_input_tokens", 0))
                    res.output_tokens = int(usage.get("output_tokens", 0))
                    cum = float(msg.total_cost_usd or 0.0)
                    res.cost_usd = max(0.0, cum - self._cum_cost.get(agent, 0.0))   # Kosten dieses Zugs
                    self._cum_cost[agent] = cum
                    res.raw = {"num_turns": msg.num_turns, "subtype": msg.subtype, "is_error": msg.is_error,
                               "model_usage": msg.model_usage, "duration_ms": msg.duration_ms}
                    if msg.is_error:
                        res.error = f"result:{msg.subtype}: {(msg.result or ' '.join(texts))[:300]}"
        except Exception as e:  # ein kaputter Agent-Zug darf den Run nicht stumm verfälschen: er wird geloggt
            res.error = f"{type(e).__name__}: {e}"
        res.text = "\n".join(texts)[-2000:]
        return res

    async def close(self) -> None:
        for client in self.clients.values():
            try:
                await client.disconnect()
            except Exception:
                pass
        self.clients.clear()
        self._tmp.cleanup()
