# E-001: Pilot – Ergebnis

- **Zeitraum:** 2026-10-21, 00:13–00:45
- **Code-Version:** Commit `51f29d4`
- **Rohdaten:** `daten/E-001-pilot/` (24 Runs, 0 Abstürze, 0 Backend-Ausfälle, 0 fehlerhafte Agenten-Züge)

## Ergebnis zu den Erwartungen

| Erwartung (prereg) | Ergebnis |
|---|---|
| Varianz von `true_completion` deutlich > 0 | **Nicht eingetreten.** Alle 24 Runs haben 1,00, die Varianz ist 0. **Deckeneffekt.** |
| C hat weniger `orphans_end` | Nicht prüfbar, alle Runs enden ohne Waisen. |
| Kein Regime erreicht systematisch `phantoms_diagnosed` = 1 | **Widerlegt.** Alle Regime erreichen 1,00. Sonnet 5.5 prüft die Wirkung **spontan**, ohne entsprechende Norm. |

**Durchsatz:** ~75 s pro Run (2–4 Ticks), Concurrency 2 lief stabil, keine Rate-Limits. Pro Run fallen ~5.000 Output-Tokens an, das sind rund 0,45 USD nach API-Preis (Schätzung des SDK).

## Prozessunterschiede (explorativ, n=6 pro Regime, keine Inferenz)

| Regime | Ticks bis fertig | Nachrichten | Kommunikations-Gini | Beobachtung |
|---|---|---|---|---|
| A_contracts | **3,5** | 8,2 | 0,30 | Am langsamsten. Der Hub ist der Engpass, und der Koordinator handelt auf **veralteter Information**: Er meldet einen Fehler, der längst behoben war. Als einziges Regime mit 100 % `reported_completion` (der Vertrag erzwingt die Meldung). |
| B_minimal | 2,8 | **13,0** | 0,16 | Am meisten Nachrichten. Arbeitsteilung entsteht über Messaging. |
| C_stigmergy | **2,5** | **0,7** | 0,33 | **Koordiniert fast ohne Nachrichten.** Board und Notizbuch ersetzen das Messaging (stigmergische Koordination funktioniert). |
| D_constitution | **2,5** | 9,5 | 0,19 | Rollen differenzieren sich spontan: Ein Agent schlägt in Tick 1 einen Plan mit **Reviewer-Rolle** vor, ein anderer übernimmt sie. Die formale Meta-Regel ("RULE:/ENDORSE:") wird **nicht** genutzt. Stattdessen entstehen informelle Lektionen im Notizbuch, z. B. *"'online' status can lie; always inspect_item after execute"*. |

## Weitere Beobachtungen
- **Weltwissen ergänzt die Struktur.** In der Business-Domäne erkennt ein Agent eine Abhängigkeit, die nicht modelliert ist ("Rechnung erstellen" vor "Rechnung senden"), und plant danach. Die Agenten koordinieren also nicht nur über die vorgegebene Struktur. Für Szenario-Design heißt das: Titel können ungewollte Hinweise geben.
- **Testbed-Artefakt.** Ein Run endet, sobald alles *tatsächlich* funktioniert, auch wenn die Organisation das noch nicht weiß oder gemeldet hat (`reported_completion` < 1 bei B, C, D). Für spätere Szenarien wäre ein Ende "alles gemeldet und wahr" sauberer. Das ist notiert, aber nicht geändert, damit die Vergleichbarkeit erhalten bleibt.

## Nachtrag: Emergenz-Analyse (post-hoc, explorativ, nicht präregistriert)

Methode: `orglab/emergence.py`. Für jeden Agenten wird ein Aktionsprofil erstellt, dazu die dominante Aktivität (ab 45 %) als emergente Rolle und die Spezialisierung als 1 − mittlere normierte Entropie. Daten: `daten/E-001-pilot/emergenz.md`.

| Regime | Spezialisierung | emergente Rollen (24 Agenten) |
|---|---|---|
| A_contracts | 0,40 | executor 17, verifier 4, communicator 2 (der Hub), generalist 1 |
| B_minimal | 0,40 | executor 12, verifier 6, generalist 6 |
| C_stigmergy | **0,33** | **generalist 12**, executor 7, verifier 5 |
| D_constitution | 0,39 | executor 15, verifier 6, generalist 2, coordinator 1 |

**Lesart (Hypothese, nicht Befund):**
- Gemeinsamer sichtbarer Zustand (C) **senkt den Bedarf an Rollendifferenzierung**: Jeder kann alles tun, weil jeder alles sieht.
- Ohne geteilten Zustand entsteht Arbeitsteilung über Rollen und Nachrichten.
- Das wäre eine Organisationsdynamik, die man gezielt testen kann → H-015.

## Grenzen
- n=3 pro Zelle, zwei Domänen, ein Modell.
- Der Deckeneffekt bedeutet: **Dieses Szenario ist für Sonnet 5.5 zu leicht, um Organisationen zu unterscheiden.** Das ist kein Beleg, dass Organisation egal ist.

## Konsequenzen
1. **H-014** formuliert (Organisationsunterschiede erst unter Last).
2. **E-002** auf `phantom_hard` (14 Pakete, 3 Phantome, 3 Regressionen) wurde vorab registriert und gestartet.
3. **Methodische Lehre:** Ein Szenario muss vor dem Regime-Vergleich auch mit dem **echten Modell** gegen die Decke kalibriert werden, nicht nur mit geskripteten Policies. Daraus wird ein Kalibrierungsschritt im Ablauf (D-010).
4. Die spontane Wirkungsprüfung von Sonnet 5.5 passt zu H-012 (Fähigkeitsschwelle). Ein Vergleich mit Haiku 5.5 auf `phantom_done` wäre der direkte Test, ob das schwächere Modell von Struktur profitiert.
