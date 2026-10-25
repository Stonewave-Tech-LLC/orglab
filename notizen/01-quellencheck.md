# Quellencheck zum Handoff "Teaching Agents Social Skills"

**Stand:** 20.10.2026 · Prüft Abschnitt 2 und 4 des Handoffs (`handoff-social-skills-benchmark.md`).

## Harness² (arXiv 2610.14224), Volltext gelesen

- **Bestätigt:** Northwestern und Google Cloud AI Research, 9.10.2026. Der Code steht unter Apache-2.0 auf https://github.com/google-research/harness2 (Projektseite: harness2.github.io), das Paper selbst unter CC BY 4.0.
- **Bestätigt:** "Bis zu 11,5 Punkte auf WorkBuddy-Bench", dazu 4,5 auf JobBench und 11,8 pp auf LAB (Harvey Legal). Gemessen wurde mit einem einzigen Schritt (k=1). Parallele Rekursion mit k=5 bringt bis zu +3,9, +4,2 bzw. +6,7 zusätzlich.
- **Bestätigt:** Es gibt acht Komponenten als Dateien: `systemprompt.md`, `guardrails.md`, `LongTermMEMORY.md`, `tool_guidance.md`, `sub_agents/<n>/AGENT.md`, `skills/<n>/SKILL.md`, `scripts/*.py` und ein Middleware-Plugin (`plugin/*.ts`, ein Hook um Tool-Calls). Die Aufteilung übernimmt AHE (Lin et al. 2026) und ergänzt sie um das Plugin.
- **Setup:** Die Executoren sind Gemini 3.5 Flash oder GLM-5 unter OpenCode bzw. Codex. Als Editor arbeitet standardmäßig Claude Opus 4.8 unter OpenCode.
- **Propose-Probe-Compose:**
  - Zuerst läuft eine Referenz-Ausführung.
  - Der Editor schlägt **zwei** Kandidaten vor. Der *invariante* zielt auf allgemeine Agenten-Schwächen wie Planung, Tool-Nutzung, Kontext und Delegation. Der *domänenspezifische* zielt auf Wissen und Prozeduren der Domäne.
  - Jeder Kandidat läuft auf **demselben Task**.
  - **Es gibt keinen Score.** Die Bewertung ist ein "behavioral contrast", also ein Vergleich von Trajektorie und Deliverable mit der Referenz. Daraus entscheidet ein LLM-Composer, was übernommen wird.
  - Bei k>1 wählt ein agentischer Selector das Ergebnis über anonymisierte Deliverables aus.
- **Korrektur zum Handoff:** Die Harnessing-Level-Rekursion schreibt **nicht** den Optimierer selbst um.
  - Wörtlich: "Model weights, stage instructions, and the decision rule remain fixed, while the library evolves."
  - Der Reflector schreibt nur Einträge in eine Bibliothek: einen übernommenen Harness plus `EXPERIENCE.md`.
  - Jeder neue Task startet wieder vom Basis-Harness H0.
- **Single- oder Multi-Agent:** Harness² ist **Single-Agent.** Subagents gibt es nur als Delegation über das Task-Tool. Weder Paper noch README sprechen von Multi-Agent.
- **Falle beim Lesen:** "SOCIAL" in Fig. 19 meint einen *Sozialwissenschafts*-Task aus JobBench, nicht Social Skills.
- **Limitations laut Paper:** Rekursion kostet zusätzliche Inferenz. Behavioral Contrasts sind anfällig für Ausführungsrauschen und für Biases, die Editor und Executor teilen, und sie garantieren keinen Transfer.

## Weitere Quellen

| Quelle | Status | Anmerkung |
|---|---|---|
| Dochkina, arXiv 2603.28990 | ✅ Abstract geprüft | Alle Zahlen stimmen: 25.000 Tasks, 8 Modelle, 4–256 Agenten, 8 Protokolle, +14 % (p<0,001). Das Hybridprotokoll heißt "Sequential". Einzelautorin, Preprint. Titel: "Drop the Hierarchy and Roles". |
| SwarmWorld, arXiv 2608.26081 | ⚠️ teilweise | Das Original ist gefunden. Der Abstract bestätigt die Differenzierung in "exploration, construction, maintenance, coordination". Die drei Voraussetzungen (Umwelt mit Gedächtnis, Task belohnt Spezialisierung, genug Population und Zeit) stehen **nur in der Sekundärquelle** und sind noch im Volltext zu prüfen. |
| Pressure Fields, arXiv 2601.08129 | ✅ Abstract geprüft | Autor: Roland Rodriguez. Raumplanung über 1.350 Trials: 48,5 % gelöst, gegenüber 12,6 % bei Gesprächskoordination und 1,5 % bei hierarchischer Steuerung. Konvergenz ist "under mild conditions" bewiesen. "Rollen- und nachrichtenfrei" ist nur impliziert, nicht wörtlich gesagt. |
| RegenHarness, arXiv 2609.27612 | ✅ Abstract geprüft | Robotik (cs.RO). Regression-Checks, Release-Authorization und versioniertes Rollout/Rollback sind bestätigt. **Wer** freigibt (Mensch oder Automat), sagt der Abstract nicht. |
| MAST, Ashery et al., MAEBE | – nicht neu abgerufen | Passt zu meinem Trainingswissen. Bei Bedarf separat prüfen. |
| NeoHorse-1, RRSI, Self-Harness, Video-RSI | – nicht geprüft | |

## Konsequenzen für das Projekt (meine Einschätzung)

1. **Harness² ist nicht direkt multi-agentisch.**
   - Was wir optimieren wollen, ist eine *Org-Konfiguration*: Rollen, Topologie, Gedächtnis, Reputation, Handoff-Templates, Normen.
   - Die acht Komponenten sind dagegen *pro Agent*.
   - Ein Umbau hieße: ein neunter "Org"-Komponententyp oder ein Harness pro Agent plus eine geteilte Org-Datei.
2. **Ein schlanker eigener Propose-Probe-Compose-Loop über eine Org-Config ist wahrscheinlich günstiger als ein Umbau.**
   - Wir übernehmen das Prinzip: zwei Kandidaten (invariant und szenariospezifisch), Probe auf demselben Seed, selektive Komposition, Bibliothek mit `EXPERIENCE.md`.
   - Harness² bleibt Referenz und Baseline.
3. **Wir haben einen Vorteil, den Harness² nicht hat: echte Verifier.**
   - Hidden Profile, Stille Post und Maulwurf haben bekannte Ground Truth.
   - Unsere Probes können also messen statt kontrastieren. Das ist methodisch stärker.
   - Der verifier-freie Modus wird damit ein *Vergleichsarm*: Findet ein kontrastiver Optimierer dieselben Module wie ein verifizierter?
4. **Die Novelty-Frage ("entdeckt ein Optimierer Social-Skill-Module, und übertragen sie sich?") ist weiter plausibel offen.**
   - Harness² testet Transfer nur zwischen Benchmarks (JobBench → WorkBuddy), nicht sozial.
   - Eine gezielte Literatursuche dazu steht noch aus.
