# Warum Agenten ehrlich überbehaupten (zu H-023)

**Anstoß:** Neo, 21.10. abends: "Ehrliche Überbehauptung kann wegen Mangel an Information sein oder … was noch?"

**Arbeitsdefinition:** Ein Agent meldet "geprüft" oder "funktioniert", glaubt das auch, aber es stimmt nicht.

## Mögliche Ursachen (Kandidaten-Taxonomie, nicht abschließend)

| # | Ursache | Kern | Wave-Beispiel | Im Testbed erzeugbar durch | Gegenmittel |
|---|---|---|---|---|---|
| 1 | **Informationsmangel** | Der echte Zustand ist für ihn nicht sichtbar | V3: Der echte Aufrufer war nicht bekannt | Board aus, Wissen nur beim Hub | Zugang zum echten Pfad, geteilter Zustand |
| 2 | **Falsches Prüfmodell (Proxy)** | Er weiß genug, hält aber das Falsche für den Beweis ("Exit 0 = wirkt") | V13: pm2 "online"; V3: synthetische DB-Probe | billiger Check, der manchmal lügt (Aces Szenario) | Beweishierarchie (H-020): wirkungsnächster Beleg zählt |
| 3 | **Veraltung** | Es stimmte beim Prüfen, inzwischen nicht mehr | Regressionen; `aus_erinnerung` im VERIFIKATIONSSTATUS | Regressionen (`phantom_hard`) | Prüfung mit Zeitstempel, Neuprüfung nach Änderungen |
| 4 | **Weitergereichte Behauptung (Hörensagen)** | Er übernimmt die Prüfung eines anderen und meldet sie als eigene. Die Beweiskette reißt | Worker-Bericht → Ace → Neo; "Neo sagt …" | Stille-Post-Kette (Teil 1, Szenario 2) | Herkunft mitführen, signierte Belege (AAP) |
| 5 | **Aufmerksamkeits- und Zeitdruck** | Er bricht nach dem ersten grünen Signal ab (satisficing) | "es läuft, weiter zum Nächsten" | knappes Budget (E-003/E-012) | Prüfpflicht an kritischen Stellen statt überall (H-016) |
| 6 | **Erwartungs- bzw. Bestätigungsfehler** | Er prüft, um zu bestätigen, nicht um zu widerlegen. "Mein Fix wirkt" ist die Hypothese, die er schützt | Fix-Meldungen nach eigenem Test | Eigentümer prüft eigenes Werk vs. Fremdprüfung | Vier-Augen- bzw. Fremdprüfung, Red Team |
| 7 | **Sprachliche Inflation** | "Verifiziert" heißt bei ihm "lief ohne Fehler". Das Wort ist nicht kalibriert | VERIFIKATIONSSTATUS als Selbstauskunft | – | feste Begriffe mit Belegpflicht ("verifiziert = Beleg X liegt vor") |
| 8 | **Anreiz zum Abschluss** | Ein "fertig" schließt den Loop, das wird belohnt. Offenlassen fühlt sich wie Versagen an | Agenten melden lieber "done" als "unklar" | Metrik, die Abschluss belohnt | "unklar" als legitimen Status zulassen und belohnen |

## Beobachtungen
- **1–4 sind epistemisch** (was er weiß). **5–8 sind motivational bzw. situativ** (wie er damit umgeht). Die Gegenmittel unterscheiden sich entsprechend: Für 1–4 braucht es bessere Belege, für 5–8 bessere Anreize und Regeln.
- **H-021 (Maulwürfe gestehen) passt ins Bild:** Absichtliche Falschmeldung erzeugt bei Claude offenbar inneren Druck zur Korrektur. Bei 1–4 fehlt dieser Druck, weil der Agent nichts Falsches *weiß*. Deshalb korrigiert sich ehrliche Überbehauptung nicht von selbst (Ace).
- **Testbar:** Jede Ursache ist eine eigene Manipulation. Ein Experiment könnte 2 und 4 gegeneinander stellen (falscher Proxy gegen Hörensagen-Kette) und messen, welche Gegenmittel jeweils wirken.

## Offene Frage an Neo
Welche dieser Ursachen siehst du bei menschlichen Teams im Verkauf am häufigsten? Neos Menschenkenntnis als Messinstrument (Teil 3 §8).
