# E-020 v3 Pilot: Bericht (nur Technik, Daten fließen nicht in die Auswertung)

- **Lauf:** 23.10.2026, endete vor 12:46. 24 Belege (Seeds 1300–1301, v4.1) × 8 Zellen = 192 Prüfungen, 3,25 $.
- **Präregistrierte Pilot-Kriterien:**
  - Ausfälle 0 % in allen Zellen
  - `run_check` in jeder ZUGANG=1-Zelle genutzt (im Mittel 3,0 je Prüfung)
  - `lookup_runbook` genutzt (75–100 % der Prüfungen)
  - **Alle Kriterien erfüllt.**

## Befund: Die Runbook-Suche ist zu starr (Validitätsproblem, vor dem Hauptlauf zu klären)
Sonnet sucht mit natürlichen Begriffen: dem Dienstnamen ("search-indexer", "notify-worker"), "invoice sending", "survey dataset D5", "D3". `lookup` erkennt aber nur Themen-Stichworte (traffic, cache, contact, weights, schema …). Ein Dienst- oder Datensatzname ergibt deshalb "No entry".

- Bei spec-reinen kaputten Belegen unter SPEC=1 wurden 18 von 28 übersehen. **In allen 18 Fällen kam der richtige Abschnitt nicht zurück.**
  - `low_traffic` und `cache_partial`: 8 von 8 übersehen, gesucht wurde nur nach Dienstname, Port und "deploy".
  - `column_loss`: 4 von 4 übersehen, "survey dataset D5" findet den Schema-Abschnitt nicht.
- Würde so der Hauptlauf laufen, mäße SPEC **"Sollwert fehlt im Auftrag UND die Suche findet ihn schlecht"**. Gemeint war nur der erste Teil. Ein echtes Team-Wiki liefert auf den Dienstnamen die Seite des Dienstes.
- Nicht als Ergebnis zu lesen: Pilot, n klein. Die SP0-Zellen hatten 0–4 % Fehler, die SP1-Zellen 12–29 %.

## Vorschlag (Entscheidung Neo, dann Abweichung in `prereg-v3.md`, dann Grok-Gutachten)
**Seitenbasierte Suche:**
- Nennt das Topic die Einheit (Dienstname, "invoice", Rechnungs- oder Kundennummer, Datensatz-ID oder "survey dataset"), kommt die **ganze Runbook-Seite dieser Einheit** zurück: alle Abschnitte inklusive der Distraktoren.
- Ein spezielles Stichwort ("port", "cache") liefert weiter nur den passenden Abschnitt.
- Unbekanntes bleibt "No entry".
- Das Material (Belege, Kanäle) bleibt unverändert, ebenso Lecktest und Fremdkontrolle, weil das Runbook dort nicht vorkommt.
- **Folge für V4:** V4 misst dann "die Norm-Quelle konsultiert" statt "den exakten Abschnitt getroffen". Das ist realistischer, und Grok hatte V4 ohnehin als Selbstselektion und nur deskriptiv eingestuft.
- Danach wäre ein zweiter kleiner Pilot nötig (~3 $), um zu prüfen, dass die Suche trifft.

## Pilot 2 (seitenbasierte Suche `seite-1`, gleiche Seeds 1300–1301), endete vor 13:05
- 192 Prüfungen, **0 Ausfälle**, 2,94 $. `run_check` in ZUGANG=1 im Mittel 3,0. Nachgeschlagen wurde bei SPEC=1 in 100 % der Prüfungen, bei SPEC=0 in 83–100 %.
- **Vorab festgelegtes Kriterium:** Bei SPEC=1 und spec-reinen kaputten Belegen kam in **28 von 28** Prüfungen mit Nachschlagen der Normwert zurück (Schwelle ≥ 80 %). **Erfüllt.**
- Nicht als Ergebnis zu lesen (n = 24, Pilot):
  - Die Fehlerrate in den SPEC=1-Zellen fiel von 12–29 % (Pilot 1) auf **4–8 %**. Der große Unterschied in Pilot 1 kam also fast vollständig von der starren Suche, nicht vom fehlenden Sollwert im Auftrag.
  - Übersehen trotz gefundener Norm gab es 2× bei `low_traffic`.
- **Folge für den Hauptlauf (Erwartung, keine Vorhersageänderung):** Mit guter Suche schlägt Sonnet fast immer nach. Ein großer SPEC-Effekt ist daher unwahrscheinlich. Die Präregistrierung bleibt unverändert, V1 kann also widerlegt werden. Laut Power-Simulation wäre ein Effekt um +0,05 zu etwa 75 % sichtbar.
- **Für die Projektfrage ist das selbst ein Hinweis:** Nicht "steht der Sollwert im Auftrag?" scheint zu entscheiden, sondern "ist er auffindbar?" (Parkplatz: Auffindbarkeit).

## Nachtrag 2026-10-23 13:26 (nach Grok-Gutachten 3)
- Der Satz "Ein großer SPEC-Effekt ist daher unwahrscheinlich" oben war **voreilig** (n = 24, und die Suche war zu leicht, `notizen/23c`). Er hat kein Gewicht für den Hauptlauf. Die Fehlerraten der Piloten 1 und 2 bleiben versiegelt.
- **5 Transkripte aus Pilot 2 gelesen (Pilotkriterium nachgeholt):**
  - Werkzeugantworten kommen an.
  - Sonnet nutzt die gefundene Norm (z. B. "runbook says D5 has 70 columns").
  - In einem Ok-Beleg bemerkte Sonnet zu Recht den Widerspruch "German template" gegen englischen Betreff. Das war ein Generatorfehler in einem Distraktor-Abschnitt, in v4.2 behoben.


## Pilot 3 (Material v4.3, Suche `seite-2`, frische Seeds 1400–1401), Bericht 13:39
Festgelegt in Abweichung 2 (`prereg-v3.md`): nur Technik, Fehlerraten werden nicht betrachtet.

- 192 Prüfungen, **0 Ausfälle in allen Zellen** (Kriterium ≤ 5 % je Zelle), 2,87 $.
- `run_check` in jeder ZUGANG=1-Zelle genutzt, im Mittel 3,0 je Prüfung.
- `lookup_runbook` in 75–100 % der Prüfungen je Zelle genutzt, die Seite der Einheit kam in 75–100 % zurück.
- **5 zufällig gezogene Transkripte gelesen** (Ziehung mit Seed 2023):
  - `business-fail_moderate-1401`: `wrong_contact` über die Kontaktliste im Runbook erkannt.
  - `research-ok_clear-1401`: Normen (Duplikate, Population, Spaltenzahl) korrekt mit den Ausgaben abgeglichen.
  - `business-ok_clear-1401`: korrekt als ok beurteilt, kein Widerspruch zum Template-Abschnitt mehr.
  - `research-fail_subtle-1400`: `duplicates_partial` über die Runbook-Zahl erkannt.
  - Das fünfte Transkript ist hier nicht einzeln vermerkt (beim Lesen nicht mitnotiert). Über alle fünf: Die Werkzeugantworten kamen vollständig an, kein neuer Widerspruch im Material sichtbar.
- **Alle Kriterien erfüllt.** Die Fehlerraten wurden nicht angesehen und bleiben versiegelt wie die aus Pilot 1 und 2.

## Prüfungen von Material v4.3 auf den Hauptlauf-Seeds 6000–6023 (Regel 12 und 17)
- **Fremdkontrolle** (GPT-6.1 Sol, effort high, 48 geschichtete Belege): **48 von 48 stimmen mit der Generator-Wahrheit überein**, keiner "nicht entscheidbar" (`fremdkontrolle.md`, 0,17 $). Der frühere Grenzfall `coding-fail_moderate-6021` liegt in der Stichprobe und wurde eindeutig als kaputt beurteilt. Die gekennzeichnete Sensitivitätsanalyse ohne ihn bleibt trotzdem wie präregistriert.
- **Lecktest** (Kurzauftrag ohne Sollwerte, kein Runbook): **0 von 42** spec-reinen kaputten Belegen ohne Sollwert sicher erkannt, je Fehlerart 0 von 6 (Kriterium ≤ 25 %; `lecktest.md`).
  - Gegenprobe: 2 von 12 Ok-Belegen (`research-ok_clear-6001`, `-6022`) hielt GPT ohne Sollwerte für nicht belegbar ("Gewichte nur auf die Summe skaliert"). Ohne Runbook ist das vertretbar, mit vollem Auftrag beurteilt die Fremdkontrolle die Ok-Belege richtig. Kein Handlungsbedarf, aber ein Hinweis: Ohne Sollwert wird bei `weights` eher Fehlalarm gegeben.
- Code-Lecktest auf den Hauptlauf-Seeds läuft in der Suite (`tests/test_evidence_v4.py`).
