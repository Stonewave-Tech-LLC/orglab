# E-015: Saboteure, die mitstimmen (Angriff auf die Selbstverwaltung), Präregistrierung

- **Datum:** 2026-10-21, ~17:45 · **Stufe:** Entdeckung
- **Anlass:**
  - In E-008 ersetzt die Abstimmung den Menschen, aber die Skript-Saboteure stimmten nicht mit.
  - Ace (notizen/12): Die ehrliche Gegenprobe ist ein Saboteur, der mitstimmt.
  - Teil 2 §6.3/§8: Sybil- und Lobbying-Gefahr der Demokratie.
- **Angriff:** Die geskripteten Saboteure (k = 2) stimmen pro Tick gegen bis zu 2 als erledigt gemeldete Pakete Ehrlicher, mit falscher Begründung ("I checked …: it FAILED"). Erreichen sie gemeinsam das Quorum, gehört das Paket einem Saboteur, der es liegen lässt.

## Arme (alle `mole_2`, geskriptete Saboteure, ohne Menschen, Seeds 0–4, coding + business)
- **V2a:** `B_no_human_vote` (Quorum 2) **mit Angriff** → neu, 10 Runs
- **V3a:** `B_no_human_vote3` (Quorum 3, also 2 Saboteure allein reichen nicht) **mit Angriff** → neu, 10 Runs
- **Referenzen** (gleiche Seeds):
  - V2 ohne Angriff (E-008 k2)
  - Frist-Regel (E-009 k2). Eine Frist braucht einen echten Fremdcheck der Umwelt, Stimmen können sie nicht auslösen.

## Vorhersagen (explorativ, gerichtet)
1. **V2a < V2:** Der Angriff schadet. Es gibt `reassigned_from_honest` > 0, also Fehlurteile durch erkaufte Mehrheiten.
2. **V3a > V2a:** Ein höheres Quorum schützt, weil Saboteure ohne ehrliche Stimme keine Mehrheit haben.
3. **Frist-Regel (E-009) ≥ V2a:** Eine Regel, die an einem Umwelt-Beleg hängt, ist gegen Behauptungen immun. Das ist der Bezug zu H-020 (Beweishierarchie): Beleg schlägt Stimme.

## Abweichungen
-
