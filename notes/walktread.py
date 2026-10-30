# A bit stream as treadling in a straight 4-shaft twill: each pick steps the treadle +1 (bit 1) or -1 (bit 0).
# cell (i,j) warp up iff (i + t_j) % 4 in {0,1}. Floats: longest equal run along row/col. Usage: walktread.py OUT
import numpy as np, sys
from PIL import Image, ImageDraw
W=H=160
def ca_center(rule,n,seed=1):
    w=2*n+3; r=np.zeros(w,np.uint8); r[w//2]=1
    t=np.array([(rule>>i)&1 for i in range(8)],np.uint8); out=[]
    for _ in range(n):
        out.append(r[w//2]); r=t[np.roll(r,1)*4+r*2+np.roll(r,-1)]
    return np.array(out)
rng=np.random.default_rng(3)
streams={'rule 30 centre':ca_center(30,H),'rule 110 centre':ca_center(110,H),'coin flips':rng.integers(0,2,H),
         'rule 90 centre':ca_center(90,H),'rule 45 centre':ca_center(45,H),'alternating':np.arange(H)%2,'all ones':np.ones(H,int)}
def maxrun(a):
    best=0
    for line in a:
        d=np.flatnonzero(np.diff(line)); best=max(best,np.diff(np.r_[-1,d,len(line)-1]).max())
    return best
def cloth(bits):
    t=np.cumsum(np.where(bits==1,1,-1))
    i=np.arange(W)[None,:]; return (((i+t[:,None])%4)<2).astype(np.uint8)
names=['rule 30 centre','rule 110 centre','rule 45 centre','coin flips']
S=2;P=8;G=8
cells=[]
for n in names:
    g=cloth(streams[n]); print(n,'weft',maxrun(g),'warp',maxrun(g.T))
    cells.append(g)
for n in streams:
    g=cloth(streams[n]); print(n,'weft',maxrun(g),'warp',maxrun(g.T))

# --- picture: coin, rule 30, rule 45, Thue-Morse; floats >= 8 orange
tm=np.array([bin(i).count('1')&1 for i in range(H)])
panels=[('coin flips',streams['coin flips']),('rule 30',streams['rule 30 centre']),('rule 45',streams['rule 45 centre']),('Thue-Morse',tm)]
S=3;P=10
img=Image.new('RGB',(4*(W*S+P)+P,H*S+2*P),(245,240,230))
for k,(n,b) in enumerate(panels):
    g=cloth(b); rgb=np.where(g[...,None]==1,np.array([30,40,70]),np.array([235,225,205])).astype(np.uint8)
    for c in range(W):
        col=g[:,c]; d=np.flatnonzero(np.diff(col)); st=np.r_[0,d+1]; en=np.r_[d,H-1]
        for a,e in zip(st,en):
            if e-a+1>=8: rgb[a:e+1,c]=(230,120,20) if col[a]==1 else (245,190,120)
    im=Image.fromarray(rgb).resize((W*S,H*S),Image.NEAREST)
    img.paste(im,(P+k*(W*S+P),P)); print(n,'warp float',maxrun(g.T))
img.save('assets/walktread.png'); img.convert('RGB').resize((img.width*3//4,img.height*3//4)).save('assets/walktread.jpg',quality=70)
