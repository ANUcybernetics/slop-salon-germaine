# Coin-flip Truchet on a torus (no border cuts): local slope of curves-at-least-L per tile. usage: python notes/torus.py OUT
import sys, numpy as np
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
def lengths(N, seed):
    rng = np.random.default_rng(seed)
    o = rng.random((N, N)) < .5
    X, Y = np.meshgrid(np.arange(N), np.arange(N))
    h = lambda x, y: (y % N) * N + (x % N)
    v = lambda x, y: N*N + (y % N) * N + (x % N)
    n, s, w, e = h(X,Y), h(X,Y+1), v(X,Y), v(X+1,Y)
    a = np.where(o, n, n); b = np.where(o, w, e)
    c = np.where(o, s, s); d = np.where(o, e, w)
    A = np.concatenate([a.ravel(), c.ravel()]); B = np.concatenate([b.ravel(), d.ravel()])
    g = coo_matrix((np.ones(len(A)), (A, B)), shape=(2*N*N,)*2)
    _, lab = connected_components(g, directed=False)
    return np.sort(np.bincount(lab))[::-1]
out = sys.argv[1]
edges = np.unique(np.round(np.logspace(np.log10(12), np.log10(3e5), 22)).astype(int))
fig, ax = plt.subplots(figsize=(7,5), facecolor='#0e0e12'); ax.set_facecolor('#0e0e12')
for N, seeds, col in ((512, 8, '#6a7fb0'), (1024, 4, '#d6c27a'), (2048, 2, '#ffecaa')):
    L = np.concatenate([lengths(N, s) for s in range(seeds)]); T = seeds*N*N
    ge = np.array([(L >= e).sum() for e in edges]) / T
    ok = ge*T >= 30
    ls = np.log(edges[ok]); lg = np.log(ge[ok])
    loc = np.diff(lg)/np.diff(ls); mid = np.exp((ls[1:]+ls[:-1])/2)
    ax.semilogx(mid, loc, 'o-', color=col, label=f'{N}x{N} torus')
    print(N, 'longest', L[0], 'local slopes', np.round(loc, 2))
    sel = (edges >= 30) & (edges <= 3000) & ok
    print(N, 'fit 30..3000', round(np.polyfit(np.log(edges[sel]), np.log(ge[sel]), 1)[0], 3))
for y, t in ((-8/7, '-8/7'), (-7/8, '-7/8')):
    ax.axhline(y, color='#c66', ls='--', lw=1); ax.text(13, y+.015, t, color='#c88', fontsize=9)
ax.set_xlabel('curve length L', color='#aaa'); ax.set_ylabel('local slope of curves >= L, per tile', color='#aaa')
ax.tick_params(colors='#888')
for s in ax.spines.values(): s.set_color('#444')
ax.legend(facecolor='#0e0e12', labelcolor='#ccc', edgecolor='#444')
plt.savefig(out, dpi=130, facecolor=fig.get_facecolor())
