# usage: stonesford.py Q OUT -- Ford circles (0..1, denominators <=Q) shaded as pebbles on a line, 1024^2, to sit beside a model's photo
import sys, numpy as np
from fractions import Fraction
from PIL import Image
Q=int(sys.argv[1]); out=sys.argv[2]
W=1024; S=2; N=W*S
yy,xx=np.mgrid[0:N,0:N].astype(float)
sky=np.array([228,236,242.]); sand=np.array([60,66,74.])
img=np.zeros((N,N,3)); base=int(N*0.5)
t=np.clip(yy/ base,0,1)[...,None]
img[:]=sky*(1-0.0*t)
img[base:]=sand
fr=sorted({Fraction(p,q) for q in range(1,Q+1) for p in range(0,q+1)}, key=lambda f:-f.denominator)
x0=N*0.27; L=N*0.46
for f in sorted(fr,key=lambda f:f.denominator):
    q=f.denominator; r=L/(2*q*q)
    cx=x0+float(f)*L; cy=base-r
    d2=((xx-cx)**2+(yy-cy)**2)/r**2
    m=d2<=1
    if not m.any(): continue
    nz=np.sqrt(np.clip(1-d2,0,1))
    nx=(xx-cx)/r; ny=(yy-cy)/r
    light=np.clip(0.55*(-nx*0.5-ny*0.7)+0.6*nz,0,1)
    g=(30+130*light)[...,None]*np.array([0.92,0.98,1.05])
    img[m]=g[m]
im=Image.fromarray(np.clip(img,0,255).astype(np.uint8)).resize((W,W),Image.LANCZOS)
im.save(out)
