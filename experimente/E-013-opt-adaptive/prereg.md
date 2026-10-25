# E-013: Optimierungslauf mit adaptivem Gate, Präregistrierung

- **Datum:** 2026-10-21, 08:46 · **Stufe:** Entdeckung (Optimierungslauf mit Rückkopplung)
- **Herkunft:** E-012 wurde gestoppt, weil das Gate nach E-005 als zu schwach erkannt wurde (D-011).
- **Frage:** Findet der Optimierer Organisationsänderungen mit Effekten von 0,04–0,09, die das alte Gate nicht sehen konnte?

## Vorhersagen (explorativ)
1. Mindestens ein Kandidat wird nachgemessen (Δ > 0, p < 0,5).
2. Werden Kandidaten übernommen, dann eher solche, die **Prüfarbeit gezielt verteilen**, als solche, die sie erhöhen (H-016) oder kürzen (H-017).

**Nullbefund**, wenn auch mit Nachmessung nichts übernommen wird: Dann ist ein Vorteil von Handregeln unter dieser Last ≲ 0,044 (40-Paare-MDE), sofern Kandidaten bis dahin nachgemessen wurden.

## Design
- Wie E-012: `phantom_stress`, Start `B_minimal_tight` (4 Calls / 8 Ticks gesperrt), Training coding + business, Holdout research (5 feste Seeds, alle 2 Iterationen).
- **Gate:** Startwert 5 Seeds je Domäne, adaptiv bis max. 20 je Domäne (Schritt 5, Nachmessen bei Δ > 0 und p < 0,5). Übernahme bei Δ ≥ 0,02, p < 0,1, Tokenfaktor ≤ 3.
- Editor Opus 5.5 · Agenten Sonnet 5.5 · Concurrency 2 · bis 10 h · patience 6
- **Kein Wissen aus E-012 im Editor:** Die Bibliothek startet leer, die abgelehnten Kandidaten aus E-012 werden nicht mitgegeben. Der Lauf ist damit unabhängig.

## Abweichungen
- **09:00–11:20:** Session-Limit während der Baseline von Iteration 1. Um 11:22 gestoppt, startet neu, sobald E-006 fertig ist, mit Concurrency 3 statt 2. Die 4 fertigen Baseline-Runs werden wiederverwendet.
- **12:40:** erneut pausiert, um E-007 vorzuziehen (Priorität: sauberer H-019-Test). Die Fortsetzung folgt direkt im Anschluss, fertige Runs bleiben erhalten.
