"""Frage 5: Urteile bei ZU = 0 und Entscheidbarkeit laut GPT (nur Satz 7000)."""
from lib import *
from collections import defaultdict, Counter

R = load()
idx = index(R)
G = load_gpt()
d = idx[7000]
ids = list(d)
assert set(ids) == set(G), 'GPT-IDs passen nicht'


def r0(i):
    return d[i]['S'][CELLS[0]]


print('===== GPT selbst =====')
gc = [int(G[i]['verdict'] == G[i]['truth']) for i in ids]
print(f'GPT Trefferquote {mean(gc):.3f}; decidable ja {sum(G[i]["decidable"] for i in ids)}/{len(ids)}')
for dec in (True, False):
    sub = [i for i in ids if G[i]['decidable'] == dec]
    print(f'  decidable={dec}: n={len(sub)}, GPT richtig {mean(int(G[i]["verdict"]==G[i]["truth"]) for i in sub):.3f}, '
          f'GPT sagt kaputt {mean(int(G[i]["verdict"] is False) for i in sub):.3f}, Wahrheit kaputt {mean(int(not G[i]["truth"]) for i in sub):.3f}')
print('\nEntscheidbarkeit nach Typ (n nicht entscheidbar / n) und vorgelegtem Kanal:')
tab = defaultdict(lambda: [0, 0]); tabc = defaultdict(lambda: [0, 0])
for i in ids:
    t = btype(r0(i)); tab[t][0] += int(not G[i]['decidable']); tab[t][1] += 1
    pc = d[i]['S']['SP0-ZU0-AU0']['presented']
    tabc[(t, pc)][0] += int(not G[i]['decidable']); tabc[(t, pc)][1] += 1
for t in sorted(tab):
    det = ', '.join(f'{k[1]}:{v[0]}/{v[1]}' for k, v in sorted(tabc.items()) if k[0] == t)
    print(f'  {t:42s} {tab[t][0]:2d}/{tab[t][1]:2d}   ({det})')
print('\nGPT-Richtigkeit nach Typ:')
for t in sorted(tab):
    sub = [i for i in ids if btype(r0(i)) == t]
    print(f'  {t:42s} GPT richtig {mean(int(G[i]["verdict"]==G[i]["truth"]) for i in sub):.2f}')


def acc(m, sub, cond):
    v = [d[i][m][c]['correct'] for i in sub for c in CELLS if cond(c)]
    return (mean(v) if v else float('nan')), sum(v), len(v)


ZU0 = lambda c: c[6] == '0'
ZU1 = lambda c: c[6] == '1'


def stat(sample):
    o = {}
    for m in MODELS:
        for dec in (True, False):
            sub = [i for i in sample if G[i]['decidable'] == dec]
            for sp in ('0', '1', '*'):
                c0 = lambda c, sp=sp: ZU0(c) and (sp == '*' or c[2] == sp)
                c1 = lambda c, sp=sp: ZU1(c) and (sp == '*' or c[2] == sp)
                a0, k0, n0 = acc(m, sub, c0); a1, k1, n1 = acc(m, sub, c1)
                o[f'{m} dec={dec!s:5s} SP={sp} ZU0'] = a0
                o[f'{m} dec={dec!s:5s} SP={sp} ZU1'] = a1
                o[f'{m} dec={dec!s:5s} SP={sp} ZU1-ZU0 pp'] = a1 - a0
                o[f'{m} dec={dec!s:5s} SP={sp} ZU1-ZU0 lo'] = lo(k1, n1) - lo(k0, n0)
        # Unterschied der ZU0-Trefferquote dec=False vs True (SP0)
        o[f'{m} ZU0 SP0: nicht-entsch. − entsch. pp'] = o[f'{m} dec=False SP=0 ZU0'] - o[f'{m} dec=True  SP=0 ZU0']
        o[f'{m} ZU-Effekt: nicht-entsch. − entsch. (lo, alle SP)'] = o[f'{m} dec=False SP=* ZU1-ZU0 lo'] - o[f'{m} dec=True  SP=* ZU1-ZU0 lo']
    return o


# nur Belege, die kaputt sind, und alle Belege getrennt
for label, base in [('alle Belege', ids), ('nur kaputte Belege', [i for i in ids if not r0(i)['truth']]),
                    ('nur intakte Belege', [i for i in ids if r0(i)['truth']])]:
    st = defaultdict(list)
    for i in base:
        st[(r0(i)['domain'], r0(i)['kind'])].append(i)
    res = boot(list(st.values()), stat, B=1000, seed=55)
    print(f'\n===== Richtigkeit nach GPT-Entscheidbarkeit, {label} =====')
    for k, v in res.items():
        pct = not k.endswith('lo') and 'lo,' not in k
        print(f'{k:52s} {fmt(v, pct=pct) if pct else fmt(v)}')

# Innerhalb der Fehlertypen, an denen beide scheitern: erklärt decidable, welche Belege scheitern?
print('\n===== Innerhalb Typ: ZU0-Fehlerquote nach decidable (Zählung über ZU0-Zellen) =====')
for t in sorted(tab):
    sub = [i for i in ids if btype(r0(i)) == t]
    line = f'{t:42s}'
    for m in MODELS:
        for dec in (True, False):
            s2 = [i for i in sub if G[i]['decidable'] == dec]
            if s2:
                a, k, n = acc(m, s2, ZU0)
                line += f' {m}/dec={str(dec)[0]}: {100*(1-a):5.1f}% ({n-k}/{n})'
    if any(1 - acc(m, sub, ZU0)[0] > 0.05 for m in MODELS):
        print(line)

# Fehlerkorrelation S~H geschichtet zusätzlich nach decidable (nur ZU0-Zellen)
print('\n===== Gemeinsame Fehler bei ZU0, geschichtet nach Typ×Zelle vs. Typ×Zelle×decidable =====')


def kappa(P, key):
    g = defaultdict(list)
    for p in P:
        g[key(p)].append(p)
    po = pe = both = eb = 0.0
    for xs in g.values():
        a = mean(x[2] for x in xs); b = mean(x[3] for x in xs)
        pe += len(xs) * (a * b + (1 - a) * (1 - b)); eb += len(xs) * a * b
    for x in P:
        po += int(x[2] == x[3]); both += x[2] * x[3]
    po /= len(P); pe /= len(P)
    return (po - pe) / (1 - pe), both, eb


def kstat(sample):
    P = []
    for i in sample:
        for c in CELLS:
            if ZU0(c):
                P.append((btype(d[i]['S'][c]), c, 1 - d[i]['S'][c]['correct'], 1 - d[i]['H'][c]['correct'], G[i]['decidable']))
    k1, b1, e1 = kappa(P, lambda p: (p[0], p[1]))
    k2, b2, e2 = kappa(P, lambda p: (p[0], p[1], p[4]))
    return {'κ Typ×Zelle': k1, 'κ Typ×Zelle×decidable': k2, 'DF Typ×Zelle': b1 / e1 if e1 else float('nan'),
            'DF Typ×Zelle×decidable': b2 / e2 if e2 else float('nan')}


st = defaultdict(list)
for i in ids:
    st[(r0(i)['domain'], r0(i)['kind'])].append(i)
res = boot(list(st.values()), kstat, B=1000, seed=56)
for k, v in res.items():
    print(f'{k:30s} {fmt(v)}')

# Explorativ: vorgelegter Kanal bei low_traffic / db_down / cache_partial
print('\n===== Explorativ: ZU0-Fehler nach vorgelegtem Kanal bei schwierigen Coding-Fehlern =====')
for fault in ['low_traffic', 'db_down', 'cache_partial']:
    for m in MODELS:
        cnt = defaultdict(lambda: [0, 0])
        for i in ids:
            rr = r0(i)
            if rr['fault'] != fault:
                continue
            for c in CELLS:
                if ZU0(c):
                    x = d[i][m][c]
                    cnt[(x['presented'], G[i]['decidable'])][0] += 1 - x['correct']
                    cnt[(x['presented'], G[i]['decidable'])][1] += 1
        print(f'{fault:14s} {m}: ' + ', '.join(f'{k[0]}/dec={str(k[1])[0]}: {v[0]}/{v[1]}' for k, v in sorted(cnt.items())))
