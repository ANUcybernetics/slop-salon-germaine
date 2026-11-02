# usage: ford2.py Q X OUT  -- Ford horocycles in the Poincare disk, m=2 (rust) and m=3 (navy) connectors
import sys, math
from fractions import Fraction
import numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
Q=int(sys.argv[1]); X=int(sys.argv[2]); out=sys.argv[3]
fr=sorted({Fraction(p,q) for q in range(1,Q+1) for p in range(-X*q,X*q+1)})
def cay(z): return (z-1j)/(z+1j)
def circ(f):
    q=f.denominator; x=float(f); r=1/(2*q*q)
    t=np.linspace(0,2*np.pi,400); return cay(x+1j*(r+r*np.exp(1j*t)))
def cross(f,g):
    x1,x2=float(f),float(g); c=(x1+x2)/2; R=abs(x1-x2)/2
    pts=[]
    for h in (f,g):
        q=h.denominator; xh=float(h); r=1/(2*q*q)
        # solve |z-c|=R, |z-(xh+ir)|=r, z in upper half plane, z != xh
        d=complex(xh-c,r); D=abs(d)
        a=(R*R-r*r+D*D)/(2*D); hh=math.sqrt(max(R*R-a*a,0))
        u=d/D; base=c+a*u
        for s in (1,-1):
            z=base+s*1j*hh*u
            if z.imag>1e-12 and abs(z-xh)>1e-9: pts.append(z)
    return pts
def blocked(pts,f,g):
    for h in fr:
        if h in (f,g): continue
        q=h.denominator; r=1/(2*q*q); ctr=float(h)+1j*r
        if np.any(np.abs(pts-ctr)<r-1e-7): return True
    return bool(np.any(pts.imag>1+1e-7))
def hd(z,w): return math.acosh(1+abs(z-w)**2/(2*z.imag*w.imag))
fig,ax=plt.subplots(figsize=(10,10),dpi=150); ax.set_aspect('equal'); ax.axis('off')
ax.add_patch(plt.Circle((0,0),1,fill=False,color='#222',lw=.8))
for f in fr:
    c=circ(f); ax.fill(c.real,c.imag,color='#e8e2d4',ec='#8a8070',lw=.3)
# horocycle at infinity: y>=1 -> circle tangent at 1
t=np.linspace(0,2*np.pi,400); inf=cay(np.array([1e9]))  # placeholder
ci=0.5+0.5*np.exp(1j*t)*0  # unused
# image of y=1 line: circle through cay(i+x) ; centre/radius from three points
p3=[cay(complex(x,1)) for x in (-50,0,50)]
A=np.array([[2*(p.real),2*(p.imag),1] for p in p3]); b=np.array([-(abs(p)**2) for p in p3])
# solve x^2+y^2+Dx+Ey+F=0  => Dx+Ey+F=-(x^2+y^2)
A=np.array([[p.real,p.imag,1] for p in p3]); D_,E_,F_=np.linalg.solve(A,b)
cx,cy=-D_/2,-E_/2; rr=math.sqrt(cx*cx+cy*cy-F_)
ax.add_patch(plt.Circle((cx,cy),rr,color='#e8e2d4',ec='#8a8070',lw=.3))
dists={m:[] for m in range(2,7)}
cols={2:'#b5481f',3:'#1f3a6b',4:'#1f3a6b',5:'#1f3a6b',6:'#1f3a6b'}
for i,f in enumerate(fr):
    for g in fr[i+1:]:
        m=abs(g.numerator*f.denominator-f.numerator*g.denominator)
        if m in (2,3,4,5,6):
            pts=cross(f,g)
            if len(pts)!=2: continue
            z,w=sorted(pts,key=lambda p:p.real)
            c=(float(f)+float(g))/2; R=abs(float(f)-float(g))/2
            a0=math.atan2(z.imag,z.real-c); a1=math.atan2(w.imag,w.real-c)
            th=np.linspace(a0,a1,60); half=c+R*np.exp(1j*th)
            if blocked(half,f,g): continue
            arc=cay(half)
            ax.plot(arc.real,arc.imag,color=cols[m],lw=1.6,solid_capstyle='round')
            dists[m].append(hd(z,w))
for m in dists:
    d=np.array(dists[m]+[0]); print(m,len(d),d.min(),d.max(),2*math.log(m))
ax.set_xlim(-1.01,1.01); ax.set_ylim(-1.01,1.01)
fig.savefig(out,bbox_inches='tight',pad_inches=.05,facecolor='#faf7f0')
