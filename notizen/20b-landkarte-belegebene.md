# Schwierigkeitslandkarte auf Belegebene (Neuberechnung nach Grok-Gutachten)

> **Korrektur 23.10. (E-021, KORREKTUR_E021):** "Reasoning aus" bedeutet hier die Standardeinstellung mit adaptivem, verborgenem Reasoning, "low" bedeutet gedrosseltes Reasoning. Aussagen "Reasoning erhöht Fehlalarme" sind umzudrehen (H-037).

**Stand:** 23.10.2026, nachts · **explorativ** · Skript `python -m orglab.landkarte_belege` · Daten wie `notizen/20`.
Einheit ist der **Beleg** (Fehlerrate je Beleg über seine Urteile gemittelt), Bootstrap über Belege (2000 Ziehungen), getrennt je Lauf. Damit sind die Intervalle ehrlicher als in `notizen/20`.

## 1. Je Lauf: Fehlalarm und Übersehen auf Belegebene

| Lauf | Fehlalarm (ok-Belege) | Übersehen (kaputte Belege) | Urteile je Beleg |
|---|---|---|---|
| E17-K2 | 0.006 [0.000; 0.017] (Belege=60) | 0.056 [0.022; 0.100] (Belege=60) | 3.0 |
| E17-K3 | 0.022 [0.006; 0.044] (Belege=60) | 0.039 [0.011; 0.072] (Belege=60) | 3.0 |
| E19-L1-v2 | 0.157 [0.102; 0.218] (Belege=72) | 0.060 [0.032; 0.093] (Belege=72) | 3.0 |
| E19-L1-v3 | 0.097 [0.056; 0.144] (Belege=72) | 0.065 [0.037; 0.102] (Belege=72) | 3.0 |
| E19-L2-v2 | 0.157 [0.116; 0.204] (Belege=72) | 0.046 [0.023; 0.074] (Belege=72) | 3.0 |
| E19-L2-v3 | 0.093 [0.056; 0.130] (Belege=72) | 0.069 [0.042; 0.102] (Belege=72) | 3.0 |
| E19-L3-v2 | 0.037 [0.014; 0.065] (Belege=72) | 0.056 [0.028; 0.088] (Belege=72) | 3.0 |
| E19-L3-v3 | 0.019 [0.000; 0.042] (Belege=72) | 0.037 [0.014; 0.065] (Belege=72) | 3.0 |

## 2. Reasoning low gegen aus, gepaart über identische Belege (Stapel 12)

Differenz = low − aus je Beleg. Positiv heißt: mit Reasoning mehr Fehler.

| Material | Δ Fehlalarm (ok-Belege) | Δ Übersehen (kaputte Belege) |
|---|---|---|
| v2.3 | 0.120 [0.079; 0.167] (Belege=72) | -0.009 [-0.028; 0.009] (Belege=72) |
| v3.1 | 0.074 [0.037; 0.116] (Belege=72) | 0.032 [0.005; 0.060] (Belege=72) |

## 3. Eskalation nach Konfidenz: Schwelle auf v2 gewählt, auf v3 geprüft

Gewählt wurde die höchste Schwelle mit höchstens 25% Eskalation auf v2: **Konfidenz < 0.80**.

| Daten | eskaliert | gefangene Fehler | Restfehlerrate |
|---|---|---|---|
| v2 (Training) | 0.20 | 0.63 | 0.024 |
| v3 (Test) | 0.14 | 0.57 | 0.027 |

Getrennt nach Modus und Reasoning (alle Läufe, gleiche Schwelle):

| Modus | Reasoning | eskaliert | gefangene Fehler |
|---|---|---|---|
| einzeln | low | 0.23 | 0.41 |
| Stapel 8 | low | 0.18 | 0.68 |
| Stapel 12 | low | 0.17 | 0.59 |
| Stapel 12 | aus | 0.12 | 0.59 |

## 4. Konfidenz gegen eine beobachtbare Regel bei ähnlichem Eskalationsanteil

Die Regel eskaliert ganze Kanäle (Domäne × Kanal), sortiert nach Fehlerrate auf v2. Ein Kanal umfasst etwa 11 % der Urteile, deshalb werden 1, 2 und 3 Kanäle gezeigt. Reihenfolge der Kanäle: coding/deploy, research/joblog, business/ledger.

| Daten | Regel | eskaliert | gefangene Fehler |
|---|---|---|---|
| v2 (Training) | Konfidenz < 0.80 | 0.20 | 0.63 |
| v2 (Training) | Kanal-Regel (1 Kanäle) | 0.11 | 0.33 |
| v2 (Training) | Kanal-Regel (2 Kanäle) | 0.22 | 0.53 |
| v2 (Training) | Kanal-Regel (3 Kanäle) | 0.33 | 0.65 |
| v3 (Test) | Konfidenz < 0.80 | 0.14 | 0.57 |
| v3 (Test) | Kanal-Regel (1 Kanäle) | 0.11 | 0.17 |
| v3 (Test) | Kanal-Regel (2 Kanäle) | 0.22 | 0.34 |
| v3 (Test) | Kanal-Regel (3 Kanäle) | 0.33 | 0.48 |

## 5. Prävalenz: dieselben Läufe bei 50 % gegen 5 % kaputter Belege (Umgewichtung)

PPV = Anteil echter Fehler unter den 'kaputt'-Urteilen des Prüfers. **Achtung (Grok-Gutachten 2):** Die Spalte 'gefangene Fehler' ist der Anteil *aller* Fehler (Übersehen und Fehlalarm), den die Eskalation erfasst. Er verschiebt sich mit der Zusammensetzung und ist **keine** Sensitivität. Maßgeblich für die Praxis ist die PPV.

| Modus/Reasoning | Prävalenz | eskaliert | gefangene Fehler | PPV der Alarme |
|---|---|---|---|---|
| einzeln / low | 50% | 0.23 | 0.41 | 0.99 |
| einzeln / low | 5% | 0.15 | 0.88 | 0.78 |
| Stapel 12 / low | 50% | 0.17 | 0.59 | 0.88 |
| Stapel 12 / low | 5% | 0.20 | 0.70 | 0.28 |
| Stapel 12 / aus | 50% | 0.12 | 0.59 | 0.97 |
| Stapel 12 / aus | 5% | 0.12 | 0.73 | 0.64 |