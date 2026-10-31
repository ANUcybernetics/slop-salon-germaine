# draw the longest closed Stern-parity Truchet loop at N, cropped to its bbox. usage: sternloop.py N OUT [px]
import sys, numpy as np
from PIL import Image, ImageDraw
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components
N=int(sys.argv[1]); out=sys.argv[2]; PX=int(sys.argv[3]) if len(sys.argv)>3 else 700
X,Y=np.meshgrid(np.arange(N),np.arange(N)); o=((X^Y)%3==0)
H=N*(N+1); h=lambda x,y:y*N+x; v=lambda x,y:H+y*(N+1)+x
n,s,w,e=h(X,Y),h(X,Y+1),v(X,Y),v(X+1,Y)
b=np.where(o,w,e); d=np.where(o,e,w)
A=np.concatenate([n.ravel(),s.ravel()]); B=np.concatenate([b.ravel(),d.ravel()])
g=coo_matrix((np.ones(len(A)),(A,B)),shape=(2*H,)*2)
k,lab=connected_components(g,directed=False); cnt=np.bincount(lab,minlength=k)
c=np.argsort(cnt)[::-1][0]
idx=np.arange(2*H); hx=np.where(idx<H,(idx%N)+.5,(idx-H)%(N+1)); hy=np.where(idx<H,idx//N,(idx-H)//(N+1)+.5)
m=lab==c; x0,x1,y0,y1=hx[m].min(),hx[m].max(),hy[m].min(),hy[m].max()
sc=PX/(max(x1-x0,y1-y0)+2)
img=Image.new('RGB',(PX,PX),(250,246,236)); dr=ImageDraw.Draw(img)
# tiles in bbox: draw arcs as segments between edge midpoints belonging to loop
for yy in range(int(y0),int(y1)+1):
  for xx in range(int(x0),int(x1)+1):
    if yy>=N or xx>=N: continue
    nn,ss,ww,ee=h(xx,yy),h(xx,yy+1),v(xx,yy),v(xx+1,yy)
    pts={nn:(xx+.5,yy),ss:(xx+.5,yy+1),ww:(xx,yy+.5),ee:(xx+1,yy+.5)}
    pairs=[(nn,ww),(ss,ee)] if o[yy,xx] else [(nn,ee),(ss,ww)]
    for p,q in pairs:
      if lab[p]==c:
        f=lambda P:((P[0]-x0+1)*sc,(P[1]-y0+1)*sc)
        dr.line([f(pts[p]),f(pts[q])],fill=(20,40,90),width=max(1,int(sc*0.5)))
img.save(out); print(N,cnt[c],x0,x1,y0,y1)
