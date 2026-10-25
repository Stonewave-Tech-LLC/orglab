# Quellen

Stand: 23.10.2026.

**Typen:** Peer-Review (PR), Preprint (PP), Leaderboard (LB), Hersteller (HS), Blog/Bericht/Forum (BL), Video, Repo (RP).

**Prüfstatus:**
- „im Original gelesen“: Volltext oder die relevanten Abschnitte selbst gelesen (HTML/Text, lokal in `quellen/papers/` abgelegt, sofern heruntergeladen)
- „nur Abstract/Zusammenfassung“
- „nur Sekundärquelle“: nur über Zitat oder Suchzusammenfassung bekannt
- „Fachwissen“: aus Vorwissen, in dieser Recherche nicht erneut geprüft

## Morpheus-Benchmarks (Frage 1)

Alle Repos wurden geklont bzw. per GitHub-API gelesen, lokal unter `quellen/`.

| Kürzel | Quelle | URL | Typ | Prüfstatus |
|---|---|---|---|---|
| Q-M1 | hogwarts-blender-benchmark (README, SPEC, prompt, Ordnerliste, Commit-Historie) | https://github.com/TheMorpheus407/hogwarts-blender-benchmark | RP | im Original gelesen. Binärdateien (.blend, PNG) nicht geladen. |
| Q-M2 | morphcook (README, SPEC-Hashes, Ordner, opencode.jsonc, time.txt) | https://github.com/TheMorpheus407/morphcook | RP | im Original gelesen. Flacher Klon, also HEAD-Stand und nicht die One-Shot-Commits. |
| Q-M3 | morphcook-cli-benchmark (README, PROMPT, SPEC, Struktur) | https://github.com/TheMorpheus407/morphcook-cli-benchmark | RP | im Original gelesen |
| Q-M4 | morphdemo-benchmark (README, SPEC, ENVIRONMENT, prompt, Ordner) | https://github.com/TheMorpheus407/morphdemo-benchmark | RP | im Original gelesen |
| Q-M5 | morphhealth-benchmark (README, SPEC-Gliederung und Anfang, .gitignore) | https://github.com/TheMorpheus407/morphhealth-benchmark | RP | im Original gelesen. SPEC nur teilweise gelesen. |
| Q-M6 | morphrig-benchmark (README, SPEC §11–12, CSV mit 96 IDs, environment.json, Dateibaum, Releases) | https://github.com/TheMorpheus407/morphrig-benchmark | RP | im Original gelesen. Run-Inhalte nur als Dateiliste. |
| Q-M7 | morphcook Issues #1–#3 und Kommentare (Aussage des Autors zur Harness-Wahl) | https://github.com/TheMorpheus407/morphcook/issues/3 | RP/Forum | im Original gelesen |
| Q-M8 | YouTube-Videos von „The Morpheus“ mit möglichen Bewertungen | (nicht gefunden) | Video | nicht gefunden, nicht geprüft |

## Modell × Harness (Frage 2, teils 5)

| Kürzel | Quelle | URL | Typ | Prüfstatus |
|---|---|---|---|---|
| Q-TB | Merrill, Shaw, Carlini et al.: Terminal-Bench (2.0), arXiv 2601.11868 | https://arxiv.org/abs/2601.11868 | PP. Das Leaderboard tbench.ai ist LB. | im Original gelesen (relevante Abschnitte). Leaderboard selbst nicht geprüft. |
| Q-HAL | Kapoor et al.: Holistic Agent Leaderboard, arXiv 2510.11977, ICLR 2026 | https://arxiv.org/abs/2510.11977 | PR | im Original gelesen (erste Hälfte des Textes) |
| Q-HALT | HAL-Traces auf Hugging Face | https://huggingface.co/datasets/agent-evals/hal_traces | RP/Daten | Existenz geprüft, Inhalt nicht |
| Q-GUN | Gundlach, Brown, Lynch, Thompson: „Just a Wrapper? How Much Do Scaffolds Matter?“ (LessWrong, 26.6.2026) | https://www.lesswrong.com/posts/jXLi3dhSpSMd7B6z8/just-a-wrapper-how-much-do-scaffolds-matter-1 | BL | nur Zusammenfassung (über WebFetch) |
| Q-EXG | „General Agent Evaluation“ (Exgentic / Open General Agent Leaderboard), arXiv 2602.22953 | https://arxiv.org/abs/2602.22953 | PP | im Original gelesen (Ergebnisse, Anhang F.3) |
| Q-STOP | Zhang et al.: „Stop Comparing LLM Agents Without Disclosing the Harness“, arXiv 2605.23950 | https://arxiv.org/abs/2605.23950 | PP (Positionspapier) | im Original gelesen (über WebFetch-Extraktion, Tabelle 2/7) |
| Q-HB | Yao et al.: Harness-Bench, arXiv 2605.27922 (v2, 15.10.2026) | https://arxiv.org/abs/2605.27922 | PP | im Original gelesen (Abstract, Setup, Tabelle 9, Interaktionen) |
| Q-HOM | „Harness or Model? Isolating the Harness Effect in Agentic Coding with a Contamination-Controlled Private Suite“, arXiv 2609.11987 | https://arxiv.org/abs/2609.11987 | PP | im Original gelesen (Abstract, Design, Ergebnisse, Diskussion) |
| Q-SCA | Vats & Golev: „The Scaffold Effect in Coding Agents“, arXiv 2607.22585 | https://arxiv.org/abs/2607.22585 | PP | nur Abstract |
| Q-LEW | Lewis: „Same Model, Different Harness: Different Coding-Agent Results“, arXiv 2608.26218 | https://arxiv.org/abs/2608.26218 | PP | nur Abstract |
| Q-BD | Mehtiyev & Assunção: „Beyond Resolution Rates: Behavioral Drivers of Coding Agent Success and Failure“, arXiv 2604.02547 | https://arxiv.org/abs/2604.02547 | PP | im Original gelesen (RQ3, Grenzen) |
| Q-DMC | „The Double Measurement Confound in Agent Benchmarks“, arXiv 2609.09218 | https://arxiv.org/abs/2609.09218 | PP | Abstract und Einleitung gelesen |
| Q-CCI | Liu: „More Is Not Always Better: Cross-Component Interference in LLM Agent Scaffolding“, arXiv 2605.05716 | https://arxiv.org/abs/2605.05716 | PP | nur Abstract |
| Q-SURV | „From Question Answering to Task Completion: A Survey on Agent System and Harness Design“, arXiv 2606.20683 | https://arxiv.org/abs/2606.20683 | PP (Survey) | Abschnitt 7.4 auszugsweise gelesen |
| Q-SWEX | SWE-bench/experiments (Vorhersagen, Logs und Ergebnisse pro Instanz, 182 Verified-Einreichungen) | https://github.com/SWE-bench/experiments | RP/Daten | Existenz und Umfang geprüft, Inhalt nicht |
| Q-EPOCH | Epoch AI, SWE-bench-Verified-Seite (Scaffold-Wechsel v2, Claude Code/Codex als Scaffolds) | https://epoch.ai/benchmarks/swe-bench-verified | LB | nur Sekundärquelle (Suchzusammenfassung, Zitat in Q-STOP) |
| Q-SEAL | SEAL vs. Claude Code, Opus 4.5 auf SWE-bench Pro, 45,9 % gegen 55,4 % | (zitiert in Q-STOP) | LB/HS | nur Sekundärquelle |

## Schwierigkeit und IRT (Frage 3)

| Kürzel | Quelle | URL | Typ | Prüfstatus |
|---|---|---|---|---|
| Q-AP | Ge, Kryvosheieva, Fried, Girit, Hariharan: „Agent psychometrics: Task-level performance prediction in agentic coding benchmarks“, arXiv 2604.00594 (ICLR-2026-Workshop) | https://arxiv.org/abs/2604.00594 | PP (Workshop) | im Original gelesen (Methode, §5.2, Anhang C.5) |
| Q-TINY | Maia Polo et al.: tinyBenchmarks, ICML 2024, arXiv 2402.14992 | https://arxiv.org/abs/2402.14992 | PR | nur Zusammenfassung |
| Q-META | Kipnis et al.: metabench, ICLR 2025, arXiv 2407.12844 | https://arxiv.org/abs/2407.12844 | PR | nur Abstract |
| Q-FLUID | Hofmann et al.: Fluid Language Model Benchmarking, COLM 2025, arXiv 2509.11106 | https://arxiv.org/abs/2509.11106 | PR | nur Abstract |
| Q-VAN | Vania et al.: Comparing Test Sets with Item Response Theory, ACL 2021, arXiv 2106.00840 | https://arxiv.org/abs/2106.00840 | PR | nur Abstract |
| Q-TRU | Truong, Tu, Liang, Li, Koyejo (2025): Schwierigkeitsvorhersage aus Aufgabeneinbettungen (amortisierte, modellbasierte Evaluation) | (zitiert in Q-AP) | PR laut Zitat, nicht geprüft | nur Sekundärquelle |
| Q-PSN | „Lost in Benchmarks? Rethinking LLM Benchmarking with Item Response Theory“ (PSN-IRT), arXiv 2505.15055 | https://arxiv.org/abs/2505.15055 | PP | nur Sekundärquelle (Suchzusammenfassung) |
| Q-MIRT | Mixture-IRT und LLM-Schwierigkeitsvorhersage, AIME-Con 2026 (Work in Progress) | https://aclanthology.org/2026.aimecon-wip.36.pdf | PR (Workshop/WIP) | nur Sekundärquelle |
| Q-KORDI | Kordi et al.: „Revisiting Generalization Across Difficulty Levels: It's Not So Easy“, arXiv 2511.21692 | https://arxiv.org/abs/2511.21692 | PP | nur Abstract |
| Q-METR | Kwa et al. (METR): Measuring AI Ability to Complete Long Software Tasks, arXiv 2503.14499 | https://arxiv.org/abs/2503.14499 | PP | nur Abstract |
| Q-LIN | Linacre (1994): Sample Size and Item Calibration Stability, Rasch Measurement Transactions 7:4, S. 328 | https://www.rasch.org/rmt/rmt74m.htm | BL (Fach-Newsletter, nicht begutachtet) | im Original gelesen (Tabelle) |
| Q-KRI | Kriegeskorte, Simmons, Bellgowan, Baker (2009): Circular analysis in systems neuroscience: the dangers of double dipping. Nat Neurosci 12:535–540 | https://pmc.ncbi.nlm.nih.gov/articles/PMC2841687 | PR | nur Zusammenfassung, ergänzt durch Fachwissen |
| Q-BA | Bland & Altman (1995): Comparing methods of measurement: why plotting difference against standard method is misleading. Lancet 346:1085–1087 | https://www-users.york.ac.uk/~mb55/meas/diffplot.htm | PR | nur Zusammenfassung, ergänzt durch Fachwissen |
| Q-RCI | Cacioli: „Beyond the Mean: Within-Model Reliable Change Detection for LLM Evaluation“, arXiv 2604.27405 | https://arxiv.org/abs/2604.27405 | PP | nur Abstract, plus Suchzusammenfassung zur Regression zur Mitte |
| Q-PROP | Järviniemi et al.: „Propensity Inference: Environmental Contributors to LLM Behaviour“, arXiv 2604.21098 | https://arxiv.org/abs/2604.21098 | PP | im Original gelesen (§2.4) |
| Q-DML | Chernozhukov et al. (2018): Double/debiased machine learning (Cross-Fitting), Econometrics Journal | – | PR | Fachwissen (nur als Hintergrund für Kreuzanpassung, im Text nicht als Beleg zitiert) |

## Fehlerkorrelation (Frage 4)

| Kürzel | Quelle | URL | Typ | Prüfstatus |
|---|---|---|---|---|
| Q-KIM | Kim, Garg, Peng, Garg: Correlated Errors in Large Language Models, ICML 2025, arXiv 2506.07962 | https://arxiv.org/abs/2506.07962 | PR | nur Abstract |
| Q-CAPA | Goel et al.: Great Models Think Alike and this Undermines AI Oversight, arXiv 2502.04313 | https://arxiv.org/abs/2502.04313 | PP. Annahme ICML 2025, nicht geprüft. | nur Abstract |
| Q-GEI | Geirhos, Meding, Wichmann: Beyond accuracy … error consistency, NeurIPS 2020, arXiv 2006.16736 | https://arxiv.org/abs/2006.16736 | PR | nur Abstract, plus Formel aus Fachwissen |
| Q-KLE | Klein, Meyen, Brendel, Wichmann, Meding: Quantifying Uncertainty in Error Consistency, arXiv 2507.06645 | https://arxiv.org/abs/2507.06645 | PP | nur Abstract |
| Q-DEI | Zhang et al.: Diversity Empowers Intelligence (DEI), arXiv 2408.07060 | https://arxiv.org/abs/2408.07060 | PP. Laut Suchtreffer ICLR 2025, nicht geprüft. | nur Abstract, Orakel-Zahlen nur Sekundärquelle |
| Q-KUN | Kuncheva & Whitaker (2003): Measures of diversity in classifier ensembles, Machine Learning 51 | – | PR | Fachwissen |
| Q-YEN | Yen (1984): Q3-Statistik für lokale Abhängigkeit (IRT) | – | PR | Fachwissen |

## Langer Kontext (Frage 6)

| Kürzel | Quelle | URL | Typ | Prüfstatus |
|---|---|---|---|---|
| Q-DU | Du et al.: Context Length Alone Hurts LLM Performance Despite Perfect Retrieval, Findings EMNLP 2025, arXiv 2510.05381 | https://arxiv.org/abs/2510.05381 | PR | nur Abstract |
| Q-ROT | Hong, Troynikov, Huber: Context Rot (Chroma Technical Report, 14.7.2025) | https://www.trychroma.com/research/context-rot | BL (Firmenbericht) | nur Zusammenfassung (über WebFetch) |
| Q-LIM | Liu et al.: Lost in the Middle, TACL, arXiv 2307.03172 | https://arxiv.org/abs/2307.03172 | PR | nur Abstract |
| Q-POS | Veseli, Chibane, Toneva, Koller: Positional Biases Shift as Inputs Approach Context Window Limits, arXiv 2508.07479 | https://arxiv.org/abs/2508.07479 | PP | nur Abstract |
| Q-NOLIMA | Modarressi et al.: NoLiMa, ICML 2025, arXiv 2502.05167 | https://arxiv.org/abs/2502.05167 | PR | nur Abstract |
| Q-SELF | Sinha, Arun, Goel, Staab, Geiping: The Illusion of Diminishing Returns (Selbstkonditionierung), ICLR 2026, arXiv 2509.09677 | https://arxiv.org/abs/2509.09677 | PR | im Original gelesen (§3.2) |
| Q-AMEL | Temkit: AMEL – Accumulated Message Effects on LLM Judgments, arXiv 2605.22714 | https://arxiv.org/abs/2605.22714 | PP (ein Autor) | nur Abstract |
| Q-LOST | Laban, Hayashi, Zhou, Neville: LLMs Get Lost In Multi-Turn Conversation, arXiv 2505.06120 | https://arxiv.org/abs/2505.06120 | PP | Abstract und Design (concat/sharded) gelesen |
| Q-SYC | Hong, Byun, Kim, Shu, Choi: Measuring Sycophancy of LMs in Multi-turn Dialogues (SYCON-Bench), Findings EMNLP 2025, arXiv 2505.23840 | https://arxiv.org/abs/2505.23840 | PR | nur Abstract |
| Q-BELIEF | Geng et al.: Accumulating Context Changes the Beliefs of Language Models, arXiv 2511.01805 | https://arxiv.org/abs/2511.01805 | PP | nur Abstract |
| Q-CCR | Song: Cross-Context Review, arXiv 2603.12123 (v2 korrigiert) | https://arxiv.org/abs/2603.12123 | PP | nur Abstract |

## Hinweise
- Lokale Kopien der gelesenen arXiv-Texte liegen in `quellen/papers/` (HTML und daraus erzeugter Text).
- Die Repo-Klone liegen in `quellen/`. Hogwarts und MorphRig wurden wegen ihrer Größe nur teilweise bzw. per API gelesen.
- Aus den Repos wurde kein Code ausgeführt.
- Viele 2026er Preprints sind sehr neu. Versionen können sich ändern, Q-HB v1 und v2 unterscheiden sich z. B. im Aufgabenumfang.
