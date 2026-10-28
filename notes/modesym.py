# D4 irrep content of the converged mode, and a picture of the centre. usage: python notes/modesym.py IN.npz OUT.png
import numpy as np, sys
from PIL import Image
D=np.load(sys.argv[1]); N=D['V'].shape[0]; c=N//2
def ops(a):
    a=a[1:,1:] if False else a
    out=[]
    for k in range(4):
        r=np.rot90(a,k); out+= [r, r.T]
    return out
# group action about centre pixel c: rot90 and transpose are symmetric about the centre for odd N
for name in ('dV','dU','V'):
    a=D[name]; e=(a**2).sum(); 
    ims=ops(a)
    # characters: rotations (k) and reflections (transpose composed)
    rot=[np.rot90(a,k) for k in range(4)]; ref=[np.rot90(a.T,k) for k in range(4)]
    # irreps A1: all +1; A2: rot +1 ref -1; B1: rot90 -1, refs (axis) +1 ...; project by averaging
    chars={'A1':([1,1,1,1],[1,1,1,1]),'A2':([1,1,1,1],[-1]*4),'B1':([1,-1,1,-1],[1,-1,1,-1]),'B2':([1,-1,1,-1],[-1,1,-1,1])}
    s={}
    for k,(cr,cf) in chars.items():
        p=sum(cr[i]*rot[i]+cf[i]*ref[i] for i in range(4))/8; s[k]=(p**2).sum()/e
    p=(a-sum(rot)/4); s['E(rest)']=1-sum(s.values())
    print(name,{k:round(v,3) for k,v in s.items()})
h=24
def pan(a):
    b=a[c-h:c+h+1,c-h:c+h+1]; m=np.abs(b).max(); return ((b/m*0.5+0.5)*255).astype(np.uint8)
def panv(a):
    b=a[c-h:c+h+1,c-h:c+h+1]; return ((b-b.min())/(b.max()-b.min())*255).astype(np.uint8)
row=np.concatenate([panv(D['V']),pan(D['dV']),pan(D['dU'])],1)
Image.fromarray(row).resize((row.shape[1]*8,row.shape[0]*8),Image.NEAREST).save(sys.argv[2])
