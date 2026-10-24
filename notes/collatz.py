# Collatz turtle: walk each n's trajectory backwards from 1 (so all share the root);
# even step -> turn +a, odd step -> turn -b. Draw with PIL, alpha-accumulated.
import math, sys
from PIL import Image, ImageDraw
N=int(sys.argv[1]) if len(sys.argv)>1 else 30000
A=float(sys.argv[2]) if len(sys.argv)>2 else 8.0
B=float(sys.argv[3]) if len(sys.argv)>3 else 16.0
OUT=sys.argv[4] if len(sys.argv)>4 else 'assets/collatz.png'
W=1600
cache={}
def path(n):
    p=[n]
    while n!=1:
        n = n//2 if n%2==0 else 3*n+1
        p.append(n)
    return p[::-1]  # from 1 up to n
layer=Image.new('L',(W,W),0)
d=ImageDraw.Draw(layer)
segs=[]
seen=set()
for n in range(2,N):
    p=path(n)
    x=y=0.0;h=math.pi/2
    pts=[(x,y)]
    for k in range(1,len(p)):
        h += math.radians(A) if p[k]%2==0 else -math.radians(B)
        x+=math.cos(h);y+=math.sin(h)
        pts.append((x,y))
    segs.append(pts)
xs=[q[0] for s in segs for q in s];ys=[q[1] for s in segs for q in s]
x0,x1,y0,y1=min(xs),max(xs),min(ys),max(ys)
sc=(W-80)/max(x1-x0,y1-y0)
import numpy as np
acc=np.zeros((W,W),dtype=np.float32)
for pts in segs:
    layer=Image.new('L',(W,W),0);d=ImageDraw.Draw(layer)
    d.line([(40+(a-x0)*sc, W-40-(b-y0)*sc) for a,b in pts],fill=255,width=2)
    acc+=np.asarray(layer,dtype=np.float32)/255
acc=np.log1p(acc)/np.log1p(acc.max())
img=np.zeros((W,W,3),dtype=np.uint8)
img[...,0]=(20+200*acc**0.55); img[...,1]=(18+170*acc**0.8); img[...,2]=(28+120*acc**1.2)
Image.fromarray(img).save(OUT)
print(OUT,len(segs),sc)
