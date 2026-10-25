# Externes Gutachten 3: Grok zu E-020 v3 (vor dem Hauptlauf, Regel 18)

- **Datum:** 2026-10-23 13:18, ein einziger Aufruf
- **Aufruf:** Grok Build CLI 1.0.62, `-m grok-4.7`
  - Plan-Modus, `--disable-web-search`, `--no-subagents`
  - gesperrte Werkzeuge: Shell, Schreiben, Web, Subagenten
  - leerer Kopie-Ordner ohne Secrets und Rohdaten, `GROK_FOLDER_TRUST=0`
  - Laut Debug-Log liefen die Antworten überwiegend über `grok-4.7-build` (einmal `grok-4.6-build`).
  - Keine Datei der Kopie wurde verändert.
- **Material:** `prereg-v3.md`, `dryrun-v3.md`, `pilot-v3-bericht.md`, `lecktest.md`, `fremdkontrolle.md`, `orglab/e020v3.py`, `evidence_v4.py`, `evidence.py`, Tests, frühere Gutachten, `notizen/29`

## Einordnung durch Claude

| Punkt | Einordnung | Konsequenz |
|---|---|---|
| **Seitenbasierte Suche = Antwortschlüssel:** Der Einheitenname steht im Kurzauftrag, die Seite liefert die Norm als beschrifteten Einzeiler (28/28). SPEC trennt nur noch "Norm im Auftrag" von "Norm eine Abfrage entfernt". V1 misst die Decke. | **berechtigt, wichtigster Punkt.** Der Fix gegen die starre Suche ist ins andere Extrem gekippt. | Realistischere Seiten: länger, mit mehreren gleich aussehenden Werten (andere Umgebungen, Vorjahr, andere Dienste), sodass "nachgeschlagen" und "Norm richtig gelesen" auseinanderfallen. **Schwelle +0,10 bleibt, Pilot-2-Raten bleiben versiegelt.** |
| **Entscheidungsregel, Power und Skript widersprechen sich:** "gestützt" verlangt Schätzung ≥ +0,10, die Power-Angabe gilt aber nur für "untere Grenze > 0". "Widerlegt" verlangt obere Grenze < +0,02. Kein Alpha, q geht in nichts ein, Tests nur bei +0,30/+0,15. | **berechtigt, mein Fehler.** | Eine kohärente Regel: Effekt nachgewiesen = untere Grenze > 0 (einseitig α 0,025). +0,10 ausgeschlossen = obere Grenze < +0,10. Praktisch null = obere Grenze < +0,02. Power-Simulation in den Code, Tests genau an den Schwellen. |
| V2 mittelt auch über Fehlerarten, deren Widerspruch im Auftrag oder Beleg steht. "Gestützt" verlangt keinen Rückgang der Fehlalarme. | teilweise berechtigt. V2 war absichtlich über alle kaputten Belege definiert. | V2 bleibt wie vorgesehen, zusätzlich sekundär V2 nur auf spec-reinen Belegen. Die Fehlalarm-Nebenvorhersage wird als eigener Punkt berichtet. |
| V4 im Skript misst noch "richtiger Abschnitt", definiert ist jetzt "Seite oder Abschnitt", beides ist nicht trennbar. | berechtigt | zwei Felder: Seite getroffen, Normabschnitt getroffen |
| **`low_traffic`:** Uptime 60–95 s bei "letzte 60 s"-Zähler, kleine absolute Zahlen (Grenzfall 6021). Code-Lecktest auf anderen Seeds. Der GPT-Lecktest deckt nur 42 von 84 Primärbelegen. | berechtigt | Uptime deutlich über dem Zählerfenster, keine Zähler im Bereich eigener Sonden. Danach nur diese Art neu leckprüfen, der Code-Lecktest läuft zusätzlich auf den Hauptlauf-Seeds. |
| **Normtext ungleich:** "±20 %" und "connects to all shards" stehen nur im Runbook, nicht im langen Auftrag | **berechtigt, echte Konfundierung** (SPEC=0 und SPEC=1 hätten verschieden viel Information) | Normtext in Auftrag und Runbook angleichen, mit Test |
| Teilwortsuche ohne Wortgrenze ("port" in "report") | berechtigt, klein | Wortgrenzen |
| Pilotkriterium "5 Transkripte gelesen" nicht abgehakt | **berechtigt** | nachholen |
| Der Pilotbericht schreibt schon die Lesart "großer SPEC-Effekt unwahrscheinlich" fest (aus n = 24) | berechtigt, das war voreilig | im Bericht als Erwartung ohne Gewicht kennzeichnen |

**Empfehlung Grok:** Hauptlauf erst nach der Runbook-Änderung, dann ein kurzer technischer Pilot auf **frischen** Seeds, danach der Hauptlauf mit unveränderter Schwelle +0,10 und einer Entscheidungsregel, die dasselbe meint wie die Power-Angaben. "Gar nicht starten wäre zu viel": V2, V3 und ein SPEC, bei dem Nachschlagen Arbeit ist, tragen die Projektfrage noch.

## Das Gutachten (wörtlich)

Ich lese zuerst `AUFTRAG.md` und halte mich danach genau an den Auftrag.Der Auftrag ist ein reines Lesegutachten zu Fassung 3. Ich lese die früheren Gutachten und die genannten Dateien.Die Präregistrierung und die Pilotberichte sind gelesen. Als Nächstes prüfe ich Auswerteskript, Generator und Tests gegen den Wortlaut.**Empfehlung: Hauptlauf erst nach einer Änderung am Runbook.** V2 und V3 wären schon jetzt informativ. V1, die teure Primärfrage, misst in dieser Fassung fast nur die Decke.

## 1. Frühere Punkte

- Anstupser und der Halbsatz „what you can look up“: behoben. Prompt ohne diese Sätze, Test dagegen (`prereg-v3.md` 17; `dryrun-v3.md` 5–45; `tests/test_e020v3.py` 11–21).
- Prompt nur im Code: behoben. Alle acht Zellen stehen wörtlich in `dryrun-v3.md`.
- Werkzeug nur bei SPEC=1: behoben. `lookup_runbook` in allen Zellen, `run_check` nur bei ZUGANG=1 (`e020v3.py` 61–74; Test 28–33).
- Themenliste bei unbekanntem Topic: behoben. Unbekannt ergibt „No entry“ (`evidence_v4.py` 120; Test `test_runbook_unknown_topic_reveals_nothing`).
- Runbook als ganzer Schlüssel auf einen Aufruf: teilweise. Stichwort liefert nur den Abschnitt. Seit der Abweichung liefert der Einheitenname wieder die ganze Seite (`prereg-v3.md` 107–112; `evidence_v4.py` 113–118).
- Lecks und die drei alten „spec-reinen“ Arten: behoben für die sieben neuen Arten. Lecktest 0/42 sicher erkannt (`lecktest.md` 6–16; `notizen/29` §4).
- V6 und die Stufe der Nicht-Unterlegenheit: behoben durch Streichung. H-036 ist draußen (`prereg-v3.md` 7).
- Kanal = Seed mod 3, nicht nach Fehlerart: behoben (`e020v3.py` 57–58; `tests/test_e020v3.py` 36–40).
- Auswerteskript: teilweise. Es existiert und ist an synthetischen Daten getestet. Entscheidungsregel, V2 und V4 weichen vom Text ab, siehe unten.
- Abbruch mit halben Seeds: teilweise. Die Warteschlange ist nach Seed sortiert, `cancel_futures=True` bricht Nicht-Gestartetes ab. Es gibt keine Sperre „Seed n fertig, bevor Seed n+1 beginnt“ (`e020v3.py` 168–190).
- Analyse-Einheit Urteil: behoben. Einheit ist der Beleg, gepaarte Differenz, Bootstrap über Belege (`e020v3.py` 230–246).
- Primärmenge ~36 und Power: teilweise. 84 spec-reine kaputte Belege (`prereg-v3.md` 18). Die Powerzahl passt nicht zum Etikett „gestützt“.
- Ground-Truth-Stapel: behoben. GPT einzeln, geschichtet, ohne Befundtext, 47/48 (`fremdkontrolle.md` 3–5).
- Grenzfall `coding-fail_moderate-6021`: teilweise. Bleibt drin, eine Sensitivität ohne ihn ist vorab festgelegt (`prereg-v3.md` 42, 106). Die Klärungsspalte in `fremdkontrolle.md` 16 ist leer.
- V5-Schwellen 0,80 und 0,85: behoben. 0,80 ist die Eskalation, ≥ 0,85 die konfidenten Fehler, beides deskriptiv (`e020v3.py` 47, 313–320).
- „Fangquote“ aus 20b: behoben. Die V5-Spalte ist der Anteil gefangener Fehler, die PPV bei 5 % steht in der Zellentabelle (`e020v3.py` 319, 328–331).
- Reasoning-Befund: behoben durch Auslagerung, kein Faktor mehr (`prereg-v3.md` 7, 23–24).
- Mehrdeutigkeit per Design draußen: nicht behoben. Weiter eine boolesche Generator-Wahrheit. `low_traffic` bleibt auch mit Norm angreifbar.
- Mindestumfang 16 Seeds: behoben. Darunter nur deskriptiv (`e020v3.py` 49, 273–279; Test 85–89).
- Pilotkriterium „Werkzeug einmal benutzt“: teilweise. Die Anstupser sind weg. Die Latte bleibt niedrig. Pilot 2 zeigt 83–100 % Nachschlagen (`pilot-v3-bericht.md` 29).
- These, Literatur, Wave-Policy, naive Baseline: nicht Gegenstand dieser Präregistrierung.

## 2. Neue Probleme

**Hoch — die seitenbasierte Suche ist der Antwortschlüssel.** Nennt das Topic den Dienst, „invoice“, die Rechnungs- oder Kundennummer, die Datensatz-ID, „survey“ oder „dataset“, kommt die ganze Seite zurück, jede Normzeile inklusive Distraktoren (`evidence_v4.py` 102–120). Diese Wörter stehen im Kurzauftrag. `right_section` wird wahr, sobald die Seite irgendeine Überschrift `[traffic]`, `[payment]`, `[schema]` enthält (`e020v3.py` 147–151). Pilot 2: bei SPEC=1 kam der Normwert in 28 von 28 nachgeschlagenen spec-reinen Prüfungen zurück (`pilot-v3-bericht.md` 29–30). SPEC trennt damit „Norm im Auftrag“ von „Norm eine Abfrage entfernt, als beschriftete Kurzliste“.

**Hoch — Entscheidungsregel, Power und Skript sagen dreierlei.** „Gestützt“ heißt: Schätzung ≥ +0,10 und untere Grenze > 0 (`e020v3.py` 287–292). Bei einem wahren Effekt von genau +0,10 liegt eine unverzerrte Schätzung nur etwa zur Hälfte darüber. Die angegebene Power „bei +0,10 etwa 1,0“ und „bei +0,05 etwa 0,75“ (`prereg-v3.md` 63–66) passt zur schwächeren Frage, ob die untere Grenze über 0 liegt. „Widerlegt“ verlangt eine Obergrenze unter +0,02. Ein Intervall, das +0,10 ausschließt und über +0,02 endet, heißt im Skript „nicht entschieden“. Der Satz, ein Nullergebnis schließe Effekte ab +0,10 aus (`prereg-v3.md` 66; `pilot-v3-bericht.md` 34), ist dieses dritte Kriterium. Eine Power-Simulation steht in `e020v3.py` nicht. q aus dem BH-Verfahren wird berichtet und geht in kein Etikett ein. Ein Alpha fehlt (`e020v3.py` 285–294). Die Tests prüfen Effekte von +0,30 und +0,15 (`tests/test_e020v3.py` 65–72), nicht die Schwellen +0,10 und +0,02.

**Mittel — V2 und V4.** V2 mittelt über alle kaputten Belege, also auch über `bounced`, `db_down` (`0/20`), `stale_process` und `amount_mismatch`, deren Widerspruch im Auftrag oder im Beleg steht (`evidence_v4.py` 36–41; `prereg-v3.md` 53). „Gestützt“ verlangt den Rückgang der Fehlalarme nicht mit (`e020v3.py` 293–296). V4 ist im Skript weiter „richtigen Abschnitt nachgeschlagen“ (`e020v3.py` 307–312). Die Abweichung hat V4 auf „Seite oder richtiger Abschnitt“ umdefiniert (`prereg-v3.md` 112). Seite und Abschnitt sind im Feld nicht trennbar.

**Mittel — `low_traffic`.** Uptime 60–95 s, Zähler „last 60 s“, kaputte Last ab 2, übliche Last ab 10/min (`evidence_v4.py` 145–154). In der Fremdkontrolle ist `…-6021` auch mit Norm „2 Requests gegen ~20/min, vielleicht nur lokale Sonden“, Uptime 67 s (`fremdkontrolle.md` 10–16, 31–37). Die Sensitivität streicht nur diesen einen Beleg. Dieselbe Bauart erzeugt weitere kleine absolute Zähler. Der Code-Lecktest prüft die Rate-Norm nicht in den Kanälen (`tests/test_evidence_v4.py` 68–74) und läuft auf Seeds 9000–9048, nicht auf 6000–6023. Der GPT-Lecktest deckt 42 der 84 Primärbelege.

**Niedrig.** Teilwortsuche ohne Wortgrenze: `"port" in "report"`, dazu `"log"`, `"pay"`, `"db"` (`evidence_v4.py` 58–72, 119). „±20 %“ und „connects to all shards“ stehen nur im Runbook, nicht im langen Auftrag (`evidence_v4.py` 148–150 gegen 263–264). Das Pilotkriterium „fünf Transkripte“ ist im Pilotbericht nicht abgehakt. Die Begründung „Belege sind unabhängig, weil jede Prüfung ein eigener Aufruf ist“ (`prereg-v3.md` 46) verwechselt Aufruf und Beleg. Das Skript bildet erst die Differenz innerhalb des Belegs und bootstrapt dann Belege. Das ist die richtige Einheit.

Die sieben Primärarten sind im Übrigen sauberer als v3: überlappende Verteilungen, keine `0/N`-Marker, `wrong_terms` statt fehlendem PDF, 0 von 42 sicheren Treffern ohne Sollwert.

## 3. Decke

Für SPEC ja. H-033 bündelt Effekt und Mechanismus: fehlender Sollwert, weil nicht nachgeschlagen wird (`prereg-v3.md` 7). Der Mechanismus ist unter dieser Suche nicht mehr die Hypothese. Pilot 2 schlägt auch bei SPEC=0 in 83–100 % nach, bei SPEC=1 immer, und die Norm kam vollständig zurück. Wer den Dienstnamen schickt, hat dieselben Sätze wie im langen Auftrag, nur als Seite mit sieben Zeilen. Ein Null bei V1 widerlegt dann „ein Orakel-Runbook erhöht das Übersehen um mindestens 0,10“. Es beantwortet nicht „fehlt der Sollwert?“ und nicht „schlagen Prüfer nicht nach?“. Die Abweichung schreibt diese Lesart schon fest: ein großer SPEC-Effekt sei unwahrscheinlich, V1 könne widerlegt werden (`prereg-v3.md` 110–114; `pilot-v3-bericht.md` 33–35), aus n = 24.

V2 und V3 hängen nicht an dieser Suche. Selbstauskunft kann das Übersehen erhöhen und `run_check` senken, auch wenn die Norm erreichbar ist.

Änderung, ohne die Schwellen an die Übersehensraten aus Pilot 2 anzupassen: Die Seite zur Einheit darf auf den Dienst-, Rechnungs- oder Datensatznamen kommen. Das war der berechtigte Fix gegen „SPEC misst eine kaputte Suche“. Die Seite muss aufhören, die Norm als beschriftete Einzeiler zu liefern. „Nachgeschlagen“ und „Norm gelesen“ müssen auseinanderfallen, über Länge und gleich aussehende Konventionen. V1 bleibt bei +0,10. Die Raten 4–8 % aus Pilot 2 bleiben versiegelt und gehen nicht in eine neue Vorhersage. Dieselbe Revision sollte den Normtext in Auftrag und Runbook angleichen und bei `low_traffic` die erste Minute als Alternative ausschließen (Uptime deutlich über das Zählerfenster, oder keine absoluten Zähler im Sondenbereich), danach nur diese Art neu leckprüfen.

## 4. Empfehlung

Erst nach dieser Änderung am Runbook, dann ein kurzer technischer Pilot auf frischen Seeds, der prüft, dass die Norm nicht mehr in 28 von 28 Seitenantworten liegt. Danach der Hauptlauf mit unveränderter Schwelle +0,10 und einer Entscheidungsregel, die dasselbe meint wie die Power-Sätze.

Jetzt starten hieße etwa 25–35 $ dafür ausgeben, eine Informationsequivalenz zu bestätigen, die der Manipulationscheck schon gezeigt hat. Gar nicht starten wäre zu viel: V2, V3 und ein SPEC, bei dem Nachschlagen Arbeit ist, tragen die Projektfrage noch.
