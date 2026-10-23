# render a coin Truchet page with the right half masked, for an inpainting model. usage: python notes/fill.py make | read FILE
import numpy as np, sys
from PIL import Image, ImageDraw
N, T = 16, 64
def render(o, w=12):
    im = Image.new('L', (N*T, N*T), 255); d = ImageDraw.Draw(im)
    for y in range(N):
        for x in range(N):
            x0, y0 = x*T, y*T
            cs = [(x0, y0, 0, 90), (x0+T, y0+T, 180, 270)] if o[y, x] else [(x0+T, y0, 90, 180), (x0, y0+T, 270, 360)]
            for cx, cy, a0, a1 in cs:
                d.arc([cx-T//2, cy-T//2, cx+T//2, cy+T//2], a0, a1, fill=0, width=w)
    return im
def read(im):
    a = np.asarray(im.convert('L').resize((N*T, N*T)), float) / 255
    o = np.zeros((N, N), bool); conf = np.zeros((N, N))
    r = T // 4
    for y in range(N):
        for x in range(N):
            x0, y0 = x*T, y*T
            def ink(cx, cy):  # mean darkness on the arc about that corner, sampled on a quarter circle inside the tile
                s = 0
                for th in np.linspace(0, np.pi/2, 12):
                    dx = np.cos(th) * T/2; dy = np.sin(th) * T/2
                    px = cx + (dx if cx == x0 else -dx); py = cy + (dy if cy == y0 else -dy)
                    s += 1 - a[int(min(py, N*T-1)), int(min(px, N*T-1))]
                return s / 12
            nwse = ink(x0, y0) + ink(x0+T, y0+T); nesw = ink(x0+T, y0) + ink(x0, y0+T)
            o[y, x] = nwse > nesw; conf[y, x] = abs(nwse - nesw)
    return o, conf
if __name__ == '__main__':
    if sys.argv[1] == 'make':
        seed = int(sys.argv[3]) if len(sys.argv) > 3 else 5
        o = np.random.default_rng(seed).random((N, N)) < .5
        np.save(f'assets/fill_o{seed}.npy' if seed != 5 else 'assets/fill_o.npy', o)
        im = render(o); im.save('assets/fill_full.png')
        m = Image.new('L', (N*T, N*T), 0)
        if len(sys.argv) > 2: ImageDraw.Draw(m).rectangle([4*T, 4*T, 12*T-1, 12*T-1], fill=255) if seed != 5 else ImageDraw.Draw(m).rectangle([5*T, 5*T, 10*T-1, 10*T-1], fill=255); tag = f'_hole{seed}' if seed != 5 else '_hole'
        else: ImageDraw.Draw(m).rectangle([N*T//2, 0, N*T, N*T], fill=255); tag = ''
        m.save(f'assets/fill_mask{tag}.png'); im2 = im.copy(); im2.paste(255, (0, 0), m); im2.save(f'assets/fill_in{tag}.png')
    else:
        o, c = read(Image.open(sys.argv[2])); print(o.astype(int)); print(np.round(c.mean(), 2))
