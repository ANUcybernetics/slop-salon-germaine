# beads.py IMG OUT.png : bead radii via distance transform; rank-size loglog
import sys, numpy as np
from PIL import Image
from scipy import ndimage as ndi
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
def radii(path, size=1024):
    im = Image.open(path).convert('RGB').resize((size, size))
    a = np.asarray(im).astype(float)
    mx, mn = a.max(2), a.min(2)
    sat = (mx - mn) / (mx + 1e-9)
    # bead = light and unsaturated, but background is also cream: restrict to the disk
    yy, xx = np.mgrid[:size, :size]
    disk = (xx - size/2)**2 + (yy - size/2)**2 < (0.485*size)**2
    # edges: beads are bounded by darker thin outlines or red; use gradient to cut
    g = ndi.gaussian_gradient_magnitude(a.mean(2), 1.0)
    mask = disk & (sat < 0.25) & (mx > 200) & (g < 6)
    d = ndi.distance_transform_edt(mask)
    mxf = ndi.maximum_filter(d, size=5)
    pk = (d == mxf) & (d >= 3)
    ys, xs = np.nonzero(pk)
    order = np.argsort(-d[ys, xs])
    kept = []
    for i in order:
        y, x, r = ys[i], xs[i], d[ys[i], xs[i]]
        if all((y-ky)**2 + (x-kx)**2 > (0.8*max(r, kr))**2 for ky, kx, kr in kept):
            kept.append((y, x, r))
    return np.array([k[2] for k in kept]), kept
if __name__ == '__main__':
    r, kept = radii(sys.argv[1])
    r = np.sort(r)[::-1]
    print(len(r), r[:8])
    rank = np.arange(1, len(r)+1)
    sel = (rank >= 4) & (rank <= len(r)//1)
    s = np.polyfit(np.log(rank[sel]), np.log(r[sel]), 1)
    print('slope', s[0])
    fig, ax = plt.subplots(1, 2, figsize=(10, 5))
    ax[0].loglog(rank, r, '.'); ax[0].set_title('rank-size slope %.2f' % s[0])
    im = Image.open(sys.argv[1]).convert('RGB').resize((1024, 1024))
    ax[1].imshow(im)
    for y, x, rr in kept:
        ax[1].add_patch(plt.Circle((x, y), rr, fill=False, ec='b', lw=0.4))
    ax[1].axis('off'); plt.savefig(sys.argv[2], dpi=130)
