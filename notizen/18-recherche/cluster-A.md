# Recherche Cluster A: Korrelierte Fehler und Dekorrelation

**Stand:** 22.10.2026 · Recherche-Agent Cluster A · Grundlage: `notizen/17` Abschnitt A
**Prüfstatus:** Volltext (Paper/Primärdokument substanziell gelesen; hier: arXiv-HTML abgerufen und maschinell ausgewertet, Zahlen aus dem Text) · Abstract (nur Abstract/Primär-Zusammenfassung) · Sekundär (nur über Dritte) · Wissen (aus Modellwissen, nicht abgerufen).
**Vorbehalt:** Fast alle Funde sind unbegutachtete arXiv-Preprints, viele von Einzelautor:innen. Zahlen aus Abstracts sind nicht gegen Tabellen geprüft. "Volltext" heißt: HTML-Fassung abgerufen und ausgewertet, nicht Zeile für Zeile gelesen.

---

## Kernfunde (nach Wichtigkeit)

### A1. Nine Judges, Two Effective Votes: Correlated Errors Undermine LLM Evaluation Panels
- **Autor:** Guneet Kohli (Einzelautor) · **Datum:** 28.05.2026 (v1) · **Link:** https://arxiv.org/abs/2605.29800
- **Prüfstatus:** Volltext (HTML)
- **Kernaussage:** 9 Frontier-Judges aus 7 Familien (GPT-4o/-mini, Claude Sonnet 4.5, Gemini 2.5 Pro, Llama 4 Maverick/Scout, Qwen3-32B, Mistral Large 3, DeepSeek-V3) auf ChaosNLI (100 Menschenlabels/Item) und RewardBench: mittleres φ der Fehlervektoren 0,33–0,44, Kish-n_eff = k/(1+(k−1)φ̄) ≈ **2,2–2,5** (Menschen: 4,0–5,8). Gap zum Condorcet-Ideal 7,6–22 pp; der beste Einzel-Judge ist in allen Bedingungen ≥ Panel. 9,1 % Fehler auf *einstimmigen* Items (unabhängig erwartet ≈ 0,02 %). **Nichts dekorreliert:** Prompt-Umformulierung (n_eff 2,17), Label-Reihenfolge (2,15), Temperatur 0,5 (2,17); **Chain-of-Thought erhöht die Korrelation** (φ̄ 0,391→0,456, n_eff 1,94). Familiengrenze kaum wirksam: gleiche Familie φ ≈ 0,44, über Familien 0,39; die drei am stärksten korrelierten Paare sind *familienübergreifend* (Claude×Gemini 0,603, GPT-4o×Claude 0,588). Aggregation (Dawid-Skene, Gewichtung, auch mit Oracle) schließt ≤ 11 % des Gaps.
- **Bedeutung für uns:** Direkter Beleg für H-026 außerhalb unseres Testbeds, aber mit Wendung: Die *Familiengrenze* ist ein schwacher Dekorrelator, die Korrelation sitzt im "Frontier-Konsens". Kish-n_eff und Condorcet-Gap sind fertige Kennzahlen für E-017 (Neuauflage E-016). Persona-Prompts wurden *nicht* getestet (offene Lücke, die wir füllen können).

### A2. N-Version Programming with Coding Agents (Knight–Leveson-Replikation)
- **Autoren:** Javier Ron, Benoit Baudry, Martin Monperrus (KTH / U. Montréal) · **Datum:** 18.06.2026 · **Link:** https://arxiv.org/abs/2606.20158
- **Prüfstatus:** Volltext (HTML)
- **Kernaussage:** 48 akzeptierte Implementierungen der Launch-Interceptor-Spezifikation (wie Knight & Leveson 1986), erzeugt von 5 Harnesses (Cursor, Claude Code, Codex, Gemini, OpenCode), 23 Modellen, 3 Sprachen (Python, Rust, Pascal); 10⁶ Zufallseingaben. Gemeinsame Ausfälle K = 429 vs. 115,4 bei Unabhängigkeit erwartet (≈ 3,7×, z = 29,2): Unabhängigkeit klar verworfen, in *jeder* Sprachscheibe. Agenten-, Modell- und Sprachgrenzen beseitigen die hohen Korrelationen nicht (viele Paare mit φ = 1 auch über Harness-Grenzen). Ursache der gemeinsamen Fehler: **schwierige/mehrdeutige Spezifikationsstellen** (Umkreis statt minimaler umschließender Kreis; Winkel-Toleranz-Semantik). Trotzdem: Mehrheitsvotum über Tripel senkt mittlere Ausfälle 387→131, Maximum 10.469→419.
- **Bedeutung für uns:** Die 40 Jahre alte Wecker-Lehre hält 1:1 für Coding-Agenten. Zwei Lehren für H-018/H-026: (1) Korrelation entsteht an *Item-Eigenschaften* (Mehrdeutigkeit, Schwierigkeit), nicht nur an Modellidentität → E-017-Belege gezielt mit mehrdeutigen Stellen bauen; (2) Voting hilft trotzdem, wenn Einzelfehler selten und teilweise verschieden sind; es versagt im Co-Failure-Kern.

### A3. When Does Combining Language Models Help? A Co-Failure Ceiling on Routing, Voting, and Mixture-of-Agents Across 67 Frontier Models
- **Autor:** Josef Chen (KAIKAKU) · **Datum:** 25.06.2026 (v1) · **Link:** https://arxiv.org/abs/2606.27288
- **Prüfstatus:** Volltext teilweise (~60 % des HTML gelesen)
- **Kernaussage:** Die Obergrenze jedes Multi-Modell-Systems ist β = Anteil der Queries, auf denen *alle* irren (Genauigkeit ≤ 1−β); das mittlere paarweise ρ identifiziert β nicht (ab m ≥ 3), und Gauß-Copula-Modelle unterschätzen β (MATH-500 ≈ 2,5×, CI 1,7–3,4). Zahlen: ρ innerhalb Familie 0,528 vs. über Familien 0,459 (schwer: 0,402 vs. 0,380). **Gleiches Modell mehrfach gesampelt: ρ_intra = 0,80; heterogenes Band: ρ_inter = 0,42.** β: MATH-500 0,052, MATH-Hard 0,044, Code 0,079, GPQA Multiple-Choice ≈ 0, aber **GPQA Free-Response 0,127** (Offenheit des Formats öffnet den Co-Failure-Tail). Mehrheitsvotum über 455 Tripel im Mittel *schlechter* als bestes Mitglied (−0,10 schwer, −0,02 gesättigt); heterogene Fusion schlägt Self-MoA bei gleicher Qualität nur knapp (+0,027). Gelernte Router holen praktisch nichts vom Oracle-Gewinn.
- **Bedeutung für uns:** Liefert das richtige Maß für H-026: nicht φ, sondern β mit Clopper-Pearson-Schranke. ρ_intra 0,80 deckt sich mit E-016 (gleiches Modell 94–187× häufiger gemeinsam falsch). Wichtig für Belegdeutung (offene Urteile ≈ Free-Response): dort ist der gemeinsame Blindfleck größer.

### A4. Diverse Evidence, Better Forecasts: Multi-Agent Deliberation Under Information Asymmetry (InfoDelphi)
- **Autor:innen:** Yuante Li, Yicheng Tao, Kate Zhang, Taozhi Wang, Gefei Gu, Yaxin Zhou · **Datum:** 02.07.2026 · **Link:** https://arxiv.org/abs/2607.01661
- **Prüfstatus:** Volltext teilweise (~85 %)
- **Kernaussage:** Sehen alle Agenten dieselbe Evidenz, wird Deliberation zu *Herding* (Inter-Agent-Varianz sinkt Runde 1→2 um 90–92 %). Lösung: Evidenz in öffentlichen Teil (Anteil ρ) und disjunkte private Teile splitten; Theorie: Corr(εᵢ,εⱼ) = ρ²σ²_pub / (ρ²σ²_pub + (1−ρ)²σ²_priv). Auf 375 Prognosemarkt-Fragen: Brier 0,178 / 77,9 % vs. ρ = 1 (alle sehen alles) 0,193 / 75,7 %; homogene Multi-Agent-Baselines (MoA u. a.) schlagen einen Einzelagenten mit CoT nicht. Alle Agenten **dasselbe Modell** (gpt-5.4-mini) — der Effekt kommt allein aus Informationsverteilung. Fehlerkorrelation selbst wurde *nicht* empirisch gemessen; Persona- oder Modell-Diversität wurde *nicht* als Kontrast getestet.
- **Bedeutung für uns:** Stärkster bisher gefundener Beleg für "Information dekorreliert" (Chat-These Memory > Persona, `notizen/17` Wildcard). Aber kein direkter Vergleich Information vs. Stil — genau diese Lücke könnten wir mit E-017 füllen. Bezug H-015: Geteilter sichtbarer Zustand (Board) könnte die Prüfer *homogenisieren*.

### A5. More Debate, Same Evidence: Structural Limits of Homogeneous Multi-Agent Groundedness
- **Autor:** Yuelyu Ji · **Datum:** 31.07.2026 · **Link:** https://arxiv.org/abs/2608.00243
- **Prüfstatus:** Volltext (kurz)
- **Kernaussage:** Drei Persona-Agenten desselben Modells (GPT-5.5 Chat: Advocate, Domain Expert, Skeptic) prüfen Groundedness auf 6 Benchmarks. Fehlerkopplung (φ) Advocate–Domain-Expert 0,671–0,927 (gepoolt 0,858) — **Persona-Etiketten dekorrelieren kaum**. Der Skeptiker (andere *Prüfaufgabe*: Falsifikation, Veto) entkoppelt auf schweren Datensätzen (WiCE 0,288, SciFact 0,375), wird aber vom Aggregator überstimmt, weil das 2:1-Mehrheitsvotum vor dem Veto greift. Panel vs. Einzelagent: +8,5 bis −4,4 pp, aufgabenabhängig (Modelle verschieden, also kein Kausalbefund).
- **Bedeutung für uns:** Erste Zahlen zu Persona-Kopplung. Stützt die Lesart: Rollen-*Stil* dekorreliert nicht, eine andere *Prüffunktion* (Falsifizieren statt Bestätigen) teilweise schon → passt zu H-018 (Prüfpfad-Diversität). Zeigt außerdem: Aggregationsregel entscheidet, ob die dekorrelierte Stimme zählt (Bezug H-020, H-028).

### A6. When LLMs Agree, Are They Right? Auditing Self-Consistency and Cross-Model Agreement as Confidence Signals
- **Autor:** Kaihua Ding (UPenn) · **Datum:** 09.07.2026 · **Link:** https://arxiv.org/abs/2607.08065
- **Prüfstatus:** Volltext (HTML)
- **Kernaussage:** 265.000 Samples (GPQA Diamond, AIME). Self-Consistency korreliert nur mäßig mit Richtigkeit (Spearman 0,20–0,59). gpt-4.1 erreicht auf GPQA bei 77 % der Fälle ≥ 80 % Selbstübereinstimmung, davon **48 % falsch**. Stärkeres Modell = höhere Übereinstimmung, aber *schlechtere* Übereinstimmungs-Richtigkeits-Kopplung (Δρ −0,18/−0,26). Explorativ über Anbieter: Wenn gpt-4.1 und Claude (Haiku 4.5/Sonnet 4.6) beide falsch liegen, wählen sie in 67–71 % dieselbe falsche Option; 6 Items von allen 4 Modellen konfident falsch.
- **Bedeutung für uns:** Kontrast zu E-016 (dort war Konfidenz ein brauchbares Eskalationssignal: ≥ 0,97 → 0,2 % Fehler). Bei schweren Items kippt das: hohe Einigkeit ist kein Richtigkeitsbeleg, auch nicht anbieterübergreifend. Die Minimalregel "nur bei Unsicherheit an Menschen" muss an schwierigen Belegen (E-017) neu geprüft werden.

### A7. Partially Correlated Verifier Cascades in LLM Harnesses: Concave Log-Odds, Polynomial Reliability, and Blind-Spot Ceilings
- **Autor:** Jiangang Han · **Datum:** 15.07.2026 · **Link:** https://arxiv.org/abs/2607.13918 (baut auf "Odds Law", arXiv 2606.15712, 14.06.2026 auf)
- **Prüfstatus:** Abstract
- **Kernaussage:** k serielle Prüf-Gates mit korrelierter Falsch-Akzeptanzrate α ~ G: Log-Odds wachsen konkav statt linear, Fehler fallen polynomiell (~k^−b) statt exponentiell; ein "Blind-Spot-Atom" (α = 1) deckelt die Gesamtevidenz bei −ln(1−π) — Zuverlässigkeit plateaut unter 1; mehr Gates können sogar schaden. Unabhängigkeits-Extrapolation unterschätzt Ausfälle synthetisch um ~20× (k = 5) bzw. ~3000× (k = 10). Zwei wiederholte Urteile je Instanz reichen, um ρ_v zu schätzen. Empfehlung: dekorrelieren (Modellfamilie, Modalität, **Evidenzquelle**) statt Gates stapeln.
- **Bedeutung für uns:** Formale Fassung von H-026 und H-018 für Prüfketten. Die Schätzmethode (R wiederholte Verdikte → Momente von G) passt direkt auf unsere Panel-Daten.

### A8. The Honest Quorum Problem: Epistemic Byzantine Fault Tolerance for Agentic Infrastructure
- **Autoren:** Jun He, Deying Yu · **Datum:** 17.07.2026 · **Link:** https://arxiv.org/abs/2607.16109
- **Prüfstatus:** Abstract
- **Kernaussage:** Klassische BFT setzt voraus, dass nicht-byzantinische Knoten die Übergangslogik korrekt ausführen. LLM-Validatoren können protokolltreu und "ehrlich" sein und trotzdem ungültige Übergänge bestätigen ("epistemischer Fehler"); wegen geteilter Gewichte/Daten/Prompts/Tools korrelieren diese. EBFT ergänzt die f-Schranke um zwei Budgets (kohärente Falsch-Zustimmung; unbrauchbare Unterstützung → Lebendigkeit). Nominell verschiedene Agenten helfen nur, wenn sie die obere Tail-Konzentration falscher Zustimmungen messbar senken.
- **Bedeutung für uns:** Direkt H-028: Unser 3f+1-Befund behandelt Lügner als einzige Fehlerquelle; EBFT ergänzt "ehrliche, korreliert irrende" Wähler. Erklärt, warum die belegbasierte Regel (Umwelt-Quittung) robuster ist als Stimmen.

### A9. Are Diversity Metrics Measuring Diversity? A Capability-Controlled Audit of Majority-Vote Gain in LLM Ensembles
- **Autor:** Donghwan Kim · **Datum:** 22.07.2026 · **Link:** https://arxiv.org/abs/2607.20768
- **Prüfstatus:** Abstract
- **Kernaussage:** 31.900 Teilmengen aus 30 LLMs (MMLU-Pro, TruthfulQA). Mehrheitsvotum schlägt das stärkste Mitglied nur in ~10 % der 3er-Teilmengen (18,7 % mit Held-out-Auswahl), obwohl Oracle-Gewinn überall positiv ist. Gängige Diversitätsmaße sind fast kollinear mit Fähigkeit (Spearman ≈ 0,99 zu 1−mittlere Genauigkeit); nach Fähigkeitskontrolle bleibt nur ein kleiner, robuster Effekt: mehr geteilte Fehler → weniger Voting-Gewinn.
- **Bedeutung für uns:** Methodische Warnung für E-017: "Diversität" ohne Fähigkeitskontrolle misst Fähigkeit. Fehlerkorrelation immer konditional auf Fehlerrate auswerten (wie Kish/φ auf Fehlervektoren, nicht Rohübereinstimmung).

### A10. A Statistical Framework for Auditing Behavioral Dependence and Induced Bias in LLM Judges
- **Autor:innen:** Chenchen Kuai, Jiwan Jiang, Zihao Zhu, Hao Wang, Keshu Wu, Zihao Li, Yunlong Zhang, Chenxi Liu, Zhengzhong Tu, Zhiwen Fan, Yang Zhou · **Datum:** v1 08.04.2026, v2 09.08.2026 · **Link:** https://arxiv.org/abs/2604.07650
- **Prüfstatus:** Abstract
- **Kernaussage:** 18 LLMs aus 6 Familien zeigen signifikante "Behavioral Entanglement" (geteilte Pretraining-Daten, Distillation, Alignment-Verfahren als vermutete Quellen). Ein Difficulty-Weighted Entanglement Index (gewichtet gemeinsame Fehler auf *leichten* Items stärker) und ein Maß für gleichgerichtete Falschantworten sagen Über-Bestätigung falscher Antworten durch Judges voraus (ρ ≈ 0,51 MMLU-Pro, ≈ 0,45 MATH-500). Entanglement-gewichtetes Verifier-Ensemble: +3,5 pp Genauigkeit gegenüber Mehrheitsvotum.
- **Bedeutung für uns:** Kandidat-Metrik für die Auswahl dekorrelierter Prüfer in E-017; "gemeinsame Fehler auf leichten Items" ist genau das Muster, das ein redundantes Prüf-Panel entwertet.

### A11. Monocultural Biases: Correlated biases in large language models lead to unequal systemic exclusion rates in hiring
- **Autor:innen:** Matthew Bone, Fabian Stephany, Maria del Rio-Chanona · **Datum:** 26.08.2026 · **Link:** https://arxiv.org/abs/2609.22169 (laut arXiv-Kommentar COLM 2026)
- **Prüfstatus:** Abstract
- **Kernaussage:** 10 LLMs je als Base- und Post-trained-Version im Hiring-Setting: **Post-Training macht die Entscheidungen deutlich korrelierter**; systemische Ausschlussrate (von allen Modellen abgelehnt) steigt von 5,6 % auf 17,3 %. Erste Folgearbeit in der Kim/Garg-Linie, die eine *Ursache* der Korrelation isoliert.
- **Bedeutung für uns:** Hinweis, wo die Korrelation herkommt: Post-Training/Alignment konvergiert Modelle. Neue Dekorrelations-Achse für H-026: Base- oder anders post-trainierte Modelle (bzw. Decision Models, Cluster F) als Prüfer.

### A12. Stochastic Sampling is Epistemically Shallow: The Dimensionality Gap Between Temperature Variation and Model Diversity in LLMs
- **Autor:** Izhar Ali · **Datum:** arXiv-ID 2607.20464 (Juli 2026); Abstract-Seite nennt "18.05.2026" — widersprüchlich, unverifiziert · laut Seite EIML@ICML 2026 · **Link:** https://arxiv.org/abs/2607.20464
- **Prüfstatus:** Abstract
- **Kernaussage:** Ein Modell 100× bei T = 1 vs. 24 verschiedene LLMs je 1× bei T = 0, Random-Matrix-Test (Marchenko-Pastur): Temperatur-Sampling erzeugt höchstens 1 Signal-Dimension über Rauschen (5 Familien, MMLU/HellaSwag/GSM8K), das Ensemble 4. Self-Consistency liefert Per-Item-Unsicherheit, aber keine Struktur über Items hinweg.
- **Bedeutung für uns:** Stützt E-016 (gleiches Modell mehrfach = kaum Redundanz). Temperatur ist kein Dekorrelator für *systematische* Fehler.

### A13. Model Capability Dominates: Inference-Time Optimization Lessons from AIMO 3
- **Autor:** Natapong Nitarach · **Datum:** 29.03.2026 (v2 16.04.2026) · **Link:** https://arxiv.org/abs/2603.27844
- **Prüfstatus:** Abstract
- **Kernaussage:** Verschiedene Lösungsstrategien pro Voter ("Diverse Prompt Mixer") sollten Fehler dekorrelieren — keine Prompt-Intervention half (3 Modelle, >23 Experimente, 50 IMO-Probleme). Schwächere Strategien kosten mehr Genauigkeit, als sie Korrelation sparen; Fähigkeit dominiert. Rest-Gap (42/50 Votum vs. ~45,5 pass@20) = Selektionsverlust → Verifier statt Prompts.
- **Bedeutung für uns:** Gegenbeleg zu Prompt-/Persona-Diversität als Hebel; passt zu E-013 (Null-Ergebnis Prompt-Regeln) und verweist auf das Selektor-Problem (H-020, Cluster B).

### A14. More Is Not More: What Matters for Diversity in LLM Opinions?
- **Autor:** Qiyang Yao · **Datum:** arXiv-ID 2607.20429; Abstract-Seite nennt "10.05.2026" — widersprüchlich, unverifiziert · **Link:** https://arxiv.org/abs/2607.20429
- **Prüfstatus:** Abstract
- **Kernaussage:** Faktorielles Design (Persona-Tiefe × Interaktionsarchitektur, 7 Modelle, 100 offene Fragen): Der Diversitätsgewinn kommt fast vollständig aus dem *ersten* Persona-Satz, mehr demografische Details helfen nicht oder schaden; verschiedene Architekturen erreichen getrennte Regionen des Meinungsraums; Temperatur und "sei divers"-Anweisungen sind vernachlässigbar.
- **Bedeutung für uns:** Achtung, misst *Meinungs*-Diversität, nicht Fehlerkorrelation. Persona verändert Ausgaben-Stil/-Verteilung — das heißt nicht, dass Fehler dekorrelieren (vgl. A5). Trennung "Ausgabevielfalt" vs. "Fehlerunabhängigkeit" ist für uns zentral.

---

## Weitere Funde (kürzer)

| Titel | Autor:innen, Datum | Link | Status | Kern / Bezug |
|---|---|---|---|---|
| A Second Judge is Not a Second Opinion: Correlated Error and Silent Failure in LLM Verifiers | Vishwarupe, Shadbolt, Alwazae; NeurIPS 2026 Workshop "Who Verifies the Agents?" | https://neurips.cc/virtual/2026/172889 | Abstract | Zwei Open-Weight-Judges: κ untereinander 0,879, mit Menschen ≈ 0,19; Konfidenz 0,94 bei 0,41–0,46 Genauigkeit. "Redundanz ist nur so viel wert wie Unabhängigkeit." Hohe Einigkeit ≠ Validität (H-026). Der Workshop selbst ist ein Ort für Cluster B. |
| Hidden Clones: Exposing and Fixing Family Bias in VLM Ensembles | Zacharie Bugaud, 17.03.2026 | https://arxiv.org/abs/2603.17111 | Abstract | 17 VLMs/8 Familien ≈ 2,5–3,6 effektive Voter; "Misleading"-Tier (1,5–6,5 % der Fragen): korrelierte Mehrheit → 0 %, obwohl bestes Modell richtig liegt. Hierarchical Family Voting holt dort 18–26 pp. Gegenpol zu A1 (dort bringt Familie wenig) — bei VLMs wirkt Familie stärker. |
| CARE: Confounder-Aware Aggregation for Reliable LLM Evaluation | Zhao, Shin, Huang, Namburi, Sala; v2 08.09.2026; laut arXiv ICML 2026 | https://arxiv.org/abs/2603.00039 | Abstract | Geteilte Störfaktoren (Länge, Stil) brechen Judge-Unabhängigkeit; Modell "wahre Qualität × gemeinsame Confounder", bis −26,8 % Fehler über 12 Benchmarks. Relevant für Information-vs-Stil: Stil ist hier *Quelle* der Korrelation. |
| Strategic Algorithmic Monoculture: Experimental Evidence from Coordination Games | Ballestero, Hosseini, Khanna, Shorrer; 10.04.2026 | https://arxiv.org/abs/2604.09502 | Abstract | LLMs haben hohe Basis-Ähnlichkeit, koordinieren hervorragend, können aber schlechter als Menschen divergieren, *wenn Divergenz belohnt wird*. (Zahl "58 % vs. 14 %" nur Sekundär.) → Anweisung "seid unabhängig" reicht nicht. |
| Auditing Multi-Agent LLM Reasoning Trees Outperforms Majority Vote and LLM-as-Judge (AgentAuditor, ACPO) | Yang, Li, Ping, Zhang, Bogdan, Thomason; v2 03.09.2026 | https://arxiv.org/abs/2602.09341 | Abstract | Voting versagt bei gemeinsamer falscher Begründung; Auflösung an Divergenzpunkten über Evidenz statt Mehrheit; bis +5 pp. Bezug H-020 (Beweishierarchie), Cluster B. |
| Don't Always Pick the Highest-Performing Model: An Information Theoretic View of LLM Ensemble Selection | Turkmen, Buyukates, Bastopcu; 08.02.2026 | https://arxiv.org/abs/2602.08003 | Abstract | Gauß-Copula-Fehlermodell → Fehlerboden, greedy MI-Auswahl. Achtung: A3 zeigt, dass Gauß-Copula β unterschätzt. |
| Can LLM-as-a-Judge Reliably Verify Rubrics in Agentic Scenarios? (RuVerBench) | Peng, Qi, Xia u. a.; v2 02.09.2026, EMNLP 2026 | https://arxiv.org/abs/2606.29920 | Volltext teilweise | **Gegenbefund:** Fehlermengen-Überlappung von Gemini-3.1 Pro, GPT-5.4, Claude Opus 4.7 nur 16,1 % (Deep Research) bzw. 20,6 % (Agentic Coding); Überlappungsmaß im Text nicht definiert. Self-Voting sättigt nach 3–5 Stimmen. |
| Correlated Errors in Large Language Models (Anker) | Elliot Kim, Avi Garg, Kenny Peng, Nikhil Garg; ICML 2025 | https://arxiv.org/abs/2506.07962 | Abstract | >350 LLMs; bei beiderseitigem Fehler 60 % gleiche Antwort; gleicher Anbieter/Architektur → mehr Korrelation; größere/genauere Modelle stärker korreliert. Keine Folgearbeit der Originalautor:innen gefunden. |
| Great Models Think Alike and this Undermines AI Oversight (CAPA) | Goel u. a.; ICML 2025 | https://arxiv.org/abs/2502.04313 | Sekundär | Fehlerähnlichkeit (CAPA) steigt mit Fähigkeit; Judges bevorzugen ähnliche Modelle. Keine 2026-Folgearbeit gefunden. |

## Klassische Anker

| Quelle | Status | Kern |
|---|---|---|
| Knight, J. C. & Leveson, N. G. (1986): "An Experimental Evaluation of the Assumption of Independence in Multiversion Programming." *IEEE Trans. Software Eng.* 12(1):96–109. Kurzfassung: https://www.kth.se/social/files/564df871f2765419e306178d/KnightLeveson.pdf | Abstract | 27 unabhängig entwickelte Versionen (zwei Universitäten, gleiche Spezifikation), 10⁶ Tests: einzeln sehr zuverlässig, aber Tests mit ≥ 2 gleichzeitig versagenden Programmen "substantially more than expected"; Unabhängigkeitsannahme statistisch verworfen. Exakte Zahlen (gemeinsame Fehlschläge beobachtet vs. erwartet) nicht abgerufen. A2 ist die direkte Replikation mit Agenten. |
| Beta-Faktor-Modell: K. N. Fleming, "A reliability model for common mode failures in redundant safety systems" (1975, General Atomic); Parametrisierung in NUREG/CR-5485 (US NRC, 1998); in IEC 61508 Standardmodell | Sekundär | β = fester Anteil der Ausfallwahrscheinlichkeit einer Komponente, der auf gemeinsame Ursachen entfällt; Redundanz reduziert nur den (1−β)-Teil. Zur LLM-Übersetzung siehe A3 (β als Co-Failure-Rate) und A7 (Blind-Spot-Atom). Originaltext nicht abgerufen. |
| Scott E. Page, *The Difference* (Princeton UP, 2007): Diversity Prediction Theorem | Sekundär | Identität für quadratischen Fehler: Kollektivfehler = mittlerer Einzelfehler − Vorhersagediversität (Varianz der Schätzungen). Mathematisch trivial wahr; die Lesart "mehr Diversität senkt Fehler" ist umstritten, weil Diversität und Einzelfehler nicht unabhängig variierbar sind (Kritik u. a. arXiv 2307.04709). Gilt für Mittelwert-Schätzungen, nicht direkt für Mehrheitsvoten bei Klassifikation. |

---

## Synthese

1. **Stärke der Korrelation ist jetzt gut belegt und groß:** Frontier-Judges liefern aus 9 Stimmen ~2 effektive (A1); Mehrheitsvoten schlagen das beste Einzelmodell nur selten (A3: im Mittel schlechter; A9: ~10 %). Gleiches Modell mehrfach gesampelt ist am schlimmsten (ρ_intra 0,80 vs. ρ_inter 0,42, A3; A12) — konsistent mit E-016.
2. **Die Familiengrenze ist ein schwächerer Dekorrelator als wir angenommen haben** (H-026 sagt "Redundanz aus derselben Modellfamilie bringt weniger"): Gleiche vs. andere Familie unterscheidet sich nur um 0,02–0,07 in ρ/φ (A1, A3); die stärksten Paare sind familienübergreifend; Agenten-, Modell- und Sprachgrenzen beseitigen gemeinsame Ausfälle nicht (A2). Die Korrelation ist ein Frontier-Konsens, mutmaßlich aus Post-Training (A11) und geteilten Daten (A10).
3. **Was nicht dekorreliert:** Temperatur, Prompt-Umformulierung, Strategie-Prompts (A1, A12, A13), Persona-Etiketten (A5: φ 0,67–0,93); CoT *erhöht* Korrelation (A1). Debatte mit geteilter Evidenz führt zu Herding (A4).
4. **Was dekorreliert (Belege, aber dünn):** disjunkte Information/Evidenz (A4, gleiches Modell!), eine andere Prüffunktion (Falsifizieren statt Bestätigen, A5), andere Evidenzquelle oder Modalität (theoretisch A7), Base- statt post-trainierter Modelle (A11, indirekt). Information vs. Stil ist **nirgends in einem Design direkt gekreuzt** — die Lücke bleibt offen und ist für uns adressierbar.
5. **Ort der Korrelation:** gemeinsame Fehler sitzen auf schwierigen, mehrdeutigen oder offenen Items (A2: Spezifikationsmehrdeutigkeit; A3: Free-Response β 0,127 vs. MC ≈ 0; Hidden Clones: "Misleading"-Tier). Dort sind die Modelle auch *konfident* falsch (A6).
6. **Widerspruch/Spannung:** RuVerBench (Volltext teilweise) findet in agentischen Rubrik-Prüfungen nur 16–21 % Fehlerüberlappung zwischen drei Frontier-Judges — bei langen, agentischen Ausgaben könnten Fehler *weniger* korrelieren (oder das Maß ist anders definiert). Chen (A3) findet dagegen, dass offene Formate den gemeinsamen Blindfleck vergrößern. Ungeklärt, und genau unser Setting (Belegdeutung in Agenten-Logs).
7. **Methodik:** β (alle falsch) mit Konfidenzschranke statt mittlerem φ (A3); Kish-n_eff und Condorcet-Gap (A1); Fähigkeit kontrollieren (A9); zwei wiederholte Verdikte je Item genügen zur Schätzung der Prüfer-Korrelation (A7).

## Hypothesen-Kandidaten (nicht ins Register übernommen)

- **HK-A1 (Information vs. Stil, faktoriell):** In E-017 sinkt die Fehlerkorrelation der Prüfer stärker durch disjunkte Beleg-Ausschnitte (verschiedene Log-Teile/Evidenzquellen) als durch Persona-Prompts oder durch Familienwechsel. Design: {gleiches Modell, andere Familie} × {gleiche Evidenz, disjunkte Evidenz} × {neutral, Persona}; Zielgröße β und Kish-n_eff, fähigkeitskontrolliert.
- **HK-A2 (Prüffunktion, präzisiert H-018):** Ein Prüfer mit anderer Prüfaufgabe (falsifizieren / Gegenprobe über anderen Aufrufpfad) dekorreliert stärker als ein zweiter Prüfer gleicher Aufgabe aus anderer Familie.
- **HK-A3 (Familiengrenze schwach):** Zwischen Frontier-Modellen verschiedener Anbieter ist φ der Fehlurteile in unserem Testbed nicht deutlich niedriger als innerhalb einer Familie (Differenz < 0,1). Würde H-026s Formulierung "dieselbe Modellfamilie" relativieren.
- **HK-A4 (Item-Ort):** Gemeinsame Fehlurteile konzentrieren sich auf mehrdeutige Belege; an eindeutigen Belegen sind die Prüfer nahezu unabhängig. Testbar, indem E-017-Belege mit annotierter Mehrdeutigkeit gebaut werden.
- **HK-A5 (CoT homogenisiert):** Prüfer mit erzwungenem Reasoning irren korrelierter als ohne (Replikation A1 im Agenten-Setting).
- **HK-A6 (Bester Einzelprüfer + Eskalation schlägt Panel):** Ein bester Einzelprüfer mit Konfidenz-Eskalation an den Menschen schlägt das 3er-Mehrheitspanel bei gleicher Mensch-Minute — aber nur auf leichten Belegen; auf schweren kippt die Konfidenz (A6 vs. E-016).
- **HK-A7 (Board homogenisiert Prüfung):** Geteilter sichtbarer Zustand (H-015) erhöht die Korrelation der Prüfurteile im Team (Herding wie A4), sodass Teams mit Board mehr gemeinsame Übersehens-Fehler haben als Teams mit privaten Notizen.
- **HK-A8 (Post-Training als Quelle):** Base-Modelle oder Decision Models (Cluster F) als zusätzliche Prüfer senken β stärker als ein weiteres post-trainiertes Chat-Modell — auch bei niedrigerer Einzelgenauigkeit.
- **HK-A9 (EBFT-Erweiterung von H-028):** Mehrheitsregeln versagen nicht nur gegen Lügner, sondern auch gegen ehrlich-korreliert irrende Wähler; die belegbasierte Frist-Regel bleibt gegen beide robust.
