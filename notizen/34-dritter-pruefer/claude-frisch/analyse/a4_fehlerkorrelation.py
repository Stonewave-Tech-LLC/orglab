"""Frage 4: Scheitern beide Modelle an denselben Belegen/Zellen? Zufallskorrigiert und geschichtet."""
from lib import *
from collections import defaultdict

R = load()
idx = index(R)


def pairs_model(d, ids, m1, m2):
    """Paare (stratum, e1, e2, p1true, p2true) auf Ebene Beleg×Zelle, beide Modelle gleiche Zelle."""
    out = []
    for i in ids:
        for c in CELLS:
            r1 = d[i][m1][c]; r2 = d[i][m2][c]
            out.append((btype(r1), c, 1 - r1['correct'], 1 - r2['correct'], r1, r2))
    return out


def pairs_self(d, ids, m):
    """Selbst-Referenz: dasselbe Modell, AU0 gegen AU1 bei gleichem SP, ZU."""
    out = []
    for i in ids:
        for sp in (0, 1):
            for zu in (0, 1):
                c0 = f'SP{sp}-ZU{zu}-AU0'; c1 = f'SP{sp}-ZU{zu}-AU1'
                r1 = d[i][m][c0]; r2 = d[i][m][c1]
                out.append((btype(r1), f'SP{sp}-ZU{zu}', 1 - r1['correct'], 1 - r2['correct'], r1, r2))
    return out


def kappa_stats(P, strat):
    """strat: Funktion (typ, zelle)->Schichtschlüssel oder None (ungeschichtet).
    κ = (Po − Pe)/(1 − Pe) mit Pe aus Schicht-Randverteilungen. Double-Fault-Verhältnis = beob./erw."""
    groups = defaultdict(list)
    for p in P:
        groups[strat(p[0], p[1]) if strat else 0].append(p)
    po = pe = both = eboth = 0.0
    n = len(P)
    for g in groups.values():
        k = len(g)
        a = sum(x[2] for x in g) / k; b = sum(x[3] for x in g) / k
        pe += k * (a * b + (1 - a) * (1 - b))
        eboth += k * a * b
    for x in P:
        po += int(x[2] == x[3]); both += x[2] * x[3]
    po /= n; pe /= n
    kap = (po - pe) / (1 - pe) if pe < 1 else float('nan')
    dfr = both / eboth if eboth > 0 else float('nan')
    return kap, dfr, both, eboth


def capa_like(P):
    """Probabilistische Variante (angelehnt an CAPA): Wahrscheinlichkeit für Urteil 'funktioniert'
    aus Urteil+Konfidenz; beobachtete Übereinstimmung = Σ p1(o)p2(o); erwartete aus den mittleren
    Trefferwahrscheinlichkeiten. Nur gültige Urteile."""
    obs = []; q1 = []; q2 = []
    for x in P:
        r1, r2 = x[4], x[5]
        if r1['vnull'] or r2['vnull']:
            continue
        p1 = r1['confidence'] if r1['verdict'] else 1 - r1['confidence']
        p2 = r2['confidence'] if r2['verdict'] else 1 - r2['confidence']
        obs.append(p1 * p2 + (1 - p1) * (1 - p2))
        t = r1['truth']
        q1.append(p1 if t else 1 - p1); q2.append(p2 if t else 1 - p2)
    co = mean(obs); a = mean(q1); b = mean(q2)
    ce = a * b + (1 - a) * (1 - b)
    return (co - ce) / (1 - ce)


ST = {
    'ungeschichtet': None,
    'Schicht Zelle': lambda t, c: c,
    'Schicht Typ': lambda t, c: t,
    'Schicht Typ×Zelle': lambda t, c: (t, c),
}


def make_stat(d):
    def stat(ids):
        o = {}
        P = pairs_model(d, ids, 'S', 'H')
        o['S-Fehlerquote'] = mean(x[2] for x in P)
        o['H-Fehlerquote'] = mean(x[3] for x in P)
        o['beide falsch (Anteil)'] = mean(x[2] * x[3] for x in P)
        o['P(H falsch | S falsch)'] = (sum(x[2] * x[3] for x in P) / sum(x[2] for x in P)) if sum(x[2] for x in P) else float('nan')
        for name, f in ST.items():
            k, dfr, _, _ = kappa_stats(P, f)
            o[f'S~H κ {name}'] = k
            o[f'S~H DF-Verh. {name}'] = dfr
        o['S~H CAPA-ähnlich (ungeschichtet)'] = capa_like(P)
        for m in MODELS:
            Q = pairs_self(d, ids, m)
            for name, f in [('ungeschichtet', None), ('Schicht Typ×SP×ZU', lambda t, c: (t, c))]:
                k, dfr, _, _ = kappa_stats(Q, f)
                o[f'{m}~{m} (AU0/AU1) κ {name}'] = k
                o[f'{m}~{m} (AU0/AU1) DF-Verh. {name}'] = dfr
        # Kreuzmodell zum Vergleich mit gleicher Zellpaarung: S in AU0 gegen H in AU1 (und umgekehrt), Schicht Typ×SP×ZU
        Q = []
        for i in ids:
            for sp in (0, 1):
                for zu in (0, 1):
                    for a_, b_ in ((0, 1), (1, 0)):
                        r1 = d[i]['S'][f'SP{sp}-ZU{zu}-AU{a_}']; r2 = d[i]['H'][f'SP{sp}-ZU{zu}-AU{b_}']
                        Q.append((btype(r1), f'SP{sp}-ZU{zu}', 1 - r1['correct'], 1 - r2['correct'], r1, r2))
        k, dfr, _, _ = kappa_stats(Q, lambda t, c: (t, c))
        o['S~H (AU gekreuzt) κ Schicht Typ×SP×ZU'] = k
        o['S~H (AU gekreuzt) DF-Verh. Schicht Typ×SP×ZU'] = dfr
        return o
    return stat


for s in (6000, 7000):
    d = idx[s]
    res = boot(strata(d), make_stat(d), B=1000, seed=s + 7)
    print(f'\n===== Satz {s} =====')
    for k, v in res.items():
        print(f'{k:48s} {fmt(v)}')
    # Rohzählung
    P = pairs_model(d, list(d), 'S', 'H')
    nS = sum(x[2] for x in P); nH = sum(x[3] for x in P); nb = sum(x[2] * x[3] for x in P)
    print(f'Zählung: Sonnet-Fehler {nS}, Haiku-Fehler {nH}, gemeinsame {nb} von {len(P)} Beleg×Zellen')
    # wo liegen gemeinsame Fehler?
    from collections import Counter
    cc = Counter((x[0], x[1]) for x in P if x[2] and x[3])
    print('gemeinsame Fehler nach Typ×Zelle:', cc.most_common(12))
    # erwartete gemeinsame Fehler je Typ×Zelle vs beobachtet (nur Schichten mit beiden Fehlerquoten >0)
    g = defaultdict(list)
    for x in P:
        g[(x[0], x[1])].append(x)
    rows = []
    for key, xs in g.items():
        a = mean(x[2] for x in xs); b = mean(x[3] for x in xs)
        if a > 0 and b > 0:
            rows.append((key, len(xs), a, b, sum(x[2] * x[3] for x in xs), len(xs) * a * b))
    print('Schichten mit Fehlern beider Modelle (Typ, Zelle, n, S-Rate, H-Rate, beob. gemeinsam, erw. gemeinsam):')
    for r in sorted(rows, key=lambda r: -r[4]):
        print(f'   {r[0][0]:40s} {r[0][1]} n={r[1]:2d} S={r[2]:.2f} H={r[3]:.2f} beob={r[4]} erw={r[5]:.2f}')
