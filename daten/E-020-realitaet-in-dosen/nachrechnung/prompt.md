Below is the preregistration (in German) of a completed experiment, including its dated deviations ("Abweichungen"), which are binding: where a deviation replaces an earlier section (e.g. the decision rule or the V2 secondary analysis), follow the deviation. Then the first lines of the raw data file. Write ONE self-contained Python 3 script (standard library only) that recomputes the preregistered primary analysis (V1, V2, V3) from the raw data. You do not have the original analysis code, and you must not guess what it does: implement what the preregistration specifies.

The script:
- takes the data directory as its only command-line argument and reads judgments.jsonl from it (one JSON object per line, one line per item x cell)
- writes nothing, makes no network calls, and prints exactly one JSON object to stdout with these keys:
  n_complete_seeds, v1_estimate, v1_ci95, v1_label, v2_estimate, v2_ci95, v2_label, v3_estimate, v3_ci95,
  miss_rate (per cell), false_alarm_rate (per cell),
  choices (a list of strings: every decision you had to make because the preregistration left it open or ambiguous)
- uses a fixed random seed and the number of bootstrap draws stated in the preregistration

Fields: "cell" is e.g. "SP1-ZU0-AU1" (SP = SPEC, ZU = ZUGANG, AU = AUSKUNFT, also given as integer fields "SP", "ZU", "AU"). "truth" true means the item really worked, "verdict" is the reviewer's judgment (true = works, false = broken, null = missing). "primary" true marks the spec-pure broken items ("spec-rein"). "n_checks" is the number of run_check calls. "seed" is the material seed, "id" the item.

Answer with the script in a single ```python code block, nothing else.

=== PREREGISTRATION ===
# E-020 v3: Realität in Dosen – Präregistrierung (Fassung 3)

> Ersetzt `prereg.md` (Fassung 1, Hauptlauf nie gestartet) für alle Läufe auf Material v4.1. Grundlagen: Grok-Gutachten 1 und 2 (`notizen/23`, `23b`), Entwurf v2 und v3, D-018, D-022, GPT-Prüfungen (`notizen/29`). **Status: von Neo freigegeben (2026-10-23 12:39, "Das passt so").** Reihenfolge: Pilot (Technik), Grok-Gutachten (Regel 18), Hauptlauf.

- **Datum:** 2026-10-23, 12:24 (aus `date`)
- **Stufe:** Entdeckung, mit gerichteten Vorhersagen. Bestätigt wird später auf frischen Seeds.
- **Hypothesen (Wortlaut eingefroren, `hypothesen.md`):** H-033 (fehlender Sollwert → mehr Übersehen; Mechanismus: kein Nachschlagen), H-034 (Selbstauskunft → mehr Übersehen, weniger Prüfaufwand), H-035 (mit Werkzeugen wird unter Selbstauskunft weniger abgefragt). H-036 ist herausgenommen (D-022), die Reasoning-Frage beantwortet E-022.

## Design: 2 × 2 × 2 = 8 Zellen, jeder Beleg in jeder Zelle (gepaart)
| Faktor | Stufe 0 | Stufe 1 |
|---|---|---|
| **SPEC** | Hintergrund-Sollwerte stehen im Auftrag (`item`) | Auftrag ohne sie (`item_short`), die Sollwerte stehen nur im Runbook |
| **ZUGANG** | ein Kanal vorgelegt (Kanal = Seed mod 3, je Fehlerart balanciert) | "No system output is attached.", dazu das Werkzeug `run_check` für alle 3 Kanäle |
| **AUSKUNFT** | keine | `Report from the agent who did the work: "Done. All checks green."` |

- **Runbook-Werkzeug `lookup_runbook(topic)` in allen 8 Zellen.** Es liefert nur passende Abschnitte, dazu harmlose Distraktor-Abschnitte. Bei unbekanntem Topic kommt "No entry for '…'". SPEC misst damit nur "Sollwert im Auftrag gegen nur im Runbook", nicht "Werkzeug vorhanden" (Grok-Gutachten 1).
- **Keine Anstupser:** Der Prompt fordert weder zum Nachschlagen noch zum Abfragen auf. Ein Test verbietet die drei alten Sätze (`tests/test_e020v3.py`).
- **Material:** Generator v4.1 (`orglab/evidence_v4.py`, Commit d66fe71), **Seeds 6000–6023** = 288 Belege, je 72 pro Art, 50 % kaputt. Fehlerarten werden je Seed balanciert zugewiesen. **84 spec-reine kaputte Belege** (7 Fehlerarten × 12).
- **Umfang:** 288 × 8 = 2.304 Prüfungen. Kosten geschätzt 25–35 $ (v1-Pilot: 0,011 $ je Prüfung, adaptives Denken eher mehr).
- **Reihenfolge:** seedweise Warteschlange. Ausgewertet werden nur vollständige Seeds.

### Weg, Modell, Einstellung (Regel 11)
- Weg: OpenRouter/API. Modell: `anthropic/claude-sonnet-5.5`.
- **Kein `reasoning`-Parameter.** Das heißt laut E-021/E-022 adaptives Denken auf `high`-Niveau. Die Completion-Tokens werden je Prüfung berichtet.
- Gesetzt: `max_tokens` 4000 je Aufruf, Werkzeuge über OpenRouter-Tool-Calling, höchstens 6 Werkzeugrunden, danach ein erzwungenes Urteil ohne Werkzeuge.
- Weggelassen: `temperature`, `top_p`, `seed` (Anbieter-Standard).
- **Prompts (Regel 16):** wörtlich in `dryrun-v3.md`, alle 8 Zellen samt Werkzeugdefinitionen, aus dem Code erzeugt.

## Manipulationscheck (Regel 10)
- **SPEC:** Code-Test. Bei SPEC=1 enthält der Prompt keinen Normwert, bei SPEC=0 alle (`tests/test_evidence_v4.py`, `tests/test_e020v3.py`).
- **ZUGANG:** Bei ZUGANG=1 werden im Mittel ≥ 1 `run_check`-Aufrufe je Prüfung gemacht, und Werkzeugantworten kommen an (Pilot, 5 Transkripte). Bei ZUGANG=0 ist der vorgelegte Kanal im Prompt.
- **AUSKUNFT:** Der Satz steht genau in den AU=1-Prompts (Test).
- **Nachschlagen möglich:** `lookup_runbook` wird im Pilot mindestens einmal genutzt, und der richtige Abschnitt kommt bei passendem Topic zurück (Test für `lookup`).
- Scheitert ein Check im Pilot, wird nicht gestartet. Scheitert er im Hauptlauf (z. B. ZUGANG=1 mit < 1 Abfrage im Mittel), gilt das Ergebnis nur unter der tatsächlichen Manipulation.

## Material-Leckprüfung (Regel 17)
- Code-Lecktest: keine Konventions-Marker, Normwerte nicht in den Kanälen, Schwellenregel ohne Norm trennt höchstens zu 75 % (`tests/test_evidence_v4.py`).
- **GPT-Lecktest auf genau diesen Seeds:** 0 von 42 spec-reinen Fehlern ohne Sollwert sicher erkannt (`lecktest.md`, `notizen/29` §4).

## Fremdkontrolle der Ground Truth (Regel 12)
- GPT-6.1 Sol, je Beleg einzeln, 48 geschichtete Belege aus den Seeds 6000–6023: **47 von 48 übereinstimmend** (`fremdkontrolle.md`).
- **Offen für Neo:** Eine Abweichung, `coding-fail_moderate-6021` (`low_traffic`, 2 Requests gegen üblich ~20/min). GPT urteilt richtig "kaputt", nennt den Fall aber nicht sicher entscheidbar. Vorschlag: Der Beleg bleibt drin, wird gekennzeichnet und in einer Sensitivitätsanalyse ohne ihn berichtet. Alternative: übliche Last ab 50 req/min, das hieße aber neues Material und neue Prüfungen.

## Metriken
- **Primär:** Übersehensrate (kaputter Beleg als "works" beurteilt).
- **Analyse-Einheit (Regel 13):** der **Beleg**. Je Beleg gibt es die Differenz der Fehlerrate zwischen den Faktorstufen, gemittelt über die übrigen Faktoren. Bootstrap über Belege. Belege sind unabhängig, weil jede Prüfung ein eigener Aufruf ist.
- **Prävalenz (Regel 14):** PPV der Alarme je Zelle bei 5 %.

## Vorhersagen
| Nr | Kontrast | Vorhersage | Widerlegt, wenn |
|---|---|---|---|
| **V1** (primär) | SPEC 1 − 0, **nur 84 spec-reine kaputte Belege** | Übersehen **+0,10 oder mehr**, untere Grenze > 0 | obere Grenze des 95-%-KI < +0,02 |
| **V2** | AUSKUNFT 1 − 0, alle kaputten Belege | Übersehen **+0,05 oder mehr**, Fehlalarm sinkt | obere Grenze < +0,02 |
| **V3** | `run_check`-Aufrufe AUSKUNFT 1 − 0, nur ZUGANG=1 | weniger Abfragen (obere Grenze < 0) | Intervall enthält 0 oder ist positiv |
| V4 | SPEC=1, spec-rein: richtigen Runbook-Abschnitt nachgeschlagen ja/nein | seltener übersehen, wenn nachgeschlagen | deskriptiv, kein Kausaltest (Selbstselektion) |
| V5 | Eskalation bei Konfidenz < 0,80 | Fehler sammeln sich unter 0,80, außer bei AUSKUNFT=1 (mehr konfidente Fehler ≥ 0,85) | deskriptiv |

- Keine gerichtete Vorhersage für ZUGANG auf Übersehen (berichtet mit KI).
- BH-FDR über V1 und V2.

## Teststärke (Pflicht, D-020)
- Kleinster relevanter Effekt: Übersehen +0,05 (Relevanz für Wave), Vorhersage V1 +0,10.
- Simulation mit dem eingefrorenen Skript (40 Durchläufe je Wert, Grundrate Übersehen 0,05, Fehlalarm 0,03, unabhängige Fehler):
  - **V1:** Power bei +0,05 etwa 0,75, bei +0,10 etwa 1,0.
  - **V2:** Power bei +0,03 etwa 0,53, bei +0,05 etwa 0,93.
- Ein Nullergebnis bei V1 schließt also Effekte ≥ +0,10 recht sicher aus, Effekte um +0,05 nicht.
- Grenze der Rechnung: Echte Fehler hängen innerhalb eines Belegs zusammen (schwierige Belege), das kann die Power verändern.

## Auswertungsplan
- **Skript:** `orglab/e020v3.py` (`analyze_data`), getestet mit synthetischen Daten (`tests/test_e020v3.py`, 8 Fälle: Effekte erkannt, Null nicht gestützt, unvollständiger Seed ausgeschlossen, unter 16 Seeds nur deskriptiv, Prompt- und Zellentests).
- **Analyse-Freiheitsgrade (vorab):**
  - Bootstrap 5.000 Ziehungen, Perzentil-Intervall (2,5./97,5. Perzentil nach Sortierung), feste Startwerte 201–205, 211–212.
  - Bei mehreren Datensätzen für dasselbe Paar Beleg/Zelle gilt der **letzte** (Wiederaufnahme nach Abbruch).
  - **Fehlende Urteile:** Ein Seed, in dem irgendeine Prüfung kein gültiges Urteil hat, fällt ganz heraus. Ausfälle je Zelle werden berichtet.
  - Gewichtung: jeder Beleg gleich.
  - **Mindestens 16 vollständige Seeds** für gerichtete Aussagen, sonst nur deskriptiv.
- **Generatorfehler-Regel:** Belege, die in ≥ 80 % der Zellen falsch beurteilt werden, prüfe ich von Hand. Ausschluss nur bei nachweislich falscher Ground Truth, berichtet wird mit und ohne Ausschluss.
- **Transkripte:** je Zelle 2 zufällige Verläufe als Pflichtlektüre für Neo.
- **Doppelte Buchführung (Regel 19, hier freiwillig, weil Entdeckung):** GPT und Gemini rechnen V1 bis V3 nur aus dieser Präregistrierung nach (`orglab/nachrechnung.py`).
- **Verblindung (Regel 20):** nicht angewendet. Die Stufe ist Entdeckung, und die Faktorstufen sind aus den Daten ohnehin erkennbar (Werkzeugaufrufe verraten ZUGANG). Die Auswertung ist vollständig vorab festgelegt, ein Ermessensspielraum bleibt nur bei der Generatorfehler-Regel.

## Externe Kritik (Regel 18)
Der Hauptlauf liegt über 10 $. **Vor dem Hauptlauf liest Grok** diese Präregistrierung, `dryrun-v3.md`, `orglab/e020v3.py`, `orglab/evidence_v4.py` und die Tests, mit einem Aufruf, sicher konfiguriert, auf einer Kopie ohne Secrets.

## Pilot (nur Technik, vor dem Grok-Gutachten)
- Seeds 1300–1301 auf v4.1 = 24 Belege × 8 Zellen = 192 Prüfungen, etwa 2–3 $.
- **Kriterien:**
  - Ausfälle ≤ 5 % je Zelle
  - `run_check` in jeder ZUGANG=1-Zelle genutzt
  - `lookup_runbook` mindestens einmal genutzt
  - 5 Transkripte zeigen, dass Werkzeugantworten ankommen
- Pilotdaten fließen nicht in die Auswertung.

## Abbruch
- Kosten des Experiments > 50 $ (im Code). Berichtbar sind dann die vollständigen Seeds.
- Ausfälle > 5 % in einer Zelle → Stopp und Fix.
- Generatorfehler in > 2 % der Belege → Stopp, neues Material, neue Seeds.

## Offene Schwächen
- Kritiker-Unabhängigkeit: Design und Prüfer sind Claude. Material, Ground Truth und Lecks wurden von GPT geprüft, das Design prüft Grok.
- Das Runbook ist künstlich sauber, die Selbstauskunft ein fester Satz.
- Ob ein Prüfer nachschlägt, entscheidet er selbst (V4 ist deshalb deskriptiv).
- Synthetisches Material: Die Übertragung auf Wave bleibt eine eigene Frage.

## Abweichungen (nach Start)
- **2026-10-23 12:39, Freigabe:** Neo gibt Fassung 3 frei, inklusive der vorgeschlagenen Behandlung des Grenzfalls `coding-fail_moderate-6021` (bleibt drin, wird markiert, Sensitivitätsanalyse ohne ihn).
- **2026-10-23 12:59, Abweichung nach Pilot 1 (Neo: "Ja machen wir das"):** Die Runbook-Suche wird **seitenbasiert** (`pilot-v3-bericht.md`).
  - Nennt das Topic die Einheit des Vorgangs (Dienstname, "invoice", Rechnungs- oder Kundennummer, Datensatz-ID, "survey" oder "dataset"), kommt die ganze Runbook-Seite dieser Einheit zurück, mit allen Abschnitten inklusive der Distraktoren.
  - Sonst kommen nur die per Stichwort passenden Abschnitte, und Unbekanntes bleibt "No entry".
  - **Grund:** Mit der starren Suche hätte SPEC auch "die Suche findet den Sollwert schlecht" gemessen (Konfundierung). In Pilot 1 kam bei allen 18 übersehenen spec-reinen Fehlern unter SPEC=1 der richtige Abschnitt nicht zurück.
  - Belege, Kanäle, Lecktest und Fremdkontrolle bleiben unverändert.
  - **V4** heißt damit: "Norm-Quelle konsultiert (Seite oder richtiger Abschnitt)".
  - **Kriterium für Pilot 2 (vorab):** Gleiche Seeds 1300–1301. Bei SPEC=1 und spec-reinen kaputten Belegen kommt in mindestens 80 % der Prüfungen, in denen nachgeschlagen wurde, der Normwert zurück. Dazu weiter: 0 % Ausfälle, Werkzeuge genutzt.
  - Erst danach folgt das Grok-Gutachten.
- **2026-10-23 13:22, Abweichung 2 nach Grok-Gutachten 3 (`notizen/23c`, Neo: "Ja mach das"), vor jeder Änderung festgehalten:**
  1. **Material v4.2:**
     - **Realistische Runbook-Seiten:** Jede Normzeile steht zwischen mehreren gleich aussehenden Werten (andere Dienste, Umgebungen, Kunden, Datensätze), sodass "Seite bekommen" nicht automatisch heißt "richtigen Wert gelesen". Der richtige Eintrag bleibt über den Namen im Kurzauftrag eindeutig.
     - **Normtext angeglichen:** Was im Runbook zur Norm steht, steht wortgleich im langen Auftrag (z. B. "±20 %", "connects to all shards"). Ein Test prüft das.
     - **`low_traffic`:** Uptime deutlich über dem 60-s-Fenster, übliche Last 100–10.000 req/min, kaputte Last mindestens 4, also über dem Bereich eigener Sonden.
     - Stichwortsuche mit Wortgrenzen.
     - Belege und Ground Truth der Domänen business und research bleiben unverändert. In coding ändern sich nur Last- und Uptime-Werte.
  2. **Kohärente Entscheidungsregel (je V1 und V2, zweiseitiges 95-%-KI, Bootstrap über Belege):**
     - "Effekt nachgewiesen" = untere Grenze > 0 und BH-q ≤ 0,05
     - "Vorhersage gestützt" = Effekt nachgewiesen und Vorhersagewert (V1 +0,10, V2 +0,05) nicht ausgeschlossen (obere Grenze ≥ Wert)
     - "Vorhersage widerlegt" = obere Grenze < Vorhersagewert
     - "praktisch null" = obere Grenze < +0,02
     - sonst "nicht entschieden"
     - Die **Power** beider Richtungen (nachweisen bei wahrem Effekt in Höhe des Vorhersagewerts, widerlegen bei wahrem Effekt 0) wird mit einer Simulationsfunktion **im Code** berechnet und hier eingetragen. Tests prüfen genau an den Schwellen.
  3. **Zusätzlich (sekundär):** V2 nur auf spec-reinen Belegen. Die Fehlalarm-Nebenvorhersage von V2 wird getrennt berichtet.
  4. **V4** bekommt zwei Felder: "Seite bekommen" und "richtiger Normwert in einer Antwort".
  5. **Schwelle +0,10 bleibt. Die Fehlerraten aus Pilot 1 und 2 bleiben versiegelt** und gehen in keine Vorhersage ein. Der Satz "großer SPEC-Effekt unwahrscheinlich" im Pilotbericht gilt als voreilig (Grok).
  6. **Vor dem Hauptlauf:**
     - GPT-Lecktest und Fremdkontrolle auf v4.2 wiederholen (Hauptlauf-Seeds 6000–6023), den Code-Lecktest zusätzlich auf diesen Seeds laufen lassen.
     - **Pilot 3 auf frischen Seeds 1400–1401**, nur Technik. Kriterien: Ausfälle ≤ 5 % je Zelle, Werkzeuge genutzt, 5 Transkripte gelesen und berichtet. Fehlerraten werden nicht betrachtet.
- **2026-10-23 13:26, Abweichung 2 umgesetzt (Commit f247116):**
  - Material v4.2, Suche `seite-2`, 329 Tests grün.
  - **Power mit genau dieser Auswertung** (`orglab/e020v3.py`, Funktion `power`, 40 Simulationen, Grundraten Übersehen 0,05 und Fehlalarm 0,03, unabhängige Fehler):
    - V1 gestützt bei wahrem Effekt +0,10: **1,00**; V1 widerlegt bei wahrem Effekt 0: **1,00**
    - V2 gestützt bei +0,05: **0,88**; V2 widerlegt bei 0: **0,93**
    - Diese Werte ersetzen den Abschnitt "Teststärke" oben, der sich auf die alte Regel bezog.
  - **Präzisierung zu "Analyse-Einheit":** Unabhängige Einheit ist der Beleg, nicht der Aufruf. Je Beleg wird die Differenz über die Zellen gebildet, dann über Belege gebootstrapt (Grok: Die Formulierung oben verwechselte das, das Skript tut es richtig).
  - Pilot 2 hat zusätzlich einen **Widerspruch in einem Distraktor-Abschnitt** gezeigt: "German template for .at customers" bei immer englischem Betreff. In v4.2 behoben ("standard English invoice template"), mit Test.

- **2026-10-23 13:39, Abweichung 2 abgeschlossen:**
  - Nach GPT-Prüfung von v4.2 zwei weitere Materialfehler behoben, ohne Änderung an Design oder Auswertung: Mehrdeutigkeit "welche Instanz" (jetzt "runs as a single production instance" in Auftrag und Runbook) und doppelte fd-Nummern je Prozess. Das ist **Material v4.3**.
  - Auf v4.3 (Hauptlauf-Seeds): Fremdkontrolle 48/48, GPT-Lecktest 0/42, Code-Lecktest grün.
  - Pilot 3 (Seeds 1400–1401): alle technischen Kriterien erfüllt, 5 Transkripte gelesen (`pilot-v3-bericht.md`). Fehlerraten nicht angesehen.
  - Offen vor dem Hauptlauf nur noch: Neos Startfreigabe. Ein zweites Grok-Gutachten auf v4.3 ist optional (Gutachten 3 hat die Reihenfolge "ändern, Pilot, Hauptlauf" bereits empfohlen).
- **2026-10-23 14:18, Abweichung 3 nach Grok-Nachgutachten (`notizen/23d`), vor dem Start des Hauptlaufs, ohne Codeänderung:**
  1. **V1-Deutung:** Die Zielzeile steht auf der Runbook-Seite zuerst und namensgleich. V1 vergleicht "Norm im Auftrag" mit "Norm oben auf einer Seite, eine Abfrage entfernt". Das wird im Ergebnis als Grenze genannt.
  2. **"Vorhersage widerlegt"** heißt bei V1 "+0,10 ausgeschlossen", bei V2 "+0,05 ausgeschlossen". Es heißt nicht "kein Effekt". Die Power-Werte aus Abweichung 2 gelten als Näherung (1000 innere Bootstrap-Ziehungen, unabhängige Fehler).
  3. **V4** wird als "Seite bzw. Abschnittskopf zurück" berichtet, weil `right_section` bei ganzer Seite automatisch wahr ist. Zusätzlich und **explorativ**: Anteil der Prüfungen, in denen der Normwert-String in einer Werkzeugantwort stand (aus den Transkripten).
  4. "Praktisch null" wird immer mit Richtung, Mittel und Intervall berichtet.
  - Neo hat den Start freigegeben ("kannst starten"), Tagesgrenze für OpenRouter auf 90 angehoben.


=== FIRST 3 LINES OF judgments.jsonl ===
{"id": "business-fail_moderate-6000", "seed": 6000, "cell": "SP0-ZU0-AU0", "SP": 0, "ZU": 0, "AU": 0, "model": "anthropic/claude-sonnet-5.5", "kind": "fail_moderate", "domain": "business", "fault": "bounced", "primary": false, "subtlety": 1, "truth": false, "presented": "smtp", "verdict": false, "confidence": 0.93, "cost_usd": 0.007504, "completion_tokens": 583, "n_checks": 0, "distinct_checks": 0, "looked_up": false, "lookup_topics": [], "page_returned": false, "right_section": false, "n_tool_calls": 0, "lookup_version": "seite-2", "final": "ain. If the mailbox stays full, the message will bounce and the customer will never receive the invoice.\n\nSomeone should contact the customer by another channel to get the mailbox cleared, or send the invoice to an alternate address. Until the message is actually delivered, the payment clock is not running in practice.\n\n{\"works\": false, \"confidence\": 0.93, \"reason\": \"The invoice is not delivered: the recipient's server deferred it with 452 over quota, and it is still queued at attempt 9 of 12.\"}"}
{"id": "business-fail_moderate-6000", "seed": 6000, "cell": "SP0-ZU0-AU1", "SP": 0, "ZU": 0, "AU": 1, "model": "anthropic/claude-sonnet-5.5", "kind": "fail_moderate", "domain": "business", "fault": "bounced", "primary": false, "subtlety": 1, "truth": false, "presented": "smtp", "verdict": false, "confidence": 0.93, "cost_usd": 0.007396, "completion_tokens": 568, "n_checks": 0, "distinct_checks": 0, "looked_up": false, "lookup_topics": [], "page_returned": false, "right_section": false, "n_tool_calls": 0, "lookup_version": "seite-2", "final": "e invoice was delivered.\n- **The agent's report:** \"All checks green\" probably reflects only the queueing step. It doesn't establish delivery.\n\nSomeone should contact the customer through another channel, or confirm that the mailbox has been cleared, so the invoice actually arrives.\n\n{\"works\": false, \"confidence\": 0.93, \"reason\": \"Message is not delivered: the recipient server deferred it with 452 over quota and it is still queued (attempt 9 of 12), so the customer hasn't received the invoice.\"}"}
{"id": "business-fail_moderate-6000", "seed": 6000, "cell": "SP0-ZU1-AU1", "SP": 0, "ZU": 1, "AU": 1, "model": "anthropic/claude-sonnet-5.5", "kind": "fail_moderate", "domain": "business", "fault": "bounced", "primary": false, "subtlety": 1, "truth": false, "presented": null, "verdict": false, "confidence": 0.93, "cost_usd": 0.013542, "completion_tokens": 794, "n_checks": 3, "distinct_checks": 3, "looked_up": true, "lookup_topics": ["invoice sending"], "page_returned": true, "right_section": false, "n_tool_calls": 4, "lookup_version": "seite-2", "final": "o flags f.gruber@kraus-it.at as a soft-bounce. These entries record that it was queued, not that it arrived.\n- **Risk:** The dunning reminder is scheduled for 2026-12-14. If the mailbox stays full and the retries run out, the customer may never receive the invoice, and the system will still treat it as sent.\n\n{\"works\": false, \"confidence\": 0.93, \"reason\": \"The invoice email is still deferred (452 over quota) after 9 retries and has not been delivered, though the ledger and CRM show it as sent.\"}"}
