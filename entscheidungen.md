# Entscheidungs-Log

Status: `vorgeschlagen` · `angenommen` · `ersetzt durch D-xxx`

---

## D-001: Eigener schlanker Optimierungs-Loop statt Harness²-Umbau
- **Datum:** 2026-10-20 · **Status:** vorgeschlagen
- **Kontext:** Wir wollen eine Org-Konfiguration optimieren (Rollen, Topologie, Gedächtnis, Normen). Harness² optimiert einen einzelnen Agenten über acht Dateien pro Agent.
- **Optionen:** (a) Harness² multi-agentisch umbauen. (b) Eigenen Loop bauen, der das Propose-Probe-Compose-Prinzip übernimmt. (c) Harness² unverändert pro Agent laufen lassen.
- **Wahl:** (b). Harness² bleibt Referenz und möglicher Vergleichsarm.
- **Begründung:** Der Umbau wäre tief, weil Probes und Composer auf einen einzelnen Agenten ausgelegt sind. Unsere Szenarien haben echte Verifier, die Harness² nicht nutzt.

## D-002: Zuerst Regime vergleichen, dann den Optimierer bauen
- **Datum:** 2026-10-20 · **Status:** vorgeschlagen
- **Kontext:** Es gibt zwei Ebenen von Selbstregulierung: zur Laufzeit (online) und zwischen Runs (offline, Optimierer).
- **Wahl:** Zuerst die Regime A–D auf mindestens zwei Modellen gegeneinander messen, danach den Optimierer (E) bauen.
- **Begründung:** Der Optimierer braucht ein verlässliches Messsignal. Der Vergleich testet nebenbei H-002 (Modellabhängigkeit).

## D-003: Ace- und Wave-Wissen gilt als Hypothesenquelle, nicht als Beleg
- **Datum:** 2026-10-20 · **Status:** angenommen (Neo: "nicht alte Fehler wiederholen, weil wir denken, das was wir gebaut haben ist bewiesen smart")
- **Konsequenz:** Ace-Aussagen landen als Hypothesen in `hypothesen.md`. Belege gibt es erst durch Rohdaten oder eigene Experimente.

## D-004: Dokumentation nach Labor-Prinzip
- **Datum:** 2026-10-20 · **Status:** angenommen (Neos Wunsch)
- **Wahl:**
  - Laborbuch, in das nur angehängt wird.
  - Hypothesen-Register.
  - Entscheidungs-Log.
  - Präregistrierung vor jedem Experiment.
  - Unveränderliche Rohdaten.
  - Auswertung nur per Skript.
  - Git.
- **Begründung:** Später soll exakt nachvollziehbar sein, was getan wurde. Das ist die Basis für Blog und Paper. Die Präregistrierung schützt vor Selbsttäuschung.

## D-005: Ein Level drüber – Szenarien testen Koordinationsmuster, nicht Domänen
- **Datum:** 2026-10-20 · **Status:** angenommen (Neo: "bei Ace sind es oft Coding-Sachen, aber daraus ergeben sich Meta-Probleme")
- **Wahl:**
  - Jedes Szenario wird als abstrakter Mechanismus definiert, z. B. "Erfolgssignal misst Handlung statt Wirkung".
  - Der Mechanismus wird dann in mehreren Domänen instanziiert: Coding, Business-Ops, Recherche.
  - Die Domäne wird damit zur Kontrollvariable.
- **Begründung:** Wir wollen Org-Mechanismen finden und keine Coding-Tricks. Wenn eine Intervention nur in einer Domäne wirkt, ist sie ein Domänen-Fix und kein Social-Skill-Modul.

## D-006: Laufzeit über das Claude Agent SDK mit Subscription, Basismodell Sonnet 5.5
- **Datum:** 2026-10-20 · **Status:** angenommen (Neo)
- **Konsequenzen:**
  - Alle Modelle kommen aus einer Familie (Claude). H-002 ist damit nur als **Vergleich der Stufen innerhalb der Familie** testbar (Haiku / Sonnet / Opus 5.5). Das passt gut zu H-012, der Fähigkeitsschwelle. Ein Vergleich über Familien hinweg bleibt eine spätere Option.
  - Große Sweeps (z. B. 50 Seeds × viele Zellen) stoßen eventuell an Subscription-Limits. Der Durchsatz ist deshalb früh in einem Pilot zu messen.

## D-007: Automatisierung mit zwei Schleifen (Messen und Optimieren)
- **Datum:** 2026-10-20 · **Status:** vorgeschlagen
- **Wahl:**
  - Die innere Schleife (Szenario → Org-Config → Runner → Event-Log → Auswerter) läuft vollautomatisch.
  - Die äußere Schleife (Editor → Probes → statistisches Gate → Bibliothek → Transfer-Check auf geheimen Szenarien) läuft automatisch, mit technisch erzwungenen Grenzen: Der Optimierer darf nur die Org-Config ändern.
  - Der Ausbau erfolgt in vier Stufen, angefangen mit einem Pilot.
- **Begründung:** Das ist Neos Ziel "automatisiert testen und bewusst optimieren im Loop". Gegenüber Harness² gibt es echte Metriken, Seeds für Statistik und einen Schutz gegen Overfitting.
- **Details:** `notizen/05-automatisierung.md`
- **Update 2026-10-21:** angenommen. Neo: "wir bauen es vollversioniert, dann können wir es auch 2 Tage laufen lassen". Umgesetzt in `orglab/`.

## D-008: Komplettes System statt Stufenausbau, mit eingebautem Mess-Gate
- **Datum:** 2026-10-21 · **Status:** angenommen
- **Wahl:**
  - Alle Stufen werden gebaut: Testbed, Sweep, Optimierer, Dauerbetrieb.
  - Der Optimierer startet technisch nur, wenn `orglab.validate` für das Szenario bestanden ist. Geskriptete Policies mit bekanntem Unterschied müssen klar getrennt werden.
  - Backend-Ausfälle (Login, Rate-Limit) brechen einen Run ab, ohne ein Ergebnis zu schreiben. Der Sweep pausiert dann mit Backoff und setzt danach fort.
- **Begründung:**
  - Ein langer unbeaufsichtigter Lauf darf weder auf Rauschen optimieren noch technische Ausfälle als "Organisation tut nichts" verbuchen.
  - Konkreter Anlass: Der erste Smoke-Run lieferte bei fehlendem Login scheinbar gültige 0-%-Ergebnisse.

## D-009: Python, agentenseitige Texte englisch, Backend austauschbar
- **Datum:** 2026-10-21 · **Status:** angenommen
- **Wahl:**
  - Das Testbed ist in Python (`orglab`).
  - Prompts, Werkzeuge und Szenariotexte für die Agenten sind englisch. Doku und Kommentare bleiben deutsch.
  - Das Modell-Backend steckt hinter einer Schnittstelle: Agent SDK (jetzt), Messages API (später), geskriptet (Tests).
- **Begründung:**
  - Ein möglicher öffentlicher Benchmark braucht Englisch.
  - Die Agent-SDK-Doku erlaubt keinen claude.ai-Login für Produkte Dritter. Wer den Benchmark extern laufen lässt, braucht also einen API-Key. Deshalb muss das Backend austauschbar sein.
  - Die Sprache ist eine versteckte Variable und wird hiermit festgehalten.

## D-010: Kalibrierung gegen die Decke vor jedem Regime-Vergleich
- **Datum:** 2026-10-21 · **Status:** angenommen (Nachtlauf, aus E-001 abgeleitet)
- **Kontext:** E-001 hat alle Regime bei 100 % gezeigt. Die geskriptete Validierung prüft nur, ob die Messung *trennen kann*, nicht, ob das echte Modell im informativen Bereich liegt.
- **Wahl:** Jedes neue Szenario bekommt vor einem Vergleich einen kleinen Kalibrierungslauf mit dem echten Modell auf dem neutralsten Regime (B_minimal). Ziel: Der Mittelwert der Primärmetrik liegt zwischen 0,3 und 0,9. Liegt er darüber, wird verschärft (mehr Pakete, Regressionen, Budget), liegt er darunter, entschärft.
- **Begründung:** Ohne Kalibrierung verbrennt man Runs in einem Bereich, in dem kein Unterschied messbar ist (Decken- oder Bodeneffekt).

## D-011: Adaptives Optimierer-Gate (sequenzielles Nachmessen)
- **Datum:** 2026-10-21 · **Status:** angenommen
- **Kontext:**
  - E-005 hat das LLM-Rauschen gemessen: sd der Paar-Differenzen 0,111.
  - Das Gate mit 10 Paaren erkennt erst Effekte ≳ 0,087. Die realistische Verbesserung über einer Baseline von ~0,9 liegt aber bei ≤ 0,1.
  - E-010 bis E-012 waren damit praktisch blind.
- **Wahl:**
  - Kandidaten starten mit 5 Seeds je Domäne (10 Paare).
  - Ist Δ > 0 und p < 0,5, wird in 5er-Schritten für Kandidat UND Baseline nachgemessen, bis das Gate besteht oder 20 Seeds je Domäne (40 Paare, MDE ≈ 0,044) erreicht sind.
  - Klar schlechtere Kandidaten kosten weiter nur 10 Paare.
- **Preis:** Optional Stopping erhöht die Falsch-Positiv-Rate. Das ist für die Entdeckungsphase akzeptiert. Jede Übernahme muss ohnehin konfirmatorisch auf frischen Seeds repliziert werden (Zwei-Stufen-Regel).
- **Alternative verworfen:** immer 40 Paare. Das wäre ~4× teurer pro Iteration und mit dem Abo nicht machbar.

## D-012: Gegenspieler außerhalb des LLM implementieren
- **Datum:** 2026-10-21 · **Status:** angenommen (aus E-006)
- **Kontext:** Claude-Maulwürfe mit geheimem Sabotageauftrag haben selten oder nur kurz sabotiert. 100 % ihrer Falschmeldungen haben sie selbst repariert, meist mit Geständnis. Misstrauen entsteht so nicht.
- **Wahl:** Für Vertrauens-, Bürokratie- und Reputationsexperimente (Teil 2 §4/§6/§7) werden Gegenspieler implementiert als:
  - (a) **geskriptete Saboteur-Agenten im LLM-Team.** Das Backend muss dafür gemischte Teams erlauben, also pro Agent LLM oder Skript.
  - (b) **Umweltfehler** (Phantome, Regressionen, gefälschte Statussignale)
  - (c) **Fremdmodelle**, sobald API-Keys da sind
- **Begründung:** Die Manipulation muss unabhängig vom Charakter des getesteten Modells gelingen. Ob LLM-Saboteure sabotieren, ist selbst eine interessante Frage (H-021), aber eine andere als die, ob die Organisation mit Sabotage umgehen kann.

## D-013: Limit-Wächter statt blindem Backoff (2026-10-22)
- **Kontext:** Das Abo hat ein 5-Stunden- und ein Wochenlimit. Bisher liefen Runs ins Limit, scheiterten und verbrauchten Backoff-Versuche (E-014: 3 Runs mussten nachgeholt werden). Das Wochenlimit (57 % am 22.10. um 00:15, Reset in 3 Tagen) teilt sich das Testbed mit Neos eigener Arbeit.
- **Optionen:** (a) weiter exponentieller Backoff, (b) feste Nachtfenster, (c) die Limit-Meldungen der SDK (`RateLimitEvent`: Status, Auslastung, Reset-Zeit) auswerten.
- **Wahl:** (c), `orglab/limits.py`. Vor jedem LLM-Run wird geprüft. Bei vollem 5-Stunden-Fenster wird bis zum Reset gewartet, ohne einen Versuch zu verbrauchen. Ab 75 % Wochenauslastung startet nichts Neues (`daten/limit_policy.json`, zur Laufzeit änderbar). `daten/PAUSE` dient als Not-Aus von Hand.
- **Begründung:** Die Runs werden nicht mehr durch Limits verfälscht oder verschwendet, und Neo behält ein Viertel des Wochenkontingents. Bestätigungsläufe haben Vorrang vor dem Optimierer, weil der in 2 Iterationen nichts gefunden hat und pro Iteration viel Kontingent kostet.

## D-014: Design von E-017 (faktorielles Prüfer-Panel)
- **Datum:** 2026-10-22 · **Status:** angenommen (Neo hat das Experiment beauftragt, Design von Claude)
- **Kontext:** E-016 hatte einen Deckeneffekt. Die Literatur (`notizen/18`) zeigt, dass niemand Information, Stil und Erfahrung im selben Design vergleicht.
- **Wahl:**
  - **Information als Kanal-Diversität bei gleicher Informationsmenge:** Jeder Prüfer sieht genau einen von drei Kanälen, und jeder Kanal ist allein entscheidbar. Die Alternative "disjunkte Teile, die nicht allein entscheidbar sind" wurde verworfen, weil sie Dekorrelation mit Blindheit vermischt.
  - **Ein Primärmodell (Sonnet 5.5) für die Faktoren** und ein kleiner Zusatzarm mit 3 Familien, statt alle Faktoren über mehrere Familien. Begründung: Kosten und die Frage "gleiches Modell".
  - **Primärmetrik φ̄** (mittlere paarweise Fehlerkorrelation) statt β, weil β stark von der Einzelfehlerrate abhängt.
  - **Erfahrung als Rohepisoden im Prompt,** nicht als destillierte Lehren (Cluster E: Lehren reproduzieren Fehler).
  - **Kalibrierung (D-010) als Stufe 0** mit festen Annahmekriterien, darunter Kanalbalance.
- **Begründung:** maximale Trennschärfe pro Dollar (~50 $ gesamt) und keine Konfundierung der Hauptfrage durch Informationsmenge oder Kanalschwierigkeit.

## D-015: E-017 wird als Stapelprüfung neu aufgelegt (E-019)
- **Datum:** 2026-10-22 · **Status:** angenommen (Neo hat Option A gewählt, ggf. mit D)
- **Kontext:** Die E-017-Kalibrierung ist gescheitert. Sonnet 5.5 erkennt Fehlerspuren in Einzelbelegen fast immer (3–9 % Fehler), auch bei langen Logs.
- **Optionen:**
  - (A) Stapelprüfung, Aufmerksamkeitsknappheit
  - (B) schwächeres Modell
  - (C) echte Mehrdeutigkeit
  - (D) ohne Reasoning
- **Wahl:** A. D ist als letzte Stufe einer vorab festgelegten Kalibrierungsleiter vorgesehen (B=8/low → B=12/low → B=12/aus).
- **Begründung:**
  - Aufmerksamkeitsknappheit ist ein Fehlermechanismus, den starke Modelle real haben. Das passt zu Wave/Ace und zu H-016.
  - Die Ground Truth bleibt hart.
  - Das Modell bleibt Claude, also relevant für eigene Orgs.
  - Neue Kalibrierungskriterien verlangen, dass sich die Fehler über Fehlerarten verteilen, die Lehre aus E-017.
- **Ersetzt:** den Hauptlauf von E-017. Dessen Präregistrierung bleibt als gescheiterte Stufe 0 stehen.

## D-016: Belegmaterial v3, Fehlerarten nach dem Muster "Status grün, quantitatives Detail widerspricht"
- **Datum:** 2026-10-22 · **Status:** angenommen (von Neo beauftragt)
- **Kontext:** In E-017 und E-019 Stufe 0 übersah Sonnet 5.5 fast nur eine Fehlerart (`db_down`: Healthcheck ok, Pool 0/20). Alle anderen Spuren erkannte es zu ≥ 94 %. Damit war Kriterium 4 (Fehler verteilt) unerreichbar.
- **Wahl:** Der Generator bekommt pro Domäne zwei zusätzliche Fehlerarten. Bei jeder ist der Gesamtstatus grün, und in **jedem** Kanal widerspricht ein quantitatives Detail:
  - **coding:** `zero_traffic` (neues Release bekommt keinen Traffic), `cache_down` (Cache-Shards 0/4)
  - **business:** `empty_attachment` (PDF fehlt, Mail nur wenige kB), `amount_mismatch` (falscher Betrag versendet)
  - **research:** `duplicates_kept` (0 Duplikate entfernt), `column_loss` (Spalten verloren)
  - Die bisherigen Fehlerarten bleiben. Je Domäne gibt es damit 4 Fehlerarten, gleich wahrscheinlich.
- **Folgen für E-019:**
  - Neue Kalibrierungsseeds 1200–1211. Die Leiter beginnt wieder bei L1.
  - Kriterium 4 wird auf 12 Fehlerarten angepasst: mindestens die Hälfte (≥ 6/12) mit Übersehensrate ≥ 0,05, und kein Beleg trägt > 5 % der Fehler.
  - Alle übrigen Kriterien, Faktoren, Vorhersagen und Auswertung bleiben unverändert.
- **Begründung:** Wir messen die Fehlerkorrelation dort, wo starke Modelle tatsächlich irren. Mehr Rauschen oder Stapelgröße allein hat das nicht erreicht (E-017, E-019 L1–L3).

## D-017: Lehren aus Fehlern werden Regeln (CLAUDE.md Regeln 10–18)
- **Datum:** 2026-10-23, ~01:40 · **Status:** angenommen (Neo: "Unbedingt")
- **Kontext:** Am 22. und 23.10. gab es mehrere Fehler, die durch Regeln, Modellwidersprüche oder externe Kritik gefangen wurden, kaum durch Einsicht allein (`notizen/25`):
  - vertauschte Reasoning-Beschriftung (E-021)
  - etwa 10 Generatorfehler
  - abhängige Urteile als unabhängig gerechnet
  - Anstupser im Prompt und Sollwert-Lecks (E-020)
  - Aussagen stärker als ihr Status
- **Wahl:** Jede wiederkehrende Fehlerart wird eine Regel mit Herkunftsangabe (CLAUDE.md, Regeln 10–18), und die Präregistrierungsvorlage bekommt die passenden Pflichtfelder: Manipulationscheck, Weg/Modell/Einstellung, Leckprüfung, Fremdkontrolle, Analyse-Einheit, Prävalenz, externe Kritik.
- **Begründung:** Einzelne Korrekturen schützen nur vor dem gleichen Fehler am gleichen Ort. Regeln schützen jede künftige Session, auch eine, die den Fehler nicht miterlebt hat.

## D-018: Fünf Weichen nach der Nacht vom 23.10.
- **Datum:** 2026-10-23, ~07:10 · **Status:** angenommen (Neo: "Ich nehme alle fünf Empfehlungen so")
- **Kontext:** Offene Entscheidungen aus `notizen/morgen-2026-10-23.md`, Empfehlungen von Claude in der neuen Session.
- **Wahl:**
  1. **E-020: Generator v4** mit leckfreien Primär-Fehlerarten, kein bloßes Einschränken der Primärmetrik. Zusätzlich wird der REASONING-Faktor neu definiert, weil es "aus" über OpenRouter nicht gibt (E-021).
  2. **Ground-Truth-Fremdkontrolle durch ein Nicht-Claude-Modell über OpenRouter** (`openai/gpt-6.1-sol`), je Beleg einzeln, geschichtet, ohne Befundtext. Neo klärt die Abweichungen. Grok bleibt für Design-Kritik reserviert (Limits).
  3. **Wave-Fälle (`notizen/28`): Neo kodiert zuerst**, danach liest er Claudes versiegelte Kodierung. Ace kommt als dritter Kodierer dazu, gilt aber nicht als unabhängig (vermutlich Claude-basiert, kannte die Hypothese).
  4. **Aces Stichprobe zunächst ohne FM-Labels** blind kodieren. Die Labels werden danach als Fremdvergleich angefragt (neue Gravity-Freigabe durch Neo).
  5. **Als Nächstes:** Neo kodiert, Claude baut Generator v4 und präregistriert eine Reasoning-Dosis-Probe (E-022, ~7 $ über OpenRouter, belastet das Abo nicht). Abo-Läufe ruhen bis zum Wochen-Reset (71 %).
- **Begründung:** Ein Einschränken der Metrik ließe SPEC genau dort nichts messen, wo es messen soll (Grok-Gutachten 2). Ein Modell als Fremdkontrolle ist billig, wiederholbar und schont Neos Zeit für die wirklich strittigen Fälle. Labels erst nach der blinden Kodierung zu holen, macht sie zur Kontrolle statt zum Anker.

## D-019: Wave-Fälle durch drei Kodierer, Neo schlichtet (ersetzt D-018 Punkt 3)
- **Datum:** 2026-10-23, ~08:00 · **Status:** angenommen (Neos Vorschlag: "du, Ace und ein anderes Modell macht die Bewertung und ich lese dann alle 3, es ist schwächer, aber ich schaffs nicht allein")
- **Kontext:** 14 Fälle × 8 Felder sind für Neo nebenbei zu viel (112 Einzelurteile).
- **Wahl:**
  - Drei unabhängige Kodierungen: Claude (versiegelt, `01-…`), GPT (`openai/gpt-6.1-sol`, blind, ohne den Abschnitt mit der Hypothese, `03-…`) und Ace (neuer Thread, nur Text, `04-…`).
  - Neo bekommt eine Vergleichsansicht und entscheidet nur dort, wo sich die drei nicht einig sind (Schlichtung).
- **Schwächen (offen benannt):**
  - Claude und Ace sind vermutlich dieselbe Modellfamilie und kannten beide die Hypothese. Ihre Übereinstimmung zählt weniger als die mit GPT.
  - Neo ist kein unabhängiger Kodierer mehr, sondern Schlichter, der die Vorschläge sieht. Das ist bewusst schwächer als die ursprüngliche Planung.
  - Übereinstimmung wird je Feld paarweise berichtet (Prozent, Cohens κ). Die Paare mit GPT sind die aussagekräftigsten.

## D-020: Doppelte Buchführung als Regel 19, Analyse-Freiheitsgrade und Power als Pflichtfelder
- **Datum:** 2026-10-23, ~11:10 · **Status:** angenommen (Neo: "Ja")
- **Kontext:**
  - Regelkritik-Panel (`notizen/31`): Das meistgenannte Thema war die ungeprüfte Auswerte-Pipeline (10 von 16 Fremdmodellen, 0 von 3 Claude). Fehlende Power-Planung nannten 4 Modelle.
  - Erste doppelte Buchführung bei E-022: Die Zahlen sind reproduziert, aber eine Lücke im eingefrorenen Skript wurde gefunden (16-Stapel-Regel), und die Fremdmodelle meldeten offene Analyse-Entscheidungen.
- **Wahl:**
  1. **CLAUDE.md Regel 19:** Jeder Bestätigungslauf wird von mindestens einem Modell anderer Familie nur aus der Präregistrierung neu ausgewertet (`orglab/nachrechnung.py`). Claude liest den Fremdcode vor dem Ausführen, ausgeführt wird er isoliert. Bei Abweichung gilt der Befund erst nach Klärung. Die Checkliste pro Befund ist ergänzt.
  2. **Präregistrierungs-Vorlage:** neuer Pflichtabschnitt "Teststärke" (kleinster relevanter Effekt, Streuung, Power oder Intervallbreite, Aussagekraft eines Nullergebnisses). Neues Pflichtfeld "Analyse-Freiheitsgrade" (Bootstrap-Ziehungen, Startwert und Quantilmethode, Umgang mit Wiederholungen und fehlenden Urteilen, Gewichtung, Mindestumfang für konfirmatorische Aussagen, Ausfälle je Arm). Dazu ein Feld für die doppelte Buchführung.
- **Nicht** übernommen (offen für spätere Entscheidung, `notizen/31`):
  - Anbieter-Logging und Anker-Stapel gegen Drift
  - HARKing-Schutz (verworfene Operationalisierungen)
  - Stichproben, die Neo selbst zieht
  - FDR über Experimente hinweg
- **Begründung:** Die doppelte Buchführung setzt laut Panel genau dort an, wo Claude am blindesten ist. Sie kostet wenige Cent und hat beim ersten Einsatz einen echten Fehler gefunden. Freiheitsgrade, die nicht in der Präregistrierung stehen, entscheidet sonst der Code, und den schreibt Claude.
- **Folge für E-022:** Das eingefrorene Skript bleibt, wie es ist. Die Lücke ist im Ergebnis dokumentiert und hat das Ergebnis nicht berührt.

## D-021: Verblindete Auswertung als Regel 20 (einfache Variante), Sandbox-Sperre als zweiter Schritt
- **Datum:** 2026-10-23, ~11:50 · **Status:** angenommen (Neo: "Ja machs mal so")
- **Kontext:**
  - Bei der Wave-Kodierung wich Claude einseitig in Richtung der eigenen Hypothesen ab (K1/K5, `notizen/30`).
  - Neos Meta-Harness-Gedanke (`notizen/32`): Regeln sollen Mechanik werden, nicht Disziplin.
- **Optionen und Verlauf:**
  - (a) Schlüsseldatei außerhalb des Repos mit Hash-Commitment, Gate erst nach Commit der verblindeten Auswertung
  - (b) Neo würfelt die Zahl. Neo fragte: "wofür braucht das einen Menschen, wenn nur gewürfelt wird?" Damit war ein Denkfehler in Claudes Vorschlag aufgedeckt: Die Zahl wäre wieder durch Claudes Hände gegangen.
  - (c) harte Rechtetrennung per Sandbox oder getrenntem Prozess. Neo: "softwaretechnisch lösbar, sowohl bei einem als auch bei mehreren Agenten".
- **Wahl:**
  - Jetzt (a) als Regel 20 (`orglab/verblindung.py`, Tests `tests/test_verblindung.py`, Vorlage ergänzt).
  - Danach (c) prüfen: Kann die Sandbox von Claude Code den Schlüsselordner wirklich sperren, auch für die Shell? Eine Einstellungsänderung braucht Neos Freigabe.
- **Schutzziel von (a):** unbewusstes Biegen und versehentliches Sehen. Absichtliches Nachschauen ist nicht abgedeckt, und das ist auch nicht das Bedrohungsmodell (Neo: Der Forscher will nichts manipulieren).
- **Begründung:**
  - Eine Konfiguration prüft man einmal, Disziplin kostet bei jedem Schritt und lässt mit der Sessionlänge nach (Beispiel: die vergessene 16-Stapel-Regel).
  - Realistischer als ein Sandbox-Ausbruch sind Abkürzungen innerhalb der eigenen Rechte (Specification Gaming). Dagegen hilft Rechtetrennung.
- **Verwandtes (Gespräch, `notizen/32`):** Kryptographie als Werkzeug für die *Integrität des Ablaufs*, nicht für die Richtigkeit des Urteils:
  - Commitment und öffentlicher Zeitstempel für Präregistrierungen
  - Secret Sharing für einen Treuhänder aus mehreren Parteien
  - Hash-Kette fürs Laborbuch (Brücke zu AAP)

## D-022: Fokus nach dem 23.10.: E-020 als Hauptlinie, REASONING-Faktor gestrichen, Regel-Stopp
- **Datum:** 2026-10-23, ~14:00 · **Status:** angenommen (Neo: "Klingt gut für mich")
- **Kontext:**
  - Am 23.10. entstanden viele Meta-Bausteine (Regeln 19 und 20, Fehlerprotokoll, Panel, `notizen/32`), aber wenig Realitätsbezug.
  - Neo: "was machen wir jetzt um uns nicht zu verkaufen".
- **Wahl:**
  1. **Hauptlinie E-020** auf Material v4.1. Das ist das Experiment, das der Wave-Frage am nächsten ist (SPEC, ZUGANG, AUSKUNFT). Hinweis aus den Wave-Fällen: Bei 4 von 5 Übersehen-Fällen hätte der Prüfer den Beleg selbst holen müssen.
  2. **Vorschlag A aus Entwurf v3 angenommen:** Der REASONING-Faktor fällt weg, weil "aus" über OpenRouter nicht existiert und E-022 die Frage abdeckt. Statt 16 gibt es **8 Zellen**. Sonnet läuft ohne `reasoning`-Parameter (adaptiv), die Tokens werden berichtet. H-036 und V6 entfallen für E-020.
  3. Kleine Pflichten: Ace-Update mit korrekten Status, blinde Kodierung des Fehlerprotokolls.
  4. **Regel-Stopp:** keine neuen Regeln und keine neuen Meta-Werkzeuge, bis E-020 gelaufen ist. Lichttest und Zerlegungs-U-Kurve bleiben auf dem Parkplatz.
- **Nach außen:** Die ehrliche Geschichte lautet "zwei belegte Befunde, einige gestützte, und eine ungewöhnlich gut prüfbare Arbeitsweise". Nichts darüber hinaus.

## D-023: Leitfrage des Projekts – wann ist ein "verifiziert" gerechtfertigt?
- **Datum:** 2026-10-23, 23:07 · **Status:** angenommen (Neo: "verdammt richtig")
- **Kontext:**
  - Nach E-020, E-023, E-024, der Recherche und dem dritten Prüfer fühlte sich das Projekt für Neo "extrem groß" an: "wir kommen immer von eins ins nächste".
  - Beim Herauszoomen zeigte sich: Alle Fäden sind dieselbe Frage auf verschiedenen Ebenen.
    - Agenten-Teams: Phantom-fertig, Maulwürfe
    - einzelne Prüfer: Sonnet/Haiku, Belege
    - Wave: "verifiziert", obwohl nicht
    - die eigene Forschung: Claudes Überbehauptungen bei vollem Kontext
  - Das Muster ist überall gleich: Ein Urteil kippt, wo die widersprechende Information nicht im Blick ist (fehlt, wird nicht geholt, geht im Kontext unter oder wird übertönt).
  - Auch die Gegenmittel wiederholen sich: andere Information statt mehr Prüfer, den Maßstab sichtbar machen, frischer Kontext, fremde Augen.
- **Wahl:** Leitfrage für alle weiteren Experimente:
  > **Was macht ein "verifiziert" gerechtfertigt, und wie muss man Information organisieren, damit es das ist?**
  - **Nach vorn:**
    - Kontext-Drift (Länge gegen Richtung, Parkplatz)
    - glückliches Vertrauen (H-041)
    - Maßstab mitgeben bzw. Nachschlagen erzwingen (H-039)
    - Prüfpfad-Diversität bzw. andere Information gegen anderes Modell (H-018, H-029)
  - **Bewusst liegen lassen:**
    - Morpheus-Daten nachbewerten
    - Modellfamilien als Selbstzweck durchtesten
    - IRT-Ambitionen ohne passende Datenmenge
  - Jede neue Idee wird zuerst gefragt: Beantwortet sie die Leitfrage?
- **Begründung:**
  - Das Projekt wird sonst breiter statt tiefer.
  - Neos Intuitionen der letzten Tage (Aufmerksamkeitsteilung, Fehler dekorrelieren, Informationskapselung, Monolith, Kontext-Drift) sind Varianten von "wer sieht wann welche Information".
  - Die Leitfrage passt direkt zu Waves Schmerzpunkt.
- **Ehrlicher Stand dazu:** Hart belegt sind E-014, E-018 und der schmale Haiku-Befund aus E-024. Alles andere ist Hypothese oder Hinweis.

## D-024: Programmvision über der Leitfrage – vertrauenswürdige automatisierte Forschung in simulierbaren Bereichen
- **Datum:** 2026-10-23, 23:24 · **Status:** angenommen als Vision (Neo: "ja halte es fest"), keine neue Baustelle
- **Kontext:**
  - Neo erkennt beim Herauszoomen: Die Multi-Agent-Frage war das Vehikel. Darunter liegt die Frage, wie man Forschung bei beliebigen simulierbaren Dingen sicher automatisiert.
  - Selbstbeobachtung: Neo schließt als Laie den Kreislauf und kann sein eigenes Urteil nicht garantieren. Die Leitfrage D-023 ist auch sein Vertrauensproblem.
- **Wahl:** Vision in `notizen/35-programmvision.md` festgehalten.
  - Forschung ist selbst ein MAS. D-023 ist dieselbe Frage eine Ebene höher.
  - Simulierbarkeit erlaubt gemessene Fangquoten der Prüfer.
  - Objekt-Befunde sind Bauteiltests für einen Research-Harness.
  - Observability ist die Messgrundlage für die Leitfrage.
- **Grenzen:**
  - Die Objektebene bleibt Fundament (D-022).
  - Vor jeder Neuheitsbehauptung kommt eine Recherche zu "automatisierte Forschung".
  - Ein Engineering-Projekt (Research-Harness als Meta-Harness oder MAS) wird es nur auf ausdrücklichen Beschluss.
- **Nächstes Bindeglied (Vorschlag):** Lichttest auf die eigene Forschungspipeline (`notizen/35` §7).
