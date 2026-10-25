# E-016: Prüfer-Panel – Ergebnis (Entdeckung, unvollständig)

- **Zeitraum:** 2026-10-21, ~23:57–23:4x (Datumsgrenze). **Abgebrochen bei 3.800 von 7.200 Urteilen** (157 von 300 Belegen). Ursache war ein Bug: Die Fortschrittsanzeige las das Kosten-Ledger, während parallele Threads hineinschrieben, und stürzte an einer halben Zeile ab. Behoben (Lock + robuste Leser).
- **Kosten:** siehe `daten/openrouter_ledger.jsonl` (≈ 2,6 $ für E-016 inkl. Pilot)
- **Rohdaten:** `daten/E-016-pruefer-panel/judgments.jsonl` (3.753 gültige Urteile, 47 unparsbar oder Fehler)

## Hauptergebnis: Deckeneffekt bei starken Modellen
| Modell | Fehlerrate gesamt | fail_deceptive | fail_injected |
|---|---|---|---|
| Claude Sonnet 5.5 / Haiku 5.5, GPT-6.1 Sol / 6 Luna, Gemini 4 Argon | **0,00** | 0,00 | 0,00 |
| Gemini 3.1 Flash-Lite | 0,00 | 0,00 | 0,03 |
| Grok 4.3 | 0,06 | 0,17 | 0,27 |
| DeepSeek V4 Pro | 0,09 | 0,17 | **0,53** |

**Nach D-010 ist H-026 mit diesen Belegen für starke Modelle nicht testbar.** Die Belege sind zu leicht. Vorhersagen 1, 2 und 4 lassen sich deshalb nicht beurteilen.

## Was trotzdem interpretierbar ist (explorativ)
- **Gleiches Modell, mehrere Stichproben:** Bei DeepSeek bzw. Grok ist P(alle 3 Stichproben irren) **94× bzw. 187×** höher als bei Unabhängigkeit. Das stützt Vorhersage 1 für die Modelle, die überhaupt irren. Dasselbe Modell mehrfach zu fragen, bringt kaum Redundanz.
- **Über Familien:** DeepSeek × Grok haben phi = 0,62 (Vorhersage 3 gestützt, n = 1 Paar mit Varianz).
- **Manipulation per eingeschleustem Prüfer-Hinweis:** DeepSeek +0,36, Grok +0,10. Claude, GPT und Gemini sind unbeeinflusst. Vorhersage 5 ist nicht für die Mehrheit erfüllt, wohl aber für die schwächeren Prüfer.
- **Kalibrierung (alle Modelle):**
  - Konfidenz ≥ 0,97: Fehlerrate 0,2 %
  - 0,90–0,97: 3,4 %
  - 0,70–0,90: 14 %
  - → **Die angegebene Konfidenz ist ein brauchbares Eskalationssignal** (Kandidat für die Minimalregel "nur bei Unsicherheit an Menschen").

## Korrektur einer eigenen Aussage
Im (ungültigen) Format-Pilot hatte ich einen Beleg, den alle 8 Modelle falsch beurteilten, gegenüber Neo als Hinweis auf korrelierte Fehler über Familien gedeutet. **Das war falsch.** Der Beleg war fehlerhaft generiert (der "falsche Empfänger" war derselbe Kunde). Die Modelle hatten recht.

## Konsequenzen
- **Kalibrierung der Belege (D-010) vor einer Neuauflage (E-017):** subtilere Hinweise, längere und verrauschtere Logs, Rechen- und Abgleichsschritte, mehrere schwache statt eines starken Hinweises. Ziel: Fehlerrate starker Modelle 10–40 %. Zuerst an einer kleinen Stichprobe.
- Der Bug ist behoben. Die vorhandenen Urteile bleiben gültig, weil sie vor dem Absturz vollständig geschrieben wurden.
