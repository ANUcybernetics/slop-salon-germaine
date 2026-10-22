# Coin page vs cascade page (q=.2, all scales) coloured by curve length, plus ccdf on a 1024 torus. usage: python notes/cascade_fig.py
import sys, numpy as np; sys.argv = ['x']
exec(open('notes/cascade.py').read().split("if __name__")[0])
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components
from PIL import Image, ImageDraw
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
cm = matplotlib.colormaps['magma']
def page(o, T):
    N = o.shape[0]; I, J = np.meshgrid(np.arange(N), np.arange(N))
    h = lambda x, y: (y % N) * N + (x % N); v = lambda x, y: N*N + (y % N) * N + (x % N)
    n, s, w, e = h(I,J), h(I,J+1), v(I,J), v(I+1,J); b = np.where(o, w, e); d = np.where(o, e, w)
    A = np.concatenate([n.ravel(), s.ravel()]); B = np.concatenate([b.ravel(), d.ravel()])
    _, lab = connected_components(coo_matrix((np.ones(len(A)), (A, B)), shape=(2*N*N,)*2), directed=False)
    size = np.bincount(lab); col = lambda k: tuple(int(255*c) for c in cm(0.08 + 0.9*np.log(size[lab[k]]) / np.log(size.max()))[:3])
    img = Image.new('RGB', (N*T, N*T), (14, 14, 18)); dr = ImageDraw.Draw(img); W = max(2, T//4)
    for j in range(N):
        for i in range(N):
            x, y = i*T, j*T
            if o[j, i]:
                dr.arc([x-T//2, y-T//2, x+T//2, y+T//2], 0, 90, fill=col(n[j, i]), width=W)
                dr.arc([x+T//2, y+T//2, x+3*T//2, y+3*T//2], 180, 270, fill=col(s[j, i]), width=W)
            else:
                dr.arc([x+T//2, y-T//2, x+3*T//2, y+T//2], 90, 180, fill=col(n[j, i]), width=W)
                dr.arc([x-T//2, y+T//2, x+T//2, y+3*T//2], 270, 360, fill=col(s[j, i]), width=W)
    return img
N, T = 128, 6
rng = np.random.default_rng(5)
a = page(rng.random((N, N)) < .5, T); b = page(cascade(N, .2, 0, np.random.default_rng(5)), T)
sheet = Image.new('RGB', (2*N*T + 12, N*T), (14, 14, 18)); sheet.paste(a, (0, 0)); sheet.paste(b, (N*T + 12, 0)); sheet.save('assets/cascade_pages.png')
fig, ax = plt.subplots(figsize=(6, 4.5), facecolor='#0e0e12'); ax.set_facecolor('#0e0e12')
M = 1024; E = np.unique(np.round(np.logspace(1.2, 5.3, 40)).astype(int))
for lab_, f, c, S in (('coin flips', lambda s: np.random.default_rng(s).random((M, M)) < .5, '#8890a8', 4),
                      ('scales stacked, q=.2', lambda s: cascade(M, .2, 0, np.random.default_rng(s)), '#ffd070', 4)):
    L = np.concatenate([lengths(f(s)) for s in range(S)]); ge = np.array([(L >= e).sum() for e in E]) / S
    k = ge >= 1; ax.loglog(E[k], ge[k], 'o-', ms=3, color=c, label=lab_)
x = np.array([30, 3000]); ax.loglog(x, 1.6e4*(x/30.)**(-1.0), '--', color='#c66', lw=1); ax.text(1500, 2.5e2, 'slope -1', color='#c88', fontsize=9)
ax.set_xlabel('curve length L', color='#aaa'); ax.set_ylabel('curves of length >= L (1024 torus)', color='#aaa'); ax.tick_params(colors='#888')
for s in ax.spines.values(): s.set_color('#444')
ax.legend(facecolor='#0e0e12', labelcolor='#ccc', edgecolor='#444'); plt.tight_layout(); plt.savefig('assets/cascade_plot.png', dpi=130, facecolor=fig.get_facecolor())
