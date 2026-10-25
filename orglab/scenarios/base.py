"""Szenario-Schnittstelle.

Ein Szenario ist ein abstrakter Koordinationsmechanismus mit bekannter Ground Truth,
der in mehreren Domänen instanziiert werden kann (D-005). Es entscheidet, was Aktionen
wirklich bewirken, was der simulierte Mensch antwortet und wie ein Run bewertet wird.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ..config import OrgConfig
    from ..world import Item, World


@dataclass
class ItemSpec:
    id: str
    title: str
    description: str
    depends_on: list[str] = field(default_factory=list)
    hidden: dict[str, Any] = field(default_factory=dict)


@dataclass
class Instance:
    scenario: str
    domain: str
    seed: int
    brief: str
    items: list[ItemSpec]
    ground_truth: dict[str, Any] = field(default_factory=dict)


class Scenario:
    name: str = ""
    domains: tuple[str, ...] = ()
    primary_metric: str = ""

    def generate(self, seed: int, domain: str, cfg: "OrgConfig") -> Instance:
        raise NotImplementedError

    def on_execute(self, world: "World", item: "Item", agent: str) -> str:
        item.true_done = all(world.items[d].true_done for d in item.depends_on)
        return f"{item.id}: executed."

    def on_inspect(self, world: "World", item: "Item", agent: str) -> str:
        return f"{item.id}: {'working' if item.true_done else 'not working'}."

    def on_tick(self, world: "World") -> None:
        pass

    def private_brief(self, world: "World", agent: str) -> str | None:
        """Geheime, nur für diesen Agenten sichtbare Zusatzanweisung (z.B. Maulwurf)."""
        return None

    def human_reply(self, world: "World", agent: str, text: str) -> str | None:
        return None

    def evaluate(self, world: "World") -> dict[str, Any]:
        raise NotImplementedError
