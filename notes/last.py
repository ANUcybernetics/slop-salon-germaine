# share of edges per length decade, tidy rules on a torus. usage: python notes/last.py
import numpy as np
exec(open('notes/rules2.py').read().split("N = 1024")[0])
N = 1024
I, J = np.meshgrid(np.arange(N), np.arange(N)); I = I.astype(np.int64); J = J.astype(np.int64)
R = rules(N)
R['parity(i&j)'] = popc(I & J) % 2 == 1
R['stripes ((i^j)>>1)&1'] = (((I ^ J) >> 1) & 1) == 1
R['diag (i+j)>>1 &1'] = (((I + J) >> 1) & 1) == 1
for k, o in R.items():
    L = lengths(o); d = np.floor(np.log10(L)).astype(int)
    m = np.array([L[d == k_].sum() for k_ in range(7)]) / L.sum()
    print(f'{k:24s} longest {L[0]:8d} curves {len(L):7d}', np.round(m, 2))
