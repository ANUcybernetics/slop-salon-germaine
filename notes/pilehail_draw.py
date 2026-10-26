# Truchet arcs on a crop of the sandpile page, next to a coin page; colour = log curve length. usage: python notes/pilehail_draw.py W T OUT (needs /tmp/pile_z.npy)
import sys, numpy as np
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components
from PIL import Image, ImageDraw
import matplotlib; cm = matplotlib.colormaps['magma']
W, T, out = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
Z = np.load('/tmp/pile_z.npy'); c = len(Z)//2; N = W
def page(o):
    I, J = np.meshgrid(np.arange(N), np.arange(N))
    h = lambda x, y: y*(N+1) + x; v = lambda x, y: (N+1)**2 + y*(N+1) + x
    n, s, w, e = h(I,J), h(I,J+1), v(I,J), v(I+1,J)
    b = np.where(o, w, e); d = np.where(o, e, w)
    A = np.concatenate([n.ravel(), s.ravel()]); B = np.concatenate([b.ravel(), d.ravel()]); M = 2*(N+1)**2
    _, lab = connected_components(coo_matrix((np.ones(len(A)), (A, B)), shape=(M, M)), directed=False)
    size = np.bincount(lab); col = lambda k: tuple(int(255*q) for q in cm(0.05 + 0.9*np.log(size[lab[k]])/np.log(size.max()))[:3])
    img = Image.new('RGB', (W*T, W*T), (14, 14, 18)); dr = ImageDraw.Draw(img); lw = max(2, T//4)
    for j in range(W):
        for i in range(W):
            x, y = i*T, j*T
            if o[j, i]:
                dr.arc([x-T//2, y-T//2, x+T//2, y+T//2], 0, 90, fill=col(n[j, i]), width=lw)
                dr.arc([x+T//2, y+T//2, x+3*T//2, y+3*T//2], 180, 270, fill=col(s[j, i]), width=lw)
            else:
                dr.arc([x+T//2, y-T//2, x+3*T//2, y+T//2], 90, 180, fill=col(n[j, i]), width=lw)
                dr.arc([x-T//2, y+T//2, x+T//2, y+3*T//2], 270, 360, fill=col(s[j, i]), width=lw)
    return img
a = page((Z[c-W//2:c+W//2, c-W//2:c+W//2] & 1) == 1)
b = page(np.random.default_rng(1).random((W, W)) < .6)
g = 24; im = Image.new('RGB', (W*T*2+g, W*T), (14, 14, 18)); im.paste(a, (0, 0)); im.paste(b, (W*T+g, 0)); im.save(out)
