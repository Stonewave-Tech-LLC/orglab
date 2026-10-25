"""Optimierer: die äußere Schleife (D-007). Propose → Probe → Gate → Compose → Reflect.

Pro Iteration:
  1. Baseline: aktuelle Config auf frischen Trainings-Seeds messen.
  2. Propose: Editor (Opus, ohne Werkzeuge) sieht Config, Kennzahlen, Auszüge der schlechtesten
     Runs, Bibliothek und verworfene Vorschläge und schlägt zwei Kandidaten vor
     (invariant = allgemeine Organisationsschwäche, specific = szenariospezifisch).
  3. Probe: Kandidaten auf denselben Seeds messen (gepaarter Vergleich).
  4. Gate: Übernahme nur bei signifikanter Verbesserung der Primärmetrik und ohne
     Kostenexplosion. Bestehen mehrere, baut der Composer eine Kombination und auch die
     muss das Gate bestehen.
  5. Reflect: Für übernommene Änderungen schreibt der Editor einen EXPERIENCE-Eintrag in die
     Bibliothek; Statistik wird automatisch angehängt.
  Regelmäßig: Transfer-Test auf Holdout-Domänen, die der Editor nie sieht.

Leitplanken, technisch erzwungen:
  - Läuft nur, wenn die Mess-Validierung des Szenarios bestanden ist.
  - Der Editor hat keine Werkzeuge; seine Ausgabe muss als OrgConfig validieren.
  - n_agents, max_ticks, max_tool_calls sind gesperrt (sonst "gewinnt" man durch mehr Budget).
  - Szenarien, Auswerter, Seeds und Holdout-Domänen liegen außerhalb seiner Reichweite.

  python -m orglab.optimize --experiment E-010-opt --start configs/regimes/B_minimal.yaml --hours 48
"""

from __future__ import annotations

import argparse
import asyncio
import json
import statistics
import time
from pathlib import Path
from typing import Any, Awaitable, Callable

from .analyze import collect, paired_permutation_test
from .config import OrgConfig
from .digest import digest
from .llm import complete, extract_json
from .runner import BackendFailure
from .scenarios import get_scenario
from .sweep import DATA, sweep
from .validate import is_validated

LOCKED = ("n_agents", "max_ticks", "max_tool_calls")

EDITOR_SYSTEM = """You are the organisation designer in a research loop. A team of AI agents works on assignments; \
you cannot change the agents or the model, only the ORGANISATION CONFIG they work under. Your job: find \
organisational changes (structure, roles, communication, shared state, norms) that make the team reliably \
produce work that truly works, and that would generalise to other kinds of work.

Config fields you may change:
- topology: "mesh" | "star" | "chain" (star: a0 is the hub)
- board: bool (shared board: everyone sees all items, owners, reported status)
- shared_notes: bool (shared notebook tools)
- human_channel: "anyone" | "hub_only" | "none"
- role_mode: "none" | "fixed" | "self_select"; roles: list of {name, mandate} (fixed: agent i gets role i, extra agents get the last role)
- norms: list of plain-text team rules (max 20, each max 400 chars)
- name, description
Locked (any change is ignored): n_agents, max_ticks, max_tool_calls.

Agent tools: send_message, list_items, claim_item, release_item, execute_item, inspect_item, report_done, \
contact_human (if allowed), add_note/read_notes (if shared_notes), declare_role (if self_select).

Principles: prefer few, general mechanisms over many specific rules; every added rule costs attention. \
Base every change on concrete evidence from the traces. Do not repeat rejected ideas unless you change them materially."""


def _cfg_diff(a: dict[str, Any], b: dict[str, Any]) -> dict[str, Any]:
    return {k: {"from": a.get(k), "to": b.get(k)} for k in sorted(set(a) | set(b)) if a.get(k) != b.get(k) and k != "name"}


def _rows_for(probe_dir: Path, cfg: OrgConfig) -> dict[tuple[str, int], dict[str, Any]]:
    return {(r["domain"], r["seed"]): r for r in collect(probe_dir) if r["config_hash"] == cfg.hash()}


def _mean(rows: dict[Any, dict[str, Any]], metric: str) -> float:
    vals = [float(r[metric]) for r in rows.values() if r.get(metric) is not None]
    return statistics.fmean(vals) if vals else float("nan")


class Optimizer:
    def __init__(self, experiment: str | Path, start: OrgConfig, scenario: str, train_domains: list[str],
                 holdout_domains: list[str], seeds_per_probe: int, backend: dict[str, Any], concurrency: int,
                 editor_model: str = "claude-opus-5-5", alpha: float = 0.1, min_effect: float = 0.02,
                 token_guard: float = 3.0, holdout_every: int = 3, holdout_seeds: int = 10,
                 editor: Callable[[str, str], Awaitable[str]] | None = None, require_validation: bool = True,
                 max_seeds_per_probe: int | None = None, extend_step: int = 5, extend_p: float = 0.5):
        self.dir = Path(experiment) if isinstance(experiment, Path) else DATA / experiment
        self.dir.mkdir(parents=True, exist_ok=True)
        self.scenario = scenario
        self.primary = get_scenario(scenario).primary_metric
        self.train, self.holdout = train_domains, holdout_domains
        self.seeds_per_probe = seeds_per_probe
        self.max_seeds_per_probe = max_seeds_per_probe or seeds_per_probe
        self.extend_step, self.extend_p = extend_step, extend_p
        self.backend, self.concurrency = backend, concurrency
        self.alpha, self.min_effect, self.token_guard = alpha, min_effect, token_guard
        self.holdout_every, self.holdout_seeds = holdout_every, holdout_seeds
        self.editor_model = editor_model
        self._editor = editor
        if require_validation and not is_validated(scenario):
            raise RuntimeError(f"Mess-Validierung für {scenario} fehlt oder ist nicht bestanden: "
                               f"erst `python -m orglab.validate --scenario {scenario}` ausführen.")
        sp = self.dir / "state.json"
        if sp.exists():
            self.state = json.loads(sp.read_text(encoding="utf-8"))
        else:
            self.state = {"iteration": 0, "start": start.to_dict(), "current": start.to_dict(), "history": [],
                          "library": [], "holdout": [], "no_improve": 0, "started": time.strftime("%Y-%m-%dT%H:%M:%S"),
                          "settings": {"scenario": scenario, "train": train_domains, "holdout": holdout_domains,
                                       "seeds_per_probe": seeds_per_probe, "max_seeds_per_probe": self.max_seeds_per_probe, "backend": backend, "alpha": alpha,
                                       "min_effect": min_effect, "token_guard": token_guard, "editor_model": editor_model}}
            self._save()

    # --- Infrastruktur ----------------------------------------------------------

    def _save(self) -> None:
        (self.dir / "state.json").write_text(json.dumps(self.state, ensure_ascii=False, indent=2), encoding="utf-8")

    def _log(self, text: str) -> None:
        line = f"{time.strftime('%Y-%m-%dT%H:%M:%S')} {text}"
        print(f"[opt] {line}", flush=True)
        with open(self.dir / "verlauf.log", "a", encoding="utf-8") as fh:
            fh.write(line + "\n")

    async def _ask(self, prompt: str, out: Path) -> str:
        out.with_suffix(".prompt.md").write_text(prompt, encoding="utf-8")
        if self._editor:
            text = await self._editor(prompt, EDITOR_SYSTEM)
        else:
            text, usage = await complete(prompt, EDITOR_SYSTEM, model=self.editor_model)
            out.with_suffix(".usage.json").write_text(json.dumps(usage, default=str, indent=2), encoding="utf-8")
        out.with_suffix(".response.md").write_text(text, encoding="utf-8")
        return text

    def _parse_cfg(self, d: dict[str, Any], base: OrgConfig, suffix: str) -> OrgConfig:
        d = dict(d)
        for k in LOCKED:
            d[k] = getattr(base, k)
        d["name"] = f"{base.name.split('~')[0]}~{suffix}"
        return OrgConfig.from_dict(d)

    async def _probe(self, cfgs: list[OrgConfig], probe_dir: Path, seeds: list[int], domains: list[str]) -> None:
        await sweep(probe_dir, self.scenario, cfgs, domains, seeds, self.backend, self.concurrency, verbose=False)

    def _gate(self, base: dict, cand: dict) -> dict[str, Any]:
        keys = sorted(set(base) & set(cand))
        diffs = [float(cand[k][self.primary]) - float(base[k][self.primary]) for k in keys]
        tok_b = _mean(base, "output_tokens") or 1.0
        tok_c = _mean(cand, "output_tokens")
        mean_diff = statistics.fmean(diffs) if diffs else 0.0
        p = paired_permutation_test(diffs)
        res = {"n_pairs": len(diffs), "base_mean": _mean(base, self.primary), "cand_mean": _mean(cand, self.primary),
               "mean_diff": mean_diff, "p": p, "token_ratio": (tok_c / tok_b) if tok_b == tok_b and tok_b > 0 else None,
               "base_false_done_rate": _mean(base, "false_done_rate"), "cand_false_done_rate": _mean(cand, "false_done_rate")}
        res["passed"] = bool(len(diffs) >= 4 and mean_diff >= self.min_effect and p < self.alpha
                             and (res["token_ratio"] is None or res["token_ratio"] <= self.token_guard))
        return res

    async def _adaptive_gate(self, it: int, cur: OrgConfig, cfg: OrgConfig, kind: str, probe_dir: Path) -> dict[str, Any]:
        """Sequenzielles Nachmessen (D-011): Vielversprechende Kandidaten (Δ > 0, p < extend_p) bekommen
        weitere gepaarte Seeds für Kandidat UND Baseline, bis das Gate besteht oder max_seeds erreicht ist.
        Optional Stopping erhöht die Falsch-Positiv-Rate etwas. Das ist für die Entdeckungsphase akzeptiert,
        die Bestätigung erfolgt separat auf frischen Seeds (Zwei-Stufen-Regel)."""
        n = self.seeds_per_probe
        while True:
            gate = self._gate(_rows_for(probe_dir, cur), _rows_for(probe_dir, cfg))
            promising = gate["mean_diff"] > 0 and gate["p"] < self.extend_p
            if gate["passed"] or not promising or n >= self.max_seeds_per_probe:
                gate["seeds_per_domain"] = n
                return gate
            more = list(range(it * 1000 + n, it * 1000 + min(n + self.extend_step, self.max_seeds_per_probe)))
            n += len(more)
            self._log(f"  {kind}: vielversprechend (Δ={gate['mean_diff']:+.3f}, p={gate['p']:.3f}), "
                      f"messe nach auf {n} Seeds je Domäne")
            await self._probe([cur, cfg], probe_dir, more, self.train)

    # --- eine Iteration -----------------------------------------------------------

    async def iteration(self) -> None:
        it = self.state["iteration"] + 1
        idir = self.dir / f"iter-{it:03d}"
        idir.mkdir(exist_ok=True)
        probe_dir = idir / "probes"
        cur = OrgConfig.from_dict(self.state["current"])
        seeds = list(range(it * 1000, it * 1000 + self.seeds_per_probe))
        self._log(f"Iteration {it}: Baseline {cur.name} ({cur.hash()}) auf Seeds {seeds[0]}–{seeds[-1]}")
        await self._probe([cur], probe_dir, seeds, self.train)
        base = _rows_for(probe_dir, cur)
        if len(base) < len(seeds) * len(self.train) // 2:
            # z.B. Session-Limit: ohne gültige Baseline ist die Iteration ungültig, nicht "keine Verbesserung"
            raise BackendFailure(f"Iteration {it}: nur {len(base)} gültige Baseline-Runs")

        # Propose
        worst = sorted(base.values(), key=lambda r: (float(r[self.primary]), -float(r.get("false_done", 0))))[:2]
        traces = "\n\n".join(f"### Run {r['domain']} seed {r['seed']} ({self.primary}={r[self.primary]})\n"
                             + digest(probe_dir / r["run_dir"]) for r in worst)
        lib = "\n".join(f"- [{e['iteration']}] {e['summary']}" for e in self.state["library"][-10:]) or "(empty)"
        rejected = "\n".join(f"- [{h['iteration']}] {h['kind']}: {json.dumps(h['diff'], ensure_ascii=False)[:300]} → "
                             f"Δ={h['gate']['mean_diff']:+.3f}, p={h['gate']['p']:.3f}"
                             for h in self.state["history"] if not h["accepted"])[-3000:] or "(none)"
        summary = {m: round(_mean(base, m), 3) for m in (self.primary, "false_done_rate", "phantoms_diagnosed",
                                                          "built_on_phantom", "messages", "escalations", "output_tokens")}
        prompt = f"""## Current organisation config
```json
{json.dumps(cur.to_dict(), ensure_ascii=False, indent=2)}
```

## Measured on {len(base)} runs (training work domains: {', '.join(self.train)})
Primary metric: {self.primary} (share of work items that truly work at the end; 1.0 is perfect).
```json
{json.dumps(summary, indent=2)}
```

## Traces of the two weakest runs (ground truth annotations come from the evaluator; agents never see them)
{traces}

## Library of accepted changes so far
{lib}

## Rejected proposals (do not repeat without material change)
{rejected}

## Task
1. Diagnose in 3–6 sentences what goes wrong organisationally (not technically).
2. Propose exactly two candidate configs:
   - "invariant": targets a general organisational weakness likely to recur in any kind of work.
   - "specific": targets what is specific to this kind of assignment.
Return only this JSON in a ```json block:
{{"diagnosis": "...", "candidates": [{{"kind": "invariant", "rationale": "...", "config": {{...full config...}}}},
{{"kind": "specific", "rationale": "...", "config": {{...full config...}}}}]}}"""
        cands: list[tuple[str, str, OrgConfig]] = []
        text = await self._ask(prompt, idir / "propose")
        for attempt in range(2):
            try:
                data = extract_json(text)
                for c in data["candidates"][:2]:
                    cands.append((c["kind"], c.get("rationale", ""), self._parse_cfg(c["config"], cur, f"i{it}{c['kind'][0]}")))
                (idir / "diagnosis.md").write_text(data.get("diagnosis", ""), encoding="utf-8")
                break
            except Exception as e:
                cands = []
                if attempt == 1:
                    self._log(f"Iteration {it}: Editor-Ausgabe unbrauchbar ({e}); Iteration ohne Kandidaten")
                    break
                text = await self._ask(prompt + f"\n\nYour previous answer could not be used: {e}. Return valid JSON only.",
                                       idir / "propose-retry")
        cands = [c for c in cands if c[2].hash() != cur.hash()]
        n_needed = len(seeds) * len(self.train) // 2
        for kind, _, cfg in cands:
            (idir / f"candidate-{kind}.yaml").write_text(cfg.to_yaml(), encoding="utf-8")

        # Probe + Gate
        results = []
        if cands:
            await self._probe([c[2] for c in cands], probe_dir, seeds, self.train)
        for kind, rationale, cfg in cands:
            if len(_rows_for(probe_dir, cfg)) < n_needed:
                raise BackendFailure(f"Iteration {it}: zu wenige gültige Probe-Runs für {kind}")
            gate = await self._adaptive_gate(it, cur, cfg, kind, probe_dir)
            results.append((kind, rationale, cfg, gate))
            self._log(f"  {kind}: Δ={gate['mean_diff']:+.3f} p={gate['p']:.3f} n={gate['n_pairs']} "
                      f"tokens×{gate['token_ratio'] or 0:.2f} → {'BESTANDEN' if gate['passed'] else 'verworfen'}")
        passing = [r for r in results if r[3]["passed"]]

        # Compose
        if len(passing) >= 2:
            cprompt = f"""Two candidate changes both improved the organisation significantly.
Current config:
```json
{json.dumps(cur.to_dict(), ensure_ascii=False, indent=2)}
```
""" + "\n".join(f"""Candidate {k} (Δ{self.primary}={g['mean_diff']:+.3f}), rationale: {r}
```json
{json.dumps(c.to_dict(), ensure_ascii=False, indent=2)}
```""" for k, r, c, g in passing) + """
Compose ONE config that keeps the supported changes of both, resolving conflicts, without adding anything new.
Return only {"rationale": "...", "config": {...}} in a ```json block."""
            try:
                data = extract_json(await self._ask(cprompt, idir / "compose"))
                comp = self._parse_cfg(data["config"], cur, f"i{it}c")
                if comp.hash() not in {p[2].hash() for p in passing}:
                    (idir / "candidate-composed.yaml").write_text(comp.to_yaml(), encoding="utf-8")
                    await self._probe([comp], probe_dir, seeds, self.train)
                    gate = await self._adaptive_gate(it, cur, comp, "composed", probe_dir)
                    results.append(("composed", data.get("rationale", ""), comp, gate))
                    self._log(f"  composed: Δ={gate['mean_diff']:+.3f} p={gate['p']:.3f} → "
                              f"{'BESTANDEN' if gate['passed'] else 'verworfen'}")
                    if gate["passed"]:
                        passing.append(results[-1])
            except (BackendFailure, KeyboardInterrupt):
                raise
            except Exception as e:
                self._log(f"  Compose fehlgeschlagen: {e}")

        # Entscheidung
        winner = max(passing, key=lambda r: r[3]["mean_diff"]) if passing else None
        for kind, rationale, cfg, gate in results:
            self.state["history"].append({"iteration": it, "kind": kind, "rationale": rationale, "config_hash": cfg.hash(),
                                          "diff": _cfg_diff(cur.to_dict(), cfg.to_dict()), "gate": gate,
                                          "accepted": winner is not None and cfg.hash() == winner[2].hash()})
        if winner:
            kind, rationale, cfg, gate = winner
            entry_dir = self.dir / "library" / f"{it:03d}-{cfg.hash()}"
            entry_dir.mkdir(parents=True, exist_ok=True)
            (entry_dir / "config.yaml").write_text(cfg.to_yaml(), encoding="utf-8")
            rprompt = f"""This change was ACCEPTED after measurement.
Change (diff vs previous config): {json.dumps(_cfg_diff(cur.to_dict(), cfg.to_dict()), ensure_ascii=False)}
Rationale: {rationale}
Evidence: {json.dumps(gate)}
Write a short EXPERIENCE entry in Markdown with sections: Situation, Change, Evidence, Lesson (when and why it works), \
Open questions. Then on the last line write 'SUMMARY: <one sentence>'."""
            exp_text = await self._ask(rprompt, idir / "reflect")
            summary_line = next((ln[8:].strip() for ln in reversed(exp_text.splitlines()) if ln.startswith("SUMMARY:")),
                                rationale[:200])
            (entry_dir / "EXPERIENCE.md").write_text(
                exp_text + f"\n\n---\n*Automatisch:* Iteration {it}, Kandidat {kind}, gepaarte Runs {gate['n_pairs']}, "
                f"Δ{self.primary} {gate['mean_diff']:+.3f}, p={gate['p']:.4f}, Tokenfaktor {gate['token_ratio']}\n",
                encoding="utf-8")
            self.state["library"].append({"iteration": it, "config_hash": cfg.hash(), "kind": kind, "summary": summary_line,
                                          "gate": gate})
            self.state["current"] = cfg.to_dict()
            self.state["no_improve"] = 0
            self._log(f"Iteration {it}: übernommen {kind} → {cfg.name} ({cfg.hash()})")
        else:
            self.state["no_improve"] += 1
            self._log(f"Iteration {it}: keine Verbesserung (Serie {self.state['no_improve']})")
        self.state["iteration"] = it
        self._save()
        if it % self.holdout_every == 0:
            await self.holdout_check()

    async def holdout_check(self) -> None:
        """Transfer-Test: Start- vs. aktuelle Config auf Domänen, die der Editor nie gesehen hat."""
        if not self.holdout:
            return
        it = self.state["iteration"]
        start, cur = OrgConfig.from_dict(self.state["start"]), OrgConfig.from_dict(self.state["current"])
        if start.hash() == cur.hash():
            return
        hdir = self.dir / "holdout"
        seeds = list(range(900_000, 900_000 + self.holdout_seeds))   # feste Holdout-Seeds, nie im Training
        await self._probe([start, cur], hdir, seeds, self.holdout)
        gate = self._gate(_rows_for(hdir, start), _rows_for(hdir, cur))
        self.state["holdout"].append({"iteration": it, "config_hash": cur.hash(), **gate})
        self._save()
        self._log(f"Holdout nach Iteration {it}: Start {gate['base_mean']:.3f} → aktuell {gate['cand_mean']:.3f} "
                  f"(Δ={gate['mean_diff']:+.3f}, p={gate['p']:.3f})")

    async def run(self, iterations: int, hours: float, patience: int) -> None:
        deadline = time.time() + hours * 3600
        while (self.state["iteration"] < iterations and time.time() < deadline
               and self.state["no_improve"] < patience):
            try:
                await self.iteration()
            except BackendFailure as e:
                self._log(f"Backend-Ausfall außerhalb der Runs ({e}); 15 min Pause")
                await asyncio.sleep(900)
        await self.holdout_check()
        self.write_report()

    def write_report(self) -> None:
        s = self.state
        lines = [f"# Optimierungslauf {self.dir.name}", "",
                 f"Gestartet {s['started']}, Iterationen {s['iteration']}, übernommene Änderungen {len(s['library'])}.",
                 f"Einstellungen: `{json.dumps(s['settings'], ensure_ascii=False)}`", "", "## Verlauf", "",
                 "| Iter | Kandidat | Δ | p | Tokens× | übernommen |", "|---|---|---|---|---|---|"]
        for h in s["history"]:
            g = h["gate"]
            lines.append(f"| {h['iteration']} | {h['kind']} | {g['mean_diff']:+.3f} | {g['p']:.3f} | "
                         f"{(g['token_ratio'] or 0):.2f} | {'✓' if h['accepted'] else ''} |")
        lines += ["", "## Bibliothek", ""] + [f"- Iteration {e['iteration']} ({e['kind']}): {e['summary']}" for e in s["library"]]
        lines += ["", "## Transfer (Holdout)", ""] + [
            f"- nach Iteration {h['iteration']}: {h['base_mean']:.3f} → {h['cand_mean']:.3f} (Δ={h['mean_diff']:+.3f}, p={h['p']:.3f})"
            for h in s["holdout"]]
        lines += ["", "## Aktuelle Config", "", "```yaml", OrgConfig.from_dict(s["current"]).to_yaml(), "```"]
        (self.dir / "bericht.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    import sys
    sys.stdout.reconfigure(encoding="utf-8")
    from .keepawake import hold
    hold()
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--experiment", required=True)
    p.add_argument("--start", required=True, help="Start-Config (YAML)")
    p.add_argument("--scenario", default="phantom_done")
    p.add_argument("--train-domains", nargs="+", default=["coding", "business"])
    p.add_argument("--holdout-domains", nargs="+", default=["research"])
    p.add_argument("--seeds-per-probe", type=int, default=6)
    p.add_argument("--iterations", type=int, default=50)
    p.add_argument("--hours", type=float, default=48)
    p.add_argument("--patience", type=int, default=6)
    p.add_argument("--concurrency", type=int, default=2)
    p.add_argument("--backend", default="agent_sdk")
    p.add_argument("--model", default="claude-sonnet-5-5")
    p.add_argument("--effort", default="medium")
    p.add_argument("--editor-model", default="claude-opus-5-5")
    p.add_argument("--holdout-every", type=int, default=3)
    p.add_argument("--holdout-seeds", type=int, default=10)
    p.add_argument("--alpha", type=float, default=0.1)
    p.add_argument("--max-seeds-per-probe", type=int, default=None, help="adaptives Nachmessen bis zu so vielen Seeds je Domäne")
    p.add_argument("--extend-p", type=float, default=0.5)
    a = p.parse_args()
    backend = ({"kind": "scripted", "policy": a.backend.split(":")[1]} if a.backend.startswith("scripted")
               else {"kind": "agent_sdk", "model": a.model, "effort": a.effort})
    opt = Optimizer(a.experiment, OrgConfig.load(a.start), a.scenario, a.train_domains, a.holdout_domains,
                    a.seeds_per_probe, backend, a.concurrency, editor_model=a.editor_model, alpha=a.alpha,
                    holdout_every=a.holdout_every, holdout_seeds=a.holdout_seeds,
                    max_seeds_per_probe=a.max_seeds_per_probe, extend_p=a.extend_p)
    asyncio.run(opt.run(a.iterations, a.hours, a.patience))


if __name__ == "__main__":
    main()
