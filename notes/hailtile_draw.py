# Window of a 1024 torus Truchet page, curves coloured by global length. usage: python notes/hailtile_draw.py OUT  (needs /tmp/hail_steps.npy from hailtile.py)
import sys, numpy as np
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components
from PIL import Image, ImageDraw
import matplotlib; cm = matplotlib.colormaps['magma']
N = 1024; S = np.load('/tmp/hail_steps.npy')
def page(o, r0, c0, W, T, out):
    I, J = np.meshgrid(np.arange(N), np.arange(N))
    h = lambda x, y: (y % N) * N + (x % N); v = lambda x, y: N*N + (y % N) * N + (x % N)
    n, s, w, e = h(I,J), h(I,J+1), v(I,J), v(I+1,J)
    b = np.where(o, w, e); d = np.where(o, e, w)
    A = np.concatenate([n.ravel(), s.ravel()]); B = np.concatenate([b.ravel(), d.ravel()])
    _, lab = connected_components(coo_matrix((np.ones(len(A)), (A, B)), shape=(2*N*N,)*2), directed=False)
    size = np.bincount(lab); col = lambda k: tuple(int(255*c) for c in cm(0.05 + 0.9*np.log(size[lab[k]]) / np.log(size.max()))[:3])
    img = Image.new('RGB', (W*T, W*T), (14, 14, 18)); dr = ImageDraw.Draw(img); lw = max(2, T//4)
    for j in range(W):
        for i in range(W):
            x, y = i*T, j*T; jj, ii = r0+j, c0+i
            if o[jj, ii]:
                dr.arc([x-T//2, y-T//2, x+T//2, y+T//2], 0, 90, fill=col(n[jj, ii]), width=lw)
                dr.arc([x+T//2, y+T//2, x+3*T//2, y+3*T//2], 180, 270, fill=col(s[jj, ii]), width=lw)
            else:
                dr.arc([x+T//2, y-T//2, x+3*T//2, y+T//2], 90, 180, fill=col(n[jj, ii]), width=lw)
                dr.arc([x-T//2, y+T//2, x+T//2, y+3*T//2], 270, 360, fill=col(s[jj, ii]), width=lw)
    return img
hail = page(S & 1 == 1, 600, 200, 80, 14, None)
coin = page(np.random.default_rng(1).random((N, N)) < .5, 600, 200, 80, 14, None)
g = 24; im = Image.new('RGB', (hail.width*2 + g, hail.height), (14, 14, 18)); im.paste(hail, (0, 0)); im.paste(coin, (hail.width + g, 0))
im.save(sys.argv[1])
