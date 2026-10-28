# rate vs steps for the same dish on different page sizes (reads assets/pg/pN.csv from lyap3.py); usage: python notes/pagefig.py OUT
import numpy as np, sys, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
ns=[251,301,351,401,451,501,601]; cols=['#d55e00']+['#555']*5+['#0072b2']
fig,ax=plt.subplots(figsize=(9,5),dpi=150)
for n,c in zip(ns,cols):
    r=np.loadtxt(f'assets/pg/p{n}.csv',delimiter=',')
    ax.plot(r[:,0],r[:,1]*1000,color=c,lw=2 if n in(251,601) else 1,label=f'page {n}')
    ax.text(14100,r[-1,1]*1000+(0.12 if n==251 else (-0.15 if n==601 else 0)),str(n),color=c,fontsize=8,va='center')
ax.set_xlabel('steps'); ax.set_ylabel('e-folds per 1000 steps'); ax.set_xlim(0,14800); ax.set_ylim(-0.6,4.2)
ax.set_title('One dish (pile 100000, F .037 K .060), seven page sizes',fontsize=10)
for s in('top','right'): ax.spines[s].set_visible(False)
plt.tight_layout(); plt.savefig(sys.argv[1])
