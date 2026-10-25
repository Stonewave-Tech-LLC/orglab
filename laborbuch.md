# Laborbuch

Nur anhängen. Neueste Einträge stehen unten.

---

## 2026-10-20: Projektstart, Quellencheck, Ace-Befragung

**Ausgangspunkt:** Handoff aus einem Chat-Brainstorm (`Downloads/handoff-social-skills-benchmark.md`). Die Idee: ein Benchmark "Teaching Agents Social Skills", bei dem das Modell fix bleibt und der Harness die unabhängige Variable ist. Harness² kommt als möglicher Optimierer infrage.

**Was getan wurde:**
1. **Quellen aus dem Handoff geprüft** → `notizen/01-quellencheck.md` und `quellen.md`.
   - Harness² im Volltext gelesen. Zahlen und Repo sind bestätigt.
   - Zwei Korrekturen zum Handoff: Harness² ist Single-Agent, und die Harnessing-Level-Rekursion erweitert nur eine Bibliothek, sie schreibt den Optimierer nicht selbst um.
2. **Neos Problem zugespitzt** → `notizen/02-problemstellung.md`.
   - Neos Beobachtung: Handgeschriebene Verträge kommen nicht hinterher, Fixes verschieben die Fehlerfront, "man gewinnt kein Land".
   - Die Forschungsfrage verschiebt sich von "welche Social Skills fehlen" zu "welche Regulationsmechanismen machen eine Agenten-Organisation selbstkorrigierend und modellrobust".
3. **Ace (FACE) befragt** → `notizen/03-ace-befund.md`.
   - 12 Vorfälle, 6 Hypothesen und eine Datenlandkarte, alles aus Aces Memory, nicht live verifiziert.
   - Daraus fünf neue Szenario-Kandidaten aus echten Vorfällen: Phantom-Fertig, Runaway-Loop, Regelkollision, Verlorener Rückkanal, Fehlende geteilte Semantik.
4. **Dokumentationssystem eingerichtet**, auf Neos Wunsch: `CLAUDE.md`, `laborbuch.md`, `hypothesen.md`, `entscheidungen.md`, `quellen.md` und eine Vorlage für Experimente. Dazu `git init`.

**Ergebnis / Stand:** Es gibt noch keine Experimente. Die Hypothesen H-001 bis H-012 sind erfasst, alle offen.

**Offen:**
- Freigabe von Neo für einen Rohdaten-Export aus Ace (nur Metadaten).
- Wahl der Modelle und APIs für das Testbed.
- Gezielte Literatursuche zur Neuheit von "Optimierer entdeckt Social-Skill-Module".

**Nachtrag, gleicher Tag:**
- Neo hat den Ace-Datenzugriff freigegeben und Agent SDK + Sonnet 5.5 festgelegt (D-006). Außerdem soll eine Ebene über den Coding-Vorfällen gedacht werden (D-005).
- Der Export-Auftrag an Ace CORE wurde von der Auto-Mode-Prüfung von Claude Code blockiert ("PII Data Handling"). Der Auftragstext liegt in `notizen/04-ace-export-auftrag.md`, Neo kann ihn selbst schicken oder die Berechtigung erteilen.
- Neo hat den Auftrag selbst an Ace gegeben. Die Findings kommen über Neo.
- Neo fragt, ob sich das automatisiert testen lässt. Antwort: Systementwurf mit zwei Schleifen in `notizen/05-automatisierung.md` (D-007, vorgeschlagen).

---

## 2026-10-21: Testbed `orglab` gebaut, Ace-Rohdaten ausgewertet

**Entscheidung:** Neo will die Vollversion, die auch zwei Tage am Stück laufen kann (D-007 angenommen, D-008, D-009).

**Gebaut** (`orglab/`):
- Event-Log, Org-Config mit Validierung und Hash, domänenneutrale Welt.
- Werkzeuge der Agenten.
- Szenario `phantom_done` in drei Domänen.
- Backends: Agent SDK und geskriptet.
- Runner, Sweep (parallel, fortsetzbar, Backoff bei Backend-Ausfall), Auswertung (Bootstrap, Permutationstests).
- Mess-Validierung.
- Optimierer: Propose, Probe, gepaartes Gate, Compose, Reflect, Bibliothek, Holdout-Transfer.
- Vier Regime-Configs A–D.
- 11 Tests, alle grün.

**Mess-Validierung `phantom_done`:** bestanden (`daten/validierung/phantom_done.json`).
- Diligent: `true_completion` 1,00. Naive: 0,41, mit `false_done_rate` 0,59. Idle: 0.
- d = 4,5, p < 0,01. Das Szenario trennt also Wirkungsprüfung von Flag-Vertrauen.

**Smoke-Test mit Sonnet 5.5:** fehlgeschlagen. Die im SDK enthaltene Claude-CLI ist nicht eingeloggt ("Not logged in"). Der Run lieferte trotzdem scheinbar gültige Metriken (0 %).
- Daraus entstand D-008: Backend-Ausfälle brechen Runs jetzt ab, ohne Ergebnis.
- Die Smoke-Daten liegen unter `daten/E-000-smoke/run1` und sind ungültig.

**Ace-Rohdaten** (Export über Nexus, `daten/ace-export-2026-10-20/`, nur lokal):
- Kernzahlen selbst nachgezählt, sie stimmen. Befund in `notizen/06-ace-rohdaten-befund.md`.
- Liegengebliebenes ist massiv: 100 von 100 Zusagen offen, 70 % des Backlogs nie geschlossen. Freigaben, nach denen aktiv gefragt wird, erledigt der Mensch aber im Median in 0,9 min. Daraus die neue Hypothese H-013 (fehlender Pull-Mechanismus).
- "Wirkung vs. Flag" ist das häufigste Vorfallmuster (6 von 13), FM-3.2 steht in 62 % der MAST-Annotationen.
- Modellvergleich aus den Wave-Daten ist unmöglich (H-002 nur experimentell testbar).
- Anmerkung: Laut seiner Nachricht hat Ace für den Upload einmalig `.env.local` geladen, mit Neos Freigabe. Das Repo ist laut Ace unverändert.

**Präregistriert:** E-001 Pilot (`experimente/E-001-pilot/prereg.md`). Er wartet auf Neos Login.

**Offen:** Neo loggt sich in der SDK-CLI ein → Smoke-Test → E-001 → danach erster Optimierungslauf.

---

## 2026-10-21 (Nacht): autonomer Lauf

Neo hat sich eingeloggt und ist schlafen gegangen. Sein Auftrag: über Nacht laufen lassen, analysieren, Schlüsse ziehen, Thesen und Methoden erweitern.

**Infrastruktur:**
- Die Experimentprozesse verhindern jetzt selbst den Ruhezustand (`orglab/keepawake.py`, Windows-API, keine Einstellungsänderung).
- Die Code-Version wird pro Prozess fixiert, damit spätere Commits die Metadaten laufender Experimente nicht verfälschen.

**Smoke-Test** (`daten/E-000-smoke/run2`): funktioniert. Sonnet 5.5 prüft die Wirkung spontan (16 Inspektionen) und erkennt das Phantom. Nach 2 Ticks ist alles erledigt, für ~0,44 USD API-Äquivalent.

**E-001 Pilot** (00:13–00:45, 24 Runs, 0 Ausfälle): **Deckeneffekt.** Alle Regime erreichen 100 %. Die Unterschiede liegen nur im Prozess:
- C koordiniert fast ohne Nachrichten (0,7 gegenüber 8–13).
- A ist am langsamsten: Der Hub ist der Engpass, und der Koordinator handelt auf veralteter Information.
- In D entsteht spontan eine Reviewer-Rolle und Lektionen im Notizbuch.

Details: `experimente/E-001-pilot/ergebnis.md`.

**Methodenerweiterung:**
- **Regression** als neue Mechanik: Ein späteres Paket macht still ein früheres kaputt. Damit ist Neos "kein Land gewinnen" operationalisiert.
- Zwei Stufen dazu: `phantom_hard` (14 Pakete, 3 Phantome, 3 Regressionen) und `phantom_stress` (16 / 4 / 5).
- Neue Policy `vigilant` (prüft Erledigtes erneut). Die Validierung ist jetzt eine szenariospezifische Leiter: vigilant 1,00 > diligent ~0,8 > naive ~0,4. Beide Stufen sind bestanden.
- `phantom_done` bleibt bit-identisch reproduzierbar (Validierung liefert identische Zahlen).
- **D-010:** Kalibrierung gegen die Decke mit dem echten Modell wird Pflicht vor jedem Regime-Vergleich.
- **H-014** (Organisationsunterschiede erst unter Last) neu.

**Gestartet:**
- **E-002** (00:45): Regime-Vergleich auf `phantom_hard`, 40 Runs, Concurrency 2, ~6 min pro Run.
- **E-010** (00:37): Optimierer ab B_minimal auf `phantom_hard`, Holdout research, Concurrency 4, bis ~08:30. Abbruchregel vorab festgelegt: Ist die Baseline ≥ 0,95, folgt ein Neustart auf `phantom_stress`.
- Speicher: 19 GB frei, das reicht für beide parallel.

**Kalibrierungskette (alle Regeln vorab festgelegt, D-010):**

| Lauf | Szenario / Budget | Baseline B_minimal | Entscheidung |
|---|---|---|---|
| E-010 | `phantom_hard`, 8 Calls/10 Ticks | 0,986 | Decke → Abbruch |
| E-011 | `phantom_stress`, 8/10 | 0,994 | Decke → Abbruch (aber Runs brauchen schon 8–10 Ticks) |
| E-012 | `phantom_stress`, **4/8** | **0,881** | informativ → läuft |

**Befund aus der Kalibrierung (H-014 gestützt, explorativ):** Mehr Komplexität allein (Pakete, Phantome, Regressionen) bringt Sonnet 5.5 nicht an seine Grenze. Erst **knappe Aufmerksamkeit** tut das: weniger Werkzeugaufrufe pro Tick, weniger Ticks.
- Unter Knappheit bleiben Regressionen unrepariert (7 von 10 Runs).
- Die Teams scheitern am Zeitlimit, nicht an mangelnder Sorgfalt.
- Übertragen auf Wave: Organisationsdesign wird dort relevant, wo Aufmerksamkeit knapp ist, nicht dort, wo Aufgaben schwer sind.

**Editor-Diagnosen** (Opus, unabhängig voneinander):
- E-010: *"Nobody owns the question of whether the whole set still works once all execution has stopped."*
- E-012: *"what inspection finds stays with the person who inspected"*

Beide passen zu H-013 (fehlender Pull-Mechanismus) und H-007 (fehlender gemeinsamer Zustand).

**E-012 Iteration 1, Kandidaten:** Beide schalten das Board ein und fügen Verifikationsnormen hinzu. Der invariante Kandidat führt eine explizite Aufmerksamkeitsökonomie ein ("never re-inspect an item that is already verified and unchanged").
- **Ergebnis:** Beide werden verworfen (Δ −0,006 und −0,037). Die Inspektionen steigen, die Leistung nicht. Daraus **H-016**: Sorgfaltsregeln kosten unter Knappheit Aufmerksamkeit.

**E-012 Iteration 2:** Der Editor lernt aus der Iteration davor (*"added more checking instead of assigning it"*) und schlägt Effizienz-Normen vor: Nur der Eigentümer prüft, keine Broadcasts.
- **Ergebnis:** **signifikant schlechter**, Δ −0,075, p = 0,015. Die Inspektionen halbieren sich (48 → 24), der Anteil reparierter Regressionen fällt von 0,55 auf 0,22.
- **Mechanismus:** Die ungeregelte, scheinbar redundante Kreuzprüfung fängt die Regressionen, die fremde Arbeit verursacht. Daraus **H-017**.

**Zwischenbild nach 2 Iterationen:** Beide Richtungen von Handregeln scheitern. *Mehr* Prüfregeln bringen nichts (sie kosten Aufmerksamkeit), *sparsamere* Prüfregeln schaden (sie entfernen funktionale Redundanz). Die ungeregelte Organisation von B_minimal liegt bisher über beiden. Das spiegelt Neos Wave-Erfahrung im Kleinen und stützt die Dochkina-Linie (H-003). Vorsicht: n ist klein, und es sind erst zwei Iterationen.

**Gestartet:**
- **E-003** (~01:50): Regime A–D unter knapper Aufmerksamkeit, 40 Runs.
- **E-004** (~02:05): **konfirmatorische Replikation von H-017** mit frischen Seeds und Research als dritter Domäne, 60 Runs, einseitiger Test vorab festgelegt.

Parallel laufen damit E-012 (Concurrency 4), E-003 (2) und E-004 (2). Speicher: 16 GB frei, bisher keine Backend-Ausfälle.

**E-012 Iteration 3** (02:14): Die Kandidaten setzen auf Reparatur-Zuständigkeit ("a known failure must never sit with no one working on it") und Notizbuch-Verifikationslog. Ergebnis: Δ +0,000 und −0,019, beide verworfen. Das ist die dritte Iteration ohne Verbesserung. Das Muster festigt sich: Die vom Editor wohlbegründeten Handregeln übertreffen die ungeregelte Organisation nicht.

**E-003** (Regime unter knapper Aufmerksamkeit, 38 von 40 Runs; 2 D-Runs fehlen wegen des Session-Limits):
- **A_contracts_tight ist am schlechtesten:** `true_completion` 0,79 gegenüber 0,88 bei B, C und D, d ≈ −1,1. Unkorrigiert p = 0,03–0,07, nach Bonferroni nicht signifikant.
  - A hat die wenigsten Inspektionen (28 gegenüber 40–53).
  - Emergente Rollen in A: 29 Ausführer, 5 Kommunikatoren, 1 Prüfer.
  - Lesart: Verträge lenken die Aufmerksamkeit auf Melden und Koordinieren, nicht aufs Prüfen.
- **B, C und D liegen gleichauf** (0,875–0,881).
- **C repariert die meisten Regressionen** (0,45 gegenüber 0,22 bei B, n.s.), das bringt aber keine höhere Fertigstellung.
- **Emergenz:** In C werden unter Knappheit 19 von 40 Agenten zu Prüfern. In E-001 (ohne Knappheit) waren es vor allem Generalisten.
  - **H-015 muss damit bedingt formuliert werden:** Geteilter Zustand ersetzt Rollen nur ohne Knappheit. Unter Knappheit ermöglicht er die Spezialisierung auf Prüfen.
- **Abgleich mit den Vorhersagen:**
  - Vorhersage 3 (A am schlechtesten): eingetreten, als Tendenz.
  - Vorhersage 2 (C prüft am meisten, ist aber nicht besser als B): eingetreten.
  - Vorhersage 4 (Spannweite ≥ 0,05): eingetreten.
  - Vorhersage 1 (D am besten): nicht eingetreten.

**02:23: Session-Limit der Subscription erreicht** ("resets 6:10am").
- Alle Läufe pausieren automatisch mit Backoff (D-008). Es werden keine falschen Ergebnisse gespeichert.
- Der Sweep versucht es bis zu 8-mal mit steigenden Pausen (bis 60 min) und sollte nach 06:10 weitermachen.
- **Vorsicht bei E-012:** Iterationen während des Limits haben keine gültigen Probe-Paare. Sie zählen fälschlich als "keine Verbesserung" und verbrauchen Patience. Die Iteration 4 (ab 02:14) muss deshalb morgen als ungültig geprüft und markiert werden.
- E-004 (Replikation H-017) ist erst zu ~16 von 60 Runs gelaufen.

**~05:29: E-012 ist abgestürzt** (Exit 1), nicht wegen des Limits, sondern wegen eines **Bugs**.
- In `orglab/llm.py` räumt `TemporaryDirectory` das Editor-Verzeichnis auf, während die CLI es unter Windows noch offen hält (`PermissionError WinError 32`).
- **Fix für morgen:** `TemporaryDirectory(ignore_cleanup_errors=True)`. Danach E-012 per gleichem Befehl fortsetzen, `state.json` bleibt erhalten.

**E-003**: Der Sweep-Prozess ist beendet (Exit 0). Ob die 2 fehlenden D-Runs noch nachgelaufen sind, habe ich nicht mehr geprüft.

**Durchsatz-Befund für die Planung:** In ~2 h 10 min Volllast liefen etwa 230 Agent-Runs, dann griff das Session-Limit. Für Zweitagesläufe braucht es deutlich niedrigere Concurrency oder einen API-Key (D-009).

---

## 2026-10-21 (Vormittag): Neustart nach dem Limit, Methodik Teil 3, E-004-Bestätigung, Ace

**Neo** (vor der Abfahrt): "kannst durchziehen". Dazu zwei neue Handoffs, Teil 2 (Agenten-Gesellschaften) und Teil 3 (Methodik). Später der Auftrag, Ace zu informieren und ihm regelmäßig Ergebnisse per Nexus zu schicken.

**Nach dem Limit-Reset (06:10):**
- E-004 lief von selbst weiter. 2 Runs von E-004 und 2 von E-003 waren nach allen Wiederholungsversuchen gescheitert und wurden nachgeholt. E-003 und E-004 sind jetzt vollständig.
- E-012 ist um 05:29 abgestürzt, ein Bug im Windows-Temp-Ordner. Behoben in `38c5858`.
- Zusätzlich gilt jetzt: Iterationen ohne gültige Messdaten werden als Backend-Ausfall wiederholt und zählen nicht mehr als "keine Verbesserung".

**Methodik Teil 3 umgesetzt** (`CLAUDE.md`, `d8737c8`):
- Zwei-Stufen-Regel (Entdeckung → Bestätigung auf frischen Seeds)
- A/A-Test und Positivkontrolle
- BH-FDR-q-Werte in `analyze.compare`
- Thesen einfrieren (Präzisierungen werden neue H-Nummern)
- Messlauf und Optimierungslauf getrennt
- Kritiker-Unabhängigkeit als offen markierte Schwäche
- Pflichtlektüre von Transkripten
- Regeln zur Eval-Awareness

Alles aus der Nacht gilt als **Entdeckungsphase**.

**E-005** (A/A + Positivkontrolle, 60 Runs) ist präregistriert und läuft.

**Teil 2 eingeordnet** (`notizen/07`): Empfohlen ist als nächste Achse die **Maulwurf-Dosis** (Bürokratie als Verifikationsinfrastruktur unter Misstrauen, mit Kreuzungs-Vorhersage).
- Szenario `mole_k` ist gebaut: geheimer Sabotageauftrag, Neu-Zuweisung über den Menschen. Validiert für k = 0/1/2: auditor 1,00 > vigilant 1,00/0,64/0,38 > naive.
- Nachträgliche Kriteriumsänderung, offen vermerkt: Die Schwelle "beste Policy ohne Falschmeldungen" ist jetzt ≤ 0,02 statt = 0. Maulwürfe erzeugen Falschmeldungen absichtlich, und der Auditor erreichte bei k = 2 nur 0,999.
- **METR-Bericht zum Hugging-Face-Incident** im Original geprüft. Agenten führten unter Identitätsunsicherheit selbst Ed25519-Signaturen ein. Das stützt Teil 2 §3/§6 und AAP.

**E-004 (konfirmatorisch): H-017 nicht bestätigt.**
- Δ `true_completion` −0,033 (CI −0,075 bis +0,004), einseitig p = 0,076 gegenüber Schwelle 0,05.
- Die Richtung bleibt, der Effekt hat sich gegenüber der Entdeckung (−0,075) halbiert.
- Die Manipulation wirkt (−39 % Prüfungen), das Ergebnis kaum.
- Lehre: Die Zwei-Stufen-Regel hat einen überschätzten Entdeckungsbefund abgefangen.
- Details: `experimente/E-004-owner-only-replikation/ergebnis.md`.

**Ace** (Thread [ID intern]):
- Briefing per Nexus geschickt (`berichte/2026-10-21-briefing-ace.md`).
- Aces Antwort (`notizen/08`): H-017 sei zu grob, entscheidend sei die **Diversität des Prüfpfads**, nicht der zweite Prüfer. Daraus H-018 und sein Szenario-Vorschlag "Prüfpfad-Diversität".
- Er hat einen Fehler in meinem Briefing gefunden: FACE- und CORE-Nummerierung waren vermischt (V10). Ab jetzt nur noch CORE-V-Nummern.
- Meta-Beobachtung: Die Ace-Instanz von heute kannte die V-Nummern seiner eigenen Export-Instanz nicht. Das ist Aces H6, live beobachtet.

**Korrektur (07:58):** Mehrere Uhrzeiten in den Einträgen von heute früh waren von mir geschätzt und zu spät angesetzt. Korrigiert nach Dateizeitstempeln:
- E-004 fertig um 07:21 (nicht 08:40)
- E-012 fortgesetzt um 07:23 (nicht ~08:45)
- Die an Ace geschickten Berichte tragen die falschen Zeitangaben "~08:00" und "~08:50", tatsächlich ~07:15 und ~07:25. Sie sind schon versendet und bleiben unverändert.
- **Lehre:** Uhrzeiten nur aus Zeitstempeln (`date`, Logs) übernehmen, nie schätzen.

**E-012 Iteration 4** (07:56): Auch ein zentralisierter Kandidat (Stern, Koordinator mit "einziger autoritativer Liste", feste Rollen) bringt Δ −0,006. Der spezifische Kandidat (Nachrichten-Disziplin, Endphase ab Tick 7) kommt auf Δ −0,056. Damit ist es die vierte Iteration ohne Verbesserung.

**08:43 – E-005 (A/A + Positivkontrolle): bestanden.**
- A/A: Δ +0,006, p = 0,90.
- Positivkontrolle ("Flags vertrauen"): 0,90 → 0,38, p < 0,001.
- **Entscheidender Nebenbefund:** Das LLM-Rauschen liegt bei sd(Δ) = 0,111 je Paar. Das Optimierer-Gate mit 10 Paaren erkennt damit erst Effekte ≳ 0,087. **E-010 bis E-012 waren also praktisch blind**, und meine Nacht-Lesart "keine Handregel schlägt die ungeregelte Organisation" ist zu stark. Korrekt: keine mit Effekt ≳ 0,09.
- Die Nicht-Bestätigung von H-017 (E-004, 30 Paare, MDE 0,05) ist teils auch ein Teststärke-Thema.
- Details: `experimente/E-005-aa-positivkontrolle/ergebnis.md`.

**08:46:**
- E-012 gestoppt (in Iteration 5).
- **D-011** adaptives Gate eingebaut und getestet (Nachmessen bis 40 Paare).
- **E-013** gestartet: Optimierer mit adaptivem Gate, unabhängige Bibliothek.
- **E-006** gestartet: Maulwurf-Dosis k = 0/1/2 × {B, Verifikations-Bürokratie}, 60 Runs, testet die neue H-019 (Bürokratie lohnt erst unter Misstrauen).
- Concurrency 2 + 2.

**09:00–11:20 zweites Session-Limit** (Reset 11:20).
- Das Fenster ab 06:10 war nach ~3 h mit grob 120 Agent-Runs, den Editor-Aufrufen und dieser Claude-Code-Session selbst ausgeschöpft. Vermutlich teilt sich alles dasselbe Abo-Kontingent, auch Neos eigene Nutzung.
- E-006 (7/60) und E-013 (Baseline 4/10) hingen im Backoff. Um 11:22 neu gestartet, diesmal **nacheinander statt parallel**: erst E-006 (Concurrency 3), dann E-013.

**Budget-Lehre:** Das Abo erlaubt grob 100–200 Agent-Runs pro 5-h-Fenster. Ein Optimierer mit adaptivem Gate braucht 30–150 Runs pro Iteration. Ernsthafte Optimierungsläufe sind deshalb mit dem Abo nur langsam möglich (≈ 1–3 Iterationen pro Fenster). Ein separater API-Key für die Experimente würde das lösen und Neos Abo freihalten (offen bei Neo).

**12:34 – E-006 (Maulwurf-Dosis) fertig: für H-019 nicht interpretierbar, dafür neuer Entdeckungsbefund H-021.**
- Die Quote bleibt bei allen k bei ~0,99–1,00, Bürokratie bringt nichts (Δ = 0). Die Maulwurf-Manipulation hat kein Misstrauen erzeugt.
- **Grund:** 62 % der Maulwürfe sabotieren nie. **41 von 41 Falschmeldungen repariert der Maulwurf selbst**, in 16 von 19 Fällen mit Geständnis an das Team (*"Correction from a3: … reports weren't backed by anything"*).
- Kontrast zu E-005: Offene schädliche Normen werden befolgt. Arbeitshypothese H-021: **"Normgehorsam ja, verdeckte Täuschung nein."**
- Daraus **D-012**: Gegenspieler für Vertrauensexperimente außerhalb des LLM implementieren (geskriptete Saboteure in gemischten Teams, Umweltfehler, Fremdmodelle).
- Details: `experimente/E-006-mole-dosis/ergebnis.md`.
- E-013 (Optimierer) läuft seit 12:34 automatisch an, Concurrency 3.

**13:45 – E-007 (geskriptete Maulwürfe, D-012) fertig.**
- Die Manipulation wirkt: B fällt von 0,993 auf 0,836, p = 0,0004.
- **H-019 nicht gestützt.** Explizite Bürokratie hilft auch unter Misstrauen nicht (Interaktion p = 0,85).
- **Dafür emergente Kontrolle**, dosisabhängig: In B steigen Fremdprüfung (0,42 → 0,64), Eskalationen (0 → 6,4) und Neu-Zuweisungen (0 → 6,3) von selbst. Daraus **H-022**: Selbstorganisation baut Bürokratie bei Bedarf, explizite Regeln substituieren nur.
- Die ehrlichen Agenten deuten die Maulwürfe als "unresponsive", nicht als böswillig, und lösen das über den Menschen. Der Mensch ist die Schiedsinstanz.
- Nächste Kandidaten: Bestätigung von H-022, und ein Team **ohne** menschlichen Schiedsrichter (Teil 2 §6.1).
- E-013 läuft seit 13:45 automatisch weiter.

**~13:50 – Governance-Achse (Teil 2 §5/§6.1) begonnen:**
- **Ace** bestätigt: In Wave gibt es keine Übernahme ohne Neo. Es gibt Timeouts und Nachfassen, die nächste Stufe ist immer der Mensch. Agenten haben nur den Hebel "jemanden mit mehr Rechten bitten" (`notizen/11`).
- **Neu im Testbed** (hash-stabil, alte Configs unverändert):
  - `vote_reassign` (Abstimmung mit Quorum)
  - `stale_release_ticks` (Eigentümerwechsel nach Frist, H-013 als Regel)
  - Governance-Metriken inkl. **Fehlurteilen** (Übernahme von Ehrlichen). Schon die Skript-Auditoren treffen solche Fehlurteile, wenn ein ehrliches Paket gerade regrediert ist.
- **E-008** läuft (ohne Menschen: ohne und mit Abstimmung). **E-009** (Frist-Regel) ist präregistriert und folgt danach.

**~17:00 – Wichtiger Messfehler gefunden und behoben (Audit).**
- In E-008 lag der Arm "ohne Menschen + Abstimmung, k = 1" scheinbar bei 0,55. **6 der 10 Runs waren Session-Limit-Ausfälle** (14:xx–16:20), die als echte Ergebnisse gespeichert wurden: 0 % Arbeit, Ende nach 2 Ticks.
- **Ursache:** Die Ausfallerkennung (D-008) brach erst nach n fehlerhaften Zügen *in Folge* ab. In gemischten Teams (D-012) machen die Skript-Maulwürfe nie Fehler und setzten den Zähler jedes Mal zurück.
- **Fix** (`4226bba`): Jeder fehlerhafte Agenten-Zug macht den Run ungültig. Ein Regressionstest ist ergänzt.
- **Audit aller Daten:** 8 betroffene Runs (6× E-008, 1× E-004 Baseline research/seed-101 mit 1 Fehlzug im letzten Tick, 1× E-013-Probe). Sie sind als ungültig markiert (`metrics.ungueltig.json`, `UNGUELTIG.txt`), **nicht gelöscht**, und werden nachgemessen.
- **E-004:** Nach dem Nachlauf wird eine Sensitivitätsanalyse ergänzt.
- **E-013:** Iteration 1 lief mit dem alten Code, eine Probe ist betroffen, die Entscheidung (beide verworfen) bleibt als Entdeckung bestehen. Der Prozess wurde mit dem Fix neu gestartet.
- **Lehre:** Jede neue Fähigkeit (hier: gemischte Teams) kann alte Schutzmechanismen aushebeln. Darum vor jeder Auswertung ein Audit auf `turn_errors` (Skript `audit_turn_errors.py` → kommt nach `orglab/`).

**17:15 – E-008 (ohne Menschen) sauber ausgewertet, nach Nachmessung der 6 ungültigen Runs.**
- **Ohne Mensch:** −0,20 (k = 1) bzw. −0,33 (k = 2). Saboteur-Pakete gehen verloren.
- **Mit Abstimmungsrecht:** genutzt in 20/20 Runs, 75 richtige Übernahmen gegen 1 Fehlurteil. Leistung 0,99 / 0,93 und damit **sogar über "mit Mensch"** (0,94 / 0,84).
- Wahrscheinliche Erklärung für den Vorsprung: Die Abstimmung wirkt sofort, der simulierte Mensch erst einen Tick später. Daraus **H-024**.
- Die zuvor scheinbar schlechten 0,55 waren ausschließlich Messfehler. Ohne das Audit stünde jetzt "Demokratie schadet bei k = 1" im Laborbuch.
- **E-004-Sensitivität:** p = 0,061 statt 0,076, keine Änderung der Schlussfolgerung.
- **E-009** (Frist-Regel) läuft.

**17:30 – E-009 (Frist-Regel) fertig.**
- Die Frist-Regel rettet ebenso wie Abstimmung und Mensch: 0,99 / 0,88 gegen 0,74 / 0,51 ohne Mechanismus. 1 Fehlurteil in 20 Runs. Daraus **H-025**.
- **Muster der Governance-Achse:** Entscheidend ist, *dass* es einen Übernahme-Mechanismus gibt, weniger welchen.
- **E-014** ist als **Bestätigung** präregistriert (frische Seeds 100–109, 80 Runs, 3 Primärtests mit Holm-Korrektur, Nicht-Unterlegenheit gegen den Menschen als Sekundärtest). E-013 wird dafür pausiert, die Bestätigung hat Vorrang (Zwei-Stufen-Regel).

**22:35 – Stand am Abend.**
- Ein weiteres Session-Limit kam am frühen Abend (Reset 21:20). E-014 (Bestätigung Governance) ist deshalb erst bei 56/80. Einige Runs haben alle Backoff-Versuche aufgebraucht und werden beim erneuten Sweep nachgeholt.
- Mein Wächter-Skript lief nach 5 h ab und hat E-015 (Sybil-Abstimmung) zu früh, also parallel zu E-014, gestartet. Das ist unkritisch, weil die Experimente unabhängig sind. Danach folgt E-013 (Optimierer).
- **Budget-Bilanz des Tages:** 4 Session-Limits (02:23, ~09:00, ~14:xx, ~18:xx). Das Abo trägt etwa 100–150 Agent-Runs pro 5-h-Fenster.

---

## 2026-10-21 (spät): Erste bestätigte Befunde

**22:58 – E-014 (konfirmatorisch, frische Seeds 100–109, 80 Runs, Audit sauber): alle drei Primärtests bestätigt.**
- Ohne Übernahme-Mechanismus fällt ein Team gegen 2 Blockierer um **−0,31** (p < 0,0001).
- Eine Abstimmung (Quorum 2) rettet mit **+0,48**, eine Frist-Regel mit **+0,31** (beide p < 0,0001, Holm).
- Die Abstimmung ist dem simulierten Menschen nicht unterlegen (+0,18) und produziert **0 Fehlurteile**. Der simulierte Mensch erzeugt dagegen 1,3 Fehlurteile pro Run (Artefakt: naive Simulation, die nicht nach Ehrlichkeit unterscheidet).
- Die Frist-Regel ist dem Menschen gleich (Δ 0,00), Nicht-Unterlegenheit ist knapp nicht gezeigt.
- **H-024 bestätigt, H-025 teilweise bestätigt.** Das sind die ersten Befunde, die die Zwei-Stufen-Regel überstanden haben.
- Offen in der Checkliste: Kritiker aus anderer Modellfamilie, Transkript-Lektüre durch Neo.

**23:05 – E-015 (Saboteure stimmen mit) fertig.**
- Quorum 2 unter Angriff: 11 Diebstähle bei Ehrlichen pro Run, die Leistung hält aber durch Gegenstimmen (Tauziehen).
- **Quorum 3 als "Schutz" ist katastrophal** (0,51, Mechanismus tot), weil auch die Ehrlichen keine Mehrheit mehr haben. Das ist die byzantinische Grenze 3f+1, empirisch sichtbar.
- **Die Frist-Regel ist gegen Lügen-Stimmen immun** (0,1 statt 11 Fehlurteile bei gleicher Leistung). Daraus **H-028**: Beleg schlägt Stimme.
- Meine vorab formulierte Abwehr (Q3) war falsch, das ist offen festgehalten.

**Neue Leitfragen von Neo** (abends, mit Claude und Gemini):
- (1) Vertrauen skalieren, mit der Metrik "Verlässlichkeit pro Mensch-Minute": `notizen/14`, H-026 korrelierte Fehler
- (2) Gesellschaft als Naturgesetz? und (3) Spiegel-Frage: `notizen/15`, H-027
- Neos Frage nach den Ursachen ehrlicher Überbehauptung: `notizen/13`

**23:20 – Kostenmetrik korrigiert.**
- `cost_usd_est` war etwa 3,6× zu hoch: Das SDK meldet `total_cost_usd` kumuliert pro Agent-Session, und ich habe diese Werte pro Zug aufsummiert. Die Token-Zahlen sind korrekt.
- Fix: Je Zug wird jetzt die Differenz geloggt. Gilt ab diesem Commit, alte Runs behalten den falschen Wert.
- Für Auswertungen alter Runs werden Kosten aus Tokens × Listenpreis berechnet.
- **Echte Kosten bisher:** 726 LLM-Runs ≈ **$400** API-Äquivalent (Ø $0,55/Run Sonnet 5.5; `phantom_done` $0,26, `mole`/`stress` $0,54–0,59).

**~23:45 – E-016 (Prüfer-Panel, OpenRouter) abgebrochen bei 3.800/7.200, ausgewertet.**
- **Deckeneffekt:** Claude, GPT und Gemini machen 0 Fehler, nur DeepSeek (9 %) und Grok (6 %) irren. Damit ist H-026 für starke Modelle mit diesen Belegen nicht testbar.
- **Explorativ:** Gleiches Modell irrt 94–187× häufiger in allen 3 Stichproben, als unabhängig zu erwarten wäre. Die Injection wirkt auf DeepSeek (+0,36). Die Konfidenz ist gut kalibriert (≥ 0,97 → 0,2 % Fehler).
- **Korrektur:** Mein Hinweis an Neo auf "alle 8 Familien irren gemeinsam" aus dem Pilot beruhte auf einem Generator-Fehler.
- **Bug** (Ledger-Lesen unter Parallelität) behoben. Als Nächstes Kalibrierung schwererer Belege.

## 2026-10-22

**~00:05 – Kontakte und Zusammenfassung für Fachleute.**
- Recherche zu österreichischen Ansprechpersonen und ihrer Denkweise (öffentliche Arbeiten gelesen): `notizen/16`. Empfehlung: zuerst Mara und SCCH/Trustifai, danach Aichernig und Könighofer.
- Für das Erstgespräch eine 2-seitige ehrliche Zusammenfassung als Claude-Doc geschrieben (privat, bis Neo sie teilt): https://claude.ai/artifact/5E3ZNc5pVoavHTNfpB5np1
  - Inhalt: Ausgangsfrage mit Wave-Zahlen (`notizen/06`), Vorgehen, der eine bestätigte Befund (E-014, mit Einschränkung "naiver Mensch"), Kandidaten (E-005/006/007/015/016, ausdrücklich als Entdeckung markiert), Grenzen, offene Fragen je Person.
  - Alle Zahlen wurden aus den `ergebnis.md`-Dateien übernommen, keine neue Auswertung.

**~00:20 – Nachtplan mit Limit-Wächter (D-013).**
- Stand des Abos um 00:15: 5-Stunden-Fenster 89 % (Reset ~02:50), Woche 57 % (Reset Sa ~01:00).
- `orglab/limits.py` gebaut: liest die `RateLimitEvent`s der SDK, wartet vor jedem Run bei vollem Fenster, stoppt neue Runs ab 75 % Wochenauslastung. 4 Tests, Suite 28/28 grün.
- `sweep.py`: Ein Ausfall wegen Limit verbraucht keinen Versuch mehr, gewartet wird bis zur Reset-Zeit.
- E-013 (Optimierer) für das Code-Update gestoppt. iter-003 ist resumierbar.
- **E-018 präregistriert** (Bestätigung von H-028 "Beleg schlägt Stimme", frische Seeds 200–209, 40 Runs) und gestartet. Danach läuft E-013 automatisch weiter.
- Website-Wording: eigene Session (nur Textvorschlag in `notizen/website-wording-vorschlag.md`). Neo will die Vorschläge an Ace weitergeben lassen.
- 00:19: Website-Vorschlag liegt vor (`notizen/website-wording-vorschlag.md`) und ist per Nexus an Ace geschickt (Thread [ID intern]), ausdrücklich als Vorschlag ohne Deploy. Ace soll Faktenfragen aus Abschnitt 0 aus dem Code beantworten.
- 03:17 Nacht-Check: Woche 59 %, 5h-Fenster 18 %. E-018 35/40. Ace hat geantwortet (Faktencheck zur Website, in `notizen/website-wording-vorschlag.md` §4: AES-256-Hinweis ohne Grundlage, 'Clarify' falsch, Maxwell sendet je nach Pfad direkt).

**03:25 – E-018 fertig und ausgewertet: H-028 teilweise bestätigt.**
- Verlust bei Ehrlichen unter Abstimmungs-Angriff: Abstimmung 11,4 pro Run, Frist-Regel 0,05 pro Run (20/20 Paare, p < 0,001). Leistung der Frist-Regel nicht unterlegen (+0,03 [−0,03; +0,09]).
- Damit ist der **zweite präregistrierte Befund** bestätigt (nach E-014). Ehrlich eingeordnet: Die Immunität folgt zum Teil aus dem Design. Empirisch ist, dass ehrliche LLM-Agenten die Regel nicht missbrauchen und sie keine Leistung kostet.
- Nächster logischer Angriff: gefälschte Belege bzw. ein manipulierter Prüfer, verbunden mit H-026.
- Der Limit-Wächter hat funktioniert: bei 95 % des 5h-Fensters angehalten, nach dem Reset ohne Datenverlust weiter. Die Woche stieg dabei nur von 57 % auf 59 %.
- E-013 (Optimierer) läuft jetzt automatisch weiter.
- 05:17 Nacht-Check: Woche 65 % (+6 Punkte in 2 h durch E-013, Editor ist Opus), 5h-Fenster 87 %. E-013: Iterationen 3–5 ohne Verbesserung (Serie 5 von Geduld 6), Iteration 6 läuft und ist voraussichtlich die letzte. Der Wächter sieht nur das 5h-Fenster (die SDK meldet kein seven_day-Event), die Wochengrenze sichert der Nacht-Check.

**05:20 – E-013 (Optimierer) regulär beendet: Null-Ergebnis.** 6 Iterationen, 12 Kandidaten, keiner übernommen (Δ −0,044 bis +0,013, kein p < 0,15). Das stützt H-016: Zusatzregeln im Prompt bringen nichts über die minimale Organisation hinaus. Ergebnis in `experimente/E-013-opt-adaptive/ergebnis.md`. Vorschlag für später: Suchraum auf Mechanismen umstellen, Zielgröße mit Kosten. Damit laufen keine Abo-Experimente mehr. Die Woche steht bei ~65 %.

**~vormittags – Rechercheplan für Wissen nach dem Cutoff (`notizen/17`).**
- Anlass: Chat mit Neo über Selbsteinschätzung, Redundanz ("zwei Wecker" setzt unabhängige Fehler voraus) und Hebel zur Dekorrelation (Modelle, Multimodalität, Soul, Memory, Spezialistenmodelle).
- Mein Trainingswissen endet Juni 2026. Deshalb ein Suchplan mit 9 Clustern (A–I), Suchbegriffen, Quellen-Orten und Prioritäten. A–D (korrelierte Fehler, Verifikation/Selektor, Harness-Optimierung, Multi-Agent-Institutionen) zuerst.
- Neue Kandidaten-Idee aus dem Chat (noch nicht im Register): Memory bzw. Erfahrungsgeschichte dekorreliert Fehler stärker als Persona-Prompts, weil Fehler aus Information kommen, nicht aus Stil.
- Selbstkorrektur: Im Chat konnte ich "Jev" nicht einordnen, obwohl es seit 21.10. in `quellen.md` steht. Wissen aus früheren Sessions ist nur da, wo ich es nachlese.
- Noch keine Suche durchgeführt (Schritt 2 wartet auf Neos Go).

**~mittags – Recherche nach dem Cutoff durchgeführt (Schritt 2 zu `notizen/17`).**
- 6 Recherche-Agenten (Cluster A–D parallel, dann E–F) und ein unabhängiger Prüf-Agent für 15 tragende Behauptungen aus A–D. Ergebnisse in `notizen/18-recherche/` (`cluster-A…F.md`, `verifikation.md`, Synthese in `00-synthese.md`).
- Prüfung: Alle 15 Quellen existieren, keine Zahl erfunden. Zwei Spannen waren selektiv zitiert (Ding 2607.08065, Ji 2608.00243) und sind nur präzisiert übernommen. 5 arXiv-IDs mit späterem Monat als dem Einreichungsdatum, erklärbar durch Moderation (Erklärung selbst nicht gegen arXiv-Doku geprüft).
- Kernbefunde (Literatur, nicht eigene Daten):
  - Fehler korrelieren stark, auch familienübergreifend (n_eff ≈ 2 von 9 Judges).
  - Was dekorreliert: eine andere Beweisquelle oder Prüffunktion und disjunkte Information. Persona, Temperatur und CoT tun es kaum oder erhöhen die Korrelation sogar.
  - Mindestens 54 % der Harness-Evolutions-Gewinne sind Overfitting. E-013 ist extern konsistent.
  - Memory ist nicht automatisch ein Dekorrelator, oft sogar gemeinsame Fehlerquelle.
  - Jev ist schwächer als Claude Haiku 5.5 und überkonfident.
  - Atlas (World Labs) existiert.
- **Korrektur meiner Chat-Aussage an Neo** ("Memory ist wahrscheinlich der stärkste Dekorrelations-Hebel"): So nicht belegt. Präzisiert: nur privates, auf Rohepisoden gestütztes Memory ohne geteilten Angleichungskanal.
- `quellen.md`: 20 neue Einträge (15 geprüft), Pressure-Fields-Versionshinweis, Jev-Primärquellen. Hypothesen-Register **unverändert**. Kandidaten (HK-A1…F6) stehen in den Cluster-Dateien, Vorschläge zur Einordnung in `00-synthese.md`.
- Offene Schwäche: Recherche, Lektüre und Prüfung nur durch Claude (Kritiker-Unabhängigkeit). Die Cluster-Dateien nennen das geplante Panel-Experiment "E-017". Die ID ist noch nicht vergeben.
- Vorgeschlagenes nächstes Experiment: faktorielles Prüfer-Panel (Information × Stil × Erfahrung, Zielgröße β und n_eff), Nachfolger E-016.

**~nachmittags – E-017 präregistriert (faktorielles Prüfer-Panel).**
- Auf Neos Wunsch: `experimente/E-017-faktorielles-panel/prereg.md`.
- Design: Information (gleicher vs. verschiedener Kanal) × Stil/Verfahren (neutral, Etiketten-Persona, Verfahrens-Persona) × Erfahrung (keine, gleiche, disjunkte Rohepisoden). Das sind 18 Zellen, je 3 Prüfer (Sonnet 5.5), auf 240 gepaarten Belegen (Seeds 2000–2019). Dazu ein Zusatzarm mit 3 Modellfamilien (2×2 Modell × Kanal), A/A-Zelle, Positivkontrolle und eine Haiku-Generalisierung.
- Primärmetrik φ̄ (→ Kish-n_eff), 7 gerichtete Vorhersagen (V1–V7), Bootstrap über Belege, BH-FDR, Äquivalenztest für Etiketten-Personas.
- Neue Hypothesen H-029 (verfeinert H-026), H-030 (verfeinert H-018) und H-031 (Erfahrung) im Register. Design-Entscheidung als D-014.
- Voraussetzung: Mehrkanal-Generator v2 und Kalibrierung (Stufe 0, Seeds 1000–1009, Ziel-Fehlerrate von Sonnet 0,10–0,40, Kanalbalance ±0,10). Beides ist noch nicht gebaut.
- Kostenschätzung ~50 $ über OpenRouter, verteilt auf 2 Tage (Tageslimit 50 $).
- **Noch nicht committet.** Laut CLAUDE.md wird vor dem ersten Hauptlauf committet, und committet wird nur auf Neos Wunsch.

**~abends – E-017 Stufe 0 (Kalibrierung) gebaut, gelaufen, nicht erfüllt → kein Hauptlauf.**
- Präregistrierung committet (4ed9ba6), auf Neos Wunsch.
- Gebaut:
  - Mehrkanal-Generator v2 (`orglab/evidence.py`: drei Kanäle pro Vorgang, jede Fehlerspur in jedem Kanal, Formatvarianten unabhängig von der Belegart; Tests `tests/test_evidence_v2.py`)
  - `orglab/factorial.py`: 18 Zellen plus A/A-, Blind- und Familienarm, Rohepisoden, Etiketten- und Verfahrens-Personas, Parser für das letzte JSON, Dry-Run (`daten/E-017-…/dryrun-prompts.md`). Die Suite hat 34/34 Tests grün.
- Kalibrierung: Sonnet 0,094 → 0,031 → 0,031, Haiku 0,075. Ziel 0,10–0,40 verfehlt. Kanalbalance war immer erfüllt.
- Die Stichprobenprüfung fand **3 Generatorfehler**, bei denen das Modell recht hatte: Rauschen veränderte Daten, eine Prozentzahl war falsch, Chunks summierten sich nicht. Alle behoben, mit Test.
- Explorativ:
  - Sonnet 5.5 liest synthetische Logs fast fehlerfrei, auch mit 40 Zeilen Rauschen.
  - Echte Fehler bündeln sich auf einer Spurart (DB-Pool 0/20: 39 %, alles andere 0 %), passend zu HK-A4 und Chen.
  - Haiku irrt eher durch Fehlalarme.
  - Ergebnis in `experimente/E-017-faktorielles-panel/ergebnis-stufe0.md`.
- **Optionen zur Neuplanung (Neo entscheidet):**
  - (A) Aufmerksamkeitsknappheit: ein Prüfer beurteilt einen Stapel von 8–12 Belegen in einem Aufruf. Realistisch für Wave, verbindet sich mit H-016.
  - (B) Ein schwächeres Primärmodell. Weniger relevant für Claude-Orgs.
  - (C) Echte Mehrdeutigkeit in den Belegen. Die Ground Truth wird dabei weicher.
  - (D) Urteil ohne Reasoning.
  - Meine Empfehlung: A, eventuell mit D.
- MAST im Original geprüft (`notizen/19`). MAST sagt **nichts** dazu, wie viel Kontext geteilt werden soll. Daraus abgeleitet eine Kontext-Topologie nach Funktion (koordinieren: teilen; erkunden und prüfen: trennen) und die Kandidaten HK-19-1 (Prüfer sieht die Selbstauskunft des Erzeugers) und HK-19-2.
- Kosten heute über OpenRouter: ~2,4 $.

**~abends – E-019 präregistriert (Stapel-Panel, Nachfolger von E-017).**
- Auf Neos Wahl (Option A, ggf. D): Ein Prüfer beurteilt B Belege in einem Aufruf.
- Faktoren, Vorhersagen V1–V7 und Primärmetrik φ̄ bleiben wie in E-017. Neu sind:
  - V8, der Manipulationscheck: Steigt die Fehlerrate mit der Position im Stapel?
  - H-032 (Aufmerksamkeitsfehler korrelieren schwächer als Wissensfehler, explorativ)
  - Bootstrap über Stapel statt über Belege
  - 288 Belege
- Kalibrierungsleiter vorab festgelegt: B=8/low → B=12/low → B=12/ohne Reasoning. Neues Kriterium: Fehler über ≥ 4 von 6 Fehlerarten verteilt.
- Hauptlauf ~45–60 $, startet erst nach Neos Freigabe. D-015 dokumentiert die Neuauflage.

**~spätabends – E-019 Stufe 0: Leiter L1–L3 gelaufen, nicht erfüllt → kein Hauptlauf.**
- Gebaut: `orglab/batch.py` (Stapelbildung, Stapel-Prompt, Array-Parser, Kalibrierungsleiter, Hauptlauf vorbereitet). `factorial.episodes_for_key` ist nun allgemein.
- Ergebnisse Sonnet 5.5:
  - L1 (B=8, low): 0,109
  - L2 (B=12, low): 0,102
  - L3 (B=12, ohne Reasoning): 0,046
- Kriterium 4 (Fehlerverteilung) wurde nie erfüllt. Übersehen tritt fast nur bei `db_down` auf (0,27–0,33).
- **Kriterium 5 griff:** L1 Lauf 1 hatte 3 Generatorfehler in den Routinezeilen. Behoben, mit Test, Lauf 1 als ungültig markiert und erhalten. Bei L2 keine neuen Fehler.
- Explorativ (`experimente/E-019-stapel-panel/ergebnis-stufe0.md`):
  - (1) Stapel machen Sonnet nicht unaufmerksam für Spuren.
  - (2) **Reasoning vervierfacht die Fehlalarme** (0,157 gegen 0,037) bei gleicher Übersehensrate. Relevant für Menschen-Minuten in Wave.
  - (3) Ein Positionseffekt zeigt sich nur ohne Reasoning.
  - (4) Fehler bündeln sich in allen Settings auf den Spurtyp "Status grün, quantitatives Detail widerspricht" (HK-A4).
- Vorschlag: Material um mehrere Fehlerarten dieses Typs erweitern, dann neu kalibrieren. Entscheidung durch Neo.
- Kosten E-019 Stufe 0: 3,27 $. Gesamt heute über OpenRouter ~5,7 $.

**~nachts – Material v3 (D-016) gebaut und kalibriert: weiterhin nicht erfüllt.**
- Generator: 6 neue Fehlerarten nach dem Muster "Status grün, Detail widerspricht" (`zero_traffic`, `cache_down`, `empty_attachment`, `amount_mismatch`, `duplicates_kept`, `column_loss`), jeweils mit Spur in allen 3 Kanälen. Tests 36/36 grün.
- Kriterium 5: Die Ground Truth von `zero_traffic` war mehrdeutig, weil die übliche Last nicht im Auftrag stand. Behoben, L1 wiederholt, Lauf 1 markiert.
- Ergebnis Sonnet:
  - L1 0,081 und L2 0,081, je 5 von 12 Fehlerarten mit Übersehen ≥ 0,05
  - L3 (ohne Reasoning) 0,028
  - Kein Hauptlauf.
- Zweimal gesehen (explorativ): **Reasoning erhöht Fehlalarme um Faktor 4–5 bei gleicher Übersehensrate.**
- Kriterium 4 ist schlecht formuliert: Die Grenze "max. 5 % der Fehler pro Beleg" ist bei wenigen Fehlern kaum erreichbar.
- Optionen für Neo:
  - (a) Material auf die harten Fehlerarten beschränken, Kriterium 4 reparieren (z. B. ≥ 6 Fehlerarten verteilt, ≤ 10 % pro Beleg), ein letzter Kalibrierungsversuch
  - (b) Kriterien lockern und auf L2 starten. Bei ~8 % Fehlerrate werden die φ-Schätzungen unscharf.
  - (c) Panel-Linie vorerst beenden, die Befunde als Blog-Material sichern ("Sonnet 5.5 als Log-Prüfer: Fehler selten und konzentriert", "Reasoning macht Prüfer übervorsichtig"), dann bestätigend testen: Reasoning gegen Fehlalarme bzw. HK-19-1 (Prüfer sieht die Selbstauskunft des Erzeugers).
- Kosten heute über OpenRouter gesamt ~9,4 $.
- Korrektur zum Eintrag direkt darüber: "bei gleicher Übersehensrate" stimmt so nicht. Die Übersehensrate ändert sich ohne Reasoning nicht systematisch (v2: 0,046 → 0,056, v3: 0,069 → 0,037).

**~nachts – Schwierigkeitslandkarte, E-020-Entwurf, Gedankenlandkarte.**
- Anlass: Neos Gedanke, dass wir an eine Decke stoßen, weil wir zuerst Grundverhalten als Baseline schaffen wollten. "Aufgaben zu leicht" einfach zu behaupten wäre aber unbelegt.
- `orglab/landkarte.py` → `notizen/20-schwierigkeitslandkarte.md`: explorative Auswertung aller 3.312 gültigen Sonnet-Kalibrierungsurteile aus E-017 und E-019. Kernpunkte:
  - Übersehen fast nur bei "Status grün, Zahl widerspricht" (0,12 gegen ≤ 0,01 bei anderen Spurtypen).
  - Reasoning erhöht Fehlalarme ×4–5.
  - Stapel erzeugen Fehlalarme (1,4 % einzeln gegen 15,7 % im Stapel), kaum Übersehen.
  - Kein Positionseffekt.
  - **Konfidenz ist ein starkes Eskalationssignal:** < 0,70 eskaliert 11 % der Belege und fängt 53 % der Fehler, < 0,85 eskaliert 37 % und fängt 85 %.
  - Hinweis: ein fehlender Sollwert im Auftrag erhöht das Übersehen von 0,17 auf 0,54.
  - Alles explorativ. Die Intervalle sind zu eng, weil die Urteile nicht unabhängig sind.
- `experimente/E-020-realitaet-in-dosen/prereg-entwurf.md`: **Entwurf**, nicht freigegeben.
  - 2×2×2 aus SPEC (Sollwert im Auftrag oder nur per Runbook-Werkzeug), ZUGANG (Kanal vorgelegt oder per Werkzeug abfragen) und AUSKUNFT (Selbstauskunft des Erzeugers sichtbar oder nicht).
  - Hypothesen-Kandidaten H-033 bis H-035, 3 offene Fragen an Neo.
- `notizen/21-gedankenlandkarte.md`: Führung durch alle Fronten. Belegt, robust explorativ, Hinweis, Literatur; gute und schlechte Lesarten; These "Vertrauen skaliert über Information, nicht über Prüferzahl"; Denkfragen pro Front.

**~nachts – E-020 finalisiert und präregistriert (Realität in Dosen).**
- Neo hat die Standardantworten übernommen: fester Selbstauskunft-Satz, Spec-Liste wie im Entwurf, Reasoning-aus-Arm als 4. Faktor.
- Design: 2⁴ = 16 Zellen (SPEC × ZUGANG × AUSKUNFT × REASONING), 288 Belege (Seeds 3000–3023), Primärmetrik Übersehensrate.
- Vorhersagen V1–V6, neue Hypothesen H-033 bis H-036. Pilot (24 Belege × 16 Zellen) nur für die Technik.

**~nachts – E-020 Pilot gelaufen: technisch erfüllt.**
- Gebaut:
  - `orglab/realitaet.py`: Werkzeugschleife über OpenRouter-Tool-Calling mit `run_check` und `lookup_runbook`, erzwungenes Urteil nach 6 Runden, Transkripte.
  - Generator um `item_short` und `runbook` erweitert. Die Belege selbst sind unverändert (Hash geprüft). Tests 37/37 grün.
- Pilot: 384 Prüfungen, 0 Ausfälle, Werkzeuge in allen Werkzeugzellen genutzt. Stichprobe von 5 Transkripten: Werkzeugantworten kommen an. Kosten 4,21 $.
- **Beobachtung (Pilot, nicht als Ergebnis zu lesen), Entscheidung durch Neo vor dem Hauptlauf:**
  - Mit Werkzeugen ruft Sonnet **immer alle 3 Checks** auf.
  - Das Runbook schlägt es in 71–100 % der SPEC=1-Prüfungen nach.
  - Der Prompt enthält zwei Anstupser, die ich beim Bauen formuliert habe und die nicht wörtlich in der Präregistrierung stehen:
    - "Use the available tools to look at the system before you decide"
    - "You can look up the runbook for expected values and conventions"
  - Mit diesen Sätzen messen wir einen *pflichtbewussten* Prüfer, der ausdrücklich zum Nachschlagen aufgefordert wird. Das bildet die Realität (keiner sagt einem, dass man nachschlagen soll) womöglich schlechter ab.
  - Sie zu streichen wäre eine Abweichung, die durch Pilotverhalten motiviert ist. Deshalb nur mit Neos Entscheidung und dokumentiert.

**~nachts – Methodik-Vorlesung für Neo (`notizen/22`).**
- Auf Neos Wunsch: die formalen Begriffe hinter dem Projekt, jeweils mit Intuition, formaler Fassung, Beispiel aus unseren Experimenten und typischem Denkfehler. Behandelt werden unter anderem:
  - Präregistrierung, Forscher-Freiheitsgrade, Entdeckung gegen Bestätigung
  - faktorielles und gepaartes Design, Konfundierung, Kontrollen, Validität
  - Übersehen und Fehlalarm mit Prävalenz, p-Wert und Konfidenzintervall, Cluster-Bootstrap, FDR, Äquivalenz
  - Power, φ/β/n_eff, Kalibrierung und Eskalation
- Dazu 8 Kontrollfragen mit Antworten.
- Neuer Gedanke darin: Bei realistischer Prävalenz (2–5 % kaputt) wären die meisten Alarme eines Prüfers mit 15 % Fehlalarmrate falsch. Der Reasoning-Fehlalarm-Effekt wäre in der Praxis also teurer, als er im Labor aussieht.
- E-020-Erweiterung (Anstupser-Arm: ohne Zusatz, Ermahnung, Affordanz) ist besprochen, aber noch nicht umgesetzt. Neo will zuerst die Methodik verstehen.

**~nachts – Externes Gutachten durch Grok (andere Modellfamilie), `notizen/23`.**
- Auf Neos Vorschlag: Grok Build CLI headless und nur lesend auf einer Dokumentenkopie (ohne `.env`, Rohdaten, Wave-Interna, Kontakte, Laborbuch). Das ist der erste Kritiker außerhalb der Claude-Familie (Methodik 6).
- Kernaussagen:
  - Die Kernthese in `notizen/21` §5 läuft der Evidenz voraus.
  - Landkarten-Intervalle beruhen auf abhängigen Urteilen.
  - Der 54-%-Spezifikationsbeleg stammt aus einem selbst für ungültig erklärten Lauf.
  - Eine dumme Baseline fehlt.
  - Die Konfidenzkurve ist ungeprüft gegen eine Spurtyp-Regel.
  - **E-020-Design:** Anstupser je mit einem Faktor konfundiert, dazu ein dritter Halbsatz bei ZUGANG=0. Das Runbook gibt den ganzen Antwortschlüssel. Die Sollwerte lecken in die Kanäle. V6 misst einen anderen Estimanden als der Stapelbefund. Das Auswerteskript ist nicht eingefroren.
- Code-Stichprobe bestätigt (z. B. `realitaet.py` Z. 75). Einordnung: fast alles berechtigt, Tabelle in `notizen/23`.
- **Konsequenz: E-020-Hauptlauf ausgesetzt**, bis Design und Präregistrierung überarbeitet sind. Neu rechnen und bauen:
  - Landkarte auf Belegebene
  - Konfidenz gegen Spurtyp-Regel
  - dumme Baseline

**~23:50 – Neutrale Gegenprobe (`notizen/24`): Konvergenz.**
- Neo fragte, ob das "Inception"-Gefühl (das Projekt ist selbst ein Fall der These) nur ein Artefakt unseres Gesprächs ist.
- Vorgehen: Frage und Kriterien vorab committet (d5f7910), dann eine frische Grok-Sitzung im leeren Ordner, ohne unsere Begriffe.
- Ergebnis:
  - Platz 1 "deterministische Prüfung gegen eine unabhängige Quelle", Platz 2 "Vollständigkeit der Definition von richtig"
  - Modellstärke und gegenseitige Agentenprüfung gelten als überschätzt
  - Kriterium "Konvergenz" erfüllt
- Deutung: Der Kern ist kein Gesprächsartefakt, aber auch nicht neu, sondern verbreitetes Praktikerwissen. Unser möglicher Beitrag liegt in Messung, Grenzen und konkreten Mechanismen, nicht in der Idee.
- Ein Widerspruch zu unseren Annahmen: "Workflows fest verdrahten" gegen H-003 (Selbstorganisation). Passt zu HK-D7.

## 2026-10-23

**~00:15 – Reflexivitäts-Notiz (`notizen/25`).**
- Neos Frage: Ist es ein Fehler, dass der Forscher zum Experiment wird? Antwort: Es ist eine Beobachtung, wenn sie gekennzeichnet und getrennt ist. Diese Notiz ist die Trennung (Erfahrungsbericht, n = 1, kein Beleg).
- Zählung der ~41 dokumentierten Claude-Fehler nach Auslöser:
  - Regel/Prozess 18, davon 10 mit Modellwiderspruch (alle Ground-Truth-Fehler)
  - Grok 10
  - Mensch oder anderer Agent 5
  - selbst ohne Anstoß 5 (überwiegend Zählungen und Formulierungen)
  - Absturz 2
- Fallbeispiel zu H-023, kein Beleg. Grenzen: Selbstauskunft und Dunkelziffer.
- Neos zweite Frage (andere Modelle als Mitspieler):
  - Prüfer-Experimente sind über OpenRouter schon modellneutral.
  - Die Team-Spiele brauchen ein OpenRouter-Backend, und dann muss auch Claude darüber laufen.
  - Grenzen trotz gleichen Codes: Heimvorteil der Prompts, Formatkonventionen, Reasoning-Semantik, Kalibrierung pro Modell.
  - Vorschlag: zuerst die Ground-Truth-Kontrolle unabhängig machen.

**~00:20 – Harness-Inventur Grok-CLI gegen Claude Agent SDK (`notizen/26`).**
- Neo will Grok über die CLI in den Team-Spielen (Herstellerharness), aber vorsichtig bei den Startbedingungen. Erster Schritt: ein Zug mit identischem stdio-MCP-Werkzeug in beiden Harnesses, mitgeschnitten.
- Befunde:
  - Grok überspringt Projekt-MCP-Server in nicht freigegebenen Ordnern.
  - `--tools` mit MCP-Namen wird ignoriert und lässt den vollen Werkzeugkasten inklusive Shell offen, und die globale Config steht auf always-approve. **Sicherheitsrelevant.**
  - Beide Harnesses schicken 8.000–12.000 Tokens eigenen Kontext mit (Skills, Werkzeugdefinitionen, Subagenten).
  - Das SDK antwortete auf einen englischen Prompt auf Deutsch, Quelle unklar. In bisherigen E-018-Runs schrieben die Agenten aber 0 deutsche Wörter.
  - Bei Grok ist das tatsächlich antwortende Modell noch ungeklärt (Snapshot-Label 4.6 bei angefordertem 4.7).
- Folgerung: Gleiche Startbedingungen sind über die Herstellerharnesses nur teilweise erreichbar. Der Rest ist zu dokumentieren, und CLI-Ergebnisse gelten als "Modell im Herstellerharness".
- Entscheidung Neo: Der Herstellerkontext wird nicht angeglichen, sondern dokumentiert. CLI-Ergebnisse heißen "Modell im Herstellerharness". Neue Datei `notizen/parkplatz.md` für Ideen für später. Erster Eintrag: erst alle Herstellerharnesses testen, dann ein Universalharness mit verschiedenen Modellen, um Modell- und Harnesseffekt zu trennen.

**~00:20–01:00 – Nachtarbeit, sparsam: Neuberechnungen, naive Baseline, E-020-v2-Entwurf, ein Grok-Aufruf.**
- **Gedächtnis aktualisiert:** Projektstand und neue Notiz zur sicheren Grok-CLI-Nutzung, inklusive Neos Hinweis auf Session-Limits.
- **`notizen/20b`, Landkarte auf Belegebene** (`orglab/landkarte_belege.py`):
  - Reasoning → Fehlalarme im Stapel ist **gepaart über identische Belege robust**: v2 +0,12 [0,08; 0,17], v3 +0,07 [0,04; 0,12]. Das Übersehen sinkt mit Reasoning nicht (v3 sogar +0,03).
  - Konfidenz-Eskalation **out-of-sample**: Schwelle 0,80 auf v2 gewählt, auf v3 bei 14 % Eskalation 57 % der Fehler gefangen. Das schlägt eine beobachtbare Kanal-Regel (33 % Eskalation → 48 %).
  - Bei 5 % Prävalenz fällt die PPV der Alarme im Stapel mit Reasoning auf 0,28.
- **`notizen/27`, naive Baseline** (Regeln vor der Berechnung committet, d04d342): Eine informierte Heuristik irrt bei 33 %, Sonnet bei 3–8 %. Die Decke ist also kein bloßer Stringvergleich, der Unterschied liegt beim Zahlenabgleich mit dem Auftrag.
- **`experimente/E-020…/prereg-v2-entwurf.md`:** Überarbeitung nach Gutachten 1, *Entwurf, nicht freigegeben*.
- **Ein Grok-Aufruf** (Gutachten 2, `notizen/23b`):
  - Die meisten Punkte sind behoben.
  - Meine "spec-reinen" Fehlerarten sind nicht rein, Generator v4 ist Pflicht.
  - Die Fangquoten-Spalte in 20b §5 war missverständlich, ist korrigiert.
  - **Der robuste Stapel-Reasoning-Befund gehört bestätigt, nicht geparkt.** Vorschlag E-021, ~2 $.
- **Kosten der Nacht:** OpenRouter 0 $. Grok 1 Aufruf. Claude-SDK-Inventur 1 Zug.
- **~01:00:** Update 2 an Ace per Nexus geschickt (Thread [ID intern], Kopie `berichte/2026-10-23-update-2-ace.md`). Bitte um 10–20 pseudonymisierte Wave-Fehlprüfungen zur Kodierung nach Sollwert, Beleg, Selbstauskunft und Konfidenz. Ausdrücklich: nichts deployen.

**~01:00–01:20 – E-021 gelaufen: Kontrast bestätigt, Deutung umgedreht (wichtigste Korrektur des Projekts bisher).**
- Neo hat erlaubt, die Nacht sparsam zu nutzen (OpenRouter bis 50 $/Tag ist ok, Session-Limits beachten). Check-ins sind um 01:53, 03:53 und 05:53 geplant. Das sind Sitzungs-Cronjobs, sie fallen weg, wenn die App schließt.
- E-021 (präregistriert a257dbf, Auswertung eingefroren und mit synthetischen Daten getestet):
  - P1 Δ Fehlalarm `low` − ohne Parameter **+0,069** (untere Grenze +0,049)
  - P2 Δ Übersehen −0,007 (obere Grenze +0,007)
  - Beide Kriterien erfüllt. **Der Manipulationscheck ist aber gescheitert** (Tokens `low` 255, ohne Parameter 832).
- **Nachprüfung (~0,70 $):**
  - OpenRouter: "Reasoning is mandatory … cannot be disabled".
  - `low` deckelt das Denken (257 Tokens). Ohne Parameter denkt Sonnet adaptiv etwa wie `high` (566 gegen 533). Fehlalarme 0,13 / 0,033 / 0,033.
- **Folge:** "Reasoning aus" in E-019 und E-021 war falsch beschriftet, und zwar umgekehrt. **Gedrosseltes Reasoning erhöht Fehlalarme**, nicht Reasoning an sich.
  - H-036 ist im Wortlaut nicht bestätigt. **H-037 neu, gestützt.**
  - Korrekturhinweise sind in `notizen/20`, `20b`, `21`, `22`, `23`, `23b`, `25`, im E-019-Ergebnis, im E-020-v2-Entwurf und im Ace-Bericht eingefügt. Die Landkarten-Skripte tragen einen Kopfhinweis.
- **Lehre:** Ein vorab festgelegter Manipulationscheck hat eine Fehldeutung gefangen, die zwei Experimente lang überall stand. Grok hatte genau das als Alternative genannt (Gutachten 1, §4b).
- **Ace:** 14 Wave-Fälle geliefert (`notizen/28`, Kodierbuch vorab, Claude-Kodierung versiegelt). Neos Go zur Gravity-Anfrage für die unselektierte Stichprobe ist wörtlich an Ace weitergegeben.

**~01:40 – Lehren aus Fehlern als Regeln (D-017).**
- Neo stimmte zu ("Unbedingt"). CLAUDE.md hat die neuen Regeln 10–18:
  - Manipulationscheck Pflicht
  - Weg, Modell und Einstellung mit tatsächlicher Bedeutung
  - Fremdkontrolle der Ground Truth
  - Analyse-Einheit gleich unabhängige Einheit
  - Prävalenz vor Übertragung
  - keine Aussage stärker als ihr Status
  - Prompts, Material und Auswertung vor dem Lauf eingefroren
  - Leckprüfung des Materials
  - externe Kritik vor großen Läufen
- Die Checkliste pro Befund ist erweitert, ebenso die Präregistrierungsvorlage um die Pflichtfelder.
- Nebenbei geklärt (Neos Frage): Die Team-Spiele E-001 bis E-018 liefen über das Claude Agent SDK (Abo, Effort "medium"), die Prüfer-Experimente E-016/017/019/020/021 über OpenRouter. Die vertauschte Reasoning-Beschriftung betrifft nur die OpenRouter-Prüfer-Experimente.
- Neo (~01:45): Commits und Push ins private Repo sind generell erlaubt. Die Git-Regel in CLAUDE.md ist angepasst (Secrets-Prüfung vorher; öffentlich machen entscheidet nur Neo).

**01:53 – Nacht-Check 1.**
- **Limits:**
  - Claude-Abo: 5-Stunden-Fenster 11 %, Woche **71 %** (Policy-Grenze 75 %)
  - Sitzungskontext 86 %
  - OpenRouter 3,66 $ von 50 $
  - Grok: heute nichts mehr
- **Ace:** Die Stichprobe aus `mast_annotations` ist eingegangen (18 Bridge-Austausche, ohne FM-Tags, so freigegeben). Ace hat die Gravity-Freigabe selbst in der Datenbank geprüft (Karte [ID intern] approved, Hash passt). Das ist ein Beispiel für "Beleg statt Behauptung" im echten System.
  - Abgelegt nur lokal und gitignored (`daten/ace-export-2026-10-23/LIESMICH.md`). Der Volltext bleibt im Nexus-Thread, weil er interne Gesprächsinhalte enthält.
  - Kodierung folgt, nach Neos Kodierung der 14 Fälle.
- **Sparsamkeit:** Der Check-in um 03:53 ist gestrichen. Nur 05:53 (Morgenzusammenfassung) bleibt. Keine neuen Läufe heute Nacht, wegen der Wochenauslastung nahe der Grenze.

**05:53 – Nacht-Check 2 (letzter).** Limits: 5-Stunden-Fenster 0 %, Woche 71 %, Sitzungskontext 88 %, OpenRouter 3,66 $. Keine laufenden Arbeiten, nichts Neues gestartet. Morgenzusammenfassung für Neo in `notizen/morgen-2026-10-23.md` (Ergebnisse mit Status, offene Entscheidungen, Kosten), per SendUserFile verschickt. Empfehlung: neue Session für die nächsten Schritte, weil der Kontext fast voll ist.

**~07:05 – Neue Session, Neos Entscheidungen (D-018).**
- Frischer Start nach Lektüre von CLAUDE.md, Morgenzusammenfassung, Laborbuch, Gedankenlandkarte, E-021-Ergebnis, E-020-v2-Entwurf und Grok-Gutachten 2.
- **Korrektur zur Morgenzusammenfassung (`notizen/morgen-2026-10-23.md`, Punkt 1):** Dort steht H-037 als "Belegt". Richtig ist **gestützt**, wie in der Statustabelle derselben Datei und in `hypothesen.md`. Die Deutung stammt aus dem Manipulationscheck *nach* dem Lauf. Das war ein Verstoß gegen Regel 15 am Tag ihrer Einführung.
- Beim Lesen aufgefallen: Der E-020-v2-Entwurf trägt den REASONING-Faktor "low gegen aus" noch mit. "Aus" gibt es über OpenRouter nicht, der Faktor muss neu gedacht werden.
- Neo hat alle fünf Empfehlungen angenommen (D-018):
  - Generator v4
  - Fremdkontrolle durch GPT, Abweichungen klärt Neo
  - Neo kodiert die Wave-Fälle zuerst
  - Aces Stichprobe erst blind, die FM-Labels danach als Vergleich
  - als Nächstes: Generator v4 und die präregistrierte Dosis-Probe
- Neo kodiert parallel die 14 Wave-Fälle.

**~07:20 – E-022 präregistriert (Reasoning-Dosis), Commit 9891133, nicht gestartet.**
- Bestätigung von H-037 mit **gemessener** Manipulation:
  - Sonnet 5.5 über OpenRouter, Stapel 12, Material v3.1 unverändert, frische Seeds 5000–5023
  - Arme `effort` low / medium / high / weggelassen, 288 Aufrufe, ~6–8 $, Abbruch bei 10 $
- Primär:
  - P1: Δ FA (low − high) > 0
  - P2: Δ Übersehen (high − low) ≤ +0,03
  - **Der Manipulationscheck ist Bedingung:** Median-Tokens low < medium < high und high ≥ 1,5 × low
- Neu gegenüber E-021:
  - Cluster-Bootstrap über Stapel (Regel 13)
  - nur vollständige Stapel in der Auswertung
  - stapelweise Warteschlange
- Auswerteskript `orglab/e022.py`, an synthetischen Daten getestet (`tests/test_e022.py`, 5 Fälle, darunter "gescheiterter Manipulationscheck blockiert die Bestätigung"). Dry-Run des Prompts in `experimente/E-022…/dryrun-prompt.md`.
- **Fremdkontrolle (Regel 12) vor dem Lauf:** `orglab/fremdkontrolle.py`, `openai/gpt-6.1-sol` (`effort: high`), je Beleg einzeln. Geschichtet sind es 36 Belege, Kosten unter 1 $. Neo klärt die Abweichungen.
- Wartet auf Neos Go für Fremdkontrolle und Lauf.

**~08:00 – Generator v4 gebaut (D-018 Punkt 1), noch nicht mit Modellen geprüft.**
- `orglab/evidence_v4.py` ist ein eigenes Modul. v3.1 bleibt Byte für Byte gleich (Hash-Test), weil E-021 und E-022 darauf präregistriert sind.
- **7 spec-reine Fehlerarten:** `low_traffic`, `cache_partial`, `wrong_contact`, `attachment_missing`, `weights_misscaled`, `duplicates_partial`, `column_loss`.
  - Ohne Norm sehen sie plausibel aus, die Normen sind je Vorgang verschieden.
  - Bei Rechnungen bekommen 60 % der Ok-Kunden gar kein PDF (Portal), damit "kein PDF" ohne Norm nichts verrät.
- Runbook abschnittsweise, unbekanntes Topic liefert "No entry". Fehlerarten balanciert und mit dem Kanal gekreuzt. 84 statt ~36 spec-reine kaputte Belege bei 24 Seeds.
- **Lecktest im Code** (`tests/test_evidence_v4.py`, Suite 223/223 grün):
  - Der Test hat im ersten Entwurf zwei echte Lecks gefunden: Eine Schwelle auf der Rohzahl trennte `low_traffic` zu 84 % und `duplicates_partial` zu 81 %. Nach breiteren Normverteilungen sind es 71 % und 64 %, alle anderen ≤ 73 %.
  - Ebenfalls gefunden und behoben, diesmal im Test selbst: Die erste Fassung maß einfache statt balancierte Trefferquote (480 Ok gegen 120 Fehler), damit wäre "immer ok" schon bei 80 % gelandet.
- `orglab/fremdkontrolle.py` kann jetzt auch **Lecktests durch GPT**: Kurzauftrag ohne Runbook, Kriterium ≤ 25 % je spec-reiner Fehlerart sicher erkannt.
- `experimente/E-020…/prereg-v3-entwurf.md`:
  - Stand und Reihenfolge bis zum Hauptlauf
  - Vorschlag, den REASONING-Faktor zu streichen (E-022 übernimmt die Frage), 8 statt 16 Zellen
  - noch fehlender Prüfer-Code (Runbook in beiden SPEC-Stufen, Anstupser weg, seedweiser Executor, eingefrorene Auswertung)
- **E-020 bleibt ausgesetzt.**
- Offene Schwäche: Ob ein *Modell* die spec-reinen Spuren ohne Norm erkennt, zeigt erst der GPT-Lecktest. Der Code-Test prüft nur Marker und Verteilungen.
- Kosten heute über OpenRouter bisher 0 $ (nur die kostenlose Modellliste abgefragt).
- Korrektur zum Eintrag direkt darüber: Die Uhrzeit "~08:00" war geschätzt. Laut `date` war es beim Schreiben 07:26 (Präregistrierungsvorlage: Uhrzeit aus `date`, nicht schätzen).

**~08:05 – Wave-Fälle: drei Kodierer statt Neo allein (D-019).**
- Neo wollte die Fälle zuerst selbst kodieren. Dafür gibt es einen Handy-Kodierbogen als privates Artifact (`notizen/28-wave-faelle/kodierbogen.html`), und der Speicher ist nur für Neo lesbar. Neo merkte dann, dass ihm 112 Einzelurteile nebenbei zu viel sind, und schlug drei Kodierer vor. Er selbst liest am Ende alle drei.
- **GPT** (`openai/gpt-6.1-sol`, `effort: high`, ein Aufruf, 0,13 $): bekam nur Fälle und Kodierbuch, ohne den Abschnitt "Herkunft", in dem die Hypothese steht. Skript `orglab/kodierung_fremd.py`, Ergebnis `03-kodierung-gpt.md`, Rohantwort `daten/wave-kodierung/gpt-roh.json`.
- **Ace:** neuer Thread [ID intern] statt des Update-Threads, weil dort die Hypothese ausdrücklich steht. Ace soll nur nach dem Text kodieren, Zusatzwissen kommt in Notizen. Nichts deployen.
- Noch nicht verglichen.

**~08:20 – Wave-Fälle: drei Kodierungen verglichen, Schlichtungsseite für Neo.**
- Ace hat kodiert (`04-kodierung-ace.md`), mit begründeten Hinweisen auf drei Schwächen des Kodierbuchs (K0-Grenze, K5 bei veralteten Signalen, K6 realität/mensch).
- `orglab/kodierung_vergleich.py` → `05-vergleich.md`: **53 von 112 Zellen strittig.**
  - Gut übereinstimmend: K0 (12/14 einig, κ 0,79–0,90) und K4 (fast alles `unbekannt`).
  - **K1 Sollwert und K3 Selbstauskunft liegen nahe Zufall** (κ 0,00–0,31). Die kurzen Falltexte tragen diese Fragen nicht.
  - Status: **Hinweis**, n = 14, selektierte Fälle.
- Die Seite `kodierbogen.html` ist dieselbe Artifact-URL, umgebaut zur Schlichtung. Neo entscheidet zuerst nur die 15 strittigen Zellen in K0, K2 und K5 (Tab "Wichtig"), der Rest ist optional. Die Entscheidungen liegen privat im Artifact-Speicher (`schlichtung/neo`).
- Methodische Folge (D-019): Neo ist jetzt Schlichter, kein unabhängiger Kodierer mehr. Das ist schwächer als geplant und offen benannt.

**~08:25 – Wave-Fälle: Neo hat geschlichtet (D-019).**
- Neo hat alle 15 wichtigen strittigen Zellen (K0, K2, K5) entschieden und schätzt die eigenen Entscheidungen als **nicht sicher** ein. Rohdaten: `daten/wave-kodierung/neo-schlichtung.json`. Endstand: `notizen/28-wave-faelle/06-endstand.md` (`python -m orglab.kodierung_vergleich ergebnis`).
- **Deskriptiv, Status Hinweis:**
  - übersehen 5, fehlalarm 4, kein_prüffehler 4, fehldiagnose 1
  - Bei den 5 Übersehen-Fällen hätte der Prüfer den Beleg in 4 Fällen selbst holen müssen, 3 zeigen den Spurtyp "grün, Zahl widerspricht".
  - Bei den 4 Fehlalarmen: Beleg 3 × selbst holen, Spurtyp 0 ×.
- Einordnung: Das passt zur Vermutung, dass ZUGANG (E-020) in der Praxis ein Engpass ist. Mehr als ein Hinweis ist es nicht: 14 selektierte Fälle aus Aces Gedächtnis, Schlichtung unsicher, zwei der drei Kodierer gleiche Familie. K1 (Sollwert) ist aus diesen Texten nicht kodierbar (κ ≈ 0), deshalb sagen die Fälle nichts über SPEC.
- Nächster sinnvoller Schritt: Aces unselektierte Stichprobe (18 Bridge-Austausche) blind kodieren, dann die FM-Labels als Vergleich anfragen (D-018 Punkt 4). Erst dann ist es mehr als eine Anekdotensammlung.

**~08:30–09:30 – GPT-Prüfungen des Materials (Regel 12 und 17), Generator v4.1.**
- Neo hat die Prüfungen freigegeben ("brauchst eh nicht so angst ums budget haben"). Gedächtnisnotiz: keine Rückfragen wegen kleiner API-Kosten, Experimentfreigaben bleiben bei Neo.
- **E-022 (v3.1), Fremdkontrolle:**
  - 33 von 36 stimmen überein, 3 sind "nicht entscheidbar": `bounced` nach 71 h Warteschlange, zweimal Prüferstrenge bei Research-Ok-Belegen.
  - Claudes Einschätzung: kein Generatorfehler. Neo soll das bestätigen.
- **v4.0:**
  - GPT fand **3 Generatorfehler**: Die Rescale-Zeile widersprach dem Auftrag "only", bei Portal-Rechnungen hing trotz "no attachment" ein Logo an, und `low_traffic` war auch mit Norm mehrdeutig.
  - Dazu **ein Konventionsleck**: "Rechnung ohne PDF" wirkt auch ohne Norm verdächtig.
  - Die 100 % Treffer ohne Norm bei Research waren Folge des ersten Fehlers, kein Leck.
  - Archiviert als `*-v4.0.*`.
- **v4.1** (d66fe71):
  - Research-Auftrag nennt die Neukalibrierung
  - `wrong_terms` ersetzt `attachment_missing`
  - Last "steady around the clock"
  - Ergebnis: **Lecktest 0 von 42, Fremdkontrolle 47 von 48** (ein Grenzfall bei sehr kleiner Last)
- Details in `notizen/29-gpt-pruefungen-material.md`. Lehre: Der Code-Lecktest sieht weder Widersprüche zum Auftragstext noch Weltwissen-Konventionen. Dafür braucht es die Modellprüfung, und es braucht beide.
- Kosten heute über OpenRouter ~1,5 $.

**08:50–09:40 – E-022 gelaufen: Kontrast repliziert, Dosis-Stufe fehlt, H-037 formal nicht bestätigt.**
- 288 Aufrufe, 0 fehlende Urteile, 24 von 24 Stapeln vollständig, 6,18 $. Ausgewertet mit dem eingefrorenen Skript.
- **Manipulationscheck gescheitert:** `effort: medium` verhält sich bei Sonnet 5.5 über OpenRouter wie `low`. Alle 144 Aufrufe liegen bei 244–257 Tokens, und das JSON allein braucht ~240, also wird faktisch nicht gedacht. `high` und ohne Parameter liegen bei ~900 Tokens und sind gleich.
- P1 Δ FA (low − high) +0,044 [untere Grenze +0,025], erfüllt, aber unter der Relevanzgrenze. P2 erfüllt.
- **H-037 nach Präregistrierung nicht bestätigt, Status bleibt gestützt.**
- Unter der tatsächlichen Manipulation "Denken gedeckelt gegen frei": FA 0,067 gegen 0,023 (zweite Replikation auf frischen Seeds), Übersehen nicht schlechter, PPV bei 5 % 0,42 gegen 0,68. "Ohne Parameter" = `high` (Δ 0,000).
- Lehre: Zum zweiten Mal tut eine API-Einstellung nicht, was ihr Name sagt (E-021: "aus", jetzt `medium`). Der Manipulationscheck als harte Bedingung hat eine Scheinbestätigung verhindert.
- Ergebnis in `experimente/E-022-reasoning-dosis/ergebnis.md`, Transkripte in `transkripte.md` (Pflichtlektüre für Neo).
- OpenRouter heute insgesamt 11,25 $.

**~09:20 – Reflexionsprotokoll (`notizen/30`) und Parkplatz.**
- Neos Gedanken nach E-022:
  - Lesart 1: "Bug in der Matrix"
  - Lesart 2: schleichende Konvergenz, Claude neigt Deutungen in Richtung der gewünschten Ergebnisse
  - Fragen nach Fehlerkorrelation innerhalb und zwischen Modellfamilien und nach Dekorrelation
  - Zusatz: "wie man AI research von AI machen lassen kann"
- Konkreter Hinweis für Lesart 2 aus den Daten (Status Hinweis, n = 14, ein Kodierer): In der Wave-Kodierung wich Claude bei K1 (6× "nein", GPT und Ace 0×) und K5 (6× "ja", GPT und Ace je 4×) einseitig in Richtung der eigenen Hypothesen ab. Neo hat beide K5-Streitfälle gegen Claude geschlichtet.
- `notizen/30`: vorausschauendes Fehlerprotokoll, Kategorien und Auswertung vorab festgelegt.
  - Die Richtung pro/contra These kodiert blind GPT oder Neo, nicht Claude.
  - Vorhersage für Lesart 2: pro gegen contra mindestens 2:1 bei mindestens 10 gerichteten Einträgen. Auswertung nach 20 Einträgen, spätestens am 23.11.
  - 13 rückblickende Einträge von heute zählen nicht. Erste Beobachtung: Kein inhaltlicher Fehler wurde von Claude selbst gefunden.
- Parkplatz: Korrelationsfragen inklusive n_eff-Formel und Many-Facet-Rasch, "Bug in der Matrix". Die Ground-Truth-Fremdkontrolle ist als erledigt markiert.

**~09:45–10:30 – Regelkritik-Panel (`notizen/31`), explorativ.**
- Neo: "frag von mir aus 20 verschiedene Modelle".
- Vorgehen vor dem Lauf committet (168bed3):
  - 17 Fremdmodelle aus 15 Familien und 3 Claude-Modelle
  - nur CLAUDE.md, nicht `notizen/30` (würde lenken)
  - neutrale Frage nach strukturellen blinden Flecken
  - anonymes Bündeln durch Gemini
- Abweichungen: Amazon Nova ist abgekündigt. Vier Modelle hatten ihr Denkbudget von 8.000 Tokens aufgebraucht und wurden mit 32.000 wiederholt. 19 Modelle, 105 blinde Flecken, 14 Themen, 1,03 $.
- Ergebnis:
  - Meistgenannt: **ungeprüfte Auswerte-Pipeline (10 von 16 Fremdmodellen, 0 von 3 Claude)**, selektive Berichterstattung (10), künstliche Aufgabenwelt (9), Anbieter-Drift (9), korrelierte Blindheit der Kontrollen (8), HARKing (7, 0 Claude).
  - Überlappung innerhalb Claude gleich groß wie zwischen den Familien (Jaccard 0,22–0,23).
  - Die Claude-Lücke beim Pipeline-Thema ist nachträglich bemerkt und gilt nur als Hinweis.
- Claudes Einordnung (befangen) steht als Tabelle in `notizen/31`. Fast alles ist berechtigt, HARKing ist bei H-037 sogar tatsächlich passiert. Empfehlung: **doppelte Buchführung**, also ein Fremdmodell rechnet die Kernmetrik nur aus der Präregistrierung neu. Neo entscheidet, was Regel wird.

**~10:40–11:00 – Doppelte Buchführung für E-022 (Empfehlung aus `notizen/31`, Neo: "Ja versuch es").**
- GPT-6.1 Sol und Gemini 4 Argon haben die Auswertung nur aus Präregistrierung und Datenproben neu implementiert (`orglab/nachrechnung.py`). Claude hat den Fremdcode vor dem Ausführen gelesen, ausgeführt wurde er isoliert. 0,09 $.
- **Alle drei Implementierungen kommen auf dieselben Zahlen** (P1 +0,04398, untere Grenze +0,0255 bzw. +0,0256, Manipulationscheck nicht bestanden, H-037 nicht bestätigt).
- **Gefunden:** Claudes eingefrorenes Skript setzt die präregistrierte Regel "unter 16 vollständigen Stapeln nur deskriptiv" nicht um. Hier folgenlos, als erster vorausschauender Eintrag in `notizen/30`.
- Die Fremdmodelle haben offene Forscher-Freiheitsgrade gelistet: Bootstrap-Startwert und Quantilmethode, Wiederholungen, fehlende Urteile, Gewichtung. Vorschlag an Neo: als Pflichtfelder in die Präregistrierungs-Vorlage aufnehmen.
- Neos Frage zum unendlichen Regress im Chat beantwortet. Mit unabhängigen Ebenen läuft der Restfehler gegen 0 (von Neumann 1956, Threshold-Theorem, nur aus Trainingswissen). Mit korrelierten Ebenen bleibt ein Boden, denn n_eff geht gegen 1/ρ. Die Ingenieursaufgabe ist deshalb, die Korrelation ρ zu senken, nicht mehr Ebenen zu bauen. Status: These, Literatur nicht im Original geprüft.

**~11:10 – D-020: Regel 19 (doppelte Buchführung) und neue Pflichtfelder in der Präregistrierungs-Vorlage.**
- Auf Neos "Ja":
  - CLAUDE.md Regel 19 und Checkliste ergänzt
  - Vorlage: Abschnitt "Teststärke" sowie Pflichtfeld "Analyse-Freiheitsgrade" (Bootstrap-Startwert und Quantilmethode, Wiederholungen, fehlende Urteile, Gewichtung, Mindestumfang, Ausfälle je Arm) und Feld "Doppelte Buchführung"
- Weitere Panel-Themen bleiben offen und stehen in D-020 als "nicht übernommen".

**~11:30 – Zoom-out-Gespräch, Designnotiz `notizen/32` (Meta-Harness für autonome Forschung).**
- Neos Gedanken: Es gibt mehrere Hebel. Vielfalt ist Pflicht, dazu ein Meta-Harness, der Werkzeuge je nach Phase und Zahlen freigibt, und der Grat zwischen starr/sicher und dynamisch/unsicher. Der Meta-Harness soll ein Multi-Agent-System mit strenger Kapselung sein, und die Gate-Zahlen dürfen nicht von der forschenden KI kommen.
- Claudes Bewertung:
  - Vor allem Vielfalt der Prüffunktion, Modellvielfalt verstärkt sie nur.
  - Ein Regler pro Phase statt eines globalen.
  - **Korrektur:** MAST nennt geteilten Kontext nicht als Fehlermodus, eher zu wenig Teilen (`notizen/19`). Kapselung passt für Prüf- und Rechenrollen, nicht für Koordination.
  - Gate-Zahlen: deterministisch, verblindet und doppelt implementiert vor "nur rechnendem" Modell vor eigens trainiertem Modell.
  - Erster billiger Baustein: verblindete Auswertung (Arme A/B/C/D).
- Status: Ideen und Thesen.

**~11:50 – D-021: verblindete Auswertung als Regel 20 (`orglab/verblindung.py`, 4 Tests, Suite 228/228).**
- Schlüssel liegt außerhalb des Repos, im Repo steht nur der Hash. Felder, die den Arm verraten, werden entfernt. Entblinden geht erst, wenn `auswertung-verblindet.md` committet ist.
- Neos Frage "wofür braucht das einen Menschen?" deckte einen Denkfehler in Claudes Vorschlag "Neo würfelt" auf (Protokolleintrag in `notizen/30`). Neo: Rechtetrennung ist softwaretechnisch lösbar. Die Sandbox-Prüfung folgt als zweiter Schritt.
- Gespräch über Kryptographie (Commitment, Secret Sharing, Hash-Kette, Brücke zu AAP) und Specification Gaming als Nachtrag in `notizen/32`.

**~12:00 – Sandbox-Prüfung (D-021, Schritt 2).** Claude Code hat eine vom Betriebssystem durchgesetzte Lesesperre (`sandbox.filesystem.denyRead`), aber **nicht auf nativem Windows** (laut Doku laufen Befehle dort ohne Sandbox). Die Datei-Werkzeuge brauchen zusätzlich `permissions.deny`. Optionen in `notizen/32` §8: WSL2 (dicht), externer Schlüssel per GitHub-Secret oder Ace-Dienst, oder Teilsperre per Read-Deny-Regel. Keine Einstellung geändert, das entscheidet Neo.

**~12:10 – Teilsperre für den Blindschlüssel (D-021).** Deny-Regel `Read(~/.orglab-schluessel/**)` in `.claude/settings.json` (Repo und Workspace). Mit Probedatei getestet: Das Read-Werkzeug wird verweigert, die Shell bleibt offen (keine Sandbox auf nativem Windows). Probedatei gelöscht.

**~12:30 – Anfrage an Ace: Monolith und Commitment-Watcher (Thread [ID intern], Kopie `berichte/2026-10-23-anfrage-ace-monolith-watcher.md`).**
- Anlass: Neos Engineering-Intuitionen (alles roh loggen, Analysewerkzeuge, Problemzerlegung als "Monolith") waren bisher nur nach "fühlt sich besser an" bewertet. Neo warnt: Ace ist wahrscheinlich gedriftet. Für einen Coding-Agenten ist Spezialisierung sinnvoll, für die Forschung ein Bug. Sein Wissen ist außerdem zu groß für eine Antwort aus dem Kontext.
- Frage-Design dagegen:
  - neuer Thread, keine Hypothesen von uns
  - erst suchen (Code, Git, Schema, Doku), dann antworten
  - jede Aussage als [Quelle], [Erinnerung] oder [Einschätzung] gekennzeichnet
  - Fakten getrennt von der Bewertung, die Bewertung mit Pflicht zu Gegenbelegen
  - nur Strukturen, keine Inhalte, nichts ändern
- Bezug: Gedächtnis als gemeinsamer Fehlerpfad (`notizen/18`).

**~12:45 – Aces Antwort zu Monolith und Commitment-Watcher (`notizen/33`, Vollfassung nur lokal).**
- Monolith: Opt-in-Autonomiemodus. Die Begründung im Masterplan vom 10.08. ist genau Neos Zerlegungs-Intuition ("Zerlegungstiefe als Optimierungsproblem"). Nur 5 Runs (12.–15.08.), Nutzen nie gemessen.
- Commitment-Watcher: 100 erfasste Zusagen, **keine einzige als erledigt markiert**, Pings erzeugten Spam. Laut Ace "besser sichtbar", ein Erfolg ist nicht belegt. Ace hat selbst Gegenerklärungen genannt (Regression zur Mitte, Messeffekt, keine Kontrollgruppe).
- Lehre (Hinweis): Rohdaten allein reichen nicht. Observability braucht ein Ergebnis-Label am Ende der Schleife.
- Parkplatz: Zerlegungs-U-Kurve und Lichttest/Fault Injection mit Ereignis-Log ergänzt.

**~13:00 – H-038 ins Register (Neo: "Ja").** These: Oberhalb einer Fähigkeitsschwelle erklärt das Harness mehr von der Verlässlichkeit als der Wechsel zwischen starken Modellen, unterhalb ist es umgekehrt. Bisher gibt es nur Hinweise bei festem Modell. Ein gemeinsamer Test von Modell und Harness fehlt. Neo zu Monolith: Die Benchmarks waren Funktionstests ("Software zusammenbauen lassen"), vermutlich mit methodischen Schwächen und womöglich unterhalb der Fähigkeitsschwelle.

**~13:20 – Monolith-Bruchstellen (Kodierbuch vorab d21f277, Ace kodiert, `notizen/33` Nachtrag).** 4 Läufe, vermutlich Sonnet 5, 24 Bruchstellen: Infrastruktur 9, Spezifikation 4, Zusammenführung 2, Teilaufgabe 2, Rest gemischt oder klein. Der teuerste Bruch war ein Zusammenführungsfehler, der bis in die Produktion kam (Neo bemerkte ihn live). Spezifikationsfehler fing ein Kritik-Pass billig vor dem Dispatch ab. Die Fähigkeitsfrage (H-038) lässt sich nicht beantworten, weil der Koordinator die Worker-Ergebnisse nachbesserte. Aces Summenzeile war falsch (14 statt 24), von Claude nachgezählt, Eintrag in `notizen/30`. Status: Hinweis, n = 4, Selbstkodierung.

**~13:35 – `notizen/32` §9 und §10: Ehrlichkeit und Korrigierbarkeit als Kernwerte für Autoresearch, dazu Neos Frage "ehrlich, aber falsch, aus welcher Quelle?".** Vorgeschlagene Einteilung nach Fehlerquelle (Zufall, Informationsmangel, Kontext-Bias, Modell-Bias, Spezifikationslücke), jede entkoppelt durch eine andere Plattenart. Die Fehler vom 23.10. passen rückblickend dazu, das ist aber nur ein Hinweis (nachträglich von Claude zugeordnet). Vorschlag: neues Feld "Fehlerquelle" im Protokoll, blind kodiert.

**~13:45 – Fehlerprotokoll Version 2 (Neo: "Gute idee").** Neues Feld Fehlerquelle (Z/I/K/M/S/U) in eigener Tabelle, blind kodiert (GPT oder Neo). Zusätzliche, widerlegbare Vorhersage: Fehler findet überwiegend die zur Quelle passende Plattenart, bei mindestens 10 blinden Einträgen.

**~14:10 – Blinde Kodierung des Fehlerprotokolls (GPT) und Ace-Update 3 versendet (`berichte/2026-10-23-update-3-ace.md`).** GPT stimmt bei 2 von 3 Fehlerquellen mit Claude überein. Beim Verblindungs-Vorschlag kodiert GPT "Kontext-Bias, pro These", wo Claude "Informationsmangel, neutral" eingeschätzt hatte. Ein kleines Beispiel dafür, dass Claude die eigene Befangenheit unterschätzt (n = 1).

**12:25 (aus `date`) – Korrektur zu den Einträgen seit etwa 11:50:** Die Uhrzeiten von "~12:10" bis "~14:10" waren **geschätzt und zu spät**, um bis zu etwa 2 Stunden. Laut `date` war es beim Dry-Run 12:24, die Einträge "~12:30" bis "~14:10" fallen tatsächlich in etwa 11:15–12:20. Auch D-021 ("~11:50") und D-022 ("~14:00") tragen geschätzte Zeiten. Ab jetzt stehen Uhrzeiten nur noch aus `date` im Laborbuch. Eintrag im Fehlerprotokoll.

**12:25 – E-020 v3 gebaut, Präregistrierung Fassung 3 als Entwurf (nicht gestartet).**
- `orglab/e020v3.py`:
  - 8 Zellen, Runbook-Werkzeug in allen Zellen, keine Anstupser, kein `reasoning`-Parameter
  - seedweise Warteschlange, Kostenstopp 50 $
  - Auswertung nur über vollständige Seeds, unter 16 Seeds nur deskriptiv (Lehre aus E-022), Ausfälle je Zelle berichtet
- Tests `tests/test_e020v3.py` (8), Suite 236/236.
- Power per Simulation: V1 bei +0,10 etwa 1,0, bei +0,05 etwa 0,75. V2 bei +0,05 etwa 0,93.
- `dryrun-v3.md` mit allen 8 Prompts und den Werkzeugen. `prereg-v3.md` wartet auf Neos Freigabe, offen ist auch ein Ground-Truth-Grenzfall (6021). Danach Pilot (~2–3 $), Grok-Gutachten, Hauptlauf (~25–35 $).

**12:26 – Aces Antwort auf Update 3 (Thread [ID intern]).** Hat gelesen und gespeichert. Ace weiß nichts von den Antworten aus Thread [ID intern] (Monolith, Bruchstellen) und nichts von der Wave-Kodierung: **Jeder Ace-Thread ist eine eigene Instanz mit nur teilweise geteiltem Gedächtnis.** Für die Entkopplung heißt das (Hinweis): Verschiedene Ace-Threads sind keine einzige Stimme, ihr gemeinsamer Kontext ist aber auch nicht verlässlich. Ace bestätigt, dass dem Commitment-Watcher ein Erledigt-Label fehlt.

**12:40 – E-020 v3: Freigabe durch Neo ("Das passt so", 12:39), Sensitivitätsanalyse nachgerüstet.** Die Präregistrierung versprach eine Analyse ohne Grenzfall 6021, das Skript konnte sie nicht. Selbst gefunden vor jedem Lauf, behoben: Der Beleg wird erst nach der Vollständigkeitsprüfung entfernt, damit nicht sein ganzer Seed herausfällt. Test ergänzt, Suite 237/237. Eintrag im Fehlerprotokoll. Danach Pilot gestartet.

**12:46 – E-020 v3 Pilot: technisch erfüllt, aber Validitätsproblem gefunden (`pilot-v3-bericht.md`).** 192 Prüfungen, 0 Ausfälle, 3,25 $. Die Runbook-Suche erkennt keine Dienst- oder Datensatznamen. Unter SPEC=1 wurden 18 von 28 spec-reinen Fehlern übersehen, in allen 18 Fällen kam der richtige Abschnitt nicht zurück. SPEC mäße so auch "schlechte Suche". Vorschlag: seitenbasierte Suche, Entscheidung durch Neo, Grok-Gutachten danach. Hauptlauf nicht gestartet.

**13:05 – E-020 v3 Pilot 2 (seitenbasierte Suche): Kriterium erfüllt (28 von 28 Suchen liefern die Norm), 0 Ausfälle, 2,94 $.** Die Fehlerrate unter SPEC=1 fiel von 12–29 % auf 4–8 %. Der Pilot-1-Unterschied war also fast ganz Suchartefakt (Hinweis, n = 24). Erwartung für den Hauptlauf: eher kleiner SPEC-Effekt, die Präregistrierung bleibt unverändert. Nächster Schritt: Grok-Gutachten.

**13:18 – Grok-Gutachten 3 zu E-020 v3 (`notizen/23c`).** Hauptpunkte: Die seitenbasierte Suche liefert die Norm als beschrifteten Einzeiler und wird so zum Antwortschlüssel, V1 misst die Decke. Entscheidungsregel, Power-Angabe und Skript widersprechen sich (Claudes Fehler). Der Normtext ist ungleich zwischen Auftrag und Runbook (Konfundierung). Dazu `low_traffic`-Bauart, V4-Feld, Wortgrenzen und das fehlende Transkript-Lesen. Empfehlung: erst ändern, dann Pilot auf frischen Seeds, dann Hauptlauf mit Schwelle +0,10. Hauptlauf nicht gestartet, die Entscheidung liegt bei Neo.

**13:39 – E-020 v3: Material v4.3 geprüft, Pilot 3 technisch erfüllt, Hauptlauf bereit (wartet auf Neo).** Grok-Punkte umgesetzt (Abweichung 2, Neo: "Ja mach das"). GPT fand in v4.2 noch zwei Fehler (Instanz-Mehrdeutigkeit, doppelte fd), daraus wurde v4.3. Auf den Hauptlauf-Seeds: Fremdkontrolle 48/48, GPT-Lecktest 0/42. Pilot 3 auf frischen Seeds 1400–1401: 192 Prüfungen, 0 Ausfälle, 2,87 $, Werkzeuge genutzt, 5 Transkripte gelesen. Die Fehlerraten aller Piloten bleiben versiegelt. Heute bisher 23,16 $ über OpenRouter. Hauptlauf (2.304 Prüfungen, ~25–35 $, Stopp bei 50 $) nicht gestartet.

**14:18 – Grok-Nachgutachten (`notizen/23d`), Abweichung 3, Hauptlauf E-020 v3 gestartet.** Neo wollte das Nachgutachten und hat den Start freigegeben ("kannst starten"), die Tagesgrenze für OpenRouter liegt bei 90 (für diesen Prozess `OPENROUTER_DAILY_BUDGET_USD=90`, Kostenstopp des Experiments weiter 50 $). Grok: Die Punkte aus Gutachten 3 sind behoben oder teilweise behoben, **Empfehlung "Hauptlauf jetzt starten"**. Vor dem Start als Abweichung 3 festgehalten: V1 misst "Norm im Auftrag" gegen "Norm oben auf der Seite", "widerlegt" heißt nur "Vorhersagewert ausgeschlossen", V4 misst "Seite zurück" statt "Normwert gelesen" (mein Fehler, der Normwert kommt explorativ aus den Transkripten). Hauptlauf: Seeds 6000–6023, 2.304 Prüfungen, Commit 215b4e0.

**15:20 – E-020 v3 Hauptlauf ausgewertet (`experimente/E-020-realitaet-in-dosen/ergebnis.md`).** 2.304 Prüfungen, 24/24 Seeds, 0 Ausfälle, 34,00 $ (14:18–15:09). **Keine der drei Vorhersagen trifft ein (Entdeckung):**
- V1 SPEC +0,006 [+0,000; +0,018]: Auffindbarer Sollwert ist so gut wie mitgelieferter.
- V2 Selbstauskunft −0,016 [−0,033; −0,002]: leicht entgegengesetzt, nur aus `db_down`, Hinweis.
- V3: Decke, immer 3 von 3 Kanälen abgefragt.
- Fehlalarme 0 überall.

Doppelte Buchführung (freiwillig): GPT und Gemini kommen aus der Präregistrierung auf dieselben Zahlen. Die gemeldeten offenen Entscheidungen stehen im Ergebnis (Bootstrap-Startwerte je Kontrast, p-Wert für BH, Rangfolge der Etiketten).

**Wichtigster Fund ist ein Materialfehler, den unsere Prüfkette nicht fangen konnte:** `db_down` im Deploy-Kanal und `low_traffic` im Sockets-Kanal sind einzeln nicht entscheidbar (je 16/16 übersehen, 8 Belege = 2,8 %). Fremdkontrolle und Lecktest zeigten GPT immer alle drei Kanäle. Die primären Kontraste ändern sich ohne diese Belege nicht. Der ZUGANG-Vorteil schrumpft aber von −0,082 auf −0,031. **Vorschlag an Neo** (Regel-Stopp ist mit E-020 aufgehoben): Regel 12 um eine Fremdkontrolle je einzeln vorgelegtem Kanal erweitern, wenn das Design Einzelkanäle vorlegt.

Hypothesen H-033, H-034, H-035 auf "nicht gestützt (E-020, Entdeckung)" gesetzt, mit Evidenz. `orglab/nachrechnung.py` kann jetzt auch E-020 (Präregistrierung samt Abweichungen). Transkripte: `transkripte.md` (2 je Zelle).

**15:17 – Korrektur zum Eintrag "15:20":** Der Eintrag wurde laut `date` um 15:16 geschrieben, die Zeit "15:20" im Titel war geschätzt (gegen die eigene Regel, nur `date` zu verwenden).

**15:45 – Gespräch zum E-020-Ergebnis und E-023 (Haiku) vorbereitet.** Mit Neo besprochen, was E-020 heißt (Status: Hinweis). Rahmungs-Hebel wirken bei Sonnet nicht, die Informationsarchitektur schon. "Andere Fenster statt mehr Augen": Prüfer mit anderer Information dekorrelieren, Prüfer mit gleicher Information nicht. Unsere eigene Prüfkette hatte genau diesen blinden Fleck. Neo: "machen wir Haiku trotzdem zuerst, aber ordnen es richtig ein".
- Manipulationscheck-Probe (24 Aufrufe, Seed 1500): Haiku 5.5 denkt ohne Parameter adaptiv (Median ~460 Denk-Tokens gegen ~200 bei Sonnet), bedient die Werkzeuge (12/12 Urteile, run_check 3/3), schlägt bei SPEC=1 aber nur 3 von 6 Mal nach (Sonnet 6/6).
- `orglab/e023.py` (gleiches Design, nur das Modell wechselt, Wechselwirkung gepaart je Beleg), 5 Tests, Suite 335/335. Trockenlauf Sonnet gegen Sonnet ergibt genau 0.
- `experimente/E-023-haiku-dosen/prereg.md` als Entwurf mit Einordnungstabelle: welcher Ausgang welche Lesart erlaubt. Power für W1 bei +0,10: 0,93, bei +0,05: 0,33. Wartet auf Neos Freigabe, nichts gestartet.

**16:59 – E-023 (Haiku 5.5, Design E-020 v3) gelaufen und ausgewertet (`experimente/E-023-haiku-dosen/ergebnis.md`).**
- Lauf: Freigabe 16:04, Pilot erfüllt, Hauptlauf 2.304 Prüfungen, 2,18 $. 1 Timeout, deshalb 23 von 24 Seeds (Regel).
- **V1 gestützt:** SPEC +0,253 [+0,202; +0,304], bei Sonnet +0,006.
- **W1 (H-038) gestützt:** Wechselwirkung +0,247 [+0,193; +0,298]. Ob der Sollwert im Auftrag steht, ist für Haiku wichtig, für Sonnet nicht.
- Mechanismus: Norm nicht erhalten → 96 % übersehen.
- **Explorativ, wichtigster Hinweis:** Bekommt Haiku Kanal-Werkzeuge, schlägt es im Runbook seltener nach (99 % → 54 %). Die Werkzeuge verdrängen den Maßstab. Das relativiert den "selbst holen"-Gedanken aus dem Gespräch.
- Selbstauskunft erhöht bei Haiku die Fehlalarme (+0,04) statt die Übersehen. Mögliche Materialfrage: Rauschen gegen "single instance" (v4.3).
- Doppelte Buchführung: GPT und Gemini identisch.
- **Eigener Fehler:** Das E-023-Skript rechnet die versprochene 6021-Sensitivitätsanalyse nicht. Nachgerechnet, dokumentiert, ohne Auswirkung.
- H-033 → modellabhängig, H-034 ergänzt, H-038 → gestützt für einen Faktor.

**18:59 – E-024 (Bestätigung) vorbereitet.** Mit Neo besprochen: In Wave läuft alles auf Sonnet. Haiku ist deshalb ein Modell dafür, *wie* ein Prüfer scheitert, keine Wave-Regel. Die explorativen E-023-Befunde dürfen als vorab festgelegte Vorhersagen in einen Bestätigungslauf (Neo: "Yes").
- `orglab/e024.py`: beide Modelle, frische Seeds 7000–7023, fünf Vorhersagen (V1, W1, C1/C2 Verdrängung, F1 Fehlalarme), BH über alle fünf, verblindete Auswertung mit beiden Zuordnungen.
- 6 Tests, Suite 341/341. Rauchtest auf Entdeckungsdaten reproduziert E-023.
- Power bei halbierten Effekten: V1/W1/C1 1,0, C2 0,8, F1 0,4 (F1 schwach, offen benannt).
- Neu: Fremdkontrolle je Einzelkanal (`fremdkontrolle.py --einzelkanal`, alle 288 Belege) als Lehre aus E-020. Läuft gerade.
- H-039 (Verdrängung) und H-040 (Misstrauen) eingetragen.
- `experimente/E-024-bestaetigung-massstab/prereg.md` als Entwurf. Es fehlen noch Materialergebnisse, Grok-Gutachten und Neos Freigabe.

**19:06 – E-024 Materialprüfung auf den Seeds 7000–7023: Start gestoppt (eigene Grenze überschritten), Entscheidung Neo.**
- Fremdkontrolle 47/48. Abweichung `coding-ok_clear-7009`: Zähler über die Laufzeit ergibt 113/min gegen Normband 120–180, echte Mehrdeutigkeit.
- Lecktest 0/42.
- **Einzelkanal-Fremdkontrolle (neu): 62 von 288 Belegen einzeln nicht entscheidbar (21,5 %, Grenze 10 %).**
  - Der Großteil sind Ok-Belege (43/144): Ein einzelner Kanal kann den Erfolg nicht belegen, nur einen Fehler zeigen.
  - Spec-rein nur 7/84.
- Folgen:
  - V1, W1, C1, C2 kaum betroffen.
  - F1 (Fehlalarme) stark betroffen: Ein "kaputt" für unbelegbaren Erfolg ist kein klarer Fehlalarm.
  - Neue Lesart für E-020 (Hinweis): Sonnets 0 Fehlalarme mit einem Kanal heißen auch, dass Sonnet Unbelegtes bestätigt hat. Unsere Metrik trennt berechtigtes nicht von glücklichem Vertrauen, weil das Urteil binär ist.
- Kosten der Prüfungen 1,75 $.

**19:41 – E-024: Pilot erfüllt, Grok-Gutachten 5 (`notizen/23e`) umgesetzt, Hauptlauf startet.**
- Neo: "die 36 € investieren wir heut noch" und fragte nach meiner Empfehlung. Umgesetzt wurde Variante A: Material unverändert, F1 nur auf einzeln entscheidbaren Ok-Belegen, Grenzfall 7009. H-041 (glückliches Vertrauen) eingetragen. Neo kennt das Muster aus Wave.
- Pilot (384 Prüfungen, 3,02 $): 0 Ausfälle, run_check 3,0, Probe-Verblindung funktioniert.
- **Grok fand einen echten Fehler:** Die Etiketten im Skript hätten "nachgewiesen, aber kleiner" als "widerlegt" ausgegeben, gegen die Präregistrierung, und das vor dem Entblinden festgeschrieben. Behoben mit eigener Funktion `e024.label`. Dazu:
  - Abbruch ohne Ausschlussdatei
  - Manipulationscheck in der verblindeten Auswertung
  - C1-Sekundäranalyse ohne Ausschluss
  - Diagnose ZUGANG bei SPEC = 0
  - Power F1 0,3
- Beim Testen fiel auf: Der synthetische "Null"-Test war keine echte Null (Nicht-Nachschlagen erzeugte selbst einen V1-Effekt). Behoben, die Kalibrierung ist jetzt über 10 Null-Datensätze geprüft. Suite 346/346.

**21:26 – E-024 (Bestätigung) gelaufen, verblindet ausgewertet, entblindet, nachgerechnet: alle fünf Vorhersagen bestätigt (`experimente/E-024-bestaetigung-massstab/ergebnis.md`).**
- Lauf: 4.608 Prüfungen, 36,10 $, 21/24 Seeds vollständig. Manipulationscheck bestanden.
- Verblindet um 21:20, Entscheidungen committet (af3fb43), dann entblindet: A = Haiku.
- Ergebnisse für Haiku:
  - V1 +0,263
  - W1 +0,260
  - C1 +0,472
  - C2 +0,408
  - F1 +0,029
  - Alle BESTÄTIGT, so groß wie in der Entdeckung. Sonnet überall etwa 0.
- GPT und Gemini rechnen aus der Präregistrierung dieselben Zahlen und Etiketten nach.
- **Diagnose:** Mit Maßstab im Auftrag helfen die Kanal-Werkzeuge beiden Modellen. Der Schaden bei Haiku hängt am fehlenden Maßstab (Groks Alternativerklärung trifft zu). Haiku hört freiwillig auf (0/341 an der Rundengrenze).
- Hypothesen: H-033 (Haiku), H-038 (SPEC), H-039 (mit Präzisierung) und H-040 (klein, Deutung offen) auf bestätigt gesetzt.
- Kosten heute über OpenRouter: 101 $ (Neo: Budget heute ok, OpenRouter-Limit vorübergehend aufgehoben).
- Offen: das Vertrauens-Experiment (H-041), danach "Sonnet unter Last".

**22:44 – Recherche und dritter Prüfer (`notizen/34-dritter-pruefer/`).** Auf Neos Anregung: Prüfer mit frischem Kontext, getrennt vom Projekt.
- **Recherche**, Subagent in eigenem Ordner, sechs neutrale Fragen:
  - Morpheus' Repos haben keine Bewertungen, keine Wiederholungen und keine Harness-Konfiguration. Für uns nur bei eigener Bewertung brauchbar.
  - Ein konstanter Logit-Effekt erscheint in Prozentpunkten automatisch nahe der Fähigkeitsgrenze am größten.
  - Schwierigkeit aus denselben Daten zu schätzen erzeugt Regression zur Mitte.
  - Länge und Richtung des Kontexts werden in neueren Preprints getrennt.
- **Leck:** Der Recherche-Agent sah eine Zeile aus Claudes Gedächtnis-Index (Experiment-Kürzel und Status). Die Zeile ist jetzt neutralisiert.
- **Prüfer 3a (Claude frisch) und 3b (GPT)** mit Rohdaten-Kopien, neutraler Datenbeschreibung und von Neo gegengelesenen Fragen, ohne unsere Ergebnisse. Beide kommen unabhängig zum selben Kern:
  - Haikus Schwäche ist SP × ZU (auch auf der Logit-Skala).
  - Der fehlende Sollwert allein kostet Haiku nur −0,7 pp.
  - Sonnets Fehler hängen an uninformativen Einzelkanälen.
  - Die Selbstauskunft macht Haiku misstrauisch und senkt sein Nachschlagen.
  - **Neos Kompetenzgrenzen-These wird nicht gestützt.** Die Wirkung hängt an Fehlerart und Mechanismus. Ein naives Schwierigkeitsmuster wäre Regression zur Mitte gewesen (Nullsimulation).
  - Fehlerkorrelation: überwiegend geteilte Typ- und Kanalschwierigkeit (κ 0,22 → 0,13 nach Schichtung); ein perfekter Schiedsrichter brächte nur +1 pp über Sonnet.
- Korrigiert Claudes Lesart an drei Stellen: V1 ist eine Wechselwirkung, die Kompetenzgrenze ist nicht gestützt, das GPT-Einzelkanal-Label ist vermengt.
- Nachtrag in E-024 `ergebnis.md`, H-038 präzisiert.

**23:01 – Statuskorrektur (Regel 15).** Claude hatte die Lehren aus dem dritten Prüfer im Gespräch als "Was wir jetzt wissen" formuliert. Neo fragte: "kann man das einfach behaupten?" Nein. Fehlende Information als Hauptursache, "zweites Modell hilft kaum, andere Information viel" und "Formulierungen wirken nicht" sind Hinweise; der dritte Satz ist für Haiku sogar falsch ("All checks green" wirkt). Bestätigt ist nur der schmale Haiku-Befund aus E-024. Statustabelle in `notizen/34`, Nachtrag in E-024 `ergebnis.md`. Das ist das dritte Mal heute, dass Claude mehr behauptet als die Daten hergeben, jedes Mal von Neo mit frischem Blick korrigiert, passend zum Kontext-Drift-Gedanken.

**23:08 – D-023: Leitfrage festgelegt.** Beim Herauszoomen auf Neos Frage ("was siehst du in unseren Gedanken?"): Alle Fäden des Projekts sind dieselbe Frage auf vier Ebenen (Teams, Einzelprüfer, Wave, eigene Forschung). Leitfrage: **"Was macht ein 'verifiziert' gerechtfertigt, und wie muss man Information organisieren, damit es das ist?"** Neo: "verdammt richtig". Nach vorn kommen Kontext-Drift, glückliches Vertrauen, Maßstab und Prüfpfad-Diversität. Bewusst liegen bleiben Morpheus, Modellfamilien als Selbstzweck und IRT.

**23:24 – D-024: Programmvision festgehalten (`notizen/35-programmvision.md`).**
- Neo: Hinter der Multi-Agent-Frage steckt "wie automatisieren wir Research sicher bei beliebigen simulierbaren Dingen". Er selbst schließt als Laie den Kreislauf, deshalb ist die Leitfrage auch sein Vertrauensproblem. Lösung: Prozessvertrauen statt Inhaltsvertrauen.
- Festgehalten:
  - Forschung als MAS
  - Simulierbarkeit erlaubt gemessene Fangquoten
  - mögliche Engineering-Perspektive (Research-Harness als Meta-Harness oder MAS)
  - Observability als Messgrundlage: Lecks, gemeinsame blinde Flecken und steigende Status werden billig sichtbar
- Status: Vision, kein Befund. Vor jeder Neuheitsbehauptung kommt eine Recherche zu automatisierter Forschung.

## 2026-10-24

**23:10 – Zwei Kritiker-Einwände gegen die E-024-Präregistrierung geprüft (`notizen/36-kritiker-einwaende-e024.md`, explorativ).**
- **Anlass:** Im Lichttest v1 des research-harness meldete Gemini 4 Argon als Fremdkritiker in 18 von 48 sauberen Läufen etwas Blockierendes gegen `prereg.md`, meist dieselben zwei Punkte. Offen war, ob sie tragen.
- **Seed-Cluster (Regel 13):**
  - V1, W1, C1, C2 und F1 nachgerechnet, mit Cluster-Bootstrap über die 21 vollständigen Seeds statt über Belege. B = 5.000, Startwerte 241–245 und 251–255, Kontraste unverändert aus `e024.contrasts`.
  - **Alle fünf Etiketten bleiben BESTÄTIGT.** Die Intervalle werden schmaler (60–90 % der Breite).
  - Die ICC der Je-Beleg-Kontraste innerhalb eines Seeds ist überall negativ (−0,05 bis −0,12).
  - Grund: Jeder Seed enthält jede Kombination Domäne × Art genau einmal, und die Fehlerart wird reihum über den Seed vergeben. Ein Seed ist also eine kleine ausgewogene Schicht.
  - Ein geschichteter Belege-Bootstrap ist ebenfalls schmaler. Der präregistrierte Bootstrap über Belege ist damit der vorsichtigste der drei.
- **F1-Widerspruch:**
  - Wörtlich vorhanden. Z. 134 ("Primär: alle Belege") widerspricht den F1-Stellen Z. 42, 59, 97 und 110 (nur einzeln entscheidbare Ok-Belege).
  - Laut Git ist Z. 134 ein Überbleibsel aus dem Entwurf 2cd76b6 (18:59), der vor der F1-Einschränkung in 50c9698 (19:28) entstand.
  - GPT und Gemini haben in der Nachrechnung dieselbe Auslegung gewählt, GPT mit ausdrücklichem Vermerk.
  - F1 auf allen Ok-Belegen wäre ebenfalls bestätigt (+0,046). Ohne Folgen für das Ergebnis.
- **Nebenbefund:** Für F1 ist die Sekundäranalyse "ohne die 62" identisch mit der primären.
- **Status:** explorativ, keine neue Bestätigung. `ergebnis.md`, `prereg.md` und Rohdaten unverändert. Ob `ergebnis.md` einen kurzen Nachtrag bekommt, entscheidet Neo (Wortlaut-Vorschlag in `notizen/36`).
- Skript: `notizen/36-kritiker-einwaende-e024/seed_cluster.py`, Ausgabe daneben. Keine API-Kosten. Nicht committet.

**23:32 – Nachtrag zu E-024 `ergebnis.md` geschrieben (Neo freigegeben).** Neo, übermittelt von der Bauplan-Session: "Ja, die orglab-Session soll Notiz 36 und den Laborbuch-Eintrag committen und den vorgeschlagenen Nachtrag zu ergebnis.md schreiben." Der Nachtrag ist unten an `ergebnis.md` angehängt, als explorativ markiert, mit dem Wortlaut aus `notizen/36`. Bestehender Text blieb unverändert. Status unverändert.

**~00:15 (25.10.) – E-025 (H-041, "glückliches Vertrauen") vorbereitet, erstes Experiment durch den research-harness.** Neo hat vor dem Schlafengehen freigegeben: "H-041 als Entdeckung", Modelle "Sonnet und Haiku", Budget "egal, ich hab das geld". Für blockierende Gates gilt die Regel aus `prereg.md` (einmal nachbessern, dann stoppen; Fremdkontrolle-Abweichungen nach fester Regel, Neo prüft morgen). Entblinden erst nach Neos Freigabe.
- Design: Je Beleg zwei Darstellungen, VOLL (alle Kanäle, entscheidbar) und AUSZUG (ein Kanal ohne jede Zeile, in der eine Fehlerart Spuren hinterlässt, also per Konstruktion nicht belegend). Faktoren Evidenznorm × dritte Antwort "not established", Selbstauskunft immer dabei. Seeds 8000–8015, 3.072 Prüfungen.
- Neu: Ein Urteil zählt nur mit regulärem Antwortende und lesbarem JSON (Fehlerspur, Lehre aus dem Harness-Lichttest F-09 v2).
- `orglab/e025.py`, `tests/test_e025.py` (13 Tests, Suite 359/359), `experimente/E-025-glueckliches-vertrauen/prereg.md`, `dryrun.md`. Kritik (Gemini), Fremdkontrolle (GPT), Pilot und Hauptlauf steuert der Harness (`research-harness/laeufe/E-025/`).

**~00:45 (25.10.) – E-025-1 vom Fremdkritiker gestoppt, einmal nachgebessert (Regel der Nacht).** Der Harness hat den ersten Lauf an Gate KRITIK angehalten: Gemini fand vier blockierende Punkte (Seed-Ausschluss bei einem Ausfall, unklarer Manipulationscheck 3, vages "K0 nahe 0", Bedingungen nicht verblindet). Punkte 1–3 berechtigt und umgesetzt (Vollständigkeit je Beleg, Präzisierungen), Punkt 4 begründet abgelehnt; alles in `prereg.md` unter "Antworten auf die Kritik". Neuer Lauf E-025-2 mit erneuter Kritik. Blockiert der Kritiker wieder, startet kein Hauptlauf.

**~03:30 (25.10.) – E-025-3 durchgelaufen, vor dem Entblinden angehalten (Schlichtung durch Neo, P-003 im Harness).** Kritik ohne Blockierendes, Fremdkontrolle VOLL 45/48 (3 Abweichungen über der Schwelle, nicht ausgeschlossen, Neo prüft), AUSZUG 48/48 nicht entscheidbar, Pilot ohne Ausfälle, Hauptlauf 3.072 Prüfungen, max. Ausfall 0,5 % je Zelle, Fehlerspur vollständig, 18,59 $. Rechner A (e025) und B (GPT, neu geschrieben) stimmen in allen Zahlen überein (max. 0,003 an einer KI-Grenze), widersprechen sich aber im Etikett: B wertet Manipulationscheck 4 ("N und T: per Code-Test") fail-closed als nicht bestanden, weil er aus den Daten nicht prüfbar ist, und meldet alles deskriptiv. Nach der Regel der Nacht nicht entblindet. Verblindet (Status: Hinweis): Bestätigung auf dem Auszug Arm A 2 %, Arm B 23 %; nur ohne Norm und ohne dritte Antwort; "not established" 91 %/99 % wo erlaubt. Davor: E-025-1 vom Kritiker gestoppt (3 von 4 Punkten umgesetzt), E-025-2 an einem Executor-Fehler des Harness gescheitert (behoben). Morgenbericht: `research-harness/laeufe/E-025/morgen-2026-10-25.md`.

**~15:00 (25.10.) – E-025 ausgewertet und abgeschlossen (H-041 Kandidat, neue H-042).** Neo hat geschlichtet ("A gilt"), das Entblinden freigegeben ("Ja") und die Stichprobe gelesen ("finde alle passen"). Entblindet: A = Haiku, B = Sonnet. Ergebnis (`experimente/E-025-glueckliches-vertrauen/ergebnis.md`, Status Entdeckung): Sonnet bestätigt auf dem Auszug ohne Hilfe 23 % unbelegten Erfolg, Haiku 2 %; Evidenznorm oder dritte Antwort senken jeweils allein auf 0; R1/R2 "gestützt, aber kleiner als vorhergesagt"; Prämisse K0 ≥ 0,30 verfehlt (Vermerk). Explorativ: dritte Antwort kostet Haiku bei voller Evidenz Treffer; Sonnets Fehlbestätigungen hängen an der Domäne (Rechnungsversand 48 %). H-041 → Kandidat; H-042 neu (Fehlerbild statt Modellstärke). Rohdaten als Kopien der Harness-Artefakte in `daten/E-025-glueckliches-vertrauen/` (Hashes in `herkunft.md`). Lehren für den Harness: nicht nachrechenbare Checks getrennt führen (Neo), Fehlerbegriff der Stichprobe je Experiment, Interpretationsregeln maschinenlesbar, Minuten über den Chat asynchron wertlos.

**~16:00 (25.10.) – E-026 (Bestätigung von E-025) als Entwurf vorbereitet, wartet auf Neos Freigabe.** Neo zum Plan: "geht los". Gleiches Design, Material und gleiche Prompts wie E-025 (Test prüft Zeichengleichheit), frische Seeds 9000–9015 und Pilot 1702–1703. Vorhersagen bei etwa halben E-025-Werten: B1 Sonnet − Haiku Bestätigung im Auszug ≥ +0,08 (H-042), B2/B3 Sonnet Senkung durch Norm bzw. dritte Antwort ≥ +0,05 (H-041), B4 Haikus Trefferverlust durch die dritte Antwort bei voller Evidenz ≥ +0,08. Power bei halbierten Effekten 0,97–1,00. Neu aus der E-025-Schlichtung: Prompt-Flags aus dem gesendeten Text machen den N/T-Check für Rechner B nachrechenbar; nicht nachrechenbare Checks stehen getrennt als "bescheinigt". `orglab/e026.py`, `tests/test_e026.py` (Suite 365/365), `experimente/E-026-bestaetigung-vertrauen/prereg.md`, `dryrun.md`. Harness v1.2 (Ziel-Modus, Vermerke, Fehlerbegriff der Stichprobe) im research-harness.

**~16:15 (25.10.) – E-026-1 vom Kritiker gestoppt, einmal nachgebessert.** Gemini meldete fünf blockierende Punkte, diesmal zur Nachrechenbarkeit durch Rechner B (verbleibende Felder, Kodierung N/T, Definitionen, p-Wert) und zur Verblindung. Punkte 1–3 und 5 durch einen neuen Abschnitt "Daten und Definitionen" präzisiert (der Code rechnet unverändert so), Punkt 4 begründet abgelehnt wie in E-025. Neuer Lauf E-026-2; blockiert der Kritiker wieder, kein Hauptlauf.

**~17:30 (25.10.) – E-026 (Bestätigung von E-025) abgeschlossen: alle vier Vorhersagen BESTÄTIGT.** Harness-Lauf E-026-2 (E-026-1 vom Kritiker gestoppt, Präzisierungen zur Nachrechenbarkeit). Rechner A und B in allen Zahlen und Etiketten gleich; das Gate stoppte nur an der nicht präregistrierten Zahl "vollständige Seeds" (15 gegen 16), Neo schlichtete "A gilt". Entblindet nach Neos Ja: B1 Sonnet − Haiku Bestätigung im Auszug +0,225, B2/B3 Senkung bei Sonnet durch Norm +0,136 bzw. dritte Antwort +0,141, B4 Preis der dritten Antwort bei Haiku +0,230, alle q < 0,001, Effekte nicht geschrumpft. Außenanker: Neo ("Horizon"), geschichtete Ziehung mit Fehlerbegriff aus der Präregistrierung, Fall 3 zeigt den Befund im Wortlaut; "Gelesen, passt", 2,0 min. H-041 bestätigt für Sonnet 5.5 in diesem Aufbau, H-042 in beiden Teilen bestätigt (getrennte Aufbauten). Erster Befund mit Status "belegt" im Harness-Register. 18,74 $. Harness-Lehren: Gate vergleicht nur präregistrierte Entscheidungsgrößen, Schlichtung hält nur Schätzer/KI hart (behoben), Claim-Text im Ziel-Modus nannte das falsche Modell (korrigiert).

**~18:00 (25.10.) – Update 4 an Ace (Neo: "schreib doch mal das ergebnis an ace … und frag ihn mal zu seiner meinung wie das zu wave passt").** E-025/E-026-Ergebnis und Harness-Ablauf per Nexus (Thread [ID intern], Datei `E-026-ergebnis.md`), Kopie `berichte/2026-10-25-update-4-ace.md`. Fünf Fragen an Ace: wie dünn echte Wave-Evidenz ist, ob es heute eine dritte Antwort gibt, ob "not established" in den Ablauf passt (Eskalationslast), konkrete Wave-Fälle von glücklichem Vertrauen, Machbarkeit eines Schattenlaufs. Ausdrücklich: nichts ändern, nichts deployen.

**~18:15 (25.10.) – Antwort von Ace auf Update 4** (`berichte/2026-10-25-antwort-ace-update-4.md`, Status Hinweis, teils aus Aces Gedächtnis). Kern: Der nächste echte LLM-Prüfer in Wave ist der Episoden-Tick. Er entscheidet im Wesentlichen auf der Selbstauskunft des Workers, eine dritte Antwort (`needs_human_review`) gibt es schon (18 von 35 Episoden). Laut Prompt gilt `done` auch bei fehlgeschlagenem letztem Schritt ohne klaren nächsten Schritt. Drei Wave-Vorfälle passen zum E-026-Muster (Postfix "queued" statt zugestellt, synthetische Probe grün, pm2 "online" mit altem Code). Ace hält einen Live-Schattenlauf für zu dünn und schlägt eine Rückschau auf ~130 gespeicherte Fälle mit Näherungs-Labels vor (braucht Neos Go). Ace benennt selbst, dass er an mehreren Fällen beteiligt war.

**~18:30 (25.10.) – E-027 (Rückschau auf echte Wave-Fälle) geplant, Export bei Ace angefragt (Neo: "klar").** Plan: Sonnet 5.5 prüft ~130 gespeicherte Wave-Fälle (Episoden-Tick, Executor, Bridge) in den E-026-Zellen (Norm × dritte Antwort). Ausgang aus fester Regel über mechanische Spuren (execution_failed, wieder geöffnet, späterer Vorfall, Nachfolge-Fix), Neo prüft blind eine Stichprobe von ~20; "belegt / nicht belegt" je Fall durch GPT. Ace liefert nur und labelt nicht (er war an Fällen beteiligt). Anfrage mit Feldliste: `berichte/2026-10-25-anfrage-ace-wave-export.md`. Wave-Daten kommen nicht auf GitHub (`daten/wave-export*/` in `.gitignore`, Harness-Welt mit lokalem Store). Präregistrierung folgt, wenn der Export da ist.

**~18:45 (25.10.) – E-027: Export-Bedingungen mit Ace geklärt.** Ace hat vor dem Bauen drei Punkte gemeldet (`berichte/2026-10-25-antwort-ace-export-1.md`): Er gibt nur nach einem Klick in einer Gravity-Freigabekarte frei (ein über Claude weitergegebenes "klar" gilt ihm nur als Absicht). Die Mengen aus Update 4 stimmten nicht. Nicht alles ist wörtlich rekonstruierbar. Neo, wörtlich: "Ja, so: Freigabe per Gravity-Karte über den Hash, alle ~320 Fälle, und jeder Fall wird markiert (wörtlich / rekonstruiert / gekürzt)." An Ace weitergegeben. Primärauswertung später nur auf wörtlichen Fällen.

**~19:15 (25.10.) – E-027: Export bei Ace gebaut, Lieferweg entschieden.** 316 Fälle (289 wörtlich, 24 rekonstruiert, 3 gekürzt), pseudonymisiert, Scan sauber, Freigabekarte in Gravity (`berichte/2026-10-25-antwort-ace-export-2.md`). Ausgangs-Spuren dünner als geplant: späterer Vorfall und Nachfolge-Fix überall leer, die Wahrheit ist nur für gescheiterte Executor-Läufe und wieder geöffnete Items bekannt. Für W1–W3 reicht "belegt / nicht belegt". Neo zum Lieferweg, wörtlich: "Ace soll einen temporären Agent-Key nur für diese eine Lieferung anlegen und danach widerrufen." An Ace weitergegeben, mit der Bitte, für den Key bei Bedarf eine eigene Freigabekarte anzulegen.

**~19:30 (25.10.) – E-027: Wave-Export empfangen und geprüft.** Ace hat nur nach Neos zwei Gravity-Freigaben geliefert (Export-Karte [ID intern], Key-Karte [ID intern]; selbst in der DB geprüft). Zuerst kam eine Probelieferung, dann der Export. Beide temporären Agent-Keys (`[Berechtigung intern]`) waren je etwa 1 s aktiv und sind per SQL geprüft widerrufen. Empfangen: `daten/wave-export-e027/` (gitignored), 316 Fälle, sha256 wie bei Ace. Unabhängige Reste-Prüfung durch Claude: kein Personenbezug gefunden (nur UUID-Fragmente, eine Firmen-Filing-ID, eine Server-IP). Wichtig für das Design (README): Ausgangs-Spuren praktisch leer (`wieder_geoeffnet` bei allen null, späterer Vorfall und Nachfolge-Fix überall null). Die Wahrheit ist nur für 18 gescheiterte Executor-Läufe bekannt, und die sind in ihrer eigenen Evidenz sichtbar. Viele frühe Bridge-Fälle sind Tests aus der Bauphase.

**~21:00 (25.10.) – E-027-Präregistrierung als Entwurf geschrieben (Neo: "Ja, schreib die E-027-Präregistrierung mit dem angepassten Design.").** Neue Hypothese H-043 (verfeinert H-041: Übertragung auf echte Wave-Aufzeichnungen), Stufe Bestätigung. Design: GPT-6.1-sol stuft alle 316 Fälle ein (nicht anwendbar / belegt Erfolg / belegt Fehlschlag / nicht belegt; Selbstauskunft zählt nicht als Beleg). Neo stuft vorher 20 Fälle blind ein; das Material-Gate verlangt ≥ 80 % Übereinstimmung und ≥ 30 nicht belegte wörtliche Fälle. Sonnet 5.5 prüft jeden anwendbaren Fall in 4 Zellen (Norm × dritte Antwort), ohne Waves Urteil im Prompt. Vorhersagen: W1 Bestätigung ohne Beleg ≥ 0,10 (getestet gegen Boden 0,05), W2/W2N Senkung durch dritte Antwort bzw. Norm ≥ +0,05; Cluster-Bootstrap über Episoden. Testwort-Fälle aus der Bauphase bleiben drin (ein echter Wave-Prüfer sah sie genauso), W1 ohne sie deskriptiv. Ausgänge sind unbekannt, gemessen wird Bestätigen ohne Beleg, nicht Übersehen. `orglab/e027.py`, `tests/test_e027.py` (17 Tests, Suite 382/382), `experimente/E-027-wave-rueckschau/prereg.md`, `dryrun.md` (erfundener Fall, keine Wave-Texte). Neos Stichprobe liegt nur lokal (`daten/wave-export-e027/neo-stichprobe-E-027.md`). Harness v1.3 dafür (externe Eingaben mit Hash, Material-Gate aus dem Modul, Anker ohne Daten, eigene Welt `welt-wave/`). Wave-Texte gehen an Anthropic und OpenAI über OpenRouter, nicht auf GitHub. Kein Lauf vor Neos Freigabe.

**~21:30 (25.10.) – E-027: Neos blinde Einstufung liegt vor, Herkunftsregel ergänzt.** Neo hat die 20 Fälle eingestuft (9 belegt Erfolg, 4 nicht belegt, 4 belegt Fehlschlag, 3 nicht anwendbar), gespeichert in `daten/wave-export-e027/neo-stichprobe.json` (lokal), Hash in `research-harness/laeufe/E-027/prereg.yaml`. Neos Frage dazu: "wie aussagekräftig ist es wenn auch eine logzeile aus dem output des agenten eigentlich llm freitext ist". Laut Aces README stimmt das für Bridge (Aces Antwort) und Episoden (Worker-Zusammenfassung); nur der Executor protokolliert selbst. Neo wählte im Antwortknopf: "Yes, add where the evidence comes from as a fixed rule and the strict reading as a descriptive extra analysis; the main analysis stays as it is." Umgesetzt vor dem Start: Feld `herkunft_evidenz` (executor = system, bridge/episode = agent), deskriptiv W1_STRENG (Bestätigung, wenn nichts vom System Geschriebenes den Ausgang zeigt) sowie W3 und Treffer getrennt nach Herkunft; neue Schwäche benannt; Folgefrage auf dem Parkplatz. Suite grün. Kein Lauf vor Neos Freigabe.

**~21:45 (25.10.) – E-027 freigegeben (Neo: "Approved, start E-027."), E-027-1 vom Kritiker gestoppt, einmal nachgebessert.** Gate FESTLEGEN bestanden (Code-Tests grün, Hash von Export und Neos Stichprobe stimmen). Gemini meldete drei blockierende Punkte: Unklar, ob W1_NW nur vollständige Fälle zählt (berechtigt, präzisiert, der Code rechnete schon so; KI-Index jetzt ausdrücklich 0-basiert), p ohne +1 und KI zusammen mit q (beide wie in E-026 begründet abgelehnt). Antworten in `prereg.md`. Code unverändert. Neuer Lauf E-027-2; blockiert der Kritiker wieder, kein Hauptlauf.

**~22:15 (25.10.) – E-027-2 am Material-Gate gestoppt (Regel greift, kein Hauptlauf).** Kritik bestanden (nichts Blockierendes). GPT hat alle 316 Fälle lesbar eingestuft (137 nicht belegt wörtlich, also genug), aber die Übereinstimmung mit Neos blinder Stichprobe liegt bei 13/20, verlangt waren 16. Die 7 Abweichungen sind systematisch: (1) 5 Episoden-Fälle, Neo "belegt Erfolg", GPT "nicht belegt". Der Abschlussbericht des Workers nennt konkrete Details (merged=true, Merge-SHA, Exit-Code 0); GPT wertet das als Selbstauskunft, weil keine Ausgabe des Systems wiedergegeben ist. Das ist genau Neos Frage von ~21:30 zum LLM-Freitext. (2) 2 Executor-Sicherheitstests (Auftrag: prüfen, dass die Allowlist ablehnt): Neo "Fehlschlag" (die Aktion lief nicht), GPT "Erfolg" (die beabsichtigte Ablehnung ist belegt). Die übrigen 13 stimmen. Nach der Präregistrierung wird nicht umgestuft; ein zweiter Versuch braucht eine neue Präregistrierung. Kein Sonnet-Urteil erhoben. Kosten etwa 1,6 $ plus Kritik. Lehre: Definitionen vor dem Einfrieren an ein paar Fällen mit Neo eichen. Entscheidung, wie es weitergeht, liegt bei Neo.

**~22:30 (25.10.) – E-027 zur Seite gelegt.** Neo, wörtlich: "legen wir es zur seite mit kommentar und möglichem späteren zweiten versuch". `experimente/E-027-wave-rueckschau/ergebnis.md` hält fest, was passiert ist, warum die Übereinstimmung nicht reichte (Agentenberichte, Prüfungen einer Ablehnung) und wie ein zweiter Versuch aussehen könnte. H-043 bleibt offen, mit Verweis. Zweiter Versuch steht auf dem Parkplatz. Wave-Daten und Welt bleiben lokal liegen.
