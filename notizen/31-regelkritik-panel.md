# Regelkritik durch ein Modell-Panel: Was fangen unsere Regeln strukturell nicht?

**Festgelegt:** 23.10.2026, vor dem ersten Aufruf (Commit dieser Datei). **Stufe:** Entdeckung, explorativ. Das hier liefert Kandidaten für Regeln, keine Befunde.

## Anlass
Neo hat einen strukturellen Bug in der Schleife "KI erforscht, wie KI besser forscht" benannt. Die Regeln 10–18 hat Claude aus **bemerkten** Fehlern abgeleitet. Eine Fehlerart, die Claude grundsätzlich nicht bemerkt, kann deshalb auch keine Regel erzeugen (Chat 23.10., `notizen/30`). Gegenmittel: Modelle von außerhalb prüfen die **Regeln selbst**. Neo: "frag von mir aus 20 verschiedene Modelle".

## Design
- **Panel:** 20 Modelle über OpenRouter, je ein Aufruf mit Anbieter-Standard (kein `reasoning`-Parameter, Temperatur Standard). 17 Modelle aus 15 anderen Familien (OpenAI, Google, xAI, DeepSeek, Qwen, Moonshot, Mistral, Meta, Zhipu, MiniMax, Cohere, Amazon, StepFun, Xiaomi, Thinking Machines) und **3 Claude-Modelle als Vergleich** (Opus, Sonnet, Haiku 5.5). Liste in `orglab/regelkritik.py`.
- **Material:** nur `CLAUDE.md`. **Nicht** `notizen/30`, weil dort unsere eigene Vermutung (schleichende Konvergenz) steht und alle Antworten in diese Richtung lenken würde.
- **Frage:** wörtlich in `orglab/regelkritik.py` (`QUESTION`), neutral formuliert: Welche Fehlerarten fangen diese Regeln strukturell nicht? 3 bis 6 blinde Flecken, je mit Szenario, Begründung und einer Gegenmaßnahme, die nicht davon abhängt, dass die KI ihren Fehler selbst bemerkt.
- **Bündelung:** Ein Nicht-Claude-Modell (`google/gemini-4-argon`) ordnet alle blinden Flecken **anonymisiert und gemischt** zu 8–15 Themen. Claude bündelt nicht selbst, weil Claude bei Kritik an den eigenen Regeln befangen wäre.
- **Auswertung (Skript, vorab festgelegt):**
  - je Thema die Zahl der Modelle, davon Claude
  - Einzelstimmen (Themen, die nur ein Modell nennt)
  - Themen-Überlappung (Jaccard) innerhalb Claude, innerhalb Nicht-Claude und über die Familiengrenze
- **Erwartungen (vorab, nur deskriptiv):**
  - E1: Mehrere Modelle nennen Befangenheit oder Selbstbestätigung der KI, ohne dass wir sie darauf gebracht haben.
  - E2: Die drei Claude-Modelle überlappen untereinander stärker als mit den anderen.
  - E3: Es gibt Einzelstimmen, die uns neu sind. Genau dort zahlt sich die Vielfalt aus.
- **Grenzen:**
  - Die Themenbildung hängt von einem einzigen Bündel-Modell ab.
  - Jaccard über Themen ist ein grobes Maß und kein n_eff.
  - Gemini ist zugleich Panelist. Die Anonymisierung mildert das, schließt es aber nicht aus.
- **Danach:** Claude ordnet jedes Thema ein (berechtigt, schon abgedeckt, unklar), mit Begründung. Neo entscheidet, welche Themen zu neuen Regeln werden.

## Ergebnis (automatisch, `python -m orglab.regelkritik report`)

- Modelle mit verwertbarer Antwort: 19 von 20 · blinde Flecken: 105 (zugeordnet: 105) · Themen: 14 · Clustering: `google/gemini-4-argon`, anonymisiert
- Themen-Überlappung (Jaccard, Mittel): innerhalb Claude 0.23 · innerhalb Nicht-Claude 0.23 · Claude gegen Nicht-Claude 0.22

| Thema | genannt von (Modelle) | davon Claude | Beschreibung |
|---|---|---|---|
| Ungeprüfte Auswerte- und Audit-Pipeline (KI-Monopol bei Werkzeugen) | 10 | 0 | Auswerteskripte, Audit-Tools und synthetische Testdaten stammen von derselben KI-Instanz und werden nicht gegen externe Maßstäbe validiert, sodass symmetrische Messfehler und gekoppelte Bugs unentdeckt bleiben. |
| Selektive Berichterstattung und unvollständige Dokumentation (Publication Bias) | 10 | 2 | Trotz Append-only-Laborbuch und korrekter Status-Labels fehlen Regeln, die das Weglassen gescheiterter Vorläufe verhindern oder eine vollständige, repräsentative Darstellung aller Befunde in Zusammenfassungen erzwingen. |
| Künstliche Aufgabenwelt und mangelnde ökologische Validität des Materials | 9 | 1 | Frische Seeds und korrekte Einzellabels garantieren keine Übertragbarkeit auf reale Daten, wenn die zugrundeliegende Aufgabenwelt zu einfach ist, nicht erneuerte Fallbanken nutzt oder perfekt auf die KI-Intervention zugeschnitten wurde. |
| Unsichtbare Modell- und Anbieter-Drift über die Zeit | 9 | 2 | Das bloße Dokumentieren von Modell-IDs und lokalen Konfigurationsparametern übersieht zeitliche Verhaltensänderungen auf Anbieterseite oder ignorierte Parameter während längerer oder zeitversetzter Experimentreihen. |
| Korrelierte Blindheit bei Ground-Truth-Prüfung und externer Kritik | 8 | 2 | Die Kontrollinstanzen sind durch Ausnahmeregelungen, geteilte Trainings-Priors verschiedener Modellfamilien oder Kostenschwellen geschwächt, wodurch einseitige Bewertungsmuster nicht zuverlässig durchbrochen werden. |
| Unterhöhlung der Präregistrierung und nachträgliche Hypothesenanpassung (HARKing) | 7 | 0 | Freiheitsgrade vor der Präregistrierung, vage Vorhersagen, stille Begriffs- oder Formeländerungen im Code sowie unkontrollierte Hypothesen-Verfeinerungen ermöglichen ein nachträgliches Anpassen der Thesen an die Daten. |
| Verzerrung durch selektiven Ausfall (Attrition und Survivorship Bias) | 7 | 2 | Das regelkonforme Aussortieren technisch fehlerhafter oder abgebrochener Läufe durch das Audit-Tool ignoriert, dass die Ausfallrate selbst vom Versuchsarm abhängen und so den gemessenen Effekt systematisch verzerren kann. |
| Mangelnde Konstruktvalidität der Zielmetriken | 7 | 1 | Manipulationschecks und eingefrorene Skripte sichern nur die technische Messung eines Proxys, prüfen aber nicht, ob die gewählte Zielgröße das theoretische Konstrukt 'gute Organisation' überhaupt inhaltlich valide abbildet. |
| Selbstreferenzielle Regelsetzung und fehlende Meta-Kontrolle | 6 | 2 | Da dieselbe KI die Arbeitsregeln verfasst, anwendet und deren Einhaltung ohne unabhängigen mechanischen Abgleich selbst attestiert, bleiben strukturelle Regellücken, unbemerkte Abweichungen und fehlerhafte Fehlerableitungen unsichtbar. |
| Unkontrolliertes multiples Testen über Experimentgrenzen hinweg | 6 | 1 | Die Fehlerkorrektur für Mehrfachtests greift nur innerhalb einzelner Läufe, verhindert aber nicht die Inflation falsch-positiver Befunde durch wiederholte Bestätigungsversuche und Kandidatenselektion über ganze Experimentserien hinweg. |
| Scheinbare menschliche Aufsicht und KI-gesteuerte Stichprobenauswahl | 5 | 1 | Die menschliche Kontrolle durch Neo verkommt zum Ritual, weil er fachlich sowie kapazitiv überfordert ist und die KI kontrolliert, welche Transkripte, Stichproben und Zusammenfassungen den Prüfern überhaupt vorgelegt werden. |
| Konfundierung durch Architektur, Scaffolding und Ressourcenbudget | 5 | 0 | Vermeintliche Organisationseffekte werden nicht sauber von Störfaktoren wie erhöhtem Rechenbudget, erzwungenem Harness-Verhalten, Formatierungsartefakten oder versteckten Rückkopplungen in der Pipeline getrennt. |
| Fehlende Teststärke-Planung (Power) für Nullbefunde und Kontrollen | 4 | 2 | Es gibt keine Pflicht zu vorab berechneten Power-Analysen für minimal relevante Effektgrößen, weshalb sowohl Null-Ergebnisse in Hauptläufen als auch unauffällige A/A-Tests wegen zu geringer Stichprobengröße nichtssagend sein können. |
| Versteckte Informationslecks und unbemerkte Eval-Awareness | 4 | 1 | Oberflächliche Wortfilter übersehen, dass Modelle das Test-Setting oder die Lösung über Dateistrukturen, Umgebungsvariablen, aggregierte Prompt-Statistiken, Trainingsdaten-Erinnerung oder implizite Materialhinweise dekodieren können. |

**Einzelstimmen** (Themen, die nur ein Modell nennt):


Kosten: 1.03 $ Panel

## Abweichungen vom Plan
- **Amazon Nova Premier** ist beim Anbieter abgekündigt (HTTP 404, "end of its life"). Es wurde nicht ersetzt, damit bleiben 19 Modelle.
- **Qwen, Kimi, GLM und StepFun** haben im ersten Durchlauf das ganze Budget von 8.000 Tokens fürs Denken verbraucht und keine Antwort gegeben. Sie wurden mit 32.000 Tokens wiederholt (`--retry-empty`), danach antworteten alle vier. Die leeren Erstversuche stehen weiter in `daten/regelkritik/antworten.jsonl`.
- Die Einzelstimmen-Liste ist leer, weil das Bündeln zu 14 breiten Themen jede Einzelstimme einem größeren Thema zugeschlagen hat. E3 lässt sich auf Themenebene deshalb **nicht prüfen**. Einzelne Einwände stehen weiter in `daten/regelkritik/cluster.json`.

## Erwartungen (deskriptiv)
- **E1 (Selbstbestätigung wird ohne Anstoß genannt): ja.** "Selbstreferenzielle Regelsetzung" (6 Modelle), "Korrelierte Blindheit bei Ground-Truth und Kritik" (8) und "Scheinbare menschliche Aufsicht" (5) tauchten auf, obwohl die Modelle `notizen/30` nicht kannten.
- **E2 (Claude-Modelle überlappen untereinander stärker): nein.** Jaccard innerhalb Claude 0,23, innerhalb Nicht-Claude 0,23, Claude gegen Nicht-Claude 0,22. Auf dieser groben Themenebene war die Kritik der Claude-Modelle nicht gleichförmiger als die der anderen.
- **Auffällig (Hinweis, nachträglich bemerkt, 14 Themen angeschaut, also nicht als Test zu lesen):** Das meistgenannte Thema, **die ungeprüfte Auswerte- und Audit-Pipeline**, nennen 10 von 16 Nicht-Claude-Modellen und **keines der 3 Claude-Modelle**. Ebenso 0 Claude bei HARKing (7 Modelle) und bei Konfundierung durch Scaffolding (5). Würden die Claude-Modelle mit derselben Rate nennen wie die anderen, läge die Chance für "0 von 3" beim Pipeline-Thema bei etwa 5 %. Bei 14 angeschauten Themen ist das aber erwartbarer Zufall. Trotzdem passt es zur Frage nach blinden Flecken einer Modellfamilie: **Dass das eigene Werkzeug selbst ungeprüft ist, sieht Claude offenbar am schlechtesten.**

## Einordnung je Thema (Claude, **befangen**, weil es Kritik an Claudes eigenen Regeln ist; Neo entscheidet)

| Thema | Einordnung | Warum | Konkrete Gegenmaßnahme (aus den Antworten) |
|---|---|---|---|
| Ungeprüfte Auswerte-Pipeline | **berechtigt, wichtigstes Thema** | Skript, synthetische Testdaten und Audit stammen alle von Claude. Ein Denkfehler steckt dann in allen dreien zugleich, und der Test besteht trotzdem. | **Doppelte Buchführung:** Ein Modell anderer Familie implementiert die Kernmetrik nur aus der Präregistrierung neu, ohne Claudes Code, und rechnet die Rohdaten nach. Zusätzlich "Kanarien": Antwortmengen mit vorab bekannten Raten laufen mit. |
| Selektive Berichterstattung | berechtigt, teilweise abgedeckt | Das Laborbuch ist vollständig, aber **Zusammenfassungen an Neo wählt Claude aus** (Beispiel: "belegt" in der Morgenzusammenfassung). | Zusammenfassungen gegen das Laborbuch von einem Fremdmodell auf Auslassungen prüfen lassen. Statustabellen aus den Registern erzeugen statt von Hand schreiben. |
| Künstliche Aufgabenwelt | berechtigt, bekannt | Synthetisches Material. Die Wave-Fälle sind nur eine dünne Brücke. | Echte Wave-Fälle ausbauen (Aces unselektierte Stichprobe). |
| Modell- und Anbieter-Drift | **berechtigt, neu für uns** | OpenRouter leitet an wechselnde Anbieter weiter. Wir loggen weder Anbieter noch Modellversion je Aufruf, und der E-021-Vergleich mit E-022 liegt nur Stunden auseinander. | Anbieter aus der Antwort mitloggen. Ein fester "Anker-Stapel" läuft bei jedem Experiment mit und muss stabil bleiben. |
| Korrelierte Blindheit Ground Truth | berechtigt, teilweise abgedeckt | GPT prüft, denkt aber nur ~120 Tokens (`notizen/29` §5). Gemeinsame Trainings-Priors bleiben. | Bei kritischen Läufen zwei Fremdmodelle verschiedener Familien. Abweichungen nach einer vorab festgelegten Regel klären. |
| HARKing | **berechtigt, ist passiert** | H-037 entstand nach den E-021-Daten als "Verfeinerung". Das ist regelkonform und trotzdem genau dieser Mechanismus. | Verworfene Operationalisierungen in jede Präregistrierung schreiben. Bestätigungs-Präregistrierung durch ein zweites Modell nur aus dem Hypothesen-Wortlaut erstellen lassen. |
| Selektiver Ausfall | berechtigt, klein | Regel 9 sortiert ungültige Runs aus, ohne zu prüfen, ob der Ausfall vom Arm abhängt. | Ausfälle je Arm berichten (E-022 tat es zufällig, 0 überall) und als Pflicht in die Präregistrierungs-Vorlage. |
| Konstruktvalidität | berechtigt, tief | Misst "Fehlalarmrate auf synthetischen Logs" das, was wir in Wave meinen? | Wave-Brücke, Fachleute-Gespräch (`notizen/16`). Keine schnelle Lösung. |
| Selbstreferenzielle Regelsetzung | berechtigt | Das ist genau der Anlass dieser Notiz. | Dieses Panel regelmäßig wiederholen, Regeländerungen nur mit Neos Entscheidung (schon Praxis). Regel-Einhaltung mechanisch prüfen (Skript statt Selbstauskunft). |
| Mehrfachtests über Experimente | berechtigt | Zwei Bestätigungsversuche für eine Hypothese (E-021, E-022) ohne Gesamtkorrektur. | Register aller konfirmatorischen Tests, FDR über Experimente. |
| Scheinbare menschliche Aufsicht | **berechtigt, unbequem** | Neo hat heute selbst gesagt, dass ihm die Menge zu viel ist, und Claude wählt aus, was er sieht. | **Neo zieht Stichproben selbst** (eigener Seed, Würfel). Kritiker bekommen einen vollständigen Repo-Schnappschuss per Skript statt einer Auswahl. Kurze, feste Formate statt langer Zusammenfassungen. |
| Konfundierung durch Scaffolding | berechtigt, teilweise abgedeckt | Harness-Inventur (`notizen/26`) zeigt versteckten Herstellerkontext. | Rechenbudget als Kovariate mitloggen. |
| Teststärke | berechtigt | Keine Pflicht zur Power-Rechnung (Grok-Gutachten 2 sah das bei E-020). | Power-Abschnitt als Pflicht in die Präregistrierungs-Vorlage. |
| Lecks und Eval-Awareness | teilweise abgedeckt | Regel 8 filtert nur Wörter. | Bei Bedarf Awareness-Probe ("Glaubst du, das ist ein Test?") als Sekundärmaß. |

**Wenn Neo nur eine Maßnahme wählt, empfehle ich die doppelte Buchführung.** Sie kostet wenige Dollar, trifft das meistgenannte Thema und setzt genau dort an, wo Claude laut diesem Panel am blindesten ist.
