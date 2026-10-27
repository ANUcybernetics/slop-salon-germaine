# Two pokes on one dish; cosine between their renormalised differences over time (does power iteration converge to one axis?)
# usage: python notes/lyap3.py N G F K STEPS W OUT   -> OUT.csv (t, rate1, rate2, cos), OUT.npy (two final unit modes)
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
P=[]
for s in (1,2):
    d=np.random.default_rng(s).standard_normal((N,N)); P.append([U.copy(),V+d*R0/np.linalg.norm(d)])
rows=[]
for t in range(1,S+1):
    U,V=step(U,V)
    for p in P: p[0],p[1]=step(p[0],p[1])
    if t%W==0:
        ds=[];rt=[]
        for p in P:
            d1=p[0]-U; d2=p[1]-V; n=np.sqrt((d1**2).sum()+(d2**2).sum()); rt.append(np.log(n/R0)/W)
            p[0]=U+d1*R0/n; p[1]=V+d2*R0/n; ds.append(np.concatenate([d1.ravel(),d2.ravel()])/n)
        c=float(ds[0]@ds[1]); rows.append((t,rt[0],rt[1],c)); print(t,'%.5f %.5f cos %.3f'%(rt[0],rt[1],c),flush=True)
open(out+'.csv','w').write('\n'.join(','.join(map(str,r)) for r in rows))
np.save(out+'.npy',np.array([(p[1]-V) for p in P]))
