# E-009: Eigentümerwechsel nach Frist – Ergebnis

- **Zeitraum:** 2026-10-21, ~17:13–17:30 · **Code:** `bbf8874` (inkl. Fix der Ausfallerkennung) · Audit sauber
- **Rohdaten:** `daten/E-009-frist-regel/k1|k2/` (20 Runs), Referenzen aus E-007 (mit Mensch) und E-008 (ohne Mensch, Abstimmung)

## Ergebnisse (`true_completion`, n = 10 je Zelle)

| Governance | k = 1 | k = 2 | Maulwurf-Pakete gerettet (k = 1 / 2) | Fehlurteile |
|---|---|---|---|---|
| keine (ohne Mensch) | 0,74 | 0,51 | 0,10 / 0,00 | – |
| **Frist-Regel** | **0,99** | **0,88** | 1,00 / 0,84 | 0 / 0,1 pro Run |
| Abstimmung (E-008) | 0,99 | 0,93 | 1,00 / 0,98 | 0,1 / 0 |
| Mensch (E-007) | 0,94 | 0,84 | 0,90 / 0,73 | – |

**Paarvergleiche der Frist-Regel:**

| gegen | k = 1 | k = 2 |
|---|---|---|
| ohne Mensch | +0,243 (p = 0,009) | +0,371 (p = 0,003) |
| Abstimmung | −0,007 (p = 1,0) | −0,050 (p = 0,12) |
| Mensch | +0,043 (p = 0,25) | +0,043 (p = 0,32) |

## Vorhersagen (prereg)
| Vorhersage | Ergebnis |
|---|---|
| 1. Frist > ohne Mensch | **Eingetreten** (+0,24 / +0,37) |
| 2. Frist ≥ Abstimmung bei weniger Kommunikation | **Teilweise.** Bei k = 1 gleichauf, bei k = 2 tendenziell etwas schwächer (n.s.). Die Kommunikation ist nicht geringer (27 / 31 gegen 25 / 29 Nachrichten). |
| 3. Fehlurteile selten, seltener als Freigaben von Maulwürfen | **Eingetreten.** 1 gegen 113 Freigaben insgesamt |

## Einordnung
- **Ein Mechanismus zum Eigentümerwechsel ist der entscheidende Hebel, seine Form ist zweitrangig.** Mensch, Abstimmung und Frist liegen alle bei 0,84–0,99, ohne Mechanismus bei 0,51–0,74.
- **Die Frist-Regel ist der einfachste Mechanismus:** unpersönlich, ohne Quorum, ohne Menschen. Sie setzt genau dort an, wo laut Ace in Wave eine Stufe fehlt ("Frist überschritten → Eigentümerwechsel").
- **Zusammen mit H-013** (Wave-Daten: liegen bleibt, was keinen Pull-Mechanismus hat) ist das die bisher praktisch relevanteste Linie des Projekts.

## Grenzen
- Entdeckung, n = 10.
- Die Saboteure sind auffällig: Sie reagieren nie, deshalb ist die Frist leicht zu triggern.
- Die Regel braucht eine Fremdprüfung als Auslöser. Ohne Prüfkultur (vgl. E-005-Positivkontrolle) greift sie nicht.

## Konsequenzen
- **H-025 (neu):** Ein unpersönlicher Eigentümerwechsel nach Frist (ausgelöst durch einen fehlgeschlagenen Fremdcheck) ersetzt den menschlichen Schiedsrichter gegen Blockierer weitgehend, bei sehr wenigen Fehlurteilen.
- **E-014:** Bestätigung der Governance-Befunde auf frischen Seeds (H-024, H-025).
