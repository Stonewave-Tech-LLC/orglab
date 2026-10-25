"""Frage 1: Urteile und Vorgehen je Modell."""
from lib import *

R = load()
idx = index(R)


def recs(d, ids, m, cond=lambda r: True):
    for i in ids:
        for r in d[i][m].values():
            if cond(r):
                yield r


def make_stat(d):
    def stat(ids):
        out = {}
        for m in MODELS:
            rs = list(recs(d, ids, m))
            fail = [r for r in rs if not r['truth']]
            ok = [r for r in rs if r['truth']]
            zu1 = [r for r in rs if r['ZU'] == 1]
            val = [r for r in rs if not r['vnull']]
            out[f'{m}_acc'] = mean(r['correct'] for r in rs)
            out[f'{m}_sens'] = mean(r['correct'] for r in fail)
            out[f'{m}_spec'] = mean(r['correct'] for r in ok)
            out[f'{m}_pworks'] = mean(r['wtrue'] for r in val)
            out[f'{m}_conf'] = mean(r['confidence'] for r in val)
            out[f'{m}_conf_right'] = mean(r['confidence'] for r in val if r['correct'])
            out[f'{m}_conf_wrong'] = mean(r['confidence'] for r in val if not r['correct'])
            out[f'{m}_overconf'] = out[f'{m}_conf'] - mean(r['correct'] for r in val)
            # Brier: Wahrscheinlichkeit, dass das Urteil stimmt = confidence
            out[f'{m}_brier'] = mean((r['confidence'] - r['correct']) ** 2 for r in val)
            out[f'{m}_lookup'] = mean(int(r['looked_up']) for r in rs)
            out[f'{m}_rightsec'] = mean(int(bool(r['right_section'])) for r in rs)
            out[f'{m}_ntopics'] = mean(len(r['lookup_topics'] or []) for r in rs)
            out[f'{m}_zu1_nchecks'] = mean(r['n_checks'] for r in zu1)
            out[f'{m}_zu1_distinct'] = mean(r['distinct_checks'] for r in zu1)
            out[f'{m}_zu1_all3'] = mean(int(r['distinct_checks'] >= 3) for r in zu1)
            out[f'{m}_zu1_none'] = mean(int(r['distinct_checks'] == 0) for r in zu1)
            out[f'{m}_ntool'] = mean(r['n_tool_calls'] for r in rs)
            out[f'{m}_tokens'] = mean(r['completion_tokens'] for r in rs)
            out[f'{m}_cost'] = mean(r['cost_usd'] for r in rs)
        for k in list(out):
            if k.startswith('S_'):
                out['D(S-H)_' + k[2:]] = out[k] - out['H_' + k[2:]]
        return out
    return stat


for s in (6000, 7000):
    d = idx[s]
    res = boot(strata(d), make_stat(d), B=1000, seed=s)
    print(f'\n===== Satz {s} =====')
    keys = [k[2:] for k in res if k.startswith('S_')]
    print(f"{'Kennzahl':14s} {'Sonnet':>26s} {'Haiku':>26s} {'Sonnet-Haiku':>28s}")
    for k in keys:
        print(f"{k:14s} {fmt(res['S_'+k])} {fmt(res['H_'+k])} {fmt(res['D(S-H)_'+k])}")

    # AUROC Konfidenz für Richtigkeit (Punkt) und Konfidenz-Verteilung
    for m in MODELS:
        val = [r for i in d for r in d[i][m].values() if not r['vnull']]
        a = auroc([r['confidence'] for r in val], [r['correct'] for r in val])
        cs = sorted(set(round(r['confidence'], 2) for r in val))
        from collections import Counter
        c = Counter(round(r['confidence'], 2) for r in val)
        print(f'{m} AUROC(conf->richtig) = {a:.3f}; häufigste Konfidenzwerte: {c.most_common(6)}')
        # Kalibrierung in Bins
        bins = [(0, .7), (.7, .8), (.8, .9), (.9, .95), (.95, 1.01)]
        line = []
        for lo_, hi_ in bins:
            b = [r for r in val if lo_ <= r['confidence'] < hi_]
            if b:
                line.append(f'[{lo_:.2f},{hi_:.2f}) n={len(b)} acc={mean(r["correct"] for r in b):.2f}')
        print('   Kalibrierung: ' + ' | '.join(line))
        nn = sum(r['vnull'] for i in d for r in d[i][m].values())
        cap = sum(r['n_tool_calls'] >= 6 for i in d for r in d[i][m].values())
        print(f'   fehlende Urteile: {nn}, Läufe mit 6 Werkzeugrunden: {cap}')
