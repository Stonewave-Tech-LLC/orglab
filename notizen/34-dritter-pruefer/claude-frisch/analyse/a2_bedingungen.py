"""Frage 2: Wirkung von SP, ZU, AU je Modell, auf Urteil und Vorgehen; Moderatoren."""
from lib import *

R = load()
idx = index(R)
FACT = ['SP', 'ZU', 'AU']


def cellf(cell):
    a = cell.split('-')
    return {'SP': int(a[0][2]), 'ZU': int(a[1][2]), 'AU': int(a[2][2])}


CF = {c: cellf(c) for c in CELLS}


def eff(d, ids, m, f, y='correct', filt=None, cond=None):
    """Mittel von y in Stufe1 minus Stufe0 (pp), plus log-OR aus Aggregat (bei binärem y).
    cond: zusätzliche Bedingung auf Zelle (dict)."""
    k1 = n1 = k0 = n0 = 0
    for i in ids:
        for c, r in d[i][m].items():
            if filt and not filt(r):
                continue
            if cond and any(CF[c][a] != v for a, v in cond.items()):
                continue
            v = r[y]
            if v is None:
                continue
            v = float(v)
            if CF[c][f]:
                k1 += v; n1 += 1
            else:
                k0 += v; n0 += 1
    if n1 == 0 or n0 == 0:
        return None, None
    if y not in ("correct", "wtrue", "looked_up", "right_section"):
        return k1 / n1 - k0 / n0, None
    return k1 / n1 - k0 / n0, lo(k1, n1) - lo(k0, n0)


FAILS = lambda r: not r['truth']
OKS = lambda r: r['truth']


def run_main(d, s):
    def stat(ids):
        o = {}
        for m in MODELS:
            for f in FACT:
                pp, lg = eff(d, ids, m, f)
                o[f'{m}|{f}|acc_pp'] = pp; o[f'{m}|{f}|acc_lo'] = lg
                pp, lg = eff(d, ids, m, f, filt=FAILS)
                o[f'{m}|{f}|sens_pp'] = pp; o[f'{m}|{f}|sens_lo'] = lg
                pp, lg = eff(d, ids, m, f, filt=OKS)
                o[f'{m}|{f}|spec_pp'] = pp; o[f'{m}|{f}|spec_lo'] = lg
                pp, lg = eff(d, ids, m, f, y='wtrue')
                o[f'{m}|{f}|pworks_pp'] = pp
                for y in ['looked_up', 'right_section', 'confidence', 'n_tool_calls', 'completion_tokens']:
                    pp, _ = eff(d, ids, m, f, y=y)
                    o[f'{m}|{f}|{y}'] = pp
        for f in FACT:
            for t in ['acc_lo', 'sens_lo', 'spec_lo']:
                o[f'S-H|{f}|{t}'] = o[f'S|{f}|{t}'] - o[f'H|{f}|{t}']
        return o
    res = boot(strata(d), stat, B=1000, seed=s)
    print(f'\n===== Satz {s}: Haupteffekte (Stufe1 - Stufe0) =====')
    for m in MODELS + ['S-H']:
        for f in FACT:
            row = [k for k in res if k.startswith(f'{m}|{f}|')]
            for k in row:
                t = k.split('|')[2]
                pct = t.endswith('_pp') or t in ('looked_up', 'right_section')
                print(f'{m:3s} {f}  {t:18s} {fmt(res[k], pct=pct) if pct else fmt(res[k])}')
    return res


def run_inter(d, s):
    """Zweifach-Wechselwirkungen auf Logit: Effekt von f bei g=1 minus bei g=0."""
    def stat(ids):
        o = {}
        for m in MODELS:
            for f, g in [('SP', 'ZU'), ('SP', 'AU'), ('ZU', 'AU')]:
                _, a1 = eff(d, ids, m, f, cond={g: 1})
                _, a0 = eff(d, ids, m, f, cond={g: 0})
                p1, _ = eff(d, ids, m, f, cond={g: 1})
                p0, _ = eff(d, ids, m, f, cond={g: 0})
                o[f'{m}|{f}x{g}|lo'] = a1 - a0
                o[f'{m}|{f}x{g}|pp'] = p1 - p0
                o[f'{m}|{f}|bei {g}=0 pp'] = p0
                o[f'{m}|{f}|bei {g}=1 pp'] = p1
        return o
    res = boot(strata(d), stat, B=1000, seed=s + 1)
    print(f'\n===== Satz {s}: Wechselwirkungen (Richtigkeit) =====')
    for k in res:
        pct = k.endswith('pp')
        print(f'{k:22s} {fmt(res[k], pct=pct) if pct else fmt(res[k])}')


def run_mod(d, s):
    """Moderatoren: Effekte je Schicht (Richtigkeit), pp und logit."""
    groups = {}
    for kind in ['ok_clear', 'ok_noisy', 'fail_moderate', 'fail_subtle']:
        groups[f'kind={kind}'] = (lambda kk: (lambda r: r['kind'] == kk))(kind)
    for dom in ['coding', 'business', 'research']:
        groups[f'dom={dom}|ok'] = (lambda dd: (lambda r: r['domain'] == dd and r['truth']))(dom)
        groups[f'dom={dom}|fail'] = (lambda dd: (lambda r: r['domain'] == dd and not r['truth']))(dom)
    groups['fail&primary'] = lambda r: (not r['truth']) and r['primary']
    groups['fail&nonprimary'] = lambda r: (not r['truth']) and not r['primary']
    for sub in (1, 2, 3):
        groups[f'fail&subtl={sub}'] = (lambda ss: (lambda r: (not r['truth']) and r['subtlety'] == ss))(sub)
    faults = sorted({r['fault'] for i in d for r in d[i]['S'].values() if not r['truth']})
    for fa in faults:
        groups[f'fault={fa}'] = (lambda ff: (lambda r: r['fault'] == ff))(fa)

    def stat(ids):
        o = {}
        for m in MODELS:
            for g, fl in groups.items():
                # Basisniveau
                vals = [r['correct'] for i in ids for r in d[i][m].values() if fl(r)]
                o[f'{m}|{g}|base'] = mean(vals)
                for f in FACT:
                    pp, lg = eff(d, ids, m, f, filt=fl)
                    o[f'{m}|{g}|{f}_pp'] = pp
                    o[f'{m}|{g}|{f}_lo'] = lg
        return o
    res = boot(strata(d), stat, B=500, seed=s + 2)
    print(f'\n===== Satz {s}: Moderatoren (Richtigkeit; pp und logit) =====')
    for m in MODELS:
        print(f'--- Modell {m}')
        for g in groups:
            b = res[f'{m}|{g}|base']
            line = f'{g:30s} acc={100*b[0]:5.1f} '
            for f in FACT:
                pp = res[f'{m}|{g}|{f}_pp']; lg = res[f'{m}|{g}|{f}_lo']
                line += f'| {f}: {100*pp[0]:+5.1f}pp [{100*pp[1]:+5.1f};{100*pp[2]:+5.1f}] lo {lg[0]:+5.2f} '
            print(line)
    return res


def behaviour_cells(d, s):
    print(f'\n===== Satz {s}: Vorgehen je Zelle =====')
    for m in MODELS:
        for c in CELLS:
            rs = [d[i][m][c] for i in d]
            print(f'{m} {c}: acc={mean(r["correct"] for r in rs):.3f} sens={mean(r["correct"] for r in rs if not r["truth"]):.3f} '
                  f'spec={mean(r["correct"] for r in rs if r["truth"]):.3f} lookup={mean(int(r["looked_up"]) for r in rs):.3f} '
                  f'rightsec={mean(int(bool(r["right_section"])) for r in rs):.3f} conf={mean(r["confidence"] or 0 for r in rs):.3f} '
                  f'tools={mean(r["n_tool_calls"] for r in rs):.2f} tok={mean(r["completion_tokens"] for r in rs):.0f}')


def sp_mediation(d, s):
    """Explorativ/geplant H-SP: Richtigkeit bei primary-Fehlern nach SP und right_section."""
    print(f'\n===== Satz {s}: H-SP primary-Fehler nach SP und Nachschlagen =====')
    for m in MODELS:
        for sp in (0, 1):
            for prim in (True, False):
                rs = [r for i in d for r in d[i][m].values() if r['SP'] == sp and (not r['truth']) and r['primary'] == prim]
                for key, lab in [('right_section', 'rightsec'), ('looked_up', 'lookup')]:
                    for v in (True, False):
                        sub = [r for r in rs if bool(r[key]) == v]
                        if sub:
                            print(f'{m} SP={sp} primary={prim!s:5s} {lab}={v!s:5s} n={len(sub):4d} acc={mean(r["correct"] for r in sub):.3f}')


for s in (6000, 7000):
    d = idx[s]
    behaviour_cells(d, s)
    run_main(d, s)
    run_inter(d, s)
    run_mod(d, s)
    sp_mediation(d, s)
