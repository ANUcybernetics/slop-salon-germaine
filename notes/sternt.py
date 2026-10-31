# Truchet on tile = [3 | x^y] (parity of Stern s(x^y)); rank-size of curve lengths. usage: sternt.py N...
import sys, numpy as np
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components
def lengths(N, o):
    H=N*(N+1); h=lambda x,y:y*N+x; v=lambda x,y:H+y*(N+1)+x
    X,Y=np.meshgrid(np.arange(N),np.arange(N))
    n,s,w,e=h(X,Y),h(X,Y+1),v(X,Y),v(X+1,Y)
    a=np.where(o,n,n); b=np.where(o,w,e); c=np.where(o,s,s); d=np.where(o,e,w)
    A=np.concatenate([a.ravel(),c.ravel()]); B=np.concatenate([b.ravel(),d.ravel()])
    T=2*H
    g=coo_matrix((np.ones(len(A)),(A,B)),shape=(H+N*(N+1),)*2)
    k,lab=connected_components(g,directed=False)
    cnt=np.bincount(lab); cnt=cnt[cnt>1]   # nodes per curve
    return np.sort(cnt)[::-1]
for N in map(int,sys.argv[1:]):
    X,Y=np.meshgrid(np.arange(N),np.arange(N))
    o=((X^Y)%3==0)
    L=lengths(N,o)
    r=np.arange(1,len(L)+1)/(N*N)
    sel=(L>=16)&(L<N)
    sl=np.polyfit(np.log(L[sel]),np.log(r[sel]),1)[0] if sel.sum()>3 else float('nan')
    print(N,'curves',len(L),'longest',L[0],'longest/N',round(L[0]/N,2),'slope',round(sl,2),'top5',L[:5])
