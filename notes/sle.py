# winding variance vs ln(chord) on the coin's giant loop (torus); compare kappa*lnR with kappa=6. usage: python notes/sle.py
import numpy as np, sys
sys.path.insert(0, 'notes')
from walk import longest_start, walk
Q = (np.pi/2)**2
for N, seed in ((512, 7), (1024, 3)):
    o = np.random.default_rng(seed).random((N, N)) < .5
    nd, L = longest_start(o); t, p = walk(o, nd); n = len(t)
    p = np.array(p); d = np.diff(p, axis=0, append=p[:1]); d = (d + N//2) % N - N//2
    P = np.vstack([[0, 0], np.cumsum(d, axis=0)[:-1]])
    h = np.concatenate([[0], np.cumsum(t)])
    rng = np.random.default_rng(1)
    lnn, lnR, var = [], [], []
    for k in range(3, int(np.log2(n)) - 1):
        w = 2**k; i = rng.integers(0, n - w, 20000)
        R = np.hypot(*(P[i + w] - P[i]).T); dh = h[i + w] - h[i]
        lnn.append(np.log(w)); lnR.append(np.log(R[R > 0]).mean()); var.append(dh.var())
    lnn, lnR, var = map(np.array, (lnn, lnR, var))
    m = slice(0, None)
    print(f'N={N} loop {n}: dlnR/dlnn = {np.polyfit(lnn[:-2], lnR[:-2], 1)[0]:.3f} (4/7=.571)')
    print('  var(qt^2) per ln n :', np.round(np.polyfit(lnn[:-2], var[:-2], 1)[0], 3))
    print('  var(qt^2) per ln R :', np.round(np.polyfit(lnR[:-2], var[:-2], 1)[0], 3), ' kappa=6 predicts', round(6 / Q, 3), '; kappa=8/3 would be', round(8/3/Q, 3))
    # chord-binned
    ii = rng.integers(0, n, 400000); ww = rng.integers(2, n // 4, 400000)
    jj = (ii + ww) % n; R = np.hypot(*(P[(ii + ww) % n] - P[ii]).T)
    dh = h[np.minimum(ii + ww, n)] - h[ii]; ok = (ii + ww) < n
    R, dh = R[ok], dh[ok]
    edges = 2.0 ** np.arange(2, 9); xs = []; vs = []
    for a, b in zip(edges[:-1], edges[1:]):
        s = (R >= a) & (R < b)
        if s.sum() > 500: xs.append(np.log(R[s]).mean()); vs.append(dh[s].var())
    print('  chord-binned var:', np.round(vs, 2), ' slope per ln R:', round(np.polyfit(xs, vs, 1)[0], 3))
