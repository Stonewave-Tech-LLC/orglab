"""Explorativ: Haiku, SP1, primary-Fehler: Richtigkeit nach Nachschlagen innerhalb Domäne × ZU (beide Sätze gepoolt)."""
from lib import *
from collections import defaultdict
R = load()
for m in MODELS:
    print(f'--- Modell {m}')
    t = defaultdict(lambda: [0, 0])
    for r in R:
        if r['m'] == m and r['SP'] == 1 and (not r['truth']) and r['primary']:
            k = (r['domain'], r['ZU'], bool(r['looked_up']))
            t[k][0] += r['correct']; t[k][1] += 1
    for k in sorted(t):
        print(f'   Domäne={k[0]:9s} ZU={k[1]} nachgeschlagen={k[2]!s:5s}: {t[k][0]:3d}/{t[k][1]:3d} = {t[k][0]/t[k][1]:.2f}')
    # Nachschlagequote je Domäne × SP × ZU (alle Belege)
    q = defaultdict(list)
    for r in R:
        if r['m'] == m:
            q[(r['domain'], r['SP'], r['ZU'])].append(int(r['looked_up']))
    print('   Nachschlagequote Domäne×SP×ZU: ' + '; '.join(f'{k[0][:3]} SP{k[1]} ZU{k[2]}: {mean(v):.2f}' for k, v in sorted(q.items())))
