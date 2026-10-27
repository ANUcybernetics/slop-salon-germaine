# Do divergence spots depend on the noise seed? usage: python notes/seedmaps.py OUT EXACT.npy N1.npy N2.npy ...
import numpy as np, sys
from scipy.ndimage import gaussian_filter
from scipy.stats import spearmanr
from PIL import Image
A=np.load(sys.argv[2]); Bs=[np.load(f) for f in sys.argv[3:]]
ds=[gaussian_filter(np.abs(A-B),6) for B in Bs]
N=A.shape[0]; yy,xx=np.mgrid[:N,:N]; r=np.hypot(yy-N//2,xx-N//2); m=r<150
for i in range(len(ds)):
    print('mass r<40 %.2f'%(ds[i][r<40].sum()/ds[i].sum()), end='  ')
print()
for i in range(len(ds)):
    for j in range(i+1,len(ds)):
        print(i,j,'rho %.2f'%spearmanr(ds[i][m],ds[j][m])[0])
# D4-folded: is the pattern of divergence one 8-image orbit?
row=np.concatenate([np.clip(d/np.percentile(d,99.5),0,1) for d in ds],1)
Image.fromarray((row*255).astype(np.uint8)).resize((row.shape[1]*2,row.shape[0]*2)).save(sys.argv[1])
