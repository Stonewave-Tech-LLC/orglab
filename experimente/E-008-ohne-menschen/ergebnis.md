# E-008: Vollautonom ohne Menschen – Ergebnis

- **Zeitraum:** 2026-10-21, 13:50–17:13
- **Unterbrechung:** Session-Limit ~14:xx–16:20. **6 Runs** des Arms "Abstimmung, k = 1" waren Limit-Ausfälle, die ein Bug der Ausfallerkennung als gültig gespeichert hatte. Sie sind als ungültig markiert und wurden um ~17:05 mit dem behobenen Code (`4226bba`) nachgemessen, siehe Laborbuch.
- **Code:** `cbf4160` (Hauptlauf), `4226bba` (Nachlauf). Der Unterschied betrifft nur die Ausfallerkennung.
- **Rohdaten:** `daten/E-008-ohne-menschen/k1|k2/` (40 gültige Runs), Referenz "mit Mensch" aus `daten/E-007-mole-skript/` (B_minimal). Audit sauber.

## Ergebnisse

| k | Arm | true_completion | Erfolg | Maulwurf-Pakete gerettet | Stimmen | Übernahmen richtig / falsch |
|---|---|---|---|---|---|---|
| 1 | mit Mensch (E-007) | 0,94 | 5/10 | 0,90 | – | (4,1 Neu-Zuweisungen durch den Menschen) |
| 1 | ohne Mensch | **0,74** | 1/10 | **0,10** | – | – |
| 1 | ohne Mensch + Abstimmung | **0,99** | 9/10 | 1,00 | 4,8 | 2,1 / 0,1 |
| 2 | mit Mensch (E-007) | 0,84 | 1/10 | 0,73 | – | (6,3 durch den Menschen) |
| 2 | ohne Mensch | **0,51** | 0/10 | **0,00** | – | – |
| 2 | ohne Mensch + Abstimmung | **0,93** | 5/10 | 0,98 | 11,6 | 5,4 / 0,0 |

**Paarvergleiche** (gleiche Seeds, `true_completion`):

| Vergleich | k = 1 | k = 2 |
|---|---|---|
| ohne Mensch − mit Mensch | −0,200 (p = 0,009) | −0,329 (p = 0,005) |
| Abstimmung − ohne Mensch | +0,250 (p = 0,005) | +0,421 (p = 0,003) |
| Abstimmung − mit Mensch | +0,050 (p = 0,063) | +0,093 (p = 0,033) |

## Vorhersagen (prereg)

| Vorhersage | Ergebnis |
|---|---|
| 1. mit Mensch > Abstimmung > ohne Mensch | **Teilweise.** Abstimmung > ohne Mensch eingetreten, aber **Abstimmung ≥ mit Mensch** (nicht vorhergesagt) |
| 2. Ohne Mensch und ohne Abstimmung kein wirksamer Ersatz | **Eingetreten.** Maulwurf-Pakete gerettet 0,10 / 0,00 |
| 3. Abstimmung wird genutzt, richtige > falsche Übernahmen | **Eingetreten.** Genutzt in 20/20 Runs, 75 richtige gegen 1 falsche Übernahme gesamt |

## Einordnung
- **Ohne Schiedsinstanz fehlt der Hebel.** Ohne Mensch und ohne Regel erkennen die Teams die kaputten Pakete (Fremdprüfungsrate 0,56–0,71), können aber nichts tun. Die Leistung fällt um 20–33 Punkte. Das passt zu Aces Beschreibung von Wave ("ein Agent ohne Neo kann nur jemanden mit mehr Rechten bitten").
- **Ein angebotenes Abstimmungsrecht nutzen die Agenten sofort und treffsicher**: 20/20 Runs, 1 Fehlurteil bei 76 Übernahmen. Das macht den Menschen in diesem Szenario **überflüssig**.
- **Abstimmung schlägt den Menschen leicht.** Wahrscheinliche Erklärung (Alternativhypothese, nicht getestet): **Latenz und Reichweite des Mechanismus.** Der simulierte Mensch antwortet erst einen Tick später und nur, wenn jemand eskaliert und dabei das Paket nennt. Die Abstimmung wirkt sofort beim zweiten Votum. Der Vorteil ist also eher "schneller Mechanismus schlägt langsamen" als "Demokratie schlägt Mensch".
- **Verbindung zu Teil 2 §6.1 (vollautonom):** Gegen *diese* Art Störung (offen sichtbar kaputte Arbeit) ist ein **emergenter Konsens ohne Vertrauenswurzel stabil**. Die schwerere Prüfung steht aus: Saboteure, die *mitstimmen* (Sybil, Teil 2 §6.3), oder Fehlurteile gegen Ehrliche bei Regressionen.

## Grenzen
- n = 10 je Zelle, Entdeckung.
- Die geskripteten Saboteure stimmen nicht mit ab, kontern nicht und antworten nicht. Ein strategischer Gegenspieler fehlt.
- Quorum 2 bei 4 Agenten ist eine niedrige Schwelle. Bei k = 2 könnten zwei kooperierende Saboteure Ehrliche "abwählen". Das ist nicht getestet, weil die Skripte nicht abstimmen.

## Konsequenzen
- **H-024 (neu):** Teams ohne menschlichen Schiedsrichter verlieren gegen Blockierer massiv. Ein einfaches Abstimmungsrecht (Quorum) wird spontan, treffsicher und ohne Fehlurteile genutzt und ersetzt den Schiedsrichter mindestens.
- **Nächster Test (Kandidat):** Saboteure, die selbst abstimmen. Dafür bräuchte es eine Skript-Policy, die Ehrliche gezielt "anzeigt". Damit würde die Sybil- und Lobbying-Gefahr der Mischverfassung (Teil 2 §8) prüfbar.
- **Praxis für Wave (Hypothese):** Eine Übernahme per Bestätigung durch einen zweiten Agenten statt durch Neo könnte den Menschen als Engpass entlasten. Voraussetzung ist ein Belegpfad, der keine Fehlurteile produziert (H-020).
