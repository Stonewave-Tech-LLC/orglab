"""EXPLORATIV (nachträglich, keine neue Bestätigung): E-024 mit Cluster-Bootstrap über Seeds statt über Belege.

Anlass: Fremdkritiker (Gemini 4 Argon) im Lichttest des research-harness, Einwand "Bootstrap über Belege statt über
Seed-Cluster" (vgl. Regel 13). Liest nur die Rohdaten, ändert nichts. Kontraste je Beleg kommen unverändert aus
`orglab.e024.contrasts`, damit nur die Resampling-Einheit wechselt.

  .venv/Scripts/python notizen/36-kritiker-einwaende-e024/seed_cluster.py > notizen/36-kritiker-einwaende-e024/ausgabe.txt
"""

from __future__ import annotations

import random
import statistics as st
import sys
from collections import defaultdict

from orglab import e020v3 as base
from orglab import e024

B = base.B  # 5000 wie präregistriert
KEYS = ("V1", "W1", "C1", "C2", "F1")


def seed_of(item: str) -> int:
    return int(item.rsplit("-", 1)[1])


def per_item_values(arms, keep=None, f1_exclude=frozenset()) -> dict[str, dict[str, float]]:
    """Je Kontrast: Beleg → Je-Beleg-Kontrast, genau wie e024.evaluate (W1 gepaart je Beleg)."""
    ct = e024.contrasts(arms[e024.HAIKU], keep, f1_exclude)
    co = e024.contrasts(arms[e024.SONNET], keep, f1_exclude)
    out = {k: dict(ct[k]) for k in ("V1", "C1", "C2", "F1")}
    out["W1"] = {i: ct["V1"][i] - co["V1"][i] for i in sorted(set(ct["V1"]) & set(co["V1"]))}
    return out


def cluster_draws(vals: dict[str, float], seed: int) -> list[float]:
    """Ganze Seeds mit Zurücklegen ziehen, alle Belege des Seeds kommen mit; Mittel über die gepoolten Belege
    (jeder Beleg gleich gewichtet, wie in der Präregistrierung)."""
    by: dict[int, list[float]] = defaultdict(list)
    for i, v in vals.items():
        by[seed_of(i)].append(v)
    clusters = [by[s] for s in sorted(by)]
    rng = random.Random(seed)
    ms = []
    for _ in range(B):
        pick = rng.choices(clusters, k=len(clusters))
        flat = [v for c in pick for v in c]
        ms.append(st.fmean(flat))
    return ms


def cluster_boot(vals, seed):
    ms = sorted(cluster_draws(vals, seed))
    return st.fmean(vals.values()), ms[int(0.025 * B)], ms[int(0.975 * B) - 1]


def cluster_p(vals, seed):
    return sum(m <= 0 for m in cluster_draws(vals, seed)) / B


def icc1(vals: dict[str, float]) -> tuple[float, float, int]:
    """ICC(1) aus einfaktorieller ANOVA (Gruppe = Seed), ungleiche Gruppengrößen über n0. Gibt (ICC, mittlere
    Gruppengröße, Anzahl Seeds). Negative Schätzungen bleiben stehen (heißen: kein Hinweis auf Zusammenhang)."""
    by: dict[int, list[float]] = defaultdict(list)
    for i, v in vals.items():
        by[seed_of(i)].append(v)
    groups = [g for g in by.values() if g]
    k, N = len(groups), sum(len(g) for g in groups)
    grand = st.fmean(v for g in groups for v in g)
    ssb = sum(len(g) * (st.fmean(g) - grand) ** 2 for g in groups)
    ssw = sum((v - st.fmean(g)) ** 2 for g in groups for v in g)
    msb, msw = ssb / (k - 1), ssw / (N - k)
    n0 = (N - sum(len(g) ** 2 for g in groups) / N) / (k - 1)
    icc = (msb - msw) / (msb + (n0 - 1) * msw) if (msb + (n0 - 1) * msw) > 0 else float("nan")
    return icc, N / k, k


def residual(vals: dict[str, float], meta: dict[str, tuple]) -> dict[str, float]:
    """Je-Beleg-Kontrast minus Mittel seiner Gruppe (Domäne, Art, Fehlerart, vorgelegter Kanal). Was danach noch am
    Seed hängt, ist nicht durch die vom Seed bestimmte Zusammensetzung erklärt."""
    by: dict[tuple, list[float]] = defaultdict(list)
    for i, v in vals.items():
        by[meta[i]].append(v)
    mu = {g: st.fmean(v) for g, v in by.items()}
    return {i: v - mu[meta[i]] for i, v in vals.items()}


def se(xs):
    return st.pstdev(xs)


def block(title, arms, meta, keep=None, ex=frozenset()):
    vals = per_item_values(arms, keep, ex)
    rows, p_item, p_clu = {}, {}, {}
    for k in KEYS:
        v = vals[k]
        m, lo, hi = base.boot(list(v.values()), e024.SEEDS_BOOT[k])
        _, clo, chi = cluster_boot(v, e024.SEEDS_BOOT[k])
        p_item[k] = base.p_greater(list(v.values()), e024.SEEDS_P[k])
        p_clu[k] = cluster_p(v, e024.SEEDS_P[k])
        # SE-Verhältnis aus unabhängigen Ziehungen (eigener Startwert, damit Perzentile oben unverändert bleiben)
        rng = random.Random(900 + KEYS.index(k))
        lst = list(v.values())
        se_item = se([st.fmean(rng.choices(lst, k=len(lst))) for _ in range(B)])
        se_clu = se(cluster_draws(v, 910 + KEYS.index(k)))
        icc, nbar, nseeds = icc1(v)
        ricc, _, _ = icc1(residual(v, meta))
        rows[k] = dict(m=m, lo=lo, hi=hi, clo=clo, chi=chi, n=len(v), deff=(se_clu / se_item) ** 2,
                       icc=icc, ricc=ricc, nbar=nbar, nseeds=nseeds)
    q_item, q_clu = base.bh(p_item), base.bh(p_clu)
    print(f"\n## {title}\n")
    print("| Nr | n (Seeds) | Mittel | KI Belege (prereg) | KI Seed-Cluster | Breite Cluster/Belege | q Belege | q Cluster "
          "| Etikett Belege | Etikett Cluster |")
    print("|---|---|---|---|---|---|---|---|---|---|")
    for k, r in rows.items():
        lb_i = e024.label(r["lo"], r["hi"], q_item[k], e024.NEED[k], False, k == "F1")
        lb_c = e024.label(r["clo"], r["chi"], q_clu[k], e024.NEED[k], False, k == "F1")
        print(f"| {k} | {r['n']} ({r['nseeds']}) | {r['m']:+.3f} | [{r['lo']:+.3f}; {r['hi']:+.3f}] | "
              f"[{r['clo']:+.3f}; {r['chi']:+.3f}] | {(r['chi'] - r['clo']) / (r['hi'] - r['lo']):.2f} | "
              f"{q_item[k]:.4f} | {q_clu[k]:.4f} | {lb_i} | {lb_c} |")
    print("\n| Nr | Belege je Seed (Mittel) | ICC(1) roh | ICC(1) nach Abzug Domäne×Art×Fehlerart×Kanal | "
          "empirischer Designeffekt (SE Cluster / SE Belege)² |")
    print("|---|---|---|---|---|")
    for k, r in rows.items():
        print(f"| {k} | {r['nbar']:.2f} | {r['icc']:+.3f} | {r['ricc']:+.3f} | {r['deff']:.2f} |")


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    js = e024.load(e024.DATA / "judgments.jsonl")
    arms, seeds = e024.prepare(js)
    ex = e024.exclusion()
    meta = {}
    for j in js:
        meta[j["id"]] = (j["domain"], j["kind"], j["fault"], base.CHANNELS[j["domain"]][j["seed"] % 3])
    print("# E-024, Cluster-Bootstrap über Seeds (EXPLORATIV, nachträglich)")
    print(f"\nVollständige Seeds: {len(seeds)} ({sorted(seeds)}). B = {B}, Startwerte KI 241–245, p 251–255.")
    block("Primär (wie prereg, nur Resampling-Einheit getauscht)", arms, meta, ex=ex)
    block(f"Sekundär: ohne die {len(ex)} einzeln nicht entscheidbaren Belege", arms, meta,
          keep=lambda i: i not in ex, ex=ex)
    block("Deskriptiv: F1 auf allen Ok-Belegen (übrige Zeilen wie primär)", arms, meta)


if __name__ == "__main__":
    main()
