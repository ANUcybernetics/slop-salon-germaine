# usage: python notes/lyap3fig.py  (reads assets/l3a,l3b .csv/.npy) -> assets/l3fig.jpg
import numpy as np, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
fig=plt.figure(figsize=(11,7),dpi=110,facecolor='#f6f2ea')
ax=fig.add_axes([.07,.6,.9,.36]); ax2=fig.add_axes([.07,.37,.9,.19],sharex=ax)
for n,c,l in (('a','#c0392b','F .037 k .060'),('b','#1f4e79','F .033 k .059')):
    r=np.loadtxt(f'assets/l3{n}.csv',delimiter=','); ax.plot(r[:,0],r[:,1],c=c,lw=1.2,label=l); ax2.plot(r[:,0],r[:,3],c=c,lw=1.2)
ax.axhline(0,c='k',lw=.5); ax.set_ylabel('growth per step\n(log, poke 1)'); ax.legend(frameon=False,loc='upper right')
ax2.set_ylabel('cosine, poke 1 vs 2'); ax2.set_xlabel('steps'); ax2.set_ylim(-1.1,1.1)
for a in (ax,ax2):
    a.set_facecolor('#f6f2ea'); [a.spines[s].set_visible(False) for s in ('top','right')]
plt.setp(ax.get_xticklabels(),visible=False)
for i,(n,t) in enumerate((('a','F .037'),('b','F .033'))):
    m=np.load(f'assets/l3{n}.npy')[0]; m=np.abs(m); m=m/m.max()
    ai=fig.add_axes([.07+i*.2,.0,.19,.24]); ai.imshow(m**.5,cmap='magma_r'); ai.axis('off'); ai.set_title('|mode| at end, '+t,fontsize=8)
fig.savefig('assets/l3fig.png'); 
