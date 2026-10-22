# Which deterministic tile rule sits on a straight line (scale-free) on a torus? usage: python notes/rules.py OUT
import sys, numpy as np
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
def lengths(o):
    N = o.shape[0]
    X, Y = np.meshgrid(np.arange(N), np.arange(N))
    h = lambda x, y: (y % N) * N + (x % N)
    v = lambda x, y: N*N + (y % N) * N + (x % N)
    n, s, w, e = h(X,Y), h(X,Y+1), v(X,Y), v(X+1,Y)
    a = n; b = np.where(o, w, e); c = s; d = np.where(o, e, w)
    A = np.concatenate([a.ravel(), c.ravel()]); B = np.concatenate([b.ravel(), d.ravel()])
    g = coo_matrix((np.ones(len(A)), (A, B)), shape=(2*N*N,)*2)
    _, lab = connected_components(g, directed=False)
    return np.sort(np.bincount(lab))[::-1]
def popc(a):
    a = a.copy(); c = np.zeros_like(a)
    while a.any(): c += a & 1; a >>= 1
    return c
def field(N, beta, seed):
    r = np.random.default_rng(seed); f = np.fft.fft2(r.standard_normal((N, N)))
    k = np.hypot(*np.meshgrid(np.fft.fftfreq(N), np.fft.fftfreq(N))); k[0, 0] = 1
    return np.fft.ifft2(f / k**(beta/2)).real
def rules(N):
    I, J = np.meshgrid(np.arange(N), np.arange(N)); I = I.astype(np.int64); J = J.astype(np.int64)
    R = {}
    R['coin'] = np.random.default_rng(1).random((N, N)) < .5
    R['and'] = popc(I & J) & 1 == 1
    tm = popc(np.arange(N)) & 1
    R['thue-morse x'] = (tm[:, None] ^ tm[None, :]).astype(bool)
    R['tm(i+j)'] = (popc(I + J) & 1).astype(bool)
    R['tm(i*j)'] = (popc((I * J) % (1 << 20)) & 1).astype(bool)
    R['pascal mod 3'] = None
    R['1/f field b=1'] = field(N, 1, 2) > 0
    R['1/f field b=2'] = field(N, 2, 3) > 0
    R['1/f field b=0.5'] = field(N, .5, 4) > 0
    del R['pascal mod 3']
    return R
N = int(sys.argv[2]) if len(sys.argv) > 2 else 1024
edges = np.unique(np.round(np.logspace(np.log10(12), np.log10(N*N/3), 20)).astype(int))
fig, ax = plt.subplots(figsize=(7,5), facecolor='#0e0e12'); ax.set_facecolor('#0e0e12')
for name, o in rules(N).items():
    L = lengths(o); T = N*N
    ge = np.array([(L >= e).sum() for e in edges]) / T
    ok = ge*T >= 5
    ls, lg = np.log(edges[ok]), np.log(ge[ok]); loc = np.diff(lg)/np.diff(ls)
    sel = (edges >= 30) & ok
    if sel.sum() < 3: print(f'{name:16s} curves {len(L)} longest {L[0]} (too short to fit)'); continue
    p = np.polyfit(np.log(edges[sel]), np.log(ge[sel]), 1)
    res = np.std(np.log(ge[sel]) - np.polyval(p, np.log(edges[sel])))
    print(f'{name:16s} curves {len(L):7d} longest {L[0]:8d} slope {p[0]:.2f} resid {res:.2f}')
    ax.loglog(edges[ok], ge[ok], 'o-', ms=3, label=f'{name} ({p[0]:.2f})')
ax.set_xlabel('curve length L', color='#aaa'); ax.set_ylabel('curves >= L per tile', color='#aaa'); ax.tick_params(colors='#888')
for s in ax.spines.values(): s.set_color('#444')
ax.legend(facecolor='#0e0e12', labelcolor='#ccc', edgecolor='#444', fontsize=7)
plt.savefig(sys.argv[1], dpi=130, facecolor=fig.get_facecolor())
