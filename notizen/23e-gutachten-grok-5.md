# Externes Gutachten 5: Grok zu E-024 (Bestätigungslauf, vor dem Hauptlauf, Regel 18)

- **Datum:** 2026-10-23 19:41, ein einziger Aufruf
- **Aufruf:** Grok Build CLI 1.0.62, `-m grok-4.7` (Debug-Log: grok-4.7), Plan-Modus, Web und Subagenten aus, Shell und Schreiben gesperrt, leerer Kopie-Ordner ohne Secrets, `GROK_FOLDER_TRUST=0`. Prüfsummen vorher und nachher gleich.
- **Material:** E-024 prereg, `e024.py`, `e020v3.py`, `evidence_v4.py`, Tests, Fremdkontrolle, Einzelkanal, Lecktest, Ergebnisse E-020/E-023, prereg E-023, Gutachten 4.

## Einordnung durch Claude

| Punkt | Einordnung | Konsequenz |
|---|---|---|
| **Etiketten im Skript widersprechen der Präregistrierung** ("nachgewiesen, aber kleiner" hieße "widerlegt"; F1-Null hieße "widerlegt") und würden vor dem Entblinden festgeschrieben | **berechtigt, hoch, mein Fehler** | eigene Funktion `e024.label`, Tests an den Grenzen |
| Fehlende Ausschlussdatei → F1 still über alle Ok-Belege | berechtigt | bricht jetzt ab, mit Test |
| Manipulationscheck erst nach dem Entblinden | berechtigt | jetzt in `analyze_blind`, Test für den Fall "gescheitert" |
| Sekundäranalyse entfernt die 62 auch aus C1 | berechtigt, klein | C1 bleibt auf allen Belegen |
| Power bildet die F1-Einschränkung nicht ab | berechtigt | neu gerechnet: F1 0,3 |
| C2 mit +0,10 gegen entdeckte +0,40 "weich" | Absicht, Schrumpfung erwartet | bleibt, "kleiner als vorhergesagt" wird mit Größe berichtet |
| Alternativerklärung C1/C2: Schaden hängt am fehlenden Sollwert (bei SPEC = 0 senkt Zugang das Übersehen) | **berechtigt, wichtig für die Deutung** | Diagnose ZUGANG bei SPEC = 0 je Modell (deskriptiv), dazu Rundengrenze aus den Transkripten |
| Modellspezifität von H-039 steht nur in der Sonnet-Spalte | berechtigt | Satz in der Präregistrierung |
| Klärungszeile 7009 leer | berechtigt | nachgetragen |
| Empfehlung: "erst die kleine Code-Änderung, danach sofort starten, kein neues Material, kein neuer Pilot" | – | umgesetzt, dann Start |

## Das Gutachten (wörtlich)

Ich lese zuerst `AUFTRAG.md` und schaue mir den Ordner an, damit ich den Auftrag genau umsetzen kann.Der Auftrag ist ein reines Lese-Gutachten. Ich lese Präregistrierung, Code, Tests und die Vorläufe, bevor ich bewerte.Die Präregistrierung ist klar. Als Nächstes prüfe ich, ob Auswertung, Paarung und die E-023-Definitionen dazu passen.**Empfehlung: noch nicht starten.** Erst eine kleine Änderung an `orglab/e024.py` (Punkt 2), danach sofort. Kein neues Material, kein neuer Pilot.

### 1. Präregistrierung — mittel

V1, W1, C1, C2 und F1 sind gerichtet und vor den Modelldaten festgeschrieben (`experimente/prereg.md` 33–42). V1 behält die Schwelle +0,10 aus E-023; dort war der Befund +0,253 (`experimente/E-023-ergebnis.md` 33, `experimente/E-023-prereg.md` 59). W1 ist mit ≥ +0,10 schärfer als in E-023, wo nur „> 0“ galt (`experimente/E-023-prereg.md` 68). C1 und C2 aus dem explorativen Abschnitt hier als Bestätigung zu prüfen, ist legitim: Seeds 7000–7023 sind frisch (`experimente/prereg.md` 21), Richtung und Kontrast stehen fest. C2 ist die dortige Differenz Übersehen bei ZUGANG 1 − 0 auf spec-reinen Belegen mit SPEC = 1; C1 ist dieselbe Differenz fürs Nachschlagen, auf alle Belege bei SPEC = 1 verbreitert (Rauchtest +0,42 / +0,40, `experimente/prereg.md` 108; Zellen `experimente/E-023-ergebnis.md` 64–67).

V1, W1 und C1 liegen bei etwa der Hälfte der Entdeckung und sind vernünftig (`experimente/prereg.md` 34–40). C2 mit +0,10 gegen entdeckte +0,404 ist weich. F1 mit +0,02 liegt auf der Grenze von „praktisch null“ (`experimente/prereg.md` 41, 50). Nach der Materialprüfung gilt F1 nur noch für 101 von 144 Ok-Belegen. Die E-023-Zahl +0,042 auf allen Ok-Belegen bleibt deskriptiv (`experimente/prereg.md` 97). Die Power, dort „gestützt“ zu treffen, ist 0,37 (`experimente/prereg.md` 59). `e024.power` bildet diese Einschränkung nicht ab (`orglab/e024.py` 266–277).

### 2. Code — hoch

Paarung, Vollständigkeit, BH, Vorzeichen und beide Blind-Zuordnungen tun, was die Präregistrierung sagt. Es gilt der letzte Datensatz je Arm, Beleg und Zelle; ein Seed zählt nur, wenn er in jedem Arm 12 × 8 Urteile hat (`orglab/e024.py` 93–102, `orglab/e020v3.py` 225–230). W1 ist die Differenz der V1-Werte auf gemeinsamen Belegen (`orglab/e024.py` 146–147). BH läuft über alle fünf einseitigen p-Werte (`orglab/e024.py` 149–155). C1 ist Nachschlagen ZUGANG 0 − 1, C2 Übersehen ZUGANG 1 − 0 (`orglab/e024.py` 127–131). F1 nimmt nur Ok-Belege außerhalb der Ausschlussliste (`orglab/e024.py` 123–133). Die verblindete Auswertung rechnet beide Zuordnungen (`orglab/e024.py` 189–196); unter 16 Seeds bleibt alles deskriptiv (`orglab/e024.py` 182–188). Die Tests prüfen Seeds, Null, A/B, den F1-Stichprobenumfang und die Länge 62 (`tests/test_e024.py` 14–68). Bootstrap-Indizes stimmen mit `experimente/prereg.md` 110 überein (`orglab/e020v3.py` 242–249).

Die Etiketten, die vor dem Entblinden nach `auswertung-verblindet.md` gehen (`experimente/prereg.md` 125), widersprechen dem Text:

- `classify` nennt „nachgewiesen, obere Grenze unter dem Vorhersagewert“ ausdrücklich „Vorhersage widerlegt“ (`orglab/e020v3.py` 275–276). Satz 51 der Präregistrierung zählt denselben Fall als bestätigt.
- Liegt die obere Grenze unter +0,02 oder unter dem Vorhersagewert, hängt dieselbe Funktion „widerlegt“ an (`orglab/e020v3.py` 277–280). Bei F1 ist der Vorhersagewert +0,02, und ein Null-Ergebnis soll „nicht bestätigt“ heißen (`experimente/prereg.md` 60). Eine F1-Ausnahme gibt es im Skript nicht. `test_null_not_supported` lässt dieses Wort durch (`tests/test_e024.py` 28–32).
- Fehlt `einzelkanal-ausschluss.json`, wird die Ausschlussmenge leer (`orglab/e024.py` 173–175). F1 läuft dann über alle Ok-Belege und bekommt trotzdem ein Entscheidungsetikett.
- „Scheitert der Manipulationscheck, nur deskriptiv“ (`experimente/prereg.md` 63–67) steht in `analyze` nach dem Entblinden (`orglab/e024.py` 225–232), nicht in `analyze_blind`. `n_checks` bleibt in den verblindeten Daten (`experimente/prereg.md` 123).

### 3. Material — mittel

Unverändertes v4.3, F1 nur auf entscheidbaren Ok-Belegen, Sekundäranalyse ohne die 62: vertretbar. 62 von 288 sind einzeln nicht entscheidbar, 43 von 144 Ok-Belege, nur 7 von 84 spec-rein (`experimente/prereg.md` 84–90, `experimente/fremdkontrolle-einzelkanal.md` 5). V1, W1 und C2 hängen an spec-reinen kaputten Belegen, C1 an `looked_up`. Ein „kaputt“ ohne belegbaren Erfolg ist kein klarer Fehlalarm (`experimente/prereg.md` 91–97).

Was dabei leicht aus dem Blick gerät: Der Generator sagt, jeder Kanal sei mit Norm allein entscheidbar (`orglab/evidence_v4.py` 11–12). Die Kontrolle zeigt das Gegenteil vor allem bei Ok-Belegen. Die E-023-Fehlalarme saßen fast nur bei verrauschten Ok-Belegen mit einem Kanal (`experimente/E-023-ergebnis.md` 107), und genau die sind überrepräsentiert (28 von 48 Coding-Ok, 15 von 48 Research, `experimente/prereg.md` 85–86). F1 prüft damit eine engere Population. Die Wiederholung von +0,042 ist nur die deskriptive Zeile. Auch die 101 „klaren“ Ok-Belege sind klar für GPT mit Sollwert; F1 mittelt über SPEC (`experimente/prereg.md` 41), und bei SPEC = 1 fehlt der Maßstab im Auftrag. `coding-ok_clear-7009` ist ein Ok-Beleg (`experimente/prereg.md` 79); die Sensitivität ohne ihn (`orglab/e024.py` 45, 195–196) lässt V1, W1 und C2 unverändert. Mit allen Kanälen urteilt GPT dort entscheidbar und „funktioniert nicht“ (`experimente/fremdkontrolle.md` 12–13); die Klärungszeile ist leer (`experimente/fremdkontrolle.md` 17). Die Sekundäranalyse entfernt dieselben 62 auch aus C1 (`orglab/e024.py` 193–194), obwohl Nachschlagen dort kein Wahrheitsurteil ist.

### 4. Deutung — mittel

C1 und C2 entstehen plausibel, weil drei übereinstimmende Kanäle wie ein Beleg wirken und der Maßstab im Runbook bleibt (`experimente/E-023-ergebnis.md` 100–104). In derselben Zelltafel fällt bei SPEC = 0 das Übersehen, obwohl seltener nachgeschlagen wird (SP0-ZU1: Übersehen 0,007 und 0,000, `experimente/E-023-ergebnis.md` 61–62). Der Schaden hängt am fehlenden Sollwert. Diesen ZUGANG-Kontrast bei SPEC = 0 hat die Präregistrierung nicht als Diagnose, und `analyze` schneidet die Zelltabelle ab (`orglab/e024.py` 234–236). Die Rundenobergrenze 6 (`orglab/e020v3.py` 38) ist die schwächere Alternative; berichtenswert ist der Anteil der Nicht-Nachschläge mit voller Rundenzahl.

H-039 spricht von schwächeren Prüfern (`experimente/prereg.md` 10). Das Etikett bestätigt den Haiku-Kontrast. Die Modellspezifität steht in der deskriptiven Sonnet-Spalte (`experimente/prereg.md` 53). V1, W1 und C2 teilen sich die Zelle SPEC = 1 × ZUGANG = 1.

Ein bestätigtes V1 oder W1 heißt: der Sollwert-Befund aus E-023 wiederholt sich auf neuen Seeds in dieser Familie (`experimente/prereg.md` 15–16). C1 ohne C2 heißt: seltener nachgeschlagen, Schaden offen. C2 ohne C1 heißt: mehr Übersehen aus einem anderen Grund. Ein F1-Null heißt: der engere Claim auf 101 Belegen ist nicht bestätigt (`experimente/prereg.md` 60). Ein V1-Null heißt: die Entdeckung wiederholt sich nicht.

### 5. Empfehlung — hoch

Vor dem Start, sonst wird die verblindete Datei mit dem falschen Entscheid festgeschrieben:

1. In `e024.evaluate` die Etiketten auf `experimente/prereg.md` 46–51 und 60 abbilden. „Nachgewiesen, aber kleiner“ ohne das Wort „widerlegt“. F1 ohne Nachweis: „nicht bestätigt“.
2. Fehlende Ausschlussdatei bricht ab (`orglab/e024.py` 173–175).
3. `analyze_blind` weist `run_check` im Mittel ≥ 1 und die Ausfälle je Zelle aus und setzt bei Scheitern deskriptiv (`experimente/prereg.md` 63–67).

Dazu ein Satz in der Präregistrierung: Sonnet-C1 und Sonnet-C2 nahe 0 tragen die Lesart „nur schwächere Prüfer“; der ZUGANG-Effekt auf das Übersehen bei SPEC = 0 ist Diagnose, ohne sechstes BH. Danach sind die etwa 36 $ der richtige nächste Schritt.
