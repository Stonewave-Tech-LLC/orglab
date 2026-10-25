# E-023 Auswertung (Haiku 5.5, Design E-020 v3) (automatisch erzeugt)

Vollständige Seeds: 23, gültige Prüfungen: 2208, spec-reine kaputte Belege: 83
Ausfälle je Zelle (ohne gültiges Urteil, vor dem Filtern): SP0-ZU0-AU0 0, SP0-ZU0-AU1 0, SP0-ZU1-AU0 0, SP0-ZU1-AU1 1, SP1-ZU0-AU0 0, SP1-ZU0-AU1 0, SP1-ZU1-AU0 0, SP1-ZU1-AU1 0

## Vorab festgelegte Kontraste (Übersehen, gepaart je Beleg, über die übrigen Faktoren gemittelt)

Regel: zweiseitiges 95-%-KI (Bootstrap über Belege), BH-q über V1/V2; nachgewiesen = untere Grenze > 0 und q ≤ 0,05; gestützt = nachgewiesen und Vorhersagewert nicht ausgeschlossen; widerlegt = obere Grenze < Vorhersagewert.

- **V1** SPEC 1 − 0, nur spec-reine Fehlerarten: **+0.253** [+0.202; +0.304], q = 0.0000 → Vorhersage gestützt (Effekt nachgewiesen, +0.10 nicht ausgeschlossen) (Vorhersage ≥ +0,10)
- **V2** AUSKUNFT 1 − 0, alle kaputten Belege: **-0.014** [-0.034; +0.005], q = 0.9338 → praktisch null, obere Grenze < +0,02 (Vorhersage widerlegt) (Vorhersage ≥ +0,05)
- V2 sekundär, nur spec-reine kaputte Belege: -0.006 [-0.036; +0.021]
- V2 Nebenvorhersage, getrennt berichtet: Fehlalarm AUSKUNFT 1 − 0 = +0.042 [+0.020; +0.065] (erwartet: sinkt → nicht gezeigt)
- **V3** run_check-Aufrufe AUSKUNFT 1 − 0 (ZUGANG = 1): **-0.01** [-0.01; +0.00] → nicht gestützt
- **V4** (deskriptiv, kein Kausaltest) SPEC = 1, spec-rein: Normabschnitt erhalten 252× → Übersehen 0.071; nicht erhalten 80× → Übersehen 0.963; davon ganze Seite erhalten 252×

## V5 Eskalation (Konfidenz < 0.8)

| AUSKUNFT | eskaliert | gefangene Fehler | Anteil konfidenter Fehler (≥ 0,85) |
|---|---|---|---|
| 0 | 0.22 | 0.44 | 0.41 |
| 1 | 0.26 | 0.54 | 0.39 |

## Zellen (sekundär)

| Zelle | Fehlalarm | Übersehen (alle) | Übersehen (spec-rein) | run_check | nachgeschlagen | Tokens | PPV bei 5 % |
|---|---|---|---|---|---|---|---|
| SP0-ZU0-AU0 | 0.094 | 0.065 | 0.072 | 0.00 | 0.61 | 1227 | 0.34 |
| SP0-ZU0-AU1 | 0.159 | 0.043 | 0.048 | 0.00 | 0.54 | 1295 | 0.24 |
| SP0-ZU1-AU0 | 0.000 | 0.007 | 0.012 | 3.00 | 0.45 | 1177 | 1.00 |
| SP0-ZU1-AU1 | 0.029 | 0.000 | 0.000 | 3.00 | 0.18 | 1123 | 0.64 |
| SP1-ZU0-AU0 | 0.087 | 0.080 | 0.096 | 0.00 | 0.88 | 1249 | 0.36 |
| SP1-ZU0-AU1 | 0.152 | 0.058 | 0.072 | 0.00 | 0.87 | 1282 | 0.25 |
| SP1-ZU1-AU0 | 0.007 | 0.333 | 0.470 | 3.01 | 0.51 | 1063 | 0.83 |
| SP1-ZU1-AU1 | 0.014 | 0.326 | 0.506 | 3.00 | 0.38 | 1051 | 0.71 |

ZUGANG 1 − 0 (Übersehen, alle kaputten, keine gerichtete Vorhersage): +0.105 [+0.056; +0.150]

Übersehen je Fehlerart (über alle Zellen):

- amount_mismatch: 0.000 (n = 88)
- bounced: 0.000 (n = 88)
- cache_partial (spec-rein): 0.198 (n = 96)
- column_loss (spec-rein): 0.010 (n = 96)
- db_down: 0.227 (n = 88)
- duplicates_partial (spec-rein): 0.011 (n = 88)
- low_traffic (spec-rein): 0.396 (n = 96)
- row_loss: 0.000 (n = 88)
- stale_process: 0.000 (n = 88)
- weights_misscaled (spec-rein): 0.010 (n = 96)
- wrong_contact (spec-rein): 0.229 (n = 96)
- wrong_terms (spec-rein): 0.250 (n = 96)

Generatorfehler-Regel (≥ 80 % der Zellen falsch): keine
Kosten: 2.09 $

## Vorab festgelegt: ohne die einzeln nicht entscheidbaren Belege (E-020 Materialbefund)

Ausgeschlossen (8): coding-fail_moderate-6005, coding-fail_moderate-6006, coding-fail_moderate-6017, coding-fail_moderate-6018, coding-fail_subtle-6000, coding-fail_subtle-6011, coding-fail_subtle-6012, coding-fail_subtle-6023

- V1 +0.250 [+0.199; +0.304] → Vorhersage gestützt (Effekt nachgewiesen, +0.10 nicht ausgeschlossen)
- V2 -0.010 [-0.029; +0.010] → praktisch null, obere Grenze < +0,02 (Vorhersage widerlegt)

## Profil je Modell (Manipulationscheck, deskriptiv)

| Modell | Prüfungen | Ausfälle | Tokens (Median) | nachgeschlagen bei SPEC=1 | run_check bei ZUGANG=1 | Fehlalarm | Übersehen |
|---|---|---|---|---|---|---|---|
| Haiku 5.5 | 2304 | 1 | 1092 | 0.66 | 3.00 | 0.068 | 0.111 |
| Sonnet 5.5 (E-020) | 2304 | 0 | 754 | 0.97 | 3.00 | 0.000 | 0.048 |

## Wechselwirkung Modell × Faktor (alle Belege): Haiku-Effekt − Sonnet-Effekt, gepaart je Beleg

| Kontrast | Effekt Haiku | Effekt Sonnet | Differenz [95-%-KI] | Belege |
|---|---|---|---|---|
| V1 SPEC (spec-rein) | +0.253 | +0.006 | **+0.247** [+0.193; +0.298] | 83 |
| V2 AUSKUNFT | -0.014 | -0.016 | **+0.002** [-0.020; +0.022] | 138 |
| ZUGANG | +0.105 | -0.085 | **+0.190** [+0.147; +0.237] | 138 |

## Wechselwirkung Modell × Faktor (ohne die einzeln nicht entscheidbaren Belege): Haiku-Effekt − Sonnet-Effekt, gepaart je Beleg

| Kontrast | Effekt Haiku | Effekt Sonnet | Differenz [95-%-KI] | Belege |
|---|---|---|---|---|
| V1 SPEC (spec-rein) | +0.250 | +0.006 | **+0.244** [+0.190; +0.297] | 79 |
| V2 AUSKUNFT | -0.010 | -0.013 | **+0.004** [-0.015; +0.023] | 130 |
| ZUGANG | +0.137 | -0.033 | **+0.169** [+0.127; +0.212] | 130 |