"""Mess-Validierung (Gate vor jedem Optimierer-Lauf, D-008).

Prüft mit geskripteten Agenten, ob ein Szenario + Auswerter bekannte Unterschiede sicher
erkennt: "diligent" (prüft Wirkung) muss klar besser sein als "naive" (vertraut Flags),
"idle" (tut nichts) muss bei null liegen. Schlägt das fehl, misst das Szenario nicht, was
es messen soll, und darauf darf nicht optimiert werden.

  python -m orglab.validate --scenario phantom_done
"""

from __future__ import annotations

import argparse
import asyncio
import json
import statistics
import time
from pathlib import Path

from .analyze import cohens_d, permutation_test
from .config import OrgConfig
from .runner import ROOT, code_version, run_one
from .scenarios import get_scenario


async def validate(scenario_name: str, seeds: int = 20) -> dict:
    scenario = get_scenario(scenario_name)
    cfg = OrgConfig.load(ROOT / "configs" / "validation.yaml")
    best, worse = scenario.validation_best, tuple(scenario.validation_worse)
    res: dict[str, dict[str, list[float]]] = {}
    for policy in (best, *worse, "idle"):
        res[policy] = {"true_completion": [], "false_done_rate": []}
        for domain in scenario.domains:
            for seed in range(seeds):
                m = await run_one(scenario_name, domain, cfg, seed, {"kind": "scripted", "policy": policy})
                for k in res[policy]:
                    res[policy][k].append(m[k])
    top = res[best]["true_completion"]
    checks = {f"{best}_completes": statistics.fmean(top) >= 0.95,
              f"{best}_few_false_done": statistics.fmean(res[best]["false_done_rate"]) <= 0.02,  # Maulwürfe melden absichtlich falsch
              "idle_is_zero": max(res["idle"]["true_completion"]) == 0.0}
    for w in worse:
        low = res[w]["true_completion"]
        checks[f"{w}_fails_measurably"] = statistics.fmean(low) <= statistics.fmean(top) - 0.1
        checks[f"{w}_vs_{best}_significant"] = permutation_test(top, low) < 0.01
    checks["naive_has_false_done"] = statistics.fmean(res["naive"]["false_done_rate"]) > 0.1
    out = {
        "scenario": scenario_name, "seeds_per_domain": seeds, "domains": list(scenario.domains),
        "means": {p: {k: round(statistics.fmean(v), 3) for k, v in d.items()} for p, d in res.items()},
        "effect_size_d": {w: round(cohens_d(top, res[w]["true_completion"]), 2) for w in worse},
        "checks": checks, "passed": all(checks.values()),
        "code": code_version(), "at": time.strftime("%Y-%m-%dT%H:%M:%S"),
    }
    vdir = ROOT / "daten" / "validierung"
    vdir.mkdir(parents=True, exist_ok=True)
    (vdir / f"{scenario_name}.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    return out


def is_validated(scenario_name: str) -> bool:
    p = ROOT / "daten" / "validierung" / f"{scenario_name}.json"
    return p.exists() and json.loads(p.read_text(encoding="utf-8")).get("passed", False)


def main() -> None:
    import sys
    sys.stdout.reconfigure(encoding="utf-8")
    p = argparse.ArgumentParser()
    p.add_argument("--scenario", default="phantom_done")
    p.add_argument("--seeds", type=int, default=20)
    a = p.parse_args()
    out = asyncio.run(validate(a.scenario, a.seeds))
    print(json.dumps({k: out[k] for k in ("means", "effect_size_d", "checks", "passed")}, indent=2))


if __name__ == "__main__":
    main()
