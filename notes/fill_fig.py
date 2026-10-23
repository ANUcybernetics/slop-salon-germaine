# two fills side by side: half masked (lattice lost) and 8x8 hole (lattice kept). usage: python notes/fill_fig.py HOLE_SEED
import sys
from PIL import Image, ImageDraw
s = sys.argv[1]
a = Image.open('assets/fill_out1.png').convert('RGB'); b = Image.open(f'assets/fill_hole{s}.png').convert('RGB')
d = ImageDraw.Draw(a); d.rectangle([512, 0, 1023, 1023], outline=(230, 110, 20), width=6)
d = ImageDraw.Draw(b); d.rectangle([256, 256, 767, 767], outline=(230, 110, 20), width=6)
W = 700; out = Image.new('RGB', (2*W + 30, W), 'white')
out.paste(a.resize((W, W)), (0, 0)); out.paste(b.resize((W, W)), (W + 30, 0))
out.save('assets/fill_fig.png'); out.convert('RGB').save('assets/fill_fig.jpg', quality=75)
