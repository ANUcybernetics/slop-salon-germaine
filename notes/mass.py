# share of all edges carried by curves of each length decade. usage: python notes/mass.py
import numpy as np
exec(open('notes/below.py').read().split("if __name__")[0])
def mass(N, g, seeds=4):
    out = np.zeros(7); 
    for s in range(seeds):
        L = lengths(g(N, np.random.default_rng(s)))
        d = np.floor(np.log10(L)).astype(int)
        for k in range(7): out[k] += L[d == k].sum()
    return out / out.sum()
N = 512; K = 10
rules = {
 'coin': lambda N, r: r.random((N, N)) < .5,
 'cascade q.2': lambda N, r: casc(N, [.2]*K, r),
 'q.02 r.6': lambda N, r: casc(N, [min(.5, .02*.6**l) for l in range(K)], r),
 'q.3 r.6': lambda N, r: casc(N, [min(.5, .3*.6**l) for l in range(K)], r),
 'q.01 r1': lambda N, r: casc(N, [.01]*K, r),
}
for k, g in rules.items(): print(f'{k:12s}', np.round(mass(N, g), 2))
