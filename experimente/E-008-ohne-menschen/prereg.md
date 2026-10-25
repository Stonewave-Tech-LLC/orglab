# E-008: Vollautonom ohne Menschen – Selbstverwaltung gegen Blockierer, Präregistrierung

- **Datum:** 2026-10-21, 13:50 · **Stufe:** Entdeckung
- **Anlass:**
  - In E-007 lösen die ehrlichen Agenten das Problem der Saboteure **ausschließlich über den Menschen** (Neu-Zuweisung).
  - Neos Teil 2 §6.1: "Vollautonom ist für Neo interessanter". Ohne Mensch fehlt die Vertrauenswurzel. Bleibt dann nur emergenter Konsens?
- **Fragen:**
  1. Wie viel kostet das Fehlen des menschlichen Schiedsrichters?
  2. Entdecken und nutzen Agenten ein angebotenes Abstimmungsrecht (`vote_reassign`, Quorum 2)?
  3. Wie oft treffen sie **Fehlurteile** (Übernahme von Paketen ehrlicher Agenten)?

## Vorhersagen (explorativ)
1. `true_completion`: mit Mensch (E-007-Daten) > ohne Mensch + Abstimmung > ohne Mensch, jeweils bei k = 1 und 2.
2. Ohne Mensch und ohne Abstimmung entstehen keine wirksamen Ersatzmechanismen (das Team hat keinen Hebel). `mole_items_recovered` fällt deutlich.
3. Mit Abstimmung: `reassign_votes` > 0 in der Mehrzahl der Runs, `reassigned_from_moles` > `reassigned_from_honest`.
4. Explorativ: Entstehen im Text Muster wie Anklage, Ausschluss oder Misstrauensbekundungen? Qualitativ in den Transkripten.

## Design
- **Szenario:** `mole_1`, `mole_2` mit geskripteten Maulwürfen (D-012)
- **Configs:** `configs/governance/B_no_human.yaml` (human_channel none), `configs/governance/B_no_human_vote.yaml` (zusätzlich reassign_quorum 2). **Referenz:** B_minimal mit Mensch aus E-007 (gleiche Seeds und Domänen).
- **Domänen:** coding, business · **Seeds:** 0–4 → 2 Configs × 2 k × 2 Domänen × 5 = **40 Runs** in `daten/E-008-ohne-menschen/k1|k2/`
- Sonnet 5.5 · Concurrency 2 (parallel zu E-013)

## Auswertung
- Mittelwerte je (k, Config) mit Bootstrap-CI.
- Paarvergleiche gegen die Referenz aus E-007 mit gleichen Seeds.
- Governance-Metriken: Stimmen, richtige und falsche Übernahmen.
- 2 Transkripte lesen.

## Abweichungen
-
