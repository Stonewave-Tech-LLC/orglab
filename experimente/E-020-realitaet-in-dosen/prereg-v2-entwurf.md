# E-020 v2 – Überarbeitungsentwurf nach dem Grok-Gutachten

> **Korrektur 23.10. (E-021, Manipulationscheck):** Was hier "Reasoning aus" heißt, war in Wahrheit die **Standardeinstellung mit adaptivem, verborgenem Reasoning** (OpenRouter: Reasoning ist bei Sonnet 5.5 nicht abschaltbar). "Reasoning low" war **gedrosseltes** Reasoning. Alle Aussagen "Reasoning erhöht Fehlalarme" sind deshalb umzudrehen: **Gedrosseltes Reasoning erhöht Fehlalarme** (H-037). Details: `experimente/E-021-reasoning-fehlalarme/ergebnis.md`.

> **Entwurf, nicht freigegeben.** Die gültige Präregistrierung ist weiter `prereg.md` (Hauptlauf ausgesetzt). Dieses Dokument listet die Änderungen, die ich vorschlage. Neo entscheidet, dann wird daraus eine neue `prereg.md`-Fassung, eine Abweichung mit Datum und ein Commit vor dem Pilot.

**Stand:** 23.10.2026, nachts. Grundlage: `notizen/23` (Grok §5), `notizen/20b` (Belegebene), `notizen/27` (naive Baseline).

## Änderungen

| # | Problem (Grok) | Vorschlag | Status |
|---|---|---|---|
| 1 | **Drei Anstupser im Prompt**, jeder mit einem Faktor konfundiert ("look at the system before you decide", "you can look up the runbook", "and what you can look up") | Alle drei streichen. **Die exakten Prompttexte aller 16 Zellen kommen wörtlich in die Präregistrierung**, aus dem Code erzeugt und eingefroren (`dryrun.md` als Anhang). | Vorschlag |
| 2 | **SPEC enthält "Werkzeug vorhanden"** (Runbook-Werkzeug nur bei SPEC=1) | `lookup_runbook` gibt es in **beiden** SPEC-Stufen. Bei SPEC=0 steht der Sollwert zusätzlich im Auftrag. SPEC misst damit nur "Sollwert im Auftrag gegen nur im Runbook". | Vorschlag |
| 3 | **Runbook gibt den ganzen Antwortschlüssel** bei jedem Aufruf | Runbook **abschnittsweise**: `lookup_runbook(topic)` liefert nur den passenden Abschnitt (z. B. traffic, database, cache, attachments, schema, duplicates, weights), dazu 3–4 harmlose Distraktor-Abschnitte. Ein unbekanntes Topic liefert nur die Themenliste. Nachschlagen wird damit eine gezielte Handlung, und V4 wird interpretierbar. | Vorschlag |
| 4 | **Sollwerte lecken in die Kanäle**, SPEC misst für viele Fehlerarten strukturell nichts | (a) **Primärmetrik nur auf vorab benannten, "spec-reinen" Fehlerarten**, deren Spur ohne Sollwert *nicht* entscheidbar ist: `zero_traffic` (übliche Last), `weights_broken` (Gewichtsnorm), `empty_attachment` (übliche Mailgröße, ohne "0 kB"). (b) Dafür **Generator v4**: Leak-Zeilen für diese drei Fehlerarten entfernen (z. B. Anhangzeile ohne Größe, keine "/1"-Normzeile in der Validierung). Ein Test stellt sicher, dass die Spur ohne Runbook nicht eindeutig ist und mit Runbook schon. (c) Die übrigen Fehlerarten laufen weiter mit und werden sekundär berichtet. | Vorschlag, braucht Generator-Arbeit und Kalibrierungs-Pilot |
| 5 | **V6 misst einen anderen Estimanden** als der Stapelbefund | V6 neu formulieren: "Reasoning-Effekt auf Fehlalarme bei **Einzelbelegen**", ausdrücklich keine Replikation des Stapelbefunds. Für die Replikation des Stapelbefunds wäre ein eigenes kleines Experiment nötig (Parkplatz). Hinweis aus `notizen/20b`: gepaart auf Belegebene ist der Stapel-Effekt in beiden Materialständen klar (+0,12 bzw. +0,07). | Vorschlag |
| 6 | **Nicht-Unterlegenheit ohne Intervallstufe** | V6: einseitig 95 %, entspricht dem 90-%-KI zweiseitig, Grenze +0,03 | Vorschlag |
| 7 | **Auswerteskript nicht eingefroren** | `orglab/realitaet_auswertung.py` vor dem Pilot schreiben, mit synthetischen Urteilen testen und committen. Enthält Cluster-Bootstrap über Belege, Paarung, BH-FDR, Ausschlussregel und Prävalenz-Umgewichtung (5 %). | Vorschlag |
| 8 | **Ein Abbruch lässt halbe Läufe zu** | Reihenfolge in **Blöcken**: Je Seed laufen alle 16 Zellen aller Belege des Seeds, bevor der nächste Seed startet. Bei Abbruch sind die vollständigen Seeds balanciert auswertbar. Berichtet wird nur über vollständige Blöcke. | Vorschlag |
| 9 | **Kanal = Seed mod 3 ist nicht geschichtet** | Vorgelegter Kanal (ZUGANG=0) **je Fehlerart balanciert** zugewiesen, nicht nur je Seed | Vorschlag |
| 10 | **Ground Truth nur von Claude geprüft** (zehnmal umgefallen) | Vor dem Hauptlauf: **30 zufällige Belege des neuen Materials** blind von einem Nicht-Claude bewerten lassen (Grok-CLI, sparsam, ein Aufruf als Stapel) oder von Neo. Jede Abweichung wird von Hand geklärt, bevor es losgeht. | Vorschlag |
| 11 | **Prävalenz 50 %** | Alle Fehlalarm- und Eskalationszahlen zusätzlich umgewichtet auf 5 % berichten (Methode wie `notizen/20b` §5) | Vorschlag |

## Was bleibt
- Faktoren SPEC × ZUGANG × AUSKUNFT × REASONING, 16 Zellen, gepaart, Sonnet 5.5 als Einzelbeleg
- Hypothesen H-033 bis H-036 (Wortlaut eingefroren, nur die Messung wird präzisiert)
- Kosten grob wie bisher (~30–50 $), dazu Generator v4 und Pilot

## Offene Fragen an Neo
1. Generator v4 mit leckfreien, spec-reinen Fehlerarten bauen (Punkt 4b, mehr Arbeit, aber sauber), **oder** nur die Primärmetrik auf die vorhandenen, am wenigsten leckenden Fehlerarten beschränken (4a, schnell, aber weniger Daten)?
2. Ground-Truth-Kontrolle (Punkt 10) durch Grok-CLI oder durch dich?
3. Anstupser-Arm ("do it better" gegen Affordanz) als Teil von E-020 oder getrennt (Parkplatz)?

## Nachtrag nach Grok-Gutachten 2 (`notizen/23b`)
- Die "spec-reinen" Fehlerarten sind im aktuellen Generator nicht rein. **Generator v4 ist Pflicht.** Spuren müssen ohne Norm plausibel aussehen, und ein Test verbietet Konventions-Lecks (0, 100, "0 kB", "0 pages").
- Bei unbekanntem Topic liefert das Runbook "kein Eintrag" statt einer Themenliste.
- Der Executor muss seedweise abarbeiten, sonst gibt es keine vollständigen Blöcke.
- Power der Primärmenge (~36 kaputte Belege) vor dem Pilot klären.
- Die Ground-Truth-Kontrolle läuft je Beleg einzeln, geschichtet, mit einem Zweitmodell.
- Die V5-Schwelle wird aus v2-Daten vorab festgelegt (0,80).
- **Neuer Vorschlag E-021:** Der Reasoning-Fehlalarm-Effekt im Stapel ist der einzige gepaart robuste Befund (`notizen/20b` §2). Seine Bestätigung auf frischen Seeds ist billig und unabhängig von E-020.
