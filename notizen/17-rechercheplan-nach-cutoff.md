# Rechercheplan: was seit Juni 2026 passiert ist

**Stand:** 22.10.2026 · Schritt 1 von 2 (nur Plan, noch keine Suche). Anlass: Neos Chat-Fragen zu Selbsteinschätzung, Redundanz ("zwei Wecker"), korrelierten Fehlern und Dekorrelations-Hebeln.

**Warum:** Mein Trainingswissen endet im Juni 2026. Alles von Juli bis Oktober 2026 (und Nischiges davor) fehlt mir oder ist lückenhaft. Beispiel: Im Chat konnte ich "Jev" nicht einordnen, obwohl es seit 21.10. in `quellen.md` steht.

**Regeln für Schritt 2:**
- Funde kommen mit Prüfstatus wie in `quellen.md` (Volltext · Abstract · Sekundär).
- Herstellerangaben und Blogposts gelten als Sekundär, bis Paper/Code geprüft ist.
- Pro Cluster: 5–15 beste Funde, je 1–2 Sätze "was heißt das für uns" mit Bezug auf H-xxx.
- Ergebnis in `notizen/18-…`, Relevantes nach `quellen.md`, neue Ideen als Hypothesen-Kandidaten (nicht direkt ins Register).

Priorität: ★★★ zuerst, ★★ danach, ★ wenn Budget übrig.

---

## Die Fragen aus dem Chat

1. Wie stark korrelieren Fehler zwischen LLMs wirklich, und was dekorreliert sie? (H-026, E-016)
2. Wie viel Zuverlässigkeit holt man über Harness/Multi-Agent heraus, verglichen mit dem nächsten Modell-Release? Und welche Harness-Gewinne überleben ein Modell-Upgrade (Bitter Lesson)?
3. Welche Hebel gibt es: andere Modelle, Multimodalität, Identität/Soul, Memory, Spezialistenmodelle (World Models, Decision Models)?
4. Wer richtet, wenn diverse Agenten sich widersprechen? (Selektor-Problem, H-020)
5. Stimmen die Trends hinter Neos These: sinkende Inferenzkosten, automatisierbare Forschung?

---

## A. Korrelierte Fehler und Dekorrelation ★★★

**Bezug:** H-026, H-018, E-016 (explorativ: gleiches Modell irrt 94–187× häufiger gemeinsam als unabhängig erwartet).

**Suchbegriffe:**
- "correlated errors" large language models · "error correlation" across LLMs · "shared failure modes" LLMs
- "algorithmic monoculture" · "homogenization" LLM outputs · "outcome homogenization"
- Folgearbeiten zu Kim, Garg, Peng, Garg "Correlated Errors in Large Language Models" (ICML 2025): Zitationen seit Juni 2026
- "ensemble diversity" LLM · "diversity prediction theorem" agents · "Condorcet jury theorem" LLM voting
- "LLM-as-a-judge" self-preference / "self-enhancement bias" · "judge agreement" across model families
- "N-version programming" LLM · "design diversity" AI · "common cause failure" AI systems
- "mixture of agents" error correlation · "multi-model debate" diversity

**Klassiker als Anker (Wissen, im Original finden):**
- Knight & Leveson 1986: unabhängig entwickelte Software-Versionen versagen öfter gemeinsam als die Unabhängigkeit vorhersagt. Das ist das Wecker-Problem, 40 Jahre vor LLMs.
- Beta-Faktor-Modell (Common-Cause-Failure in Kerntechnik/Luftfahrt) · "dissimilar redundancy" (Airbus Fly-by-Wire).
- Scott Page: Diversity Prediction Theorem.

**Wildcard:** Gibt es Arbeiten, die *Information* vs. *Stil* als Dekorrelations-Quelle trennen? Das wäre direkt die Memory-vs-Persona-Frage aus dem Chat.

## B. Verifikation, Ground Truth, Selektor ★★★

**Bezug:** H-018, H-020, H-023, H-028, E-018.

**Suchbegriffe:**
- "verifier" scaling agents 2026 · "generative verifier" · "process reward model" agents
- "pass^k" reliability (τ-bench-Linie) · "reliability" vs "capability" agents · "consistency" benchmarks
- "self-verification" failure LLM · "verification gap" · "false completion" / "premature completion" agents
- "reward hacking" detection 2026 · "specification gaming" coding agents · "test tampering"
- "best-of-n selection" judge failure · "selector" bias · "aggregation" multi-agent answers
- "proof-carrying" LLM code · Lean / formal verification agents 2026 · "property-based testing" LLM
- "receipts" / "attestation" agent actions (Brücke zu AAP)

## C. Harness Engineering und automatische Harness-Optimierung ★★★

**Bezug:** H-005, H-006, E-013 (Null-Ergebnis Prompt-Regeln), Harness², AHE.

**Suchbegriffe:**
- Zitationen/Folgearbeiten zu Harness² (arXiv 2610.14224) und AHE (Lin et al. 2026)
- "harness engineering" · "agent harness" optimization · "scaffold" ablation · "meta-harness"
- "automated design of agentic systems" (ADAS-Linie) · "Darwin Gödel Machine" Folgearbeiten · OpenEvolve / AlphaEvolve-Nachbauten
- GEPA / DSPy 2026 · "prompt optimization" multi-agent · "self-improving agents" 2026
- "context engineering" · "context rot" · "long-horizon agents" context management
- **Bitter-Lesson-Frage:** "scaffold" gains model upgrade · "harness" transfer across models · "do agent frameworks age"
- Benchmarks, bei denen derselbe Modell-Checkpoint mit verschiedenen Scaffolds läuft (SWE-bench, Terminal-Bench, OSWorld, WorkBuddy-Bench, JobBench)

**Orte:** Changelogs/Engineering-Blogs von Claude Agent SDK, Claude Code, Codex CLI, OpenCode, OpenHands, SWE-agent.

## D. Multi-Agent-Organisation und emergente Institutionen ★★★

**Bezug:** H-001…H-004, H-012, H-015, H-022, H-024, H-025, H-028, `notizen/07`.

**Suchbegriffe:**
- Folgearbeiten zu Dochkina (2603.28990), SwarmWorld (2608.26081), Pressure Fields (2601.08129), MAST (2503.13657)
- "agent societies" · "multi-agent governance" · "agent constitution" · "voting" LLM agents · "liquid democracy" agents
- "Byzantine fault tolerance" LLM agents · "consensus" LLM agents adversarial
- "reputation system" agents · "trust" multi-agent LLM · "Sybil" agents
- "stigmergy" LLM · "blackboard architecture" LLM 2026 · "shared state" agents coordination
- "collusion" LLM agents · "secret collusion" / steganography · "emergent coordination" deception
- Concordia (DeepMind) · Project Sid / Altera · Agent Village · "AI town" Nachfolger
- METR Hugging-Face-Incident: Folgeberichte, Reaktionen von OpenAI/Hugging Face, Analysen der selbst eingeführten Ed25519-Signaturen

## E. Memory, Identität, Konsistenz über Zeit ★★

**Bezug:** Elara/soul.md, Companion-Harness, Chat-Hypothese "Memory dekorreliert stärker als Persona".

**Suchbegriffe:**
- "procedural memory" agents · "skill library" agents 2026 · "experience replay" LLM agents · `EXPERIENCE.md`-artige Ansätze
- "memory consolidation" agents · "sleep-time compute" · "reflection" memory long-horizon
- Memory-Benchmarks: LongMemEval, LoCoMo, Nachfolger 2026
- "persona vectors" (Anthropic 2025) Folgearbeiten · "persona drift" · "character consistency" long conversations · "identity stability" agents
- "persona prompting" effect on accuracy/knowledge (Hypothese: Persona ändert Stil, nicht Wissen)
- "heterogeneous experience" ensembles · "agents with different histories" diversity
- Produkte/Repos: Letta, Mem0, Zep/Graphiti, Claude Memory Tool, ChatGPT Memory: Änderungen seit Juni

## F. Spezialistenmodelle und neue Modellklassen ★★

**Bezug:** H-026 (andere Architektur als Dekorrelator), `notizen/14` Nachtrag Jev.

**Suchbegriffe:**
- **Decision Models:** Jev / TypeSafe AI (Paper? Kalibrierungsbelege?), Artificial Analysis Decision Index, Konkurrenzprodukte
- **World Models:** World Labs (Marble; "ATLAS" verifizieren, Name unklar), DeepMind Genie-Linie, Meta V-JEPA, NVIDIA Cosmos: Was kam seit Juni?
- "world model" + agents planning · "world model" as verifier / simulator for agent actions
- kleine, kalibrierte Klassifikatoren als Prüfer · "reward model" as judge · "uncertainty quantification" LLM 2026 · "conformal prediction" LLM agents
- multimodale Verifikation (Screenshot-/Video-Prüfung von Agenten-Ergebnissen)

## G. Mensch im Loop: Verlässlichkeit pro Mensch-Minute ★★

**Bezug:** `notizen/14` Baustein C, H-024.

**Suchbegriffe:**
- "learning to defer" LLM · "selective prediction" agents · "abstention" calibration
- "scalable oversight" 2026 · "AI control" (Redwood) trusted/untrusted monitoring · "untrusted monitoring" collusion
- "audit sampling" agents · "spot check" human oversight · "human-agent teaming" reliability

## H. Vertrauens-Infrastruktur für Agenten (AAP) ★

**Bezug:** AAP, H-028, METR-Signaturen.

**Suchbegriffe:**
- AP2 Updates seit Wechsel zur FIDO Alliance · ACP (OpenAI/Stripe) · Visa TAP · Web Bot Auth (IETF)
- "agent identity" standards · MCP authorization · A2A protocol security · "verifiable credentials" agents · "agent receipts"

## I. Trends hinter der These ★

**Suchbegriffe:**
- Inferenzkosten-Verfall 2026: Epoch AI, Artificial Analysis (Preis pro Intelligenz-Index-Punkt)
- METR "time horizon" Update 2026
- "automated AI research" · "AI scientist" 2026 · PaperBench / MLE-bench / RE-Bench Stand · "automated alignment research"

---

## Quellen-Orte

**Paper:**
- arXiv cs.MA, cs.AI, cs.CL, cs.LG, cs.SE (Juli–Oktober 2026)
- **OpenReview ICLR 2027 Submissions** (Deadline ~Ende Sept.): das dichteste Archiv für genau dieses Zeitfenster
- NeurIPS 2026 Accepted Papers + Workshops · COLM 2026
- Semantic Scholar (Zitationsverfolgung) · alphaXiv · Hugging Face Daily Papers

**Labs und Eval-Organisationen:**
- Anthropic (Research, Engineering, Alignment Science Blog) · OpenAI · Google DeepMind / Google Research · Meta FAIR · Microsoft Research (AutoGen/Magentic)
- DeepSeek · Qwen · Moonshot · Zhipu
- METR · Epoch AI · Apollo Research · Redwood Research · UK AISI (Inspect) · Artificial Analysis

**News und Newsletter:**
- Import AI · Interconnects · Latent Space · Simon Willison · AINews (smol.ai) · Zvi · The Decoder (deutsch) · Heise

**GitHub:**
- Trending (Python/TS/Rust, "agent")
- awesome-Listen zu Multi-Agent/Agent-Memory
- Repos: harness2, OpenHands, SWE-agent, OpenCode, Letta, CrewAI, LangGraph, AG2, CAMEL, Concordia

**Community:** Hacker News · r/LocalLLaMA · X-Accounts der Paper-Autor:innen

## Vorschlag für Schritt 2

- Pro ★★★-Cluster (A–D) ein paralleler Recherche-Agent, danach E–F. G–I nur, wenn Budget bleibt.
- Jeder Agent liefert Funde mit Link, Datum, Prüfstatus und Bezug H-xxx.
- Ich führe zusammen, prüfe die wichtigsten 5–10 im Original und schreibe `notizen/18`.
- Budget: Websuche läuft über das Abo. Wochenstand laut Laborbuch ~65 % (05:17). Mit 4 parallelen Agenten bleibt das moderat.
