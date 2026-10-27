# Compare power-iteration modes with each other and with the seed-shaken sites map. usage: python notes/lyapcmp.py
import numpy as np
from scipy.ndimage import gaussian_filter
from scipy.stats import spearmanr
m1=np.load('assets/lyap1.npy'); m2=np.load('assets/lyap2.npy'); ref=np.load('assets/lyap1_ref.npy')
a1=gaussian_filter(np.abs(m1),5); a2=gaussian_filter(np.abs(m2),5)
print('mode overlap (signed) %.3f  abs-smooth rho %.3f'%(abs((m1*m2).sum()), spearmanr(a1.ravel(),a2.ravel())[0]))
ds=[gaussian_filter(np.abs(ref-np.load('assets/seed%d.png.npy'%s)),5) for s in (2,3,4)]
mn=np.min(ds,0)
for nm,a in (('mode1',a1),('mode2',a2)):
    print(nm,'vs sites map rho %.3f'%spearmanr(a.ravel(),mn.ravel())[0])
N=401; y,x=np.mgrid[:N,:N]; r=np.hypot(y-200,x-200)
for lo,hi in ((0,40),(40,100),(100,170),(170,300)):
    s=(r>=lo)&(r<hi); print(lo,hi,'mass mode1 %.2f mode2 %.2f sites %.2f'%((m1[s]**2).sum(),(m2[s]**2).sum(),(mn[s]**2).sum()/(mn**2).sum()))
