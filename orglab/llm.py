"""Einzelne LLM-Aufrufe ohne Werkzeuge (Editor, Composer, Reflector des Optimierers).

Der Editor bekommt bewusst KEINE Werkzeuge: Er kann nur Text zurückgeben, aus dem wir eine
Org-Config parsen und validieren. So kann er technisch nichts anderes ändern (D-007).
"""

from __future__ import annotations

import json
import re
import tempfile
from typing import Any

from claude_agent_sdk import AssistantMessage, ClaudeAgentOptions, ResultMessage, TextBlock, query

from .runner import BackendFailure


async def complete(prompt: str, system: str, model: str = "claude-opus-5-5", effort: str = "high") -> tuple[str, dict[str, Any]]:
    # Windows: die CLI hält das Verzeichnis beim Aufräumen evtl. noch offen (WinError 32, Absturz E-012)
    with tempfile.TemporaryDirectory(prefix="orglab-editor-", ignore_cleanup_errors=True) as tmp:
        options = ClaudeAgentOptions(model=model, system_prompt=system, tools=[], setting_sources=[],
                                     max_turns=1, cwd=tmp, effort=effort)
        texts: list[str] = []
        usage: dict[str, Any] = {}
        async for msg in query(prompt=prompt, options=options):
            if isinstance(msg, AssistantMessage):
                texts += [b.text for b in msg.content if isinstance(b, TextBlock)]
            elif isinstance(msg, ResultMessage):
                usage = {"usage": msg.usage, "cost_usd": msg.total_cost_usd, "model_usage": msg.model_usage}
                if msg.is_error:
                    raise BackendFailure(f"editor: {msg.subtype}: {(msg.result or ' '.join(texts))[:300]}")
    return "\n".join(texts), usage


def extract_json(text: str) -> Any:
    m = re.search(r"```json\s*(.+?)```", text, re.S)
    raw = m.group(1) if m else text[text.find("{"): text.rfind("}") + 1]
    return json.loads(raw)
