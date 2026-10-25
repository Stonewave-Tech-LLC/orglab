"""Frage 6: Gegenproben und Robustheit."""
from lib import *
import re, json
from collections import defaultdict, Counter

R = load()
idx = index(R)

# 1. Stimmt das Feld verdict mit dem letzten JSON im Text 'final' überein? (Messfehler beim Parsen)
print('===== 1. verdict gegen letztes JSON im Endtext =====')
mis = Counter(); tot = Counter(); nojson = Counter()
for r in R:
    if r['vnull']:
        continue
    ms = re.findall(r'\{[^{}]*"works"\s*:\s*(true|false)[^{}]*\}', r['final'])
    tot[r['m']] += 1
    if not ms:
        nojson[r['m']] += 1
        continue
    v = ms[-1] == 'true'
    if v != r['verdict']:
        mis[r['m']] += 1
for m in MODELS:
    print(f'{m}: Urteile {tot[m]}, ohne JSON im Endausschnitt {nojson[m]}, Widerspruch {mis[m]}')

# 2. Fehlende Urteile ausgeschlossen statt als falsch
print('\n===== 2. Fehlende Urteile ausgeschlossen =====')
R2 = load(null_as_wrong=False)
for s in (6000, 7000):
    for m in MODELS:
        rs = [r for r in R2 if r['set'] == s and r['m'] == m and r['correct'] is not None]
        ra = [r for r in R if r['set'] == s and r['m'] == m]
        print(f'{s} {m}: Trefferquote ohne Nulls {mean(r["correct"] for r in rs):.4f} (mit Nulls als falsch {mean(r["correct"] for r in ra):.4f})')
nb = [r for r in R if r['vnull']]
print('Nulls nach Beleg:', Counter((r['id'], r['m']) for r in nb))
# Gemeinsame Fehler ohne den Timeout-Beleg
d = idx[7000]
both = sum((1 - d[i]['S'][c]['correct']) * (1 - d[i]['H'][c]['correct']) for i in d for c in CELLS)
both2 = sum((1 - d[i]['S'][c]['correct']) * (1 - d[i]['H'][c]['correct']) for i in d for c in CELLS if i != 'business-fail_moderate-7016')
print(f'7000 gemeinsame Fehler {both}, ohne business-fail_moderate-7016: {both2}')

# 3. Drift / Lauf: Modellabstand und Effekte je Satz (aus a1/a2) – hier kompakt: Differenz der Haupteffekte zwischen Sätzen
print('\n===== 3. Replikation 6000 gegen 7000: Haupteffekte (pp) je Modell =====')
for m in MODELS:
    for f in ['SP', 'ZU', 'AU']:
        vals = []
        for s in (6000, 7000):
            rs = [r for r in R if r['set'] == s and r['m'] == m]
            e = mean(r['correct'] for r in rs if r[f] == 1) - mean(r['correct'] for r in rs if r[f] == 0)
            vals.append(e)
        print(f'{m} {f}: 6000 {100*vals[0]:+5.1f}pp, 7000 {100*vals[1]:+5.1f}pp')

# 4. Haiku-Nachschlagen in SP1-ZU1: ist das Nicht-Nachschlagen belegspezifisch oder zufällig?
print('\n===== 4. Haiku: Konsistenz des Nachschlagens zwischen AU0 und AU1 (gleicher Beleg, gleiche SP/ZU) =====')
for s in (6000, 7000):
    d = idx[s]
    for sp, zu in [(1, 1), (1, 0), (0, 1), (0, 0)]:
        a = [int(d[i]['H'][f'SP{sp}-ZU{zu}-AU0']['looked_up']) for i in d]
        b = [int(d[i]['H'][f'SP{sp}-ZU{zu}-AU1']['looked_up']) for i in d]
        pa, pb = mean(a), mean(b)
        po = mean(int(x == y) for x, y in zip(a, b))
        pe = pa * pb + (1 - pa) * (1 - pb)
        k = (po - pe) / (1 - pe) if pe < 1 else float('nan')
        print(f'{s} SP{sp}-ZU{zu}: Nachschlagen AU0 {pa:.2f}, AU1 {pb:.2f}, κ(AU0,AU1) {k:+.2f}')
    # Nachschlagen nach Domäne in SP1-ZU1
    dd = defaultdict(list)
    for i in d:
        for au in (0, 1):
            r = d[i]['H'][f'SP1-ZU1-AU{au}']
            dd[(r['domain'], r['truth'])].append(int(r['looked_up']))
    print('   SP1-ZU1 Nachschlagequote nach Domäne/Wahrheit:', {k: round(mean(v), 2) for k, v in sorted(dd.items())})

# 5. Konfidenz bei den Haiku-Fehlern in SP1-ZU1 (primary): stille Fehler?
print('\n===== 5. Konfidenz: Haiku SP1-ZU1, primary-Fehler =====')
rs = [r for r in R if r['m'] == 'H' and r['SP'] == 1 and r['ZU'] == 1 and (not r['truth']) and r['primary'] and not r['vnull']]
print(f'richtig n={sum(r["correct"] for r in rs)}, mittl. Konfidenz {mean(r["confidence"] for r in rs if r["correct"]):.3f}; '
      f'falsch n={sum(1-r["correct"] for r in rs)}, mittl. Konfidenz {mean(r["confidence"] for r in rs if not r["correct"]):.3f}')
rs = [r for r in R if r['m'] == 'H' and r['truth'] and r['ZU'] == 0 and not r['vnull']]
print(f'Haiku ZU0 intakte Belege: falsch-Alarm n={sum(1-r["correct"] for r in rs)}, Konfidenz {mean(r["confidence"] for r in rs if not r["correct"]):.3f}; '
      f'richtig Konfidenz {mean(r["confidence"] for r in rs if r["correct"]):.3f}')
rs = [r for r in R if r['m'] == 'S' and (not r['truth']) and r['ZU'] == 0 and not r['vnull']]
print(f'Sonnet ZU0 kaputte Belege: übersehen n={sum(1-r["correct"] for r in rs)}, Konfidenz {mean(r["confidence"] for r in rs if not r["correct"]):.3f}; '
      f'erkannt Konfidenz {mean(r["confidence"] for r in rs if r["correct"]):.3f}')

# 6. AU: Bezieht sich der Endtext auf den Agentenbericht? (explorativ, grobe Textsuche)
print('\n===== 6. AU1: Erwähnung des Agentenberichts im Endausschnitt (explorativ) =====')
pat = re.compile(r'all checks green|agent|"done', re.I)
for m in MODELS:
    for truth in (True, False):
        rs = [r for r in R if r['m'] == m and r['AU'] == 1 and r['truth'] == truth and not r['vnull']]
        men = [r for r in rs if pat.search(r['final'])]
        nmen = [r for r in rs if not pat.search(r['final'])]
        print(f'{m} truth={truth!s:5s}: erwähnt {len(men)}/{len(rs)}; Trefferquote erwähnt {mean(r["correct"] for r in men):.3f}, '
              f'nicht erwähnt {mean(r["correct"] for r in nmen):.3f}')
    rs0 = [r for r in R if r['m'] == m and r['AU'] == 0 and not r['vnull']]
    print(f'   {m} AU0 Kontrolle: Muster trifft in {sum(bool(pat.search(r["final"])) for r in rs0)}/{len(rs0)}')

# 7. Werkzeugrunden-Kappung
print('\n===== 7. Läufe mit 6 Werkzeugrunden =====')
for r in R:
    if r['n_tool_calls'] >= 6:
        print(r['set'], r['m'], r['id'], r['cell'], r['correct'])

# 8. ZU1: Reihenfolge – riefen die Modelle zuerst die Kanäle oder zuerst das Runbook? (nicht in Daten) -> nur Zählung
print('\n===== 8. ZU1: Anteil mit allen 3 Kanälen und Nachschlagen je Modell =====')
for m in MODELS:
    rs = [r for r in R if r['m'] == m and r['ZU'] == 1]
    print(f'{m}: alle 3 Kanäle {mean(int(r["distinct_checks"]>=3) for r in rs):.3f}, nachgeschlagen {mean(int(r["looked_up"]) for r in rs):.3f}')
