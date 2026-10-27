# Power iteration on the dish: reference run + nearby run, difference renormalised to norm R0 every W steps.
# usage: python notes/lyap.py N G F K STEPS W SEED OUT   -> OUT.npy = final unit difference in V (and growth log)
import numpy as np, sys
N,G,F,K,S,W,seed=int(sys.argv[1]),int(sys.argv[2]),float(sys.argv[3]),float(sys.argv[4]),int(sys.argv[5]),int(sys.argv[6]),int(sys.argv[7]); out=sys.argv[8]
z=np.zeros((N,N),np.int64); z[N//2,N//2]=G
while True:
    k=z//4
    if not k.any(): break
    z-=4*k; z[1:]+=k[:-1]; z[:-1]+=k[1:]; z[:,1:]+=k[:,:-1]; z[:,:-1]+=k[:,1:]
U=np.ones((N,N)); V=np.zeros((N,N)); V[z==3]=0.5; U[z==3]=0.5
rng=np.random.default_rng(seed); R0=1e-7
dU=rng.standard_normal((N,N))*0; dV=rng.standard_normal((N,N))
dV*=R0/np.linalg.norm(dV)
U2=U+dU; V2=V+dV
lap=lambda a: np.roll(a,1,0)+np.roll(a,-1,0)+np.roll(a,1,1)+np.roll(a,-1,1)-4*a
def step(U,V):
    uvv=U*V*V
    return U+0.16*lap(U)-uvv+F*(1-U), V+0.08*lap(V)+uvv-(F+K)*V
log=[]
for t in range(1,S+1):
    U,V=step(U,V); U2,V2=step(U2,V2)
    if t%W==0:
        d1=U2-U; d2=V2-V
        n=np.sqrt((d1**2).sum()+(d2**2).sum()); log.append(np.log(n/R0)/W)
        U2=U+d1*R0/n; V2=V+d2*R0/n
        print(t,'rate/step %.5f'%log[-1],flush=True)
d=(V2-V); d/=np.linalg.norm(d)
np.save(out+'.npy',d); np.save(out+'_ref.npy',V)
