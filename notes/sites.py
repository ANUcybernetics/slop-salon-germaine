# Sites that diverge under every seed: dish with min-over-seeds |dV| laid on it. usage: python notes/sites.py OUT EXACT.npy N1.npy ...
import numpy as np, sys
from scipy.ndimage import gaussian_filter
from PIL import Image
A=np.load(sys.argv[2]); Bs=[np.load(f) for f in sys.argv[3:]]
ds=np.stack([gaussian_filter(np.abs(A-B),5) for B in Bs])
mn=ds.min(0); mn=np.clip(mn/np.percentile(mn,99.7),0,1)
v=np.clip(A/A.max(),0,1)
pal=np.array([[8,6,20],[70,30,110],[230,90,80],[255,235,170]],float)
x=v*3; i=np.minimum(x.astype(int),2); f=(x-i)[...,None]
base=(pal[i]*(1-f)+pal[i+1]*f)
dim=base*0.35
glow=np.array([90,230,255],float)
w=(mn**0.7)[...,None]
over=dim*(1-w)+ (base*0.5+glow*0.9)*w
row=np.concatenate([base,over],1).clip(0,255).astype(np.uint8)
Image.fromarray(row).resize((row.shape[1]*2,row.shape[0]*2),Image.LANCZOS).save(sys.argv[1])
