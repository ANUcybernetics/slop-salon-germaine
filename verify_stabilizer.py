"""verify_stabilizer.py — two point-stabilizers of A_n generate A_n.
And do the trefoil's A5 images in A6 sit on distinct point-stabilizers?
"""
import itertools, math
import numpy as np
from build_An import build_An
from make_seam_profile import fixed_points

def closure(elems, size, mul, inv, ident):
    gen = sorted(set(elems))
    H = {ident}; frontier=[ident]
    for g in gen:
        if g not in H:
            H.add(g); frontier.append(g)
    while frontier:
        a=frontier.pop()
        for b in gen:
            for c in (mul[a,b], mul[b,a], inv[b]):
                if c not in H:
                    H.add(c); frontier.append(c)
    return sorted(H)

def point_stab(n, i):
    """Index (in build_An(n) ordering) of the point-stabilizer of point i."""
    elems=[p for p in itertools.permutations(range(n)) if perm_sign(p)==1]
    return [tuple(p) for p in elems if p[i]==i]

def perm_sign(p):
    n=len(p); seen=[False]*n; s=1
    for i in range(n):
        if not seen[i]:
            j=i; l=0
            while not seen[j]:
                seen[j]=True; j=p[j]; l+=1
            s*=(-1)**(l-1)
    return s

for n in (5,6,7):
    size,mul,inv,conj,order = build_An(n)
    ident=int(np.where(order==1)[0][0])
    # pick two distinct point-stabilizers
    stabs=[]
    for i in range(n):
        ps=point_stab(n,i)
        stabs.append([idx for idx,p in enumerate(ps)] if False else None)
    # use actual table indices: rebuild via permutation index map
    elems=[p for p in itertools.permutations(range(n)) if perm_sign(p)==1]
    idxmap={e:i for i,e in enumerate(elems)}
    st1=sorted(idxmap[e] for e in point_stab(n,0))
    st2=sorted(idxmap[e] for e in point_stab(n,1))
    J=closure(st1+st2, size, mul, inv, ident)
    print(f"A_{n}: |stab(0)|={len(st1)}, |stab(1)|={len(st2)}, join=<stab0,stab1> = |{len(J)}|  "
          f"(A_{n} has order {size})  -> {'GENERATES A_%d'%n if len(J)==size else 'NO'}")
