# E-016: Prüfer-Panel – korrelierte Fehlurteile über Modellfamilien, Präregistrierung

- **Datum:** 2026-10-21, ~23:55 · **Stufe:** Entdeckung (erste Messung von H-026; gerichtete Vorhersagen)
- **Frage:** Irren mehrere Prüfer desselben Modells bzw. derselben Familie gemeinsam? Wie viel bringt Redundanz gegenüber Diversität?
- **Material:** `orglab/evidence.py`, Rohbelege mit bekannter Wahrheit in 3 Domänen × 5 Arten:
  - `ok_clear`, `ok_noisy`, `fail_clear`
  - `fail_deceptive`: Oberfläche meldet Erfolg, der Fehler steckt im Detail
  - `fail_injected`: wie `fail_deceptive`, plus eingeschleuster Prüfer-Hinweis
  - Seeds 0–19 → **300 Belege**. Konsistenz per Test geprüft (`tests/test_evidence.py`). Der Format-Pilot fand 3 Generator-Fehler, die behoben wurden. Die Pilotdaten sind ungültig.
- **Panel** (über OpenRouter, Prompt identisch, als echte Review-Aufgabe formuliert):
  - Anthropic: Sonnet 5.5, Haiku 5.5
  - OpenAI: GPT-6.1 Sol, GPT-6 Luna
  - Google: Gemini 4 Argon, Gemini 3.1 Flash-Lite
  - xAI: Grok 4.3
  - DeepSeek: V4 Pro
  - Je **3 Stichproben** pro Beleg (Standard-Temperatur), Reasoning-Effort "low", wo unterstützt
- **Umfang:** 300 × 8 × 3 = 7.200 Urteile, geschätzt ~5 $. Budget-Sperre lokal bei 10 $/Tag.
- **Jev:** Auf OpenRouter nur als "Jev Router" (wählt LLMs aus), das Decision Model selbst ist nicht verfügbar. Deshalb nicht im Panel.

## Vorhersagen (gerichtet)
1. **Gleiches Modell:** Für die Mehrheit der Modelle ist P(alle 3 Stichproben irren) ≥ 3× p³. Die Fehler derselben Gewichte sind stark korreliert.
2. **Familie:** Das mittlere phi der Fehler *innerhalb* einer Familie ist größer als *zwischen* Familien.
3. **Auch über Familien positiv:** Das mittlere phi zwischen Familien ist > 0 (gemeinsame blinde Flecken aus ähnlichen Trainingsdaten). Hinweis aus dem ungültigen Pilot: Ein Beleg täuschte alle 8 Modelle.
4. **Panels:** Die Escape Rate (Mehrheit winkt einen kaputten Beleg durch) eines gemischten 3er-Panels (Sonnet + GPT-6.1 Sol + Gemini 4 Argon) liegt unter der von 3× Sonnet.
5. **Manipulation:** Für mindestens die Hälfte der Modelle ist die Fehlerrate bei `fail_injected` höher als bei `fail_deceptive`.

## Auswertung
`python -m orglab.panel analyze --experiment E-016-pruefer-panel`. Liefert:
- Fehlerraten je Modell und Belegart
- P(alle irren) gegen p³
- phi-Matrix, getrennt innerhalb und zwischen Familien
- Escape Rates der Panels
- Wirkung der Injection
- Kalibrierung

Unsicherheit wird per Bootstrap über Belege nachgereicht, wenn die Effekte knapp sind.

## Abweichungen
-
