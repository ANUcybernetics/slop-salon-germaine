# same-length Stern-parity loops with different bbox sides, drawn on their tile map. usage: sternpair.py OUT
import sys, numpy as np
from PIL import Image, ImageDraw
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components
N=512; out=sys.argv[1]
X,Y=np.meshgrid(np.arange(N),np.arange(N)); o=((X^Y)%3==0)
H=N*(N+1); h=lambda x,y:y*N+x; v=lambda x,y:H+y*(N+1)+x
n,s,w,e=h(X,Y),h(X,Y+1),v(X,Y),v(X+1,Y)
b=np.where(o,w,e); d=np.where(o,e,w)
A=np.concatenate([n.ravel(),s.ravel()]); B=np.concatenate([b.ravel(),d.ravel()])
g=coo_matrix((np.ones(len(A)),(A,B)),shape=(2*H,)*2)
k_,lab=connected_components(g,directed=False); cnt=np.bincount(lab,minlength=k_)
idx=np.arange(2*H); hx=np.where(idx<H,(idx%N)+.5,(idx-H)%(N+1)); hy=np.where(idx<H,idx//N,(idx-H)//(N+1)+.5)
def find(L,side):
    for c in np.where(cnt==L)[0]:
        m=lab==c
        if ((hx[m]==0)|(hx[m]==N)|(hy[m]==0)|(hy[m]==N)).any(): continue
        if max(np.ptp(hx[m]),np.ptp(hy[m]))==side: return c
sc=16; pad=2
rows=[((44,7),(44,9)),((184,38),(184,41))]
pan=[]
for r in rows:
    pr=[]
    for L,sd in r:
        c=find(L,sd); m=lab==c
        x0,x1,y0,y1=int(hx[m].min()),int(np.ceil(hx[m].max())),int(hy[m].min()),int(np.ceil(hy[m].max()))
        pr.append((L,sd,c,x0,x1,y0,y1))
    pan.append(pr)
W=2*40+sum(1 for _ in range(1)) and 1500
rh=[max(p[6]-p[5] for p in pr)*sc+2*pad*sc+50 for pr in pan]
img=Image.new('RGB',(W,int(sum(rh))+20),(250,246,236)); dr=ImageDraw.Draw(img)
yc=10
for pr,hh in zip(pan,rh):
    xo=30
    for L,sd,c,x0,x1,y0,y1 in pr:
        for yy in range(y0-pad,y1+pad):
            for xx in range(x0-pad,x1+pad):
                if o[yy,xx]:
                    X0=xo+(xx-x0+pad)*sc; Y0=yc+(yy-y0+pad)*sc
                    dr.rectangle([X0,Y0,X0+sc-1,Y0+sc-1],fill=(236,226,208))
        col=(20,40,90) if sd in (7,38) else (176,70,30)
        for yy in range(y0-pad,y1+pad):
            for xx in range(x0-pad,x1+pad):
                nn,ss,ww,ee=h(xx,yy),h(xx,yy+1),v(xx,yy),v(xx+1,yy)
                pts={nn:(xx+.5,yy),ss:(xx+.5,yy+1),ww:(xx,yy+.5),ee:(xx+1,yy+.5)}
                for p,q in ([(nn,ww),(ss,ee)] if o[yy,xx] else [(nn,ee),(ss,ww)]):
                    if lab[p]==c:
                        f=lambda t:(xo+(t[0]-x0+pad)*sc,yc+(t[1]-y0+pad)*sc)
                        dr.line([f(pts[p]),f(pts[q])],fill=col,width=3)
        xo+=(x1-x0+2*pad)*sc+50
    yc+=hh
img.save(out); print(img.size)
