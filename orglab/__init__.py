"""orglab: Testbed für emergente Organisation in Multi-Agent-Systemen.

Aufbau:
  events     – unveränderliches Event-Log (JSONL), die Datengrundlage jeder Auswertung
  config     – Org-Konfiguration (YAML), die unabhängige Variable und das Einzige, was der Optimierer ändern darf
  world      – Weltzustand: Arbeitspakete, Nachrichten, Board, simulierter Mensch
  tools      – die Werkzeuge, mit denen Agenten in der Welt handeln
  scenarios  – Mechanismen mit bekannter Ground Truth, in mehreren Domänen instanziiert (D-005)
  backends   – wer die Agenten spielt: Claude Agent SDK oder geskriptete Policies (Tests, Validierung)
  runner     – ein Run = Szenario × Config × Seed × Modell
  sweep      – viele Runs, parallel, fortsetzbar
  metrics    – generische Metriken aus dem Event-Log
  analyze    – Statistik über Runs (Bootstrap-CIs, Permutationstests)
  validate   – Mess-Validierung: trennt die Messung gute von schlechter Organisation?
"""

__version__ = "0.1.0"
