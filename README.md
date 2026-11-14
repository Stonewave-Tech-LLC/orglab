# orglab: when is a "verified" justified?

Preregistered experiments on how LLM agents check each other's work. **Lead researcher: Neo Erbler** (Stonewave Tech LLC). Code and analyses were written with Claude (Anthropic) as research assistant; every commit says so.

> Lab notes, hypotheses and preregistrations are in German (`laborbuch.md`, `hypothesen.md`, `experimente/`). This README is the English entry point. German version: [README.de.md](README.de.md).

## The question

We build multi-agent systems at Stonewave, and they fail in a specific way: an agent reports "done", another agent or a human accepts it, and nobody notices that the evidence never showed the work succeeded. The project's guiding question (decision D-023):

**What makes a "verified" justified, and how must information be organised so that it is?**

## Findings so far

Every claim carries its status, in three levels:

- **confirmed (full protocol):** predicted in advance, preregistered, replicated on fresh material, analysed blind, and recomputed independently by at least one model from another family (E-024: two, E-026: one).
- **replicated (earlier protocol):** preregistered and replicated on fresh seeds, but before the research harness existed: no independent recomputation by another model family (E-014).
- **exploratory:** the effect replicated on fresh seeds, but the preregistration cannot be shown to predate the first run from the commit history (E-018).

Each result holds **for its setup** (models, prompts, constructed evidence); see the linked result files for limits. *n* is the number of evidence items (E-024, E-026) or runs (E-014, E-018) per condition and model.

| Finding | Status | Where |
|---|---|---|
| **Happy trust.** Shown evidence that cannot establish success (a "queued", "exit 0" or "pm2 online" line), Claude Sonnet 5.5 as verifier still confirms success in **27.7 %** of cases [95 % CI 21.5–34.0]; Claude Haiku 5.5 in 5.2 % [2.6–8.4]. n = 191. | confirmed (E-026) | [E-026](experimente/E-026-bestaetigung-vertrauen/ergebnis.md), discovery [E-025](experimente/E-025-glueckliches-vertrauen/ergebnis.md) |
| Two remedies, each on its own, bring Sonnet's unsupported confirmations to about zero: an evidence norm in the instruction (27.7 % → 0.5 %, 1 of 191) and allowing a third answer "not established" (27.7 % → 0 of 191). The preregistered tests are main effects averaged over the other factor in a 2×2 design, which halves their size: −13.6 points [−16.8; −10.5] and −14.1 points [−17.5; −11.0]. | confirmed (E-026) | same |
| The price: with full evidence, the third answer lowers Haiku's correct verdicts from 94.2 % to 71.2 % (−23.0 points [−29.3; −16.8]); Sonnet loses 4.2 points. n = 191. | confirmed (E-026) | same |
| Which verifier fails depends on the failure mode, not on model strength: without the yardstick in the prompt the weaker model (Haiku) misses more; without decisive evidence the stronger one (Sonnet) confirms more. | confirmed, in separate setups (E-024, E-026) | [E-024](experimente/E-024-bestaetigung-massstab/ergebnis.md), E-026 |
| Haiku misses far more faults when the yardstick (target values) is missing from the prompt: +26.3 points [20.7–32.2], n = 76 spec-only items; Sonnet does not (difference Haiku − Sonnet +26.0 points). | confirmed for Haiku 5.5 (E-024) | E-024 |
| Teams of agents without a human arbiter lose badly against a blocker (−30.7 points of true completion). A simple quorum vote restores it, with **0 wrong decisions in 20 runs**; the simulated human arbiter made 1.3 per run. That arbiter was deliberately naive, so the robust part is "the vote makes no wrong decisions", not "a vote beats a human". n = 20 runs per arm. | replicated, earlier protocol (E-014) | [E-014](experimente/E-014-governance-bestaetigung/ergebnis.md) |
| An evidence-based rule (an environment receipt instead of a vote) withstands lying votes: honest agents lost 0.05 packages per run instead of 11.4 under the vote (all 20 pairs in the same direction). | exploratory (E-018) | [E-018](experimente/E-018-beleg-statt-stimme/ergebnis.md) |
| Several plausible ideas did **not** hold. **H-034:** a visible self-report ("Done. All checks green.") did not make verifiers sloppier; Haiku became more suspicious, not less (false alarms +4.2 points). **H-035:** verifiers with tools did not query less evidence under a self-report (Sonnet queried all 3 channels in every cell, little room to move). **H-017:** strict ownership of checks did not reduce robustness on confirmation (−3.3 points, CI includes zero). | not supported / refuted | `hypothesen.md` (H-017, H-034, H-035) |

**On preregistration timestamps.** For each experiment the preregistration commit precedes the first data commit in the lab book history (E-026 by 1 h, E-025 by 16 h, E-014 by 12 s before the first run started; E-024 was drafted at 18:59, amended after the material check and frozen before the pilot and main run); for E-018 it does not, hence "exploratory". Commit dates are self-reported and were not witnessed by a third party before the repository was created on GitHub (22 Oct 2026, 19:17 UTC).

**First test on real data: stopped.** E-027 was to test happy trust on 316 real records from our own agent system. It stopped at its material gate before any verifier ran. On 7 of the 20 cases Neo had labelled blind, GPT and Neo disagreed about what counts as evidence: is an agent's detailed completion report evidence, or only a claim? That disagreement is itself an observation (status: hint), and a second attempt with a sharper definition is planned. [E-027 result](experimente/E-027-wave-rueckschau/ergebnis.md). The internal records are not in this repository.

## How we work

The rules are in [CLAUDE.md](CLAUDE.md) (German). Each one exists because of a mistake we actually made; the origin is written next to it. In short:

- **Two stages.** Discovery runs only produce candidates. A candidate becomes a finding only if it replicates in a preregistered run on fresh seeds.
- **Preregister and freeze.** Hypothesis, directed prediction, design, analysis script (tested on synthetic data) and exact prompts are committed before the main run.
- **Manipulation checks.** Each factor is checked for doing what its name says. Once, "reasoning off" turned out to be adaptive reasoning; the interpretation was backwards for two experiments.
- **Independent ground truth.** A model from another family, or Neo, checks the material blind before the main run.
- **Double bookkeeping.** After the run, a model from another family rewrites the primary analysis from the preregistration text and three data lines alone; the numbers must match.
- **Blind analysis.** Arms are renamed before analysis and unblinded only after the analysis is fixed and anchored by a git tag.
- **External critique** from another model family before every larger run.
- **No claim stronger than its status** (confirmed, supported, exploratory, hint), also in summaries and posts.

Since E-025, experiments run through the [research-harness](https://github.com/Stonewave-Tech-LLC/research-harness), which enforces these rules with code gates instead of good intentions.

## Repository layout

| Path | Content |
|---|---|
| `laborbuch.md` | Lab book, append-only chronicle |
| `hypothesen.md`, `entscheidungen.md`, `quellen.md` | Registers: hypotheses (H-xxx) with status and evidence, decisions (D-xxx), sources |
| `experimente/E-xxx-*/` | One folder per experiment: `prereg.md`, `dryrun.md` (exact prompts), `ergebnis.md`, transcripts |
| `daten/E-xxx-*/` | Raw data, never modified (large event logs and internal exports stay local) |
| `orglab/` | Testbed and experiment code (Python) |
| `configs/`, `tests/` | Organisation configs, tests |
| `notizen/` | Working notes |

**What is not public:** our correspondence with the agents of our production system and notes about that system (incidents, analyses of its raw data, infrastructure) stay in the private working repository, and internal exports were never committed. A few links in the lab book therefore point to files that are not in this copy. Internal IDs are replaced by `[ID intern]`. The rules for the public copy (what is left out, what is redacted, what blocks a release) live in the private repository.

## Running

Python 3.13, a virtual environment, and an OpenRouter key in `.env` (`OPENROUTER_API_KEY`) for the model calls.

```
py -3.13 -m venv .venv
.venv\Scripts\python -m pip install -e .
.venv\Scripts\python -m pytest -q
.venv\Scripts\python -m orglab.e026 dryrun        # exact prompts of an experiment
.venv\Scripts\python -m orglab.e026 power         # power simulation on synthetic data
```

Model IDs, settings and omitted parameters are listed in each preregistration.

## License and citation

Code: MIT ([LICENSE](LICENSE)). Texts and data: CC BY 4.0 ([LICENSE-docs.md](LICENSE-docs.md)). Citation: [CITATION.cff](CITATION.cff).
