# Arbeitsregeln für dieses Forschungsprojekt

Dieses Projekt erforscht, wie Organisation in Multi-Agent-Systemen entsteht und wie man sie gezielt optimiert. Neo will am Ende genau nachvollziehen können, was gemacht wurde, und technisch darüber bloggen. **Dokumentation ist deshalb Teil der Arbeit, nicht Nacharbeit.** Jede Session hält sich an diese Regeln, ohne dass man sie daran erinnern muss.

## Die fünf Dokumente

| Datei | Zweck | Regel |
|---|---|---|
| `laborbuch.md` | Chronik: was wurde wann getan, warum, was kam heraus | **Nur anhängen.** Alte Einträge nie umschreiben. Irrtümer korrigiert ein neuer Eintrag ("Korrektur zu Eintrag vom …") |
| `hypothesen.md` | Alle Vermutungen mit ID (H-xxx), Quelle, Status | Status nur mit Verweis auf Evidenz ändern (Experiment-ID oder Quelle) |
| `entscheidungen.md` | Wichtige Weichenstellungen (D-xxx): Kontext, Optionen, Wahl, Begründung | Revidierte Entscheidungen bleiben stehen und werden als "ersetzt durch D-yyy" markiert |
| `quellen.md` | Literatur und externe Quellen mit Prüfstatus | Unterscheiden: im Original geprüft, nur Abstract, nur Sekundärquelle |
| `experimente/E-xxx-name/` | Ein Ordner pro Experiment | Siehe unten |

`notizen/` enthält Arbeitsdokumente wie Analysen und Zuspitzungen. Sie dürfen sich ändern. Was wichtig ist, wandert in die fünf Dokumente oben.

## Ablauf eines Experiments

1. **Vorher `prereg.md` ausfüllen** (Vorlage in `experimente/_vorlage/`): Hypothese, konkrete Vorhersage, Design, Metriken, Anzahl Seeds, Auswertungsplan, Abbruchkriterien. Danach committen. Das schützt davor, sich hinterher die passende Geschichte zur Datenlage auszudenken.
2. **Durchführen:** Config, Code-Version (Git-Commit), Modell-IDs und Seeds werden automatisch mitgeloggt. Rohdaten kommen nach `daten/E-xxx/` und werden **nie verändert**.
3. **Auswerten:** Nur per Skript aus den Rohdaten. Was vom Plan in `prereg.md` abweicht, wird als "explorativ" markiert.
4. **`ergebnis.md` schreiben:** Was kam heraus, bezogen auf die Vorhersage, plus Überraschungen und Grenzen. **Negative und Null-Ergebnisse gehören dazu.**
5. **Danach:** Laborbuch-Eintrag schreiben und Hypothesen-Status aktualisieren.

## Methodik (aus Handoff Teil 3, seit 21.10.)

1. **Zwei Stufen.**
   - *Entdeckung*: explorative Läufe, Optimierer, post-hoc-Analysen. Das liefert nur **Kandidaten**.
   - *Bestätigung*: Ein Kandidat gilt erst als **Befund**, wenn er in einem präregistrierten Lauf auf **frischen Seeds** repliziert. Gerichtete Vorhersage, vorab festgelegter Test, Daten aus Stufe 1 werden nie wiederverwendet.
   - In `prereg.md` steht `Stufe: Entdeckung | Bestätigung`.
2. **Pipeline-Kontrollen.**
   - Regelmäßig ein **A/A-Test** (zwei identische Configs mit anderem Namen). Er darf keinen Effekt zeigen.
   - Eine **Positivkontrolle** (absichtlich schädliche Config). Sie muss erkannt werden.
   - Bei Effekten ist nach Möglichkeit eine **Dosis-Wirkung** zu prüfen.
3. **Mehrfachtests.**
   - Paarvergleiche berichten zusätzlich q-Werte (Benjamini-Hochberg-FDR, `analyze.compare`).
   - Effektgrößen gehen vor p-Werte. Die Leitfrage lautet: Ist der Effekt groß genug für Wave oder Ace?
4. **Thesen einfrieren.**
   - Der Wortlaut einer Hypothese in `hypothesen.md` wird nie geändert.
   - Eine Präzisierung wird eine neue Hypothese ("verfeinert H-xxx"). Der Status wird nur mit Evidenz-Verweis geändert.
   - Die Änderungsgeschichte steht in Git und im Laborbuch.
5. **Messlauf und Optimierungslauf trennen.**
   - Messläufe (Sweeps) haben keine Rückkopplung.
   - Optimierungsläufe (Harness-Rückkopplung) liefern nur Entdeckungen.
6. **Kritiker-Unabhängigkeit.**
   - Wer ein Experiment entworfen hat, bestätigt es nicht selbst. Ein Kritiker sollte eine andere Modellfamilie sein und blind prüfen.
   - Solange nur Claude verfügbar ist, steht das bei jedem Befund ausdrücklich als offene Schwäche.
7. **Transkripte lesen.**
   - Zu jedem Befund gehören 2–3 zufällig gezogene Verläufe je Arm, auch der langweiligen Kontrollbedingung, als Pflichtlektüre für Neo (`orglab.digest`).
8. **Eval-Awareness.**
   - Agentenprompts enthalten keine Wörter wie "benchmark", "experiment" oder "test".
   - Klassische Paradigmen (Hidden Profile, Asch, …) werden nur getarnt und prozedural variiert eingesetzt.

9. **Audit vor jeder Auswertung:** `python -m orglab.audit daten` zeigt Runs mit fehlerhaften Agenten-Zügen (z. B. Session-Limit). `analyze.collect` überspringt sie automatisch mit Warnung. Betroffene Runs werden als ungültig markiert (`metrics.ungueltig.json` + `UNGUELTIG.txt`), nie gelöscht.

## Lehren aus Fehlern (seit 23.10., D-017; Regel 19 seit D-020, Regel 20 seit D-021)

Diese Regeln stammen aus Fehlern, die uns tatsächlich passiert sind. Die Herkunft steht jeweils dabei, damit klar ist, wovor die Regel schützt.

10. **Manipulationscheck ist Pflicht.**
    - Jede Präregistrierung nennt eine messbare Prüfung, ob die Manipulation wirklich das tut, was ihr Name sagt (z. B. Reasoning-Tokens, Werkzeugaufrufe, Promptlänge).
    - Scheitert sie, gilt der Befund nur unter seiner *tatsächlichen* Manipulation.
    - *Herkunft:* E-019 und E-021. "Reasoning aus" war in Wahrheit adaptives Reasoning, die Deutung stand zwei Experimente lang falsch herum.
11. **Weg, Modell und Einstellung stehen in jeder Präregistrierung und in jedem Ergebnis**, mit ihrer *tatsächlichen* Bedeutung beim Anbieter:
    - Weg: SDK/Abo, OpenRouter/API oder Hersteller-CLI
    - exakte Modell-ID
    - jeder gesetzte und jeder *weggelassene* Parameter
    - *Herkunft:* E-021 (OpenRouter: Reasoning bei Sonnet 5.5 nicht abschaltbar), Harness-Inventur `notizen/26`.
12. **Fremdkontrolle der Ground Truth vor jedem Hauptlauf.**
    - Ein Nicht-Claude-Modell oder Neo beurteilt eine geschichtete Stichprobe neuen Materials blind und je Beleg einzeln.
    - Abweichungen werden von Hand geklärt, bevor es losgeht.
    - *Herkunft:* rund zehn Generatorfehler, bei denen das Prüfer-Modell recht hatte (`notizen/25`).
13. **Analyse-Einheit ist die unabhängige Einheit.**
    - Hängen Messungen zusammen (derselbe Beleg in mehreren Kanälen, Urteile im selben Stapel), wird auf Beleg- bzw. Stapelebene ausgewertet, mit Cluster-Bootstrap.
    - Intervalle auf abhängigen Einzelurteilen gelten nicht als Beleg.
    - *Herkunft:* Grok-Gutachten 1, `notizen/20` gegen `notizen/20b`.
14. **Prävalenz vor jeder Übertragung.**
    - Fehlalarm- und Eskalationszahlen aus dem Labor (50 % kaputt) werden vor jeder Aussage über Wave zusätzlich bei realistischer Prävalenz berichtet (Standard 5 %, PPV).
    - *Herkunft:* Grok-Gutachten 1 §3, `notizen/20b` §5.
15. **Keine Aussage ist stärker als ihr Status.**
    - Was das Projekt verlässt oder in Zusammenfassungen steht (an Neo, Ace, Blog, Notizen), trägt seinen Status: belegt, gestützt, explorativ oder Hinweis.
    - Explorative Befunde werden nicht als Tatsache formuliert, auch nicht im Gespräch.
    - *Herkunft:* "Reasoning erhöht Fehlalarme" ging als Tatsache an Ace. Die These in `notizen/21` §5 lief der Evidenz voraus (Grok).
16. **Prompts, Material und Auswertung werden vor dem Lauf eingefroren.**
    - Die exakten Prompttexte aller Zellen (Dry-Run), der Generator-Commit und das Auswerteskript werden vor dem ersten Hauptlauf committet. Das Skript wird vorher mit synthetischen Daten getestet.
    - Was im Code steht, aber nicht in der Präregistrierung, gilt als Forscher-Freiheitsgrad.
    - *Herkunft:* E-020, Anstupser im Prompt (Grok-Gutachten 1 §5).
17. **Das Material darf nicht leichter lesbar sein als die Hypothese verlangt.**
    - Ist eine Spur auch ohne den manipulierten Faktor entscheidbar (Lecks wie "0/20", "0 kB", "Mittelwert 100"), misst der Faktor dort nichts.
    - Ein Test muss solche Lecks für die Primär-Fehlerarten ausschließen.
    - *Herkunft:* E-020 SPEC, Grok-Gutachten 1 und 2.
18. **Externe Kritik vor großen Läufen.**
    - Vor jedem Hauptlauf über 10 $ oder jeder neuen Kernthese liest ein Kritiker aus anderer Modellfamilie Präregistrierung und Code. Er arbeitet auf einer Kopie ohne Secrets und ist sparsam einzusetzen (Grok-Limits, `notizen/26`).
    - *Herkunft:* Grok fand vor dem E-020-Hauptlauf Fehler, die ~45 $ entwertet hätten.
19. **Doppelte Buchführung bei jedem Bestätigungslauf.**
    - Nach dem Lauf implementiert mindestens ein Modell anderer Familie die Primärauswertung neu, **nur aus der Präregistrierung und Beispielzeilen der Rohdaten**, ohne Claudes Code (`python -m orglab.nachrechnung E-xxx`).
    - Claude liest den Fremdcode vor dem Ausführen und führt ihn isoliert aus (`python -I`).
    - Weichen die Zahlen ab, gilt der Befund erst nach Klärung. Die vom Fremdmodell gemeldeten offenen Entscheidungen werden im Ergebnis gelistet.
    - *Herkunft:* Regelkritik-Panel (`notizen/31`). Das meistgenannte Thema war die ungeprüfte Auswerte-Pipeline (10 von 16 Fremdmodellen, keines der 3 Claude-Modelle). Bei E-022 fand die Nachrechnung eine Lücke im eingefrorenen Skript (16-Stapel-Regel fehlte).
20. **Verblindete Auswertung bei jedem Bestätigungslauf.**
    - Vor der Auswertung: `python -m orglab.verblindung verblinden E-xxx --feld … --arme … --weg …`. Die Arme heißen dann A, B, C, …. Der Schlüssel liegt außerhalb des Repos, im Repo steht nur sein Hash.
    - Felder, die den Arm verraten können (Token-Zahlen, Rohtext, Kosten), werden aus der verblindeten Kopie entfernt. Welche das sind, steht in der Präregistrierung.
    - Claude wertet nur die verblindete Kopie aus, schreibt alle Entscheidungen in `auswertung-verblindet.md` und committet. Erst dann: `python -m orglab.verblindung entblinden E-xxx`.
    - Ein Manipulationscheck, der den Arm verrät, läuft erst nach dem Entblinden oder rein deterministisch im Skript.
    - Schutzziel ist unbewusstes Biegen und versehentliches Sehen. Eine harte Sperre per Sandbox ist geplant (`notizen/32`).
    - *Herkunft:* Claudes einseitige Abweichung bei der Wave-Kodierung (K1/K5, `notizen/30`). Neos Meta-Harness-Gedanke (`notizen/32`). Standard in Medizin und Teilchenphysik.

**Checkliste pro Befund:**
- [ ] repliziert auf frischen Seeds
- [ ] A/A sauber
- [ ] Positivkontrolle erkannt
- [ ] **Manipulationscheck bestanden** (Regel 10)
- [ ] vorab festgelegt, inklusive Prompts, Material und Auswerteskript (Regel 16)
- [ ] Weg, Modell und Einstellung dokumentiert (Regel 11)
- [ ] Ground Truth fremdkontrolliert (Regel 12)
- [ ] auf der richtigen Analyse-Einheit ausgewertet (Regel 13)
- [ ] von einem Fremdmodell unabhängig nachgerechnet (Regel 19)
- [ ] verblindet ausgewertet, erst danach entblindet (Regel 20)
- [ ] Effektgröße relevant, auch bei realistischer Prävalenz (Regel 14)
- [ ] Kritiker hat versucht, den Befund zu brechen
- [ ] Eval-Awareness und Lehrbuch-Effekt bedacht
- [ ] Transkripte gelesen
- [ ] mit einem Befehl reproduzierbar

## Grundsätze

- **Belegt oder vermutet?** Jede Behauptung ist entweder belegt (mit Verweis) oder als Hypothese markiert. Wissen aus dem bestehenden System (Ace, Wave) gilt als Hypothesenquelle und nicht als bewiesen.
- **Am Ende jeder Arbeitssession:** einen Laborbuch-Eintrag schreiben und Neo mitteilen, was dokumentiert wurde.
- **Git:** Commits und Push ins private Repo (github.com/Stonewave-Tech-LLC/social-skills-benchmark) sind erlaubt (Neo, 23.10.). Vorher prüfen, dass keine Secrets oder internen Rohdaten (`.env`, `daten/ace-export-*`) dabei sind. Das Repo öffentlich zu machen, entscheidet nur Neo. Commit-Nachrichten verweisen auf Laborbuch-Datum und E-/D-/H-IDs.
- **Sprache:** Deutsch, Fachbegriffe dürfen englisch bleiben.
