# distribution of |do| (odd-count difference) for n vs n+d, with the lattice residual of each
import numpy as np
s=np.load('/tmp/steps.npy').astype(np.int64); o=np.load('/tmp/odds.npy').astype(np.int64)
e=s-o; L=np.log2(3); N=len(s)-1
for k in (0,6,12):
    d=1<<k; n=np.arange(1<<10,N-d+1)
    de=e[n+d]-e[n]; do=o[n+d]-o[n]
    m=do>0
    print(f"d=2^{k}  do>0 share {m.mean():.2f}  (sign do<0: {(do<0).mean():.2f}, 0: {(do==0).mean():.2f})")
    for v in range(1,30):
        sel=do==v
        if sel.sum()==0: continue
        print(f"  do={v:2d} share {sel.mean()*100:5.2f}%  mean de {de[sel].mean():6.2f}  r={np.mean(de[sel]-L*v):+.3f}  de modes {np.bincount(de[sel]-de[sel].min()).argmax()+de[sel].min()}")
