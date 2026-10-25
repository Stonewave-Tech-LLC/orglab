"""Gemischte Teams (D-012): einzelne Agenten werden von einem anderen Backend gespielt.

Hauptfall: Die Maulwürfe eines `mole_k`-Szenarios sind geskriptete, hartnäckige Saboteure, die nie
gestehen. Die ehrlichen Agenten bleiben LLM-Agenten. So hängt die Manipulation nicht vom Charakter
des getesteten Modells ab (E-006: Claude-Maulwürfe gestehen und reparieren selbst).
"""

from __future__ import annotations

from ..tools import ToolSpec
from .base import TurnResult


class MixedBackend:
    name = "mixed"

    def __init__(self, primary, secondary, secondary_agents: set[str]):
        self.primary, self.secondary = primary, secondary
        self.secondary_agents = set(secondary_agents)
        self.model = f"{primary.model}+{secondary.model}[{','.join(sorted(secondary_agents))}]"

    def _for(self, agent: str):
        return self.secondary if agent in self.secondary_agents else self.primary

    async def start(self, agent: str, system_prompt: str, tools: list[ToolSpec]) -> None:
        await self._for(agent).start(agent, system_prompt, tools)

    async def turn(self, agent: str, prompt: str) -> TurnResult:
        return await self._for(agent).turn(agent, prompt)

    async def close(self) -> None:
        await self.primary.close()
        await self.secondary.close()
