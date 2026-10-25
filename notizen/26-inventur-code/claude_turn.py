"""Inventur Claude-Seite: ein Zug über das Agent SDK mit demselben stdio-MCP-Werkzeug wie bei Grok.
Gibt die Init-Nachricht (Werkzeuge, Modell, MCP) und den Token-Verbrauch aus."""
import asyncio
import json
import os
import sys

from claude_agent_sdk import ClaudeAgentOptions, ResultMessage, SystemMessage, query

HERE = os.path.dirname(os.path.abspath(__file__))
EMPTY = os.path.join(HERE, "claude-welt")
os.makedirs(EMPTY, exist_ok=True)


async def main() -> None:
    opts = ClaudeAgentOptions(
        system_prompt="INVENTUR-SYSTEM-PROMPT-MARKER. You are agent a1 in a small team. Use your tools to check work items.",
        tools=[],
        setting_sources=[],
        cwd=EMPTY,
        mcp_servers={"world": {"type": "stdio", "command": sys.executable, "args": [os.path.join(HERE, "toy_mcp.py")]}},
        allowed_tools=["mcp__world__inspect_item"],
        model="claude-sonnet-5-5",
        max_turns=4,
    )
    async for msg in query(prompt="Check work item A-1 with your tool and tell me in one sentence whether it works.", options=opts):
        if isinstance(msg, SystemMessage) and msg.subtype == "init":
            d = msg.data
            print("INIT", json.dumps({k: d.get(k) for k in ("model", "tools", "mcp_servers", "permissionMode", "slash_commands",
                                                            "agents", "skills", "output_style")}, ensure_ascii=False)[:1500])
        if isinstance(msg, ResultMessage):
            print("RESULT", msg.result)
            print("USAGE", json.dumps(msg.usage))


asyncio.run(main())
