# single-source abelian sandpile: G grains at centre of NxN, relax. usage: python notes/pile.py N G OUT
import numpy as np, sys
from PIL import Image
N, G, out = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
z = np.zeros((N, N), np.int64); z[N//2, N//2] = G
while True:
    k = z // 4
    if not k.any(): break
    z -= 4*k
    z[1:] += k[:-1]; z[:-1] += k[1:]; z[:, 1:] += k[:, :-1]; z[:, :-1] += k[:, 1:]
print('max height', z.max(), 'edge touched', z[0].any() or z[:, 0].any())
pal = np.array([[14,10,28],[120,40,110],[240,110,70],[250,225,150]], np.uint8)
Image.fromarray(pal[z]).resize((N*3, N*3), Image.NEAREST).save(out)
