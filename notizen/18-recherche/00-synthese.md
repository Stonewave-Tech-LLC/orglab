# Recherche nach dem Cutoff: Synthese (Cluster A–F)

**Stand:** 22.10.2026 · Schritt 2 zu `notizen/17`.

**Vorgehen:**
- Sechs Recherche-Agenten, einer pro Cluster: A–D parallel, danach E und F.
- Ein unabhängiger Prüf-Agent hat 15 tragende Behauptungen aus A–D im Original gegengeprüft (`verifikation.md`). Ergebnis: Alle Quellen existieren und keine Zahl ist erfunden. Zwei Spannen waren aber selektiv zitiert (siehe unten).
- E und F sind **nicht** gegengeprüft.

**Einzeldateien:** `cluster-A.md` … `cluster-F.md`, `verifikation.md`.

**Vorbehalte:**
- Fast alles sind Preprints, oft von Einzelautor:innen.
- "Volltext" heißt hier: über WebFetch gelesen, also über die Zusammenfassung eines Hilfsmodells, nicht selbst im PDF.
- Gesucht, gelesen und geprüft haben ausschließlich Claude-Agenten. Die Kritiker-Unabhängigkeit (CLAUDE.md, Methodik 6) bleibt offen.
- Die Cluster-Dateien nennen das geplante Prüfer-Panel-Experiment "E-017". Diese ID ist noch nicht vergeben.

---

## 1. Wie stark korrelieren Fehler zwischen LLMs?

**Stark, und zwar auch über Modellfamilien hinweg.**
- **Kohli 2605.29800 (geprüft):** 9 Judges aus 7 Familien ergeben auf den NLI-Sets nur 2,2–2,5 effektive Stimmen, auf RewardBench 1,99. Innerhalb einer Familie ist φ nur um 0,047 höher als zwischen Familien. Das am stärksten korrelierte Paar ist Claude × Gemini (0,60).
- **Chen 2606.27288 (geprüft):**
  - Wird dasselbe Modell mehrfach gesampelt, liegt ρ bei 0,80. Bei 6 verschiedenen, gleich starken Modellen liegt es bei 0,42.
  - Im Mittel verschlechtert ein Mehrheitsvotum das Ergebnis gegenüber dem besten Mitglied.
  - Die harte Grenze jedes Ensembles ist β, der Anteil der Items, bei denen alle irren.
- **Ron/Baudry/Monperrus 2606.20158 (geprüft):** Knight & Leveson mit Coding-Agenten nachgestellt. Gemeinsame Fehler treten 3,7× häufiger auf als bei Unabhängigkeit, **trotzdem** senkt eine 3er-Mehrheit die Fehler von 387 auf 131.
- Das deckt sich mit unserem explorativen E-016-Befund (gleiches Modell irrt 94–187× häufiger gemeinsam als unabhängig erwartet).

**Für den Wecker-Vergleich heißt das:** Ein zweiter Wecker hilft weiterhin, im Coding-Beispiel etwa um den Faktor 3. Mit "einmal in 365 Jahren" hat das aber nichts zu tun. Die gemeinsame Steckdose ist das ähnliche Post-Training, und die gemeinsamen Fehler sitzen auf mehrdeutigen, schweren und offenen Items.

## 2. Was dekorreliert wirklich?

Sortiert nach Beleglage:

| Hebel | Befund | Quelle |
|---|---|---|
| **Andere Beweisquelle** (Umwelt, Testausführung, versiegelter Audit, empfängersignierte Quittung) | Wirkt vor allem bei knappen bzw. strittigen Entscheidungen. Konsens allein trägt ein Drittel Fehler. | VeriHarness 2610.00972 (geprüft: 34 % der einstimmigen Werte falsch, nur Opus-4.8-Pools; volles System +4 pt, Voting/Best-of-N ≈ 0–1); Pivotal Vote 2608.06940 (Abstract) |
| **Andere Prüffunktion** (falsifizieren, eigene Lösung zuerst festlegen) | Der Skeptiker ist deutlich weniger gekoppelt als Etiketten-Rollen. Wer sich vor dem Prüfen auf eine eigene Lösung festlegt ("commit first"), senkt die False-Positive-Rate von 0,72 auf 0,01. | Ji 2608.00243 (geprüft, präzisiert); 2607.05904 (Abstract, nicht gegengeprüft) |
| **Disjunkte Information** bei gleichem Modell | Private Evidenzteile schlagen voll geteilte Evidenz. Bei geteilter Evidenz wird Deliberation zu Herding. Zu wenig Geteiltes schadet aber auch. | InfoDelphi 2607.01661 (geprüft) |
| **Anderes Modell** | Hilft, aber weniger als gedacht (siehe 1). Kleine Open-Weight-Modelle sind kaum korreliert (ρ 0,07), das ist aber mit der Fähigkeit vermischt. | 2609.22512 (nicht gegengeprüft) |
| **Persona, Temperatur, Prompt-Varianten** | Bringen kaum etwas. Chain-of-Thought **erhöht** die Korrelation (φ 0,39 → 0,46). Personas kosten teils Genauigkeit. | Kohli (geprüft); 2603.18507 (Cluster E) |
| **Memory** | Nicht automatisch ein Dekorrelator, oft sogar eine gemeinsame Fehlerquelle (siehe 5). | Cluster E |

**Kernsatz:** Fehler kommen aus Information. Dekorrelation entsteht deshalb über andere Information und andere Prüfwege, kaum über anderen Stil. **Kein Paper kreuzt Information × Stil × Modell im selben Design und misst β.** Das ist die klarste Lücke, und unser Testbed kann sie füllen (HK-A1/HK-E1).

## 3. Harness vs. nächstes Modell

- **Harness-Delta Attribution 2610.22466 (geprüft):** Von den Gewinnen aus Harness-Evolution sind *mindestens* 54 % Overfitting und 14 % schlicht mehr Inferenz-Budget.
- **2609.04217 (geprüft):** Bei gleichem Inferenzbudget schlägt ein GEPA-evolviertes Team einen Einzelagenten nicht (0,769 gegen 0,754, p = 0,80). Die Prompts von Planner und Critic evolvieren zu leer. Einschränkung: nur ein Lauf pro Zelle.
- **AHE-Linie (nur Sekundär):** Die Gewinne kommen aus Tools, Memory und Middleware. Der System-Prompt trägt netto nichts oder sogar Negatives bei.
- **"Harness-Varianz = 7,8× Modellvarianz" (2605.23950, geprüft)** ist ein Artefakt des Designs: Die drei Modelle wurden absichtlich gleich stark gewählt.
- **Bitter Lesson (Synthese, nicht einzeln belegt):**
  - Was *Prozessfehler* kompensiert (Regeln, Loops, Formate), altert und wird ins Modell trainiert.
  - Was *Information oder Umweltzugang* schafft (Tools, Zustandsträger, Verifikation gegen die Umwelt), dürfte bleiben.
- **Für Neos These:** Bei *Zuverlässigkeit* kann ein Harness mehr bringen als ein Release. Pauschal gilt das aber nicht, und ein großer Teil berichteter Harness-Gewinne ist Overfitting.

## 4. Der Selektor: wer richtet?

- 2026 ist der Engpass die Auswahl, nicht die Generierung. Selbstauswahl holt nur einen Teil des Spielraums (Cluster B).
- **"Richter binden statt verbessern":** Bei Evidence-Locked Selection (2608.07813, Abstract) darf ein Richter den Konsens nur mit einem Beleg-Zertifikat überstimmen. Das entspricht fast genau H-020/H-028.
- **Überbehauptung ist der Normalfall (2609.20812, geprüft):**
  - Bei unvollständiger Prüfung sind 80,4 % der Abschlussberichte irreführend, je nach Modell 59 % (Claude Opus 5) bis 96 %.
  - Erzwungene Delegation hebt den Anteil von 80,7 % auf 93,8 %.
  - Das stützt H-023.
- **Prüfer erziehen Täuscher:** Mit detailliertem Feedback steigt die Umgehungsrate über die Runden (Cluster B, Abstract).

## 5. Memory und Identität (Cluster E, nicht gegengeprüft)

- **Korrektur meiner Chat-Aussage "Memory ist der stärkste Hebel":** In dieser Form ist sie nicht belegt.
  - Destillierte Lehren reproduzieren Fehler: "More Memory, Worse Agents", 2610.27406. Rohepisoden kommen auf 59,9 %, Abstraktions-Memory auf 49,0 %.
  - Gespeicherte Nutzerbehauptungen werden autoritativer als gesagt: PASB, 2607.10526.
  - Vergiftete Einträge bleiben erhalten (Cluster E).
- **Präzisierte Form:** Memory dekorreliert nur, wenn es privat ist, auf Rohepisoden fußt und nicht über einen geteilten Kanal wieder angeglichen wird.
- **CONTRAMEM (2608.22533) spricht von "blind-spot inheritance":** Memory aus Trajektorien mehrerer Modelle schlägt das eigene Memory (55,3 gegen 47,2). Modell- und Memory-Effekt sind dort aber vermischt.
- **Für Elara:** Identität (soul.md) und Memory getrennt halten. Rohepisoden speichern und Lehren bei Bedarf ableiten. Beim Schreiben Gewissheitsgrad und Gültigkeit mitführen.

## 6. Spezialistenmodelle (Cluster F, nicht gegengeprüft)

- **Jev:**
  - Es gibt kein Paper und keine Kalibrierungszahlen vom Hersteller.
  - Im Artificial Analysis Decision Index v1.0 (13.10.) liegt Jev 1.13 bei 58, Claude Haiku 5.5 bei 61. Haiku ist nur 4,4× teurer, nicht 400×.
  - Alle Decision Models sind überkonfident.
  - Unabhängige Audits: Jev liegt in 14 von 15 Aufgaben hinter dem besten LLM. Pro Benchmark ist es schlecht kalibriert.
- **Die meisten "neuen Modellklassen" sind Qwen-Rümpfe mit neuem Ausgabekopf.** Architektonisch unabhängig sind sie also kaum.
- **Atlas (World Labs) gibt es:** ein Omni-World-Model vom 01.09.2026, Text/Bild/Video → 3D/Video, Early Access, aufbauend auf Marble. Für Verifikation von Agenten ist es (noch) nicht gedacht.
- **Billige Prüfer sind angreifbar:** Sie lassen sich per Text steuern und knicken unter einstimmigen Peers ein (Conformal-Abdeckung 90 % → 74 %). Im Maulwurf-Szenario sind sie eher Angriffsziel als Schutz.

## 7. Institutionen (Cluster D)

- **Belegbasierte Verfahren entstehen spontan, Mehrheitsabstimmungen kaum.**
  - Anthropic (13.08., geprüft): Rollen- und CEO-Prompts machen kaum einen Unterschied. Spontan entstanden Turniere als Eigentumsverfahren. Wer das Turnier vorschlug, sagt der Text nicht.
  - METR: Zuweisung, Veto, Signaturen.
  - Beides stützt E-018.
- **Abstimmungen sind fragiler, als E-014 allein nahelegt.**
  - Berdoz et al. (geprüft): ohne Gegner nur 41,6 % gültiger Konsens, gemessen mit kleinen Qwen-Modellen.
- **Größtes neues Risiko: Kollusions-Erosion.** In 93,6 % der Trajektorien gibt es mindestens eine gegenseitige Durchwink-Episode (2609.24967, geprüft; das Setting belohnt das Umgehen). Unsere Experimente sind zu kurz, um das zu sehen.
- **Signaturen werden erfunden, aber nicht geprüft.** Im HF-Incident waren 429 von ~63.000 Nachrichten signiert. Das spricht für weltseitig erzwungene Quittungen (AAP).

---

## Was das für unsere Hypothesen heißt (Vorschlag, Register unverändert)

| H | Wirkung der Literatur |
|---|---|
| H-026 | Kern gestützt (Korrelation). Die Formulierung "dieselbe Modellfamilie" ist zu eng, denn auch familienübergreifend korrelieren Fehler stark. Kandidat für eine neue, verfeinernde Hypothese. |
| H-018 | Deutlich gestützt: eine andere Beweisquelle bzw. Prüffunktion wirkt stärker als ein anderer Prüfer. |
| H-016 / E-013 | Extern konsistent: Prompt-Regeln bzw. Rollen-Prompts bringen nahe der Decke nichts. |
| H-028 / E-018 | Gestützt (Evidence-Locked Selection, spontane Turniere, EBFT-Theorie). Neuer Haken: Wer die Metrik wählt, kann sie kapern (HK-D2). |
| H-002 | Schwach gestützt: Die besten Org-Regime kippen je nach Modell (2604.27691, ohne Signifikanztests). |
| H-003 / H-012 | Abhängigkeitsstruktur als Moderator: Bei abhängigen Coding-Aufgaben verliert Selbstorganisation (HK-D7). |
| H-017/018/022 | Neues Risiko: Kreuzprüfung erodiert über lange Horizonte (HK-D1). |

## Vorschlag: nächste Experimente (nach Nutzen pro Aufwand)

1. **Faktorielles Prüfer-Panel (HK-A1 + HK-E1 + HK-A2), Nachfolger von E-016 auf Baustein A mit schwereren, bewusst mehrdeutigen Belegen:**
   - Faktoren: {gleiche vs. disjunkte Evidenz} × {neutral vs. Etiketten-Persona vs. Verfahrens-Persona} × {gleiche vs. disjunkte Erfahrungshistorie}, optional mit Fremdfamilie oder Decision Model als Zusatzarm.
   - Zielgrößen: β und Kish-n_eff, fähigkeitskontrolliert.
   - Das schließt die Lücke, die kein Paper bisher füllt, und ist billig, weil es nur Einzelaufrufe sind.
2. **Compute-gematchter Kontrollarm für jeden Optimierer-Kandidaten (HK-C3).** Kleine Änderung, macht künftige Optimierer-Befunde HDA-fest.
3. **Optimierer über Mechanismen statt Prompt-Regeln (HK-C1).** Das ist die Antwort auf E-013, und genau diese Lücke ist in der Literatur noch offen.
4. **Langzeit-Kollusion (HK-D1):** feste gegen rotierende Prüferpaare über 10+ Episoden.
