# Externes Gutachten 2: Grok zum E-020-Überarbeitungsentwurf

> **Korrektur 23.10. (E-021, Manipulationscheck):** Was hier "Reasoning aus" heißt, war in Wahrheit die **Standardeinstellung mit adaptivem, verborgenem Reasoning** (OpenRouter: Reasoning ist bei Sonnet 5.5 nicht abschaltbar). "Reasoning low" war **gedrosseltes** Reasoning. Alle Aussagen "Reasoning erhöht Fehlalarme" sind deshalb umzudrehen: **Gedrosseltes Reasoning erhöht Fehlalarme** (H-037). Details: `experimente/E-021-reasoning-fehlalarme/ergebnis.md`.

- **Datum:** 23.10.2026, nachts
- **Aufruf:** ein einziger Grok-CLI-Aufruf (Limit-schonend), `-m grok-4.7`, Plan-Modus, ohne Gedächtnis, Web und Subagenten
- **Material:** Kopie mit dem früheren Gutachten, `prereg-v1`, `prereg-v2-entwurf`, `notizen/20b`, `notizen/27`, `realitaet.py`, `evidence.py`

## Einordnung durch Claude

| Punkt | Einordnung | Konsequenz |
|---|---|---|
| Meine drei "spec-reinen" Fehlerarten sind nicht rein (`0 kB`/`0 pages`, `mean 100`, `requests: 0` sind auch ohne Sollwert verdächtig) | **berechtigt, mein Fehler** | Generator v4: Spuren so bauen, dass sie *ohne* Norm plausibel aussehen (z. B. Last 3 statt 0, Anhang 2 kB ohne "0", Gewichtsmittel 1,4 statt 100). Ein Test verbietet Konventions-Lecks. |
| Die Themenliste bei unbekanntem Topic verrät, welche Sollwerte existieren; V4 bleibt Selbstselektion | berechtigt | Bei unbekanntem Topic "kein Eintrag" statt Themenliste. V4 bleibt deskriptiv. |
| Blöcke je Seed brauchen eine echte Umstellung des Executors (alle Jobs gehen auf einmal raus) | berechtigt | Executor seedweise abarbeiten |
| Primärmenge nur ~36 kaputte Belege bei unveränderten Schwellen | berechtigt (Power) | mehr Seeds für die Primärarten oder Schwellen begründet anpassen, vor dem Pilot |
| Ground-Truth-Kontrolle als Stapel ist ungeeignet (Fehlalarme im Stapel ~0,16) | berechtigt | Zweitmodell je Beleg einzeln, geschichtet auf die Primärarten, ohne Befundtext |
| V5-Schwelle 0,85 gegen 0,80 in der Neuberechnung | berechtigt | Schwelle vorab aus Daten ohne E-020 festlegen (0,80 aus v2) |
| 20b §5: "gefangene Fehler" steigt bei 5 % Prävalenz, das ist keine Sensitivität | **berechtigt**, die Spalte war missverständlich benannt | 20b korrigiert: Die Spalte ist der Anteil *aller* Fehler (inklusive Fehlalarme) und verschiebt sich mit der Zusammensetzung. Die maßgebliche Zahl ist die PPV. |
| **Der einzige robuste Befund (Reasoning → Fehlalarme im Stapel) wird geparkt** | **berechtigt.** Ein eigener Bestätigungstest ist billig | Vorschlag **E-021**: präregistrierte Bestätigung auf frischen Seeds, Stapel 12, low gegen aus, gepaart. ~2 $. |
| Naive Baseline: Die These "Stringvergleich" fällt in dieser Breite. Bei Leck-Markern schlägt B2 Sonnet aber (`empty_attachment`) | angenommen | wie in `notizen/27` |

## Das Gutachten (wörtlich)

Ich lese das frühere Gutachten, den Überarbeitungsentwurf und die beiden neuen Auswertungen, ohne etwas zu ändern.Bewertet ist der Entwurf. `realitaet.py` und `evidence.py` sind unverändert.

## 1. §5

- **Anstupser, Prompt nur im Code, leeres Pilotkriterium:** behoben. Alle drei Sätze sollen weg, alle 16 Texte wörtlich eingefroren werden. Die Texte stehen in diesem Entwurf noch nicht.
- **Runbook = ganzer Schlüssel:** teilweise. Abschnitte beheben den einen Aufruf. Die Themenliste bei unbekanntem Topic ist ein Inhaltsverzeichnis der Sollwerte. V4 bleibt Selbstselektion; „wird interpretierbar“ ist zu stark.
- **Werkzeug nur bei SPEC=1:** behoben. Offen, ob das Runbook in beiden Stufen derselbe Text ist.
- **Lecks, Primärmetrik über strukturelle Nullen:** teilweise. `column_loss`, `cache_down`, `db_down`, `duplicates_kept` aus der Primärmenge zu nehmen, trifft `/47`, `0/4`, `0/20` und „unique < n bei dropped 0“. Die drei „spec-reinen“ Arten sind es im Quelltext nicht: `empty_attachment` hat `0 kB` und `0 pages` (der Entwurf streicht nur die Anhanggröße), `weights_broken` zeigt im kaputten Pfad `mean 100.4` und `sum of weights / n: 100.38`, keine „/1“-Zeile, `zero_traffic` zeigt `requests …: 0` ohne die Rate.
- **V6 anderer Estimand:** behoben. Umgeschrieben auf Einzelbelege, Stapel ausdrücklich geparkt.
- **Nicht-Unterlegenheit ohne Stufe:** behoben. Einseitig 95 % = zweiseitiges 90-%-KI, Grenze +0,03; das ist dieselbe Schranke.
- **Auswerteskript:** teilweise. Zusage, es vor dem Pilot zu committen. Die Inhaltsliste nennt Primärmenge, vollständige Blöcke und „richtiger Abschnitt“ nicht.
- **Abbruch, Kosten:** teilweise. Blöcke je Seed beheben halbe Zellen. 30–50 $ bei bis zu sechs Runden bleiben stehen. Ein Seed enthält die drei Primärarten nur zufällig. Der Executor schickt alle Jobs auf einmal (`as_completed`); ohne echte Umstellung der Reihenfolge gibt es beim Stopp kaum vollständige Seeds.
- **Kanal = Seed mod 3:** behoben. Je Fehlerart zu balancieren, ist die richtige Stelle.
- **Ground Truth hart, Mehrdeutigkeit per Design draußen:** nicht.

Prävalenz und Zweitbewertung sind §3 und §6. Die 5-%-Umgewichtung als Zusatzbericht ist richtig. Die 30er-Stichprobe beantwortet die Zweitbewertung nur der Form nach.

## 2. Neue Probleme

Die Wortlaute H-033 bis H-036 und die Schwellen +0,10 / Obergrenze +0,02 bleiben, die Primärmenge fällt auf etwa 36 kaputte Belege. „Anhangzeile ohne Größe“ nimmt dem Delivery-Kanal die vergleichbare Zahl und lässt `0 pages` stehen. Die Ground-Truth-Kontrolle ist ein Stapelaufruf; in dem Format liegen die Fehlalarme bei etwa 0,16, und von 30 zufälligen Belegen fallen kaum welche auf die drei Primärarten. V5 bleibt bei 0,85, die Neuberechnung benutzt 0,80. Die „Fangquote“ in 20b §5 steigt bei Einzel/low von 0,41 auf 0,88, wenn die Prävalenz auf 5 % sinkt. Das ist keine Sensitivität. Dieselbe Methode soll ins Skript.

## 3. Die zwei Auswertungen

- **Reasoning:** Urteil nach oben korrigiert, nur für den Stapel. Gepaart, beide Materialstände, +0,12 [0,079; 0,167] und +0,07 [0,037; 0,116]; Übersehen sinkt nicht (v3 +0,032). Kriterienshift und Übertragung auf Nachbaritems bleiben offen, ebenso ob `effort` dasselbe Modell ist. V6 an Einzelbelegen testet diese Zelle nicht. Der Entwurf parkt den einzigen Befund, den 20b trägt.
- **Konfidenz:** Die Kanalregel-Vermutung fällt. Auf v3 fängt Konfidenz < 0,80 bei 14 % Eskalation 57 % der Fehler, zwei auf v2 gelernte Kanäle bei 22 % nur 34 %. Ohne Intervall, ohne Trennung Übersehen/Fehlalarm, Schwelle nachgesehen, v2 und v3 verschiedenes Material. Die Policy-Zahl ist die PPV: Stapel/low von 0,88 bei 50 % auf 0,28 bei 5 %.
- **Naive Baseline:** „Die Decke ist Stringvergleich“ halte ich in dieser Breite nicht aufrecht. B3 irrt bei 0,33, Sonnet bei 0,03–0,08; der Abstand liegt bei Zeilen, Spalten, Gewichten, Last. Dieselbe Notiz setzt einen generator-informierten Prüfer bei nahezu 100 %. B2 kennt die Generatorsprache und schlägt Sonnet an den Leak-Markern (`empty_attachment`: B3 0,00, Sonnet L2 0,21). Baseline je Kanal, Sonnet im Stapel.

## 4. Die drei Fragen

1. Generator v4, und die Primärmenge erst nach einem Test, der Konventionen verbietet: Last 0, Mittelwert 100 und 0 Seiten dürfen ohne Norm nicht als eindeutig gelten.
2. Zweitmodell je Beleg einzeln, geschichtet auf die Primärarten, ohne Befundtext; Neo nur bei Abweichung.
3. Nebenarm außerhalb der 16 Zellen, nur bei SPEC=1, Teil der Seeds, Text vor dem Pilot einfrieren.

**Nicht geprüft:** keine jsonl, `landkarte_belege` und `baseline_naiv` nicht im Ordner, nichts ausgeführt, Bootstrap und Umgewichtung nicht nachgerechnet. Die Punktdifferenzen in 20b §2 stimmen mit §1 überein. `reasoning.effort`, Kosten und der Registerwortlaut jenseits von `prereg-v1.md` ungeprüft.
