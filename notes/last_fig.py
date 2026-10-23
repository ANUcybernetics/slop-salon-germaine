# coin torus page, arcs painted by decade of their curve's length; beside it, who reaches each decade. usage: python notes/last_fig.py
import numpy as np
from PIL import Image, ImageDraw
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
def comps(o):
    N = o.shape[0]; X, Y = np.meshgrid(np.arange(N), np.arange(N))
    h = lambda x, y: (y % N) * N + (x % N); v = lambda x, y: N*N + (y % N) * N + (x % N)
    n, s, w, e = h(X,Y), h(X,Y+1), v(X,Y), v(X+1,Y)
    A = np.concatenate([n.ravel(), s.ravel()]); B = np.concatenate([np.where(o, w, e).ravel(), np.where(o, e, w).ravel()])
    _, lab = connected_components(coo_matrix((np.ones(len(A)), (A, B)), shape=(2*N*N,)*2), directed=False)
    return lab, n, s
PAL = ['#2b2d42', '#4a6fa5', '#3fa7a0', '#d9c84a', '#ee8a3a', '#e8426b', '#ffffff']
N = 192; S = 10
o = np.random.default_rng(7).random((N, N)) < .5
lab, n, s = comps(o); size = np.bincount(lab)
img = Image.new('RGB', (N*S, N*S), '#0e0e12'); d = ImageDraw.Draw(img)
for y in range(N):
    for x in range(N):
        for (node, cx, cy, st) in ((n[y, x], x + (0 if o[y, x] else 1), y, 0 if o[y, x] else 90),
                                   (s[y, x], x + (1 if o[y, x] else 0), y + 1, 180 if o[y, x] else 270)):
            if not o[y, x]: st = {0: 90, 90: 90}.get(st, st)
            k = int(np.floor(np.log10(size[lab[node]])))
            r = S/2; px, py = cx*S, cy*S
            a0 = {(0,0): 0, (1,0): 90, (1,1): 180, (0,1): 270}[(cx-x, cy-y)]
            d.arc([px-r, py-r, px+r, py+r], a0, a0+90, fill=PAL[k], width=2)
img.save('assets/last_page.png')
print('longest', size.max(), 'decades', np.bincount(np.floor(np.log10(size[np.unique(lab)])).astype(int)))
