# Reflexivität: was wir an uns selbst beobachtet haben

> **Korrektur 23.10. (E-021, Manipulationscheck):** Was hier "Reasoning aus" heißt, war in Wahrheit die **Standardeinstellung mit adaptivem, verborgenem Reasoning** (OpenRouter: Reasoning ist bei Sonnet 5.5 nicht abschaltbar). "Reasoning low" war **gedrosseltes** Reasoning. Alle Aussagen "Reasoning erhöht Fehlalarme" sind deshalb umzudrehen: **Gedrosseltes Reasoning erhöht Fehlalarme** (H-037). Details: `experimente/E-021-reasoning-fehlalarme/ergebnis.md`.

**Stand:** 23.10.2026 · **Art:** Erfahrungsbericht bzw. Fallstudie (n = 1 Projekt), qualitativ. **Kein Befund und kein Beleg für eine Hypothese**, nur Hypothesenquelle (CLAUDE.md: Wissen aus dem eigenen System gilt als Hypothesenquelle).

**Anlass:** Neos Frage, ob es ein Fehler ist, dass der Forscher selbst zum Experiment wird, oder eine Beobachtung. Antwort: Es ist eine Beobachtung, *wenn* sie gekennzeichnet, dokumentiert und von den Ergebnissen getrennt ist. Dieses Dokument ist diese Trennung.

---

## 1. Wie wurden unsere Fehler gefunden?

**Quelle:** Laborbuch (20.–23.10.), Ergebnisdateien, `notizen/23` (Grok-Gutachten), Verifikation in `notizen/18`. Gezählt sind nur **dokumentierte** Fehler von Claude (Code, Material, Design, Aussagen).

**Auslöser-Kategorien:**
- **Regel/Prozess:** Stichprobe (Kriterium 5), Audit, Pilot, Dry-Run, Tests, Prüfagent, präregistrierte Vorhersage, Quellencheck
- **davon mit Modellwiderspruch:** Die Prüfer-Modelle urteilten "falsch", und die Stichprobe zeigte, dass das Modell recht hatte
- **Externer Kritiker:** Grok
- **Mensch oder anderer Agent mit Systemwissen:** Neo, Ace
- **Selbst, ohne äußeren Anstoß:** Claude bemerkt es beim erneuten Lesen
- **Absturz:** Exception, Programm bricht ab

| # | Fehler | Auslöser | Art |
|---|---|---|---|
| 1 | Handoff-Annahmen zu Harness² (Single-Agent, Rekursion) | Regel: Quellencheck | Aussage |
| 2 | E-012 Absturz (Windows-Temp-Ordner) | Absturz | Code |
| 3 | Uhrzeiten im Laborbuch geschätzt und falsch | selbst (Dateizeitstempel) | Dokumentation |
| 4 | Session-Limit-Ausfälle als Ergebnisse gezählt (E-008, 8 Runs) | Regel: Audit, angestoßen durch auffälligen Wert | **Messung** |
| 5 | Vorab formulierte Abwehr Q3 (Quorum 3 schützt) falsch | Regel: präregistrierte Vorhersage gegen Daten | Annahme |
| 6 | Kostenmetrik 3,6× zu hoch | unklar (im Laborbuch kein Auslöser notiert) | Messung |
| 7–9 | E-016-Pilot: 3 Generatorfehler, dazu meine falsche Deutung "alle 8 Familien irren gemeinsam" | Regel: Pilot, **mit Modellwiderspruch** | **Ground Truth** |
| 10 | Ledger-Lesen unter Parallelität | Absturz | Code |
| 11–13 | Website-Vorschlag: AES-256 ohne Grundlage, "Clarify" falsch, Maxwell-Pfad | anderer Agent (Ace, Faktencheck aus dem Code) | Aussage |
| 14 | "Memory ist wahrscheinlich der stärkste Dekorrelations-Hebel" | Regel: Recherche (Cluster E widersprach) | Aussage |
| 15–16 | Zwei selektiv zitierte Spannen in der Recherche | Regel: Prüfagent (gleiche Familie, andere Rolle) | Aussage |
| 17–18 | E-017 K1: Rauschen veränderte Daten, Prozentzahl falsch | Regel: Stichprobe, **mit Modellwiderspruch** | **Ground Truth** |
| 19 | E-017 K3: Chunk-Summen | Regel: Stichprobe, **mit Modellwiderspruch** | **Ground Truth** |
| 20 | S2-Verfahren stand nach dem Beleg ("commit first" unmöglich) | Regel: Dry-Run gelesen | Design |
| 21–23 | E-019 L1: 3 Fehler in Routinezeilen | Regel: Stichprobe, **mit Modellwiderspruch** | **Ground Truth** |
| 24 | `zero_traffic` ohne Sollwert, Ground Truth mehrdeutig | Regel: Stichprobe, **mit Modellwiderspruch** | **Ground Truth** |
| 25 | Testdatei durch Escape-Fehler beschädigt | Regel: Tests liefen rot | Code |
| 26 | Test-Zuordnung vertauscht (hätte nichts geprüft) | selbst | Code |
| 27 | Kriterium 4 schlecht konstruiert | selbst, angestoßen durch Daten | Design |
| 28 | "bei gleicher Übersehensrate" | selbst (Tabelle erneut gelesen) | Aussage |
| 29 | "6× falsch gewertet" (tatsächlich ~10) | selbst | Aussage |
| 30–39 | Grok: These zu stark; 54 % aus ungültigem Lauf; abhängige Urteile; zirkuläres Material; Prävalenz ignoriert; V6 anderer Estimand; Runbook als Antwortschlüssel; Sollwert-Leaks; dritter Anstupser; Auswerteskript nicht eingefroren | **externer Kritiker** | Design, Aussage |
| 40–41 | "Inception-Gefühl könnte ein Gesprächsartefakt sein"; "Decke als 'zu leicht' zu behaupten wäre unbelegt" | Mensch (Neo) | Deutung |

**Zählung (gerundet, die Kategorien überlappen teilweise):**

| Auslöser | Anzahl | davon Design- oder Ground-Truth-Fehler |
|---|---|---|
| Regel/Prozess | 18 | 13 (darunter alle 10 Ground-Truth-Fehler) |
| davon mit Modellwiderspruch | 10 | 10 |
| Externer Kritiker (Grok) | 10 | 8 |
| Mensch oder anderer Agent | 5 | 0 (aber 2 Rahmen- bzw. Deutungsfehler) |
| Selbst, ohne äußeren Anstoß | 5 | 1 (Kriterium 4, durch Daten angestoßen) |
| Absturz | 2 | 0 |
| unklar | 1 | – |

### Was man daraus ablesen kann (und was nicht)
- **Beobachtung:**
  - Die *schweren* Fehler (falsche Ground Truth, Designfehler, die ein Experiment entwertet hätten) wurden **fast alle von Regeln, Modellwidersprüchen oder einem externen Kritiker** gefunden.
  - Was ich ohne Anstoß selbst fand, waren überwiegend Zählungen, Formulierungen und Zeitangaben.
  - Das passt als **Fallbeispiel** zu H-023 (ehrliche Überbehauptung wird von außen korrigiert) und zur These von billiger Prüfung. Es **belegt** keines von beiden.
- **Dunkelziffer:** Gezählt ist nur, was gefunden wurde. Fehler, die keine unserer Kontrollen sieht, fehlen per Definition. Vor allem fehlen Fehler, die Prüfer-Modell *und* Generator gleich machen (H-026 auf Ebene des Forschungsprozesses).
- **Selbstauskunft:** Diese Tabelle hat Claude über Claudes Fehler geschrieben. Die Einordnung "selbst gefunden" und "schwer" ist meine. Eine unabhängige Kodierung (Neo oder ein Fremdmodell, anhand des Laborbuchs) wäre die saubere Version.

---

## 2. Andere Modelle als Mitspieler: hilft das? (Neos Frage, 23.10.)

**Kurz:** Ja, gegen "Claude prüft Claude". Aber nur, wenn der Harness wirklich gleich ist, und selbst dann nicht vollständig.

**Wo es schon geht:**
- **Prüfer-Experimente** (`panel.py`, `factorial.py`, `batch.py`, `realitaet.py`) laufen über OpenRouter. Das Modell ist nur ein Parameter: gleiche Prompts, gleiche Werkzeuge (OpenAI-Tool-Format), gleiche Auswertung.
- E-016 hatte so schon 8 Modelle aus 5 Familien. Grok über die API (nicht die Grok-Build-CLI, die ist ein eigener Harness) ließe sich hier ohne Umbau einsetzen.

**Wo es Code braucht:**
- Die **Team-Spiele** (`orglab/runner.py`) laufen über `backends/agent_sdk.py`, also das Claude Agent SDK. Andere Modelle können dort nicht mitspielen.
- Die Schnittstelle ist aber vorbereitet (`backends/base.py`: "später mit der Messages API … oder geskripteten Policies").
- Nötig ist ein **OpenRouter-Backend** mit derselben Welt, denselben Werkzeugen und derselben Rundenlogik.
- **Wichtig:** Für einen fairen Vergleich muss dann auch **Claude über dieses neue Backend** laufen, nicht über das SDK. Das SDK bringt eigenes Gerüst mit, und dann wäre der Harness nicht mehr gleich. Die bisherigen SDK-Ergebnisse (E-001 bis E-018) wären die Referenz, kein Vergleichsarm.

**Warum gleicher Code nicht ganz reicht (Harness × Modell):**
1. **Heimvorteil:** Alle Prompts wurden mit Claude geschrieben und an Claude-Verhalten debuggt. Sie könnten Claude begünstigen. Gegenmittel: Prompt-Paraphrasen als Robustheitscheck, oder ein Prompt, den ein Fremdmodell bzw. ein Mensch gegenliest.
2. **Werkzeug- und Formatkonventionen** unterscheiden sich (Tool-Calling, JSON-Treue, Kontextlänge). Gegenmittel: ein Pilot pro Modell mit Parse- und Ausfallkriterien, wie bei E-020.
3. **"Reasoning low/aus" heißt bei jedem Anbieter etwas anderes.** Gegenmittel: Reasoning nur innerhalb eines Modells vergleichen, nie zwischen Modellen.
4. **Kalibrierung pro Modell:** Die Decke liegt je Modell woanders (D-010).
5. **Literatur:** Es gibt keinen universell besten Harness. Harness-Varianz und Modellwahl interagieren (`notizen/18`, Cluster C). Unterschiede zwischen Modellen sind deshalb immer "Modell *in diesem* Harness".

**Welche Rolle zuerst unabhängig machen?** Drei Rollen sind bisher Claude:
- **Kritiker** (seit 22.10. teilweise Grok)
- **Ground-Truth-Kontrolle** (Generator, Stichprobe)
- **Probanden**

Für die Glaubwürdigkeit am wichtigsten ist die **Ground-Truth-Kontrolle**, denn dort sind wir zehnmal umgefallen. Ein Fremdmodell oder ein Mensch beurteilt blind eine Stichprobe von Belegen, bevor ein Hauptlauf startet. Fremde Probanden bringen vor allem **Generalisierung** (H-002) und erst danach Unabhängigkeit.
