# E-024 Pilot (nur Technik), 19:37

- Seeds 1600–1601, beide Modelle, 384 Prüfungen, 3,02 $, Log `daten/E-024-bestaetigung-massstab/pilot.log`
- **Kriterien:**
  - Ausfälle 0 in allen Zellen und Modellen (Kriterium ≤ 5 %): erfüllt
  - `run_check` bei ZUGANG=1: Haiku 3,01, Sonnet 3,00: erfüllt
  - Feld `model` in allen Zeilen (192 + 192): erfüllt
  - **Probe-Verblindung** mit Wegwerf-Schlüssel in einem Testordner (Scratchpad, nicht im Repo):
    - Arme A/B, Tokens, Kosten und Antworttext entfernt
    - `e024.analyze_blind` läuft ohne Modellnamen im Text, nur deskriptiv (unter 16 Seeds)
    - erfüllt
  - 3 Transkripte gelesen (Ziehung Seed 2024): erfüllt. Werkzeugantworten kommen an, die Begründungen beziehen sich auf die Belege.
- Fehlerraten nicht angesehen.
