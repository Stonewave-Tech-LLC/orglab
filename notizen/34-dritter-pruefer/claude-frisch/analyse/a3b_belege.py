"""Beleg-Ebene: Fehler je Beleg (von 8 Zellen) je Modell; Verteilung und schwerste Belege."""
from lib import *
from collections import Counter
R = load(); idx = index(R); G = load_gpt()
for s in (6000, 7000):
    d = idx[s]
    for m in MODELS:
        e = {i: sum(1 - d[i][m][c]['correct'] for c in CELLS) for i in d}
        print(f'{s} {m}: Verteilung Fehler/8 je Beleg: {sorted(Counter(e.values()).items())}')
    print(f'{s}: Belege mit >=3/8 Fehlern bei einem Modell:')
    for i in sorted(d):
        es = sum(1 - d[i]['S'][c]['correct'] for c in CELLS); eh = sum(1 - d[i]['H'][c]['correct'] for c in CELLS)
        if es >= 3 or eh >= 3:
            r = d[i]['S'][CELLS[0]]
            g = G.get(i, {}).get('decidable', '-')
            print(f'   {i:34s} {r["fault"]:16s} Kanal={r["presented"]:10s} S={es}/8 H={eh}/8 GPT-entscheidbar={g}')
