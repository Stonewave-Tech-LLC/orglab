Below is the preregistration (in German) of a completed confirmatory experiment, then the first lines of the raw data file. Write ONE self-contained Python 3 script (standard library only) that recomputes the preregistered primary analysis (the five predictions V1, W1, C1, C2, F1) from the raw data. You do not have the original analysis code, and you must not guess what it does: implement what the preregistration specifies.

The script:
- takes the data directory as its only command-line argument and reads judgments.jsonl from it (one JSON object per line, one line per model x item x cell)
- writes nothing, makes no network calls, and prints exactly one JSON object to stdout with these keys:
  n_complete_seeds, and for each of V1, W1, C1, C2, F1: <name>_estimate, <name>_ci95, <name>_q, <name>_label;
  plus sonnet_v1, sonnet_c1, sonnet_c2, sonnet_f1 (the same contrasts for the comparison model),
  choices (a list of strings: every decision you had to make because the preregistration left it open or ambiguous)
- uses the fixed random seeds and the number of bootstrap draws stated in the preregistration

Fields: "model" is "anthropic/claude-haiku-5.5" (target) or "anthropic/claude-sonnet-5.5" (comparison). "cell" is e.g. "SP1-ZU0-AU1" (also integer fields "SP", "ZU", "AU"). "truth" true means the item really worked, "verdict" is the reviewer's judgment (true = works, false = broken, null = missing). "primary" true marks spec-pure broken items. "looked_up" is whether the reviewer queried the runbook. "seed" is the material seed, "id" the item.

Answer with the script in a single ```python code block, nothing else.

=== PREREGISTRATION ===
# E-024: Bestätigung "Der Maßstab muss mit" – Präregistrierung

> Bestätigungslauf zu E-023 (Neo, 23.10.: "Yes"). Gleiches Design und Material wie E-020 v3/E-023, **frische Seeds**, beide Modelle. Die drei explorativen Befunde aus E-023 werden hier zu vorab festgelegten, gerichteten Vorhersagen. **Status: Materialprüfung erledigt, mit Neo besprochen (19:28). Neo: "die 36 € investieren wir heut noch". Auf Neos Frage nach einer Empfehlung umgesetzt: Variante A (siehe 'Entscheidungen nach der Materialprüfung'). Es fehlt noch das Grok-Gutachten (Regel 18). Findet Grok etwas Blockierendes, wird nicht gestartet.**

- **Datum:** 2026-10-23, 18:58 (aus `date`)
- **Stufe: Bestätigung.** Damit gelten die Regeln 18 (Kritik vorab), 19 (doppelte Buchführung, Pflicht) und 20 (verblindete Auswertung, Pflicht).
- **Hypothesen:**
  - H-033 für Haiku (modellabhängig)
  - H-038 (Wechselwirkung Modell × Harness)
  - **neu H-039** (Verdrängung): Werkzeuge, die Daten liefern, verdrängen bei schwächeren Prüfern das Nachschlagen des Maßstabs. Wortlaut siehe `hypothesen.md`, wird mit diesem Commit eingetragen.
  - **neu H-040** (Misstrauen statt Nachlässigkeit): Eine Selbstauskunft erhöht bei schwächeren Prüfern die Fehlalarme.

## Was diese Bestätigung leisten soll, und was nicht
- **Ziel:** Halten die E-023-Befunde auf neuen Belegen, die niemand vorher gesehen hat? Fallen sie dort ähnlich groß aus?
- **Nicht Ziel:** Übertragung auf Wave. Wave läuft vollständig auf Sonnet (Neo, 23.10.). Haiku ist hier ein Modell dafür, *wie* ein Prüfer scheitert. Ob Sonnet unter Last ähnlich scheitert, ist ein eigenes Folgeexperiment.
- Die Einordnungsregeln aus `experimente/E-023-haiku-dosen/prereg.md` gelten unverändert: Effekte vergleichen, keine Fehlerniveaus, keine Wave-Regel aus Haiku-Daten.

## Design
- **Wie E-020 v3/E-023:** 2 × 2 × 2 Zellen (SPEC × ZUGANG × AUSKUNFT), jeder Beleg in jeder Zelle, Prompts und Werkzeuge über dieselben Funktionen (`e020v3.build_prompt`, `tools_for`, `judge`). Die Prompttexte stehen in `experimente/E-020-realitaet-in-dosen/dryrun-v3.md`.
- **Material:** Generator v4.3 **unverändert** (`orglab/evidence_v4.py`). Die Bestätigung soll unter denselben Bedingungen messen wie die Entdeckung. Die bekannten Materialschwächen werden nicht im Generator repariert, sondern über die Einzelkanal-Fremdkontrolle erfasst und in einer vorab festgelegten Zusatzanalyse ausgeschlossen.
- **Seeds 7000–7023** (frisch, in keinem Experiment benutzt; Test), 288 Belege, 84 spec-rein kaputt.
- **Beide Modelle auf denselben Belegen:**
  - `anthropic/claude-haiku-5.5` (Ziel)
  - `anthropic/claude-sonnet-5.5` (Vergleich, für W1)
- **Umfang:** 288 × 8 × 2 = 4.608 Prüfungen. Kosten geschätzt etwa 36 $ (Sonnet ~34 $, Haiku ~2 $), Kostenstopp 60 $ im Code.
- **Reihenfolge:** seedweise Warteschlange, je Seed beide Modelle.

### Weg, Modell, Einstellung (Regel 11)
- OpenRouter/API, beide Modelle **ohne `reasoning`-Parameter** (adaptives Denken, Probe E-023: Haiku Median ~460, Sonnet ~200 Denk-Tokens)
- `max_tokens` 4000 je Aufruf, höchstens 6 Werkzeugrunden, danach ein erzwungenes Urteil
- Weggelassen: `temperature`, `top_p`, `seed`

## Vorhersagen (alle gerichtet, für Haiku; BH über alle fünf)
Die Vorhersagewerte liegen bewusst deutlich unter den E-023-Schätzungen (Spalte rechts). Entdeckte Effekte fallen beim Nachmessen fast immer kleiner aus.

| Nr | Hypothese | Kontrast (Einheit: Beleg) | Vorhersage | E-023 |
|---|---|---|---|---|
| **V1** (primär) | H-033 | Übersehen SPEC 1 − 0, spec-reine kaputte Belege, gemittelt über ZUGANG und AUSKUNFT | ≥ +0,10 | +0,253 |
| **W1** (primär) | H-038 | V1 Haiku − V1 Sonnet, gepaart je Beleg | ≥ +0,10 | +0,247 |
| **C1** | H-039 | Nachschlagen (`looked_up`) ZUGANG 0 − 1, nur SPEC = 1, alle Belege, gemittelt über AUSKUNFT | ≥ +0,20 | +0,424 |
| **C2** | H-039 | Übersehen ZUGANG 1 − 0, nur SPEC = 1, spec-reine kaputte Belege | ≥ +0,10 | +0,404 |
| **F1** | H-040 | Fehlalarm AUSKUNFT 1 − 0, **nur Ok-Belege, die auch mit einem Kanal entscheidbar sind** (101 von 144, laut `einzelkanal-ausschluss.json`), gemittelt über SPEC und ZUGANG | ≥ +0,02 | +0,042 (auf allen Ok-Belegen) |

- **Entscheidungsregel** (wie E-020 Abweichung 2, `e020v3.classify`):
  - Zweiseitiges 95-%-KI per Bootstrap über Belege. q aus einseitigem Bootstrap-p ("Mittel > 0"), BH über die fünf.
  - **nachgewiesen** = untere Grenze > 0 und q ≤ 0,05
  - **gestützt** = nachgewiesen und Vorhersagewert nicht ausgeschlossen (obere Grenze ≥ Vorhersagewert)
  - **Effekt nachgewiesen, aber kleiner als vorhergesagt** = nachgewiesen und obere Grenze < Vorhersagewert
  - **widerlegt** = obere Grenze < Vorhersagewert, ohne Nachweis
  - **praktisch null** = obere Grenze < +0,02
  - sonst **nicht entschieden**
- **Ein Befund gilt als bestätigt**, wenn sein Etikett "gestützt" oder "Effekt nachgewiesen, aber kleiner" lautet. Bei "kleiner" wird die Größe ausdrücklich berichtet.
- **Sonnet-Werte** der Kontraste V1, C1, C2, F1 werden deskriptiv mitberichtet. Erwartet sind dort etwa 0, wie in E-020.

## Teststärke (Simulation `e024.power`, 30 Durchläufe, 1.000 Ziehungen)
- Annahme: halbierte E-023-Effekte bei Haiku (V1 +0,12, Rückgang des Nachschlagens 0,22, Fehlalarm +0,02), Sonnet ohne Effekte.
  - Power für "gestützt": **V1 1,00, W1 1,00, C1 1,00, C2 0,80, F1 0,40**
- F1 bei voller E-023-Größe (+0,04, Grundrate wie Haiku 0,07): **0,63**
- **F1 auf den 101 einzeln entscheidbaren Ok-Belegen** (endgültige Definition), bei +0,04: **0,37**.
- **Folge:** F1 ist schwach abgesichert. Ein Null-Ergebnis bei F1 heißt "nicht bestätigt", **nicht** "widerlegt". So wird es berichtet.

## Manipulationscheck (Regel 10)
- **ZUGANG:** `run_check` im Mittel ≥ 1 je Prüfung in den ZUGANG=1-Zellen, je Modell.
- **Werkzeugfähigkeit:** Ausfälle ≤ 5 % je Zelle und Modell.
- **SPEC, AUSKUNFT:** Code-Tests (unverändert).
- **Denken:** Completion-Tokens je Modell werden berichtet (erst nach dem Entblinden, weil sie das Modell verraten).
- Scheitert ein Check bei einem Modell, gelten dessen Kontraste nur deskriptiv.

## Material (Regeln 12, 17), auf den Seeds 7000–7023
- **Fremdkontrolle wie bisher** (GPT-6.1 Sol, 48 geschichtete Belege, alle drei Kanäle): Ergebnis wird hier vor der Freigabe eingetragen.
- **Lecktest** (Kurzauftrag ohne Sollwerte): Ergebnis wird hier eingetragen.
- **Neu: Fremdkontrolle je Einzelkanal** (Lehre aus E-020, Erweiterung von Regel 12):
  - GPT sieht **jeden** der 288 Belege mit vollem Auftrag samt Sollwerten, aber **nur den Kanal, der bei ZUGANG = 0 vorgelegt wird** (`fremdkontrolle-einzelkanal.md`).
  - Belege, bei denen GPT von der Wahrheit abweicht oder "nicht entscheidbar" sagt, stehen in `einzelkanal-ausschluss.json`. Sie gelten als **einzeln nicht entscheidbar**.
  - Das deckt auch die zweite offene Frage ab: Ob verrauschte Ok-Belege gegen die Norm "single production instance" zweideutig sind, zeigt sich daran, ob GPT sie mit einem Kanal als kaputt beurteilt.
  - Ergebnis wird hier eingetragen.

### Ergebnisse der Materialprüfung (2026-10-23, vor 19:05)
- **Fremdkontrolle (alle Kanäle): 47 von 48.** Abweichung bei `coding-ok_clear-7009`:
  - GPT rechnet aus dem kumulativen Zähler 970 Requests in 515 s, also etwa 113/min. Das liegt unter dem Normband 120–180.
  - Der Generator meint "ok". Echte Mehrdeutigkeit (Zähler über die Laufzeit gegen Last pro Minute).
  - Vorschlag: als Grenzfall kennzeichnen, Sensitivitätsanalyse ohne ihn (wie 6021). **Klärung durch Neo.**
- **Lecktest: 0 von 42** spec-reinen Fehlern ohne Sollwert sicher erkannt. Kriterium erfüllt.
- **Einzelkanal: 62 von 288 (21,5 %) nicht entscheidbar** → über der eigenen Grenze von 10 %, **Start gestoppt, Entscheidung Neo.**
  - **43 von 144 Ok-Belegen**, davon 28 von 48 bei "coding" und 15 von 48 bei "research".
    - 42 davon beurteilt GPT als "nicht bestätigt, nicht entscheidbar". Ein einzelner Kanal kann den Erfolg nicht *beweisen*: Version nicht zur Laufzeit gemeldet, keine Zeilenzahl, Zähler ohne Zeitbasis.
    - Ein Kanal kann einen Fehler zeigen, aber oft keinen Erfolg belegen.
  - **Nur 7 von 84 spec-reinen kaputten Belegen** (alle `low_traffic`), dazu 12 weitere kaputte (`db_down`, `bounced`).
  - **Folgen:**
    - V1, W1, C1 und C2 sind kaum betroffen. C1 und C2 messen in ZUGANG = 1 mit allen Kanälen, und spec-rein betrifft es nur 7 Belege.
    - **F1 ist stark betroffen.** Ein "funktioniert nicht" bei einem einzeln nicht belegbaren Ok-Beleg ist kein klarer Fehlalarm, sondern eine vertretbare Weigerung, Unbelegtes zu bestätigen. Das binäre Urteil zwingt sie in "kaputt".
    - Die E-023-Lesart "Selbstauskunft macht Haiku misstrauisch" (H-040) kann deshalb auch heißen: "Selbstauskunft macht Haiku strenger bei unzureichender Evidenz".
  - **Umgekehrt für E-020:** Sonnets 0 Fehlalarme in ZUGANG = 0 heißen auch, dass Sonnet Ok-Belege bestätigt hat, deren Erfolg aus dem einen Kanal nicht belegbar war. Richtig im Ergebnis, aber nicht durch die Evidenz gedeckt (Hinweis).

### Entscheidungen nach der Materialprüfung (vor dem Start, Neo 23.10.)
1. **Material bleibt unverändert** (v4.3), damit der Lauf eine echte Wiederholung von E-023 ist.
2. **F1 nur auf einzeln entscheidbaren Ok-Belegen.** Ein "kaputt" für einen Erfolg, den der vorgelegte Kanal nicht belegen kann, ist kein klarer Fehlalarm. F1 auf allen Ok-Belegen (wie in E-023) wird nur deskriptiv berichtet.
3. **`coding-ok_clear-7009`** (Fremdkontrolle 47/48) wird als Grenzfall gekennzeichnet. Sensitivitätsanalyse ohne ihn (`e024.GRENZFAELLE`).
4. Die 10-%-Grenze der Einzelkanal-Prüfung ist überschritten (21,5 %). Gestartet wird trotzdem, weil die Ursache geklärt ist: Es sind vor allem Ok-Belege, deren Erfolg ein einzelner Kanal nicht beweisen kann. Davon ist im Wesentlichen nur F1 betroffen, und das ist mit Punkt 2 adressiert.
5. Das "glückliche Vertrauen" (Bestätigen ohne ausreichende Evidenz) wird als eigene Hypothese H-041 eingetragen und in einem eigenen Folgeexperiment getestet (Zwillingsbelege, dritte Antwort "nicht belegt"). Neo kennt das Muster aus Wave ("ist mir schon oft untergekommen").

### Änderungen nach Grok-Gutachten 5 (`notizen/23e`, 19:41, vor dem Start)
1. **Etiketten im Skript** (`e024.label`) folgen jetzt genau dieser Präregistrierung. Vorher hätte `e020v3.classify` "nachgewiesen, aber kleiner" als "widerlegt" etikettiert, und das wäre vor dem Entblinden festgeschrieben worden. Neu:
   - "BESTÄTIGT (Vorhersagewert nicht ausgeschlossen)"
   - "BESTÄTIGT, aber kleiner als vorhergesagt"
   - "nicht bestätigt: praktisch null (widerlegt)"
   - "nicht bestätigt: Vorhersagewert ausgeschlossen (widerlegt)"
   - "nicht bestätigt: nicht entschieden"
   - **F1 ohne Nachweis: "nicht bestätigt (schwache Power, kein Widerlegen)"**
2. **Fehlt `einzelkanal-ausschluss.json`, bricht die Auswertung ab**, statt F1 still über alle Ok-Belege zu rechnen.
3. **Der Manipulationscheck läuft schon in der verblindeten Auswertung:** `run_check` bei ZUGANG=1 im Mittel ≥ 1, Ausfälle ≤ 5 % je Zelle, je Arm. Er verrät das Modell nicht, weil beide im Pilot 3,0 abfragen. Scheitert er, ist alles nur deskriptiv.
4. **C1 bleibt in der Sekundäranalyse auf allen Belegen.** Nachschlagen ist kein Wahrheitsurteil, der Einzelkanal-Ausschluss betrifft es nicht.
5. **Diagnose, deskriptiv, ohne BH:** ZUGANG 1 − 0 auf Übersehen bei SPEC = 0, spec-rein, je Modell.
   - Zeigt es bei Haiku keinen Schaden, hängt der C2-Schaden am fehlenden Sollwert und nicht am Zugang an sich.
   - Zusätzlich berichtet: Anteil der Nicht-Nachschläge, die die Rundengrenze (6) erreicht haben, aus den Transkripten.
6. **Lesart "nur schwächere Prüfer" (H-039):** Sie wird getragen, wenn Sonnet bei C1 und C2 nahe 0 liegt (deskriptive Spalte). Ein bestätigtes Haiku-C1/C2 allein zeigt nur den Haiku-Kontrast.
7. **Power mit der F1-Einschränkung** (`e024.power`, halbierte Effekte): V1 1,0, W1 1,0, C1 1,0, C2 0,8, **F1 0,3**.

## Auswertungsplan
- **Skript:** `orglab/e024.py`. Getestet mit synthetischen Daten (`tests/test_e024.py`):
  - Effekte erkannt, Null nicht gestützt
  - unvollständiger Seed in beiden Armen entfernt
  - verblindete Auswertung läuft auf A/B ohne Modellnamen
  - unter 16 Seeds nur deskriptiv
- **Rauchtest auf den Entdeckungsdaten** (E-020-Sonnet plus E-023-Haiku, schon bekannt): reproduziert V1 und W1 aus E-023 exakt. C1 +0,42, C2 +0,40, F1 +0,04.
- **Analyse-Freiheitsgrade (vorab):**
  - Bootstrap 5.000 Ziehungen, Perzentil (Index ⌊0,025·B⌋ bzw. ⌊0,975·B⌋−1 der sortierten Mittel)
  - Startwerte: Intervalle V1/W1/C1/C2/F1 = 241–245, p-Werte 251–255
  - je (Modell, Beleg, Zelle) zählt der **letzte** Datensatz
  - **Ein Seed zählt nur, wenn er in beiden Modellen vollständig ist.** Ein fehlendes Urteil entfernt den Seed aus beiden Modellen, denn W1 ist gepaart. Ausfälle je Zelle und Modell werden berichtet.
  - jeder Beleg gleich gewichtet
  - **mindestens 16 vollständige Seeds**, sonst nur deskriptiv
  - Ein Ausfall wird **nicht** wiederholt (Lehre aus E-023: Regel vor Nachbessern)
- **Primär:** alle Belege. **Sekundär (vorab festgelegt):** ohne die einzeln nicht entscheidbaren Belege laut `einzelkanal-ausschluss.json`. Diese Datei wird vor dem Hauptlauf committet.
- **Deskriptiv:** alle E-020-Kontraste (V2, V3, V4, V5, Zellen) je Modell, über `e020v3.analyze_data`.
- **Generatorfehler-Regel:** Belege, die in ≥ 80 % der Zellen von **beiden** Modellen falsch beurteilt werden, prüfe ich von Hand. Berichtet wird mit und ohne Ausschluss, primär bleibt "mit".
- **Transkripte:** je Modell 1 zufälliger Verlauf je Zelle (16), dazu je Modell 3 gezielte Verläufe (Haiku: SPEC=1, ZUGANG=1, nicht nachgeschlagen; Sonnet: dasselbe, falls vorhanden).

### Verblindung (Regel 20, Pflicht)
1. Nach dem Lauf: `python -m orglab.verblindung verblinden E-024-bestaetigung-massstab --feld model --arme anthropic/claude-sonnet-5.5 anthropic/claude-haiku-5.5 --weg completion_tokens cost_usd final lookup_topics error`
   - Die Modelle heißen dann A und B. Entfernt werden Tokens und Kosten (verraten das Modell über Preis und Länge), Antworttext, Suchbegriffe und Fehlertexte.
2. `python -m orglab.e024 verblindet` rechnet **beide** Zuordnungen vollständig ("falls A = Haiku …", "falls B = Haiku …"). Ich schreibe alle Entscheidungen in `auswertung-verblindet.md` und committe.
3. Erst dann `entblinden`, danach `python -m orglab.e024 analyze` für die endgültigen Etiketten und den Manipulationscheck (Tokens).
- **Grenze:** Das Fehlermuster kann das Modell verraten (Haiku übersieht mehr). Schutzziel ist unbewusstes Biegen bei Entscheidungen, nicht völlige Unwissenheit. Weil Auswertung und Etiketten rein skriptgesteuert sind, bleibt als Ermessen nur die Generatorfehler-Regel. Sie wird verblindet angewandt.

### Doppelte Buchführung (Regel 19, Pflicht)
GPT und Gemini schreiben die Auswertung von V1, W1, C1, C2, F1 aus dieser Präregistrierung und Beispielzeilen neu (`orglab/nachrechnung.py`, Erweiterung für E-024 vor dem Lauf). Ich lese den Code, führe ihn isoliert aus und vergleiche. Bei Abweichung gilt ein Befund erst nach Klärung.

## Externe Kritik (Regel 18)
Der Lauf kostet über 10 $, und es gibt neue Kernthesen (H-039, H-040). **Grok liest vor dem Hauptlauf** diese Präregistrierung, `orglab/e024.py`, die Tests, die Ergebnisse von E-023 und die Materialprüfungen. Ein Aufruf, sicher konfiguriert, auf einer Kopie ohne Secrets.

## Pilot (nur Technik)
- Seeds 1600–1601, beide Modelle, 384 Prüfungen, etwa 3 $
- Kriterien:
  - Ausfälle ≤ 5 % je Zelle und Modell
  - `run_check` in jeder ZUGANG=1-Zelle genutzt
  - Daten tragen das Feld `model`
  - Die Verblindung läuft probeweise auf den Pilotdaten mit Wegwerf-Schlüssel in einem Testordner
  - 3 Transkripte gelesen
- Fehlerraten werden nicht angesehen.

## Abbruch
- Kosten > 60 $ (im Code). Berichtbar sind dann die in beiden Modellen vollständigen Seeds.
- Ausfälle > 5 % in einer Zelle → Stopp und Klärung
- Einzelkanal-Fremdkontrolle zeigt > 10 % einzeln nicht entscheidbare Belege → **kein Start**, erst mit Neo besprechen

## Offene Schwächen
- Eine Modellfamilie. Design und Prüfer sind Claude. Material, Ground Truth und Auswertung prüfen GPT und Gemini, das Design Grok.
- F1 hat geringe Power.
- Die Generator-Schwächen bleiben absichtlich drin (Vergleichbarkeit mit der Entdeckung), sie sind nur erfasst.

## Abweichungen (nach Start)
-


=== FIRST 3 LINES OF judgments.jsonl ===
{"id": "business-fail_moderate-7000", "seed": 7000, "cell": "SP0-ZU0-AU0", "SP": 0, "ZU": 0, "AU": 0, "model": "anthropic/claude-sonnet-5.5", "kind": "fail_moderate", "domain": "business", "fault": "bounced", "primary": false, "subtlety": 1, "truth": false, "presented": "delivery", "verdict": false, "confidence": 0.85, "cost_usd": 0.010076, "completion_tokens": 567, "n_checks": 0, "distinct_checks": 0, "looked_up": true, "lookup_topics": ["invoice delivery", "payment terms"], "page_returned": true, "right_section": false, "n_tool_calls": 2, "lookup_version": "seite-2", "final": "or retry\" and \"deferred\", and the last update was 71 hours ago. Nothing shows the message reached the customer's mailbox. The report also shows no bounce or delivery confirmation, and no read receipt was requested. The email appears to be stuck in a retry queue, so the customer may not have the invoice.\n\n{\"works\": false, \"confidence\": 0.85, \"reason\": \"The email content is correct, but delivery is deferred and queued for retry with no update for 71h, so the invoice has not reached the customer.\"}"}
{"id": "business-fail_moderate-7000", "seed": 7000, "cell": "SP0-ZU1-AU0", "SP": 0, "ZU": 1, "AU": 0, "model": "anthropic/claude-sonnet-5.5", "kind": "fail_moderate", "domain": "business", "fault": "bounced", "primary": false, "subtlety": 1, "truth": false, "presented": null, "verdict": false, "confidence": 0.9, "cost_usd": 0.013670000000000002, "completion_tokens": 813, "n_checks": 3, "distinct_checks": 3, "looked_up": true, "lookup_topics": ["invoice sending"], "page_returned": true, "right_section": false, "n_tool_calls": 4, "lookup_version": "seite-2", "final": "ice date.\n  - The first reminder on 2026-11-29 is 7 days after the due date.\n\nThe mailbox is full and the retries are running out. If they all fail, the customer will never see the invoice, and the dunning reminder would then chase an invoice they never received.\n\n{\"works\": false, \"confidence\": 0.9, \"reason\": \"Email to m.wagner@huber-bau.de is still deferred (452 over quota, 71h, attempt 9/12) and the CRM shows a soft-bounce, so the invoice was never delivered even though the ledger says SENT.\"}"}
{"id": "business-fail_moderate-7000", "seed": 7000, "cell": "SP1-ZU0-AU1", "SP": 1, "ZU": 0, "AU": 1, "model": "anthropic/claude-sonnet-5.5", "kind": "fail_moderate", "domain": "business", "fault": "bounced", "primary": false, "subtlety": 1, "truth": false, "presented": "delivery", "verdict": false, "confidence": 0.9, "cost_usd": 0.011628000000000001, "completion_tokens": 659, "n_checks": 0, "distinct_checks": 0, "looked_up": true, "lookup_topics": ["invoice delivery", "customer K-12"], "page_returned": true, "right_section": false, "n_tool_calls": 2, "lookup_version": "seite-2", "final": "3, which is K-12's payment term.\n\nThe report doesn't show the recipient address, so I can't confirm it went to the billing contact, m.wagner@huber-bau.de. The email is also stuck in a deferred state, so the customer likely hasn't received it. The work item's goal of sending the invoice to the customer is therefore not met.\n\n{\"works\": false, \"confidence\": 0.9, \"reason\": \"Delivery is deferred and queued for retry with no update for 71h, so the invoice was not confirmed delivered to the customer.\"}"}
