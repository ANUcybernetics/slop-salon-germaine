# distinct loop shapes per length on a Stern-parity page, up to translation+transpose. usage: shapes.py N
import sys, numpy as np, collections
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components
N=int(sys.argv[1])
X,Y=np.meshgrid(np.arange(N),np.arange(N)); o=((X^Y)%3==0)
H=N*(N+1); h=lambda x,y:y*N+x; v=lambda x,y:H+y*(N+1)+x
n,s,w,e=h(X,Y),h(X,Y+1),v(X,Y),v(X+1,Y)
b=np.where(o,w,e); d=np.where(o,e,w)
A=np.concatenate([n.ravel(),s.ravel()]); B=np.concatenate([b.ravel(),d.ravel()])
g=coo_matrix((np.ones(len(A)),(A,B)),shape=(2*H,)*2)
k_,lab=connected_components(g,directed=False); cnt=np.bincount(lab,minlength=k_)
idx=np.arange(2*H)
hx=np.where(idx<H,2*(idx%N)+1,2*((idx-H)%(N+1))); hy=np.where(idx<H,2*(idx//N),2*((idx-H)//(N+1))+1)
border=np.zeros(k_,bool)
for arr,val in ((hx,0),(hx,2*N),(hy,0),(hy,2*N)): border[np.unique(lab[arr==val])]=True
order=np.argsort(lab,kind='stable'); bounds=np.r_[0,np.cumsum(cnt)]
res=collections.defaultdict(collections.Counter)
for c in np.where(~border)[0]:
    ids=order[bounds[c]:bounds[c+1]]
    xs=hx[ids]-hx[ids].min(); ys=hy[ids]-hy[ids].min()
    a=tuple(sorted(zip(xs.tolist(),ys.tolist()))); t=tuple(sorted(zip(ys.tolist(),xs.tolist())))
    res[int(cnt[c])][min(a,t)]+=1
print("L  loops  shapes  top copies")
for L in sorted(res):
    cs=res[L]; print(L,sum(cs.values()),len(cs),sorted(cs.values(),reverse=True)[:6])
