# Walk threading AND treadling: ends step +-1 by bit stream a, picks by stream b; cell up iff (s_i+t_j)%4<2. Usage: walkboth.py OUT
import numpy as np, sys
from PIL import Image
N=160
def ca_center(rule,n):
    w=2*n+3; r=np.zeros(w,np.uint8); r[w//2]=1
    t=np.array([(rule>>i)&1 for i in range(8)],np.uint8); out=[]
    for _ in range(n):
        out.append(r[w//2]); r=t[np.roll(r,1)*4+r*2+np.roll(r,-1)]
    return np.array(out)
rng=np.random.default_rng(5)
tm=np.array([bin(i).count('1')&1 for i in range(N)])
walk=lambda b:np.cumsum(np.where(b==1,1,-1))
def cloth(a,b):
    return (((walk(a)[None,:]+walk(b)[:,None])%4)<2).astype(np.uint8)
def runs(g):
    out=[]
    for line in g:
        d=np.flatnonzero(np.diff(line)); out.append(np.diff(np.r_[-1,d,len(line)-1]).max())
    return max(out)
panels=[('coin x coin',rng.integers(0,2,N),rng.integers(0,2,N)),
        ('rule 30 x rule 45',ca_center(30,N),ca_center(45,N)),
        ('Thue-Morse x coin',tm,rng.integers(0,2,N)),
        ('Thue-Morse x Thue-Morse',tm,tm)]
S=3;P=10
img=Image.new('RGB',(4*(N*S+P)+P,N*S+2*P),(245,240,230))
for k,(n,a,b) in enumerate(panels):
    g=cloth(a,b); print(n,'weft',runs(g),'warp',runs(g.T))
    rgb=np.where(g[...,None]==1,np.array([30,40,70]),np.array([235,225,205])).astype(np.uint8)
    for ax in (0,1):
        G=g if ax==1 else g.T; R=rgb if ax==1 else rgb.transpose(1,0,2)
        for r in range(N):
            line=G[r]; d=np.flatnonzero(np.diff(line)); st=np.r_[0,d+1]; en=np.r_[d,N-1]
            for s,e in zip(st,en):
                if e-s+1>=8: R[r,s:e+1]=(230,120,20) if line[s]==1 else (245,190,120)
    img.paste(Image.fromarray(rgb).resize((N*S,N*S),Image.NEAREST),(P+k*(N*S+P),P))
img.save('assets/walkboth.png'); img.resize((img.width*3//4,img.height*3//4)).convert('RGB').save('assets/walkboth.jpg',quality=70)
