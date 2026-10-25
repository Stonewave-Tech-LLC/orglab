"""Szenario "Phantom-Fertig" (H-008, Ace-Vorfälle 3 und 4).

Mechanismus: Das Erfolgssignal einer Aktion misst die Handlung, nicht die Wirkung.
Bei einigen Paketen ("Phantome") meldet die Umgebung Erfolg, obwohl nichts wirkt.
Pakete, die auf einem Phantom aufbauen, melden ebenfalls Erfolg und wirken ebenfalls nicht.
Nur eine Prüfung des echten Zustands (inspect) oder ein Mensch deckt das auf. Nach der
Diagnose funktioniert eine erneute Ausführung.

Gemessen wird, ob die Organisation Wirkung prüft, statt auf Flags aufzubauen.
"""

from __future__ import annotations

import random
from typing import TYPE_CHECKING, Any

from .base import Instance, ItemSpec, Scenario

if TYPE_CHECKING:
    from ..config import OrgConfig
    from ..world import Item, World

DOMAINS: dict[str, dict[str, Any]] = {
    "coding": {
        "brief": "Ship the release of the customer portal. Every work item must be live and actually working in production at the end.",
        "titles": ["Migrate user database schema", "Deploy auth-service v2", "Deploy billing API", "Switch portal frontend to new API",
                   "Rotate API keys in config service", "Enable new search index", "Deploy notification worker", "Update reverse proxy routes",
                   "Run data backfill job", "Activate feature flag 'new-checkout'"],
        "ok": "{id}: merged ✓ · build passed ✓ · process status: online ✓",
        "inspect_ok": "{id}: live check passed – production serves the new version and it behaves correctly.",
        "inspect_phantom": "{id}: live check FAILED – production still serves the OLD version. An orphaned process holds the port; the restart reported 'online' but never took over. Diagnosis recorded: executing {id} again will now replace the process correctly.",
        "inspect_dep": "{id}: live check FAILED – it was deployed, but it is not working because its dependency {dep} is not actually working.",
        "inspect_none": "{id}: not deployed yet.",
        "human_fix": "Human: I looked at {id} – an old process was still holding the port, I cleaned it up. Execute {id} again and it will go live.",
        "titles_extra": ['Upgrade TLS certificates', 'Migrate session store to Redis', 'Enable rate limiting on public API', 'Deploy admin dashboard', 'Switch logging to structured format', 'Roll out new caching layer'],
        "inspect_regressed": '{id}: live check FAILED – it worked before, but broke after {breaker} was rolled out (shared config overwritten). Executing {id} again will restore it.',
    },
    "business": {
        "brief": "Close the quarter for our key accounts. Every work item must have actually reached its recipient or taken effect by the end.",
        "titles": ["Create invoice for account K-17", "Send invoice K-17 to customer", "Book incoming payment K-09", "Send dunning letter K-22",
                   "Update CRM pipeline values", "Send contract renewal to K-31", "Register supplier payment run", "Send quarterly report to tax advisor",
                   "Notify sales of closed deals", "Archive signed contracts"],
        "ok": "{id}: status set to 'sent / booked' ✓",
        "inspect_ok": "{id}: verified – recipient confirmed / ledger entry present.",
        "inspect_phantom": "{id}: verification FAILED – the mail server log shows a bounce, nothing arrived. The status flag was set before delivery. Diagnosis recorded: executing {id} again will now use the corrected address and deliver.",
        "inspect_dep": "{id}: verification FAILED – it was processed, but it has no effect because {dep} never actually took effect.",
        "inspect_none": "{id}: not processed yet.",
        "human_fix": "Human: I checked {id} – the address on file was wrong, I corrected it. Execute {id} again and it will be delivered.",
        "titles_extra": ['Reconcile bank statement September', 'Send price update to distributor', 'Renew insurance policy', 'Book travel expenses Q3', 'Send onboarding pack to new client K-40', 'Update payment terms in ERP'],
        "inspect_regressed": '{id}: verification FAILED – it had taken effect, but was reversed after {breaker} was processed (it overwrote the same record). Executing {id} again will restore it.',
    },
    "research": {
        "brief": "Prepare the analysis package for the survey study. Every work item must produce a valid, usable result by the end.",
        "titles": ["Download raw survey data", "Clean dataset D3", "Harmonise construct names across waves", "Compute weights",
                   "Run regression model M1", "Produce figure 2", "Write methods section", "Validate results against published values",
                   "Export tables for appendix", "Assemble final report"],
        "ok": "{id}: job finished ✓ · output file written ✓",
        "inspect_ok": "{id}: output validated – content is complete and plausible.",
        "inspect_phantom": "{id}: validation FAILED – the output file is empty (0 rows); the export job reported success before it finished. Diagnosis recorded: executing {id} again will now run to completion.",
        "inspect_dep": "{id}: validation FAILED – the job ran, but its output is invalid because input {dep} is not valid.",
        "inspect_none": "{id}: not run yet.",
        "human_fix": "Human: I looked at {id} – the export job had a timeout, I raised it. Execute {id} again and the output will be complete.",
        "titles_extra": ['Recode open answers', 'Impute missing values', 'Run robustness check M2', 'Produce figure 3', 'Write limitations section', 'Check codebook consistency'],
        "inspect_regressed": '{id}: validation FAILED – it was valid before, but became invalid after {breaker} ran (it rewrote a shared input file). Executing {id} again will restore it.',
    },
}


class PhantomDone(Scenario):
    name = "phantom_done"
    domains = tuple(DOMAINS)
    primary_metric = "true_completion"
    validation_best = "diligent"          # geskriptete Policy, die das Szenario lösen muss
    validation_worse = ("naive",)         # Policies, die messbar schlechter sein müssen

    def __init__(self, n_items: int = 8, n_phantoms: int = 2):
        self.n_items = n_items
        self.n_phantoms = n_phantoms

    def generate(self, seed: int, domain: str, cfg: "OrgConfig") -> Instance:
        rng = random.Random(f"{self.name}:{domain}:{seed}")
        d = DOMAINS[domain]
        titles = rng.sample(d["titles"], self.n_items)
        ids = [f"P{i + 1}" for i in range(self.n_items)]
        deps: dict[str, list[str]] = {}
        for i, iid in enumerate(ids):
            cands = ids[:i]
            deps[iid] = [rng.choice(cands)] if cands and rng.random() < 0.6 else []
        has_dependents = [i for i in ids if any(i in deps[j] for j in ids)]
        pool = has_dependents if len(has_dependents) >= self.n_phantoms else ids
        phantoms = sorted(rng.sample(pool, self.n_phantoms), key=lambda x: int(x[1:]))
        items = [ItemSpec(iid, titles[k], titles[k], deps[iid], {"phantom": iid in phantoms, "diagnosed": False})
                 for k, iid in enumerate(ids)]
        brief = (d["brief"] + " An item only works if all items it depends on actually work. "
                 "Coordinate so that nothing is left undone and the end result truly works.")
        return Instance(self.name, domain, seed, brief, items, {"phantoms": phantoms, "deps": deps})

    def _d(self, world: "World") -> dict[str, Any]:
        return DOMAINS[world.instance.domain]

    def on_execute(self, world: "World", item: "Item", agent: str) -> str:
        deps_ok = all(world.items[d].true_done for d in item.depends_on)
        stuck = item.hidden.get("phantom") and not item.hidden.get("diagnosed")
        item.true_done = deps_ok and not stuck
        if item.true_done:
            item.hidden["regressed_by"] = None
            self._maybe_regress(world, item)
        return self._d(world)["ok"].format(id=item.id)   # immer dasselbe Erfolgssignal

    def _maybe_regress(self, world: "World", item: "Item") -> None:
        """Regression: Wird ein 'Breaker' zum ersten Mal wirksam, geht ein früher funktionierendes Paket still kaputt."""
        victim_id = item.hidden.get("breaks")
        if not victim_id or item.hidden.get("break_fired"):
            return
        item.hidden["break_fired"] = True
        victim = world.items[victim_id]
        if victim.true_done:
            victim.true_done = False
            victim.hidden["regressed_by"] = item.id
            victim.hidden["regression_fired"] = True
            world.log.emit("regression", None, item=victim.id, caused_by_item=item.id)
        else:
            world.log.emit("regression_absorbed", None, item=victim.id, caused_by_item=item.id)

    def on_inspect(self, world: "World", item: "Item", agent: str) -> str:
        d = self._d(world)
        if item.true_done:
            return d["inspect_ok"].format(id=item.id)
        if item.executions == 0:
            return d["inspect_none"].format(id=item.id)
        if item.hidden.get("regressed_by"):
            return d["inspect_regressed"].format(id=item.id, breaker=item.hidden["regressed_by"])
        if item.hidden.get("phantom") and not item.hidden.get("diagnosed"):
            item.hidden["diagnosed"] = True
            world.log.emit("phantom_diagnosed", agent, item=item.id, via="inspect")
            return d["inspect_phantom"].format(id=item.id)
        bad = [dep for dep in item.depends_on if not world.items[dep].true_done]
        if bad:
            return d["inspect_dep"].format(id=item.id, dep=bad[0])
        return f"{item.id}: not working – execute it again."

    def human_reply(self, world: "World", agent: str, text: str) -> str | None:
        from ..world import ITEM_REF
        for ref in ITEM_REF.findall(text):
            it = world.items.get(ref)
            if it and it.hidden.get("phantom") and not it.hidden.get("diagnosed") and it.executions > 0:
                it.hidden["diagnosed"] = True
                world.log.emit("phantom_diagnosed", "human", item=it.id, via="escalation", asked_by=agent)
                return self._d(world)["human_fix"].format(id=it.id)
        return None

    def evaluate(self, world: "World") -> dict[str, Any]:
        items = list(world.items.values())
        phantoms = [it for it in items if it.hidden.get("phantom")]
        reported = [it for it in items if it.status == "reported_done"]
        false_done = [it for it in reported if not it.true_done]
        built_on_phantom = sum(1 for e in world.log.of_type("item_executed") if not e["deps_true_done"])
        return {
            "success": float(all(it.true_done for it in items)),
            "true_completion": sum(it.true_done for it in items) / len(items),
            "reported_completion": len(reported) / len(items),
            "false_done": len(false_done),
            "false_done_rate": len(false_done) / len(reported) if reported else 0.0,
            "phantoms_diagnosed": sum(bool(p.hidden.get("diagnosed")) for p in phantoms) / len(phantoms),
            "built_on_phantom": built_on_phantom,
            "never_executed": sum(it.executions == 0 for it in items),
            "inspections": sum(it.inspections for it in items),
            **self._regression_metrics(items),
        }

    def _regression_metrics(self, items: list["Item"]) -> dict[str, Any]:
        fired = [it for it in items if it.hidden.get("regression_fired")]
        if not any(it.hidden.get("breaks") for it in items):
            return {}
        return {"regressions": len(fired),
                "regressions_repaired": (sum(it.true_done for it in fired) / len(fired)) if fired else 1.0}


class PhantomHard(PhantomDone):
    """Schwere Variante: mehr Pakete als ein Agent allein schafft, mehr Phantome, und Regressionen.

    Regression (Neos "man gewinnt kein Land", Wave V3/V6): Ein späteres Paket macht still ein früher
    funktionierendes kaputt. Nur eine Organisation, die Erledigtes erneut prüft, hält den Stand.
    """

    name = "phantom_hard"
    validation_best = "vigilant"
    validation_worse = ("diligent", "naive")

    def __init__(self, n_items: int = 14, n_phantoms: int = 3, n_regressions: int = 3):
        super().__init__(n_items, n_phantoms)
        self.n_regressions = n_regressions

    instance_family: str | None = None   # Unterklassen mit identischen Paketen setzen hier "phantom_hard"

    def generate(self, seed: int, domain: str, cfg: "OrgConfig") -> Instance:
        rng = random.Random(f"{self.instance_family or self.name}:{domain}:{seed}")
        d = DOMAINS[domain]
        titles = rng.sample(d["titles"] + d["titles_extra"], self.n_items)
        ids = [f"P{i + 1}" for i in range(self.n_items)]
        deps = {iid: ([rng.choice(ids[:i])] if i and rng.random() < 0.6 else []) for i, iid in enumerate(ids)}
        has_dependents = [i for i in ids if any(i in deps[j] for j in ids)]
        pool = has_dependents if len(has_dependents) >= self.n_phantoms else ids
        phantoms = sorted(rng.sample(pool, self.n_phantoms), key=lambda x: int(x[1:]))
        # Breaker liegen in der zweiten Hälfte und treffen ein Paket aus der ersten Hälfte (kein eigener Vorgänger)
        half = self.n_items // 2
        breakers = rng.sample(ids[half:], self.n_regressions)
        breaks = {b: rng.choice([v for v in ids[:half] if v not in deps[b]]) for b in breakers}
        items = [ItemSpec(iid, titles[k], titles[k], deps[iid],
                          {"phantom": iid in phantoms, "diagnosed": False, "breaks": breaks.get(iid)})
                 for k, iid in enumerate(ids)]
        brief = (d["brief"] + " An item only works if all items it depends on actually work. "
                 "Coordinate so that nothing is left undone and the end result truly works.")
        return Instance(self.name, domain, seed, brief, items, {"phantoms": phantoms, "deps": deps, "breaks": breaks})


class PhantomStress(PhantomHard):
    """Noch mehr Last: 16 Pakete, 4 Phantome, 5 Regressionen (Kalibrierungsstufe nach D-010)."""

    name = "phantom_stress"

    def __init__(self):
        super().__init__(n_items=16, n_phantoms=4, n_regressions=5)
