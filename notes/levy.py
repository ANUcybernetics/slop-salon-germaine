#!/usr/bin/env python3
"""Levy test: python levy.py OUT.png [DIGITS]. ln q_n vs 1.1866 n for cubic irrationals, pi, and a random-real band."""
import sys, random, numpy as np
from math import log, pi as PI, pi
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
OUT = sys.argv[1]; Dg = int(sys.argv[2]) if len(sys.argv) > 2 else 5000
S = 10**Dg; NQ = int(Dg/1.03/0.5*0.5)  # ~ digits*ln10/1.1866/ ... generous
LEVY = PI**2/(12*log(2))
def lnq(num, den, n):
    # ln q_n for n=0..: track q exactly
    out = []; q0, q1 = 0, 1
    for _ in range(n):
        if den == 0: break
        a = num//den; num, den = den, num - a*den
        q0, q1 = q1, a*q1 + q0
        out.append(q1)
    return out
def lnlist(qs):
    return np.array([log(q) if q.bit_length() < 1000 else (q.bit_length()-1)*log(2)+log(q/(1<<(q.bit_length()-1))) if False else (log(q >> (q.bit_length()-60)) + (q.bit_length()-60)*log(2)) for q in qs])
def root(f, lo, hi):  # increasing f on [lo,hi] (scaled ints), f(lo)<0<f(hi)
    while hi-lo > 1:
        m = (lo+hi)//2
        if f(m) < 0: lo = m
        else: hi = m
    return lo
cub = {}
cub['cbrt 2'] = root(lambda x: x**3 - 2*S**3, S, 2*S)
cub['plastic x3=x+1'] = root(lambda x: x**3 - x*S*S - S**3, S, 2*S)
cub['x3-3x-1'] = root(lambda x: x**3 - 3*x*S*S - S**3, S, 2*S)
def atan_inv(x, P):
    s = t = P//x; x2 = x*x; n = 1; sign = 1
    while t:
        t //= x2; n += 2; sign = -sign; s += sign*(t//n)
    return s
PP = 10**(Dg+20)
cub['pi'] = 4*(4*atan_inv(5, PP) - atan_inv(239, PP))
curves = {}
for k, v in cub.items():
    num, den = (v, S) if k != 'pi' else (v, PP)
    curves[k] = lnlist(lnq(num, den, 10**9))
random.seed(7)
rnd = []
for _ in range(300):
    r = random.randrange(S)
    rnd.append(lnlist(lnq(S + r, S, 10**9)))
M = min(min(len(c) for c in curves.values()), min(len(c) for c in rnd))
M = int(M*0.9)  # stay clear of the tail where precision runs out
n = np.arange(1, M+1)
def z(c): return c[:M] - LEVY*n
R = np.array([z(c) for c in rnd])
lo, hi, md = np.percentile(R, 5, axis=0), np.percentile(R, 95, axis=0), np.median(R, axis=0)
fig, ax = plt.subplots(figsize=(10, 6), dpi=130)
ax.fill_between(n, lo, hi, color='#cccccc', label='300 random reals, 5-95%')
ax.plot(n, md, color='#888888', lw=1)
cols = {'cbrt 2': '#d95f02', 'plastic x3=x+1': '#1b9e77', 'x3-3x-1': '#7570b3', 'pi': '#000000'}
for k, c in curves.items():
    ax.plot(n, z(c), color=cols[k], lw=1.4, label=k)
ax.axhline(0, color='k', lw=.5)
ax.set_xlabel('n (number of quotients)'); ax.set_ylabel('ln q_n  -  1.1866 n')
ax.legend(frameon=False, loc='upper left'); ax.set_title('Levy drift: are the cubics typical?')
for s in ('top', 'right'): ax.spines[s].set_visible(False)
fig.tight_layout(); fig.savefig(OUT)
# summary: percentile rank of each at the end
for k, c in curves.items():
    zz = z(c)
    print(k, 'final', round(zz[-1], 2), 'rank among random', round((R[:, -1] < zz[-1]).mean(), 3), 'n', M,
          'min rank', round(min((R[:, i] < zz[i]).mean() for i in range(M)), 3), 'max rank', round(max((R[:, i] < zz[i]).mean() for i in range(M)), 3))
