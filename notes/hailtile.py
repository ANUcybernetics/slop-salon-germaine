# Truchet page whose tile (i,j) is a Collatz feature of n = i*N+j+1 (raster). usage: python notes/hailtile.py  (torus N=1024)
import numpy as np
exec("import numpy as np\nfrom scipy.sparse import coo_matrix\nfrom scipy.sparse.csgraph import connected_components\ndef lengths" + open('notes/rules.py').read().split("def lengths")[1].split("def popc")[0])
N = 1024
n0 = np.arange(1, N*N+1, dtype=np.int64)
x = n0.copy(); steps = np.zeros_like(x); odds = np.zeros_like(x)
while (x > 1).any():
    m = x > 1; od = m & (x & 1 == 1); ev = m & ~od
    x[od] = 3*x[od] + 1; x[ev] >>= 1
    steps[m] += 1; odds[od] += 1
S = steps.reshape(N, N); O = odds.reshape(N, N)
np.save('/tmp/hail_steps.npy', S); np.save('/tmp/hail_odds.npy', O)
R = {'coin': np.random.default_rng(1).random((N, N)) < .5,
     'steps odd': S & 1 == 1, 'odd-steps odd': O & 1 == 1, 'steps>median': S > np.median(S),
     'steps%3==0': S % 3 == 0, 'steps>>3 odd': (S >> 3) & 1 == 1}
edges = np.unique(np.round(np.logspace(np.log10(16), np.log10(3e5), 14)).astype(int))
for k, o in R.items():
    L = lengths(o); ge = np.array([(L >= e).sum() for e in edges]) / (N*N)
    sel = (edges >= 30) & (edges <= 3000) & (ge*N*N >= 10)
    sl = np.polyfit(np.log(edges[sel]), np.log(ge[sel]), 1)[0]
    d = np.floor(np.log10(L)).astype(int); m = np.array([L[d == q].sum() for q in range(7)]) / L.sum()
    print(f'{k:16s} frac {o.mean():.2f} longest {L[0]:7d} curves {len(L):7d} slope {sl:.2f}', np.round(m, 2))
