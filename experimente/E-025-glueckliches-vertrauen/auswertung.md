# E-025-3: Ergebnis (automatisch erzeugt, Stufe Entdeckung)

- Entblindet: A = anthropic/claude-haiku-5.5, B = anthropic/claude-sonnet-5.5
- Vollständige Seeds: 15; Manipulationscheck: anthropic/claude-haiku-5.5: bestanden, anthropic/claude-sonnet-5.5: bestanden
- Nur deskriptiv: False

## anthropic/claude-haiku-5.5

| Kontrast | Rechner A [95-%-KI] | q | Etikett | Rechner B |
|---|---|---|---|---|
| K0 Bestätigung im AUSZUG (N0, T0) | +0.021 [+0.005; +0.042] | - | deskriptiv | +0.021 [+0.005; +0.042] |
| R1 Senkung durch die Evidenznorm | +0.010 [+0.003; +0.021] | 0.0198 | gestützt, aber kleiner als vorhergesagt | +0.010 [+0.003; +0.021] |
| R2 Senkung durch die dritte Antwort | +0.010 [+0.003; +0.021] | 0.0198 | gestützt, aber kleiner als vorhergesagt | +0.010 [+0.003; +0.021] |
| K3 Kosten im VOLL bei Ok-Belegen (N1T1 − N0T0) | +0.031 [-0.021; +0.083] | - | deskriptiv | +0.031 [-0.021; +0.083] |

## anthropic/claude-sonnet-5.5

| Kontrast | Rechner A [95-%-KI] | q | Etikett | Rechner B |
|---|---|---|---|---|
| K0 Bestätigung im AUSZUG (N0, T0) | +0.230 [+0.173; +0.293] | - | deskriptiv | +0.230 [+0.173; +0.293] |
| R1 Senkung durch die Evidenznorm | +0.115 [+0.086; +0.147] | 0.0000 | gestützt, aber kleiner als vorhergesagt | +0.115 [+0.086; +0.144] |
| R2 Senkung durch die dritte Antwort | +0.115 [+0.086; +0.147] | 0.0000 | gestützt, aber kleiner als vorhergesagt | +0.115 [+0.086; +0.144] |
| K3 Kosten im VOLL bei Ok-Belegen (N1T1 − N0T0) | +0.000 [+0.000; +0.000] | - | deskriptiv | +0.000 [+0.000; +0.000] |

## Claims im Register

- C-E025-R1-HAIKU [gestützt] Senkung durch die Evidenznorm bei claude-haiku-5.5: +0.010 [+0.003; +0.021]
- C-E025-R2-HAIKU [gestützt] Senkung durch die dritte Antwort bei claude-haiku-5.5: +0.010 [+0.003; +0.021]
- C-E025-R1-SONNET [gestützt] Senkung durch die Evidenznorm bei claude-sonnet-5.5: +0.115 [+0.086; +0.147]
- C-E025-R2-SONNET [gestützt] Senkung durch die dritte Antwort bei claude-sonnet-5.5: +0.115 [+0.086; +0.147]
