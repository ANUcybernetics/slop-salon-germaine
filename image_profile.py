import numpy as np
from collections import Counter
from build_PSL import build_PSL
WORDS = {"conway": [-1, 2, -1, 2, -1, 3, -2, -2, -1, 3, 3],
         "kt": [-1, 2, 2, -3, -3, 2, 1, -2, -2, 3, -2, 3, -2]}
def apply_auto(X, moves, mul, inv, conj):
    for (i, eps) in moves:
        a = X[:, i].copy(); b = X[:, i + 1].copy()
        if eps > 0:
            na = conj[a, b]; nb = a
        else:
            na = b; nb = conj[inv[b], a]
        X[:, i] = na; X[:, i + 1] = nb
    return X
def closure(gens, mul):
    S=set([1]); frontier=[1]
    while frontier:
        ng=[]
        for f in frontier:
            for g in gens:
                h=int(mul[f,g])
                if h not in S: S.add(h); ng.append(h)
        frontier=ng
    return len(S)
size, mul, inv, conj, order, reps = build_PSL(13)
classes = {}
for b in range(size):
    rep = min(int(conj[a, b]) for a in range(size))
    classes.setdefault(rep, []).append(b)
# order each class by element order
for name, word in WORDS.items():
    moves=[(abs(g)-1,1 if g>0 else -1) for g in word]
    print(f"\n=== {name} : per-class reach (image size) ===")
    rows=[]
    for rep, members in classes.items():
        m=len(members); mem=np.array(members,dtype=np.int64)
        g3=np.repeat(mem,m); g4=np.tile(mem,m)
        A=np.zeros((m*m,4),dtype=np.int64); A[:,0]=rep; A[:,2]=g3; A[:,3]=g4
        imgs=Counter()
        for x2 in members:
            A[:,1]=x2
            mask=np.all(apply_auto(A.copy(),moves,mul,inv,conj)==A,axis=1)
            for r in np.nonzero(mask)[0]:
                imgs[closure([rep,int(x2),int(g3[r]),int(g4[r])],mul)]+=1
        rows.append((int(order[rep]), m, dict(imgs)))
    for o,m,imgs in sorted(rows):
        # summarize distinct image sizes -> counts
        s = {k:v for k,v in sorted(imgs.items())}
        print(f"  order {o:2d} (|C|={m:3d}): fixed tuples={sum(imgs.values()):3d}  image sizes (subgroup order -> #tuples) {s}")
