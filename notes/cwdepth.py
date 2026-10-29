import numpy as np, sys
from PIL import Image
# depth of (a,b) in the Calkin-Wilf tree = sum of continued-fraction quotients of a/b; vectorised Euclid
R=int(sys.argv[1]); S=int(sys.argv[2]); out=sys.argv[3]
a,b=np.meshgrid(np.arange(1,R+1),np.arange(1,R+1))
x=a.copy(); y=b.copy(); d=np.zeros_like(x)
for _ in range(R+2):
    live=y>0
    if not live.any(): break
    q=np.where(live,x//np.where(live,y,1),0)
    d+=q
    x,y=np.where(live,y,x),np.where(live,x-q*y,y)
g=x
cop=(g==1)
d=d-1  # root (1,1) has depth 0
v=np.zeros(d.shape); v[cop]=np.log2(d[cop]+1)
v/=v.max()
import matplotlib; matplotlib.use('Agg')
from matplotlib import cm
rgb=(matplotlib.colormaps['magma'](v)[...,:3]*255).astype(np.uint8)
rgb[~cop]=(10,10,14)
Image.fromarray(rgb[::-1]).resize((S,S),Image.NEAREST).save(out)
print(cop.sum(), d[cop].max(), "min depth>1 median", np.median(d[cop]))
