# Converged Lyapunov mode vs the dish's own fields. usage: python notes/modephys.py N G F K STEPS W OUT
# saves OUT.npz (U,V,dU,dV unit mode) after STEPS with one poke, renormalised every W steps
import numpy as np, sys
N,G,F,K,S,W=int(sys.argv[1]),int(sys.argv[2]),float(sys.argv[3]),float(sys.argv[4]),int(sys.argv[5]),int(sys.argv[6]); out=sys.argv[7]
z=np.zeros((N,N),np.int64); z[N//2,N//2]=G
while True:
    k=z//4
    if not k.any(): break
    z-=4*k; z[1:]+=k[:-1]; z[:-1]+=k[1:]; z[:,1:]+=k[:,:-1]; z[:,:-1]+=k[:,1:]
U=np.ones((N,N)); V=np.zeros((N,N)); V[z==3]=0.5; U[z==3]=0.5
R0=1e-7
lap=lambda a: np.roll(a,1,0)+np.roll(a,-1,0)+np.roll(a,1,1)+np.roll(a,-1,1)-4*a
def step(U,V):
    uvv=U*V*V
    return U+0.16*lap(U)-uvv+F*(1-U), V+0.08*lap(V)+uvv-(F+K)*V
d=np.random.default_rng(1).standard_normal((N,N)); pU,pV=U.copy(),V+d*R0/np.linalg.norm(d)
for t in range(1,S+1):
    U,V=step(U,V); pU,pV=step(pU,pV)
    if t%W==0:
        d1=pU-U; d2=pV-V; n=np.sqrt((d1**2).sum()+(d2**2).sum())
        pU=U+d1*R0/n; pV=V+d2*R0/n
        if t%2000==0: print(t,np.log(n/R0)/W,flush=True)
d1=pU-U; d2=pV-V; n=np.sqrt((d1**2).sum()+(d2**2).sum())
np.savez(out+'.npz',U=U,V=V,dU=d1/n,dV=d2/n)
