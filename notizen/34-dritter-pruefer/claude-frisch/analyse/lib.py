"""Gemeinsame Hilfsfunktionen: Laden, Bootstrap über Belege, Logit."""
import json, math, random, os, sys
from collections import defaultdict

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'daten')
CELLS = [f'SP{a}-ZU{b}-AU{c}' for a in (0, 1) for b in (0, 1) for c in (0, 1)]
MODELS = ['S', 'H']
MNAME = {'anthropic/claude-sonnet-5.5': 'S', 'anthropic/claude-haiku-5.5': 'H'}

try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass


def _read(fn):
    with open(os.path.join(BASE, fn), encoding='utf8') as f:
        return [json.loads(l) for l in f if l.strip()]


def load(null_as_wrong=True):
    """Gibt Liste der Urteile zurück mit Zusatzfeldern set, m, correct, vnull, wtrue."""
    out = []
    for fn, s in [('urteile_seeds6000_sonnet.jsonl', 6000), ('urteile_seeds6000_haiku.jsonl', 6000),
                  ('urteile_seeds7000_beide.jsonl', 7000)]:
        for r in _read(fn):
            r['set'] = s
            r['m'] = MNAME[r['model']]
            r['vnull'] = r['verdict'] is None
            if r['vnull']:
                r['correct'] = 0 if null_as_wrong else None
                r['wtrue'] = None
            else:
                r['correct'] = int(r['verdict'] == r['truth'])
                r['wtrue'] = int(r['verdict'] is True)
            out.append(r)
    return out


def load_belege():
    d = {}
    for fn in ['belege_seeds6000.jsonl', 'belege_seeds7000.jsonl']:
        for b in _read(fn):
            d[b['id']] = b
    return d


def load_gpt():
    return {r['id']: r for r in _read('gpt_einzelkanal_seeds7000.jsonl')}


def btype(r):
    """Belegtyp, über Seed-Sätze vergleichbar."""
    if r['truth']:
        return f"{r['domain']}|{r['kind']}"
    return f"{r['domain']}|{r['kind']}|{r['fault']}"


def index(R):
    """idx[set][id][m][cell] = record"""
    idx = defaultdict(lambda: defaultdict(lambda: defaultdict(dict)))
    for r in R:
        idx[r['set']][r['id']][r['m']][r['cell']] = r
    return idx


def strata(idx_set):
    """Belege eines Satzes nach domain×kind geschichtet."""
    st = defaultdict(list)
    for i, d in idx_set.items():
        any_r = next(iter(next(iter(d.values())).values()))
        st[(any_r['domain'], any_r['kind'])].append(i)
    return list(st.values())


def logit(p, n=None):
    """Logit eines Anteils; mit n wird Haldane-Korrektur benutzt."""
    if n is not None:
        k = p * n
        p = (k + 0.5) / (n + 1)
    p = min(max(p, 1e-9), 1 - 1e-9)
    return math.log(p / (1 - p))


def lo(k, n):
    return math.log((k + 0.5) / (n - k + 0.5))


def boot(strata_ids, stat, B=2000, seed=1):
    """Cluster-Bootstrap über Belege, geschichtet. stat(ids)->dict name->float.
    Rückgabe dict name->(punkt, lo, hi)."""
    rng = random.Random(seed)
    all_ids = [i for s in strata_ids for i in s]
    point = stat(all_ids)
    draws = defaultdict(list)
    for _ in range(B):
        ids = []
        for s in strata_ids:
            ids.extend(rng.choice(s) for _ in range(len(s)))
        res = stat(ids)
        for k, v in res.items():
            if v is not None and not (isinstance(v, float) and math.isnan(v)):
                draws[k].append(v)
    out = {}
    for k, v in point.items():
        d = sorted(draws[k])
        if not d:
            out[k] = (v, float('nan'), float('nan'))
            continue
        out[k] = (v, d[int(0.025 * len(d))], d[min(len(d) - 1, int(0.975 * len(d)))])
    return out


def fmt(t, nd=3, pct=False):
    v, a, b = t
    if pct:
        return f"{100*v:6.1f} [{100*a:6.1f}; {100*b:6.1f}]"
    return f"{v:7.{nd}f} [{a:7.{nd}f}; {b:7.{nd}f}]"


def mean(x):
    x = list(x)
    return sum(x) / len(x) if x else float('nan')


def pearson(x, y):
    n = len(x)
    mx, my = mean(x), mean(y)
    sxy = sum((a - mx) * (b - my) for a, b in zip(x, y))
    sxx = sum((a - mx) ** 2 for a in x)
    syy = sum((b - my) ** 2 for b in y)
    if sxx == 0 or syy == 0:
        return float('nan')
    return sxy / math.sqrt(sxx * syy)


def ranks(x):
    o = sorted(range(len(x)), key=lambda i: x[i])
    r = [0.0] * len(x)
    i = 0
    while i < len(o):
        j = i
        while j + 1 < len(o) and x[o[j + 1]] == x[o[i]]:
            j += 1
        for k in range(i, j + 1):
            r[o[k]] = (i + j) / 2 + 1
        i = j + 1
    return r


def spearman(x, y):
    return pearson(ranks(x), ranks(y))


def auroc(scores, labels):
    """AUROC: P(score bei label 1 > score bei label 0), Bindungen halb."""
    pos = [s for s, l in zip(scores, labels) if l]
    neg = [s for s, l in zip(scores, labels) if not l]
    if not pos or not neg:
        return float('nan')
    # über Ränge
    allv = scores
    r = ranks(allv)
    rp = sum(ri for ri, l in zip(r, labels) if l)
    n1, n0 = len(pos), len(neg)
    return (rp - n1 * (n1 + 1) / 2) / (n1 * n0)
