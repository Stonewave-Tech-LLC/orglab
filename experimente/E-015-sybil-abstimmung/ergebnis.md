# E-015: Saboteure, die mitstimmen – Ergebnis

- **Zeitraum:** 2026-10-21, ~22:32–23:04 · **Code:** `8c10f27` · Audit sauber
- **Rohdaten:** `daten/E-015-sybil-abstimmung/` (20 Runs), Referenzen E-008 k2 und E-009 k2 (gleiche Seeds 0–4, gepaart)

## Ergebnisse (`mole_2`, 2 von 4 Agenten sind geskriptete Saboteure, ohne Menschen)

| Arm | true_compl. | Erfolg | Stimmen | Übernahmen von Saboteuren | **Diebstahl bei Ehrlichen** |
|---|---|---|---|---|---|
| Abstimmung Q2, ohne Angriff (E-008) | 0,93 | 5/10 | 11,6 | 5,4 | 0,0 |
| **Abstimmung Q2, mit Angriff** | 0,89 | 2/10 | 34,8 | 5,4 | **11,0** |
| **Abstimmung Q3, mit Angriff** | **0,51** | 0/10 | 44,6 | **0,0** | 0,0 |
| Frist-Regel (E-009) | 0,88 | 3/10 | – | (8,2 Freigaben) | 0,1 |
| ohne Mechanismus (E-008) | 0,51 | 0/10 | – | – | – |

**Paarvergleiche** (`true_completion`):
- Q2 mit Angriff − Q2 ohne: −0,043 (p = 0,50)
- **Q3 mit Angriff − Q2 mit Angriff: −0,379 (p = 0,005)**
- Frist − Q2 mit Angriff: −0,007 (p = 1,0)
- Q2 mit Angriff − ohne Mechanismus: +0,379 (p = 0,003)

## Vorhersagen
| Vorhersage | Ergebnis |
|---|---|
| 1. Der Angriff schadet (Diebstahl > 0) | **Teilweise.** Diebstahl massiv (11 pro Run), aber die Leistung sinkt nur um 0,04 (n.s.). Die Ehrlichen holen sich die Pakete per Gegenstimmen zurück: ein "Tauziehen" mit 35 Stimmen pro Run. |
| 2. Ein höheres Quorum (3) schützt | **Widerlegt, und zwar drastisch.** Mit Q3 erreichen auch die zwei Ehrlichen nie eine Mehrheit, der Mechanismus ist tot (0,51, gleich "ohne Mechanismus"). |
| 3. Die Frist-Regel ist gegen Behauptungen immun | **Eingetreten.** Gleiche Leistung wie Q2 unter Angriff, aber 0,1 statt 11 Fehlurteile. |

## Einordnung
- **Die byzantinische Grenze erscheint empirisch.** Bei n = 4 Agenten verträgt ein Abstimmungsverfahren höchstens f = 1 Saboteur (n ≥ 3f+1). Bei f = 2 gibt es kein Quorum, das zugleich Sicherheit (keine Diebstähle) und Lebendigkeit (Ehrliche können handeln) bietet:
  - Q2 ist lebendig, aber unsicher (11 Diebstähle).
  - Q3 ist sicher, aber tot.
  - Meine vorab formulierte "Abwehr" Q3 war ein Denkfehler, und das Experiment hat ihn sichtbar gemacht.
- **Beleg schlägt Stimme (H-020):** Die Frist-Regel verlangt einen Umwelt-Beleg (fehlgeschlagener Fremdcheck). Lügen-Stimmen können sie nicht auslösen. Sie ist damit gegen diesen Angriff **strukturell immun** und erreicht die Leistung der Abstimmung ohne deren Fehlurteile. Das ist ein direktes Argument für "Quittungen der Umwelt statt Selbstauskunft" (AAP-Prinzip, `notizen/14`).
- **Tauziehen als emergentes Verhalten:** Die ehrlichen LLM-Agenten holen gestohlene Pakete sofort per Gegenstimme zurück. Der Mechanismus ist missbrauchbar, wird aber auch zur Gegenwehr genutzt. Die Kosten sind hoch (3× so viele Stimmen, mehr Kommunikation), die Leistung bleibt erstaunlich stabil.

## Grenzen
- Entdeckung, n = 10.
- Skript-Saboteure mit einfacher Strategie (bis zu 2 Lügen-Stimmen pro Tick).
- Nur n = 4. Die Bedingung 3f+1 lässt sich erst mit größeren Teams sauber variieren (z. B. n = 7, f = 2).

## Konsequenzen
- **H-028 (neu):** Mehrheitsbasierte Selbstverwaltung unter LLM-Agenten unterliegt dem Sicherheits-/Lebendigkeits-Zielkonflikt der byzantinischen Fehlertoleranz. Belegbasierte Regeln (Umwelt-Quittung) umgehen ihn gegen Lügen-Stimmen.
- **Nächster Test (Kandidat):** n = 7 mit f = 1, 2, 3 und Quorum-Varianten. Wird die Grenze 3f+1 exakt sichtbar? Dazu Absprache-Saboteure, die sich gegenseitig bestätigen (`notizen/14` B).
