# does the share of each lattice point (do, de=round(L*do)) depend only on its residual r? across d. plus corrected residual width
import numpy as np
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
s=np.load('/tmp/steps.npy').astype(np.int64); o=np.load('/tmp/odds.npy').astype(np.int64)
e=s-o; L=np.log2(3); N=len(s)-1
fig,ax=plt.subplots(1,2,figsize=(11,4.6),dpi=150)
cols={0:'#1b6ca8',6:'#d9822b',12:'#2a9d6f'}
for k in (0,6,12):
    d=1<<k; n=np.arange(1<<10,N-d+1)
    de=e[n+d]-e[n]; do=o[n+d]-o[n]
    r=de-L*do; rc=r-np.log2((n+d)/n)
    print(k,'sd r',r.std(),'sd corrected',rc.std(),'median |rc|',np.median(abs(rc)))
    nz=~((do==0)&(de==0)); v=np.arange(1,60)
    x=[];y=[]
    for u in v:
        sel=(np.abs(do)==u)
        if sel.sum()<50: continue
        x.append(np.mean(np.sign(do[sel])*(de[sel]-L*do[sel]))); y.append(sel.sum()/nz.sum())
    x=np.array(x);y=np.array(y)
    ax[0].scatter(np.abs(x),y,s=14,c=cols[k],label=f'd = 2^{k}')
    ax[1].hist(r[nz],bins=np.linspace(-.6,.6,121),histtype='step',color=cols[k],density=True,label=f'd = 2^{k}')
ax[0].set_yscale('log'); ax[0].set_xlabel('|r| of lattice point (de - log2(3) do)'); ax[0].set_ylabel('share of differing pairs'); ax[0].legend()
ax[1].set_xlabel('r = de - log2(3)*do'); ax[1].set_ylabel('density'); ax[1].legend()
plt.tight_layout(); plt.savefig('assets/dscan.png')
