# usage: polar.py IMG CROPFRAC R1 R2 ...  -- angular FFT of intensity at radii (px of 512 resize of crop)
import sys, numpy as np
from PIL import Image
from scipy.ndimage import map_coordinates
im = Image.open(sys.argv[1]).convert('L'); w,h = im.size
f = float(sys.argv[2]); s=min(w,h)*f
im = im.crop((int((w-s)/2),int((h-s)/2),int((w+s)/2),int((h+s)/2))).resize((512,512))
a = np.asarray(im,float); c=255.5
th = np.linspace(0,2*np.pi,720,endpoint=False)
for r in map(float, sys.argv[3:]):
    v = map_coordinates(a,[c+r*np.sin(th),c+r*np.cos(th)],order=1); v-=v.mean()
    F = np.abs(np.fft.rfft(v))[1:33]
    top = np.argsort(F)[::-1][:3]+1
    print(r, 'peaks', [(int(k), round(F[k-1]/F.sum(),2)) for k in top])
