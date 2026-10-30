# usage: python ford.py QMAX OUT  -- Ford circles on [0,1]; tangent pairs (|bp-aq|=1) dotted, m=2 near-misses as thin chords
import sys, math
from math import gcd
from PIL import Image, ImageDraw
Q=int(sys.argv[1]); OUT=sys.argv[2]; X0=float(sys.argv[3]); X1=float(sys.argv[4])
W=2400; S=W/(X1-X0); H=1500
img=Image.new("RGB",(W,H),(18,16,24)); d=ImageDraw.Draw(img,"RGBA")
fr=[(p,q) for q in range(2,Q+1) for p in range(0,q+1) if gcd(p,q)==1]
def C(p,q):
    r=1/(2*q*q); return p/q, r
cols={1:(240,235,220),2:(235,150,60),3:(210,70,80),4:(60,170,170),5:(110,120,220)}
for p,q in sorted(fr,key=lambda t:-t[1]):
    x,r=C(p,q); cx=(x-X0)*S; cy=H-r*S; rr=r*S
    c=cols.get(q,(120,110,150)) if q<=5 else (90+ (q*7)%90,110,150+(q*13)%90)
    d.ellipse([cx-rr,cy-rr,cx+rr,cy+rr],fill=c+(70,),outline=c+(230,),width=1)
# tangency points between consecutive Farey neighbours at level Q
fr.sort(key=lambda t:t[0]/t[1])
for (p,q),(a,b) in zip(fr,fr[1:]):
    if abs(b*p-a*q)==1:
        x1,r1=C(p,q); x2,r2=C(a,b)
        t=r1/(r1+r2); tx=(x1+(x2-x1)*t)*S; ty=H-(r1+(r2-r1)*0)*S*0
        # tangent point on line of centres
        cy1=r1; cy2=r2
        px=x1+(x2-x1)*t; py=cy1+(cy2-cy1)*t
        qx=(px-X0)*S; d.ellipse([qx-4,H-py*S-4,qx+4,H-py*S+4],fill=(255,255,255,255))
img.save(OUT)
print(len(fr))
