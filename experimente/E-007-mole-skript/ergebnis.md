# E-007: Misstrauensdosis mit geskripteten Maulwürfen – Ergebnis

- **Zeitraum:** 2026-10-21, 12:42–13:45 · **Code:** `f3b6c28`
- **Rohdaten:** `daten/E-007-mole-skript/k1|k2/` (40 Runs, 0 Abstürze, 0 Fehlzüge) + `daten/E-006-mole-dosis/k0/` (20 Runs, vorab so festgelegt)

## Ergebnis zu den Vorhersagen

| Vorhersage | Ergebnis |
|---|---|
| 1. Dosis-Wirkung (Manipulationscheck) | **Eingetreten.** B: 0,993 → 0,943 → 0,836 (k = 0/1/2), k0 gegen k2 p = 0,0004. Erfolg (alles wahr): 9/10 → 5/10 → 1/10 |
| 2. H-019: Bürokratievorteil wächst mit k | **Nicht eingetreten.** Δ(Bürokratie − B) = 0,000 / −0,029 / +0,014. Interaktion +0,014, p = 0,85 |
| 3. Emergente Bürokratie in B steigt mit k | **Deutlich eingetreten**, siehe Tabelle |
| 4. Mehr gerettete Maulwurf-Pakete mit Bürokratie | Tendenz: 1,00 gegen 0,90 (k = 1), 0,81 gegen 0,73 (k = 2). Ohne Wirkung auf die Gesamtquote |

**Emergente Kontrollinfrastruktur in der ungeregelten Organisation (B_minimal):**

| k | Fremdprüfungsrate | Eskalationen | Neu-Zuweisungen | Nachrichten | Prüfungen |
|---|---|---|---|---|---|
| 0 | 0,42 | 0,0 | 0,0 | 14,9 | 53,0 |
| 1 | 0,58 | 4,1 | 4,1 | 32,5 | 64,1 |
| 2 | 0,64 | 6,4 | 6,3 | 34,5 | 51,7 |

Die explizite Bürokratie zeigt dasselbe Muster auf fast gleichem Niveau (Eskalationen 0 / 2,9 / 5,3).

## Einordnung
- **Neos These aus Teil 2 §4 ist gestützt, als Entdeckung:** Steigt das Misstrauen, erfindet die Organisation von selbst Kontrolle: mehr Fremdprüfung, Eskalation an den Menschen, Umverteilung der Arbeit, mehr Kommunikation. Das geschieht **dosisabhängig** und ohne jede Regel.
- **Warum die explizite Bürokratie nichts bringt:** Die emergente Kontrolle leistet dasselbe. Die Regel ersetzt nur, was ohnehin entsteht (Substitution). Das passt zu E-012/E-013 und H-016: Handregeln bringen über die Selbstorganisation hinaus keinen messbaren Vorteil.
- **Zuschreibung im Wohlwollen:** Die ehrlichen Agenten deuten die Maulwürfe als **unzuverlässig, nicht als böswillig** (*"a1 appears unresponsive: P2 and P6 … are marked done but not actually processed"*). Gelöst wird das über den Menschen (Neu-Zuweisung), nicht über Konfrontation oder Ausschluss.
  - Das ist ein Hinweis auf eine Grenze der Selbstregulation: **Ohne einen Menschen als Schiedsinstanz hätte das Team keinen Hebel gegen einen Agenten, der Pakete blockiert.** Der Mensch ist hier die "Zentralbank" des Vertrauens (Teil 2 §6.1).
- **Die Grenze der Selbstregulation:** Trotz emergenter Kontrolle sinkt die Leistung bei k = 2 auf 0,84. Die Selbstregulation dämpft, sie kompensiert aber nicht voll. Gemessen an `mole_items_recovered` gehen 27 % der Maulwurf-Pakete verloren.

## Grenzen
- n = 10 je Zelle, Entdeckungsphase.
- Die Maulwürfe antworten nie auf Nachrichten, das macht sie "auffällig stumm". Raffiniertere Saboteure (antworten plausibel, sabotieren selten) wären ein schwierigerer Test.
- Neu-Zuweisung gibt es nur über den Menschen. Ein vollautonomes Team ohne diesen Kanal ist ungetestet (Teil 2 §6.1, interessant für Neo).

## Konsequenzen
- **H-019:** Status "nicht gestützt (Entdeckung E-007)".
- **H-022 (neu):** Selbstorganisierte Teams bauen Kontrollinfrastruktur (Fremdprüfung, Eskalation, Umverteilung) dosisabhängig zum Misstrauen auf. Explizite Bürokratie-Regeln substituieren diese nur.
- **Nächste naheliegende Experimente:**
  1. **Bestätigung von H-022** auf frischen Seeds: B allein, k = 0/1/2, n = 20 je Zelle, Trend-Test.
  2. **Ohne menschlichen Schiedsrichter** (`human_channel: none`): Was tut ein vollautonomes Team gegen einen Blockierer? Entstehen Ausschluss, Umgehung oder Abstimmung? Das ist Neos Lieblingsfrage aus Teil 2 §6.1.
