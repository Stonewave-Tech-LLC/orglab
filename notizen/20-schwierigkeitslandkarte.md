# Schwierigkeitslandkarte: Was macht Prüfaufgaben für Sonnet 5.5 schwer?

> **Korrektur 23.10. (E-021, KORREKTUR_E021):** "Reasoning aus" bedeutet hier die Standardeinstellung mit adaptivem, verborgenem Reasoning, "low" bedeutet gedrosseltes Reasoning. Aussagen "Reasoning erhöht Fehlalarme" sind umzudrehen (H-037).

**Stand:** 22.10.2026 · **explorativ**, nicht präregistriert · Skript: `python -m orglab.landkarte`
Daten: alle Kalibrierungsläufe aus E-017 und E-019. Ungültige Läufe werden nur dort gezeigt, wo es ausdrücklich steht.
Raten mit 95-%-Wilson-Intervall. Urteile desselben Belegs über Kanäle oder Läufe sind nicht unabhängig, die Intervalle sind deshalb zu eng. Lies sie als Größenordnung.

## 1. Überblick je Lauf

| Lauf | Modus | Material | Reasoning | gültig | Fehlerrate | Fehlalarm | übersehen |
|---|---|---|---|---|---|---|---|
| E17-K1 | einzeln | v2.0 | low | nein: Rauschen veränderte Daten (Generatorfehler) | 0.094 | 0.078 | 0.111 |
| E17-K2 | einzeln | v2.1 | low | ja | 0.031 | 0.006 | 0.056 |
| E17-K3 | einzeln | v2.2 | low | ja | 0.031 | 0.022 | 0.039 |
| E17-K3-Haiku | einzeln | v2.2 | low | ja | 0.075 | 0.117 | 0.033 |
| E19-L1-v2-ungültig | Stapel 8 | v2.2 | low | nein: Routinezeilen widersprüchlich (Generatorfehler) | 0.104 | 0.162 | 0.046 |
| E19-L1-v2 | Stapel 8 | v2.3 | low | ja | 0.109 | 0.157 | 0.060 |
| E19-L2-v2 | Stapel 12 | v2.3 | low | ja | 0.102 | 0.157 | 0.046 |
| E19-L3-v2 | Stapel 12 | v2.3 | aus | ja | 0.046 | 0.037 | 0.056 |
| E19-L1-v3-mehrdeutig | Stapel 8 | v3.0 | low | nein: zero_traffic ohne übliche Last im Auftrag (mehrdeutig) | 0.106 | 0.116 | 0.097 |
| E19-L1-v3 | Stapel 8 | v3.1 | low | ja | 0.081 | 0.097 | 0.065 |
| E19-L2-v3 | Stapel 12 | v3.1 | low | ja | 0.081 | 0.093 | 0.069 |
| E19-L3-v3 | Stapel 12 | v3.1 | aus | ja | 0.028 | 0.019 | 0.037 |

Gültige Sonnet-Urteile gesamt: **3312**, davon Fehler: 215.

## 2. Übersehen je Fehlerart (Sonnet, alle gültigen Läufe)

| Fehlerart | Art der Spur | Übersehensrate [95-%-KI] |
|---|---|---|
| `db_down` | Status grün, eine Zahl widerspricht | 0.256 [0.20; 0.32] (n=195) |
| `zero_traffic` | Status grün, eine Zahl widerspricht | 0.167 [0.10; 0.27] (n=72) |
| `empty_attachment` | Status grün, eine Zahl widerspricht | 0.139 [0.08; 0.24] (n=72) |
| `amount_mismatch` | Identität mit Auftrag abgleichen (Commit, Adresse, Betrag) | 0.067 [0.02; 0.18] (n=45) |
| `cache_down` | Status grün, eine Zahl widerspricht | 0.048 [0.02; 0.13] (n=63) |
| `weights_broken` | Status grün, eine Zahl widerspricht | 0.025 [0.01; 0.05] (n=276) |
| `stale_process` | Identität mit Auftrag abgleichen (Commit, Adresse, Betrag) | 0.014 [0.00; 0.04] (n=222) |
| `row_loss` | Menge mit Auftrag abgleichen (Zeilen, Duplikate, Spalten) | 0.007 [0.00; 0.04] (n=150) |
| `bounced` | Zustand ohne Fehlerwort (zurückgestellt, ausstehend) | 0.000 [0.00; 0.02] (n=180) |
| `wrong_recipient` | Identität mit Auftrag abgleichen (Commit, Adresse, Betrag) | 0.000 [0.00; 0.01] (n=255) |
| `duplicates_kept` | Menge mit Auftrag abgleichen (Zeilen, Duplikate, Spalten) | 0.000 [0.00; 0.06] (n=63) |
| `column_loss` | Menge mit Auftrag abgleichen (Zeilen, Duplikate, Spalten) | 0.000 [0.00; 0.06] (n=63) |

## 3. Nach Art der Spur zusammengefasst

| Art der Spur | Übersehensrate |
|---|---|
| Status grün, eine Zahl widerspricht | 0.121 [0.10; 0.15] (n=678) |
| Identität mit Auftrag abgleichen (Commit, Adresse, Betrag) | 0.011 [0.01; 0.02] (n=522) |
| Menge mit Auftrag abgleichen (Zeilen, Duplikate, Spalten) | 0.004 [0.00; 0.02] (n=276) |
| Zustand ohne Fehlerwort (zurückgestellt, ausstehend) | 0.000 [0.00; 0.02] (n=180) |

## 4. Reasoning: low gegen aus (gleiches Material, Stapel 12)

| Material | Reasoning | Fehlalarm | übersehen |
|---|---|---|---|
| v2.3 | low | 0.157 [0.11; 0.21] (n=216) | 0.046 [0.03; 0.08] (n=216) |
| v2.3 | aus | 0.037 [0.02; 0.07] (n=216) | 0.056 [0.03; 0.09] (n=216) |
| v3.1 | low | 0.093 [0.06; 0.14] (n=216) | 0.069 [0.04; 0.11] (n=216) |
| v3.1 | aus | 0.019 [0.01; 0.05] (n=216) | 0.037 [0.02; 0.07] (n=216) |

## 5. Fehlalarme: wo entstehen sie? (Sonnet, Reasoning low, gültige Läufe)

| Domäne | Kanal | Fehlalarm |
|---|---|---|
| research | joblog | 0.213 [0.15; 0.29] (n=136) |
| business | ledger | 0.169 [0.12; 0.24] (n=136) |
| research | output | 0.140 [0.09; 0.21] (n=136) |
| business | smtp | 0.132 [0.09; 0.20] (n=136) |
| research | validation | 0.059 [0.03; 0.11] (n=136) |
| coding | deploy | 0.051 [0.03; 0.10] (n=136) |
| coding | sockets | 0.037 [0.02; 0.08] (n=136) |
| business | delivery | 0.022 [0.01; 0.06] (n=136) |
| coding | probe | 0.015 [0.00; 0.05] (n=136) |

## 6. Einzelbeleg gegen Stapel (Sonnet, Reasoning low, Material v2)

Achtung: Das Material unterscheidet sich zwischen den Läufen in Details (v2.1–v2.3), deshalb nur grob vergleichbar.

| Modus | Fehlalarm | übersehen |
|---|---|---|
| einzeln | 0.014 [0.01; 0.03] (n=360) | 0.047 [0.03; 0.07] (n=360) |
| Stapel 8 | 0.157 [0.11; 0.21] (n=216) | 0.060 [0.04; 0.10] (n=216) |
| Stapel 12 | 0.157 [0.11; 0.21] (n=216) | 0.046 [0.03; 0.08] (n=216) |

## 7. Subtilität der Spur (Sonnet, alle gültigen Läufe)

| subtlety | Fehlalarm | übersehen |
|---|---|---|
| 1 | 0.077 [0.06; 0.10] (n=828) | 0.037 [0.03; 0.05] (n=828) |
| 2 | 0.069 [0.05; 0.10] (n=447) | 0.082 [0.06; 0.11] (n=462) |
| 3 | 0.081 [0.06; 0.11] (n=381) | 0.055 [0.04; 0.08] (n=366) |

## 8. Position im Stapel (Sonnet, Stapel 12)

| Reasoning | Slot 1–4 | Slot 5–8 | Slot 9–12 |
|---|---|---|---|
| low | 0.090 [0.06; 0.13] (n=288) | 0.097 [0.07; 0.14] (n=288) | 0.087 [0.06; 0.13] (n=288) |
| aus | 0.028 [0.01; 0.05] (n=288) | 0.042 [0.02; 0.07] (n=288) | 0.042 [0.02; 0.07] (n=288) |

## 9. Konfidenz: Sind die Fehler sicher vorgetragen? (Sonnet, alle gültigen Läufe)

| angegebene Konfidenz | Anteil aller Urteile | Fehlerrate |
|---|---|---|
| 0.00–0.70 | 0.11 | 0.325 [0.28; 0.38] (n=348) |
| 0.70–0.85 | 0.26 | 0.080 [0.06; 0.10] (n=870) |
| 0.85–0.95 | 0.53 | 0.018 [0.01; 0.03] (n=1750) |
| 0.95–1.00 | 0.10 | 0.000 [0.00; 0.01] (n=344) |

Median-Konfidenz der falschen Urteile: 0.60 · der richtigen: 0.85

### 9b. Eskalationskurve: Mensch prüft nur Urteile unter einer Konfidenzschwelle

Bezug `notizen/14` (Verlässlichkeit pro Mensch-Minute). Annahme: Der Mensch beurteilt eskalierte Belege fehlerfrei.

| Schwelle | eskaliert (Anteil Belege) | davon gefangene Fehler | Restfehlerrate ohne Mensch |
|---|---|---|---|
| < 0.60 | 0.01 | 0.07 | 0.061 |
| < 0.70 | 0.11 | 0.53 | 0.031 |
| < 0.80 | 0.17 | 0.61 | 0.025 |
| < 0.85 | 0.37 | 0.85 | 0.010 |
| < 0.90 | 0.60 | 0.96 | 0.002 |
| < 0.95 | 0.90 | 1.00 | 0.000 |

## 10. Spezifikation: derselbe Fehler mit und ohne Sollwert im Auftrag (`zero_traffic`)

| Auftrag | Übersehensrate |
|---|---|
| ohne übliche Last (ungültiger Lauf, Ground Truth mehrdeutig) | 0.542 [0.35; 0.72] (n=24) |
| mit "normally handles ~N requests/min" | 0.167 [0.10; 0.27] (n=72) |

## 11. Haiku gegen Sonnet (gleiches Material, Einzelbeleg, E-017 K3)

| Modell | Fehlalarm | übersehen |
|---|---|---|
| Sonnet 5.5 | 0.022 [0.01; 0.06] (n=180) | 0.039 [0.02; 0.08] (n=180) |
| Haiku 5.5 | 0.117 [0.08; 0.17] (n=180) | 0.033 [0.02; 0.07] (n=180) |