"""Präregistrierte Auswertung E-018 (siehe prereg.md). Aufruf: python experimente/E-018-beleg-statt-stimme/auswertung.py"""
import csv
import random
import statistics
from pathlib import Path

from orglab.analyze import bootstrap_ci

ROOT = Path(__file__).resolve().parents[2]
rows = list(csv.DictReader(open(ROOT / "daten/E-018-beleg-statt-stimme/results.csv", encoding="utf-8")))
arm = {"B_no_human_vote": "V2a", "B_no_human_deadline": "F"}
data = {}
for r in rows:
    loss = float(r["reassigned_from_honest"] or 0) + float(r["auto_released_from_honest"] or 0)
    data[(arm[r["config_name"]], r["domain"], int(r["seed"]))] = {
        "loss": loss, "tc": float(r["true_completion"]), "votes": float(r["reassign_votes"] or 0),
        "theft": float(r["reassigned_from_honest"] or 0)}
keys = sorted({(d, s) for (_, d, s) in data})
assert len(keys) == 20 and all(("V2a", *k) in data and ("F", *k) in data for k in keys)


def one_sided_less(diffs, n=20000, seed=0):
    """P(mean <= beobachtet) unter zufälligen Vorzeichen; H1: mittlere Differenz < 0."""
    rng = random.Random(seed)
    obs = statistics.fmean(diffs)
    hits = sum(statistics.fmean([d if rng.random() < 0.5 else -d for d in diffs]) <= obs + 1e-12 for _ in range(n))
    return (hits + 1) / (n + 1)


for metric in ("loss", "tc", "votes", "theft"):
    v = [data[("V2a", *k)][metric] for k in keys]
    f = [data[("F", *k)][metric] for k in keys]
    d = [b - a for a, b in zip(v, f)]
    lo, hi = bootstrap_ci(d)
    print(f"{metric:6s} V2a={statistics.fmean(v):.3f} F={statistics.fmean(f):.3f} "
          f"Δ(F−V2a)={statistics.fmean(d):+.3f} KI[{lo:+.3f}, {hi:+.3f}]"
          + (f" p_einseitig={one_sided_less(d):.5f}" if metric == "loss" else ""))
print("Manipulationscheck: Runs V2a mit Verlust bei Ehrlichen:",
      sum(data[("V2a", *k)]["theft"] > 0 for k in keys), "/ 20")
