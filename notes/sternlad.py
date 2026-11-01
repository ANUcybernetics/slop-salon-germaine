# ladder of Stern-parity loops, one per k: L=(14*2^k+76+4*(k odd))/3, laid flat. usage: sternlad.py OUT
import sys, numpy as np
from PIL import Image, ImageDraw
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components
N=1024; out=sys.argv[1]
X,Y=np.meshgrid(np.arange(N),np.arange(N)); o=((X^Y)%3==0)
H=N*(N+1); h=lambda x,y:y*N+x; v=lambda x,y:H+y*(N+1)+x
n,s,w,e=h(X,Y),h(X,Y+1),v(X,Y),v(X+1,Y)
b=np.where(o,w,e); d=np.where(o,e,w)
A=np.concatenate([n.ravel(),s.ravel()]); B=np.concatenate([b.ravel(),d.ravel()])
g=coo_matrix((np.ones(len(A)),(A,B)),shape=(2*H,)*2)
k_,lab=connected_components(g,directed=False); cnt=np.bincount(lab,minlength=k_)
idx=np.arange(2*H); hx=np.where(idx<H,(idx%N)+.5,(idx-H)%(N+1)); hy=np.where(idx<H,idx//N,(idx-H)//(N+1)+.5)
W=1500; sc=6.0; rowh=[]
panels=[]
for k in range(3,8):
    L=(14*2**k+76+4*(k%2))//3
    for c in np.where(cnt==L)[0]:
        m=lab==c
        if ((hx[m]==0)|(hy[m]==0)).any(): continue
        if max(np.ptp(hx[m]),np.ptp(hy[m]))==2**k+2: break
    else: raise SystemExit('no loop k=%d'%k)
    m=lab==c; x0,x1,y0,y1=hx[m].min(),hx[m].max(),hy[m].min(),hy[m].max()
    segs=[]
    for yy in range(int(y0),int(y1)+1):
      for xx in range(int(x0),int(x1)+1):
        nn,ss,ww,ee=h(xx,yy),h(xx,yy+1),v(xx,yy),v(xx+1,yy)
        pts={nn:(xx+.5,yy),ss:(xx+.5,yy+1),ww:(xx,yy+.5),ee:(xx+1,yy+.5)}
        pairs=[(nn,ww),(ss,ee)] if o[yy,xx] else [(nn,ee),(ss,ww)]
        for p,q in pairs:
            if lab[p]==c: segs.append((pts[p],pts[q]))
    P=np.array([p for sg in segs for p in sg]); mu=P.mean(0)
    u,sv,vt=np.linalg.svd(P-mu); R=vt  # rows: along, across
    T=lambda p,mu=mu,R=R:(np.array(p)-mu)@R.T
    allp=np.array([T(p) for p in P]); lo=allp.min(0); hi=allp.max(0)
    panels.append((k,L,segs,T,lo,hi))
tot=sum((hi[1]-lo[1])*sc+70 for *_,lo,hi in panels)+40
img=Image.new('RGB',(W,int(tot)),(250,246,236)); dr=ImageDraw.Draw(img)
yc=30
for k,L,segs,T,lo,hi in panels:
    col=(20,40,90) if k%2==0 else (176,70,30)
    for p,q in segs:
        a=T(p);bq=T(q)
        f=lambda t:(20+(t[0]-lo[0])*sc, yc+(t[1]-lo[1])*sc)
        dr.line([f(a),f(bq)],fill=col,width=3)
    yc+=(hi[1]-lo[1])*sc+70
img.save(out); print(img.size,[(k,L) for k,L,*_ in panels])
