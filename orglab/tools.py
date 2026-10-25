"""Werkzeuge der Agenten. Backend-neutral definiert; jedes Backend bindet sie auf seine Art an.

Welche Werkzeuge ein Agent bekommt, hängt von der Org-Config ab (Board, Notizbuch, Rollen,
Menschenkanal). Jeder Aufruf wird geloggt und gegen das Tick-Budget gezählt.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable

from .world import World


@dataclass
class ToolSpec:
    name: str
    description: str
    schema: dict[str, Any]
    handler: Callable[[str, dict[str, Any]], str]


def _obj(props: dict[str, Any], required: list[str] | None = None) -> dict[str, Any]:
    return {"type": "object", "properties": props, "required": required if required is not None else list(props)}


S = {"type": "string"}


def build_tools(world: World) -> list[ToolSpec]:
    cfg = world.cfg
    tools = [
        ToolSpec("send_message", "Send a message to a teammate (agent id like 'a2') or to 'all' reachable teammates.",
                 _obj({"to": S, "text": S}), lambda a, x: world.send_message(a, x["to"], x["text"])),
        ToolSpec("list_items", "List the work items you know about, with dependencies, owner and reported status.",
                 _obj({}), lambda a, x: world.list_items(a)),
        ToolSpec("claim_item", "Take ownership of a work item. Only the owner can execute or report it.",
                 _obj({"item_id": S}), lambda a, x: world.claim(a, x["item_id"])),
        ToolSpec("release_item", "Give up ownership of a work item you own.",
                 _obj({"item_id": S}), lambda a, x: world.release(a, x["item_id"])),
        ToolSpec("execute_item", "Carry out a work item you own. Returns the system's status signal.",
                 _obj({"item_id": S}), lambda a, x: world.execute(a, x["item_id"])),
        ToolSpec("inspect_item", "Check the real, current state of any work item you know about.",
                 _obj({"item_id": S}), lambda a, x: world.inspect(a, x["item_id"])),
        ToolSpec("report_done", "Mark a work item you own as done, with a short note.",
                 _obj({"item_id": S, "note": S}), lambda a, x: world.report_done(a, x["item_id"], x.get("note", ""))),
    ]
    if cfg.human_channel != "none":
        tools.append(ToolSpec("contact_human", "Send a message to the responsible human (escalation, questions, blockers). "
                              "The human answers next tick.", _obj({"text": S}), lambda a, x: world.escalate(a, x["text"])))
    if cfg.shared_notes:
        tools += [
            ToolSpec("add_note", "Write an entry into the team's shared notebook.", _obj({"text": S}),
                     lambda a, x: world.add_note(a, x["text"])),
            ToolSpec("read_notes", "Read the team's shared notebook.", _obj({}), lambda a, x: world.read_notes(a)),
        ]
    if cfg.reassign_quorum:
        tools.append(ToolSpec("vote_reassign", f"Vote to take over a work item owned by another agent, e.g. if it is "
                              f"reported done but does not work and its owner does not fix it. When {cfg.reassign_quorum} "
                              "teammates have voted, the item is reassigned to the voter who completes the quorum.",
                              _obj({"item_id": S, "reason": S}), lambda a, x: world.vote_reassign(a, x["item_id"], x.get("reason", ""))))
    if cfg.role_mode == "self_select":
        tools.append(ToolSpec("declare_role", "Choose your role in the team: " +
                              "; ".join(f"{r.name}: {r.mandate}" for r in cfg.roles),
                              _obj({"role": S}), lambda a, x: world.declare_role(a, x["role"])))
    return [_metered(world, t) for t in tools]


def _metered(world: World, spec: ToolSpec) -> ToolSpec:
    inner = spec.handler

    def handler(agent: str, args: dict[str, Any]) -> str:
        world.turn_calls[agent] += 1
        if world.turn_calls[agent] > world.cfg.max_tool_calls:
            result = "ERROR: tool budget for this tick is used up. End your turn now."
        else:
            try:
                result = inner(agent, args)
            except KeyError as e:
                result = f"ERROR: missing argument {e}"
        world.log.emit("tool_call", agent, tool=spec.name, args=args, result=result[:500])
        return result

    return ToolSpec(spec.name, spec.description, spec.schema, handler)


def system_prompt(world: World, agent: str) -> str:
    cfg = world.cfg
    lines = [f"You are agent {agent} in a team of {cfg.n_agents} AI agents working on a shared assignment.",
             "You act in the world only through your tools. The world advances in ticks; each tick you receive new "
             "information and may make a limited number of tool calls."]
    if cfg.role_mode == "fixed":
        role = next(r for r in cfg.roles if r.name == world.roles[agent])
        lines.append(f"Your role: {role.name} – {role.mandate}")
        others = [f"{a}: {world.roles[a]}" for a in world.agents if a != agent]
        lines.append("Teammates' roles: " + ", ".join(others))
    elif cfg.role_mode == "self_select":
        lines.append("Roles are not assigned. You may choose one with declare_role if it helps the team.")
    nb = cfg.neighbors(agent)
    lines.append(f"You can message: {', '.join(nb) if nb else 'nobody'}.")
    if cfg.board:
        lines.append("There is a shared board: everyone sees all work items with owner and reported status.")
    else:
        lines.append("There is no shared board: you only see items you were told about or own.")
    if cfg.shared_notes:
        lines.append("There is a shared notebook the whole team can read and write.")
    if cfg.can_escalate(agent):
        lines.append("You can contact the responsible human with contact_human.")
    elif cfg.human_channel == "none":
        lines.append("There is no human you can contact; the team has to resolve everything itself.")
    if cfg.stale_release_ticks:
        lines.append(f"Deadline rule: an item reported done that fails a check by a teammate and is not re-executed by its "
                     f"owner within {cfg.stale_release_ticks} ticks is released automatically and anyone can claim it.")
    if cfg.reassign_quorum:
        lines.append(f"The team can take over an item from its owner by vote (vote_reassign, {cfg.reassign_quorum} votes needed).")
    if cfg.norms:
        lines.append("Team rules:\n" + "\n".join(f"- {n}" for n in cfg.norms))
    private = world.scenario.private_brief(world, agent)
    if private:
        lines.append(private)
    return "\n".join(lines)
