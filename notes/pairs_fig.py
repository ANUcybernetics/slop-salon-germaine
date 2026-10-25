# figure: n vs n+512, how much the odd-step count differs (needs /tmp/steps.npy, /tmp/odds.npy from pairs.py)
import numpy as np, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
s=np.load('/tmp/steps.npy');a=np.load('/tmp/odds.npy');b=s-a
n=np.arange(1000,len(s)-1-4096); d=512
da=a[n+d]-a[n]; db=b[n+d]-b[n]
L=np.log2(3); dev=da*L-db
fig,ax=plt.subplots(1,2,figsize=(12,4.6),dpi=130,facecolor='#f4efe6')
for x in ax: x.set_facecolor('#f4efe6')
vals,cnt=np.unique(da,return_counts=True)
frac=cnt/len(da)
ax[0].bar(vals,frac,color='#8a2f2f',width=.8)
for v in (5,12,17,24,29,36,41):
    ax[0].axvline(v,color='#222',lw=.4,ls=':'); ax[0].axvline(-v,color='#222',lw=.4,ls=':')
ax[0].set_yscale('log'); ax[0].set_xlim(-60,60); ax[0].set_ylim(1e-4,.3)
ax[0].set_xlabel('odd steps of n+512 minus odd steps of n'); ax[0].set_ylabel('share of n')
ax[0].set_title('picks 0, 5, 12, 17, 24, 29...',fontsize=10)
# right: even-step difference vs odd-step difference, dot area = share
v=np.unique(np.stack([da,db],1),axis=0,return_counts=True)
pts,c=v; keep=c>len(da)*3e-5
ax[1].scatter(pts[keep,0],pts[keep,1],s=c[keep]/len(da)*3000+3,color='#8a2f2f',alpha=.8)
xs=np.array([-70,70]); ax[1].plot(xs,xs*L,color='#222',lw=.7)
ax[1].set_xlim(-70,70); ax[1].set_ylim(-110,110)
ax[1].set_xlabel('odd-step difference'); ax[1].set_ylabel('even-step difference')
ax[1].set_title('on the line  even = odd x log2 3',fontsize=10)
plt.tight_layout(); plt.savefig('assets/pairs.png')
print(np.mean(np.abs(dev)<0.2), np.mean(np.abs(dev)<0.1))
