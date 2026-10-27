# Three panels: dish; power-iteration mode from perturbation seed 1; mode from seed 2 (signed, blue/red). usage: python notes/lyapfig.py OUT
import numpy as np, sys
from PIL import Image
ref=np.load('assets/lyap1_ref.npy'); ms=[np.load('assets/lyap%d.npy'%s) for s in (1,2)]
pal=np.array([[8,6,20],[70,30,110],[230,90,80],[255,235,170]],float)
v=np.clip(ref/ref.max(),0,1); x=v*3; i=np.minimum(x.astype(int),2); f=(x-i)[...,None]
base=(pal[i]*(1-f)+pal[i+1]*f)
def sg(m):
    a=np.clip(m/np.percentile(np.abs(m),99.7),-1,1)[...,None]
    pos=np.array([255,120,60.]); neg=np.array([70,200,255.])
    c=np.where(a>0,pos,neg); w=np.abs(a)**0.6
    return base*0.25*(1-w)+c*w
row=np.concatenate([base,sg(ms[0]),sg(ms[1])],1).clip(0,255).astype(np.uint8)
Image.fromarray(row).resize((row.shape[1]*2//1,row.shape[0]*2//1),Image.LANCZOS).save(sys.argv[1])
