# Dritter Prüfer: drei Lesarten derselben Daten (23.10.2026, abends)

**Anlass.** Neo: "Sollte das ein dritter Prüfer, also eine neue Session, gegen unsere Daten halten?" Gemeint ist ein Prüfer, dessen Kontext nicht mit unseren Thesen gefüllt ist (Neos Kontext-Drift-Gedanke, `notizen/parkplatz.md`).

**Aufbau, strikt getrennt:**
- **Recherche** (`recherche/`): Subagent mit frischem Kontext, eigener Ordner außerhalb des Repos, sechs neutrale Fragen.
- **Prüfer 3a** (`claude-frisch/`): ein Claude mit frischem Kontext.
- **Prüfer 3b** (`gpt/`): GPT-6.1 Sol. GPT schrieb ein Skript, Claude las es und führte es isoliert aus (`python -I`), danach deutete GPT seine Ausgabe selbst.
- Beide Prüfer sahen nur:
  - Rohdaten-Kopien (E-020, E-023, E-024 unter neutralen Dateinamen)
  - die neutrale Datenbeschreibung (`README_DATEN.md`)
  - den Methodenbericht der Recherche
  - die von Neo gegengelesenen Fragen (`claude-frisch/FRAGEN.md`)
- Keine Ergebnisse, Hypothesen, Notizen oder Laborbuch.

**Lecks, offen benannt:**
- Der Recherche-Agent sah beim Start automatisch eine Zeile aus Claudes Gedächtnis-Index mit Experiment-Kürzeln und Statuswörtern. Er gibt an, sie nicht verwendet zu haben.
- Vor dem Start von 3a wurde diese Zeile neutralisiert.
- 3a gibt an, vorher nur die Datenstruktur und die Randverteilung der GPT-Datei gesehen zu haben.

## Wo beide Prüfer übereinstimmen (und mit Claudes Lesart)
| Befund | 3a (Claude frisch) | 3b (GPT) | Claude (E-023/E-024) |
|---|---|---|---|
| Sonnet 97,6 / 97,0 % richtig, Haiku 91,0 / 90,3 %, Abstand in beiden Seed-Sätzen gleich | ja | ja | – |
| **Größter Effekt: Haiku bei SP = 1 *und* ZU = 1**, auch auf der Logit-Skala (Wechselwirkung −2,6 / −2,2) | ja | ja | ja (C1/C2) |
| Haiku übersieht spec-reine Fehler fast nur, wenn es nicht nachschlägt (mit 93 % richtig, ohne 2–4 %) | ja | ja | ja (V4) |
| Beide Modelle fragen bei ZU = 1 alle drei Kanäle ab. Der Unterschied liegt im Nachschlagen des Maßstabs | ja | ja | ja |
| Sonnets Fehler sitzen fast nur bei ZU = 0, bei `db_down`/`low_traffic`, und Zugang behebt sie | ja | ja | ja (Materialbefund E-020) |
| "All checks green" macht Haiku misstrauischer, nicht gefälliger | ja | ja | ja (F1, Deutung offen) |
| Das GPT-Einzelkanal-Label ist mit GPTs Urteilsneigung vermengt ("nicht entscheidbar" = immer "kaputt") | ja | ja | **nein, übersehen** |

## Wo die Prüfer Claudes Lesart korrigieren oder schärfen
1. **SP allein schadet Haiku kaum.** Bei ZU = 0 kostet der fehlende Sollwert Haiku nur −0,7 pp. Der gesamte "V1-Effekt" (+0,26) kommt aus der Kombination mit dem Kanal-Werkzeug (ZU = 1: −15 pp).
   - Claudes Ergebnistext zu E-024 nannte das zwar ("Schaden nur, wenn Maßstab fehlt" plus Diagnose), V1 wurde aber als eigenständiger Befund ("fehlender Sollwert → mehr Übersehen") berichtet.
   - **Genauer:** Für Haiku ist "Sollwert fehlt" nur dann schädlich, wenn gleichzeitig Daten-Werkzeuge da sind.
2. **Die Kompetenzgrenzen-These (Neo) wird von beiden nicht gestützt.**
   - Eine naive Analyse (Schwierigkeit aus denselben Daten) erzeugt das Muster "Effekt bei schweren Belegen". Die Nullsimulation von 3a erzeugt es genauso stark: **Regression zur Mitte**.
   - Mit unabhängigen Schwierigkeitsschätzern (anderer Seed-Satz, anderes Modell, Kreuzanpassung) hängt die Wirkung **an der Fehlerart und am Mechanismus** (braucht es einen Sollwert? ist der vorgelegte Kanal informativ?), nicht an einer allgemeinen Schwierigkeitsachse.
   - Subtilitätsstufen des Generators zeigen praktisch keine Wirkung.
   - **Wichtig für die Zukunft:** Diesen Zirkelschluss hätte Claude ohne die Recherche leicht selbst gebaut.
3. **Keine einheitliche Schwierigkeitsskala.** Die Typ-Schwierigkeit ist je Modell über die Seed-Sätze sehr stabil (r 0,93 / 0,95), zwischen den Modellen nur mäßig ähnlich (r ≈ 0,5, attenuationskorrigiert 0,54). Haiku hat eigene Fehlermodi, etwa Kontakt und Zahlungsziel ohne Nachschlagen.
4. **Fehlerkorrelation ist überwiegend geteilte Typ- und Kanalschwierigkeit.**
   - Roh κ 0,22 / 0,28, gemeinsame Fehler 6,5-mal so häufig wie unter Unabhängigkeit.
   - Nach Schichtung über Typ × Zelle: κ 0,13 / 0,17, Double-Fault-Verhältnis 1,8 (3a).
   - Ein perfekter Schiedsrichter zwischen beiden Modellen brächte nur etwa +1 pp über Sonnet (3b).
   - **Folge für Redundanz (Hinweis):** Haiku als *schwächerer* Zweitprüfer *derselben Familie* bringt neben Sonnet hier fast nichts. Ein gleich starker Zweitprüfer einer anderen Familie wurde nie getestet.
5. **Neu (3b):** Die Selbstauskunft senkt Haikus Nachschlagen um 11–12 pp, in beiden Seed-Sätzen.
6. **Neu (3a, explorativ):** Haiku verpasst die spec-reinen Fehler mit *höherer* Konfidenz als die erkannten. Das ist glückliches Vertrauen im Kleinen (H-041).
7. **Neu (3a):** Die Entscheidung, nachzuschlagen, ist bei Haiku nur mäßig belegkonsistent (κ 0,48–0,64 zwischen AU0 und AU1). Es ist teils Zufall, ob Haiku nachschlägt.

## Was das für die Thesen heißt
- **H-039 (Verdrängung)**: von beiden unabhängig gestützt, auch auf der Logit-Skala. Kausal ist nur der Zusammenhang mit dem Werkzeugformat gezeigt. Ob "mehr Information" oder "Format" wirkt, ist im Design vermengt. Ein Test wäre eine Bedingung, die das Nachschlagen erzwingt.
- **H-038 (Wechselwirkung Modell × Harness)**: Die Wechselwirkung ist robust. Das in H-038 behauptete Muster einer *Fähigkeitsschwelle* bzw. die Kompetenzgrenzen-Lesart ist **nicht gestützt**. Die Wirkung ist mechanismus- und fehlerartspezifisch.
- **Neos Kompetenzgrenzen-These**: In diesen Daten nicht gestützt. Das ist kein Widerlegen, denn Sonnet liegt an der Decke, und es gibt nur 6 Belege je Fehlerart und Art. Die naheliegendere Lesart (Hinweis) ist: Es kommt darauf an, welche Information für den Fehler nötig ist und ob das Modell sie sich holt.
- **Fehlerkorrelation (Hinweis):** Was beide Modelle gemeinsam verfehlen, liegt vor allem bei uninformativen Einzelkanälen. Diese waren aber teils ein Fehler unseres eigenen Generators: Die fehlende Information ist hier zum Teil eingebaut. Es passt zu Neos Gedanken "Informationsmangel als Fehlerquelle". Ob andere Information besser dekorreliert als ein anderes, gleich starkes Modell, ist **nicht getestet**.

## Methodisch gelernt
- **Der dritte Prüfer hat sich gelohnt.** Zwei unabhängige Lesarten kamen zum selben Kern und haben Claude an drei Stellen korrigiert: V1 als Wechselwirkung, die Kompetenzgrenze als Artefakt-Risiko, das GPT-Label als vermengt.
- Ohne die Recherche zur Regression zur Mitte hätte die naheliegende Analyse die Kompetenzgrenzen-These scheinbar bestätigt.
- Kosten: Recherche und Prüfer 3a über das Abo, Prüfer 3b über OpenRouter (wenige Dollar).

## Status der Kernaussagen (Korrektur 23.10. 23:01, nach Neos Nachfrage "kann man das einfach behaupten?")
Claude hatte die Aussagen im Gespräch unter der Überschrift "Was wir jetzt wissen" formuliert. Das war zu stark (Regel 15). Gültiger Status:

| Aussage | Status | Warum nicht stärker |
|---|---|---|
| Fehler entstehen vor allem durch fehlende Information | **Hinweis** | Bei Sonnet teils hausgemacht (Generatorfehler: uninformative Einzelkanäle). Bei Haiku ist der Zusammenhang mit dem Nachschlagen beobachtet, nicht kausal (Nachschlagen nicht erzwungen) |
| Ein zweites Modell hilft kaum, andere Information viel | **Hinweis, zweiter Teil schwach** | Nur Haiku als schwächerer Zweitprüfer derselben Familie. "Andere Information" stützt sich auf +4 pp bei Sonnet, ohne Vorhersage, zur Hälfte Materialartefakt |
| Formulierungen wirken nicht, Information wirkt | **für Sonnet im Labor gestützt, für Haiku falsch** | Bei Haiku wirkt "All checks green" (Nachschlagen −11 bis −12 pp, Fehlalarme +). Sonnet nur im sauberen Labor mit einem Fall |
| Kompetenzgrenze ist es eher nicht | **in diesen Daten nicht gestützt** | Nicht widerlegt: Sonnet an der Decke, 6 Belege je Fehlerart, schmale Schwierigkeitsspanne |

**Bestätigt** (vorab festgelegt, frische Seeds, verblindet, nachgerechnet) ist nur: Bei Haiku 5.5 führen fehlender Sollwert plus Daten-Werkzeuge zu deutlich weniger Nachschlagen und deutlich mehr Übersehen (E-024).

**Übereinstimmung dreier Auswerter** heißt nur, dass die Auswertung robust ist. Es ist keine weitere Bestätigung, denn alle haben dieselben Daten gesehen.

**Was fehlt, um 1–3 zu behaupten:**
1. Material mit geprüft entscheidbaren Einzelkanälen und ein Arm, der das Nachschlagen erzwingt.
2. Ein gleich starker Zweitprüfer anderer Familie gegen einen Zweitprüfer mit anderer Information, im direkten Vergleich.
3. Sonnet unter realistischen Bedingungen (langer Kontext, mehrere Fälle).
4. Für alles: echte statt synthetischer Aufgaben.
