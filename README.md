# orglab: when is a "verified" justified?

Preregistered experiments on how LLM agents check each other's work. **Lead researcher: Neo Erbler** (Stonewave Tech LLC). Code and analyses were written with Claude (Anthropic) as research assistant; every commit says so.

> Lab notes, hypotheses and preregistrations are in German (`laborbuch.md`, `hypothesen.md`, `experimente/`). This README is the English entry point. German version: [README.de.md](README.de.md).

## The question

We build multi-agent systems at Stonewave, and they fail in a specific way: an agent reports "done", another agent or a human accepts it, and nobody notices that the evidence never showed the work succeeded. The project's guiding question (decision D-023):

**What makes a "verified" justified, and how must information be organised so that it is?**

## Findings so far

Every claim carries its status. *Confirmed* means: predicted in advance, preregistered, replicated on fresh material, analysed blind and recomputed independently by a model from another family. Each result holds **for its setup** (models, prompts, constructed evidence); see the linked result files for limits.

| Finding | Status | Where |
|---|---|---|
| **Happy trust.** Shown evidence that cannot establish success (a "queued", "exit 0" or "pm2 online" line), Claude Sonnet 5.5 as verifier still confirms success in 27.7 % of cases [95 % CI 21.5–34.0]; Claude Haiku 5.5 in 5.2 %. | confirmed (E-026) | [E-026](experimente/E-026-bestaetigung-vertrauen/ergebnis.md), discovery [E-025](experimente/E-025-glueckliches-vertrauen/ergebnis.md) |
| Allowing a third answer "not established", or adding an evidence norm to the instruction, each brings Sonnet's unsupported confirmations to about zero (−14 percentage points each). | confirmed (E-026) | same |
| The price: with full evidence, the third answer costs Haiku 23 percentage points of correct verdicts. | confirmed (E-026) | same |
| Which verifier fails depends on the failure mode, not on model strength: without the yardstick in the prompt the weaker model (Haiku) misses more; without decisive evidence the stronger one (Sonnet) confirms more. | confirmed, in separate setups (E-024, E-026) | [E-024](experimente/E-024-bestaetigung-massstab/), E-026 |
| Haiku misses far more faults when the yardstick (target values) is missing from the prompt (+26 points); data tools crowd out looking it up. Sonnet shows neither. | confirmed for Haiku 5.5 (E-024) | E-024 |
| Teams of agents without a human arbiter lose badly against a blocker; a simple quorum vote replaces the arbiter, with no wrong decisions observed. | confirmed (E-014) | [E-014](experimente/E-014-governance-bestaetigung/) |
| An evidence-based rule (an environment receipt instead of a vote) is immune to lying votes. | confirmed (E-018) | [E-018](experimente/E-018-beleg-statt-stimme/) |
| Several plausible ideas did **not** hold: a visible self-report ("Done. All checks green.") did not make verifiers sloppier; strict ownership of checks did not reduce robustness on confirmation. | not supported / refuted | `hypothesen.md` (H-017, H-034, H-035) |

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
