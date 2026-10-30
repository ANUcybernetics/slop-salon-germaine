# usage: foldcount.py IMG  -- correlation of image with its rotations about centre, per fold k
import sys, numpy as np
from PIL import Image
im = Image.open(sys.argv[1]).convert('L').resize((512,512))
a = np.asarray(im, float); a -= a.mean()
for k in (2,3,4,5,6,7,8,9,10,11,12,13,14,16):
    b = np.asarray(im.rotate(360/k, resample=Image.BILINEAR), float); b -= b.mean()
    print(k, round((a*b).sum()/np.sqrt((a*a).sum()*(b*b).sum()),3))
