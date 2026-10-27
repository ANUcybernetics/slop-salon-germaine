# Break the pile's eightfold symmetry with noise eps on V. usage: python notes/gs_break.py N G F K STEPS EPS SEED OUT
import numpy as np, sys
from PIL import Image
N,G,F,K,S=int(sys.argv[1]),int(sys.argv[2]),float(sys.argv[3]),float(sys.argv[4]),int(sys.argv[5])
eps=float(sys.argv[6]); seed=int(sys.argv[7]); out=sys.argv[8]
z=np.zeros((N,N),np.int64); z[N//2,N//2]=G
while True:
    k=z//4
    if not k.any(): break
    z-=4*k; z[1:]+=k[:-1]; z[:-1]+=k[1:]; z[:,1:]+=k[:,:-1]; z[:,:-1]+=k[:,1:]
U=np.ones((N,N)); V=np.zeros((N,N))
V[z==3]=0.5; U[z==3]=0.5
V+=eps*np.random.default_rng(seed).random((N,N))
lap=lambda a: np.roll(a,1,0)+np.roll(a,-1,0)+np.roll(a,1,1)+np.roll(a,-1,1)-4*a
def defect(V):
    # symmetry defect around the pile centre (N//2): fold with d4 images, crop to odd box
    A=V
    ims=[A,A.T,A[::-1],A[:,::-1],A[::-1,::-1],A.T[::-1],A.T[:,::-1],A.T[::-1,::-1]]
    return np.std(np.stack(ims),0)
snaps={}
for t in range(S+1):
    if t in (0,250,500,1000,1500,2000,3000,4500,6000):
        d=defect(V); snaps[t]=d; print(t,'defect mean %.4f max %.4f  V max %.3f'%(d.mean(),d.max(),V.max()),flush=True)
    uvv=U*V*V
    U+=0.16*lap(U)-uvv+F*(1-U)
    V+=0.08*lap(V)+uvv-(F+K)*V
np.save(out+'.npy',V)
v=np.clip(V/V.max(),0,1)
pal=np.array([[8,6,20],[70,30,110],[230,90,80],[255,235,170]],float)
x=v*3; i=np.minimum(x.astype(int),2); f=(x-i)[...,None]
img=(pal[i]*(1-f)+pal[i+1]*f).astype(np.uint8)
Image.fromarray(img).resize((N*2,N*2),Image.LANCZOS).save(out)
