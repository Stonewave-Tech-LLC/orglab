"""Audit: findet Runs mit fehlerhaften Agenten-Zügen (z.B. Session-Limit). Vor jeder Auswertung laufen lassen:
  python -m orglab.audit daten
"""
import json
import sys
from collections import Counter
from pathlib import Path

root = Path(sys.argv[1])
bad = []
for m in root.rglob("metrics.json"):
    d = json.loads(m.read_text(encoding="utf-8"))
    if d.get("turn_errors", 0) > 0:
        bad.append((m.parent.relative_to(root).as_posix(), d["turn_errors"], d.get("end_reason"), d.get("true_completion")))
print(len(bad))
print(Counter(b[0].split("/")[0] for b in bad))
for b in sorted(bad):
    print(b)
