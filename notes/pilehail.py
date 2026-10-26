# Truchet page with tile = sandpile height parity (page 500^2, G grains). usage: python notes/pilehail.py N G OUT
import numpy as np, sys
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components
from PIL import Image
import matplotlib; cm = matplotlib.colormaps['magma']
N, G, out = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
z = np.zeros((N, N), np.int64); z[N//2, N//2] = G
while True:
    k = z // 4
    if not k.any(): break
    z -= 4*k
    z[1:] += k[:-1]; z[:-1] += k[1:]; z[:, :-1] += k[:, 1:]; z[:, 1:] += k[:, :-1]
np.save('/tmp/pile_z.npy', z)
def curves(o):
    I, J = np.meshgrid(np.arange(N), np.arange(N))
    h = lambda x, y: y*(N+1) + x; v = lambda x, y: (N+1)*(N+1) + y*(N+1) + x   # bordered
    n, s, w, e = h(I,J), h(I,J+1), v(I,J), v(I+1,J)
    b = np.where(o, w, e); d = np.where(o, e, w)
    A = np.concatenate([n.ravel(), s.ravel()]); B = np.concatenate([b.ravel(), d.ravel()])
    M = 2*(N+1)*(N+1)
    _, lab = connected_components(coo_matrix((np.ones(len(A)), (A, B)), shape=(M, M)), directed=False)
    return lab, np.bincount(lab), n
def stats(o, name):
    lab, size, n = curves(o); used = np.unique(lab[n]); sz = np.sort(size[used])[::-1]
    print(name, 'curves', len(sz), 'longest', sz[:5], 'median', int(np.median(sz)), 'mass in top10 %.2f' % (sz[:10].sum()/sz.sum()))
    return lab, size, n
rng = np.random.default_rng(1)
for name, o in [('pile parity', z & 1 == 1), ('pile h>=2', z >= 2), ('coin', rng.random((N, N)) < .5)]:
    lab, size, n = stats(o, name)
    if name == 'pile parity':
        c = cm(0.05 + 0.9*np.log(size[lab[n]]) / np.log(size.max()))[..., :3]
        Image.fromarray((c*255).astype(np.uint8)).resize((N*3, N*3), Image.NEAREST).save(out)
