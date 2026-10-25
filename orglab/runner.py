"""Ein Run = Szenario × Domäne × Org-Config × Seed × Backend.

Schreibt in sein Verzeichnis: events.jsonl (Rohdaten, unveränderlich), run.json (alle
Metadaten zur Reproduktion), metrics.json (Auswertung). metrics.json wird zuletzt
geschrieben und markiert einen Run als abgeschlossen.
"""

from __future__ import annotations

import functools
import json
import platform
import random
import subprocess
import time
from dataclasses import asdict
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path
from typing import Any

from . import limits
from .config import OrgConfig
from .events import EventLog
from .metrics import generic_metrics
from .scenarios import get_scenario
from .tools import build_tools, system_prompt
from .world import World

ROOT = Path(__file__).resolve().parent.parent


class BackendFailure(RuntimeError):
    """Das Backend liefert keine echten Agenten-Züge (Login, Rate-Limit, Netz).

    Ein solcher Run wird abgebrochen und NICHT als Ergebnis gespeichert, sonst sähe ein
    technischer Ausfall aus wie eine Organisation, die nichts tut.
    """


@functools.lru_cache(maxsize=1)
def code_version() -> dict[str, Any]:
    """Einmal pro Prozess ermittelt: Ein laufender Sweep nutzt den Code von seinem Start,
    auch wenn währenddessen neue Commits entstehen."""
    def git(*args: str) -> str:
        try:
            return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True, timeout=10).stdout.strip()
        except Exception:
            return ""
    try:
        sdk = version("claude-agent-sdk")
    except PackageNotFoundError:
        sdk = None
    return {"git_commit": git("rev-parse", "HEAD") or None, "git_dirty": bool(git("status", "--porcelain", "orglab")),
            "claude_agent_sdk": sdk, "python": platform.python_version()}


def make_backend(spec: dict[str, Any], world: World):
    backend = _make_single_backend(spec, world)
    moles = set(world.instance.ground_truth.get("moles", []))
    if spec.get("scripted_moles") and moles:
        # D-012: Maulwürfe als hartnäckige Skripte, ehrliche Agenten bleiben beim primären Backend
        from .backends.mixed import MixedBackend
        from .backends.scripted import ScriptedBackend
        backend = MixedBackend(backend, ScriptedBackend(world, "naive", mole_votes=bool(spec.get("mole_votes"))), moles)
    return backend


def _make_single_backend(spec: dict[str, Any], world: World):
    kind = spec["kind"]
    if kind == "scripted":
        from .backends.scripted import ScriptedBackend
        return ScriptedBackend(world, spec.get("policy", "diligent"))
    if kind == "agent_sdk":
        from .backends.agent_sdk import AgentSDKBackend
        return AgentSDKBackend(spec.get("model", "claude-sonnet-5-5"), spec.get("effort", "medium"),
                               world.cfg.max_tool_calls)
    raise ValueError(f"Unbekanntes Backend {kind}")


async def run_one(scenario_name: str, domain: str, cfg: OrgConfig, seed: int,
                  backend_spec: dict[str, Any], out_dir: Path | None = None) -> dict[str, Any]:
    if out_dir:
        out_dir.mkdir(parents=True, exist_ok=True)
        for f in ("events.jsonl", "metrics.json"):
            (out_dir / f).unlink(missing_ok=True)   # unvollständiger Vor-Run wird komplett neu gemacht
    if backend_spec.get("kind", "agent_sdk") != "scripted":
        await limits.wait_for_budget()   # kein Run startet in ein volles Abo-Limit (orglab/limits.py)
    scenario = get_scenario(scenario_name)
    instance = scenario.generate(seed, domain, cfg)
    if backend_spec.get("scripted_moles"):
        instance.ground_truth["scripted_moles"] = True
    log = EventLog(out_dir / "events.jsonl" if out_dir else None)
    rng = random.Random(f"order:{seed}")
    world = World(cfg, scenario, instance, log, rng)
    backend = make_backend(backend_spec, world)
    meta = {"scenario": scenario_name, "domain": domain, "seed": seed, "config_name": cfg.name,
            "config_hash": cfg.hash(), "config": cfg.to_dict(), "backend": backend_spec,
            "model": backend.model, "code": code_version(), "instance": asdict(instance),
            "started": time.strftime("%Y-%m-%dT%H:%M:%S")}
    if out_dir:
        (out_dir / "run.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
    log.emit("run_start", None, **{k: meta[k] for k in ("scenario", "domain", "seed", "config_hash", "model")})
    t0 = time.time()
    end_reason = "max_ticks"
    try:
        tools = build_tools(world)
        for a in world.agents:
            await backend.start(a, system_prompt(world, a), tools)
        for tick in range(1, cfg.max_ticks + 1):
            world.start_tick(tick)
            log.emit("tick_start")
            order = list(world.agents)
            rng.shuffle(order)
            calls_this_tick = 0
            for a in order:
                world.turn_calls[a] = 0
                prompt = world.turn_prompt(a)
                log.emit("agent_turn_start", a, prompt=prompt)
                r = await backend.turn(a, prompt)
                calls = min(world.turn_calls[a], cfg.max_tool_calls + 1)
                calls_this_tick += calls
                log.emit("agent_turn_end", a, tool_calls=world.turn_calls[a], text=r.text, error=r.error,
                         input_tokens=r.input_tokens, output_tokens=r.output_tokens,
                         cache_read_tokens=r.cache_read_tokens, cost_usd=r.cost_usd, raw=r.raw)
                # Jeder fehlerhafte Agenten-Zug macht den Run ungültig: Der Agent konnte nicht handeln.
                # (Früher erst nach n Fehlern in Folge – in gemischten Teams setzten fehlerfreie Skript-Agenten
                # den Zähler zurück, und Session-Limit-Runs landeten als scheinbar gültige Ergebnisse in E-008.)
                if r.error:
                    log.emit("backend_failure", a, error=r.error)
                    raise BackendFailure(r.error)
                if world.all_done():
                    break
            if world.all_done():
                end_reason = "all_done"
                break
            if calls_this_tick == 0 and not world.human_pending and not any(world.inbox.values()):
                end_reason = "quiescent"   # alle schweigen, nichts unterwegs: die Org hat aufgehört
                break
    except BaseException:
        log.close()   # Run bleibt ohne metrics.json, gilt also als nicht abgeschlossen
        raise
    finally:
        await backend.close()
    metrics = {"end_reason": end_reason, "wall_s": round(time.time() - t0, 1),
               **scenario.evaluate(world), **generic_metrics(world)}
    log.emit("run_end", None, end_reason=end_reason, metrics=metrics)
    log.close()
    if out_dir:
        (out_dir / "metrics.json").write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    return metrics
