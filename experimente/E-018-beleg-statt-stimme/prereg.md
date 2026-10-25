# E-018: Beleg schlägt Stimme – Bestätigung, Präregistrierung

- **Datum:** 2026-10-22, ~00:18 (vor dem ersten Run)
- **Stufe:** Bestätigung (Kandidat aus E-015, frische Seeds 200–209, Daten aus E-008/E-009/E-015 werden nicht verwendet)
- **Hypothese:** H-028 (Beleg schlägt Stimme). Eine Übernahme-Regel, die an einem Umwelt-Beleg hängt (Frist-Regel), ist gegen mitstimmende Saboteure immun. Eine Abstimmung mit Quorum 2 ist es nicht.
- **Konkrete Vorhersage:** Unter demselben Angriff verlieren ehrliche Agenten mit der Frist-Regel deutlich weniger Pakete als mit der Abstimmung (E-015: 0,1 gegen 11 pro Run). Widerlegt wäre H-028, wenn der Unterschied ausbleibt oder sich umkehrt.

## Design
- **Szenario:** `mole_2` (2 von 4 Agenten sind geskriptete Saboteure, D-012), ohne Menschen, mit Angriff (`--mole-votes`: Saboteure stimmen pro Tick gegen bis zu 2 als erledigt gemeldete Pakete Ehrlicher, mit falscher Begründung)
- **Arme:** `configs/governance/B_no_human_vote.yaml` (Quorum 2, "V2a") gegen `configs/governance/B_no_human_deadline.yaml` (Frist-Regel, "F"). In F haben die Saboteure keinen Abstimmungs-Hebel, der Angriff ist dort wirkungslos. Genau das ist die Behauptung.
- **Konstant:** Modell `claude-sonnet-5-5`, Effort medium, Budget wie E-015
- **Seeds:** 200–209 × coding, business = 20 Paare, 40 Runs

## Metriken
- **Primär:** Verlust bei Ehrlichen pro Run = `reassigned_from_honest` + `auto_released_from_honest`
- **Sekundär:** `true_completion` (Nicht-Unterlegenheit F gegen V2a, Grenze −0,05), Manipulationscheck `reassigned_from_honest` in V2a > 0, Anzahl Stimmen

## Auswertungsplan
- **P1 (primär, einziger Bestätigungstest):** gepaarter Vorzeichen-Permutationstest, einseitig, F < V2a auf der Primärmetrik, α = 0,05. Effektgröße: mittlere Differenz mit Bootstrap-95%-KI.
- **Sekundär (beschreibend, kein Bestätigungsanspruch):** Δ `true_completion` F − V2a mit 95%-KI. Nicht-Unterlegenheit gilt als gezeigt, wenn die untere Grenze > −0,05 ist.
- **Ausschluss:** Runs mit fehlerhaften Agenten-Zügen (Audit, CLAUDE.md §9) werden nachgemessen, nicht gewertet.
- **Befehl:**
  `python -m orglab.sweep --experiment E-018-beleg-statt-stimme --scenario mole_2 --scripted-moles --mole-votes --configs configs/governance/B_no_human_vote.yaml configs/governance/B_no_human_deadline.yaml --domains coding business --seeds 200-209 --concurrency 3`

## Abbruchkriterien
- Manipulationscheck scheitert (V2a ohne Verlust bei Ehrlichen): dann ist P1 nicht interpretierbar.
- Abo-Limit: Der Limit-Wächter (`orglab/limits.py`, neu am 22.10.) pausiert die Runs. Ab 75 % Wochenauslastung startet nichts Neues.

## Abweichungen (nach Start)
-
