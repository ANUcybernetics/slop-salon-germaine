# bbox sides of every closed Stern-parity Truchet loop with >=MIN nodes. usage: sternsides.py N MIN
import sys, numpy as np
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components
N=int(sys.argv[1]); MIN=int(sys.argv[2])
H=N*(N+1); h=lambda x,y:y*N+x; v=lambda x,y:H+y*(N+1)+x
X,Y=np.meshgrid(np.arange(N),np.arange(N)); o=((X^Y)%3==0)
n,s,w,e=h(X,Y),h(X,Y+1),v(X,Y),v(X+1,Y)
b=np.where(o,w,e); d=np.where(o,e,w)
A=np.concatenate([n.ravel(),s.ravel()]); B=np.concatenate([b.ravel(),d.ravel()])
g=coo_matrix((np.ones(len(A)),(A,B)),shape=(2*H,)*2)
k,lab=connected_components(g,directed=False)
cnt=np.bincount(lab,minlength=k)
idx=np.arange(2*H); hx=np.where(idx<H,(idx%N)+.5,(idx-H)%(N+1)); hy=np.where(idx<H,idx//N,(idx-H)//(N+1)+.5)
res={}
for c in np.where(cnt>=MIN)[0]:
    m=lab==c
    if ((hx[m]==0)|(hx[m]==N)|(hy[m]==0)|(hy[m]==N)).any(): continue
    key=(int(cnt[c]),int(max(np.ptp(hx[m]),np.ptp(hy[m]))))
    res[key]=res.get(key,0)+1
for key in sorted(res): print(key,res[key])
