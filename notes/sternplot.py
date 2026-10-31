# rank-size of Stern-parity Truchet vs coin (slope -8/7 line). usage: sternplot.py OUT
import sys, numpy as np, importlib.util
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
sys.argv=['x']; spec=importlib.util.spec_from_file_location('st','notes/sternt.py'); st=importlib.util.module_from_spec(spec); spec.loader.exec_module(st)
out=sys.argv_out if hasattr(sys,'argv_out') else None
import os; out=os.environ['OUT']
fig,ax=plt.subplots(figsize=(7,7),facecolor='#0e0e12'); ax.set_facecolor('#0e0e12')
for N,c in ((256,'#6a7fb0'),(512,'#7fb0a0'),(1024,'#d6c27a'),(2048,'#ffecaa')):
    X,Y=np.meshgrid(np.arange(N),np.arange(N)); L=st.lengths(N,(X^Y)%3==0)
    ax.loglog(L,np.arange(1,len(L)+1)/(N*N),'.',ms=3,color=c,label=f'{N}x{N}')
x=np.array([8,4000]); ax.loglog(x,0.5*(x/8.)**(-8/7)*0.05,'--',color='#e8793a',lw=1,label='coin flips, -8/7')
ax.loglog(x,0.5*(x/8.)**(-1.81)*0.05,'--',color='#aaa',lw=1,label='this rule, -1.81')
ax.set_xlabel('curve length',color='#aaa'); ax.set_ylabel('curves at least this long, per tile',color='#aaa')
ax.tick_params(colors='#888'); [s.set_color('#444') for s in ax.spines.values()]
ax.legend(facecolor='#0e0e12',labelcolor='#ccc',edgecolor='#444'); plt.savefig(out,dpi=130,facecolor=fig.get_facecolor())
