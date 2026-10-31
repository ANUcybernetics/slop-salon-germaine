# longest Stern-parity Truchet curves: lengths, bbox, and whether closed. usage: sternbig.py N...
import sys, numpy as np
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components
for N in map(int,sys.argv[1:]):
    H=N*(N+1); h=lambda x,y:y*N+x; v=lambda x,y:H+y*(N+1)+x
    X,Y=np.meshgrid(np.arange(N),np.arange(N)); o=((X^Y)%3==0)
    n,s,w,e=h(X,Y),h(X,Y+1),v(X,Y),v(X+1,Y)
    b=np.where(o,w,e); d=np.where(o,e,w)
    A=np.concatenate([n.ravel(),s.ravel()]); B=np.concatenate([b.ravel(),d.ravel()])
    g=coo_matrix((np.ones(len(A)),(A,B)),shape=(2*H,)*2)
    k,lab=connected_components(g,directed=False)
    cnt=np.bincount(lab,minlength=k)
    # node coordinates: horizontal-edge midpoints (x+.5,y), vertical (x,y+.5)
    idx=np.arange(2*H); hx=np.where(idx<H,(idx%N)+.5,(idx-H)%(N+1)); hy=np.where(idx<H,idx//N,(idx-H)//(N+1)+.5)
    for c in np.argsort(cnt)[::-1][:6]:
        m=lab==c
        # closed iff every node has degree 2 (no border node)
        onb=((hx[m]==0)|(hx[m]==N)|(hy[m]==0)|(hy[m]==N)).sum()
        print(N,cnt[c],'bbox',hx[m].min(),hx[m].max(),hy[m].min(),hy[m].max(),'border nodes',onb)
    print()
