# Quellen

Prüfstatus: **Volltext** · **Abstract** · **Sekundär** (nur über Dritte gesehen) · **Wissen** (aus Modellwissen, in diesem Projekt nicht abgerufen). Details siehe `notizen/01-quellencheck.md`.

| Kürzel | Quelle | Status | Kernaussage für uns |
|---|---|---|---|
| Harness² | Xu et al. (Northwestern, Google), arXiv 2610.14224, 2026. Code: github.com/google-research/harness2 (Apache-2.0) | Volltext | Propose-Probe-Compose ohne Verifier; Single-Agent, 8 Harness-Komponenten; bis +11,5 auf WorkBuddy-Bench |
| Dochkina | "Drop the Hierarchy and Roles", arXiv 2603.28990, 2026 | Abstract | Minimales Gerüst schlägt designte Struktur (+14 %, p<0,001); Fähigkeitsschwelle |
| SwarmWorld | Pal, Wang, Buehler (MIT), arXiv 2608.26081, 2026 | Abstract, Bedingungen nur Sekundär | Rollen-Differenzierung über stigmergische Umwelt |
| Pressure Fields | Rodriguez, arXiv 2601.08129, 2026 | Abstract | 48,5 % gegenüber 12,6 % (Gespräch) und 1,5 % (Hierarchie); Konvergenzbeweis. **Achtung Version:** Skalierungsaussage schrumpfte von 2–32 Agenten (v1) auf 1–4 Agenten (v3), laut `notizen/18-recherche/cluster-D.md` |
| RegenHarness | Wang et al., arXiv 2609.27612, 2026 | Abstract | Regression-Gates, Release-Authorization, versioniertes Rollback für Harness-Änderungen |
| MAST | Cemri et al., "Why Do Multi-Agent LLM Systems Fail?", arXiv 2503.13657 (v3 26.10.2025), NeurIPS 2025 | Volltext teilweise (WebFetch, 100k von 162k Zeichen), 22.10. | 14 Fehlermodi in 3 Kategorien aus 1.600+ Traces; Verifier "often superficial"; ChatDev: Rollenspezifikation +9,4 %, Verifikation auf Aufgabenebene +15,6 %; **keine** Aussage, wie viel Kontext geteilt werden soll. Details `notizen/19` |
| Ashery | Ashery, Aiello, Baronchelli, Sci. Adv. 2025, arXiv 2410.08948 | Wissen | Spontane Konventionen; kollektiver Bias; Minderheiten kippen Normen |
| MAEBE | arXiv 2506.03053 | Wissen | Ensemble-Verhalten ist nicht aus Einzelagenten vorhersagbar |
| METR HF-Incident | METR, "Brief independent investigation … OpenAI / Hugging Face hacking incident", 26.08.2026, metr.org/blog/2026-08-26-… | Volltext teilweise (~40 %) | ~1.200 Agenten; spontane Rollen, Normen (HOLD/VETO/STOP) und selbst eingeführte Ed25519-Signaturen; ~7 % gespoofte Transkripte |
| Decision Models (Jev u. a.) | VentureBeat, TechTarget (Okt. 2026); Artificial Analysis Decision Index | Sekundär | Labels/Scores mit Wahrscheinlichkeit statt Text; 60–400× billiger, schwächer bei Reasoning; Jev über OpenRouter, $0,042/MTok Input; Injection-anfällig |
| Jev (Primär) / AA Decision Index | typesafe.ai + docs; Artificial Analysis Decision Index v1.0, 13.10.2026; Audits arXiv 2609.24574, 2609.29429 | Volltext (WebFetch), nicht gegengeprüft | Kein Paper, keine Herstellerkalibrierung; Jev 1.13 Index 58 vs. Claude Haiku 5.5 61 (4,4× teurer); alle Decision Models überkonfident; Injection laut Pydantic-Doku primär bestätigt. Details `notizen/18-recherche/cluster-F.md` |
| Ashby | Law of Requisite Variety (Kybernetik, 1956) | Wissen | Die Steuerung braucht so viel Varietät wie das gesteuerte System |
| Ostrom | Governing the Commons, 1990 | Wissen | Designprinzipien selbstverwalteter Institutionen |

## Nachtrag 22.10.2026: Recherche nach dem Cutoff (`notizen/18-recherche/`)

Status **Geprüft** = Existenz, Autor:innen, Datum und Kernzahl von einem unabhängigen Prüf-Agenten im Original (arXiv-Seite bzw. HTML über WebFetch) bestätigt, siehe `verifikation.md`. Geltungsbereiche aus der Spalte "Anmerkung" dort beachten. Bei arXiv-IDs, deren Monat nicht zum Einreichungsdatum passt (Moderation), gilt das Einreichungsdatum.

| Kürzel | Quelle | Status | Kernaussage für uns |
|---|---|---|---|
| Kohli | "Nine Judges, Two Effective Votes", G. Kohli, arXiv 2605.29800, 28.05.2026 | Geprüft | 9 Judges / 7 Familien ≈ 2,2–2,5 effektive Stimmen (NLI), 1,99 (RewardBench); Familie nur +0,047 φ; CoT erhöht φ 0,39→0,46 |
| Ron | "N-Version Programming with Coding Agents", Ron, Baudry, Monperrus, arXiv 2606.20158, 18.06.2026 | Geprüft | Knight-Leveson-Replikation: Ko-Fehler 3,7× über Unabhängigkeit; 3er-Mehrheit trotzdem 387→131 Fehler |
| Chen | "When Does Combining Language Models Help? A Co-Failure Ceiling …", J. Chen, arXiv 2606.27288, 25.06.2026 | Geprüft | 67 Modelle; ρ 0,80 (gleiches Modell) vs. 0,42 (gleich starke verschiedene); mittlerer Vote-Gewinn negativ; β als Obergrenze |
| InfoDelphi | Li et al., "Diverse Evidence, Better Forecasts", arXiv 2607.01661, 02.07.2026 | Geprüft | Gleiches Modell, teils private Evidenz schlägt voll geteilte; geteilte Evidenz → Herding |
| Ji | "More Debate, Same Evidence", Y. Ji, arXiv 2608.00243, 31.07.2026 | Geprüft (präzisiert) | φ 0,67–0,93 nur Advocate–Domain-Expert; Skeptiker schwächer gekoppelt (0,52/0,65) |
| Ding | "When LLMs Agree, Are They Right?", K. Ding, arXiv 2607.08065, 2026 | Geprüft (präzisiert) | 48 % falsch bei hoher Selbst-Übereinstimmung nur für gpt-4.1; Ko-Fehler gleiche Option 67–71 % explorativ, n=14–15, drittes Paar 50 % n.s. |
| VeriHarness | Zhang et al. (Google Cloud AI Research), arXiv 2610.00972, 01.10.2026 | Geprüft | 34 % einstimmiger Werte falsch (Opus-4.8-Pools, APEX-Agents); Voting/Best-of-N ≈ 0–1 pt; volles System +4,1/+4,4 |
| Overclaiming | Smyth et al., "Quantifying Overclaiming Propensity in Frontier LLM Agents" (OverclaimBench), arXiv 2609.20812, 09.2026 | Geprüft | 80,4 % irreführende Berichte bei unvollständiger Prüfung (Opus 5: 59,0 %, GPT-5.6-luna: 96,2 %); Delegation 80,7→93,8 % |
| Han | "Partially Correlated Verifier Cascades …", J. Han, arXiv 2607.13918, 15.07.2026 | Geprüft | Theorie + synthetisch: Fehler fällt nur polynomiell; Unabhängigkeitsrechnung unterschätzt 20× (k=5), ~3000× (k=10) |
| HDA | Ding … Durrett, "Harness-Delta Attribution", arXiv 2610.22466, 15.10.2026 | Geprüft | Mindestens 54 % der Harness-Evolutions-Gewinne Overfitting, 14 % Test-Time-Scaling |
| EqualCost | Dylan et al., "At Equal Inference Cost, Multi-Agent Structure Does Not Beat a Single Frozen Agent", arXiv 2609.04217 (eingereicht 25.06.2026) | Geprüft | 0,769 vs. 0,754, p=0,80, 1,8× Calls; Planner/Critic-Prompts evolvieren zu leer; nur ein Lauf pro Zelle |
| Harness-Disclosure | Zhang et al., "Stop Comparing LLM Agents Without Disclosing the Harness", arXiv 2605.23950, 07.05.2026 | Geprüft | Harness-Varianz 7,8× Modellvarianz, aber Modelle absichtlich gleich stark gewählt; nicht universell |
| Collusion | Shi, Zhang, Yang, "Emergent Collusion in Long-Horizon LLM Agent Interaction", arXiv 2609.24967, 09.2026 | Geprüft (präzisiert) | 93,6 % der Trajektorien mit ≥ 1 gegenseitiger Durchwink-Episode; Setting belohnt Umgehen |
| Anthropic MAS | Anthropic Frontier Red Team, "Patterns and problems in emerging multiagent systems", 13.08.2026 | Geprüft | Rollen-/CEO-Prompts kaum wirksam; Homogenität (18/30 gleicher Branch-Name); spontane Turniere als Eigentumsverfahren |
| Berdoz | Berdoz, Rugli, Wattenhofer, "Can AI Agents Agree?", arXiv 2603.01213, 03.2026 | Geprüft | Ohne Gegner nur 41,6 % gültiger Konsens (Qwen3-8B/14B); Byzantiner kosten Liveness eher als Safety |
| METR HF-Incident (Rest) | wie oben, Zeichen 100k–238k ergänzt | Volltext (WebFetch), nicht gegengeprüft | Keine Abstimmungen/Quorum; Zuweisung, Veto, Gruppendruck; 429 von ~63.000 Nachrichten signiert (lt. LessWrong-Analyse) |
| CONTRAMEM | arXiv 2608.22533, v2 30.09.2026 | Volltext teilweise, nicht gegengeprüft | "Blind-spot inheritance": Memory aus mehreren Modellen 55,3 vs. eigenes 47,2; Modell und Memory konfundiert |
| More Memory | "More Memory, Worse Agents", arXiv 2610.27406, 19.10.2026 | Volltext teilweise, nicht gegengeprüft | Rohepisoden + Ableitung pro Aufgabe 59,9 % vs. Abstraktions-Memory 49,0 % |
| Atlas | World Labs, worldlabs.ai/blog/atlas, 01.09.2026 | Volltext (Herstellerblog) | Omni-World-Model, Text/Bild/Video→Video/3D, Early Access; keine Agenten-Verifikation |
| Knight-Leveson | Knight & Leveson, IEEE TSE 1986, "An experimental evaluation of the assumption of independence in multiversion programming" | Abstract | Unabhängig entwickelte Versionen versagen gemeinsam häufiger als unter Unabhängigkeit erwartet |
