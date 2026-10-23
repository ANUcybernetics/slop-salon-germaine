# tiles the fill model drew inside 8x8 holes vs the coin it replaced. usage: python notes/fill_stats.py SEEDS...
import numpy as np, sys
sys.path.insert(0, 'notes')
from fill import read, Image
def rings(o):  # 2x2 blocks that close a ring: NW tile True?? ring = [[T? ...]] tiles (0,0)=o False.. compute via arcs: centre corner shared by four tiles
    # centre corner is NW of tile (1,1) [o True there], NE of (1,0)... [o False], SE of (0,0) [o True], SW of (0,1) [o False]
    # that makes the four arcs around the centre: a ring about that corner
    a, b, c, d = o[:-1, :-1], o[:-1, 1:], o[1:, :-1], o[1:, 1:]
    r1 = a & ~b & ~c & d      # arcs hug the centre corner
    r2 = ~a & b & c & ~d      # arcs face away: ring around the centre tile-block's outside... (diamond)
    return r1.sum() + r2.sum(), r1.size
tot = dict(m=[], t=[])
for s in sys.argv[1:]:
    o = np.load(f'assets/fill_o{s}.npy'); r, c = read(Image.open(f'assets/fill_hole{s}.png'))
    h = (slice(4, 12), slice(4, 12))
    out = np.ones((16, 16), bool); out[h] = False
    for name, g in (('model', r[h]), ('coin ', o[h])):
        eq_h = (g[:, 1:] == g[:, :-1]).mean(); eq_v = (g[1:] == g[:-1]).mean()
        eq_d = (g[1:, 1:] == g[:-1, :-1]).mean(); eq_a = (g[1:, :-1] == g[:-1, 1:]).mean()
        ri, n = rings(g)
        print(f'seed {s} {name} p(True) {g.mean():.2f}  agree horiz {eq_h:.2f} vert {eq_v:.2f} diag {eq_d:.2f} anti {eq_a:.2f}  rings {ri}/{n}')
    print(f'   outside match {(r == o)[out].mean():.2f}  hole match {(r == o)[~out].mean():.2f}')
