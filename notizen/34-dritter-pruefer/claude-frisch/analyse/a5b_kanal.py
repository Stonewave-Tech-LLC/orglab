"""Explorativ: Fehler bei ZU0 nach Fehlerart × vorgelegtem Kanal, beide Sätze; Anteil der Sonnet-Fehler in ZU0."""
from lib import *
from collections import defaultdict
R = load()
for m in MODELS:
    rs = [r for r in R if r['m'] == m and not r['correct']]
    print(f'{m}: Fehler gesamt {len(rs)}, davon ZU0 {sum(r["ZU"]==0 for r in rs)}, davon kaputte Belege {sum(not r["truth"] for r in rs)}')
print()
t = defaultdict(lambda: defaultdict(lambda: [0, 0]))
for r in R:
    if r['ZU'] == 0 and r['domain'] == 'coding':
        key = (r['fault'], r['presented'])
        t[key][(r['m'], r['set'])][0] += 1 - r['correct']; t[key][(r['m'], r['set'])][1] += 1
for key in sorted(t):
    print(f'{key[0]:14s} {key[1]:8s} ' + '  '.join(f'{m}{s}: {t[key][(m,s)][0]:2d}/{t[key][(m,s)][1]:2d}' for m in MODELS for s in (6000, 7000)))
