# Truchet page for rule (i&j)==0 on a torus; each curve coloured by its length. usage: python notes/sierp_draw.py N T OUT
import sys, numpy as np
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components
from PIL import Image, ImageDraw
import matplotlib; cm = matplotlib.colormaps['magma']
N, T, out = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
I, J = np.meshgrid(np.arange(N), np.arange(N)); o = (I & J) == 0
h = lambda x, y: (y % N) * N + (x % N); v = lambda x, y: N*N + (y % N) * N + (x % N)
n, s, w, e = h(I,J), h(I,J+1), v(I,J), v(I+1,J)
b = np.where(o, w, e); d = np.where(o, e, w)
A = np.concatenate([n.ravel(), s.ravel()]); B = np.concatenate([b.ravel(), d.ravel()])
_, lab = connected_components(coo_matrix((np.ones(len(A)), (A, B)), shape=(2*N*N,)*2), directed=False)
size = np.bincount(lab); col = lambda k: tuple(int(255*c) for c in cm(0.08 + 0.9*np.log(size[lab[k]]) / np.log(size.max()))[:3])
img = Image.new('RGB', (N*T, N*T), (14, 14, 18)); dr = ImageDraw.Draw(img); W = max(2, T//4)
for j in range(N):
    for i in range(N):
        x, y = i*T, j*T
        if o[j, i]:   # n-w arc at top-left corner, s-e arc at bottom-right
            dr.arc([x-T//2, y-T//2, x+T//2, y+T//2], 0, 90, fill=col(n[j, i]), width=W)
            dr.arc([x+T//2, y+T//2, x+3*T//2, y+3*T//2], 180, 270, fill=col(s[j, i]), width=W)
        else:         # n-e arc at top-right, s-w arc at bottom-left
            dr.arc([x+T//2, y-T//2, x+3*T//2, y+T//2], 90, 180, fill=col(n[j, i]), width=W)
            dr.arc([x-T//2, y+T//2, x+T//2, y+3*T//2], 270, 360, fill=col(s[j, i]), width=W)
img.save(out)
