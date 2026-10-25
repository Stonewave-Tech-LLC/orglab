"""Viele Runs: Configs × Domänen × Seeds, parallel mit begrenzter Gleichzeitigkeit, fortsetzbar.

Beispiel:
  python -m orglab.sweep --experiment E-001-pilot --scenario phantom_done \
      --configs configs/regimes/A_contracts.yaml configs/regimes/C_stigmergy.yaml \
      --domains coding business --seeds 0-4 --concurrency 2

Fortsetzen: denselben Befehl erneut ausführen; Runs mit metrics.json werden übersprungen.
"""

from __future__ import annotations

import argparse
import asyncio
import json
import time
from pathlib import Path
from typing import Any

from .analyze import report
from .config import OrgConfig
from . import limits
from .runner import ROOT, BackendFailure, run_one

DATA = ROOT / "daten"


def parse_seeds(s: str) -> list[int]:
    out: list[int] = []
    for part in s.split(","):
        if "-" in part:
            a, b = part.split("-")
            out += range(int(a), int(b) + 1)
        else:
            out.append(int(part))
    return out


def run_dir(exp_dir: Path, cfg: OrgConfig, domain: str, seed: int) -> Path:
    return exp_dir / f"{cfg.name}-{cfg.hash()}" / domain / f"seed-{seed:03d}"


async def sweep(experiment: str | Path, scenario: str, configs: list[OrgConfig], domains: list[str], seeds: list[int],
                backend: dict[str, Any], concurrency: int = 2, verbose: bool = True,
                max_backend_retries: int = 8) -> list[dict[str, Any]]:
    exp_dir = Path(experiment) if isinstance(experiment, Path) else DATA / experiment
    exp_dir.mkdir(parents=True, exist_ok=True)
    (exp_dir / "configs").mkdir(exist_ok=True)
    for cfg in configs:
        (exp_dir / "configs" / f"{cfg.name}-{cfg.hash()}.yaml").write_text(cfg.to_yaml(), encoding="utf-8")
    jobs = [(c, d, s) for c in configs for d in domains for s in seeds]
    todo = [j for j in jobs if not (run_dir(exp_dir, *j) / "metrics.json").exists()]
    if verbose:
        print(f"[sweep] {exp_dir.name}: {len(jobs)} Runs, davon {len(jobs) - len(todo)} schon fertig, {len(todo)} offen", flush=True)
    sem = asyncio.Semaphore(concurrency)
    results: list[dict[str, Any]] = []
    done = 0
    t0 = time.time()

    pause_until = 0.0   # gemeinsame Zwangspause aller Jobs nach Backend-Ausfall (z.B. Rate-Limit)

    async def job(cfg: OrgConfig, domain: str, seed: int) -> None:
        nonlocal done, pause_until
        async with sem:
            rd = run_dir(exp_dir, cfg, domain, seed)
            m: dict[str, Any] = {}
            attempt = 0
            while attempt <= max_backend_retries:
                await asyncio.sleep(max(0.0, pause_until - time.time()))
                try:
                    m = await run_one(scenario, domain, cfg, seed, backend, rd)
                    results.append(m)
                    break
                except BackendFailure as e:
                    blocked, _ = limits.blocked_until()
                    if blocked:   # Abo-Limit laut SDK erreicht: bis zum Reset warten, Versuch nicht verbrauchen
                        wait = int(blocked - time.time())
                        pause_until = max(pause_until, blocked)
                    else:
                        wait = min(60 * 2 ** attempt, 3600)
                        pause_until = max(pause_until, time.time() + wait)
                        attempt += 1
                    rd.mkdir(parents=True, exist_ok=True)
                    with open(exp_dir / "backend_failures.log", "a", encoding="utf-8") as fh:
                        fh.write(f"{time.strftime('%Y-%m-%dT%H:%M:%S')} {rd.relative_to(exp_dir)} attempt {attempt}: {e}\n")
                    if verbose:
                        print(f"[sweep] Backend-Ausfall ({e}); Pause {wait // 60} min, Versuch {attempt + 1}/{max_backend_retries}", flush=True)
                    m = {"crash": f"BackendFailure: {e}"}
                except Exception as e:   # ein abgestürzter Run wird protokolliert, der Sweep läuft weiter
                    rd.mkdir(parents=True, exist_ok=True)
                    (rd / "crash.txt").write_text(f"{type(e).__name__}: {e}", encoding="utf-8")
                    m = {"crash": str(e)}
                    break
            done += 1
            if verbose:
                rate = (time.time() - t0) / done
                print(f"[sweep] {done}/{len(todo)} {cfg.name}/{domain}/seed {seed}: "
                      f"{ {k: m.get(k) for k in ('end_reason', 'true_completion', 'false_done_rate', 'crash') if k in m} } "
                      f"(~{rate * (len(todo) - done) / 60:.0f} min übrig)", flush=True)

    await asyncio.gather(*(job(*j) for j in todo))
    (exp_dir / "sweep.json").write_text(json.dumps({
        "scenario": scenario, "configs": [c.name for c in configs], "domains": domains, "seeds": seeds,
        "backend": backend, "concurrency": concurrency, "finished": time.strftime("%Y-%m-%dT%H:%M:%S")},
        indent=2), encoding="utf-8")
    report(exp_dir)
    return results


def main() -> None:
    import sys
    sys.stdout.reconfigure(encoding="utf-8")
    from .keepawake import hold
    hold()
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--experiment", required=True)
    p.add_argument("--scenario", default="phantom_done")
    p.add_argument("--configs", nargs="+", required=True)
    p.add_argument("--domains", nargs="+", default=["coding", "business", "research"])
    p.add_argument("--seeds", default="0-4")
    p.add_argument("--backend", default="agent_sdk", help="agent_sdk | scripted:diligent | scripted:naive")
    p.add_argument("--model", default="claude-sonnet-5-5")
    p.add_argument("--effort", default="medium")
    p.add_argument("--concurrency", type=int, default=2)
    p.add_argument("--scripted-moles", action="store_true", help="Maulwürfe als geskriptete Saboteure (D-012)")
    p.add_argument("--mole-votes", action="store_true", help="geskriptete Maulwürfe stimmen mit falscher Begründung gegen Ehrliche")
    a = p.parse_args()
    if a.backend.startswith("scripted"):
        backend = {"kind": "scripted", "policy": a.backend.split(":")[1] if ":" in a.backend else "diligent"}
    else:
        backend = {"kind": "agent_sdk", "model": a.model, "effort": a.effort}
    if a.scripted_moles:
        backend["scripted_moles"] = True
    if a.mole_votes:
        backend["mole_votes"] = True
    configs = [OrgConfig.load(c) for c in a.configs]
    asyncio.run(sweep(a.experiment, a.scenario, configs, a.domains, parse_seeds(a.seeds), backend, a.concurrency))


if __name__ == "__main__":
    main()
