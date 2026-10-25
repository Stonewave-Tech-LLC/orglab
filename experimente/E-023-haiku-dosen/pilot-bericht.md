# E-023 Pilot (nur Technik), 16:08

- Seeds 1400–1401, 192 Prüfungen, `anthropic/claude-haiku-5.5`, 0,18 $, Log `daten/E-023-haiku-dosen/pilot.log`
- **Kriterien:**
  - Ausfälle 0 in allen Zellen (Kriterium ≤ 5 %): erfüllt
  - `run_check` 3,0 je Prüfung in jeder ZUGANG=1-Zelle: erfüllt
  - 3 Transkripte gelesen (Ziehung Seed 2023): erfüllt. Werkzeugantworten kommen an, Haiku gleicht mit Runbook-Werten ab.
- **Beschreibend (keine Fehlerraten):** Nachgeschlagen wurde bei SPEC=1 in 83 % (ZUGANG=0) bzw. 38–50 % (ZUGANG=1) der Prüfungen, bei SPEC=0 in 21–58 %. Mit Kanälen schlägt Haiku also seltener nach. Sonnet lag in E-020 bei 81–100 %.
- **Offen vermerkt:** Im gezogenen Transkript `business-fail_moderate-1401` (SPEC=1, ZUGANG=1) urteilte Haiku ohne Nachschlagen "funktioniert". Das ist beim Pflicht-Lesen zwangsläufig gesehen worden. Es fließt in keine Vorhersage ein, Präregistrierung und Schwellen bleiben unverändert.
- Hauptlauf gestartet.
