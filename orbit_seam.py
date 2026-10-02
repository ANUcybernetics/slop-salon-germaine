import numpy as np
from build_PSL import build_PSL
WORDS = {"conway": [-1, 2, -1, 2, -1, 3, -2, -2, -1, 3, 3],
         "kt": [-1, 2, 2, -3, -3, 2, 1, -2, -2, 3, -2, 3, -2]}
def apply_auto(X, moves, mul, inv, conj):
    for (i, eps) in moves:
        a=X[:,i].copy(); b=X[:,i+1].copy()
        if eps>0: na=conj[a,b]; nb=a
        else: na=b; nb=conj[inv[b],a]
        X[:,i]=na; X[:,i+1]=nb
    return X
def closure(gens,mul):
    S={1}; fr=[1]
    while fr:
        ng=[]
        for f in fr:
            for g in gens:
                h=int(mul[f,g])
                if h not in S: S.add(h); ng.append(h)
        fr=ng
    return len(S)
for p,seamorder in [(7,3),(13,6)]:
    size,mul,inv,conj,order,reps = build_PSL(p)
    classes={}
    for b in range(size):
        rep=min(int(conj[a,b]) for a in range(size))
        classes.setdefault(rep,[]).append(b)
    rep=[r for r in classes if order[r]==seamorder][0]
    members=classes[rep]; m=len(members); mem=np.array(members,dtype=np.int64)
    g3=np.repeat(mem,m); g4=np.tile(mem,m)
    A=np.zeros((m*m,4),dtype=np.int64); A[:,0]=rep; A[:,2]=g3; A[:,3]=g4
    print(f"\n--- PSL(2,{p}), seam class order {seamorder}, |C|={m} ---")
    for name,word in WORDS.items():
        moves=[(abs(g)-1,1 if g>0 else -1) for g in word]
        onto_orbits=set(); nonto=0
        for x2 in members:
            A[:,1]=x2
            mask=np.all(apply_auto(A.copy(),moves,mul,inv,conj)==A,axis=1)
            for r in np.nonzero(mask)[0]:
                t=(rep,int(x2),int(g3[r]),int(g4[r]))
                if closure(list(t),mul)==size:
                    nonto+=1
                    orb={tuple(int(mul[mul[g,x],inv[g]]) for x in t) for g in range(size)}
                    onto_orbits.add(min(orb))
        print(f"  {name}: onto-hand tuples(x1=rep)={nonto}  distinct Inn-orbits={len(onto_orbits)}")
