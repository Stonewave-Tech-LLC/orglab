import asyncio
from pathlib import Path

import pytest

from orglab.config import OrgConfig
from orglab.events import load_events
from orglab.runner import ROOT, run_one

VALID = OrgConfig.load(ROOT / "configs" / "validation.yaml")


def run(policy, domain="coding", seed=0, cfg=VALID, out=None):
    return asyncio.run(run_one("phantom_done", domain, cfg, seed, {"kind": "scripted", "policy": policy}, out))


@pytest.mark.parametrize("domain", ["coding", "business", "research"])
def test_diligent_completes_and_naive_leaves_phantoms(domain):
    d = run("diligent", domain)
    n = run("naive", domain)
    assert d["true_completion"] == 1.0 and d["false_done"] == 0
    assert n["true_completion"] < 1.0 and n["false_done"] > 0
    assert d["phantoms_diagnosed"] == 1.0


def test_hard_variant_regressions_need_vigilance():
    def hard(policy, seed):
        return asyncio.run(run_one("phantom_hard", "coding", VALID, seed, {"kind": "scripted", "policy": policy}))
    vig = [hard("vigilant", s) for s in range(5)]
    dil = [hard("diligent", s) for s in range(5)]
    assert all(m["true_completion"] == 1.0 and m["regressions_repaired"] == 1.0 for m in vig)
    assert sum(m["regressions"] for m in dil) > 0
    assert sum(m["true_completion"] for m in dil) < sum(m["true_completion"] for m in vig)


def test_phantom_done_generation_unchanged_by_hard_variant():
    from orglab.scenarios import get_scenario
    inst = get_scenario("phantom_done").generate(0, "coding", VALID)
    assert len(inst.items) == 8 and all(it.hidden.get("breaks") is None for it in inst.items)


def test_idle_is_quiescent():
    m = run("idle")
    assert m["true_completion"] == 0 and m["end_reason"] == "quiescent"


def test_generation_is_deterministic():
    from orglab.scenarios import get_scenario
    s = get_scenario("phantom_done")
    assert s.generate(7, "coding", VALID) == s.generate(7, "coding", VALID)
    assert s.generate(7, "coding", VALID) != s.generate(8, "coding", VALID)


def test_run_writes_complete_record(tmp_path: Path):
    run("diligent", out=tmp_path)
    assert {"events.jsonl", "run.json", "metrics.json"} <= {p.name for p in tmp_path.iterdir()}
    ev = load_events(tmp_path / "events.jsonl")
    assert ev[0]["type"] == "run_start" and ev[-1]["type"] == "run_end"
    assert [e["seq"] for e in ev] == list(range(len(ev)))


def test_topology_and_permissions():
    cfg = OrgConfig.load(ROOT / "configs" / "regimes" / "A_contracts.yaml")
    assert cfg.can_message("a0", "a2") and not cfg.can_message("a1", "a2")
    assert cfg.can_escalate("a0") and not cfg.can_escalate("a1")
    assert cfg.entry_agents() == ["a0"]


def test_config_rejects_unknown_fields_and_limits():
    with pytest.raises(ValueError):
        OrgConfig.from_dict({"name": "x", "secret_power": True})
    with pytest.raises(ValueError):
        OrgConfig.from_dict({"name": "x", "n_agents": 99})


def test_emergence_analysis(tmp_path: Path):
    from orglab.emergence import analyze_run
    run("diligent", out=tmp_path)
    e = analyze_run(tmp_path)
    assert 0 <= e["specialization"] <= 1 and e["n_distinct_roles"] >= 1
    assert e["emergent_roles"].count(":") == VALID.n_agents


def test_backend_failure_aborts_without_metrics(tmp_path: Path, monkeypatch):
    from orglab import runner
    from orglab.backends.base import TurnResult

    class Broken:
        name, model = "broken", "broken"
        async def start(self, *a): pass
        async def turn(self, *a): return TurnResult(error="Not logged in")
        async def close(self): pass

    monkeypatch.setattr(runner, "make_backend", lambda spec, world: Broken())
    with pytest.raises(runner.BackendFailure):
        asyncio.run(run_one("phantom_done", "coding", VALID, 0, {"kind": "broken"}, tmp_path))
    assert not (tmp_path / "metrics.json").exists()


def test_mole_dose_and_private_brief():
    from orglab.scenarios import get_scenario
    from orglab.tools import system_prompt
    from orglab.world import World
    from orglab.events import EventLog
    import random
    s = get_scenario("mole_1")
    inst = s.generate(5, "business", VALID)
    mole = inst.ground_truth["moles"][0]
    w = World(VALID, s, inst, EventLog(None), random.Random(0))
    assert "PRIVATE" in system_prompt(w, mole) and "PRIVATE" not in system_prompt(w, "a0")
    m_aud = asyncio.run(run_one("mole_1", "business", VALID, 5, {"kind": "scripted", "policy": "auditor"}))
    m_vig = asyncio.run(run_one("mole_1", "business", VALID, 5, {"kind": "scripted", "policy": "vigilant"}))
    assert m_aud["reassignments"] > 0 and m_aud["true_completion"] > m_vig["true_completion"]
    assert m_vig["mole_false_reports"] > 0


def test_bh_qvalues():
    from orglab.analyze import bh_qvalues
    q = bh_qvalues([0.01, 0.04, 0.03, 0.5])
    assert q == pytest.approx([0.04, 0.0533333, 0.0533333, 0.5], rel=1e-4)


def test_all_regimes_load():
    for p in (ROOT / "configs" / "regimes").glob("*.yaml"):
        OrgConfig.load(p)


def test_mixed_team_scripted_moles_persist():
    # ehrliche Agenten tun nichts (idle), geskriptete Maulwürfe melden trotzdem falsch – und gestehen nie
    m = asyncio.run(run_one("mole_2", "coding", VALID, 1, {"kind": "scripted", "policy": "idle", "scripted_moles": True}))
    assert m["mole_false_reports"] > 0 and m["true_completion"] == 0.0
    from orglab.scenarios import get_scenario
    from orglab.world import World
    from orglab.events import EventLog
    from orglab.tools import system_prompt
    import random
    s = get_scenario("mole_2"); inst = s.generate(1, "coding", VALID); inst.ground_truth["scripted_moles"] = True
    w = World(VALID, s, inst, EventLog(None), random.Random(0))
    assert all("PRIVATE" not in system_prompt(w, a) for a in w.agents)


def test_vote_reassign_governance_without_human():
    base = VALID.to_dict()
    no_vote = OrgConfig.from_dict({**base, "name": "nh", "human_channel": "none"})
    vote = OrgConfig.from_dict({**base, "name": "nhv", "human_channel": "none", "reassign_quorum": 2})
    assert no_vote.hash() != vote.hash() and VALID.hash() == OrgConfig.from_dict(base).hash()
    run_ = lambda cfg, s: asyncio.run(run_one("mole_1", "coding", cfg, s, {"kind": "scripted", "policy": "auditor"}))
    without = [run_(no_vote, s) for s in range(4)]
    with_vote = [run_(vote, s) for s in range(4)]
    # Fehlurteile (Übernahme von Ehrlichen, deren Paket gerade regrediert ist) sind möglich, aber seltener
    assert sum(m["reassigned_from_moles"] for m in with_vote) > sum(m["reassigned_from_honest"] for m in with_vote)
    assert sum(m["true_completion"] for m in with_vote) > sum(m["true_completion"] for m in without)


def test_stale_release_deadline_rule():
    cfg = OrgConfig.from_dict({**VALID.to_dict(), "name": "dl", "human_channel": "none", "stale_release_ticks": 1})
    assert "stale_release_ticks" in cfg.to_dict() and "stale_release_ticks" not in VALID.to_dict()
    ms = [asyncio.run(run_one("mole_1", "coding", cfg, s, {"kind": "scripted", "policy": "auditor"})) for s in range(3)]
    assert sum(m["auto_released_from_moles"] for m in ms) > 0


def test_single_turn_error_in_mixed_team_invalidates_run(tmp_path: Path, monkeypatch):
    from orglab import runner
    from orglab.backends.base import TurnResult
    from orglab.backends.mixed import MixedBackend
    from orglab.backends.scripted import ScriptedBackend

    class FlakyLLM:
        name, model = "flaky", "flaky"
        async def start(self, *a): pass
        async def turn(self, agent, prompt): return TurnResult(error="You've hit your session limit")
        async def close(self): pass

    monkeypatch.setattr(runner, "make_backend",
                        lambda spec, world: MixedBackend(FlakyLLM(), ScriptedBackend(world, "naive"), {"a1"}))
    with pytest.raises(runner.BackendFailure):
        asyncio.run(run_one("mole_1", "coding", VALID, 0, {"kind": "x"}, tmp_path))
    assert not (tmp_path / "metrics.json").exists()


def test_voting_moles_can_steal_honest_items():
    cfg = OrgConfig.from_dict({**VALID.to_dict(), "name": "nhv", "human_channel": "none", "reassign_quorum": 2})
    spec = {"kind": "scripted", "policy": "auditor", "scripted_moles": True, "mole_votes": True}
    ms = [asyncio.run(run_one("mole_2", "coding", cfg, s, spec)) for s in range(4)]
    assert sum(m["reassigned_from_honest"] for m in ms) > 0
