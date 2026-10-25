"""Frage 3: Schwierigkeit je Typ/Beleg und Modell; Ähnlichkeit; Effekt × Schwierigkeit ohne Zirkelschluss."""
from lib import *
import random, math
from collections import defaultdict

R = load()
idx = index(R)
FACT = ['SP', 'ZU', 'AU']
CF = {c: {'SP': int(c[2]), 'ZU': int(c[6]), 'AU': int(c[10])} for c in CELLS}
OTHER = {'S': 'H', 'H': 'S'}


def rec0(d, i):
    return d[i]['S'][CELLS[0]]


# ---------- 3a: Typ-Schwierigkeit je Modell und Satz ----------
def type_err(s, m, cells=CELLS):
    d = idx[s]
    k = defaultdict(float); n = defaultdict(int)
    for i in d:
        for c in cells:
            r = d[i][m][c]
            k[btype(r)] += 1 - r['correct']; n[btype(r)] += 1
    return {t: (k[t], n[t]) for t in n}


types = sorted(type_err(6000, 'S'))
TE = {(s, m): type_err(s, m) for s in (6000, 7000) for m in MODELS}
TE0 = {(s, m, f): type_err(s, m, [c for c in CELLS if CF[c][f] == 0]) for s in (6000, 7000) for m in MODELS for f in FACT}
print('===== 3a Fehlerquote je Belegtyp (alle 8 Zellen; n = 8 × Belege) =====')
print(f"{'Typ':42s} {'S6000':>7s} {'S7000':>7s} {'H6000':>7s} {'H7000':>7s}")
for t in types:
    row = ''.join(f' {100*TE[(s,m)][t][0]/TE[(s,m)][t][1]:6.1f}%' for m in MODELS for s in (6000, 7000))
    print(f'{t:42s}{row}')


def lgt(kn):
    k, n = kn
    return lo(k, n)


def corr_block(cells=CELLS, label='alle Zellen', unit='type'):
    """Korrelationen der Typ-Schwierigkeiten (Logit) zwischen Modellen/Sätzen."""
    te = {(s, m): type_err(s, m, cells) for s in (6000, 7000) for m in MODELS}
    v = {k: [lgt(te[k][t]) for t in types] for k in te}
    out = {}
    out['S6000~S7000 (Rel. Sonnet)'] = pearson(v[(6000, 'S')], v[(7000, 'S')])
    out['H6000~H7000 (Rel. Haiku)'] = pearson(v[(6000, 'H')], v[(7000, 'H')])
    out['S6000~H6000 (gleiche Belege)'] = pearson(v[(6000, 'S')], v[(6000, 'H')])
    out['S7000~H7000 (gleiche Belege)'] = pearson(v[(7000, 'S')], v[(7000, 'H')])
    out['S6000~H7000 (kreuz)'] = pearson(v[(6000, 'S')], v[(7000, 'H')])
    out['S7000~H6000 (kreuz)'] = pearson(v[(7000, 'S')], v[(6000, 'H')])
    rs = out['S6000~S7000 (Rel. Sonnet)']; rh = out['H6000~H7000 (Rel. Haiku)']
    cross = (out['S6000~H7000 (kreuz)'] + out['S7000~H6000 (kreuz)']) / 2
    out['kreuz, attenuationskorrigiert'] = cross / math.sqrt(rs * rh) if rs > 0 and rh > 0 else float('nan')
    sp = {}
    sp['Spearman S6000~H7000'] = spearman(v[(6000, 'S')], v[(7000, 'H')])
    sp['Spearman S7000~H6000'] = spearman(v[(7000, 'S')], v[(6000, 'H')])
    print(f'\n--- Korrelation der Typ-Schwierigkeit (Logit, Haldane), {label}, {len(types)} Typen')
    for k_, x in {**out, **sp}.items():
        print(f'   {k_:38s} {x:+.3f}')
    return out


corr_block()
# je Zelle: Typ × Zelle als Einheit (240 Einheiten)
def type_cell_vectors(s, m):
    d = idx[s]
    k = defaultdict(float); n = defaultdict(int)
    for i in d:
        for c in CELLS:
            r = d[i][m][c]
            key = (btype(r), c)
            k[key] += 1 - r['correct']; n[key] += 1
    keys = sorted(n)
    return keys, [lo(k[x], n[x]) for x in keys]


keys, _ = type_cell_vectors(6000, 'S')
V = {(s, m): type_cell_vectors(s, m)[1] for s in (6000, 7000) for m in MODELS}
print('\n--- Typ × Zelle als Einheit (240 Einheiten, je 12 Belege)')
rs = pearson(V[(6000, 'S')], V[(7000, 'S')]); rh = pearson(V[(6000, 'H')], V[(7000, 'H')])
c1 = pearson(V[(6000, 'S')], V[(7000, 'H')]); c2 = pearson(V[(7000, 'S')], V[(6000, 'H')])
print(f'   Rel. Sonnet {rs:+.3f}, Rel. Haiku {rh:+.3f}, kreuz S~H {c1:+.3f} / {c2:+.3f}, '
      f'gleiche Belege S~H 6000 {pearson(V[(6000,"S")],V[(6000,"H")]):+.3f} 7000 {pearson(V[(7000,"S")],V[(7000,"H")]):+.3f}, '
      f'korrigiert {((c1+c2)/2)/math.sqrt(rs*rh):+.3f}')
# Wo sind beide schwer? Typ×Zelle mit Fehlerquote >= 20 % (gepoolt über Sätze)
print('\n--- Typ × Zelle mit gepoolter Fehlerquote >= 20 % bei mindestens einem Modell')
pool = {}
for m in MODELS:
    for s in (6000, 7000):
        d = idx[s]
        for i in d:
            for c in CELLS:
                r = d[i][m][c]
                key = (m, btype(r), c)
                a = pool.setdefault(key, [0, 0]); a[0] += 1 - r['correct']; a[1] += 1
tc = sorted({(k[1], k[2]) for k in pool})
for t, c in tc:
    es = pool[('S', t, c)]; eh = pool[('H', t, c)]
    if es[0] / es[1] >= 0.2 or eh[0] / eh[1] >= 0.2:
        print(f'   {t:40s} {c}: Sonnet {100*es[0]/es[1]:5.1f}%  Haiku {100*eh[0]/eh[1]:5.1f}%  (n={es[1]})')

# Bootstrap für die Kreuzkorrelation (Typ-Ebene) über Belege beider Sätze
print('\n--- Bootstrap (1000) der Typ-Korrelationen, Belege in beiden Sätzen geschichtet gezogen')
rng = random.Random(3)
st = {s: strata(idx[s]) for s in (6000, 7000)}


def type_err_ids(s, m, ids):
    d = idx[s]
    k = defaultdict(float); n = defaultdict(int)
    for i in ids:
        for c in CELLS:
            r = d[i][m][c]
            k[btype(r)] += 1 - r['correct']; n[btype(r)] += 1
    return [lo(k[t], n[t]) for t in types]


bs = defaultdict(list)
for b in range(1000):
    ids = {s: [i for g in st[s] for i in (rng.choice(g) for _ in g)] for s in (6000, 7000)}
    v = {(s, m): type_err_ids(s, m, ids[s]) for s in (6000, 7000) for m in MODELS}
    rs = pearson(v[(6000, 'S')], v[(7000, 'S')]); rh = pearson(v[(6000, 'H')], v[(7000, 'H')])
    cr = (pearson(v[(6000, 'S')], v[(7000, 'H')]) + pearson(v[(7000, 'S')], v[(6000, 'H')])) / 2
    bs['rel_S'].append(rs); bs['rel_H'].append(rh); bs['kreuz'].append(cr)
    if rs > 0 and rh > 0:
        bs['korr'].append(cr / math.sqrt(rs * rh))
for k_, x in bs.items():
    x = sorted(x)
    print(f'   {k_:8s} 95%-Intervall [{x[int(.025*len(x))]:+.3f}; {x[int(.975*len(x))]:+.3f}]  Median {x[len(x)//2]:+.3f}')

# ---------- 3b: Beleg-Schwierigkeit innerhalb Typ: gibt es Belege, die schwerer sind als ihr Typ? ----------
print('\n===== 3b Streuung der Beleg-Schwierigkeit innerhalb von Typ × Zelle =====')
# Test: Wenn ein Beleg in Zelle (SP,ZU,AU=0) falsch ist, ist er in (SP,ZU,AU=1) häufiger falsch als der Typ×Zelle-Durchschnitt?
for m in MODELS:
    for s in (6000, 7000):
        d = idx[s]
        obs = exp = 0.0; npairs = 0
        # Typ×Zelle-Raten
        tr = defaultdict(lambda: [0, 0])
        for i in d:
            for c in CELLS:
                r = d[i][m][c]; a = tr[(btype(r), c)]; a[0] += 1 - r['correct']; a[1] += 1
        for i in d:
            for sp in (0, 1):
                for zu in (0, 1):
                    c0 = f'SP{sp}-ZU{zu}-AU0'; c1 = f'SP{sp}-ZU{zu}-AU1'
                    r0 = d[i][m][c0]; r1 = d[i][m][c1]
                    e0 = 1 - r0['correct']; e1 = 1 - r1['correct']
                    t = btype(r0)
                    p0 = tr[(t, c0)][0] / tr[(t, c0)][1]; p1 = tr[(t, c1)][0] / tr[(t, c1)][1]
                    obs += e0 * e1; exp += p0 * p1; npairs += 1
        print(f'{m} {s}: gemeinsame Fehler AU0&AU1 beob. {obs:.0f}, erwartet bei Unabhängigkeit innerhalb Typ×Zelle {exp:.1f} (Verhältnis {obs/exp if exp else float("nan"):.2f})')


# ---------- 3c: Effekt × Schwierigkeit ----------
def fit_additive(d, m, ids):
    """logit p_bc = a_b + g_c  (keine Beleg×Bedingung-Wechselwirkung). Haldane-artige Glättung über
    einen schwachen Prior a_b ~ N(mu, 2^2)."""
    a = {i: 0.0 for i in ids}
    g = {c: 0.0 for c in CELLS}
    y = {i: {c: d[i][m][c]['correct'] for c in CELLS} for i in ids}
    for it in range(60):
        mu = mean(a.values())
        for i in ids:
            for _ in range(2):
                gr = -(a[i] - mu) / 4.0; h = -1 / 4.0
                for c in CELLS:
                    p = 1 / (1 + math.exp(-(a[i] + g[c])))
                    gr += y[i][c] - p; h -= p * (1 - p)
                a[i] -= gr / h
        for c in CELLS:
            gr = 0.0; h = -1e-6
            for i in ids:
                p = 1 / (1 + math.exp(-(a[i] + g[c])))
                gr += y[i][c] - p; h -= p * (1 - p)
            g[c] -= gr / h
        # Identifizierbarkeit: g von SP0-ZU0-AU0 = 0
        g0 = g[CELLS[0]]
        for c in CELLS:
            g[c] -= g0
        for i in ids:
            a[i] += g0
    return a, g


def effect_groups(Y, ids, f, diff, thr, eval_cells=CELLS):
    """Effekt von f in Gruppen leicht (diff<=thr) / schwer (diff>thr). Y[i][c] = correct.
    Gibt dict mit pp- und logit-Effekt je Gruppe und Differenz zurück."""
    out = {}
    for gname, sel in (('leicht', lambda x: x <= thr), ('schwer', lambda x: x > thr)):
        k1 = n1 = k0 = n0 = 0
        for i in ids:
            if not sel(diff[i]):
                continue
            for c in eval_cells:
                if CF[c][f]:
                    k1 += Y[i][c]; n1 += 1
                else:
                    k0 += Y[i][c]; n0 += 1
        if n1 == 0 or n0 == 0:
            out[gname + '_pp'] = float('nan'); out[gname + '_lo'] = float('nan'); out[gname + '_n'] = 0
            continue
        out[gname + '_pp'] = k1 / n1 - k0 / n0
        out[gname + '_lo'] = lo(k1, n1) - lo(k0, n0)
        out[gname + '_n'] = n1 + n0
    out['diff_pp'] = out['schwer_pp'] - out['leicht_pp']
    out['diff_lo'] = out['schwer_lo'] - out['leicht_lo']
    return out


def difficulties(s, m, f, Y, Yother, ids, te_other_set):
    """Gibt dict Schätzer -> (diff je Beleg, Schwelle, eval_cells-Liste oder 'cross') zurück."""
    d = idx[s]
    est = {}
    # zirkulär: Fehler in Zellen mit f=0, eigenes Modell
    c0 = [c for c in CELLS if CF[c][f] == 0]
    est['zirkulär (F=0, eigenes Modell)'] = ({i: mean(1 - Y[i][c] for c in c0) for i in ids}, 0.0, CELLS)
    # S1: extern Art
    est['S1 extern (Art=fail_subtle/ok_noisy)'] = ({i: float(rec0(d, i)['kind'] in ('fail_subtle', 'ok_noisy')) for i in ids}, 0.5, CELLS)
    # S2: Typ-Schwierigkeit aus dem anderen Satz, gleiches Modell
    est['S2 Typ aus anderem Satz'] = ({i: te_other_set[btype(rec0(d, i))][0] / te_other_set[btype(rec0(d, i))][1] for i in ids}, 0.05, CELLS)
    # S2b: Typ-Schwierigkeit aus dem anderen Satz, nur Basisstufe F=0
    te0 = TE0[(13000 - s, m, f)]
    est['S2b Typ anderer Satz, nur F=0'] = ({i: te0[btype(rec0(d, i))][0] / te0[btype(rec0(d, i))][1] for i in ids}, 0.05, CELLS)
    # S3: anderes Modell, gleicher Beleg, alle Zellen
    est['S3 anderes Modell'] = ({i: mean(1 - Yother[i][c] for c in CELLS) for i in ids}, 0.0, CELLS)
    return est


def s4_effect(Y, ids, f):
    """S4 Kreuzanpassung über Zellen: Schwierigkeit aus Zellen mit G=g (beide f-Stufen), Effekt in G=1-g."""
    res = []
    for g in [x for x in FACT if x != f]:
        for gv in (0, 1):
            dc = [c for c in CELLS if CF[c][g] == gv]
            ec = [c for c in CELLS if CF[c][g] != gv]
            diff = {i: mean(1 - Y[i][c] for c in dc) for i in ids}
            res.append(effect_groups(Y, ids, f, diff, 0.0, ec))
    out = {}
    for k in res[0]:
        vals = [r[k] for r in res if not (isinstance(r[k], float) and math.isnan(r[k]))]
        out[k] = mean(vals) if vals else float('nan')
    return out


def all_stats(s, m, Y, Yother, ids):
    o = {}
    te_other = TE[(13000 - s, m)]
    for f in FACT:
        est = difficulties(s, m, f, Y, Yother, ids, te_other)
        for name, (diff, thr, ec) in est.items():
            r = effect_groups(Y, ids, f, diff, thr, ec)
            for k, v in r.items():
                o[(f, name, k)] = v
        r = s4_effect(Y, ids, f)
        for k, v in r.items():
            o[(f, 'S4 Kreuzanpassung Zellen', k)] = v
    return o


print('\n===== 3c Effekt × Schwierigkeit (Richtigkeit). schwer−leicht: Differenz der Effekte =====')
print('Nullverteilung: 200 Simulationen aus additivem Logit-Modell a_b + g_c je Modell (keine Beleg×Bedingung-Wechselwirkung)')
NSIM = 200
for s in (6000, 7000):
    d = idx[s]
    ids = list(d)
    Yall = {m: {i: {c: d[i][m][c]['correct'] for c in CELLS} for i in ids} for m in MODELS}
    fits = {m: fit_additive(d, m, ids) for m in MODELS}
    rng = random.Random(s)
    sims = {m: [] for m in MODELS}
    for b in range(NSIM):
        Ys = {}
        for m in MODELS:
            a, g = fits[m]
            Ys[m] = {i: {c: int(rng.random() < 1 / (1 + math.exp(-(a[i] + g[c])))) for c in CELLS} for i in ids}
        for m in MODELS:
            sims[m].append(all_stats(s, m, Ys[m], Ys[OTHER[m]], ids))
    for m in MODELS:
        obs = all_stats(s, m, Yall[m], Yall[OTHER[m]], ids)
        print(f'\n--- Satz {s}, Modell {m}  (g_c der Nullanpassung: ' + ', '.join(f'{c}:{fits[m][1][c]:+.2f}' for c in CELLS) + ')')
        for f in FACT:
            for name in ['zirkulär (F=0, eigenes Modell)', 'S1 extern (Art=fail_subtle/ok_noisy)', 'S2 Typ aus anderem Satz',
                         'S2b Typ anderer Satz, nur F=0', 'S3 anderes Modell', 'S4 Kreuzanpassung Zellen']:
                def q(k):
                    x = sorted(v[(f, name, k)] for v in sims[m] if not math.isnan(v[(f, name, k)]))
                    if not x:
                        return float('nan'), float('nan'), float('nan')
                    return x[int(.025 * len(x))], x[len(x) // 2], x[int(.975 * len(x)) - 1]
                ql = q('diff_lo'); qp = q('diff_pp')
                o = lambda k: obs[(f, name, k)]
                print(f'{f} {name:38s} leicht {100*o("leicht_pp"):+6.1f}pp/{o("leicht_lo"):+5.2f}lo (n={o("leicht_n")})  '
                      f'schwer {100*o("schwer_pp"):+6.1f}pp/{o("schwer_lo"):+5.2f}lo (n={o("schwer_n")})  '
                      f'Diff {100*o("diff_pp"):+6.1f}pp [Null {100*qp[0]:+5.1f};{100*qp[2]:+5.1f}]  '
                      f'{o("diff_lo"):+5.2f}lo [Null {ql[0]:+5.2f};{ql[2]:+5.2f}]')
