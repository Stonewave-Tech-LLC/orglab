# E-021: Ergebnis – Kontrast bestätigt, Deutung umgedreht

- **Lauf:** 23.10.2026, ~00:45–01:00. 144 Aufrufe, 1.728 Urteile, 0 fehlend. Kosten 3,19 $.
- **Präregistrierung:** `prereg.md` (Commit a257dbf vor dem Lauf). Auswertung: `orglab/e021.py` (eingefroren), Rohausgabe `daten/E-021-reasoning-fehlalarme/auswertung.md`.

## Vorab festgelegte Tests

| Test | Ergebnis | Kriterium |
|---|---|---|
| **P1** Δ Fehlalarm (`low` − ohne Parameter), Belegebene | **+0,069**, untere Grenze des einseitigen 95-%-KI **+0,049**, p < 0,0001. FA 0,102 gegen 0,032 | erfüllt, relevant (≥ +0,05) |
| **P2** Δ Übersehen (ohne Parameter − `low`) | **−0,007**, obere Grenze +0,007 | erfüllt (≤ +0,03) |
| **Manipulationscheck** Completion-Tokens `low` > ohne Parameter | **gescheitert:** `low` 255, ohne Parameter 832 | **nicht erfüllt, und umgekehrt** |

## Was der gescheiterte Manipulationscheck bedeutet
Nachprüfung direkt nach dem Lauf (zwei kleine Proben, zusammen ~0,70 $, im Ledger als "E-021 Manipulationsprüfung"):
1. OpenRouter meldet für `anthropic/claude-sonnet-5.5`: **"Reasoning is mandatory for this endpoint and cannot be disabled."** Einen Zustand "ohne Reasoning" gibt es nicht.
2. Auf denselben 6 Stapeln ergab sich:

| Einstellung | Completion-Tokens (Median, Spanne) | Fehlalarm |
|---|---|---|
| `effort: low` | 257 (244–257) | 0,130 |
| ohne Parameter | 566 (257–1.206) | 0,033 |
| `effort: high` | 533 (257–1.371) | 0,033 |

   Die gemeldeten `reasoning_tokens` sind immer 0. Das Denken ist verborgen, wird aber über die Completion-Tokens abgerechnet.
3. **Ohne Parameter denkt Sonnet adaptiv, etwa so viel wie bei `high`. `low` deckelt das Denken auf fast null.**

**Damit ist die Beschriftung "Reasoning low gegen aus" in E-019 und E-021 falsch, und zwar umgekehrt.** Tatsächlich verglichen wurde **"gedrosseltes Reasoning" gegen "normales, adaptives Reasoning"**.

## Einordnung
- **Der vorab festgelegte Kontrast ist auf frischen Seeds bestätigt:** `effort: low` erzeugt deutlich mehr Fehlalarme als die Standardeinstellung, bei gleicher Übersehensrate.
- **H-036 in ihrem Wortlaut ("Reasoning *erhöht* die Fehlalarmrate") ist nicht bestätigt.** Die Manipulation war invertiert. Die Daten zeigen das Gegenteil: **Mehr Denken senkt die Fehlalarme.**
- **Neue Hypothese H-037:** "Gedrosseltes Reasoning erhöht die Fehlalarmrate von Prüfern gegenüber normalem Reasoning, ohne die Übersehensrate zu senken."
  - **Status: gestützt.** Der Kontrast war vorab festgelegt und lief auf frischen Seeds. Die Deutung stammt aber aus dem Manipulationscheck *nach* dem Lauf.
  - Eine saubere Bestätigung mit **gemessenem** Reasoning-Umfang (z. B. low / medium / high, Tokens als Manipulationscheck) steht aus.
- **Praktisch für Wave:**
  - Prüfer mit gedrosseltem Reasoning alarmieren 3- bis 4-mal so oft unnötig.
  - Bei 5 % Prävalenz ist nur etwa jeder dritte ihrer Alarme echt (PPV 0,32 gegen 0,60 bei Standardeinstellung).
  - "Sparen am Denken" kostet bei Prüfern Menschen-Minuten.

## Sekundär
- **S1:** Konfidenz < 0,80 eskaliert bei `low` 16 % und fängt 62 % der Fehler, bei Standard 10 % und 37 %. Die Erwartung "≥ 50 % bei ≤ 25 %" ist nur für `low` erfüllt. Bei Standardeinstellung sind die verbleibenden Fehler seltener und weniger an niedrige Konfidenz gebunden.
- **S2:** PPV bei 5 % Prävalenz: `low` 0,32, Standard 0,60.
- **S3:** Der Effekt zeigt sich in fast allen Kanälen, am stärksten bei business/smtp und business/ledger.
- **Generatorfehler-Regel:** kein ok-Beleg in beiden Armen in allen Kanälen als kaputt beurteilt.

## Lehre (für den Blog)
Ein vorab festgelegter Manipulationscheck hat eine Fehldeutung gefangen, die zwei Experimente lang (E-019, E-021) in allen Notizen stand. Grok hatte genau diese Möglichkeit genannt (Gutachten 1, §4b): "low" und "aus" sind vielleicht nicht dasselbe Modell mit einem Schalter. **Ohne Manipulationscheck hätten wir das Gegenteil der Wahrheit "bestätigt".**

## Grenzen
- Gilt für Sonnet 5.5 über OpenRouter, Stapel 12, synthetisches Material v3.1.
- Was "Standard" genau bedeutet (adaptives Denken, Budget), ist Anbietersache und nicht dokumentiert.
- Kritiker-Unabhängigkeit offen (Claude prüft Claude).
