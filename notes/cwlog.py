import numpy as np, sys
from PIL import Image
import matplotlib; matplotlib.use('Agg')
# coprime pairs (a,b), max(a,b)=M row, column = log2(b/a); colour = log2 CF-quotient sum
M=int(sys.argv[1]); W=int(sys.argv[2]); out=sys.argv[3]
img=np.zeros((M,W)); cnt=np.zeros((M,W))
for m in range(1,M+1):
    o=np.arange(1,m+1)
    # pairs (m,o) and (o,m)
    for a,b in ((np.full_like(o,m),o),(o,np.full_like(o,m))):
        x=a.copy(); y=b.copy(); d=np.zeros_like(x)
        while (y>0).any():
            live=y>0; q=np.where(live,x//np.where(live,y,1),0); d+=q
            x,y=np.where(live,y,x),np.where(live,x-q*y,y)
        cop=x==1
        r=np.log2(b[cop]/a[cop]); col=((r+np.log2(M))/(2*np.log2(M))*(W-1)).astype(int)
        np.add.at(img[m-1],col,np.log2(d[cop]))
        np.add.at(cnt[m-1],col,1)
v=np.where(cnt>0,img/np.maximum(cnt,1),np.nan)
v=(v-np.nanmin(v))/(np.nanmax(v)-np.nanmin(v))
rgb=(matplotlib.colormaps['magma'](np.nan_to_num(v))[...,:3]*255).astype(np.uint8)
rgb[np.isnan(v)]=(10,10,14)
Image.fromarray(rgb[::-1]).save(out)
