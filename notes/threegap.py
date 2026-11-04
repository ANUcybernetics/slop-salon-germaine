import sys, numpy as np
from PIL import Image
# usage: threegap.py OUT ROWS  -- panels for phi, sqrt2, pi (mod 1)
out=sys.argv[1]; R=int(sys.argv[2]); W=480
alphas=[("phi",(5**.5-1)/2),("sqrt2",2**.5-1),("pi",np.pi-3)]
pal=[(250,200,60),(40,90,160),(210,60,60),(30,30,30)]
panels=[]
nclass=[]
for name,a in alphas:
    img=np.zeros((R*2,W,3),np.uint8); img[:]=(14,14,18)
    cnt=[]
    for N in range(2,R+2):
        p=np.sort((np.arange(N)*a)%1.0)
        g=np.diff(np.append(p,p[0]+1))
        # classes by rounding
        key=np.round(g,9); u=np.unique(key); cnt.append(len(u))
        order=np.argsort(u)
        cls={v:i for i,v in enumerate(u)}
        x=(p*W).astype(int); x2=(np.append(p[1:],p[0]+1)*W).astype(int)
        y=(N-2)*2
        for xi,xj,k in zip(x,x2,key):
            c=pal[min(cls[k],3)]
            xi=min(xi,W-1); xj=min(max(xj,xi+1),W)
            img[y:y+2,xi:xj-1 if xj-xi>2 else xj]=c
            if xj<=W and xj-xi>2: img[y:y+2,xj-1]=(14,14,18)
    nclass.append(max(cnt)); panels.append(img)
sep=np.zeros((R*2,10,3),np.uint8)
im=np.concatenate([panels[0],sep,panels[1],sep,panels[2]],1)
Image.fromarray(im).save(out)
print(nclass)
