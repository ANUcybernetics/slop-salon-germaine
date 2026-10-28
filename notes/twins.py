# Push a converged dish along +mode and -mode, run on, save the two outcomes. usage: python notes/twins.py IN.npz F K EPS STEPS OUT
import numpy as np, sys
D=np.load(sys.argv[1]); F,K,eps,S=float(sys.argv[2]),float(sys.argv[3]),float(sys.argv[4]),int(sys.argv[5]); out=sys.argv[6]
lap=lambda a: np.roll(a,1,0)+np.roll(a,-1,0)+np.roll(a,1,1)+np.roll(a,-1,1)-4*a
def step(U,V):
    uvv=U*V*V
    return U+0.16*lap(U)-uvv+F*(1-U), V+0.08*lap(V)+uvv-(F+K)*V
st={'plus':(D['U']+eps*D['dU'],D['V']+eps*D['dV']),'minus':(D['U']-eps*D['dU'],D['V']-eps*D['dV']),'ref':(D['U'].copy(),D['V'].copy())}
for t in range(S):
    for k,(U,V) in st.items(): st[k]=step(U,V)
np.savez(out,**{k:v[1] for k,v in st.items()})
