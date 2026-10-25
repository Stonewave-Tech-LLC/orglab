# E-022: Reasoning-Dosis und Fehlalarme bei der Stapelprüfung – Präregistrierung

- **Datum:** 2026-10-23, 07:17 (aus `date`), vor jedem Lauf
- **Stufe:** **Bestätigung.** Frische Seeds 5000–5023, nie zuvor benutzt (geprüft per `grep` über `orglab/`, `notizen/`, `experimente/`).
- **Hypothese:** H-037 (Wortlaut eingefroren): "Gedrosseltes Reasoning (OpenRouter `effort: low`) erhöht die Fehlalarmrate von Prüfern gegenüber normalem (adaptivem) Reasoning, ohne die Übersehensrate zu senken."
- **Warum noch einmal:** In E-021 war der Kontrast vorab festgelegt, die *Deutung* entstand aber erst nach dem gescheiterten Manipulationscheck. Hier wird der Reasoning-Umfang als Bedingung **gemessen** (Regel 10), und es gibt eine Dosis-Stufe dazwischen (Methodik 2, Dosis-Wirkung).

## Konkrete Vorhersage
- Fehlalarmrate `low` deutlich über `high`: Δ ≥ +0,05 (E-021: 0,102 gegen 0,032; Probe: 0,130 gegen 0,033).
- `medium` liegt dazwischen oder auf `high`-Niveau.
- Die Übersehensrate bei `high` ist nicht wesentlich höher als bei `low` (≤ +0,03).
- **Widerlegt**, wenn P1 scheitert (untere Grenze ≤ 0) **bei bestandenem Manipulationscheck**: Dann erzeugt mehr Denken *nicht* weniger Fehlalarme, und der E-021-Kontrast hing an etwas anderem als dem Denkumfang.

## Design
- **Material:** Generator v3.1, unverändert seit Commit d4683a9 (`orglab/evidence.py`, `generate_set_v2`), Seeds 5000–5023 × 3 Domänen × 4 Arten = **288 Belege** (50 % kaputt, 12 Fehlerarten).
- **Stapel:** einmal gemischt (Tag `"e022"`), 24 Stapel zu je 12. Zusammensetzung und Reihenfolge sind in allen Armen identisch.
- **Zelle:** I1-S0-E0 aus E-019, wie E-021. Drei Prüferpositionen sehen je Beleg einen anderen Kanal.
- **Arme (gepaart, unabhängige Variable):** `reasoning.effort` = `low` · `medium` · `high` · **weggelassen** ("ohne")
- **Konstant:** Prompt, Parser, Wiederholungsregel, `max_tokens = 4000` (alles aus `orglab/batch.py`, unverändert wie in E-021)
- **Umfang:** 24 Stapel × 3 Positionen × 4 Arme = **288 Aufrufe**, 3.456 Urteile. Kosten geschätzt 6–8 $ (E-021: 144 Aufrufe 3,19 $; `high` denkt länger).
- **Reihenfolge:** stapelweise in die Warteschlange (alle Arme und Positionen eines Stapels hintereinander). Bei einem Abbruch liegen damit fast nur vollständige Stapel vor.

### Weg, Modell, Einstellung (Regel 11)
- **Weg:** OpenRouter/API (`orglab/openrouter.py`)
- **Modell:** `anthropic/claude-sonnet-5.5`
- **Parameter:**
  - `reasoning: {"effort": "low" | "medium" | "high"}` je Arm. Tatsächliche Bedeutung laut E-021-Probe: `low` deckelt das verborgene Denken (~257 Completion-Tokens), `high` erlaubt mehr (Median ~533). `medium` ist noch nie gemessen worden.
  - Arm "ohne": **kein** `reasoning`-Parameter. Bedeutung laut OpenRouter und E-021: adaptives Reasoning, abschalten ist nicht möglich ("Reasoning is mandatory for this endpoint").
  - Weggelassen: `temperature` (Anbieter-Standard), `top_p`, `seed`. Gesetzt: `max_tokens = 4000`, `usage.include = true`.
  - `reasoning_tokens` meldet OpenRouter bei Sonnet 5.5 als 0, das Denken ist verborgen. Gemessen wird es deshalb über die **Completion-Tokens** (Antwort plus verborgenes Denken).
- **Prompts (Regel 16):** `dryrun-prompt.md` enthält den exakten Text (Stapel 1, alle 3 Positionen). Er ist in allen Armen identisch, nur der API-Parameter unterscheidet sich.

## Manipulationscheck (Bedingung, Regel 10)
- **Messung:** Median der Completion-Tokens je Aufruf und Arm.
- **Bestanden, wenn:** `low` < `medium` < `high` **und** Median(`high`) ≥ 1,5 × Median(`low`).
- **Scheitert er,** gilt H-037 als **nicht bestätigt**, auch wenn P1 und P2 erfüllt sind. Berichtet wird dann nach dem tatsächlichen Tokenumfang je Arm, nicht nach dem Parameternamen.

## Material-Leckprüfung (Regel 17)
- Manipuliert wird der Prüfer, nicht das Material. Die Frage "Liest der Prüfer die Spur ohne den Faktor?" stellt sich hier nicht, weil jeder Beleg in allen Armen identisch ist.
- Bekannte Lecks im v3.1-Material ("0/20", "0 kB", "mean 100") verringern die Zahl der *Übersehen*-Gelegenheiten. Sie betreffen nicht die Primärmetrik, die auf Ok-Belegen gemessen wird.

## Fremdkontrolle der Ground Truth (Regel 12, D-018)
- **Vor dem Hauptlauf:** `python -m orglab.fremdkontrolle E-022`
- **Prüfer:** `openai/gpt-6.1-sol` über OpenRouter, `reasoning.effort = high`, **je Beleg einzeln**, sieht Auftrag und alle drei Kanäle, keine Fehlerart, keinen Befundtext.
- **Stichprobe:** geschichtet aus genau diesen 288 Belegen: je Domäne und Fehlerart 2 kaputte (24) und je Domäne und Ok-Art 2 Ok-Belege (12), zusammen **36**. Kosten < 1 $.
- **Abweichungen** (anderes Urteil oder "nicht entscheidbar") **klärt Neo von Hand** in `fremdkontrolle.md`. Bei einem Generatorfehler wird **nicht gestartet**: Generator reparieren, Abweichung hier eintragen, neu prüfen.

## Metriken
- **Primär:** Fehlalarmrate auf Ok-Belegen, Kontrast `low` − `high`
- **Analyse-Einheit (Regel 13):** Der **Beleg** ist die Einheit der Rate (Mittel über seine 3 Kanal-Urteile). Die Unsicherheit wird per **Cluster-Bootstrap über Stapel** geschätzt (10.000 Ziehungen), weil Urteile im selben Aufruf zusammenhängen. *Neu gegenüber E-021*, das über Belege gezogen hat.
- **Prävalenz (Regel 14):** PPV der Alarme je Arm bei 50 % und umgewichtet auf 5 %.

## Auswertungsplan
- **P1 (konfirmatorisch):** Δ FA = FA(`low`) − FA(`high`), gepaart je Ok-Beleg. Erfüllt, wenn die untere Grenze des einseitigen 95-%-Intervalls > 0 ist und die Punktschätzung > 0. Relevant ab +0,05.
- **P2 (konfirmatorisch, Nicht-Unterlegenheit):** Δ Übersehen = Miss(`high`) − Miss(`low`), gepaart je kaputtem Beleg. Erfüllt, wenn die obere Grenze des einseitigen 95-%-Intervalls ≤ +0,03 ist.
- **H-037 gilt als bestätigt, wenn P1, P2 und der Manipulationscheck alle erfüllt sind.** Keine Mehrfachkorrektur, weil alle drei gemeinsam Bedingung sind (Intersection-Union).
- **Sekundär (vorab festgelegt, nicht konfirmatorisch):**
  - S1 Dosis: FA, Miss und PPV je Arm mit zweiseitigem 95-%-KI. Erwartung FA(`low`) > FA(`medium`) ≥ FA(`high`).
  - S2: Δ FA (ohne − `high`). Erwartung ≈ 0 (E-021-Probe). Damit wird die Deutung "ohne = adaptiv ≈ high" geprüft.
  - S3: Eskalation bei Konfidenz < 0,80 (Schwelle aus `notizen/20b` §3): Anteil eskaliert und Anteil gefangener Fehler je Arm.
  - S4: Fehlalarm je Domäne.
- **Ausdrücklich nicht ausgewertet:** Zusammenhänge zwischen Tokens und Fehlern *innerhalb* eines Arms. Dort entscheidet das Modell selbst, wie lange es denkt, also ist das mit der Schwierigkeit konfundiert. Höchstens explorativ und dann so markiert.
- **Auswerteskript:** `orglab/e022.py` (`analyze_data`). Vor dem Lauf mit synthetischen Daten getestet (`tests/test_e022.py`, 5 Fälle: Effekt erkannt, Null nicht bestätigt, P2-Verletzung, gescheiterter Manipulationscheck blockiert die Bestätigung, unvollständiger Stapel ausgeschlossen) und mit dieser Präregistrierung committet.
- **Ausschlüsse:**
  - In die Auswertung gehen nur **vollständige Stapel**: jeder Arm an jeder Position mit ≥ 95 % geparsten Urteilen nach bis zu zwei Wiederholungen.
  - **Generatorfehler-Regel:** Ein Ok-Beleg, den alle 4 Arme in allen 3 Kanälen als kaputt beurteilen, wird von Hand geprüft. Ausgeschlossen wird er nur bei nachweislich falscher Ground Truth. Berichtet wird mit und ohne Ausschluss.
- **Transkripte:** 2 zufällige Stapel-Antworten je Arm in `transkripte.md`, Pflichtlektüre für Neo.

## Externe Kritik (Regel 18)
- Geschätzte Kosten unter 10 $ (Abbruch bei 10 $), keine neue Kernthese (Replikation von H-037 mit gemessener Manipulation). **Kein externes Gutachten vorgesehen.** Kritiker-Unabhängigkeit bleibt offen: Design, Material und Prüfer sind Claude, nur die Ground-Truth-Kontrolle ist GPT.

## Abbruchkriterien
- Kosten des Experiments > 10 $ → Abbruch (im Code, `COST_STOP`). Berichtbar sind dann die vollständigen Stapel. Unter 16 vollständigen Stapeln wird nur deskriptiv berichtet, nicht konfirmatorisch.
- Fehlen nach den Wiederholungen > 5 % der Urteile eines Arms → Abbruch, Pipeline reparieren.
- Lehnt OpenRouter `medium` ab (Fehler statt Antwort) → Abbruch nach dem ersten Stapel, Abweichung dokumentieren.

## Offene Schwächen
- Das Material ist synthetisch (v3.1), Stapel 12, nur Sonnet 5.5 über OpenRouter. Wave-Prüfer arbeiten anders.
- Was `effort` beim Anbieter genau steuert (Budget, Stil, Modellvariante?), ist nicht dokumentiert. Gemessen werden nur Tokens.
- Ein Teil der Fehlalarme könnte begründete Vorsicht sein, weil die Ground Truth "Rauschen ist ok" eine Definition des Generators ist (Grok-Gutachten 1 §4b). Die Fremdkontrolle prüft das nur stichprobenartig.
- Der Ledger-Eintrag von `judge_batch` trägt weiterhin den Zweck "E-019-stapel-panel …", weil der Aufrufcode unverändert bleibt. Die Kosten von E-022 stehen in `calls.jsonl`.

## Abweichungen (nach Start)
- **23.10., 08:49, vor dem Lauf (keine Abweichung, nur Protokoll):**
  - Fremdkontrolle gelaufen (`fremdkontrolle.md`, `notizen/29` §1): 33 von 36 stimmen überein, 3 Belege sind "nicht entscheidbar".
    - `bounced` nach 71 h Warteschlange
    - zweimal Prüferstrenge bei Research-Ok-Belegen
  - Claude sieht darin keinen Generatorfehler, Neo hat zugestimmt und den Lauf freigegeben ("klar kannst starten").
  - Präzisierung zu Regel 11: Der Fremdprüfer denkt bei `effort: high` tatsächlich nur ~120 Reasoning-Tokens je Beleg (`notizen/29` §5).
  - Code von `orglab/e022.py`, `batch.py`, `evidence.py`, `factorial.py` und `openrouter.py` seit der Präregistrierung (9891133) unverändert (`git diff` leer).
