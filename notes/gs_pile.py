# Gray-Scott seeded by sandpile heights. usage: python notes/gs_pile.py N G F K STEPS OUT
import numpy as np, sys
from PIL import Image
N,G,F,K,S=int(sys.argv[1]),int(sys.argv[2]),float(sys.argv[3]),float(sys.argv[4]),int(sys.argv[5]); out=sys.argv[6]
z=np.zeros((N,N),np.int64); z[N//2,N//2]=G
while True:
    k=z//4
    if not k.any(): break
    z-=4*k; z[1:]+=k[:-1]; z[:-1]+=k[1:]; z[:,1:]+=k[:,:-1]; z[:,:-1]+=k[:,1:]
U=np.ones((N,N)); V=np.zeros((N,N))
V[z==3]=0.5; U[z==3]=0.5
lap=lambda a: np.roll(a,1,0)+np.roll(a,-1,0)+np.roll(a,1,1)+np.roll(a,-1,1)-4*a
for t in range(S):
    uvv=U*V*V
    U+=0.16*lap(U)-uvv+F*(1-U)
    V+=0.08*lap(V)+uvv-(F+K)*V
v=np.clip(V/V.max(),0,1)
pal=np.array([[8,6,20],[70,30,110],[230,90,80],[255,235,170]],float)
x=v*3; i=np.minimum(x.astype(int),2); f=(x-i)[...,None]
img=(pal[i]*(1-f)+pal[i+1]*f).astype(np.uint8)
Image.fromarray(img).resize((N*2,N*2),Image.LANCZOS).save(out)
print('V max',V.max(),'mean',V.mean())
