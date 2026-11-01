# the shapes of one length chain, one row per length, 4 shapes each by copy count. usage: shapedraw.py N L1,L2,.. OUT
import sys, numpy as np, collections
from PIL import Image, ImageDraw
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components
N=int(sys.argv[1]); Ls=[int(t) for t in sys.argv[2].split(',')]; out=sys.argv[3]
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
rows=[]
for L in Ls:
    cl=collections.defaultdict(list)
    for c in np.where((cnt==L)&~border)[0]:
        ids=order[bounds[c]:bounds[c+1]]
        xs=hx[ids]-hx[ids].min(); ys=hy[ids]-hy[ids].min()
        a=tuple(sorted(zip(xs.tolist(),ys.tolist()))); t=tuple(sorted(zip(ys.tolist(),xs.tolist())))
        cl[min(a,t)].append(c)
    top=sorted(cl.values(),key=len,reverse=True)[:4]
    rows.append((L,[(len(t),t[0]) for t in top]))
# segments of a component
LA=lab[A]; 
def segs(c):
    m=LA==c; return A[m],B[m]
S=230; cellw=300; img=Image.new('RGB',(cellw*4+20,(S+40)*len(rows)+10),(250,246,236)); dr=ImageDraw.Draw(img)
for r,(L,shs) in enumerate(rows):
    for k,(cp,c) in enumerate(shs):
        a,bb=segs(c); xa,ya,xb,yb=hx[a],hy[a],hx[bb],hy[bb]
        x0=min(xa.min(),xb.min()); y0=min(ya.min(),yb.min()); x1=max(xa.max(),xb.max()); y1=max(ya.max(),yb.max())
        sc=min((cellw-30)/max(x1-x0,1),S/max(y1-y0,1)); sc=min(sc,12)
        ox=10+k*cellw+((cellw-20)-(x1-x0)*sc)/2; oy=10+r*(S+40)+(S-(y1-y0)*sc)/2
        for i in range(len(a)):
            dr.line([ox+(xa[i]-x0)*sc,oy+(ya[i]-y0)*sc,ox+(xb[i]-x0)*sc,oy+(yb[i]-y0)*sc],fill=(20,40,90),width=2)
        dr.text((10+k*cellw,10+r*(S+40)+S+8),f"L={L}  x{cp}  {int(x1-x0)//2}x{int(y1-y0)//2}",fill=(80,70,60))
img.save(out); print(img.size,[(L,[c for c,_ in s]) for L,s in rows])
