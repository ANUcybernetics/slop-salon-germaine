# Regress the converged mode dV on the dish's own fields, per patch. usage: python notes/modephys2.py IN.npz
import numpy as np, sys
D=np.load(sys.argv[1]); V=D['V']; m=D['dV']; U=D['U']; mu=D['dU']
N=V.shape[0]
g=lambda a,ax: (np.roll(a,-1,ax)-np.roll(a,1,ax))/2
Vx,Vy=g(V,1),g(V,0)
L=np.roll(V,1,0)+np.roll(V,-1,0)+np.roll(V,1,1)+np.roll(V,-1,1)-4*V
print('V range',V.min(),V.max(),'mode energy in V',(m**2).sum(),'in U',(mu**2).sum())
E=m**2; ys,xs=np.unravel_index(np.argsort(E.ravel())[::-1][:5],E.shape); print('top cells',list(zip(ys,xs)),E.ravel()[np.argsort(E.ravel())[::-1][:5]])
# energy radial profile
yy,xx=np.mgrid[:N,:N]; r=np.hypot(yy-N//2,xx-N//2)
for a,b in [(0,20),(20,40),(40,70),(70,100),(100,150),(150,200),(200,290)]:
    s=(r>=a)&(r<b); print('r',a,b,'share of mode energy %.3f of area %.3f'%(E[s].sum()/E.sum(),s.mean()))
# patch regressions, patches 21x21 centred on top-energy sites
def fit(cy,cx,h=10):
    sl=(slice(cy-h,cy+h+1),slice(cx-h,cx+h+1))
    y=m[sl].ravel(); res={}
    for name,cols in {'shift(Vx,Vy)':[Vx,Vy],'amp(V)':[V],'width(L)':[L],'shift+amp+width':[Vx,Vy,V,L],'U':[U]}.items():
        A=np.stack([c[sl].ravel() for c in cols],1); co,*_=np.linalg.lstsq(A,y,rcond=None)
        res[name]=1-((y-A@co)**2).sum()/(y**2).sum()
    return res
# energy-weighted over 20x20 blocks
tot={}
blocks=[]
for cy in range(10,N-10,21):
    for cx in range(10,N-10,21):
        blocks.append((E[cy-10:cy+11,cx-10:cx+11].sum(),cy,cx))
blocks.sort(reverse=True)
for e,cy,cx in blocks[:8]:
    print('block',cy,cx,'energy %.3f'%e,{k:round(v,2) for k,v in fit(cy,cx).items()})
