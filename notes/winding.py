# variance of heading change over a window w, along the longest loop of a rule. usage: python notes/winding.py
import numpy as np, sys
sys.path.insert(0, 'notes')
from walk import longest_start, walk
def popc(a):
    c = np.zeros_like(a)
    while a.any(): c += a & 1; a = a >> 1
    return c
def rules(N):
    I, J = np.meshgrid(np.arange(N), np.arange(N)); I = I.astype(np.int64); J = J.astype(np.int64)
    return {'coin': np.random.default_rng(7).random((N, N)) < .5,
            'sierp (i&j)==0': (I & J) == 0,
            'parity(i&j)': popc(I & J) % 2 == 1,
            'i*j>>10 odd': (((I * J) >> 10) & 1) == 1}
W = [2**k for k in range(0, 14)]
for N in (192, 512):
    for name, o in rules(N).items():
        nd, L = longest_start(o); t, _ = walk(o, nd); n = len(t)
        h = np.concatenate([[0], np.cumsum(t)])
        row = []
        for w in W:
            if w * 4 > n: break
            d = h[w:] - h[:-w]
            row.append(d.var())
        print(f'N={N:4d} {name:16s} loop {n:7d} net {t.sum():4d} var@2^k:', np.round(row, 1))
