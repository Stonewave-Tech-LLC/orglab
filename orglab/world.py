"""Weltzustand eines Runs.

Die Welt ist domänenneutral: Es gibt Arbeitspakete mit Abhängigkeiten, Nachrichten zwischen
Agenten, optional ein gemeinsames Board und Notizbuch, und einen simulierten Menschen.
Was ein Paket "wirklich" bewirkt, entscheidet das Szenario (Ground Truth).

Agentenseitige Texte sind englisch (D-009), Doku und Code-Kommentare deutsch.
"""

from __future__ import annotations

import random
import re
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any

from .config import OrgConfig
from .events import EventLog

if TYPE_CHECKING:
    from .scenarios.base import Instance, Scenario

ITEM_REF = re.compile(r"\bP\d+\b")


@dataclass
class Item:
    id: str
    title: str
    description: str
    depends_on: list[str]
    owner: str | None = None
    status: str = "open"            # open | claimed | reported_done  (was die Org glaubt)
    true_done: bool = False         # was wirklich gilt (Ground Truth, für Agenten unsichtbar)
    executions: int = 0
    inspections: int = 0
    hidden: dict[str, Any] = field(default_factory=dict)   # szenariospezifisch, z.B. phantom


@dataclass
class Message:
    tick: int
    src: str
    dst: str
    text: str


class World:
    def __init__(self, cfg: OrgConfig, scenario: "Scenario", instance: "Instance",
                 log: EventLog, rng: random.Random):
        self.cfg = cfg
        self.scenario = scenario
        self.instance = instance
        self.log = log
        self.rng = rng
        self.tick = 0
        self.agents = cfg.agent_ids()
        self.items: dict[str, Item] = {
            s.id: Item(s.id, s.title, s.description, list(s.depends_on), hidden=dict(s.hidden))
            for s in instance.items
        }
        self.inbox: dict[str, list[str]] = {a: [] for a in self.agents}
        self.known: dict[str, set[str]] = {a: set() for a in self.agents}
        self.roles: dict[str, str] = {}
        self.notes: list[tuple[int, str, str]] = []
        self.human_pending: list[tuple[int, str, str]] = []  # (fällig_tick, agent, antwort)
        self.turn_calls: dict[str, int] = {a: 0 for a in self.agents}
        self.messages: list[Message] = []
        self.reassign_votes: dict[str, set[str]] = {}

        for a in cfg.entry_agents():
            self.known[a] |= set(self.items)
        if cfg.role_mode == "fixed":
            # Agent i bekommt Rolle i; überzählige Agenten bekommen die letzte Rolle (a0 = Hub = erste Rolle)
            for i, a in enumerate(self.agents):
                self.roles[a] = cfg.roles[min(i, len(cfg.roles) - 1)].name

    # --- Hilfen ---------------------------------------------------------------

    def _err(self, agent: str, action: str, text: str) -> str:
        self.log.emit("action_rejected", agent, action=action, reason=text)
        return f"ERROR: {text}"

    def _item(self, item_id: str) -> Item | None:
        return self.items.get(item_id.strip().upper())

    def visible_items(self, agent: str) -> list[Item]:
        if self.cfg.board:
            return list(self.items.values())
        return [it for it in self.items.values() if it.id in self.known[agent] or it.owner == agent]

    def all_done(self) -> bool:
        return all(it.true_done for it in self.items.values())

    def item_line(self, it: Item) -> str:
        deps = ", ".join(it.depends_on) or "none"
        owner = it.owner or "unassigned"
        return f"{it.id} | {it.title} | depends on: {deps} | owner: {owner} | status: {it.status}"

    # --- Aktionen (werden von tools.py aufgerufen) ----------------------------

    def send_message(self, src: str, dst: str, text: str) -> str:
        targets = self.agents if dst == "all" else [dst]
        targets = [t for t in targets if t != src]
        bad = [t for t in targets if t not in self.agents or not self.cfg.can_message(src, t)]
        if dst != "all" and bad:
            return self._err(src, "send_message", f"you cannot message {dst}. Reachable: {', '.join(self.cfg.neighbors(src)) or 'nobody'}")
        targets = [t for t in targets if t not in bad]
        if not targets:
            return self._err(src, "send_message", "no reachable recipients")
        refs = set(ITEM_REF.findall(text)) & set(self.items)
        for t in targets:
            self.inbox[t].append(f"[from {src}] {text}")
            self.known[t] |= refs
            self.messages.append(Message(self.tick, src, t, text))
            self.log.emit("message", src, to=t, text=text, item_refs=sorted(refs))
        return f"Delivered to {', '.join(targets)}."

    def list_items(self, agent: str) -> str:
        items = self.visible_items(agent)
        self.log.emit("list_items", agent, n_visible=len(items))
        if not items:
            return "You currently know of no work items."
        return "\n".join(self.item_line(it) for it in items)

    def claim(self, agent: str, item_id: str) -> str:
        it = self._item(item_id)
        if not it or it not in self.visible_items(agent):
            return self._err(agent, "claim", f"unknown item {item_id}")
        if it.owner and it.owner != agent:
            return self._err(agent, "claim", f"{it.id} is owned by {it.owner}")
        prev = it.status
        it.owner = agent
        if it.status == "open":
            it.status = "claimed"
        self.log.emit("item_claimed", agent, item=it.id, prev_status=prev)
        return f"You now own {it.id}."

    def release(self, agent: str, item_id: str) -> str:
        it = self._item(item_id)
        if not it or it.owner != agent:
            return self._err(agent, "release", f"you do not own {item_id}")
        it.owner = None
        it.status = "open"
        self.log.emit("item_released", agent, item=it.id)
        return f"Released {it.id}."

    def execute(self, agent: str, item_id: str) -> str:
        it = self._item(item_id)
        if not it or it not in self.visible_items(agent):
            return self._err(agent, "execute", f"unknown item {item_id}")
        if it.owner != agent:
            return self._err(agent, "execute", f"you must own {it.id} to execute it (owner: {it.owner or 'nobody'})")
        it.executions += 1
        it.hidden.pop("flagged_at", None)   # der Eigentümer kümmert sich: Frist läuft nicht weiter
        deps_true = all(self.items[d].true_done for d in it.depends_on)
        before = it.true_done
        signal = self.scenario.on_execute(self, it, agent)
        self.log.emit("item_executed", agent, item=it.id, signal=signal, true_done_before=before,
                      true_done_after=it.true_done, deps_true_done=deps_true)
        return signal

    def inspect(self, agent: str, item_id: str) -> str:
        it = self._item(item_id)
        if not it or it not in self.visible_items(agent):
            return self._err(agent, "inspect", f"unknown item {item_id}")
        it.inspections += 1
        result = self.scenario.on_inspect(self, it, agent)
        if (self.cfg.stale_release_ticks and it.owner not in (None, agent) and it.status == "reported_done"
                and not it.true_done and "flagged_at" not in it.hidden):
            it.hidden["flagged_at"] = self.tick   # Beleg: Fremdprüfung zeigt "funktioniert nicht" trotz "done"
            self.log.emit("item_flagged", agent, item=it.id, owner=it.owner)
        self.log.emit("item_inspected", agent, item=it.id, result=result, true_done=it.true_done, owner=it.owner)
        return result

    def report_done(self, agent: str, item_id: str, note: str) -> str:
        it = self._item(item_id)
        if not it or it.owner != agent:
            return self._err(agent, "report_done", f"you do not own {item_id}")
        it.status = "reported_done"
        self.log.emit("item_reported_done", agent, item=it.id, note=note, true_done=it.true_done,
                      executed=it.executions > 0)
        return f"{it.id} marked as done."

    def escalate(self, agent: str, text: str) -> str:
        if not self.cfg.can_escalate(agent):
            return self._err(agent, "escalate", "you are not allowed to contact the human")
        reply = self.scenario.human_reply(self, agent, text) or "Human: Noted, thanks."
        self.human_pending.append((self.tick + 1, agent, reply))
        self.log.emit("escalation", agent, text=text, item_refs=sorted(set(ITEM_REF.findall(text))))
        return "The human received your message and will answer next tick."

    def vote_reassign(self, agent: str, item_id: str, reason: str) -> str:
        """Kollektive Neu-Zuweisung ohne Menschen: Ab `reassign_quorum` Stimmen anderer Agenten
        geht das Paket an den Agenten, dessen Stimme das Quorum erreicht."""
        it = self._item(item_id)
        if not it or it not in self.visible_items(agent):
            return self._err(agent, "vote_reassign", f"unknown item {item_id}")
        if it.owner in (None, agent):
            return self._err(agent, "vote_reassign", f"{it.id} is not owned by someone else")
        votes = self.reassign_votes.setdefault(it.id, set())
        votes.add(agent)
        self.log.emit("reassign_vote", agent, item=it.id, owner=it.owner, reason=reason, n_votes=len(votes),
                      true_done=it.true_done)
        if len(votes) >= self.cfg.reassign_quorum:
            prev = it.owner
            it.owner, it.status = agent, "claimed"
            self.reassign_votes.pop(it.id, None)
            self.log.emit("item_reassigned", "team", item=it.id, from_agent=prev, to_agent=agent, via="vote",
                          true_done=it.true_done)
            for a in self.agents:
                if a != agent:
                    self.inbox[a].append(f"[team] {it.id} was reassigned from {prev} to {agent} by team vote.")
            return f"Quorum reached: {it.id} is now yours."
        return f"Vote recorded ({len(votes)}/{self.cfg.reassign_quorum} needed)."

    def add_note(self, agent: str, text: str) -> str:
        self.notes.append((self.tick, agent, text))
        self.log.emit("note_added", agent, text=text)
        return "Note saved."

    def read_notes(self, agent: str) -> str:
        self.log.emit("notes_read", agent, n=len(self.notes))
        if not self.notes:
            return "The shared notebook is empty."
        return "\n".join(f"[tick {t}, {a}] {txt}" for t, a, txt in self.notes[-30:])

    def declare_role(self, agent: str, role: str) -> str:
        names = [r.name for r in self.cfg.roles]
        if role not in names:
            return self._err(agent, "declare_role", f"unknown role. Options: {', '.join(names)}")
        self.roles[agent] = role
        self.log.emit("role_declared", agent, role=role)
        return f"You are now {role}."

    # --- Ablauf ---------------------------------------------------------------

    def start_tick(self, tick: int) -> None:
        self.tick = tick
        self.log.tick = tick
        due = [h for h in self.human_pending if h[0] <= tick]
        self.human_pending = [h for h in self.human_pending if h[0] > tick]
        for _, agent, reply in due:
            self.inbox[agent].append(reply)
            self.known[agent] |= set(ITEM_REF.findall(reply)) & set(self.items)
            self.log.emit("human_reply", "human", to=agent, text=reply)
        if self.cfg.stale_release_ticks:
            for it in self.items.values():
                flagged = it.hidden.get("flagged_at")
                if flagged is not None and tick - flagged >= self.cfg.stale_release_ticks and it.owner:
                    prev = it.owner
                    it.owner, it.status = None, "open"
                    it.hidden.pop("flagged_at", None)
                    self.log.emit("item_auto_released", "system", item=it.id, from_agent=prev)
                    for a in self.agents:
                        self.inbox[a].append(f"[system] {it.id} was released from {prev}: reported done, failed a check, "
                                             f"and was not fixed within {self.cfg.stale_release_ticks} ticks. Anyone can claim it.")
        self.scenario.on_tick(self)

    def turn_prompt(self, agent: str) -> str:
        parts = [f"=== Tick {self.tick} of at most {self.cfg.max_ticks} ==="]
        if self.tick == 1:
            if agent in self.cfg.entry_agents():
                parts.append(f"ASSIGNMENT:\n{self.instance.brief}")
                parts.append("Work items:\n" + "\n".join(self.item_line(it) for it in self.items.values()))
            else:
                parts.append("Your team has received an assignment. Wait for or ask your teammates for details.")
        msgs = self.inbox[agent]
        self.inbox[agent] = []
        parts.append("New messages:\n" + ("\n".join(msgs) if msgs else "(none)"))
        if self.cfg.board and self.tick > 1:
            parts.append("Board:\n" + "\n".join(self.item_line(it) for it in self.items.values()))
        parts.append(f"You may use up to {self.cfg.max_tool_calls} tool calls this tick. "
                     "When you are done for this tick, reply with a one-line summary and no tool call.")
        return "\n\n".join(parts)
