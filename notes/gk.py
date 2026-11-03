#!/usr/bin/env python3
"""Gauss-Kuzmin: python gk.py OUT.png [DIGITS]. Digit counts a=1..8 (+ >8) vs expected, for cubics/pi/e, z-scores against random reals."""
import sys, random, numpy as np
from math import log2, log, sqrt
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
OUT = sys.argv[1]; Dg = int(sys.argv[2]) if len(sys.argv) > 2 else 3000
S = 10**Dg
def cf(num, den, n=10**9):
    out = []
    while den and len(out) < n:
        a = num//den; num, den = den, num-a*den; out.append(a)
    return out
def root(f, lo, hi):
    while hi-lo > 1:
        m = (lo+hi)//2
        if f(m) < 0: lo = m
        else: hi = m
    return lo
def atan_inv(x, P):
    s = t = P//x; x2 = x*x; n = 1; sg = 1
    while t:
        t //= x2; n += 2; sg = -sg; s += sg*(t//n)
    return s
PP = 10**(Dg+20)
nums = {}
nums['cbrt 2'] = (root(lambda x: x**3-2*S**3, S, 2*S), S)
nums['plastic'] = (root(lambda x: x**3-x*S*S-S**3, S, 2*S), S)
nums['pi'] = (4*(4*atan_inv(5, PP)-atan_inv(239, PP)), PP)
# e = sum 1/k!
P = 10**(Dg+20); t = P; s = P; k = 1
while t:
    t //= k; s += t; k += 1
nums['e'] = (s, P)
K = 9
p = np.array([-log2(1-1/(a+1)**2) for a in range(1, K)]); p = np.append(p, 1-p.sum())
def counts(a):
    a = np.array(a); c = np.array([(a == i).sum() for i in range(1, K)]); return np.append(c, (a >= K).sum())
def chi(c):
    n = c.sum(); e = n*p; return ((c-e)**2/e).sum(), n
curves = {k: cf(*v)[:int(Dg*0.9/1.03/ log(10)*1.1866*0+Dg*0.9*2.30259/1.1866/1.0)] for k, v in nums.items()}
# usable quotients ~ Dg*ln10/(2*1.1866) (pairs of digits per quotient); trim to 85%
M = int(Dg*2.302585/(2*1.1866)*0.85)
random.seed(3)
rnd = [counts(cf(S+random.randrange(S), S)[:M]) for _ in range(300)]
rchi = np.array([chi(c)[0] for c in rnd])
fig, (a1, a2) = plt.subplots(1, 2, figsize=(11, 5), dpi=130, gridspec_kw={'width_ratios': [3, 2]})
cols = {'cbrt 2': '#d95f02', 'plastic': '#1b9e77', 'pi': '#000000', 'e': '#7570b3'}
w = 0.2; x = np.arange(K)
R = np.array(rnd)/ (M*p)
a1.fill_between(x, np.percentile(R, 5, axis=0), np.percentile(R, 95, axis=0), color='#dddddd', step=None, label='300 random reals, 5-95%')
for i, (k, c) in enumerate(curves.items()):
    cc = counts(c[:M]); a1.plot(x, cc/(M*p), 'o-', color=cols[k], label=k, lw=1)
    x2, n = chi(cc); print(k, 'M', M, 'chi2', round(x2, 2), 'rank among random', round((rchi < x2).mean(), 3), 'counts', cc.tolist())
a1.axhline(1, color='k', lw=.5); a1.set_xticks(x); a1.set_xticklabels([str(i) for i in range(1, K)]+['9+'])
a1.set_xlabel('quotient a'); a1.set_ylabel('observed / Gauss-Kuzmin expected'); a1.legend(frameon=False)
a2.hist(rchi, bins=30, color='#cccccc'); 
for k, c in curves.items():
    a2.axvline(chi(counts(c[:M]))[0], color=cols[k], lw=2, label=k)
a2.set_xlim(0, 30); a2.text(29, a2.get_ylim()[1]*0.8, 'e: %d  ->' % chi(counts(curves['e'][:M]))[0], ha='right', color=cols['e'])
a2.set_xlabel('chi-square of 9 bins (8 dof) '); a2.set_title(f'{M} quotients each')
for a in (a1, a2):
    for s in ('top', 'right'): a.spines[s].set_visible(False)
fig.tight_layout(); fig.savefig(OUT)
print('random chi2 mean', rchi.mean(), 'p95', np.percentile(rchi, 95))
