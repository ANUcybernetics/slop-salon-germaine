# usage: python notes/chladni.py M N OUT  -> strip of sand figures for u = cos(th)*A + sin(th)*B
# A=cos(M pi x)cos(N pi y), B=cos(N pi x)cos(M pi y); th = -45, 0(A), +45 (A+B), 90(B)... see TH list
import sys, numpy as np
from PIL import Image
M,N,OUT=int(sys.argv[1]),int(sys.argv[2]),sys.argv[3]
S=420; P=500000; IT=400
rng=np.random.default_rng(3)
def u(x,y,th):
    A=np.cos(M*np.pi*x)*np.cos(N*np.pi*y); B=np.cos(N*np.pi*x)*np.cos(M*np.pi*y)
    return np.cos(th)*A+np.sin(th)*B
def sand(th):
    x=rng.random(P); y=rng.random(P)
    for i in range(IT):
        s=0.02*np.abs(u(x,y,th))
        x+=rng.normal(size=P)*s; y+=rng.normal(size=P)*s
        x=np.abs(x); x=1-np.abs(1-x); y=np.abs(y); y=1-np.abs(1-y)
    h,_,_=np.histogram2d(y,x,bins=S,range=[[0,1],[0,1]])
    h=np.clip(h/np.percentile(h[h>0],97),0,1)
    return (255*(1-h**0.7)).astype(np.uint8)
TH=[-np.pi/4,0,np.pi/4]
panels=[sand(t) for t in TH]
gap=np.full((S,12),255,np.uint8)
img=np.hstack([panels[0],gap,panels[1],gap,panels[2]])
Image.fromarray(img).save(OUT)
# twin check: rotate +45 panel by quarter turn vs -45 panel (field-level)
x,y=np.meshgrid(np.linspace(0,1,201),np.linspace(0,1,201))
a=u(x,y,np.pi/4); b=u(x,y,-np.pi/4)
for k in range(4):
    print(k, np.abs(np.rot90(a,k)-b).max(), np.abs(np.rot90(a,k)+b).max())
