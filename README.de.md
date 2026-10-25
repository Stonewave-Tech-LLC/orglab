# Emergente Organisation in Multi-Agent-Systemen

Forschungsprojekt von Neo (Stonewave), gestartet am 20.10.2026.

**Frage:** Welche Regulationsmechanismen machen eine Agenten-Organisation selbstkorrigierend und modellrobust? Und lassen sich diese Mechanismen mit einem Propose-Probe-Compose-Loop (Prinzip aus Harness²) gezielt finden?

**Stand (21.10.):**
- Das Testbed `orglab` ist gebaut und getestet.
- Die Mess-Validierung für `phantom_done` ist bestanden.
- Der Pilot E-001 ist präregistriert. Er wartet auf den Login der SDK-CLI.

## Bedienung

Alles aus dem Projektordner heraus, mit der Umgebung `.venv`.

```powershell
# einmalig: Login der im SDK enthaltenen Claude-CLI (öffnet den Browser, Abo-Account wählen, danach /exit)
& ".venv\Lib\site-packages\claude_agent_sdk\_bundled\claude.exe"     # dann: /login

.venv\Scripts\python -m pytest                                   # Tests
.venv\Scripts\python -m orglab.validate --scenario phantom_done  # Mess-Validierung (Pflicht vor Optimierung)

# Sweep: Regime vergleichen (fortsetzbar: einfach erneut starten)
.venv\Scripts\python -m orglab.sweep --experiment E-001-pilot --configs configs\regimes\A_contracts.yaml configs\regimes\B_minimal.yaml configs\regimes\C_stigmergy.yaml configs\regimes\D_constitution.yaml --domains coding business --seeds 0-2

# Optimierer: läuft bis zu 48 h, schreibt state.json, verlauf.log, bericht.md, library/ (fortsetzbar)
.venv\Scripts\python -m orglab.optimize --experiment E-010-opt --start configs\regimes\B_minimal.yaml --hours 48

.venv\Scripts\python -m orglab.analyze daten\E-001-pilot          # Auswertung neu erzeugen
```

Einen einzelnen Run lesbar machen: `python -c "from orglab.digest import digest; from pathlib import Path; print(digest(Path('daten/…/seed-000')))"`

## Austausch mit Ace

Neo hat am 21.10. darum gebeten, Ace zu informieren und ihm regelmäßig Ergebnisse zu schicken.
- **Thread:** `[ID intern]` (`send_to_ace` mit dieser `thread_id`)
- **Dateien:** über `nexus_send_text` mit derselben `thread_id`
- **Berichte:** Kopien liegen in `berichte/`
- **Regel:** Ace bekommt Projekt- und Ergebnisinformationen, aber nie Ace-Exportdaten zurück und keine Zugangsdaten.

## Wo was liegt
- `CLAUDE.md`: Arbeits- und Dokumentationsregeln, für Menschen und für Claude
- `laborbuch.md`: Chronik
- `hypothesen.md`, `entscheidungen.md`, `quellen.md`: Register
- `notizen/`: Arbeitsdokumente (Quellencheck, Problemstellung, Ace-Befund)
- `experimente/`: ein Ordner pro Experiment, Vorlage in `_vorlage/`
- `daten/`: Rohdaten, unveränderlich (Event-Logs und Ace-Export nur lokal, siehe `.gitignore`)
- `orglab/`: das Testbed (Aufbau im Docstring von `orglab/__init__.py`)
- `configs/`: Org-Configs (Regime A–D, Validierung)
- `tests/`: Tests
