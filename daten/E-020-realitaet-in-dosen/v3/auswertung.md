# E-020 v3 Auswertung (automatisch erzeugt)

Vollständige Seeds: 24, gültige Prüfungen: 2304, spec-reine kaputte Belege: 84
Ausfälle je Zelle (ohne gültiges Urteil, vor dem Filtern): SP0-ZU0-AU0 0, SP0-ZU0-AU1 0, SP0-ZU1-AU0 0, SP0-ZU1-AU1 0, SP1-ZU0-AU0 0, SP1-ZU0-AU1 0, SP1-ZU1-AU0 0, SP1-ZU1-AU1 0

## Vorab festgelegte Kontraste (Übersehen, gepaart je Beleg, über die übrigen Faktoren gemittelt)

Regel: zweiseitiges 95-%-KI (Bootstrap über Belege), BH-q über V1/V2; nachgewiesen = untere Grenze > 0 und q ≤ 0,05; gestützt = nachgewiesen und Vorhersagewert nicht ausgeschlossen; widerlegt = obere Grenze < Vorhersagewert.

- **V1** SPEC 1 − 0, nur spec-reine Fehlerarten: **+0.006** [+0.000; +0.018], q = 0.7324 → praktisch null, obere Grenze < +0,02 (Vorhersage widerlegt) (Vorhersage ≥ +0,10)
- **V2** AUSKUNFT 1 − 0, alle kaputten Belege: **-0.016** [-0.033; -0.002], q = 1.0000 → praktisch null, obere Grenze < +0,02 (Vorhersage widerlegt) (Vorhersage ≥ +0,05)
- V2 sekundär, nur spec-reine kaputte Belege: +0.000 [+0.000; +0.000]
- V2 Nebenvorhersage, getrennt berichtet: Fehlalarm AUSKUNFT 1 − 0 = +0.000 [+0.000; +0.000] (erwartet: sinkt → nicht gezeigt)
- **V3** run_check-Aufrufe AUSKUNFT 1 − 0 (ZUGANG = 1): **-0.00** [-0.01; +0.00] → nicht gestützt
- **V4** (deskriptiv, kein Kausaltest) SPEC = 1, spec-rein: Normabschnitt erhalten 336× → Übersehen 0.042; nicht erhalten 0× → Übersehen nan; davon ganze Seite erhalten 336×

## V5 Eskalation (Konfidenz < 0.8)

| AUSKUNFT | eskaliert | gefangene Fehler | Anteil konfidenter Fehler (≥ 0,85) |
|---|---|---|---|
| 0 | 0.08 | 0.38 | 0.50 |
| 1 | 0.08 | 0.17 | 0.48 |

## Zellen (sekundär)

| Zelle | Fehlalarm | Übersehen (alle) | Übersehen (spec-rein) | run_check | nachgeschlagen | Tokens | PPV bei 5 % |
|---|---|---|---|---|---|---|---|
| SP0-ZU0-AU0 | 0.000 | 0.097 | 0.071 | 0.00 | 0.86 | 724 | 1.00 |
| SP0-ZU0-AU1 | 0.000 | 0.069 | 0.071 | 0.00 | 0.81 | 740 | 1.00 |
| SP0-ZU1-AU0 | 0.000 | 0.014 | 0.000 | 3.00 | 1.00 | 850 | 1.00 |
| SP0-ZU1-AU1 | 0.000 | 0.000 | 0.000 | 3.00 | 1.00 | 855 | 1.00 |
| SP1-ZU0-AU0 | 0.000 | 0.097 | 0.083 | 0.00 | 0.95 | 703 | 1.00 |
| SP1-ZU0-AU1 | 0.000 | 0.090 | 0.083 | 0.00 | 0.94 | 731 | 1.00 |
| SP1-ZU1-AU0 | 0.000 | 0.014 | 0.000 | 3.00 | 1.00 | 856 | 1.00 |
| SP1-ZU1-AU1 | 0.000 | 0.000 | 0.000 | 3.00 | 1.00 | 847 | 1.00 |

ZUGANG 1 − 0 (Übersehen, alle kaputten, keine gerichtete Vorhersage): -0.082 [-0.127; -0.042]

Übersehen je Fehlerart (über alle Zellen):

- amount_mismatch: 0.000 (n = 96)
- bounced: 0.000 (n = 96)
- cache_partial (spec-rein): 0.021 (n = 96)
- column_loss (spec-rein): 0.000 (n = 96)
- db_down: 0.302 (n = 96)
- duplicates_partial (spec-rein): 0.000 (n = 96)
- low_traffic (spec-rein): 0.250 (n = 96)
- row_loss: 0.000 (n = 96)
- stale_process: 0.000 (n = 96)
- weights_misscaled (spec-rein): 0.000 (n = 96)
- wrong_contact (spec-rein): 0.000 (n = 96)
- wrong_terms (spec-rein): 0.000 (n = 96)

Generatorfehler-Regel (≥ 80 % der Zellen falsch): keine
Kosten: 34.00 $

## Sensitivitätsanalyse ohne Grenzfälle ['coding-fail_moderate-6021'] (vorab festgelegt)

- V1 +0.006 [+0.000; +0.018] · V2 -0.016 [-0.035; -0.002] · vollständige Seeds 24