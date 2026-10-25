# Harness-Inventur: Was schicken Grok-CLI und Claude Agent SDK wirklich mit?

**Stand:** 23.10.2026, ~00:20 · Erster Schritt zum **Äquivalenz-Protokoll** für Team-Spiele mit Grok über die CLI (Neos Wunsch: Herstellerharness statt API, aber vorsichtig bei den Startbedingungen).

## Aufbau
- **Ein** Welt-Werkzeug `inspect_item` als stdio-MCP-Server. Er protokolliert jeden Aufruf; Code in `notizen/26-inventur-code/`.
- **Ein** Zug: Systemprompt mit Marker (28 Tokens), Aufgabe: "Check work item A-1 with your tool …"
- **Grok:** Grok Build CLI 1.0.62, `-m grok-4.7`, headless, leerer Ordner mit `.grok/config.toml`, `--debug-file`
- **Claude:** Claude Agent SDK 0.2.169, Optionen wie `orglab/backends/agent_sdk.py` (`tools=[]`, `setting_sources=[]`, eigener Systemprompt), aber mit demselben stdio-MCP-Server statt des In-Process-Servers

## Befunde

| # | Thema | Grok-CLI | Claude Agent SDK | Folge |
|---|---|---|---|---|
| 1 | **Projekt-MCP-Server** | **übersprungen** ("folder untrusted"). Das Modell meldete "no tool available" und suchte im Workspace | verbunden | Grok braucht `GROK_FOLDER_TRUST=0` (nur für diesen Prozess) oder `--trust` (schreibt eine dauerhafte Freigabe in `~/.grok/trusted_folders.toml`) |
| 2 | **Werkzeug-Allowlist** | `--tools world__inspect_item` wird **nicht erkannt**, Grok behält stillschweigend den **vollen Werkzeugkasten** inklusive Shell | `allowed_tools` wirkt, nur das MCP-Werkzeug ist da | Bei Grok stattdessen `--disallowed-tools` mit allen eingebauten Werkzeugen. **Ohne das hätte ein Grok-Agent Shell-Zugriff gehabt.** |
| 3 | **Freigaben** | Die globale Grok-Config steht auf `permission_mode = "always-approve"` | `permissionMode: default` | Zusammen mit Befund 2 ein **Sicherheitsrisiko**. Bei Grok immer die eingebauten Werkzeuge entfernen. |
| 4 | **Versteckter Kontext** | auch nach Entfernen der eingebauten Werkzeuge noch: Werkzeugdefinitionen 5.680 Tokens, 19 Skills 1.988 Tokens, Workflows 176. **Zusammen ≈ 7.800 Tokens.** Unser MCP-Werkzeug hat 108, unser Systemprompt 28. | erster Request: **≈ 11.700 Tokens** Cache-Erzeugung, obwohl unser Prompt plus Werkzeug ≈ 150 Tokens sind. Die Init-Nachricht listet 19 Skills, ~55 Slash-Befehle und 5 Subagenten (aus Neos Plugins und eingebaut). | **Beide Hersteller schicken 8.000–12.000 Tokens eigenen Kontext mit, inhaltlich verschieden.** "Gleiche Startbedingungen" sind über die Herstellerharnesses nicht erreichbar, nur dokumentierbar. |
| 5 | **Sprache** | antwortete auf Englisch | antwortete auf einen englischen Prompt **auf Deutsch** | Es gibt einen nutzerbezogenen Einfluss trotz `setting_sources=[]`. Die Quelle ist noch nicht gefunden (kein `~/.claude/CLAUDE.md`, keine `language` in `settings.json`). **Bisherige Experimente:** 3 E-018-Runs geprüft, 0 deutsche und ~270 englische Wörter in Agentennachrichten. In den Spielen wirkt es also offenbar nicht, aber der Mechanismus ist ungeklärt. |
| 6 | **Gedächtnis** | aus (Standard; `--no-memory`; "stays off in temporary directories"). Global leer. Ein Workspace "neoer" mit 11 Beobachtungen vom 18.10., nicht aus unseren Läufen | – | Für Experimente immer `--no-memory` setzen und einen eigenen Ordner verwenden |
| 7 | **Modell** | angefordert `grok-4.7`, im Request so gesetzt. Ein interner Kontext-Snapshot nennt aber `grok-4.6`. Es gibt auch eine Variante "grok-4.7-build-fast". | Init: `claude-sonnet-5-5` | Bei Grok ist noch ungeklärt, welches Modell antwortet. **Die Modell-ID der Antwort pro Aufruf loggen.** |
| 8 | **Reasoning** | Standard "high", Zusammenfassungen "low" | SDK-Standard (in den Experimenten "medium") | nicht vergleichbar, nur innerhalb eines Modells variieren |
| 9 | **Kompaktierung** | automatisch ab 85 % Kontext, 1 Kompaktierung erlaubt | eigene Autokompaktierung | Kurze Runden halten, Kompaktierungs-Ereignisse loggen |
| 10 | **Freigaben pro Ordner** | Folder-Trust schaltet MCP, Hooks, Projektanweisungen und Projekt-Skills gemeinsam frei | – | Mit `GROK_FOLDER_TRUST=0` ist auch das Laden von Projekt-Skills und Hooks aus dem Ordner offen. Der Ordner muss deshalb leer sein. |

## Was das für "gleiche Startbedingungen" heißt
1. **Gleich machbar:** Welt, Werkzeug (identischer stdio-MCP-Server), Systemprompt, Aufgabe, Rundenlogik, Gedächtnis aus, keine eingebauten Werkzeuge.
2. **Nicht gleich machbar, nur messbar und dokumentierbar:**
   - der versteckte Herstellerkontext (≈ 8.000 gegen ≈ 12.000 Tokens, verschiedene Inhalte)
   - Reasoning-Semantik
   - Kompaktierung
   - Modellrouting
3. **Teilweise reduzierbar**, aber nur über **dauerhafte Änderungen an deinen Tool-Configs**, deshalb deine Entscheidung:
   - Grok: Skills über `[skills]` in `~/.grok/config.toml` abschalten
   - Claude: Plugins und Skills für die SDK-Sitzungen abschalten (Mechanismus noch zu prüfen)
4. **Die ehrliche Formulierung jedes CLI-Ergebnisses:** "Modell X *in seinem Herstellerharness* (Konfiguration siehe Inventur)". Kein reiner Modellvergleich. Für den reinen Modellvergleich bleibt der API-Weg (OpenRouter, identischer Kontext).

## Entscheidung (Neo, 23.10.)
Der versteckte Herstellerkontext bleibt, wie er ist, und wird dokumentiert. Ergebnisse über die CLI werden als "Modell *im Herstellerharness*" formuliert. Ein Universalharness mit verschiedenen Modellen steht auf dem Parkplatz (`notizen/parkplatz.md`).

## Offen
- Herkunft der deutschen Antwort im SDK
- Welches Grok-Modell tatsächlich antwortet (Antwort-Metadaten)
- Wie man Skills und Plugins in beiden Harnesses abschaltet, ohne Neos Arbeitsumgebung zu verändern (z. B. eigenes `HOME` bzw. Config-Verzeichnis nur für Experimente)
- Inventur mit einem vollständigen Team-Zug (4 Agenten, mehrere Runden, `--resume`)
