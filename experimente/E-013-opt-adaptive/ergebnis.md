# E-013: Optimierer mit adaptivem Gate – Ergebnis (Entdeckung, Null-Ergebnis)

- **Zeitraum:** 2026-10-21, 08:46, bis 2026-10-22, 05:17. Mehrfach unterbrochen: Session-Limits, Vorrang für E-014 und E-018, Code-Update für den Limit-Wächter (D-013).
- **Rohdaten:** `daten/E-013-opt-adaptive/` (`verlauf.log`, `bericht.md`, `state.json`, iter-001 bis 006)
- **Setup:** `phantom_stress`, Start `B_minimal_tight`, Training coding + business, Holdout research. Propose-Editor Claude Opus 5.5, Agenten Sonnet 5.5. Je Iteration zwei Kandidaten (invariant, spezifisch), Gate mit 10 Paaren (adaptiv bis 20 je Domäne).

## Ergebnis
- **6 Iterationen, 12 Kandidaten, 0 übernommen.** Der Optimierer hat nach der Geduldsregel (6 Iterationen ohne Verbesserung) regulär gestoppt.
- Alle Effekte liegen zwischen −0,044 und +0,013 (`true_completion`), keiner ist auch nur tendenziell signifikant (kleinstes p = 0,153, für einen negativen Effekt). 8 von 12 Kandidaten waren schlechter als die Baseline.
- Mehrere Kandidaten sparten Tokens (bis ×0,68), ohne messbar zu schaden. Weil das Gate auf Leistung zielt, wurden sie nicht übernommen.

## Einordnung
- **Gestützt:** H-016 und die Befunde aus E-007, E-011 und E-012. Handgeschriebene oder vom Modell vorgeschlagene Zusatzregeln bringen über eine minimale Organisation hinaus nichts Messbares. Unter Knappheit kosten sie eher Aufmerksamkeit.
- **Nicht gezeigt:** Dass es keine bessere Regel gibt. Die Teststärke reicht nur für Effekte ab etwa 8–9 Punkten. Kleine Verbesserungen sieht dieses Gate nicht.
- **Methodische Lehre:** Ein Optimierer, der um Regeln im Prompt herum sucht, findet in einem Szenario nahe der Decke wenig. Mehr verspricht eine Suche über **Mechanismen** (Übernahme-Regeln, Beleg-Pflichten), wie sie E-014 und E-018 bestätigt haben. Außerdem lohnt sich ein Ziel, das Kosten einbezieht, etwa Leistung pro Token oder pro Mensch-Minute.
- **Kosten:** Der Opus-Editor macht den Optimierer teuer im Abo. Die letzten 3 Iterationen kosteten etwa 6 Punkte Wochenkontingent.
