# Recherche: Modell, Harness und Aufgabenschwierigkeit

Stand: 23.10.2026. Erstellt von einem Recherche-Agenten mit frischem Kontext. Das Experiment-Projekt wurde nicht gelesen. Die Quellen mit Typ und Prüfstatus stehen in `quellen.md`, hier werden sie mit Kurzschlüsseln in eckigen Klammern zitiert, z. B. [Q-HB].

Kennzeichnung der Belegstärke im Text:
- **PR**: Peer-Review (Konferenz oder Journal)
- **PP**: Preprint (arXiv, ohne Begutachtung oder nur Workshop)
- **LB**: Leaderboard
- **HS**: Herstellerangabe
- **BL**: Blog, technischer Bericht ohne Begutachtung, Forum
- **RP**: Repository
- **FW**: Fachwissen, in dieser Recherche nicht erneut im Original geprüft

Viele der wichtigsten Arbeiten zu Frage 2 und 5 sind Preprints aus dem Jahr 2026. Sie sind neu und noch nicht begutachtet, manche wurden schon nachträglich korrigiert. Ihre Zahlen sind deshalb vorläufig.

---

## 1. Die Benchmarks von „The Morpheus Tutorials“ (TheMorpheus407)

### Kurzantwort
Die Repositories enthalten **Endzustände der Arbeitsverzeichnisse**: eine Aufgabe, ein Lauf pro Modell. Sie enthalten **keine Bewertungen**, weder pro Teilaufgabe noch gesamt. Sie enthalten auch keine Laufprotokolle, Transkripte, Token- oder Kostenzahlen und keine Wiederholungen. Die Harness-Konfiguration wurde absichtlich entfernt.

Als Rohdaten für die Fragen (a) bis (c) taugen sie nur, wenn man **selbst bewertet**, also Artefakte prüft oder baut. Selbst dann bleibt die Aussagekraft gering:
- n = 1 Lauf pro Zelle,
- 6 Modelle bei den neueren Benchmarks,
- Harness und Hersteller sind vollständig miteinander vermengt.

Für (c) gibt es nur zwei Einzelpaare, für die keine Bewertung vorliegt.

### Befunde je Repository
Alles wurde im Original geprüft: geklont bzw. über die GitHub-API gelesen am 23.10.2026 [Q-M1 bis Q-M6].

| Repo | Aufgabe | Läufe | Harness-Information | Bewertung |
|---|---|---|---|---|
| `hogwarts-blender-benchmark` | Hogwarts samt Umgebung prozedural in Blender über den MCP-Server „blender-official“. SPEC etwa 9,7 KB in Abschnitten (Burg, Umgebung, Licht, Materialien, Handwerk, Ablauf, Abgaben). Prompt in einer Zeile. | 24 Ordner, je 1 Lauf. Juli bis Oktober 2026. | Nur in den Ordnernamen: `GLM-5.3-in-Cline` und `GLM-5.3-in-Kimi-Code`. Sonst keine Angabe. | Keine. Abgegeben werden `.blend` und 7 Renderbilder (4K-PNG), teils mit Build-Skripten. Die Referenzbilder sind aus urheberrechtlichen Gründen nicht enthalten, deshalb lässt sich die Ähnlichkeit zum Vorbild von außen nicht prüfen. |
| `morphcook` | Flutter-App nach SPEC (etwa 25 KB) | 32 Ordner. Die README nennt nur 7. | Ordnernamen: `GLM-5.3` und `GLM-5.3-in-Kimi-Code`. Dazu `qwen-3.8-27b`, `-128k` und `-256k` (opencode mit Ollama, Kontextfenster 64k, 128k und 256k). Im Ordner `-256k` liegt keine App. | Keine. `time.txt` (Wanduhrzeit) gibt es nur bei den 4 GPT-5.6-Varianten. Die SPEC-Fassungen unterscheiden sich zwischen den Läufen (4 verschiedene Hashwerte, 27 identisch). Nur der **erste Commit** pro Ordner ist der One-Shot, danach folgen menschliche Nachbesserungen, vor allem bei Fable 5. |
| `morphcook-cli-benchmark` | Dieselbe SPEC, 14 Coding-CLIs, Modell laut README konstant | Nur 3 von 14 veröffentlicht: Antigravity CLI, Claude Code, Codex CLI | **Welches Modell, steht nirgends.** Ausdrücklich ausgeschlossen sind Bewertungen, Ranglisten, Logs, Transkripte, Kosten, Token, Validierungsberichte und Harness-Code. | Keine |
| `morphdemo-benchmark` | Drei native Linux-Demos mit genau 65.536, 16.384 und 4.096 Byte | 6 Modelle, je 1 Lauf, 23.9. bis 14.10.2026 | `.claude/`, `.codex/`, `.cline/` und `opencode.json*` sind per `.gitignore` entfernt. | Keine. Die SPEC hat viele objektiv prüfbare Kriterien: Bytegröße, 50 bis 70 s Laufzeit, Escape, Wort „MORPH“, Audio, mindestens 3 Phasen. |
| `morphhealth-benchmark` | Android-App in Flutter mit CLI. SPEC auf Deutsch, Abschnitte P01 bis P12 mit aufzählbaren Einzelanforderungen, z. B. 13 Vitamine und 8 Mineralstoffe. | dieselben 6 Modelle, je 1 Lauf | wie oben entfernt | Keine. Selbstberichte der Modelle liegen vor (README, `docs/`, `check.sh`). |
| `morphrig-benchmark` | Charakter mit Rig, 96 benannten Animationen (`required_animations.csv`), Gesichtsrig und Weg Blender → Unreal → Linux | dieselben 6 Modelle, je 1 Lauf. Builds liegen als Release-Assets bei. | wie oben entfernt | Keine. Selbstberichte liegen vor: `known_issues.md`, `animation_manifest.json`, Validierungsberichte. |

**Woher das Harness kommt:** Der Autor schreibt in Issue #3 von `morphcook` sinngemäß, er nutze möglichst die hauseigenen CLIs der Hersteller, sonst meist opencode [Q-M7, RP/Forum, im Original gelesen]. Das ist keine systematische Angabe pro Lauf. Modell und Harness sind also **pro Hersteller vermengt**.

**Wo die Bewertung steht:** Bewertungen des Autors gibt es vermutlich nur in seinen YouTube-Videos. Gefunden habe ich keine. Das ist **nicht verifiziert**.

### Eignung für (a), (b) und (c)
- **(a) Schwierigkeit pro Teilaufgabe über Modelle hinweg:** Nicht direkt möglich, weil keine Bewertung pro Teilaufgabe vorliegt. Möglich wäre es nur mit einem eigenen Prüfschema. Kandidaten dafür sind die 96 Animations-IDs (MorphRig), die P-Anforderungen (MorphHealth) und die harten Kriterien von MorphDemo.
  - Bei 6 Modellen und 1 Lauf ist eine Schwierigkeitsschätzung sehr unsicher. Nach Rasch-Faustregeln braucht man ungefähr 30 „Personen“ für ±1 Logit (95 %) und ungefähr 100 für ±0,5 Logit [Q-LIN, siehe Frage 3].
  - Hogwarts und MorphCook haben mehr Modelle (24 bzw. 32). Dort sind die Bedingungen aber uneinheitlich: SPEC-Versionen, Datum, Harness, Kontextfenster.
  - Die Selbstberichte der Modelle sind **keine unabhängige Bewertung**.
- **(b) Scheitern verschiedene Modelle an denselben Teilaufgaben?** Grundsätzlich mit eigenem Prüfschema möglich. Bei 1 Lauf pro Modell lässt sich aber zufälliges Scheitern nicht von systematischem trennen. Die Fehlerübereinstimmung müsste für die unterschiedlichen Erfolgsraten korrigiert werden (siehe Frage 4).
- **(c) Dasselbe Modell in verschiedenen Harnesses:** Praktisch nicht möglich. Es gibt nur diese Fälle, jeweils mit n = 1:
  - GLM-5.3 in Cline gegen Kimi Code (Hogwarts),
  - GLM-5.3 gegen GLM-5.3 in Kimi Code (MorphCook),
  - Qwen-3.8-27B mit drei Kontextgrößen in opencode (MorphCook; das ist eine Konfigurationsvariation, kein anderes Harness),
  - 3 CLIs mit **unbekanntem** Modell (morphcook-cli).

  Zu keinem dieser Fälle gibt es eine Bewertung.
- **Wiederholungen pro Modell:** keine. Es gibt einen Ordner pro Modell, die READMEs sprechen von „single run“ bzw. „one-shot“.

### Offene Punkte
- Ob der Autor intern Bewertungen pro Kriterium führt, ließ sich nicht klären. Das Video-Material wurde nicht gefunden bzw. nicht geprüft.
- Welches Modell im CLI-Benchmark lief, ist unbekannt.
- Bei MorphCook muss man für One-Shot-Vergleiche die Git-Historie (erster Commit pro Ordner) auswerten. Der flache Klon zeigt den nachbearbeiteten Stand.

---

## 2. Öffentliche Vergleiche Modell × Harness

### Kurzantwort
Die Befunde widersprechen sich, und das liegt zu einem großen Teil am **Versuchsplan**. Wie groß der Anteil von Modell, Harness und Wechselwirkung ausfällt, hängt stark davon ab, **wie verschieden die gewählten Modelle und Harnesses sind**. Wählt man Modelle ähnlicher Stärke und stark verschiedene Harnesses, dominiert das Harness, und umgekehrt.

Wiederkehrende Muster:
1. Wechselwirkungen gibt es. Kein Harness ist für alle Modelle das beste, Rangfolgen kehren sich um.
2. Bei gleichem Modell liegen die Unterschiede oft im Bereich von etwa 0 bis 15 Prozentpunkten. In Extremfällen sind es mehr, z. B. bei generischen gegenüber spezialisierten Scaffolds.
3. Mehrere Quellen berichten, dass **schwächere oder offene Modelle empfindlicher auf das Harness reagieren** und dass der Harness-Unterschied mit stärkeren Modellgenerationen schrumpft. Das ist relevant für Frage 5, hat aber Vorbehalte (Boden- und Deckeneffekte, siehe dort).

### Wichtigste Belege
- **Terminal-Bench 2.0** [Q-TB, PP; Leaderboard: LB]
  - Aufbau: 89 Aufgaben, 6 Agenten × 16 Modelle, **mindestens 5 Läufe pro Kombination**, zusammen 32.155 Versuche.
  - Die Autoren folgern: „model selection is usually more important than agent scaffold“. Die Grafik pro Modell zeigt jeweils das *beste* Harness.
  - Herstellereigene CLIs liefen nur mit Modellen des eigenen Herstellers. Modell und Harness sind deshalb teilweise vermengt.
  - Als neutrale Vergleichsbasis dient Terminus 2.
  - Im Original gelesen (HTML, relevante Abschnitte).
- **HAL, Holistic Agent Leaderboard** [Q-HAL, PR ICLR 2026]
  - Umfang: 21.730 Rollouts, 9 Modelle, 9 Benchmarks.
  - Spezialisierte Scaffolds schlagen das generische in 9 von 12 Fällen (CORE-Bench Hard) bzw. 11 von 12 (SWE-bench Verified Mini).
  - Modell-abhängig: Claude-Modelle sind mit BrowserUse besser, OpenAI-Modelle mit SeeAct.
  - Wie oft pro Konfiguration wiederholt wurde, steht im gelesenen Teil nicht.
  - Logs auf Hugging Face (`agent-evals/hal_traces`).
- **„Just a wrapper?“** (Gundlach et al., auf Basis der HAL-Daten) [Q-GUN, BL]
  - Scaffold-Dummies erklären in einer Regression mehr als Modell-Dummies.
  - Etwa gleich viele „turbulente“ Effekte (Rangfolgen ändern sich) wie gleichmäßige.
  - GAIA: Kendall τ = 0,17 zwischen den Rangfolgen.
  - Vorbehalt: Alles ist relativ zum generischen HAL-Basis-Scaffold gemessen.
- **Exgentic / General Agent Evaluation** [Q-EXG, PP]
  - Aufbau: 5 Architekturen × 3 geschlossene Modelle × 6 Benchmarks.
  - Varianzanteile (η²): **Modell 27,8 %, Architektur 0,5 %, Wechselwirkung 5,4 %** (additive Zerlegung).
  - Zweifaktorielle ANOVA: Modell F(2,78) = 34,95; Agent F(4,78) = 0,16, p = 0,96.
  - Mit offenen Modellen wird der Architektureffekt signifikant: F(4,136) = 3,82, p = 0,006. Beispiel: dasselbe offene Modell auf τ²-Bench zwischen 0,83 und 0,00 je nach Architektur.
  - Innerhalb eines Modells schwanken die Ergebnisse um bis zu 12 Prozentpunkte.
- **„Stop Comparing LLM Agents Without Disclosing the Harness“** [Q-STOP, PP, Positionspapier]
  - Faktorielles Experiment: 3 Modelle ähnlicher Stärke × 3 *selbst entworfene* Harness-Stufen. 100 Aufgaben aus SWE-bench Verified, **2 Läufe pro Zelle**.
  - Varianz über Harnesses im Mittel 18,5 pp², über Modelle 2,4 pp², Verhältnis etwa 7,8×.
  - Rangfolgen kehren sich in 6 von 9 Vergleichen um.
  - Die Autoren schränken selbst ein: Das Ergebnis ist nicht universell, das Raster ist klein, η² ist verzerrt.
  - Das Ergebnis ist **konstruktionsbedingt**: Die Modelle wurden als „vergleichbar stark“ ausgewählt.
  - Zitierte Sekundärzahlen: Claude Opus 4.5 auf SWE-bench Pro mit SEAL-Scaffold 45,9 %, mit Claude Code 55,4 %. Epoch berichtet bis zu 11 bzw. 15 pp Scaffold-Effekt auf SWE-bench Verified. Diese Zahlen habe ich nicht im Original geprüft.
- **Harness-Bench** [Q-HB, PP, v2 vom Okt. 2026]
  - Aufbau: 7 native Harnesses × 10 Modelle, 300 Aufgaben mit Teilpunkten. **Jede Kombination wurde nur einmal ausgeführt.**
  - Kein Harness ist für alle Modelle das beste. Die Vollpunkt-Rate von GLM-5.3 schwankt um 13,5 pp.
  - Interaktionsresiduen nach dem additiven Modell nennen konkrete Paare, die schlechter abschneiden als erwartet (Kimi mit Claude Code, Qwen mit Goose).
  - Spearman-Korrelation zwischen mittlerer Modellstärke und Streuung über Harnesses: **−0,73** (stärkere Modelle schwanken weniger). Für die Vollpunkt-Rate liegt sie dagegen bei **+0,16**.
  - Die Residuen hängen von der Modellauswahl ab, das schreiben die Autoren selbst.
  - Versionswechsel: v1 (Mai 2026) hatte laut Sekundärquelle 106 Aufgaben, v2 hat 300.
- **„Harness or Model?“** [Q-HOM, PP]
  - Herstellereigenes Harness gegen neutrales, gleiches Modell, private und kontaminationskontrollierte Aufgaben, 80 Aufgaben × 2 Wiederholungen.
  - **Kein Durchschnittseffekt nachweisbar:** Opus 4.8 −1,25 pp [−10,0; +7,5], GPT-5.5 +1,25 pp [−4,4; +6,9].
  - Eine *post hoc* gefundene Wechselwirkung mit dem Aufgabentyp: Bei Repository-Aufgaben liegt das native Harness 9,0 pp zurück, bei Wettbewerbsaufgaben 23,7 pp vorn (Permutations-p = 0,003). Die Autoren kennzeichnen das ausdrücklich als nicht bestätigt.
  - Methodisch vorbildlich: Bootstrap auf Aufgabenebene, offengelegte Abweichungen vom Plan, Korrektur eines eigenen Telemetriefehlers.
- **„The Scaffold Effect“** [Q-SCA, PP]
  - 2 Modelle × 3 Open-Source-Harnesses auf 50 Aufgaben aus Terminal-Bench Pro.
  - Erfolgsunterschiede bei gleichem Modell 0 bis 8 pp, die Konfidenzintervalle schließen meist 0 ein.
  - Bis zu 40-fache Unterschiede in den Token pro gelöster Aufgabe.
  - „Fehler-Fingerabdrücke“ des Harness wiederholen sich über die Modelle hinweg.
- **„Behavioral Drivers of Coding Agent Success“** [Q-BD, PP]
  - Daten: 9.374 Trajektorien, 19 Agenten (8 Frameworks, 14 LLMs) auf SWE-bench Verified, aus öffentlichen Einreichungen, also ein natürliches Experiment.
  - Agenten mit gleichem LLM stimmen auf 85 bis 93 % der Aufgaben überein, Agenten mit gleichem Framework auf 47 bis 88 %.
  - Der Framework-Unterschied schrumpft über drei Claude-Generationen von 19,4 auf 3,8 auf 0,9 pp.
  - Vorbehalt: Es ist **rohe Übereinstimmung, nicht zufallskorrigiert**. Sie steigt mechanisch, wenn beide Agenten hohe Erfolgsraten haben (siehe Frage 4).
- **Agent Psychometrics** [Q-AP, PP, ICLR-Workshop]
  - IRT mit der Fähigkeit als **Summe θ_LLM + θ_Scaffold auf der Logit-Skala**.
  - Die additive Form schnitt bei der Kreuzvalidierung am besten ab, auch besser als eine Form mit modellspezifischer Harness-Empfindlichkeit.
  - Die Autoren warnen: Die Unabhängigkeit könnte verschwinden, wenn Modelle zusammen mit ihren Scaffolds trainiert werden.
- **Weitere:**
  - Cross-Component Interference [Q-CCI, PP]: Kombinationen von Komponenten, die bei 8B schaden, helfen bei 70B. Die Wirkung hängt also von der Modellgröße ab.
  - Lewis [Q-LEW, PP]: Ein Eingriff in das Kontextmanagement wirkt stark bei engem Kontextfenster und kaum bei weitem.
  - Double Measurement Confound [Q-DMC, PP]: Auf τ-bench verschiebt das Scaffold die Belohnung um bis zu 0,267, und Rangfolgen kippen.

### Vorbehalte
- **Leaderboards sind Beobachtungsdaten:** Prompts, Versionen, Budgets und Ingenieursaufwand unterscheiden sich gleichzeitig [Q-STOP, Q-SURV].
- **Herstellerzahlen** stammen oft aus dem jeweils besten eigenen Harness.
- **Kontamination:** Öffentliche Benchmarks wie SWE-bench liegen möglicherweise in den Trainingsdaten. Q-HOM nutzt deshalb private Aufgaben.
- **Wenige Läufe:** Viele Studien haben nur 1 bis 2 Läufe pro Zelle. Dann ist die Wechselwirkung kaum von Rauschen zu trennen.
- **Varianzanteile sind abhängig vom Design:** Sie hängen davon ab, welche Modelle und Harnesses einbezogen werden, und sind keine Naturkonstanten [Q-HB, Q-EXG].

### Offene Punkte
- Es gibt keine Studie mit großem, randomisiertem und wiederholtem Faktorplan, die Modelle über die ganze Fähigkeitsspanne einschließt.
- Die Daten auf Versuchsebene von Terminal-Bench (mindestens 5 Läufe pro Zelle) wären dafür geeignet. Ob sie öffentlich verfügbar sind, habe ich nicht geprüft.
- `SWE-bench/experiments` enthält Ergebnisse pro Instanz für 182 Verified-Einreichungen. Das ist öffentlich und geprüft, aber ohne Wiederholungen.

---

## 3. Schwierigkeit von Aufgaben messen (IRT und Alternativen)

### Kurzantwort
IRT ist in der LLM-Evaluation etabliert. Typische Verfahren:
- Rasch (1PL) bzw. 2PL auf binären Erfolgsdaten, Modelle als „Personen“,
- Anwendungen: Testverkürzung, adaptives Testen, Schwierigkeitsvorhersage aus Aufgabenmerkmalen.

Die großen Arbeiten nutzen **Hunderte bis Tausende Modelle** (Open LLM Leaderboard). Agenten-Studien kommen mit wenigen Dutzend Agenten aus, wenn es viele Aufgaben und Wiederholungen gibt. Mit sehr wenigen Modellen sind die Schwierigkeitsschätzungen grob.

Der gefährlichste Fallstrick für Neos Fragestellung ist **Zirkularität**, also „double dipping“: Wer die Schwierigkeit aus denselben verrauschten Daten schätzt, mit denen danach ein Effekt in Abhängigkeit von dieser Schwierigkeit gemessen wird, erzeugt durch Regression zur Mitte Scheineffekte.

### Vorgehen (Belege)
- **Grundmodell:** Rasch-Modell P(Erfolg) = σ(θ_Modell − β_Aufgabe). Für Agenten erweitert zu σ(θ_LLM + θ_Scaffold − β) [Q-AP]. Bei Wiederholungen werden die Versuche als Bernoulli-Beobachtungen gezählt, die AUC bleibt dabei vergleichbar [Q-AP].
- **Anwendungen:**
  - Testverkürzung: tinyBenchmarks, etwa 100 Items für ungefähr 2 % Fehler [Q-TINY, PR ICML 2024]; metabench mit Daten von über 5.000 LLMs [Q-META, PR ICLR 2025].
  - Adaptives Testen: Fluid Benchmarking [Q-FLUID, PR COLM 2025].
  - Vergleich von Testsätzen: Vania et al. mit nur **18 Modellen** und 29 Datensätzen [Q-VAN, PR ACL 2021].
  - Schwierigkeit aus *Aufgabenmerkmalen* vorhersagen, ohne Antwortdaten: Truong et al. 2025 (über [Q-AP]) und Agent Psychometrics [Q-AP].
- **Externe Schwierigkeitsmaße als Alternative zu IRT:**
  - Menschliche Bearbeitungszeit, z. B. METR „time horizon“ [Q-METR, PP].
  - Von Menschen geschätzte Schwierigkeit. In Terminal-Bench korreliert sie mit der empirischen Schwierigkeit nur mit r = 0,436 [Q-TB].
  - Patch-Komplexität: ρ = −0,38, und gerade bei „einfachen“ Patches gibt es nie gelöste Aufgaben [Q-BD].
- **Mindestdatenmenge (Rasch, Psychometrie):** Linacre 1994 [Q-LIN, Fachnewsletter] gibt als Stichprobengröße für stabile Item-Kalibrierung an:

  | Genauigkeit | Konfidenz | Personen |
  |---|---|---|
  | ±1 Logit | 95 % | etwa 16 bis 36, Richtwert 30 |
  | ±1 Logit | 99 % | etwa 27 bis 61, Richtwert 50 |
  | ±0,5 Logit | 95 % | etwa 64 bis 144, Richtwert 100 |
  | ±0,5 Logit | 99 % | etwa 108 bis 243, Richtwert 150 |

  Übertragen auf LLMs: Bei 6 Modellen und 1 Lauf ist die Schwierigkeit pro Aufgabe nur grob ordinal schätzbar. Wiederholte Läufe desselben Modells sind **keine unabhängigen Personen**. Sie verbessern die Schätzung von p(Modell, Aufgabe), aber nicht die Verallgemeinerung über Modelle.

### Fallstricke
1. **Zirkularität bzw. Regression zur Mitte.** Ein Beispiel: Man ordnet Aufgaben nach dem Erfolg *in der Basisbedingung* in Klassen und vergleicht dann Behandlung gegen Basis pro Klasse. Dann zeigt sich auch ohne jeden echten Effekt, dass „schwere“ Aufgaben sich verbessern und „leichte“ verschlechtern.
   - Grundlagen: Kriegeskorte et al. 2009 [Q-KRI, PR]. Bland & Altman 1995 [Q-BA, PR]: Wer die Differenz gegen *eine* der beiden Messungen aufträgt, sieht immer einen Zusammenhang, auch wenn keiner existiert. Gegen den *Mittelwert* beider Messungen aufgetragen passiert das nicht, solange die Varianzen gleich sind.
   - Für LLMs dokumentiert: Cacioli 2026 [Q-RCI, PP] findet auf Item-Ebene, dass Items mit niedriger Genauigkeit sich zwischen Modellversionen „verbessern“ und Items mit hoher Genauigkeit sich „verschlechtern“. Regression zur Mitte erklärt dort einen Teil.
   - Für LLMs dokumentiert: Järviniemi et al. [Q-PROP, PP] erwarten Regression zur Mitte, wenn man iterativ auf eine Bedingung optimiert, und ergreifen ausdrücklich Gegenmaßnahmen: zufällige Konfigurationen und zufällige Modelle beim Iterieren.
2. **Wie man Zirkularität vermeidet** (Standardverfahren, teils FW):
   - Schwierigkeit aus **unabhängigen Daten** schätzen: andere Modelle, nicht die untersuchten. Möglich auch mit Leave-one-model-out: Für jedes Modell m wird β aus allen anderen Modellen geschätzt.
   - Bei mehreren Wiederholungen: **Kreuzanpassung (cross-fitting)**. Die Läufe werden geteilt, Hälfte A schätzt die Schwierigkeit, Hälfte B den Effekt, danach werden die Rollen getauscht.
   - Die Schwierigkeit **symmetrisch aus beiden Bedingungen** schätzen (Mittelwert, analog zu Bland-Altman) und nicht aus der Basisbedingung. Das genügt aber nur, wenn die Varianzen gleich sind.
   - **Externe Kovariaten** nutzen: menschliche Zeit, Aufgabenmerkmale, vor dem Experiment festgelegte Schwierigkeitsklassen.
   - **Nullsimulation:** Parametrischer Bootstrap aus einem Modell *ohne* Wechselwirkung. Damit prüft man, welches Muster die Analyse rein mechanisch erzeugt.
   - **Präregistrierung** der Klasseneinteilung, um Partitionen nach Datenansicht zu vermeiden. Q-HOM zeigt genau dieses Problem und legt es offen.
3. **Wahl der Skala.** Effekte, die auf der Logit-Skala additiv sind, sind auf der Prozentskala am größten bei p ≈ 0,5 und verschwinden an Boden und Decke. Siehe Frage 5.
4. **Mehrdimensionalität bzw. Differential Item Functioning:** Eine gemeinsame Schwierigkeitsskala setzt voraus, dass die Rangfolge der Aufgaben für alle Modelle gleich ist. Mixture-IRT stellt diese Annahme in Frage [Q-MIRT, Workshop, nur Abstract]. Das lässt sich durch Modellvergleich prüfen (1D gegen 2D bzw. Mixture-IRT).
5. **Weitere Fallstricke:**
   - Boden- und Deckeneffekte: Aufgaben, die nie oder immer gelöst werden, tragen keine Information.
   - Bewertungsfehler und mehrdeutige Items.
   - Zufälliger Entscheidungsweg bei T > 0 und Varianz zwischen Läufen [Q-RCI].
   - Teilpunkte müssen binarisiert oder mit Modellen für mehrstufige Antworten (polytom) ausgewertet werden.

### Offene Punkte
- Ich habe keine Arbeit gefunden, die für Agenten-Benchmarks die Zirkularität „Schwierigkeit gegen Harness-Effekt“ ausdrücklich durchrechnet. Die Gegenmaßnahmen oben sind übertragenes Standardwissen.
- Belastbare Regeln für Mindestgrößen speziell für LLM-Agenten fehlen.

---

## 4. Fehlerkorrelation zwischen LLMs

### Kurzantwort
Ja, Modelle scheitern zu einem erheblichen Teil an denselben Aufgaben, und zwar **stärker, je fähiger sie sind**. Das gilt auch über Familien und Anbieter hinweg. Gemeinsame Architektur und gemeinsamer Anbieter erhöhen die Korrelation zusätzlich.

Für Agenten gilt nach einer Studie: Gleiches LLM erzeugt mehr Übereinstimmung als gleiches Framework.

Konsequenz: **Redundanz durch mehrere Modelle ist weniger wert, als die Unabhängigkeitsannahme verspricht.** Sie hilft am meisten bei Modellen mit unterschiedlichen Fehlermengen. Ein Orakel, das die richtige Lösung auswählt, ist dabei eine obere Schranke, keine erreichbare Leistung.

### Belege
- **Kim et al. 2025** [Q-KIM, PR ICML 2025]
  - Über 350 LLMs. Auf einem Leaderboard-Datensatz stimmen Modelle in 60 % der Fälle überein, wenn beide falsch liegen.
  - Größere und genauere Modelle haben stark korrelierte Fehler, auch über Architekturen und Anbieter hinweg.
  - Folgen für LLM-as-Judge und für Monokultur-Effekte, etwa beim Bewerber-Screening.
- **Goel et al. 2025, „Great Models Think Alike“** [Q-CAPA, PP; nach meinem Wissen ICML 2025, nicht geprüft]
  - Einführung von CAPA, einem zufallskorrigierten probabilistischen Übereinstimmungsmaß für Fehler.
  - Fehler werden mit steigender Fähigkeit ähnlicher. Richter-Modelle bevorzugen ähnliche Modelle.
- **Fehlerkonsistenz nach Geirhos et al. 2020** [Q-GEI, PR NeurIPS]
  - Cohens κ auf Trial-Ebene. Die erwartete Übereinstimmung unter Unabhängigkeit ist c_exp = p₁p₂ + (1−p₁)(1−p₂), so wird für unterschiedliche Genauigkeit korrigiert.
  - Vorbehalt der Autoren selbst: κ ist durch die Genauigkeiten begrenzt und nicht völlig unabhängig von ihnen.
  - Klein et al. 2025 [Q-KLE, PP] zeigen: Die Werte sind ohne Konfidenzintervalle oft nicht belastbar. Sie liefern Bootstrap-Intervalle, eine Power-Planung und ein „Kopier-Wahrscheinlichkeits“-Modell. Viele berichtete Unterschiede zwischen Modellen sind nicht signifikant.
- **Agenten**
  - Mehtiyev & Assunção [Q-BD]:
    - Gleiches LLM: 85 bis 93 % Übereinstimmung pro Aufgabe. Gleiches Framework: 47 bis 88 %.
    - 55 von 500 Aufgaben (11 %) wurden von keinem Agenten gelöst.
    - 12 dieser nie gelösten Aufgaben haben einfache Patches.
    - Aber: rohe Übereinstimmung ohne Zufallskorrektur.
  - DEI [Q-DEI, PP]: Ein Ensemble mit Orakel-Auswahl löst auf SWE-bench Lite deutlich mehr als der beste Einzelagent (laut Sekundärquelle 54,3 % gegenüber durchschnittlich 26,6 %). Die realistische Auswahl ohne Orakel bringt weniger (27,3 % → 34,3 %).
  - Terminal-Bench: Einige Aufgaben löst kein Modell und kein Agent [Q-TB].

### Maße, die unterschiedliche Stärke berücksichtigen
- **Cohens κ bzw. Fehlerkonsistenz** [Q-GEI], **CAPA** [Q-CAPA].
- **Klassische Diversitätsmaße aus der Ensemble-Literatur** (FW, Kuncheva & Whitaker 2003): Q-Statistik, Double-Fault (Anteil gemeinsamer Fehler im Verhältnis zum Erwartungswert bei Unabhängigkeit), Disagreement.
- **Im IRT-Rahmen:** Residualkorrelation nach Herausrechnen von θ und β. Gemeinsames Scheitern, das über die gemeinsame Schwierigkeit hinausgeht, zeigt sich als lokale Abhängigkeit, z. B. als Q3-Statistik nach Yen (FW).
  - Das trennt zwei Fälle: „alle scheitern, weil die Aufgabe schwer ist“ und „bestimmte Modelle scheitern gemeinsam“.
  - Zentral, weil rohe Fehlerüberlappung immer schon durch die Schwierigkeitsverteilung entsteht.
- **Bei Wiederholungen:** zuerst p(Modell, Aufgabe) schätzen, dann die Korrelation dieser Wahrscheinlichkeiten über Aufgaben berechnen, mit Korrektur für die Messunsicherheit (Attenuation).

### Folgen für Redundanz
- Die Wahrscheinlichkeit, dass alle k Modelle scheitern, liegt deutlich über dem Produkt der Einzelfehlerraten. Wie stark, hängt von der Fehlerkorrelation ab.
- Bei **richtigen Antworten mit Verifikator** (Tests) bringt Diversität mehr als bei Mehrheitsentscheid oder LLM-Richter, denn die Richter teilen die Fehler [Q-KIM, Q-CAPA].
- Mehrere Modelle derselben Familie bringen am wenigsten.

### Offene Punkte
- Für Agenten gibt es kaum zufallskorrigierte Analysen der Fehlerkorrelation über Modelle *und* Harnesses mit Wiederholungen.
- Ob die Korrelation zunimmt, weil die Modelle sich angleichen, oder weil sie beide sehr gut sind (Deckeneffekt), ist nicht sauber getrennt. Gerade dafür braucht man κ bzw. CAPA statt roher Übereinstimmung.

---

## 5. Methodik: Hängt ein Harness-Effekt von der Nähe zur Fähigkeitsgrenze ab?

### Kurzantwort
Das Prüfmodell sollte ein **gemischtes logistisches Modell bzw. eine erklärende IRT** sein: Erfolg ~ Harness × (θ_m − β_j), mit zufälligen Effekten für Aufgabe und Modell. Die Schwierigkeit β_j muss **unabhängig** von den Daten geschätzt werden, an denen man den Harness-Effekt misst.

Entscheidend ist die **Vorfrage nach der Skala**. Ein auf der Logit-Skala *konstanter* Harness-Effekt erzeugt auf der Prozentskala automatisch das Muster „wirkt am stärksten nahe der Grenze (p ≈ 0,5), kaum bei sehr leichten oder sehr schweren Aufgaben“. Das ist eine mathematische Folge der logistischen Funktion, keine besondere Wechselwirkung.

Eine echte Abhängigkeit von der Grenznähe muss also **über diese Erwartung hinausgehen**. Sie zeigt sich als von null verschiedener Interaktionsterm auf der Logit-Skala oder als Abweichung von einer Nullsimulation.

### Vorschlag für ein sauberes Design
1. **Vollständig gekreuzter Faktorplan:** Modell × Harness-Faktor × Aufgabe, **mindestens 3 bis 5 Wiederholungen pro Zelle**. Terminal-Bench nutzt mindestens 5, Q-HOM 2 und plant 3 für eine Replikation. Reihenfolge und Zeitpunkt der Läufe randomisieren, damit Drift bei API-Modellen nicht mit dem Faktor zusammenfällt [Q-HAL: Anbieter tauschen Gewichte].
2. **Schwierigkeit unabhängig schätzen**, mit einer der folgenden Optionen:
   - aus einem separaten Datensatz, z. B. andere Modelle, eine Basisbedingung mit eigenen Wiederholungen oder öffentliche Leaderboard-Daten,
   - per Kreuzanpassung über geteilte Wiederholungen,
   - über externe Merkmale: menschliche Zeit oder vorab festgelegte Klassen.

   Optional zwei Varianten vergleichen: β gemeinsam für alle Modelle (Annahme einer gemeinsamen Skala) gegen modellspezifische Grenznähe p̂_mj aus den Hold-out-Wiederholungen.
3. **Modell (FW):**

   logit P(y_mjhr = 1) = θ_m − β_j + γ_h + δ_h·(θ_m − β_j) + u_mh + v_jh

   - δ_h ist die interessierende Wechselwirkung „Wirkung hängt von der Grenznähe ab“.
   - u_mh erfasst die modellspezifische Harness-Passung (Kompatibilität).
   - v_jh erfasst die aufgabenspezifische Harness-Wirkung.
   - Ergänzend die Kurven auf der Prozentskala angeben.
4. **Inferenz:**
   - Bootstrap bzw. Permutation auf Aufgabenebene, mit Clustern nach Aufgabe [Q-HOM].
   - Vorab registrierte primäre Tests und FDR-Korrektur.
   - Parametrische Nullsimulation aus dem Modell mit δ = 0, um mechanische Muster zu kalibrieren.
5. **Power:** Wechselwirkungen brauchen ein Vielfaches der Stichprobe von Haupteffekten (FW, Faustregel: etwa 4× für eine gleich große Interaktion). Q-HOM zeigt, dass schon Haupteffekte von 8 bis 12 pp mit 80 Aufgaben × 2 Wiederholungen nur knapp nachweisbar sind.

### Konkurrierende Erklärungen und wie man sie unterscheidet

| Erklärung | Vorhersage | Unterscheidung |
|---|---|---|
| **Artefakt der Skala bzw. Boden und Decke** | Prozent-Effekt am größten bei p ≈ 0,5, Logit-Effekt konstant | Modell auf Logit-Skala, δ_h testen, Nullsimulation |
| **Regression zur Mitte bzw. Zirkularität** | „Hilft bei schweren, schadet bei leichten Aufgaben“, auch ohne echten Effekt | Unabhängige oder kreuzangepasste Schwierigkeit, Bland-Altman-Logik, Nullsimulation [Q-KRI, Q-BA, Q-RCI] |
| **Modellspezifische Strategien bzw. Harness-Passung statt gemeinsamer Skala** | Die Wirkung hängt am *Modell* (u_mh), nicht an der Grenznähe. Herstellereigene Harnesses passen zum eigenen Modell [Q-TB, Q-GUN]. | Varianz von u_mh gegen δ_h schätzen. Prüfen, ob die Grenznähe die Wirkung *innerhalb* eines Modells über Aufgaben vorhersagt. Gegenprobe: Harness-Wechsel ohne Herstellerbezug. |
| **Mehrdimensionalität bzw. DIF** (Aufgaben sind für verschiedene Modelle aus verschiedenen Gründen schwer) | Ein 1D-Rasch-Modell passt schlecht, die Schwierigkeitsrangfolgen unterscheiden sich zwischen Modellen | 2D- oder Mixture-IRT gegen 1D vergleichen (Hold-out-Likelihood), Residualkorrelationen [Q-MIRT] |
| **Aufgabentyp als Störvariable** | Die Schwierigkeit korreliert mit der Aufgabenart, und das Harness wirkt eigentlich auf die Art. Beispiel Q-HOM: Repository- gegen Wettbewerbsaufgaben mit umgekehrtem Vorzeichen. | Typ als Kovariate bzw. Schichtung, Wirkung der Grenznähe *innerhalb* eines Typs |
| **Budget und Abbruch** | Schwere Aufgaben stoßen an Zeit-, Turn- oder Kontextgrenzen. Das Harness verändert diese Grenzen, z. B. durch Kompaktierung [Q-LEW, Q-HB]. | Abbruchgründe protokollieren, Budget als eigenen Faktor variieren oder konstant halten, Ergebnis auch bei gekappten Läufen bewerten [Q-HOM: 22 von 81 gekappten Läufen hatten einen bestandenen Patch] |
| **Gleichmäßiger Effekt („rising tide“) gegen ungleichmäßigen („turbulent“)** | Gleiche Wirkung für alle gegen Umsortierung | Ränge und Kendall τ über Bedingungen [Q-GUN] |
| **Modellstärke statt Aufgabengrenze** (der Befund „schwache Modelle reagieren empfindlicher“) | Die Empfindlichkeit hängt an θ_m und nicht an θ_m − β_j | Beide Terme getrennt ins Modell aufnehmen. Dafür braucht man Aufgaben über die ganze Schwierigkeitsspanne für jedes Modell. |
| **Zufällige Entscheidungswege** | Aufgaben nahe der Grenze haben p ≈ 0,5 und damit maximale Bernoulli-Varianz, also mehr „Effekte“ durch Zufall | Wiederholungen, Modellierung auf Ebene der Wahrscheinlichkeit statt einzelner Läufe |

### Was die Literatur dazu nahelegt (vorläufig)
- **Additiv auf Logit-Ebene passt gut:** Agent Psychometrics findet für SWE-bench-artige Daten, dass die additive Logit-Zerlegung LLM + Scaffold ohne Interaktionsterm am besten vorhersagt [Q-AP]. Daraus folgt bereits das Muster „Prozent-Effekt am größten nahe der Grenze“.
- **Stärkere Modelle schwanken weniger über Harnesses:** Belege sind Q-HB (ρ = −0,73 für den Mittelwert, aber +0,16 für die Vollpunkt-Rate), Q-EXG (offene Modelle empfindlicher), Q-BD (Framework-Unterschied schrumpft mit der Generation) und Q-CCI (Wirkung hängt von der Modellgröße ab). Das ist mit „Grenznähe“ *und* mit Boden- oder Deckeneffekten vereinbar und wurde in keiner dieser Arbeiten auf der Logit-Skala getrennt.
- **Harness-Effekte sind bedingt:** Sie hängen ab von Aufgabentyp [Q-HOM], Kontextregime [Q-LEW] und Zielmaß [Q-HB].

### Offene Punkte
Ich habe keine Studie gefunden, die genau diese Hypothese (Harness-Effekt × Grenznähe) mit unabhängig geschätzter Schwierigkeit und Wiederholungen prüft.

---

## 6. Langer Kontext: Länge gegen inhaltliche Richtung

### Kurzantwort
Die Leistung sinkt mit wachsendem Kontext, auch weit unterhalb der nominalen Fenstergröße. Mehrere Studien trennen inzwischen ausdrücklich Faktoren:
- **reine Länge** (selbst mit Leerzeichen-Füllung oder maskierten Tokens),
- **Position** (Lost in the Middle, abhängig vom relativen Füllgrad),
- **inhaltliche Nähe bzw. Ablenker** (Distraktoren),
- **inhaltliche Richtung**: eigene frühere Fehler, Bewertungstendenz der Vorgeschichte, Nutzerdruck, angesammelte Überzeugungen.

Ein Befund ist besonders wichtig für Neos Frage: Bei Richtungseffekten zählt oft **der Inhalt, nicht die Länge**. AMEL findet, dass 5 und 50 voreingenommene Turns dieselbe Verschiebung erzeugen. Bei Sinha et al. verschlechtert ein höherer Anteil eigener Fehler in der Vorgeschichte die Genauigkeit bei gleicher Länge.

### Belege, nach Art der Trennung geordnet

**Länge isoliert**
- Du et al. [Q-DU, PR Findings EMNLP 2025]: Bei perfektem Abruf fällt die Leistung um 13,9 bis 85 %. Das gilt auch mit Leerzeichen statt Text, mit maskierten irrelevanten Tokens und mit der Evidenz direkt vor der Frage.
- Chroma „Context Rot“ [Q-ROT, BL bzw. technischer Bericht]:
  - 18 Modelle. Nadel und Frage bleiben fest, nur die Füllmenge wächst.
  - Zusätzlich variiert: Ähnlichkeit zwischen Nadel und Frage, Zahl der Distraktoren (0, 1 oder 4), Kohärenz des Heuhaufens. Überraschend: Gemischte Heuhaufen schneiden besser ab.
  - LongMemEval fokussiert (etwa 300 Token) gegen voll (etwa 113k Token).
  - Die Autoren räumen ein, dass Länge und Schwierigkeit nicht überall getrennt sind.

**Position**
- Liu et al. [Q-LIM, PR TACL]: Lost in the Middle.
- Veseli et al. [Q-POS, PP]: Der Effekt ist am stärksten bis etwa 50 % des Kontextfensters. Darüber dominiert die Nähe zum Ende.

**Inhalt bzw. Abruf**
- NoLiMa [Q-NOLIMA, PR ICML 2025]: Ohne wörtliche Übereinstimmung zwischen Frage und Nadel fallen 11 von 13 Modellen bei 32k unter 50 % ihres Werts bei kurzem Kontext.

**Richtung des Inhalts bei kontrollierter Länge**
- Sinha et al. [Q-SELF, PR ICLR 2026]:
  - Die Fehlerrate in der Vorgeschichte wird kontrafaktisch manipuliert. Eine vollständig korrigierte Vorgeschichte misst den reinen Langkontext-Effekt, injizierte Fehler messen die *Selbstkonditionierung*.
  - Beide Effekte existieren.
  - Größere Modelle beheben den Längeneffekt weitgehend, die Selbstkonditionierung aber nicht.
  - „Thinking“-Modelle zeigen keine Selbstkonditionierung.
  - Das Entfernen der Vorgeschichte (Kontext-Engineering) hilft.
- AMEL [Q-AMEL, PP]:
  - Aufbau: 12 Modelle, 84.088 Aufrufe. Die Polarität der Vorgeschichte (positiv, negativ oder neutral) wird mit der Länge (5 bis 50 Turns) gekreuzt.
  - Verschiebung in Richtung der Polarität: d = −0,17. Bei unsicheren Items stärker: d = −0,36.
  - **Kein Längeneffekt** (|r| < 0,01), auch kein Positionseffekt. Negative Vorgeschichten wirken 1,52× stärker.
  - In der neutralen Bedingung gibt es eine kleine, signifikante Drift mit der Länge.
  - Eine Arbeit mit einem Autor.
- Laban et al. [Q-LOST, PP]:
  - Dieselben Informationen, verteilt über mehrere Turns („sharded“), gegen gebündelt in einer Nachricht („concat“). So wird die Struktur bei gleichem Inhalt getrennt.
  - Im Mittel −39 % über mehrere Turns, vor allem durch höhere Unzuverlässigkeit.
  - Frühe falsche Annahmen werden beibehalten, ein Ankereffekt der eigenen Zwischenlösungen.
- SYCON-Bench [Q-SYC, PR Findings EMNLP 2025]:
  - Anhaltender Nutzerdruck über mehrere Turns, 17 Modelle.
  - Alignment-Tuning verstärkt Zustimmungstendenz. Skalierung und Reasoning verringern sie.
  - Perspektive in der dritten Person senkt sie um bis zu 63,8 %.
- Geng et al. [Q-BELIEF, PP]:
  - Angesammelter Kontext durch Gespräche oder Lektüre verschiebt geäußerte „Überzeugungen“: GPT-5 um 54,7 % nach 10 Runden, Grok 4 um 27,2 % nach dem Lesen gegnerischer Texte.
  - Die Verschiebung zeigt sich auch in der Werkzeugwahl, also bei Agenten.

**Agenten bzw. Harness**
- Lewis [Q-LEW]: Ältere Werkzeugausgaben zu kürzen verdoppelt ungefähr die Fail-to-Pass-Rate bei engem Fenster (20k Token) und wirkt kaum bei weitem Fenster.
- Harness-Bench [Q-HB]: Kompaktierung ersetzte Werkzeugergebnisse, bevor das Modell sie überhaupt gesehen hatte. Belegt in 38 von 237 untersuchten Läufen.
- Cross-Context Review [Q-CCR, PP]: Eine Überprüfung in frischer Sitzung findet mehr injizierte Fehler als eine zweite Überprüfung in derselben Sitzung. Die Vorteile gegenüber anderen Bedingungen sind über alle Läufe hinweg nicht signifikant (v2 wurde korrigiert).
- MorphCook [Q-M2]: Qwen-3.8-27B mit 64k, 128k und 256k Kontext ist ein anekdotischer Einzelfall, n = 1 und unbewertet.

### Vorbehalte
- Viele Studien nutzen synthetische Aufgaben, etwa Nadel im Heuhaufen oder Schlüssel-Wert-Abfragen. Die Übertragbarkeit auf Agenten mit Werkzeugausgaben ist unklar.
- Die Effekte unterscheiden sich stark zwischen Modellen und Modellgenerationen. Ältere Befunde wie Lost in the Middle lassen sich nicht überall reproduzieren [Q-POS].
- Wirkungen von Richtung und Inhalt sind oft klein pro Item (AMEL: d ≈ 0,17), wachsen aber bei unsicheren Items.

### Offene Punkte
- Ein vollständiger Faktorplan **Länge × Richtung × Aufgabenschwierigkeit** für *Agenten* fehlt. AMEL kommt dem nur für Bewertungsaufgaben nahe.
- Offen ist auch, ob Richtungseffekte wie Selbstkonditionierung bei Aufgaben nahe der Fähigkeitsgrenze stärker sind. AMEL deutet das an: stärker bei unsicheren Items.

---

## Querschnitt: Was folgt für die Planung einer Analyse

1. **Bewertungen selbst erheben:** Die Morpheus-Rohdaten liefern weder Bewertungen pro Teilaufgabe noch Wiederholungen noch eine saubere Harness-Variation. Wer sie nutzen will, muss selbst ein Prüfschema anlegen. Dann taugen sie höchstens für Hypothesen, nicht für Tests. Für Tests besser geeignet: öffentliche Daten mit Ergebnissen pro Aufgabe und Wiederholungen (Terminal-Bench, HAL-Traces, SWE-bench/experiments) oder ein eigener Faktorplan.
2. **Anteile hängen vom Design ab:** „Modell gegen Harness“ ist keine feste Zahl. Man muss die Auswahl der Modelle und Harnesses begründen und das Ergebnis nur für diesen Ausschnitt formulieren.
3. **Skala vorab festlegen:** Vor der Analyse entscheiden, ob Wechselwirkungen auf der Logit- oder der Prozentskala gemeint sind. Ein additives Logit-Modell erzeugt Grenznähe-Muster in Prozent von selbst.
4. **Schwierigkeit und Effekt nie aus denselben Läufen schätzen:** Kreuzanpassung, Leave-one-model-out oder externe Schwierigkeit verwenden, plus Nullsimulation.
5. **Fehlerüberlappung zufallskorrigieren** (κ oder CAPA, mit Konfidenzintervallen) und gegen das IRT-Basismodell prüfen. Rohe Übereinstimmung täuscht.
6. **Kontext faktoriell planen:** Länge mit neutraler Füllung gegen Richtung bei gleicher Länge kreuzen. Vorbilder: Q-SELF, Q-AMEL, Q-LOST (concat gegen sharded), Q-DU.
