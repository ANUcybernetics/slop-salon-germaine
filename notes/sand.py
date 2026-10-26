# BTW sandpile, open boundary. usage: python notes/sand.py N DROPS SEED  -> assets/sand_cfg.png, sand_big.png, prints rank-size slope
import numpy as np, sys
from PIL import Image
N, D, seed = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
rng = np.random.default_rng(seed)
z = rng.integers(0, 4, (N, N)).astype(np.int32)
def relax(z, track=False):
    cnt = np.zeros_like(z) if track else None
    tot = 0
    while True:
        t = z >= 4
        if not t.any(): return tot, cnt
        k = (z // 4) * t
        z -= 4*k
        z[1:] += k[:-1]; z[:-1] += k[1:]; z[:, 1:] += k[:, :-1]; z[:, :-1] += k[:, 1:]
        tot += int(k.sum())
        if track: cnt += k
sizes = []; best = (0, None); warm = 0
for _ in range(40):
    z += rng.integers(0, 2, (N, N)).astype(np.int32); relax(z)
for d in range(D):
    i, j = rng.integers(0, N, 2); z[i, j] += 1
    if z[i, j] < 4: 
        if d >= warm: sizes.append(0)
        continue
    zc = z.copy() if d >= warm else None
    tot, _ = relax(z)
    if d >= warm:
        sizes.append(tot)
        if tot > best[0]: best = (tot, (zc, i, j))
s = np.array([x for x in sizes if x > 0]); print('avalanches', len(s), 'of', D, 'max', s.max())
s.sort(); s = s[::-1]
r = np.arange(1, len(s)+1); sel = (s >= 10) & (r >= 5)
print('rank-size slope (size vs rank)', np.polyfit(np.log(r[sel]), np.log(s[sel]), 1)[0])
pal = np.array([[18,18,30],[60,90,160],[230,160,60],[245,240,225]], np.uint8)
Image.fromarray(pal[np.clip(z,0,3)]).resize((N*4,N*4), Image.NEAREST).save('assets/sand_cfg.png')
zc, i, j = best[1]; zc = zc.copy(); zc[i, j] += 1
tot, cnt = relax(zc, True)
c = np.log1p(cnt) / np.log1p(cnt.max())
img = (np.stack([c*255, c**2*200, (1-c)*80*(cnt>0)], -1)).astype(np.uint8)
Image.fromarray(img).resize((N*4,N*4), Image.NEAREST).save('assets/sand_big.png')
