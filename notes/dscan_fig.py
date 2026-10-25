# share of differing (n, n+d) pairs per odd-count difference, vs its lattice residual |r|; d = 1, 64, 4096 overlay
import numpy as np
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
s=np.load('/tmp/steps.npy').astype(np.int64); o=np.load('/tmp/odds.npy').astype(np.int64)
e=s-o; L=np.log2(3); N=len(s)-1
fig,ax=plt.subplots(figsize=(7,5),dpi=150)
for k,c,m in ((0,'#1b6ca8','o'),(6,'#d9822b','s'),(12,'#2a9d6f','^')):
    d=1<<k; n=np.arange(1<<10,N-d+1)
    de=e[n+d]-e[n]; do=o[n+d]-o[n]; nz=~((do==0)&(de==0))
    x=[];y=[];lab=[]
    for u in range(1,60):
        sel=np.abs(do)==u
        if sel.sum()<50: continue
        x.append(abs(np.mean(np.sign(do[sel])*(de[sel]-L*do[sel])))); y.append(sel.sum()/nz.sum()); lab.append(u)
    ax.scatter(x,y,s=26,c=c,marker=m,alpha=.8,label=f'n vs n+{d}')
    if k==0:
        for xi,yi,l in zip(x,y,lab):
            if yi>0.02: ax.annotate(str(l),(xi,yi),textcoords='offset points',xytext=(5,4),fontsize=9)
ax.set_yscale('log'); ax.set_xlabel('how far the odd-step difference sits off the line: |evens - 1.585 x odds|')
ax.set_ylabel('share of pairs that differ'); ax.legend(); ax.set_ylim(1e-4,0.15)
plt.tight_layout(); plt.savefig('assets/dscan_fig.png')
