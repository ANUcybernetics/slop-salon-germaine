# curve-length stats of a Truchet page cropped inside the pile. usage: python notes/pilecrop.py W  (needs /tmp/pile_z.npy)
import numpy as np, sys
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components
z = np.load('/tmp/pile_z.npy'); N0 = len(z); W = int(sys.argv[1]); c = N0//2
ys, xs = np.nonzero(z); print('support half-width', (xs.max()-xs.min())//2)
z = z[c-W//2:c+W//2, c-W//2:c+W//2]; N = W
def curves(o):
    I, J = np.meshgrid(np.arange(N), np.arange(N))
    h = lambda x, y: y*(N+1) + x; v = lambda x, y: (N+1)*(N+1) + y*(N+1) + x
    n, s, w, e = h(I,J), h(I,J+1), v(I,J), v(I+1,J)
    b = np.where(o, w, e); d = np.where(o, e, w)
    A = np.concatenate([n.ravel(), s.ravel()]); B = np.concatenate([b.ravel(), d.ravel()]); M = 2*(N+1)**2
    _, lab = connected_components(coo_matrix((np.ones(len(A)), (A, B)), shape=(M, M)), directed=False)
    return np.sort(np.bincount(lab)[np.unique(lab[n])])[::-1]
rng = np.random.default_rng(1)
def rep(name, sz):
    print(f'{name:12s} curves {len(sz):5d} longest {sz[:4]} med {int(np.median(sz))} top10 mass {sz[:10].sum()/sz.sum():.2f} tiles {N*N}')
rep('pile parity', curves(z & 1 == 1)); rep('pile h>=2', curves(z >= 2)); rep('pile h>=1', curves(z >= 1)); rep('pile h==3', curves(z == 3))
rep('coin', curves(rng.random((N, N)) < .5))
# match density
p = (z & 1).mean(); rep('coin same p', curves(rng.random((N, N)) < p)); print('p', p)
