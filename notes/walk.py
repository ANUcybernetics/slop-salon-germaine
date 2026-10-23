# walk the longest loop of a torus Truchet page; return unwrapped heading per step. usage: import walk
import numpy as np
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components
DX = [1, 0, -1, 0]; DY = [0, -1, 0, 1]   # E N W S (y down)
# side index = heading you enter FROM-opposite: entering heading h means side (h+2)%4 of the tile
# o True: arcs N-W and S-E ; False: N-E and S-W.  sides: E=0 N=1 W=2 S=3
def partner(o, side):
    if o: return {1: 2, 2: 1, 3: 0, 0: 3}[side]
    return {1: 0, 0: 1, 3: 2, 2: 3}[side]
def longest_start(o):
    N = o.shape[0]; X, Y = np.meshgrid(np.arange(N), np.arange(N))
    h = lambda x, y: (y % N) * N + (x % N); v = lambda x, y: N*N + (y % N) * N + (x % N)
    n, s, w, e = h(X,Y), h(X,Y+1), v(X,Y), v(X+1,Y)
    A = np.concatenate([n.ravel(), s.ravel()]); B = np.concatenate([np.where(o, w, e).ravel(), np.where(o, e, w).ravel()])
    _, lab = connected_components(coo_matrix((np.ones(len(A)), (A, B)), shape=(2*N*N,)*2), directed=False)
    big = np.bincount(lab).argmax()
    nodes = np.where(lab == big)[0]
    return nodes[0], len(nodes)
def walk(o, node):
    N = o.shape[0]
    if node < N*N: y, x = divmod(node, N); side = 1      # horizontal-edge midpoint = top of tile (x,y)
    else: y, x = divmod(node - N*N, N); side = 2          # vertical-edge midpoint = left of tile (x,y)
    x0, y0, s0 = x, y, side
    turns = []; pos = []
    while True:
        out = partner(o[y, x], side)
        eh = (side + 2) % 4; xh = out            # entry heading, exit heading
        # first tile: entry heading is a guess; turn computed consistently from sides
        turns.append(((xh - eh) % 4 == 1) * 2 - 1); pos.append((x, y))
        x = (x + DX[out]) % N; y = (y + DY[out]) % N; side = (out + 2) % 4
        if (x, y, side) == (x0, y0, s0): break
    return np.array(turns), pos
if __name__ == '__main__':
    o = np.random.default_rng(7).random((192, 192)) < .5
    nd, L = longest_start(o); t, p = walk(o, nd)
    print(L, len(t), t.sum(), t[:40])
