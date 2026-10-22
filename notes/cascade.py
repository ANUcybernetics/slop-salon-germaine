# Truchet tile = XOR over scales l of Bernoulli(q) flips on 2^l blocks. usage: python notes/cascade.py
import sys, numpy as np
exec("import numpy as np\nfrom scipy.sparse import coo_matrix\nfrom scipy.sparse.csgraph import connected_components\ndef lengths" + open('notes/rules.py').read().split("def lengths")[1].split("def popc")[0])
def cascade(N, q, lo, rng):
    o = np.zeros((N, N), bool); l = lo
    while (1 << l) <= N:
        b = 1 << l; m = N // b
        f = rng.random((m, m)) < q
        o ^= np.kron(f, np.ones((b, b), bool)).astype(bool); l += 1
    return o
edges = np.unique(np.round(np.logspace(np.log10(16), np.log10(2e5), 14)).astype(int))
def run(N, q, lo, seeds=3):
    L = np.concatenate([lengths(cascade(N, q, lo, np.random.default_rng(s))) for s in range(seeds)]); T = seeds*N*N
    ge = np.array([(L >= e).sum() for e in edges]) / T; ok = ge*T >= 20
    ls, lg = np.log(edges[ok]), np.log(ge[ok]); return np.round(np.diff(lg)/np.diff(ls), 2), L.max()
if __name__ == '__main__':
    N = 512
    for lo in (0, 1, 2):
        for q in (.5, .3, .15, .05):
            print('lo', lo, 'q', q, *run(N, q, lo))
