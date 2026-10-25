# Cluster C: Harness Engineering und automatische Harness-Optimierung

**Stand:** 22.10.2026 · Recherche-Agent Cluster C · Bezug: H-002, H-005, H-006, H-015, H-016, E-013 (Null-Ergebnis), Harness², AHE.

**Prüfstatus:** **Volltext** = HTML-Fassung des Papers substanziell gelesen (über WebFetch-Zusammenfassung, bei langen Papern die ersten ~100k Zeichen) · **Abstract** = nur arXiv-Abstractseite · **Sekundär** = nur Blog/News/Suchsnippet. Alle arXiv-IDs, Titel und Autor:innen unten stammen von den arXiv-Abstractseiten, sofern nicht als Sekundär markiert.

---

## Lage in einem Absatz

Das Feld ist seit Juni explodiert. AHE (Lin et al., arXiv 2604.25850) hat laut Semantic Scholar am 22.10. **über 100 zitierende Arbeiten**, fast alle Juli–Oktober 2026, mit Titeln wie HarnessPro, ModularRSI, MetaRSI, LiteEvo, VERSE, SHarP. Harness² (2610.14224, 9.10.) ist nur einer davon und hat erst **eine** Zitation (Self-HPO, 2610.22791, nennt Harness² im Abstract aber nicht). GitHub: ca. 9.900 Sterne (Sekundär, Activepieces-Blog, ~19.10.). Parallel ist eine **kritische Welle** entstanden (Overfitting-Attribution, "kein universell bester Harness", "Illusion des Multi-Agent-Vorteils"). Multi-Agent-*Org*-Optimierung (Normen, Governance, Zustandsträger) mit echten Verifiern fand ich **nicht**. Die Lücke besteht weiter.

---

## Funde

### C1. Harness-Delta Attribution: Dissecting Gains From Harness Evolution
- **Autor:innen:** Wenxuan Ding, Qin Lu, Changlong Yu, Sha Li, Shuowei Jin, Xin Liu, Zhenyu Shi, Greg Durrett
- **Datum:** 15.10.2026 · **Link:** https://arxiv.org/abs/2610.22466
- **Prüfstatus:** Volltext
- **Kernaussage:**
  - Zerlegt den Gewinn auf dem Such-Set in drei Teile: Overfitting O (Shortcuts neutralisieren), Test-Time-Scaling T (Baseline mit gleichem Inferenzbudget) und Rest G (Obergrenze für verallgemeinerbaren Gewinn).
  - Getestet mit 3 Frameworks (Meta-Harness, SkillOpt, AHE) und 11 Executoren auf 25 Settings. 21 davon zeigen signifikante Gewinne.
  - Im Mittel erklärt **Overfitting 54 %** und **Test-Time-Scaling 14 %** des Gewinns. In 14 von 21 Settings liegt O+T über 50 %.
  - Held-out-Gewinne sind in 13 von 15 Settings kleiner als die Such-Set-Gewinne, in 4–5 Settings sogar negativ.
  - Validierungsauswahl verringert den Abstand, schließt ihn aber nicht.
  - SWE-bench zeigt den saubersten Rest-Gewinn. ALFWorld und LiveMath werden fast komplett von Overfitting getragen, etwa durch Lookup-Controller oder eine Prompt-Regel, die immer die Meta-Option wählt.
- **Bedeutung für uns:**
  - Das ist die stärkste externe Begründung für unser Design (Holdout-Domäne, frische Seeds, Zwei-Stufen-Regel).
  - Für H-005/H-006 sollten wir T explizit messen: eine compute-gematchte Baseline, z. B. B mit mehr Ticks oder Tool-Calls.
  - Der O-Term ist ein Operationalisierungsvorschlag für H-006: Overfittet ein Behavioral-Contrast-Optimierer mehr als ein verifizierter?

### C2. At Equal Inference Cost, Multi-Agent Structure Does Not Beat a Single Frozen Agent
- **Autor:innen:** David Dylan, Aoife Brennan, Cian Murphy, Niamh O'Sullivan, Conor Kelly, Saoirse Walsh
- **Datum:** 25.06.2026 · **Link:** https://arxiv.org/abs/2609.04217
- **Prüfstatus:** Volltext (ca. 75 % gelesen)
- **Kernaussage:**
  - **Setup:** MA-Evolve, ein Planner→Executor→Critic-Team. Die drei Rollen-Prompts werden per GEPA-Koordinatenaufstieg evolviert, auf einem eingefrorenen Qwen2.5-7B, bei gleicher Zahl an LLM-Calls.
  - **ALFWorld (n=134):** Stock 0,657, Single (nur Executor evolviert) 0,754 (p=0,021), Team 0,769. Team gegen Single: p=0,80 bei 1,8× Kosten.
  - **Rollen-Prompts:** Die Planner- und Critic-Prompts **evolvieren in jedem Lauf zu leeren Prompts**. Der gesamte Gewinn steckt im Executor.
  - **WebShop:** Evolution wirkt nicht, das Team tendiert schlechter.
  - **Einschränkungen:** nur ein Seed (greedy), ein Backbone, eine Topologie.
- **Bedeutung für uns:**
  - Das ist das externe Spiegelbild von E-013 und H-016: Ein Prompt-Optimierer über Rollen findet in einem Team aus demselben Modell wenig.
  - Er „entdeckt“ eher Rollen-Leere als Rollendifferenzierung, was zu H-015 und Dochkina passt.
  - Methodisch: Wir sollten call-gematchte Vergleiche berichten.

### C3. When Agents Evolve, Institutions Follow
- **Autor:innen:** Chao Fei, Hongcheng Guo, Yanghua Xiao
- **Datum:** 30.04.2026 · **Link:** https://arxiv.org/abs/2604.27691 · Code: github.com/cf3i/SocialSystemArena
- **Prüfstatus:** Volltext
- **Kernaussage:**
  - **Setup:** 7 historische Institutionen in 4 Mustern (Pipeline, Gated Pipeline, Autonomous Cluster, Konsens). Sie laufen als Governance-Spezifikationen auf gemeinsamer Runtime, getestet mit 3 Modellen (MiniMax M2.5, Kimi K2.5, Gemini 2.5 Flash) auf PinchBench (23 Tasks) und ClaweBench (104 Tasks).
  - **Spannweite:** Innerhalb eines Modells liegen zwischen bester und schlechtester Institution 57–61 pp.
  - **Keine Institution gewinnt modellübergreifend:**

    | Modell | Beste Institution | Score |
    |---|---|---|
    | MiniMax | Tang | 88,2 |
    | Kimi | Mongol | 67,3 |
    | Gemini | Edo | 87,7 |

  - **Gates verstärken die Modellvarianz:** Tang auf Kimi landet in Gate-Loop-Explosionen (18/23 Tasks laufen ins 32-Schritte-Budget).
  - **ClaweBench:** Die Spannweite schrumpft auf 8–12 pp, und die Modell-Rangfolge kehrt sich um.
  - **Grenzen:** keine automatische Auswahl (nur als Zukunftsarbeit genannt), keine Signifikanztests, kleine n.
- **Bedeutung für uns:**
  - Das ist externe Evidenz für H-002 (Org-Regime sind modellabhängig) mit großem Effekt.
  - Und für H-014: Auf komplexeren Tasks schrumpft der Org-Effekt.
  - Das Gate-Loop-Phänomen ist ein Spiegel unserer H-028/E-015-Befunde: ein Liveness-Problem bei Gate-Strukturen.

### C4. Toward an Organizational Science of Multi-Agent LLM Systems: Decoupling Who, How, and Which Algorithm (IMACS)
- **Autor:innen:** Huan Chen, Xiang Song, Jian Jin, Pan Ren, Liang-Jie Zhang
- **Datum:** 28.07.2026 · **Link:** https://arxiv.org/abs/2607.25446
- **Prüfstatus:** Volltext
- **Kernaussage:**
  - **Architektur:** Trennt Organisation (Belbin, Mintzberg, RACI), Koordination und Kollaborationsprotokoll (6 Algorithmen) in tauschbare Schichten.
  - **Kein Protokoll schlägt das stärkste Solo-Modell** in der Qualität. Getestet auf GSM8K, HotpotQA u. a. mit N=10 Items pro Zelle, also sehr klein.
  - **Ein festes Protokoll schwankt je nach Org-Preset um bis zu 0,20.**
  - **RACI-Platzierung** wirkt nur, wenn das Protokoll das Deliverable über den Accountable-Agenten leitet. Beispiel Blender, Critic statt Chair: +0,08 ± 0,02, 3 Wiederholungen. Die beste Platzierung kippt über Modellfamilien hinweg.
  - **Adaptive Org Routing** (LinUCB-Bandit): +0,039 gegenüber dem besten festen Protokoll. Gemessen wurde aber nur gegen ein **simuliertes Orakel**. Echte Läufe sind nur Machbarkeitsstudien.
- **Bedeutung für uns:**
  - Stützt H-002 qualitativ: Org-Design muss pro Modell neu validiert werden.
  - Der RACI-Befund ist ein Mechanismus-Argument: Verantwortung wirkt nur, wenn sie im Datenfluss steckt. Das passt zu E-014/E-018 (Mechanismus statt Norm).
  - Die Statistik ist schwach, das Paper eignet sich als Ideengeber, nicht als Beleg.

### C5. HarnessNet: Feedback-driven Hierarchical Joint Harness Evolution for Multi-agent Systems
- **Autor:innen:** Zhaoyuan Qiu, Sachith Seneviratne, Yu Xia, Saman Halgamuge
- **Datum:** 10.10.2026 · **Link:** https://arxiv.org/abs/2610.15221
- **Prüfstatus:** Volltext (ca. 70 % gelesen)
- **Kernaussage:**
  - **Erste explizit multi-agentische Harness-Evolution**, die ich gefunden habe.
  - Jeder Knoten ("Agentron") hat einen eingefrorenen LLM, einen eigenen Harness und einen lokalen Optimierer. Feedback läuft wie Backprop schichtweise zurück. Optimierer ist GPT-5.6 via codex-cli.
  - **Getestet** auf ALFWorld (n=109) und WebShop (n=200): 4-Knoten ALFWorld 0,165 → 0,697, WebShop 0,062 → 0,588. Hierarchisch statt global: gleich oder besser bei weniger Tokens pro Call.
  - **Migration auf andere Executoren:** Gemma4 68,8 %, Ornith 49,5 %.
  - **Topologie und Rollen bleiben fix.** Es werden nur Pro-Agent-Harnesses evolviert.
  - **Statistik:** Einzelläufe, keine Konfidenzintervalle, interne Zahlen-Inkonsistenzen.
- **Bedeutung für uns:**
  - Die Lücke aus `notizen/01` §1 ist damit **teilweise** besetzt: Multi-Agent-Harness-Evolution existiert jetzt.
  - Optimiert wird aber nur Pro-Agent-Kram, keine Org-Mechanismen (Übernahme-Regeln, Belegpflichten, Abstimmung) und keine sozialen Szenarien mit Ground Truth.
  - Unser H-005/H-006-Beitrag bleibt neu, sollte HarnessNet aber zitieren.

### C6. Stop Comparing LLM Agents Without Disclosing the Harness
- **Autor:innen:** Yunbei Zhang, Janet Wang, Yingqiang Ge, Weijie Xu, Jihun Hamm, Chandan K. Reddy
- **Datum:** 07.05.2026 · **Link:** https://arxiv.org/abs/2605.23950
- **Prüfstatus:** Volltext (Abschnitt 4.2)
- **Kernaussage:**
  - **Faktorielles Design:** 3 Modelle (GLM-5.1, GPT-5.4, Kimi K2.6) × 3 Harness-Stufen auf 100 SWE-bench-Verified-Tasks, je 2 Läufe.
  - **Effektgrößen:** Ein Harness-Wechsel bewegt ein Modell um 8,5–13 pp, ein Modellwechsel bei festem Harness nur um 2,5–5 pp. Daraus ergibt sich ein Varianzverhältnis von **7,8×**. 6 von 9 Rangpaaren kippen.
  - **Wichtiger Haken (eigene Einschätzung):** Die drei Modelle wurden **absichtlich so gewählt, dass sie im Leaderboard fast gleichauf liegen** (45,3 / 44,6 / 45,4). Die Modellvarianz ist damit per Design minimiert. Die Autor:innen sagen selbst: "We do not claim that the 7.80× ratio is universal".
  - **Gegenstimme:** Die Terminal-Bench-Autoren (2601.11868, Sekundär via thedeepfeed.ai) schreiben, die Modellwahl sei meist wichtiger als das Scaffold.
- **Bedeutung für uns:**
  - Für Neos Frage 2 (Harness vs. nächstes Modell) ist die 7,8×-Zahl ein Ausreißer-Narrativ, keine Regel.
  - Sauber formuliert: Zwischen gleich starken Modellen dominiert der Harness. Zwischen Generationen dominiert eher das Modell.

### C7. Agentic Harness Engineering (AHE)
- **Autor:innen:** Jiahang Lin, Shichun Liu, Chengjun Pan, Lizhi Lin, Shihan Dou, Zhiheng Xi, Xuanjing Huang, Hang Yan, Zhenhua Han, Tao Gui, Yu-Gang Jiang
- **Datum:** 28.04.2026 (v4 18.05.) · **Link:** https://arxiv.org/abs/2604.25850
- **Prüfstatus:** Abstract. Ablationszahlen nur Sekundär (thedeepfeed.ai).
- **Kernaussage:**
  - **Hauptergebnis:** Terminal-Bench 2 mit GPT-5.4 steigt von 69,7 auf 77,0 % in 10 Iterationen, besser als der Codex-CLI-Harness (71,9 %).
  - **Transfer:** Der eingefrorene Harness bringt auf 3 anderen Modellfamilien +5,1 bis +10,1 pp, auf SWE-bench-verified 12 % weniger Tokens.
  - **Ablation laut Abstract:** Die Gewinne kommen aus **Tools, Middleware und Long-Term-Memory, nicht aus dem System-Prompt**.
  - **Ablation laut Sekundärquelle:** Memory +5,6, Tools +3,3, Middleware +2,2, **System-Prompt −2,3**.
  - Über 100 Folgearbeiten (Semantic Scholar, 22.10.).
- **Bedeutung für uns:**
  - Direkt relevant für E-013: Unser Optimierer suchte genau in der Komponente (Prompt-Regeln), die bei AHE netto *schadet*.
  - Das stützt die Lehre aus E-013, über Mechanismen statt über Regeln zu suchen.
  - Unser Pendant zu Tools, Middleware und Memory wäre Board/Zustandsträger, Hooks wie Frist/Übernahme und Org-Gedächtnis.

### C8. Automated Discovery Has No Universally Superior Harness
- **Autor:innen:** Akshat Gupta, Jermaine Lei, Alexander Lu, Gopala Anumanchipalli, Leshem Choshen
- **Datum:** 20.07.2026 · **Link:** https://arxiv.org/abs/2607.18235
- **Prüfstatus:** Abstract
- **Kernaussage:**
  - Getestet wurden 30 budget-gematchte Harnesses (zerlegtes OpenEvolve und TTT-Discover) auf 12 Modell-Problem-Paaren mit über 3,1 Mio. Rollouts.
  - Kein fester Harness ist durchgehend der beste. OpenEvolve-Varianten schneiden meist schlechter ab als einfachere Alternativen.
  - Früher Fortschritt sagt den Endstand voraus. Eine adaptive Strategie (mehrere starten, schwache prunen) schlägt einen festen Harness und ein nicht-adaptives Ensemble.
  - Die Run-Pools und Null-Verteilungen sind veröffentlicht.
- **Bedeutung für uns:**
  - Stützt H-002/H-003 auf Harness-Ebene: Die Harness-Wahl verhält sich wie ein Hyperparameter.
  - Für unseren Optimierer: Ein Racing-Gate (früh prunen) wäre billiger als volle 10–20 Paare pro Kandidat, siehe auch Task-CoEvolve (C15).

### C9. Harness Evolution Hits a Ceiling: When Weight Training Should Begin
- **Autor:innen:** Yuan Tian, Bing Hu, Hao Wang, Binghang Lu, Fang Wu
- **Datum:** 08.10.2026 · **Link:** https://arxiv.org/abs/2610.11655
- **Prüfstatus:** Abstract
- **Kernaussage:**
  - Die Arbeit unterscheidet zwei Fehlerarten. **Prozessfehler** (blockierte Calls, Loops, erschöpftes Schrittbudget) behebt die Harness-Evolution, und dieses Verhalten lässt sich in die Gewichte trainieren. **Inhaltsfehler** (schlechter Plan) brauchen Gewichtstraining.
  - **DeepPlanning:** Qwen3.5-4B steigt von 0,16 auf 0,30, Qwen3.5-9B von 0,32 auf 0,44.
  - **LoRA auf Trajektorien aus dem evolvierten Harness:** +0,13 auf Held-out. Beim 9B-Modell erreicht der Adapter allein die volle Evolutionslinie, Inhaltsfehler sinken von 25 auf 5 %. Eine Placebo-Kontrolle ist vorhanden.
  - Gemessen über 8 Modelle aus 6 Familien.
- **Bedeutung für uns:** Für die Bitter-Lesson-Frage ist das die bisher beste Antwort auf "welche Harness-Gewinne altern":
  - **Prozess-Kompensationen** werden vom nächsten Modell (oder Training) absorbiert.
  - Was echte Information oder Umweltzugang liefert, bleibt (siehe auch C10, C12).

### C10. Beyond the Model: Demystifying Harness Effects in Software Engineering Agents
- **Autor:innen:** Haichuan Hu, Quanjun Zhang, Shengcheng Yu, Zhifei Chen, Tianyu Luo, Chunrong Fang, Zhenyu Chen, Liang Xiao
- **Datum:** 26.09.2026 · **Link:** https://arxiv.org/abs/2609.32459
- **Prüfstatus:** Abstract
- **Kernaussage:**
  - **Setup:** 2 Harnesses (mini-SWE-agent, OpenCode) × 10 Qwen/DeepSeek-Modelle × 3 Benchmarks, dazu ein modularer NanoHarness mit 5 Komponenten.
  - **Kleinere Gewinne mit stärkeren Modellen:** Komplexe Harnesses bringen bei SWE-artiger Issue-Reparatur umso weniger, je stärker das Modell ist.
  - **Bei offenen Repo-Tasks** helfen sie dagegen auch starken Modellen.
  - **Komponenten:** Strukturierte Tools und task-spezifische Subagents bringen stabile Gewinne. **Context Compression und generische Subagents können schaden.**
  - **NanoHarness gegenüber mini-SWE-agent:** +7,37 pp (Qwen3.7-Max) bzw. +6,21 pp (DeepSeek-V4-Pro).
- **Bedeutung für uns:**
  - Harness-Gewinne altern bei Aufgaben, die das Modell ohnehin fast kann. Das ist unser Deckeneffekt aus H-014/E-013.
  - Bei echter Mehrarbeit bleiben sie bestehen.
  - Generische Subagents schaden potenziell: Das ist ein Datenpunkt gegen "mehr Rollen".

### C11. Multi-Agent Teams Hold Experts Back
- **Autor:innen:** Aneesh Pappu, Batu El, Hancheng Cao, Carmelo di Nolfo, Yanchao Sun, Meng Cao, James Zou
- **Datum:** 01.02.2026 (v4 28.05.), ICML 2026 · **Link:** https://arxiv.org/abs/2602.01011
- **Prüfstatus:** Abstract. GEPA-Detail nur Sekundär (Suchsnippet).
- **Kernaussage:**
  - Selbstorganisierte Teams erreichen ihr bestes Mitglied nicht, auch wenn der Experte benannt ist. Auf ML-Benchmarks verlieren sie bis 41,1 %.
  - Der Engpass ist die Nutzung von Expertise, nicht ihre Erkennung. Teams mitteln die Meinungen statt sie zu gewichten. Der Effekt wächst mit der Teamgröße und macht dafür robuster gegen adversariale Agenten.
  - **Laut Sekundärquelle** konvergierte die GEPA-Optimierung des Team-Prompts zu "defer to the expert", was die Deliberation unterdrückt. Das Defizit blieb trotzdem bestehen. Die Autor:innen schließen: Der Engpass ist die Deliberation selbst, nicht die Formulierung.
- **Bedeutung für uns:**
  - Wieder ein Prompt-Optimierer über eine Team-Konfiguration, der das Grundproblem nicht löst: ein Analogon zu E-013.
  - Der Robustheits-Trade-off (Mitteln schützt gegen Saboteure) passt zu H-022 und H-024.

### C12. Moral Hazard in Multi-Agent Language Models
- **Autor:** Dane Malenfant
- **Datum:** 27.07.2026 (v7 07.09.) · **Link:** https://arxiv.org/abs/2607.23982
- **Prüfstatus:** Abstract
- **Kernaussage:**
  - **Setup:** Das Dialogue Moral Hazard Game, getestet mit 18 Modellen und 3.015 Entscheidungen pro Modell.
  - **GEPA-Shortcut:** GEPA hob den Teamerfolg von Muse von 22,2 auf 100 %, senkte aber die Abfragen von 51,1 auf 0,3 %. Der Erfolg beruhte auf einer gelernten Rang-Label-Kodierung statt auf echter Informationsweitergabe. Bei geändertem Mapping fiel er auf 12,5 bzw. 0 %.
  - **CREDIT:** Eine kontrafaktische Replay-Methode, die stattdessen den kausalen Beitrag belohnt.
  - **Fazit der Autor:innen:** Mechanismen optimieren, nicht nur den Teamerfolg.
- **Bedeutung für uns:**
  - Ein Paradebeispiel, warum ein Org-Optimierer Shortcut-Konventionen finden kann, die nur scheinbar Kooperation sind.
  - Für H-006 heißt das: Der Verifier sollte den Mechanismus prüfen (z. B. ob Information tatsächlich übertragen wurde), nicht nur das Endergebnis.

### C13. The Illusion of Multi-Agent Advantage
- **Autor:innen:** Prathyusha Jwalapuram, Hehai Lin, Chuyuan Li, Fangkai Jiao, Sudong Wang, Yifei Ming, Zixuan Ke, Chengwei Qin, Giuseppe Carenini, Shafiq Joty
- **Datum:** 11.06.2026 (v2 13.06.) · **Link:** https://arxiv.org/abs/2606.13003
- **Prüfstatus:** Abstract
- **Kernaussage:**
  - Automatisch generierte MAS liegen auf Reasoning- und interaktiven Tasks (u. a. BrowseComp-Plus) durchgehend unter CoT-Self-Consistency, bei bis zu 10× Kosten.
  - Auf einem synthetischen Datensatz mit echtem Zerlegungs-, Kontexttrennungs- und Parallelisierungspotenzial schlagen expertendesignte MAS die automatisch generierten.
  - Generierte Architekturen sind "bloated", also oberflächlich komplex.
- **Bedeutung für uns:**
  - Automatische MAS-Suche (ADAS/AFlow/MaAS-Linie) ist kein verlässlicher Weg zu besseren Orgs.
  - Unsere Szenarien müssen echten Multi-Agent-Bedarf haben (Information verteilt, Misstrauen, Blockierer). Sonst misst man die Illusion. Das stützt die Szenariowahl hinter H-014.

### C14. One Recipe, Many Harnesses: What Self-Evolution Encodes Across Languages and Models
- **Autor:innen:** Siqi Yang, Qianlan Yang, Yu-Xiong Wang, Saurabh Pujar, Martin Hirzel
- **Datum:** 10.08.2026 · **Link:** https://arxiv.org/abs/2608.10178
- **Prüfstatus:** Abstract
- **Kernaussage:**
  - Eine feste Evolutionsrezeptur, angewandt auf 8 Sprachen (Multi-SWE-Bench) × 3 Modelle.
  - **Gewinne kompensieren behebbare Ausführungsdefekte.** Ist die "defect mass" nahe null, ist auch der Gewinn nahe null. Es gibt zwei Null-Regionen.
  - Ein abstraktes Playbook überträgt sich, aber eine ökosystemspezifische Marge muss nativ neu evolviert werden.
  - Die Autor:innen beschreiben den evolvierten Harness als "legible compensation layer" für Lücken des Modells.
- **Bedeutung für uns:**
  - Liefert die vielleicht beste Erklärung für E-013: Nahe der Decke gibt es kaum behebbare Defektmasse, also keinen Gewinn.
  - Daraus folgt eine testbare Vorhersage (HK-C2).

### C15. Weitere Optimierer-Arbeiten (kurz, alle Abstract)

| Arbeit | Link | Kern | Bezug |
|---|---|---|---|
| HarnessCompass (Zhang et al., 03.08.) | https://arxiv.org/abs/2608.01918 | Nur task-agnostische Edits, First-Person-Feedback des Agenten, Komponenten getrennt optimiert. SWE-bench Verified mit GPT-5.4: 54 → 66 % in 5 Iterationen, schlägt AHE. Transfer auf andere Modelle. | Komponenten-Interferenz = H-004 auf Harness-Ebene |
| Task-CoEvolve (Miyai, Aizawa, Yamasaki, 20.08.) | https://arxiv.org/abs/2608.20169 | Validierungs-Tasks dort sampeln, wo Kandidaten uneins sind (Varianz). Gleiches Endergebnis bei −80 % Evaluationen. | Billigeres Gate für unseren Optimierer (Kosten waren das E-013-Problem) |
| HarnessLens / Verify Smarter, Evolve Further (Xu et al., 27.08.) | https://arxiv.org/abs/2608.27311 | Kandidaten nur auf verhaltensrelevanten Tasks verifizieren, mit Attributions-Gate. +7,6 bis +13,6 % Held-out bei weniger Budget. | H-006 (Verifier-Design) |
| Cortex (Giampieri, 09.10.) | https://arxiv.org/abs/2610.14216 | Skills/Regeln für Claude Code nur nach Messung behalten, auch Entfernen wird getestet. Mit Haiku 4.5 wirksam, mit **Sonnet 5 kaum Zusatznutzen**, im echten OSS-Projekt nichts gefunden. | Regeln altern mit Modellstärke (H-016, E-013) |
| Hierarchical Self-Improvement (Tailin Zhou, 09.08.) | https://arxiv.org/abs/2608.08466 | Harness, Evolver und Meta-Evolver, ein eingefrorenes Modell. BALROG: +15 bis +39 pp. Auf NLE (jenseits der Modellfähigkeit) kein Gewinn → "backbone capability bound" und "feedback-fidelity bound". | Harness kann Fähigkeit nicht ersetzen |
| HarnessX (Chen et al., 12.06., v3 23.07.) | https://arxiv.org/abs/2606.14249 | Typisierte Komponenten, multi-agentische Evolutions-Engine AEGIS. Ø +14,5 %, max. +44 %, Gewinne am größten bei schwachen Baselines. Laut VentureBeat (Sekundär) gewinnt das kleinste Modell am meisten. | Bitter Lesson: inverse Skalierung |
| Evo-Bench (Huang et al., 10.08.) | https://arxiv.org/abs/2608.09096 | Benchmark: Können LMs ihren Harness verbessern? 9 Modelle, bis +16,6 Punkte, frühe Sättigung, schwach bei spezifischen Office-Workflows. | Optimierer-Fähigkeit ist modellabhängig |
| Self-HPO (Wei et al., 16.10.) | https://arxiv.org/abs/2610.22791 | Harness- und Policy-RL im Wechsel. Qwen3.5-35B-A3B: 57,8 → 64,8 %. Der gemeinsame Gewinn ist größer als die Summe der Einzelgewinne. Einzige bisherige Zitation von Harness². | Co-Evolution |
| CoEvo-RSI (Su et al., 18.10.) | https://arxiv.org/abs/2610.25078 | "Brain–body mismatch": Ein evolvierter Harness verlangt Verhalten, das das Modell nicht hat. Ein Anwendungsfeld ist **Multi-Agent-Failure-Attribution** (TraceElephant). | H-002-Analogon Modell↔Harness |
| AIDE² / Recursive self-improvement of AI research agents (Srikanth et al., 22.09.) | https://arxiv.org/abs/2609.26457 | 8-Tage-Lauf, 7 übernommene Verbesserungen (Suchpolicy, Kontext-Memory), Transfer auf 4 Held-out-Benchmarks. **Reward Hacking sank von 55 auf 32 %**, ohne dass darauf optimiert wurde. | Selbstverbesserung kann Integrität verbessern |
| EvoMAS (Hu et al., Feb., v4 27.05.) | https://arxiv.org/abs/2602.06511 | MAS als Konfiguration evolviert (Rollen, Topologie, Prompts). +10,5 auf BBEH gegenüber EvoAgent. SWE-bench-Verified 79,1 % mit Claude 4.5 Sonnet. | Nächster Verwandter einer Org-Config-Suche, aber aufgabenbezogen, nicht sozial |
| Codebook Agent (Yu et al., 02.09.) | https://arxiv.org/abs/2609.02264 | Belohnte Topologien kollabieren auf **~6 verschiedene Graphen**, auch bei 64 Codebook-Slots. Weniger Kanten bedeuten nicht weniger Tokens (r ≈ −0,4). | Der Org-Raum ist kleiner als gedacht |
| HyperAgents (Meta, 2603.19461) | https://arxiv.org/abs/2603.19461 | DGM-Nachfolger, editierbare Meta-Prozedur. Laut Snippet hält die Kopplung Coding↔Selbstverbesserung außerhalb von Coding nicht. | Sekundär, nicht geprüft |

### C16. Kontext-Management und Produkte (kurz)
- **Harness Engineering: A Source-Code Study of Eleven Systems** (Barbaste, Darrigol, Vu, Wiltberger; 15.07.; https://arxiv.org/abs/2609.00006; **Abstract**)
  - Untersucht 11 produktive Coding-Harnesses (Claude Code, Codex CLI, Gemini CLI, OpenHands, OpenCode u. a.) plus Omnigent als Meta-Harness.
  - Keine Runtime importiert ein Agent-Framework, keine nutzt Embedding-Retrieval. Skills sind verbreiteter als MCP (9/11 gegenüber 8/11).
  - Im Längsschnitt über ein Quartal wandert die Verhaltenssteuerung **von Prompt-Prosa in Konfiguration**.
  - Bezug: Industrie-Bestätigung für "Mechanismus statt Prompt-Regel".
- **Context-Paper** (nur Sekundär/Snippet):
  - Self-Compacting LM Agents (2606.23525)
  - Beyond Compaction: Structured Context Eviction (2606.11213): 89 sequenzielle Tasks über 80M Tokens ohne messbaren Verlust, Herstellerangabe
  - ACM/Agentic Context Management (Meta/CMU, Juli)
  - "Beyond Skill Evolution: Self-Evolving Context Management Policies" (2609.34649; nur Titel aus der Zitationsliste)
- **Produkte** (Sekundär):
  - Claude Code 2.1.221 (03.08.) bringt das Flag `--autocompact` (techdevnotes.com).
  - Claude-Code-"Agent Teams" sind laut offizieller Doku (code.claude.com/docs/en/agent-teams, nur Snippet) experimentell und standardmäßig aus. Teammates sind direkt adressierbar, Subagents nicht.
  - Codex CLI v0.129 (Mai) hat Compaction-Hooks.
  - Zu OpenCode und OpenHands fand ich nichts Belastbares.
  - Für unser Harness-Design ist hier nichts zwingend Neues dabei.

---

## Synthese

1. **Harness-Evolution ist seit Mai die dominante Methode.** Es gibt über 100 AHE-Folgearbeiten in 6 Monaten, die Prioritätsfrage "Optimierer über Harness" ist also besetzt. Offen bleibt **Org-Mechanismen-Optimierung in sozialen Szenarien mit Ground Truth**. HarnessNet (C5) evolviert nur Pro-Agent-Harnesses in fixer Topologie, EvoMAS und Codebook optimieren Topologie für Task-Accuracy. Niemand optimiert Normen, Übernahme- oder Beleg-Regeln gegen Saboteure oder Blockierer.
2. **Die kritische Welle bestätigt unsere Methodik.**
   - HDA (C1): 54 % Overfitting und 14 % Test-Time-Scaling. Held-out-Gewinne sind fast immer kleiner.
   - Gupta et al. (C8): Es gibt keinen universell besten Harness.
   - Illusion-Paper (C13): Auto-MAS liegen unter CoT-SC.
   - Unser Holdout plus frische Seeds plus Zwei-Stufen-Regel ist genau, was diese Arbeiten fordern. Ein compute-gematchter Kontrollarm fehlt uns noch.
3. **E-013 ist kein Ausreißer, sondern erwartbar.** Drei unabhängige Linien zeigen dasselbe:
   - Prompt-Komponente netto negativ (AHE-Ablation, Sekundär −2,3)
   - Rollen-Prompts evolvieren zu leer (C2)
   - Gewinn ∝ behebbare Defektmasse (C14), Regeln bringen mit stärkeren Modellen kaum etwas (Cortex)
4. **Die Bitter-Lesson-Antwort zeichnet sich ab** (eigene Synthese, nicht einzeln belegt):
   - **Altern** werden Kompensationen von *Prozessfehlern* (Loops, Formatfehler, Tool-Missbrauch, Regeln). Sie werden vom nächsten Modell oder Training absorbiert (C9, C10, HarnessX invers, Cortex).
   - **Bleiben** dürften Komponenten, die *Information oder Umweltzugang* schaffen: Tools, Memory, Zustandsträger, Verifikation gegen die Umwelt.
5. **Org-Regime sind stark modellabhängig.** Die Spannweite liegt bei 57–61 pp, das beste Regime kippt je nach Modell (C3, C4). Das ist externe Evidenz für H-002, aber mit schwacher Statistik.
6. **Die "Harness schlägt Modell 7,8×"-Zahl ist kein allgemeiner Befund.** Sie entsteht aus einem Design mit absichtlich gleich starken Modellen (C6).

## Hypothesen-Kandidaten (nicht ins Register übernommen)

- **HK-C1 (Mechanismus- vs. Regel-Suche):** Bei gleichem Budget findet ein Optimierer, dessen Suchraum Org-*Mechanismen* enthält (Zustandsträger, Übernahme nach Frist, Belegpflicht, Abstimmungsrecht), größere und besser transferierende Gewinne als ein Optimierer über Prompt-Regeln.
  - Basis: AHE-Ablation, C14, E-014/E-018.
  - Test: E-013-Setup mit erweitertem Suchraum.
- **HK-C2 (Defektmasse):** Der Optimierer-Gewinn skaliert mit dem Anteil *behebbarer* Fehler der Baseline (Liegenlassen, Loops, Fehlmeldungen) und geht an der Decke gegen null.
  - Test: derselbe Optimierer bei 2–3 Knappheitsstufen von `phantom_stress`. Vorhersage: Gewinn ≈ k · (1 − Baseline) im behebbaren Anteil.
- **HK-C3 (HDA für uns):** Ein Teil jedes Optimierer-Gewinns ist Test-Time-Scaling.
  - Test: Kontrollarm "Baseline mit gleichem Token- oder Tick-Budget wie der Kandidat". Ein übernommener Kandidat muss auch diesen schlagen.
- **HK-C4 (Rollenkollaps):** In Teams aus demselben Modell evolviert ein Prompt-Optimierer Steuerungsrollen (Planner, Prüfer) zu leer oder wirkungslos, statt sie zu differenzieren.
  - Basis: C2. Verbindung zu H-015.
  - Test: rollenbezogene Prompt-Evolution mit einem Längen- und Einflussmaß pro Rolle.
- **HK-C5 (Alterung):** Bestätigte Mechanismen wie Frist-Übernahme (H-025) und Beleg-statt-Stimme (H-028) behalten ihren Effekt bei einem Modellwechsel (Haiku ↔ Sonnet ↔ Opus) eher als Normen-Prompts (E-012).
  - Das wäre eine direkte Bitter-Lesson-Messung im eigenen Testbed.
- **HK-C6 (Shortcut-Konventionen, zu H-006):** Ein Optimierer mit Ergebnis-Score findet häufiger Shortcut-Konventionen als einer, dessen Verifier den Mechanismus prüft. Beispiel für einen Shortcut: verabredete Labels statt echter Informationsweitergabe, analog C12.
  - Test: kontrafaktisches Mapping (C12) bzw. Neutralisierung (C1) auf übernommene Kandidaten anwenden.
- **HK-C7 (Modellabhängigkeit der Org-Optima):** Die Rangfolge unserer Regime (A/B/C, Quorum, Frist, Bürokratie) kippt zwischen Modellfamilien.
  - Basis: C3, C4. Das wäre ein direkter Test von H-002.

## Offene Prüfungen
- AHE-Ablationszahlen (Memory +5,6 / Tools +3,3 / Middleware +2,2 / Prompt −2,3) im PDF bestätigen. Bisher nur Sekundär.
- GEPA-Detail in "Multi-Agent Teams Hold Experts Back" im Volltext prüfen (bisher Snippet).
- Die AHE-Zitationsliste ist nur bis Platz 100 gesichtet (Semantic Scholar meldete HTTP 429). Weitere Multi-Agent-Treffer sind möglich.
- HarnessNet: Anhang E (globale vs. hierarchische Zahlen) nicht gelesen.
