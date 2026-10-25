"""Org-Konfiguration: beschreibt die Organisation, nicht die Agenten.

Das ist die unabhängige Variable der Experimente und die einzige Datei, die der Optimierer
verändern darf (D-007). Alles hier muss deshalb validierbar und hashbar sein.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

import yaml

TOPOLOGIES = ("mesh", "star", "chain")
ROLE_MODES = ("fixed", "self_select", "none")
HUMAN_CHANNELS = ("anyone", "hub_only", "none")

OPTIONAL_DEFAULTS = {"reassign_quorum": 0, "stale_release_ticks": 0}   # nachträglich ergänzte Felder; Default wird weggelassen

LIMITS = {"n_agents": (2, 12), "max_ticks": (2, 40), "max_tool_calls": (2, 30),
          "norms": 20, "norm_len": 400, "roles": 12}


@dataclass
class Role:
    name: str
    mandate: str


@dataclass
class OrgConfig:
    name: str
    description: str = ""
    n_agents: int = 4
    topology: str = "mesh"          # wer wem Nachrichten schicken darf
    board: bool = False             # gemeinsamer, für alle sichtbarer Zustand aller Arbeitspakete
    shared_notes: bool = False      # gemeinsames Notizbuch (institutionelles Gedächtnis)
    human_channel: str = "anyone"   # wer an den Menschen eskalieren darf
    role_mode: str = "none"
    roles: list[Role] = field(default_factory=list)
    norms: list[str] = field(default_factory=list)   # Regeln/Verträge im Klartext
    max_ticks: int = 12
    max_tool_calls: int = 8         # pro Agent und Tick
    # Selbstverwaltung ohne Menschen (Teil 2 §5/§6): Mit so vielen Stimmen anderer Agenten wird ein Paket
    # neu zugewiesen. 0 = aus. Neue Felder mit Default werden nicht gehasht (Hash-Stabilität alter Configs).
    reassign_quorum: int = 0
    # Frist-Regel (H-013, notizen/11): Ein als erledigt gemeldetes Paket, das bei einer Fremdprüfung nicht
    # funktioniert und vom Eigentümer binnen so vielen Ticks nicht erneut ausgeführt wird, wird frei. 0 = aus.
    stale_release_ticks: int = 0

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> "OrgConfig":
        d = dict(d)
        d["roles"] = [Role(**r) for r in d.get("roles", [])]
        unknown = set(d) - set(cls.__dataclass_fields__)
        if unknown:
            raise ValueError(f"Unbekannte Config-Felder: {sorted(unknown)}")
        cfg = cls(**d)
        cfg.validate()
        return cfg

    @classmethod
    def load(cls, path: str | Path) -> "OrgConfig":
        with open(path, encoding="utf-8") as fh:
            return cls.from_dict(yaml.safe_load(fh))

    def validate(self) -> None:
        def rng(key: str, val: int) -> None:
            lo, hi = LIMITS[key]
            if not lo <= val <= hi:
                raise ValueError(f"{key}={val} außerhalb [{lo}, {hi}]")

        rng("n_agents", self.n_agents)
        rng("max_ticks", self.max_ticks)
        rng("max_tool_calls", self.max_tool_calls)
        if not 0 <= self.stale_release_ticks <= self.max_ticks:
            raise ValueError("stale_release_ticks muss in [0, max_ticks] liegen")
        if not 0 <= self.reassign_quorum < self.n_agents:
            raise ValueError("reassign_quorum muss in [0, n_agents) liegen")
        if self.topology not in TOPOLOGIES:
            raise ValueError(f"topology muss in {TOPOLOGIES} sein")
        if self.role_mode not in ROLE_MODES:
            raise ValueError(f"role_mode muss in {ROLE_MODES} sein")
        if self.human_channel not in HUMAN_CHANNELS:
            raise ValueError(f"human_channel muss in {HUMAN_CHANNELS} sein")
        if self.role_mode != "none" and not self.roles:
            raise ValueError("role_mode != none braucht roles")
        if len(self.roles) > LIMITS["roles"]:
            raise ValueError("zu viele Rollen")
        if len(self.norms) > LIMITS["norms"] or any(len(n) > LIMITS["norm_len"] for n in self.norms):
            raise ValueError("zu viele oder zu lange Normen")

    def to_dict(self) -> dict[str, Any]:
        d = asdict(self)
        for key, default in OPTIONAL_DEFAULTS.items():
            if d.get(key) == default:
                d.pop(key)
        return d

    def to_yaml(self) -> str:
        return yaml.safe_dump(self.to_dict(), allow_unicode=True, sort_keys=False)

    def hash(self) -> str:
        canon = json.dumps(self.to_dict(), sort_keys=True, ensure_ascii=False)
        return hashlib.sha256(canon.encode()).hexdigest()[:12]

    # --- abgeleitete Struktur -------------------------------------------------

    def agent_ids(self) -> list[str]:
        return [f"a{i}" for i in range(self.n_agents)]

    def hub(self) -> str:
        return "a0"

    def can_message(self, src: str, dst: str) -> bool:
        if src == dst:
            return False
        if self.topology == "mesh":
            return True
        if self.topology == "star":
            return self.hub() in (src, dst)
        i, j = int(src[1:]), int(dst[1:])
        return abs(i - j) == 1

    def neighbors(self, agent: str) -> list[str]:
        return [a for a in self.agent_ids() if self.can_message(agent, a)]

    def entry_agents(self) -> list[str]:
        """Wer den Auftrag mit der vollständigen Paketliste anfangs erhält."""
        if self.topology == "mesh" or self.board:
            return self.agent_ids()
        return [self.hub()]

    def can_escalate(self, agent: str) -> bool:
        if self.human_channel == "anyone":
            return True
        if self.human_channel == "hub_only":
            return agent == self.hub()
        return False
