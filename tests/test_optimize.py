"""Mechanik-Test des Optimierers ohne LLM: Fake-Editor + Agenten, die Normen befolgen."""

import asyncio
import json

from orglab.config import OrgConfig
from orglab.optimize import Optimizer
from orglab.runner import ROOT


async def fake_editor(prompt: str, system: str) -> str:
    if "Propose exactly two" in prompt:
        cur = json.loads(prompt.split("```json", 1)[1].split("```", 1)[0])
        inv = dict(cur, norms=cur["norms"] + ["Before reporting an item done, verify its real state with inspect_item."])
        spec = dict(cur, board=True, max_ticks=40)   # max_ticks ist gesperrt und muss ignoriert werden
        return "```json\n" + json.dumps({"diagnosis": "flags trusted", "candidates": [
            {"kind": "invariant", "rationale": "verify effect", "config": inv},
            {"kind": "specific", "rationale": "board", "config": spec}]}) + "\n```"
    return "## Situation\n...\nSUMMARY: Verifying effect before reporting done fixes phantom completions."


def test_optimizer_accepts_real_improvement_and_rejects_noise(tmp_path):
    start = OrgConfig.load(ROOT / "configs" / "regimes" / "B_minimal.yaml")
    opt = Optimizer(tmp_path / "opt", start, "phantom_done", ["coding", "business"], ["research"],
                    seeds_per_probe=4, backend={"kind": "scripted", "policy": "norm"}, concurrency=4,
                    editor=fake_editor, require_validation=False, holdout_every=1, holdout_seeds=4)
    asyncio.run(opt.run(iterations=1, hours=1, patience=3))
    s = opt.state
    accepted = [h for h in s["history"] if h["accepted"]]
    assert len(accepted) == 1 and accepted[0]["kind"] == "invariant"
    spec = next(h for h in s["history"] if h["kind"] == "specific")
    assert not spec["accepted"] and "max_ticks" not in spec["diff"]
    assert any("inspect_item" in n for n in s["current"]["norms"])
    assert s["holdout"] and s["holdout"][-1]["mean_diff"] > 0      # Transfer auf ungesehene Domäne
    assert (tmp_path / "opt" / "bericht.md").exists()
    assert list((tmp_path / "opt" / "library").glob("*/EXPERIENCE.md"))


def test_adaptive_gate_extends_promising_candidates(tmp_path, monkeypatch):
    start = OrgConfig.load(ROOT / "configs" / "regimes" / "B_minimal.yaml")
    opt = Optimizer(tmp_path / "opt2", start, "phantom_done", ["coding"], [], seeds_per_probe=5,
                    backend={"kind": "scripted", "policy": "norm"}, concurrency=2, editor=fake_editor,
                    require_validation=False, max_seeds_per_probe=15, extend_step=5)
    probes, verdicts = [], iter([{"mean_diff": 0.04, "p": 0.3, "passed": False},
                                 {"mean_diff": 0.04, "p": 0.08, "passed": True}])

    async def fake_probe(cfgs, probe_dir, seeds, domains):
        probes.append(list(seeds))

    monkeypatch.setattr(opt, "_probe", fake_probe)
    monkeypatch.setattr(opt, "_gate", lambda base, cand: dict(next(verdicts)))
    gate = asyncio.run(opt._adaptive_gate(1, start, start, "x", tmp_path))
    assert gate["passed"] and gate["seeds_per_domain"] == 10 and probes == [list(range(1005, 1010))]
