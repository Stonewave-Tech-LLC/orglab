# Externes Gutachten: Grok (xAI) über das Projekt

> **Korrektur 23.10. (E-021, Manipulationscheck):** Was hier "Reasoning aus" heißt, war in Wahrheit die **Standardeinstellung mit adaptivem, verborgenem Reasoning** (OpenRouter: Reasoning ist bei Sonnet 5.5 nicht abschaltbar). "Reasoning low" war **gedrosseltes** Reasoning. Alle Aussagen "Reasoning erhöht Fehlalarme" sind deshalb umzudrehen: **Gedrosseltes Reasoning erhöht Fehlalarme** (H-037). Details: `experimente/E-021-reasoning-fehlalarme/ergebnis.md`.

- **Datum:** 22.10.2026, auf Neos Vorschlag
- **Aufruf:** Grok Build CLI 1.0.62, `grok -m grok-4.7 --permission-mode plan --disable-web-search --no-subagents`, headless. Die CLI meldete keinen Fehler. Welches Modell tatsächlich lief, habe ich nicht separat verifiziert.
- **Material:** eine Kopie der Dokumente, kein Zugriff aufs Repo, keine `.env`, keine Rohdaten:
  - Arbeitsregeln
  - Register (Hypothesen, Entscheidungen, Quellen)
  - Notizen 14 und 18–22
  - alle Präregistrierungen und Ergebnisse
  - die Module `evidence`, `realitaet`, `batch` und `landkarte`
- Interne Wave-Daten (`notizen/06`), die Kontaktliste (`notizen/16`) und das Laborbuch wurden bewusst nicht mitgegeben.
- **Prompt:** unabhängiges, kritisches Gutachten auf Konferenzniveau, Fragen 1–8 (Gesamturteil, Einwände, Methodik, Alternativerklärungen, E-020, blinde Flecken, nächste Schritte, Positives).
- **Bedeutung für die Methodik:** Das ist der erste Kritiker aus einer **anderen Modellfamilie** (CLAUDE.md, Methodik 6). Er hat nicht blind geprüft, weil er die Dokumente der Autoren las. Er ist trotzdem unabhängiger als alles bisher.

---

## Einordnung durch Claude (was ich annehme, was nur teilweise)

| Punkt des Gutachtens | Einordnung | Konsequenz |
|---|---|---|
| Die These in `notizen/21` §5 läuft der Evidenz voraus. "Nicht mehr Prüfer" ist unbelegt; Ron et al. widersprechen der starken Lesart | **berechtigt** | §5 wird als These mit Belegstatus umformuliert: "Information" und "Prüferzahl" sind nicht gegeneinander getestet. |
| Die These verschmilzt drei Fehler (fehlender Sollwert, Integrationsfehler unter grünem Status, Priming) | **berechtigt** | Für die Literatur und den Blog getrennt halten |
| Der 54-%-Spezifikationsbeleg widerspricht der eigenen Ungültigkeitsentscheidung | **berechtigt**, den Fehler hatte ich nicht gesehen | Nicht mehr als Evidenz für H-033 zitieren, nur als Anlass |
| Wilson-Intervalle auf abhängigen Urteilen; Punktwerte als Befund zitiert | **berechtigt** | Landkarte auf Belegebene neu rechnen (Cluster-Bootstrap) |
| Spurtyp-Kategorien sind nachträglich beschriftet und zirkulär (D-016 baut, was übersehen wurde) | **teilweise.** Die Zirkularität ist echt. Ob der Spurtyp ein "Faktor" ist, war nie behauptet, aber §3 der Landkarte liest sich so | Spurtyp nur deskriptiv. Für eine Bestätigung braucht es eine vorab festgelegte Klassifikation neuer Fehlerarten. |
| Reasoning gegen Fehlalarme nur im Stapel gemessen; E-020 V6 misst einen anderen Estimanden (Einzelbeleg) | **berechtigt** | V6 umformulieren oder Stapel-Arm vorsehen |
| Konfidenzkurve gepoolt und in-sample; eine Spurtyp-Regel könnte gleich viel fangen; Prävalenz 50 % | **berechtigt.** Der Vergleich mit einer Spurtyp-Regel ist ein sehr guter Vorschlag | Neu rechnen: Konfidenz gegen Spurtyp-Regel, getrennt nach Modus und Reasoning |
| Es fehlt eine dumme Baseline (Stringvergleich ohne LLM) | **berechtigt**, wichtig | Bauen. Klärt, wie viel "Prüfleistung" Stringvergleich ist. |
| E-020: Die Anstupser sind je mit einem Faktor konfundiert; dazu der dritte Halbsatz "and what you can look up" bei ZUGANG=0 | **berechtigt.** Der Halbsatz steht in `realitaet.py` Z. 75, von mir übersehen | Alle drei Sätze raus. Der exakte Prompt kommt in die Präregistrierung. |
| E-020: `lookup_runbook` liefert unabhängig vom Topic alles; die Sollwerte lecken in die Kanäle (47 Spalten, 0/20, 0/4) | **berechtigt.** Damit misst SPEC für die meisten Fehlerarten strukturell nichts | Primärmetrik auf Fehlerarten beschränken, deren Sollwert nur im Auftrag steht (vorab benannt), oder Leaks entfernen. Runbook abschnittsweise. Werkzeug in beiden SPEC-Stufen. |
| E-020: Auswerteskript nicht eingefroren; Abbruch lässt halbe Läufe zu | **berechtigt** | Skript vor dem Lauf schreiben und committen. Festlegen, was bei Abbruch berichtbar ist. |
| Die Welt wurde an das Modell angepasst, nicht die Metrik an die Mehrdeutigkeit | **teilweise.** Die Reparaturen waren Ground-Truth-Fehler, keine Bequemlichkeit. Der Effekt auf die Decke ist aber real: Mehrdeutigkeit ist per Design ausgeschlossen. | Später ein eigener Arm mit gelabelter Mehrdeutigkeit (Mensch als Ground Truth) |
| Wave-Policy-Schlüsse ("Wave braucht schon jetzt …") sind verfrüht | **berechtigt** | In `notizen/21` als Hypothesen kennzeichnen, nicht als Empfehlungen |
| Kritiker-Unabhängigkeit praktisch nie scharf | **berechtigt.** Dieses Gutachten ist der erste Schritt | Zweitmodell bewertet die Ground Truth einer Stichprobe neu |
| Positives: Zwei-Stufen-Regel eingehalten, E-014/E-018 sauber, D-014 richtig | angenommen | – |

**Gesamt:** Der Gutachter hat fast überall recht. Am wertvollsten ist, dass er Fehler im *E-020-Design vor dem Start* findet: Leaks, Runbook als Antwortschlüssel, ein dritter Anstupser. Die hätten den Hauptlauf (~45 $) weitgehend entwertet. **E-020 startet nicht, bevor die Punkte behoben sind.**

---

## Das Gutachten (wörtlich, ungekürzt)

Ich lese zuerst die Gedanken- und Schwierigkeitslandkarte und verschaffe mir dann einen Überblick über die übrigen Unterlagen, ohne etwas zu ändern.Die Landkarte ist klar. Als Nächstes lese ich die Methodikregeln, die Kernthese und die Experimente, auf denen das Urteil hängt.Die Prompt-Sätze stehen im Code, nicht in der Präregistrierung. Ich lese Harness, Ergebnisse und die Stellen, an denen die These über die Daten hinausgeht.Die Kernthese ist eine Interpretation, kein Befund. Belastbar bestätigt sind zwei enge Governance-Resultate. Die Prüfer-These stützt sich auf explorative, abhängige und teils zirkulär konstruierte Kalibrierungsdaten.

Rohdaten unter `daten/` liegen in diesem Ordner nicht. Die Raten unten stammen aus den Ergebnisdateien und aus `notizen/20-schwierigkeitslandkarte.md`. Die Aggregationslogik habe ich in `code/landkarte.py` und `code/evidence.py` geprüft, die jsonl-Zeilen nicht neu ausgezählt. Die Literaturzahlen habe ich nicht in den Originalen gelesen, nur in `quellen.md` und `notizen/18-recherche-synthese.md`. Die OpenRouter-Semantik von `reasoning.effort` habe ich nicht geprüft.

## 1. Gesamturteil

Was sich mit den eigenen Regeln als Befund bezeichnen lässt, sind E-014 und E-018: Gegen geskriptete Blockierer und Lügenstimmen wirken Übernahmeregeln, und der Beleg-Arm ist gegen Stimmen immun, teils weil er das per Konstruktion ist (`experimente/E-018-beleg-statt-stimme/ergebnis.md`). Die These, Vertrauen skaliere über bessere Information statt über mehr Prüfer, ist davon nicht gedeckt. H-026 ist ungetestet, E-017 und E-019 sind an der Decke gescheitert, und die Landkarte ist ausdrücklich nicht präregistriert. Die drei Sätze in `notizen/21-gedankenlandkarte.md` §5 ziehen Entdeckungen, eine ungültige Spezifikationsbeobachtung und fremde Preprints zu einer Kausalaussage zusammen, die das Register (`hypothesen.md`) noch als offen führt. Für ein Laborprotokoll ist die Selbstkennzeichnung gut. Für die These, so wie sie dasteht, reicht die Evidenz nicht.

## 2. Stärkste Einwände gegen die Kernthese

Die These verschmilzt drei verschiedene Fehler. Bei `zero_traffic` fehlt der Referenzwert. Bei `db_down` steht er im Beleg (`db pool ready (0/20)`, `code/evidence.py`). Bei der Selbstauskunft ersetzt eine Behauptung den Beleg. Nur der erste Fall ist "fehlende Information". Der zweite ist ein Integrationsfehler unter einem grünen Statuswort. Der dritte ist Priming. "Bessere Information" erklärt sie nicht gemeinsam.

"Nicht mehr Prüfer" ist die unbelegte Hälfte. Die Korrelationsmessung, derentwegen das Panel gebaut wurde, ist nicht gelaufen (`notizen/21` §3, H-026, H-029). Die eigene Literaturstelle, die das Projekt als geprüft führt, sagt das Gegenteil der starken Lesart: Bei Ron u. a. senkt eine 3er-Mehrheit die Fehler von 387 auf 131, trotz 3,7-facher Ko-Fehler (`notizen/18-recherche-synthese.md` §1). Das steht in der Tabelle der schlechten Lesarten und fällt in §5 wieder heraus.

Der Spezifikationsbeleg, auf den H-033 und E-020 sich stützen, ist der schwächste Punkt der Kette. 54 % gegen 17 % vergleicht einen von den Autoren selbst für ungültig erklärten Lauf (Ground Truth mehrdeutig, n = 24 Urteile) mit späteren Läufen (`notizen/20` §10, `experimente/E-019-stapel-panel/ergebnis-stufe0.md`). Wer die 54 % als Modellfehler zählt, widerspricht der eigenen Entscheidung, den Lauf zu verwerfen. Wer sie als "das Modell hatte recht" liest, hat keinen Effekt mehr, sondern einen Hinweis, dass die Aufgabe ohne Sollwert nicht entscheidbar war.

E-018 zeigt, dass eine Regel, die Lügenstimmen keinen Hebel gibt, ehrliche Sonnet-Agenten kaum missbrauchen. Es zeigt nicht, dass ein zweiter Prüfer mit anderer Information weniger bringt als ein Sollwert. H-017, die näher an "ein zweiter Prüfer hilft nicht" liegt, ist in der Bestätigung geschrumpft und nicht bestätigt (`hypothesen.md`, Δ −0,033, KI schneidet 0).

"Aufmerksamkeitsmangel spielt kaum eine Rolle" engt Aufmerksamkeit auf Übersehen ein. Dieselbe Landkarte zeigt Fehlalarme von etwa 1,4 % im Einzelbeleg auf 15,7 % im Stapel (`notizen/20` §6). Der Stapel verändert das Urteil stark. Er verschiebt es zur Übervorsicht. Das ist ein Kontext- oder Kriterieneffekt und kein Beleg dafür, dass Aufmerksamkeit irrelevant ist.

## 3. Methodische Schwächen

**Abhängigkeit.** `landkarte.py` hängt alle gültigen Läufe aneinander und rechnet Wilson-Intervalle auf Urteilen. Dieselben Seeds laufen durch L1, L2 und L3, jeder Beleg in drei Kanälen. 3.312 Sonnet-Urteile sind nach den dokumentierten Seeds etwa 120 + 144 + 144 Belege, mehrfach beurteilt, nicht 3.312 unabhängige Aufgaben. Für `zero_traffic` ist der Erwartungswert sechs Belege pro Seed-Satz (12 Seeds, zwei Fehler-Arten, vier Fehlerarten gleich wahrscheinlich). n = 72 ist die Urteilzahl. Die Intervalle sind, wie die Datei selbst sagt, zu eng. Die Gedankenlandkarte zitiert danach Punktwerte ("Faktor 4–5", "53 %", "85 %") als stünden die Intervalle.

**Zirkuläre Materialkonstruktion.** D-016 erweitert den Generator um das Muster, das Sonnet in der Kalibrierung als einziges übersah, und erklärt dieses Muster dann zur Fehlerklasse. Innerhalb der Klasse streut die Übersehensrate von 2,5 % (`weights_broken`) bis 26 % (`db_down`). `amount_mismatch` liegt bei 6,7 % und wird als "Identität" geführt, obwohl auch dort eine Zahl dem Auftrag widerspricht (`notizen/20` §2–3). Die Spurtyp-Tabelle ist eine nachträgliche Beschriftung, kein unabhängiger Faktor. Die a-priori-Subtilität (1/2/3) sagt das Übersehen nicht voraus (§7).

**Konfundierungen, die schon vor E-020 im Befund stecken.** Reasoning "low" gegen "aus" ist nur im Stapel 12 gemessen (§4). Einzelbeleg und Stapel vergleichen zudem v2.1–v2.3 (§6). Die Konfidenzkurve poolt Einzelbeleg, Stapel, beide Materialstände und beide Reasoning-Stufen (§9). Die Spezifikationszeile poolt in den Arm "mit Sollwert" auch den Lauf ohne Reasoning. Ein Effekt, der nur in einer Zelle lebt, wird so zur Eigenschaft "des Prüfers".

**Statistik der bestätigten Experimente.** E-014 und E-018 sind sauberer: frische Seeds, gepaart, vorab festgelegt, große Effekte, Holm bzw. Permutation. Grenzen stehen in den Ergebnisdateien und gelten: ein Modell, ein Szenario, naive Mensch-Simulation (1,3 Fehlurteile pro Run, deshalb sieht die Abstimmung besser aus als der Mensch), Saboteure ohne Belegfälschung. E-013 ist ein Nullresultat eines Gates, das laut D-011 erst ab etwa 0,09 Punkten etwas sieht. "Prompt-Regeln bringen nichts" heißt dort: nichts Großes in sechs Iterationen nahe der Decke.

**Konstrukt- und externe Validität.** Jeder Kanal ist allein entscheidbar (D-014, Kommentar in `code/evidence.py`). Das ist für eine Korrelationsfrage richtig und für "echte Prüfung" falsch. Echte Prüfung ist oft gerade deshalb schwer, weil kein Kanal reicht. Die Ground Truth ist eine vom Generator gesetzte Boolesche Variable. Rund zehnmal lag der Generator falsch und das Modell richtig (`notizen/21` §6). Die verbleibenden "Fehlalarme" sind Urteile gegen diese Boolesche Variable, nicht gegen einen menschlichen Auditor. Eine Menschen-Baseline auf denselben Belegen fehlt. Haiku übersieht in E-017 K3 ähnlich wenig wie Sonnet (3,3 % gegen 3,9 %) und alarmiert häufiger (`notizen/20` §11). Die Decke auf dem Übersehen ist damit keine Sonnet-Leistung.

**Prävalenz.** Im Labor ist die Hälfte der Belege kaputt. `notizen/22-methodik-vorlesung.md` §11 rechnet selbst vor, dass 15 % Fehlalarm bei seltener Prävalenz fast alle Alarme falsch macht. Trotzdem wird die Eskalationskurve aus der 50-%-Mischung in Mensch-Minuten übersetzt (`notizen/20` §9b, `notizen/21` §2 Punkt 7).

**Synthetik und Autoridentität.** Generator, Prompt, Auswertung und Prüfer sind Claude. Die Fehlerspuren sind lokale String-Widersprüche: ein Buchstabe in der Adresse, ein verrutschtes Komma, `0/20`, Mean 100 statt 1. Das ist die Klasse, in der Sprachmodelle stark sind. Identitätsabgleiche liegen bei ≤ 1 % Übersehen, sobald der Sollwert im Auftrag steht. Die Decke ist auch eine Eigenschaft dieser Hypothesenklasse.

**Literatur als tragende Säule.** "Geprüft" heißt in `notizen/18`: ein Claude-Agent hat eine WebFetch-Zusammenfassung gegen die arXiv-Seite gehalten. Cluster E und F sind nicht gegengeprüft. "Volltext" ist dort ausdrücklich nicht das PDF. Darauf eine These über Dekorrelation zu stützen, ist ein Literaturreview mit bekanntem Common-Cause, nicht ein eigener Test.

## 4. Alternative Erklärungen

**(a) Decke in E-017 und E-019.** Die naheliegende Erklärung ist die Aufgabe, nicht ein allgemeines Prüftalent. Die Spur ist in jedem Kanal vollständig, das Rauschen wurde nach den ersten Läufen so bereinigt, dass es die Daten nicht mehr verändert, und Mehrdeutigkeit wurde entfernt, sobald das Modell sie beanstandete (`zero_traffic`, Chunk-Summen, SMTP-Widersprüche). Was übrig ist, sind entscheidbare Templates. Der Stapel bis 12 bei weiterhin kurzem Log ist eine schwache Aufmerksamkeitsmanipulation: kein Zeitlimit, kein echter Langkontext, keine Unterbrechung. Ein Positionseffekt auf die Fehlerrate fehlt (`notizen/20` §8); das spricht gegen simples Ermüden und lässt offen, ob Übersehen und Fehlalarm sich über die Position verschieden verhalten. §8 poolt beides. Zusätzlich kann das Modell Referenzwissen mitbringen (ein Pool mit 0 aktiven Verbindungen ist verdächtig, Survey-Gewichte liegen um 1). Dann ist "Sollwert nicht im Auftrag" nicht gleich "Information fehlt". Unsicher bin ich bei dem Anteil, den Vorwissen trägt. Das ist ohne Ablation nicht getrennt.

**(b) Reasoning erhöht Fehlalarme.** Vier Lesarten sind mit denselben Tabellen verträglich. Erstens ein Kriterienshift: Mit Reasoning werden harmlose Auffälligkeiten verbalisiert (Timeout mit Retry, Greylisting, Deprecation), und die Ground Truth nennt `ok_noisy` trotzdem intakt. Dieselbe Pipeline hat solche "Fehlalarme" schon mehrfach nachträglich als Generatorfehler anerkannt. Zweitens ein Interaktionseffekt mit dem Stapel: Der Kontrast existiert nur bei B = 12. Reasoning kann den Verdacht von einem kaputten Item auf die Nachbaritems übertragen. E-020 prüft Einzelbelege und damit einen anderen Estimanden. Drittens sind "low" und "aus" möglicherweise nicht dasselbe Modell mit einem Schalter. Ob OpenRouter dabei Checkpoint, Systemprompt oder Tokenbudget wechselt, habe ich nicht geprüft. Viertens ist die Zusammenfassung "ohne mehr echte Fehler zu finden" auf v3 schief: dort fällt das Übersehen von 0,069 auf 0,037, wenn Reasoning aus ist (`notizen/20` §4). Die Intervalle überlappen, die Richtung ist nicht stabil, und "kauft nichts" ist stärker als die Daten.

**(c) Konfidenz-Eskalationskurve.** Die Kurve ist monoton und damit ein Kandidat, mehr nicht. Die Schwellen sind auf denselben Urteilen gewählt, auf denen die Fangquote berichtet wird. Dieselben schweren Belege gehen mehrfach ein und können beide Seiten der Kurve tragen: viele Fehler und niedrige Konfidenz. Eine Regel "eskaliere `db_down` und `zero_traffic`" könnte denselben Fang liefern. Das ist nicht gegengerechnet. E-016 ist keine unabhängige Bestätigung: ebenfalls explorativ, abgebrochen, die Fehler stammen vor allem von Grok und DeepSeek. Die Annahme, der Mensch sei auf den eskalierten Belegen fehlerfrei, macht aus der Kurve eine Obergrenze (`notizen/20` §9b). Dazu kommt die Literatur, die das Projekt selbst zitiert: Unter Druck und bei schweren Items sind Modelle konfident falsch. Ob die Konfidenz nur ein Stil-Token (0,6 / 0,8 / 0,9) ist, kann ich ohne die jsonl nicht sagen. Ebenfalls ungeprüft: ob Reasoning die Konfidenz systematisch nach unten verschiebt. Dann sind Fehlalarm-Effekt und Eskalationskurve teilweise dasselbe Phänomen, zweimal gezählt.

## 5. E-020 vor dem Start

Die beiden Sätze gehören nicht in den Hauptprompt. Sie sollten auch kein voller fünfter Faktor sein.

`Use the available tools to look at the system before you decide` steht nur bei ZUGANG = 1. `You can look up the runbook for expected values and conventions` steht nur bei SPEC = 1 (`code/realitaet.py`, `build_prompt`). Jeder Satz ist mit genau einem Faktor vollständig konfundiert. H-033 behauptet, der Prüfer schlage nicht nach. H-035 behauptet, unter Selbstauskunft werde weniger abgefragt. Die Sätze weisen das Verhalten an, dessen Ausbleiben die Hypothese ist. Gemessen wird dann Befolgung einer Anweisung. Zusätzlich sagt der Zweig ZUGANG = 0 immer "and what you can look up", auch wenn kein Werkzeug existiert. Das ist ein dritter, nicht präregistrierter Anstupser. In `prereg.md` steht zum Prompt nur "Rahmen wie E-017 S0". Den E-017-Prompt habe ich hier nicht. Die Behandlungstexte stehen im Code und nicht in der Präregistrierung. `notizen/22` §2 benennt genau das als Forscher-Freiheitsgrad.

Ein 2⁵-Design verdoppelt den Lauf, vermischt zwei verschiedene Sätze zu einem Faktor und verwässert V1, V2 und V6. Die Frage "rettet ein Satz das Nachschlagen?" ist eine andere Frage. Wenn sie gestellt werden soll, dann als vorab festgelegter Nebenarm nur bei SPEC = 1, auf einem Teil der Seeds, außerhalb des Primärmodells. Die Entscheidung muss vor dem Piloten fallen. Das Pilotkriterium "Werkzeug mindestens einmal benutzt" ist mit den Sätzen fast automatisch erfüllt und sagt dann nichts über die Manipulation.

Unabhängig davon würde ich das Design an diesen Stellen ändern:

- `lookup_runbook` gibt unabhängig vom Topic das ganze Runbook zurück (`_run_tool`). Ein Aufruf ist der Antwortschlüssel. V4 hat dann kaum Varianz, sobald der Satz das Werkzeug erwähnt. Entweder abschnittsweise antworten, mit einem Distraktor und einer falschen Topic-Antwort, oder V4 als Mechanismusanspruch streichen.
- SPEC = 1 fügt das Werkzeug hinzu, SPEC = 0 hat keins. Das ist in der Präregistrierung benannt und trotzdem der zentrale Kontrast. Sauberer: Das Werkzeug ist in beiden Stufen da. Bei Stufe 0 liefert es nur, was schon im Auftrag steht.
- Referenzwerte lecken in die Kanäle. `schema: {cols}/47` und `read raw/...: 47 columns` enthalten die 47 auch im Kurzauftrag. `cache connected (0/4 shards)` und `db pool ready (0/20)` enthalten den Sollwert im Beleg. Für diese Fehlerarten kann Nachschlagen nichts mehr ändern. Der einzige saubere SPEC-Fall im Generator ist `zero_traffic` (Rate nur im Auftrag) und teilweise `weights_broken` und `duplicates_kept`. V1 mittelt über alle kaputten Belege und damit über viele strukturelle Nullen. Die präregistrierte Primärmetrik sollte die vorab benannte anfällige Klasse sein.
- V6 repliziert den Stapelbefund nicht. Entweder die Hypothese auf Einzelbelege umschreiben oder einen Stapel-Arm vorsehen. Ein Nullresultat im Einzelbeleg widerlegt §4 der Landkarte nicht.
- Die Nicht-Unterlegenheit in V6 nennt keine Intervallstufe. 90 % und 95 % sind verschiedene Tests.
- `report()` in `realitaet.py` ist eine Zellentabelle. Den Cluster-Bootstrap, die Paarung und die Ausschlussregel gibt es als Prosa in der Präregistrierung und nicht als eingefrorenes Skript.
- Kanal = Seed mod 3 ist nicht nach Fehlerart geschichtet. `joblog` und `ledger` sind in der Landkarte die Fehlalarm-Kanäle. Bei seltenem Übersehen verschiebt das den Haupteffekt.
- "Ground Truth bleibt hart" dosiert Zugriffskosten, nicht Realität. Der interessantere Fall, mehrdeutige Sollwerte, bei denen das Modell und der Generator auseinanderfallen, ist per Design ausgeschlossen.
- 4.608 Aufrufe mit bis zu sechs Werkzeugrunden für 30–50 $ ist optimistisch. Die Abbruchregel "über 60 $, dann Rücksprache" lässt einen halben Lauf zu, aus dem man danach eine Geschichte bauen kann. Vorher festlegen, welche Kontraste bei Abbruch noch berichtbar sind und welche nicht.

## 6. Was übersehen wird

Der Generator definiert die Welt, die der Prüfer können muss. Nach jedem Widerspruch wurde die Welt an das Modell angepasst, nicht die Metrik an die Mehrdeutigkeit. Die Decke ist auch das Ergebnis dieser Auswahl.

Es gibt keine dumme Baseline. Ein Abgleich von Auftrag und Signaturzeile, ohne LLM, würde zeigen, welcher Teil der "Prüfleistung" Stringvergleich ist. Haiku gegen Sonnet auf dem Übersehen legt nahe: fast alles.

Die Policy-Schlüsse laufen der Evidenz voraus. `notizen/21` §5 sagt, Wave brauche schon jetzt Sollwerte in jedem Ticket, ferngehaltene Selbstauskunft und Eskalation nach Konfidenz. Das sind die offenen Hypothesen H-033, H-034 und die unbestätigte Kurve.

Langzeit, Kollusion, geteiltes Gedächtnis und Fremdmodelle in Teams stehen als Lücken im Dokument und fehlen in der These. Die These ist eine Aussage über Organisationen. Die Daten sind Einzelurteile über kurze, synthetische Logs plus zwei Kurzläufe mit geskripteten Maulwürfen.

Kritiker-Unabhängigkeit ist als Kästchen offen und wird praktisch nie scharf. Design, Literaturprüfung, Generatorreparatur und Prüfer sind eine Modellfamilie. Ein zweites Modell, das die Ground Truth einer Stichprobe neu bewertet, fehlt. Genau dort ist das Projekt schon zehnmal umgefallen.

Die Kernmetrik "Verlässlichkeit pro Mensch-Minute" wird nie gemessen. Eskalationsanteil ist keine Zeit, der Mensch ist perfekt gesetzt, die Prävalenz ist die des Labors.

## 7. Was ich als Nächstes täte

1. E-020 nicht starten, bevor der exakte Prompt in der Präregistrierung steht, die beiden Sätze und der Look-up-Halbsatz draußen sind, das Runbook nicht mehr das ganze Soll auf einen Aufruf herausgibt, und das Auswerteskript inklusive Cluster-Einheit und Abbruchregel eingefroren ist. Primärmetrik auf die Fehlerarten legen, deren Sollwert wirklich nur im Auftrag steht.
2. Die vorhandenen Urteile neu rechnen, an Belegen statt an Urteilen, getrennt nach Lauf. Drei Kontraste reichen: Reasoning nur innerhalb Stapel 12 und gepaart; Konfidenz gegen eine Spurtyp-Regel; die Eskalationskurve getrennt nach Reasoning und Modus. Wenn die Kurve den Spurtyp nicht schlägt, ist Punkt 7 der Gedankenlandkarte erledigt, bevor weiteres Geld in dieselbe Konfidenz fließt.
3. Eine kleine, vor dem Sehen festgelegte Kodierung echter Wave-Fälle, mit zweitem Kodierer. Nicht 10–20 frei interpretierte Anekdoten. Dieselbe Frage wie im Labor: War der Sollwert da, war der Beleg da, war eine Selbstauskunft davor, und war das Urteil konfident falsch? Solange das nicht existiert, bleibt jede Übertragung auf Wave eine Hypothese.

## 8. Was gut ist

Die Zwei-Stufen-Regel wird an der eigenen empfindlichsten Stelle eingehalten: H-017 bleibt widerlegt, E-017 und E-019 bleiben ohne Hauptlauf, Generatorfehler werden als ungültig markiert statt umetikettiert. E-014 und E-018 haben große, vorab festgelegte Effekte und nennen den Konstruktionsanteil von E-018 ausdrücklich. D-014, jeder Kanal allein entscheidbar, ist die richtige Kontrolle für die Frage, die das Panel eigentlich stellen sollte. Die Tabelle guter und schlechter Lesarten in `notizen/21` §4 ist genauer als die These, die darunter steht.
