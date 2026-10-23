# per-level flip prob q_l = min(.5, q0 * r**l): can the cascade go below slope -1? usage: python notes/below.py
import numpy as np
exec("import numpy as np\nfrom scipy.sparse import coo_matrix\nfrom scipy.sparse.csgraph import connected_components\ndef lengths" + open('notes/rules.py').read().split("def lengths")[1].split("def popc")[0])
def casc(N, qs, rng):
    o = np.zeros((N, N), bool)
    for l, q in enumerate(qs):
        b = 1 << l
        if b > N: break
        m = N // b; f = rng.random((m, m)) < q
        o ^= np.kron(f, np.ones((b, b), bool)).astype(bool)
    return o
def fit(N, qs, seeds=6, lo=30, hi=3000):
    L = np.concatenate([lengths(casc(N, qs, np.random.default_rng(s))) for s in range(seeds)]); T = seeds*N*N
    e = np.unique(np.round(np.logspace(np.log10(lo), np.log10(hi), 16)).astype(int))
    ge = np.array([(L >= x).sum() for x in e]) / T; ok = ge*T >= 10
    s, c = np.polyfit(np.log(e[ok]), np.log(ge[ok]), 1); return round(s, 2), L.max()
if __name__ == '__main__':
    N = 512; K = 10
    for q0 in (.02, .1, .3):
        for r in (.6, .8, 1, 1.25, 1.6):
            qs = [min(.5, q0*r**l) for l in range(K)]
            print('q0', q0, 'r', r, fit(N, qs), flush=True)
