"""Statistik über Runs: sammeln, zusammenfassen, vergleichen.

Bewusst ohne numpy/scipy: Bootstrap-Konfidenzintervalle und Permutationstests reichen für
unsere Zellgrößen und sind leicht nachzuvollziehen.
"""

from __future__ import annotations

import csv
import json
import random
import statistics
from pathlib import Path
from typing import Any, Iterable

KEYS = ("config_name", "config_hash", "domain", "scenario", "seed", "model")


def collect(exp_dir: Path) -> list[dict[str, Any]]:
    rows = []
    for mpath in sorted(exp_dir.rglob("metrics.json")):
        run = json.loads((mpath.parent / "run.json").read_text(encoding="utf-8"))
        metrics = json.loads(mpath.read_text(encoding="utf-8"))
        if metrics.get("turn_errors", 0) > 0:   # Schutz: Runs mit ausgefallenen Agenten-Zügen nie auswerten
            print(f"[analyze] WARNUNG: übersprungen (turn_errors={metrics['turn_errors']}): {mpath.parent}")
            continue
        rows.append({**{k: run.get(k) for k in KEYS}, "run_dir": str(mpath.parent.relative_to(exp_dir)), **metrics})
    return rows


def write_csv(rows: list[dict[str, Any]], path: Path) -> None:
    if not rows:
        return
    fields = list(dict.fromkeys(k for r in rows for k in r))
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)


def bootstrap_ci(xs: list[float], n: int = 2000, alpha: float = 0.05, seed: int = 0) -> tuple[float, float]:
    if len(xs) < 2:
        return (xs[0], xs[0]) if xs else (float("nan"), float("nan"))
    rng = random.Random(seed)
    means = sorted(statistics.fmean(rng.choices(xs, k=len(xs))) for _ in range(n))
    return means[int(n * alpha / 2)], means[int(n * (1 - alpha / 2)) - 1]


def permutation_test(a: list[float], b: list[float], n: int = 5000, seed: int = 0) -> float:
    """Zweiseitiger p-Wert für Differenz der Mittelwerte."""
    if not a or not b:
        return float("nan")
    rng = random.Random(seed)
    obs = abs(statistics.fmean(a) - statistics.fmean(b))
    pooled = a + b
    hits = 0
    for _ in range(n):
        rng.shuffle(pooled)
        if abs(statistics.fmean(pooled[:len(a)]) - statistics.fmean(pooled[len(a):])) >= obs - 1e-12:
            hits += 1
    return (hits + 1) / (n + 1)


def paired_permutation_test(diffs: list[float], n: int = 10000, seed: int = 0) -> float:
    """Zweiseitiger Vorzeichen-Permutationstest für gepaarte Differenzen (gleiche Seeds, gleiche Domäne)."""
    if not diffs or all(d == 0 for d in diffs):
        return 1.0
    rng = random.Random(seed)
    obs = abs(statistics.fmean(diffs))
    hits = sum(abs(statistics.fmean([d if rng.random() < 0.5 else -d for d in diffs])) >= obs - 1e-12 for _ in range(n))
    return (hits + 1) / (n + 1)


def cohens_d(a: list[float], b: list[float]) -> float:
    if len(a) < 2 or len(b) < 2:
        return float("nan")
    sa, sb = statistics.variance(a), statistics.variance(b)
    pooled = ((len(a) - 1) * sa + (len(b) - 1) * sb) / (len(a) + len(b) - 2)
    return (statistics.fmean(a) - statistics.fmean(b)) / pooled ** 0.5 if pooled > 0 else float("inf")


def group(rows: Iterable[dict[str, Any]], by: tuple[str, ...]) -> dict[tuple, list[dict[str, Any]]]:
    out: dict[tuple, list[dict[str, Any]]] = {}
    for r in rows:
        out.setdefault(tuple(r[k] for k in by), []).append(r)
    return out


def summarize(rows: list[dict[str, Any]], metrics: list[str], by: tuple[str, ...] = ("config_name", "domain")) -> str:
    lines = ["| " + " | ".join(by) + " | n | " + " | ".join(f"{m} (95%-CI)" for m in metrics) + " |",
             "|" + "---|" * (len(by) + 1 + len(metrics))]
    for key, rs in sorted(group(rows, by).items(), key=lambda kv: [str(k) for k in kv[0]]):
        cells = []
        for m in metrics:
            xs = [float(r[m]) for r in rs if r.get(m) is not None]
            lo, hi = bootstrap_ci(xs)
            cells.append(f"{statistics.fmean(xs):.3f} ({lo:.2f}–{hi:.2f})" if xs else "–")
        lines.append("| " + " | ".join(str(k) for k in key) + f" | {len(rs)} | " + " | ".join(cells) + " |")
    return "\n".join(lines)


def bh_qvalues(ps: list[float]) -> list[float]:
    """Benjamini-Hochberg: q-Werte (False Discovery Rate) für eine Familie von Tests."""
    m = len(ps)
    order = sorted(range(m), key=lambda i: ps[i])
    q = [0.0] * m
    running = 1.0
    for rank in range(m, 0, -1):
        i = order[rank - 1]
        running = min(running, ps[i] * m / rank)
        q[i] = running
    return q


def compare(rows: list[dict[str, Any]], metric: str, by: str = "config_name") -> str:
    groups = {k[0]: [float(r[metric]) for r in rs] for k, rs in group(rows, (by,)).items()}
    names = sorted(groups)
    pairs = [(a, b) for i, a in enumerate(names) for b in names[i + 1:]]
    ps = [permutation_test(groups[a], groups[b]) for a, b in pairs]
    qs = bh_qvalues(ps)
    lines = [f"Paarvergleiche für `{metric}` (Permutationstest, zweiseitig; q = BH-FDR über diese Familie; Cohen's d)", "",
             "| A | B | Δ (A−B) | p | q | d |", "|---|---|---|---|---|---|"]
    for (a, b), p, q in zip(pairs, ps, qs):
        d = statistics.fmean(groups[a]) - statistics.fmean(groups[b])
        lines.append(f"| {a} | {b} | {d:+.3f} | {p:.4f} | {q:.4f} | {cohens_d(groups[a], groups[b]):.2f} |")
    return "\n".join(lines)


def report(exp_dir: Path, primary: str = "true_completion",
           secondary: tuple[str, ...] = ("false_done_rate", "phantoms_diagnosed", "messages", "output_tokens")) -> str:
    rows = collect(exp_dir)
    write_csv(rows, exp_dir / "results.csv")
    if not rows:
        return "Keine abgeschlossenen Runs."
    text = "\n\n".join([
        f"# Auswertung {exp_dir.name}", f"Runs: {len(rows)}",
        "## Je Config und Domäne", summarize(rows, [primary, *secondary]),
        "## Je Config (über Domänen)", summarize(rows, [primary, *secondary], by=("config_name",)),
        "## " + primary, compare(rows, primary),
    ])
    (exp_dir / "auswertung.md").write_text(text, encoding="utf-8")
    return text


if __name__ == "__main__":
    import sys
    print(report(Path(sys.argv[1])))
