# Naive Baseline ohne LLM: Wie viel ist Stringvergleich?

**Stand:** 23.10.2026, nachts · explorativ · Skript `python -m orglab.baseline_naiv` · Anlass: Grok-Gutachten §6 und §7.
Material: Generator v3.1, Seeds 1200–1211 (144 Belege × 3 Kanäle = 432 Einzelurteile), dieselben Einheiten wie die Sonnet-Kalibrierung E-019 v3.

**Regeln** (vor der Berechnung festgelegt):
- **B1 Widerspruch:** Kommt im Kanal ein Kennzeichen derselben Art wie im Auftrag vor (Version, 7-stelliger Hash, E-Mail, €-Betrag), aber keines mit dem Wert aus dem Auftrag, gilt der Beleg als kaputt.
- **B2 Warnwörter:** error, fail, refused, bounced, deferred, expired, pending, mismatch, unreachable, degraded, timeout, NaN, SYN-SENT, ✗, `0/N`, `0 kB`, `(0 pages)`, `dropped 0`. Diese Liste ist **informiert**: Ich kenne die Sprache des Generators.
- **B3** = B1 oder B2.

## Gesamt

| Prüfer | Fehlalarm | übersehen | Fehlerrate |
|---|---|---|---|
| B1 | 0.167 | 0.727 | 0.447 |
| B2 | 0.120 | 0.588 | 0.354 |
| B3 | 0.250 | 0.403 | 0.326 |
| Sonnet L1 (Stapel 8, low) | 0.097 | 0.065 | 0.081 |
| Sonnet L2 (Stapel 12, low) | 0.093 | 0.069 | 0.081 |
| Sonnet L3 (Stapel 12, aus) | 0.019 | 0.037 | 0.028 |

## Übersehen je Fehlerart

| Fehlerart | B1 | B2 | B3 | Sonnet L2 |
|---|---|---|---|---|
| `amount_mismatch` | 0.00 | 0.73 | 0.00 | 0.07 |
| `bounced` | 0.67 | 0.33 | 0.33 | 0.00 |
| `cache_down` | 1.00 | 0.14 | 0.14 | 0.05 |
| `column_loss` | 1.00 | 0.86 | 0.86 | 0.00 |
| `db_down` | 1.00 | 0.33 | 0.33 | 0.13 |
| `duplicates_kept` | 1.00 | 0.67 | 0.67 | 0.00 |
| `empty_attachment` | 0.46 | 0.21 | 0.00 | 0.21 |
| `row_loss` | 1.00 | 0.83 | 0.83 | 0.00 |
| `stale_process` | 0.67 | 0.33 | 0.33 | 0.00 |
| `weights_broken` | 1.00 | 0.83 | 0.83 | 0.17 |
| `wrong_recipient` | 0.00 | 1.00 | 0.00 | 0.00 |
| `zero_traffic` | 1.00 | 0.62 | 0.62 | 0.17 |

## Fehlalarm je Domäne und Kanal (B3)

| Domäne/Kanal | B3 Fehlalarm |
|---|---|
| business/delivery | 0.50 |
| business/ledger | 0.00 |
| business/smtp | 1.00 |
| coding/deploy | 0.00 |
| coding/probe | 0.42 |
| coding/sockets | 0.00 |
| research/joblog | 0.33 |
| research/output | 0.00 |
| research/validation | 0.00 |
## Deutung (Claude, nach der Berechnung)
- **Die Decke ist kein Stringvergleich.** Selbst eine informierte Heuristik, die die Sprache des Generators kennt, irrt bei 33 % der Urteile (40 % übersehen, 25 % Fehlalarm). Sonnet irrt bei 3–8 %.
- **Was Sonnet zusätzlich leistet**, sieht man an den Fehlerarten, bei denen die Heuristik versagt und Sonnet nicht: `row_loss`, `column_loss`, `duplicates_kept`, `weights_broken` und `zero_traffic`. Dort muss man **Zahlen mit dem Auftrag abgleichen** (Zeilen gegen Rohzeilen, 41 gegen 47 Spalten, Gewichtsmittel 100 gegen 1). Das ist Lesen und Rechnen, kein Wortabgleich.
- **Damit ist Groks Alternative "die Decke ist Stringvergleich" für dieses Material nicht gestützt.** Seine zweite Beobachtung bleibt stehen: Haiku übersieht ähnlich wenig. Die Leistung ist also keine Sonnet-Besonderheit, ein aktuelles Sprachmodell reicht.
- **Grenze:** Ein deterministischer Prüfer, den man *für diesen Generator* schreibt, käme auf nahezu 100 %, denn er wüsste, wo die Spuren liegen. Das sagt aber nichts über echte Prüfaufgaben. Interessant ist genau der Fall, in dem niemand die Spur vorher kennt.
- **B1 ist grob:** Fremde E-Mail-Adressen im SMTP-Log (Routinezeilen) lösen Fehlalarme aus. Eine klügere Regel würde die Queue-ID verfolgen. Das ändert das Gesamtbild nicht.
