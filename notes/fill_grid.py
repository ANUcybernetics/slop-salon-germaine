# does ink cross tile edges only at edge midpoints? share of ink on edge lines within +-8px of a midpoint. usage: python notes/fill_grid.py IMG
import numpy as np, sys
from PIL import Image
N, T = 16, 64
a = 1 - np.asarray(Image.open(sys.argv[1]).convert('L').resize((N*T, N*T)), float) / 255
# left half: vertical edges k=1..7, right half k=9..15; horizontal edges use only columns of that half
def half(reg, off=0):
    c0, c1, r0, r1 = reg; tot = near = 0
    for k in range(c0 + 1, c1):                              # interior vertical edges: ink vs y
        line = a[r0*T:r1*T, k*T + off]; m = np.abs(np.arange(r0*T, r1*T) % T - T//2) <= 8
        tot += line.sum(); near += line[m].sum()
    for k in range(r0 + 1, r1):                              # interior horizontal edges
        line = a[k*T + off, c0*T:c1*T]; m = np.abs(np.arange(c0*T, c1*T) % T - T//2) <= 8
        tot += line.sum(); near += line[m].sum()
    return near / tot
base = 17 / 64   # share if ink were uniform: width of window / T
print('uniform would be', round(base, 2))
REG = {'left (true)': (0, 8, 0, 16), 'right (model)': (8, 16, 0, 16), 'hole (model)': (5, 10, 5, 10), 'ring (true)': (0, 4, 0, 4)}
for name, reg in REG.items():
    print(f'{name:14s} on edges {half(reg):.2f}   control, lines shifted T/4: {half(reg, T//4):.2f}')
