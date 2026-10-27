# Does divergence sit where stripe orientation is incoherent? usage: python notes/coherence.py EXACT.npy NOISED.npy OUT
import numpy as np, sys
from scipy.ndimage import gaussian_filter, uniform_filter
from scipy.stats import spearmanr
from PIL import Image
A=np.load(sys.argv[1]); B=np.load(sys.argv[2]); out=sys.argv[3]
d=np.abs(A-B)
gy,gx=np.gradient(gaussian_filter(A,1.0))
res={}
for s in (4,8,16):
    jxx=gaussian_filter(gx*gx,s); jyy=gaussian_filter(gy*gy,s); jxy=gaussian_filter(gx*gy,s)
    coh=np.sqrt((jxx-jyy)**2+4*jxy**2)/(jxx+jyy+1e-12)
    dl=gaussian_filter(d,s)
    N=A.shape[0]; c=N//2; yy,xx=np.mgrid[:N,:N]; r=np.hypot(yy-c,xx-c)
    m=(A.max()*0+1)*(r<150)
    rho=spearmanr(coh[m>0],dl[m>0])[0]
    # partial: within radius bins
    ps=[]
    for lo in range(0,150,30):
        k=(r>=lo)&(r<lo+30); ps.append(spearmanr(coh[k],dl[k])[0])
    print('sigma',s,'rho(coh,|dV| smoothed)=%.3f'%rho,'by radius bin',np.round(ps,2))
    res[s]=(coh,dl)
coh,dl=res[8]
def norm(a): return np.clip((a-a.min())/(np.percentile(a,99.5)-a.min()),0,1)
row=np.concatenate([norm(A),1-coh/ coh.max(),norm(dl)],1)
Image.fromarray((row*255).astype(np.uint8)).resize((row.shape[1]*2,row.shape[0]*2)).save(out)
