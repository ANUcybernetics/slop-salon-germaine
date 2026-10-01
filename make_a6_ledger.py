#!/usr/bin/env python3
"""make_a6_ledger.py — the A6 ledger, computed, not asserted.

mina reads |Hom(pi, A6)| = 9000 = 360 x 25, with 25 = 1 floor + 20 onto A6
+ 4 onto A5, "each hand a free Inn-orbit of size 360."

The floor is the diagonal (x1=x2=x3=x4), a SET of size |A6| = 360. A set of 360
is not one Inn-orbit: two diagonal tuples (g,g,g,g), (h,h,h,h) are conjugate iff
g,h are conjugate, so the floor splits into one orbit per A6 conjugacy class.

This script computes the real decomposition of the beta-hat-fixed set in A6:
every Inn-orbit (hand) with its size, its image order, and whether it is
diagonal (on the floor) or onto A6. The ledger either adds up or it doesn't.
"""
import sys, time, itertools
import numpy as np
from collections import Counter, defaultdict
from build_An import build_An

WORDS = {
    "conway": ([-1, 2, -1, 2, -1, 3, -2, -2, -1, 3, 3], 4),
    "kt":     ([-1, 2, 2, -3, -3, 2, 1, -2, -2, 3, -2, 3, -2], 4),
}


def apply_auto(X, moves, mul, inv, conj):
    for (i, eps) in moves:
        a = X[:, i].copy(); b = X[:, i + 1].copy()
        if eps > 0:
            na = conj[a, b]; nb = a
        else:
            na = b; nb = conj[inv[b], a]
        X[:, i] = na; X[:, i + 1] = nb
    return X


def subgroup_order(gens, mul, ident, size):
    inH = np.zeros(size, dtype=bool)
    H = [int(ident)]; inH[ident] = True
    frontier = [int(ident)]
    for g in gens:
        if not inH[g]:
            inH[g] = True; H.append(g); frontier.append(g)
    while frontier:
        a = frontier.pop()
        for b in gens:
            for c in (int(mul[a, b]), int(mul[b, a])):
                if not inH[c]:
                    inH[c] = True; H.append(c); frontier.append(c)
    return len(H)


def inn_orbit_set(tup, mul, inv, size):
    orb = set()
    for g in range(size):
        orb.add(tuple(int(mul[mul[g, x], inv[g]]) for x in tup))
    return orb


def canonical(orb):
    return min(orb)


def elems(n):
    def sign(p):
        seen = [False] * n; s = 1
        for i in range(n):
            if not seen[i]:
                j = i; l = 0
                while not seen[j]:
                    seen[j] = True; j = p[j]; l += 1
                s *= (-1) ** (l - 1)
        return s
    return [p for p in itertools.permutations(range(n)) if sign(p) == 1]


def ledger(name, n=6, verbose=True):
    size, mul, inv, conj, order = build_An(n)
    word, _ = WORDS[name]
    ident = int(np.where(order == 1)[0][0])
    moves = [(abs(g) - 1, 1 if g > 0 else -1) for g in word]

    # conjugacy classes by representative
    classes = {}
    for b in range(size):
        rep = min(int(conj[a, b]) for a in range(size))
        classes.setdefault(rep, []).append(b)

    t0 = time.time()
    # orbit canonical -> (representative tuple, orbit)
    orbits = {}
    for rep, members in sorted(classes.items(), key=lambda kv: -len(kv[1])):
        m = len(members)
        if m == 1:
            continue
        mem = np.array(members, dtype=np.int64)
        g3 = np.repeat(mem, m); g4 = np.tile(mem, m)
        for x2 in mem:
            A = np.zeros((m * m, 4), dtype=np.int64)
            A[:, 0] = rep; A[:, 1] = x2; A[:, 2] = g3; A[:, 3] = g4
            mask = np.all(apply_auto(A.copy(), moves, mul, inv, conj) == A, axis=1)
            for r in np.nonzero(mask)[0]:
                tup = (rep, int(x2), int(g3[r]), int(g4[r]))
                orb = inn_orbit_set(tup, mul, inv, size)
                c = canonical(orb)
                if c not in orbits:
                    orbits[c] = orb

    # tally
    total = 0
    by_img_order = defaultdict(int)        # orbit count by image order
    by_size = defaultdict(int)             # orbit count by orbit size
    diag_orbits = []                       # orbits on the floor (diagonal)
    onto_orbits = []                       # orbits onto A6 (image order = size)
    img_orbit_sizes = defaultdict(list)    # image order -> [orbit sizes]
    for c, orb in orbits.items():
        tup = orb_to_rep(orb, c)
        im = subgroup_order(list(tup), mul, ident, size)
        osz = len(orb)
        total += osz
        by_img_order[im] += 1
        by_size[osz] += 1
        img_orbit_sizes[im].append(osz)
        if all(x == tup[0] for x in tup):
            diag_orbits.append((osz, im))
        if im == size:
            onto_orbits.append((osz, c))

    if verbose:
        print(f"== {name} in A_{n} ==  ({time.time()-t0:.1f}s)")
        print(f"  |Hom| (total fixed tuples) = {total}")
        print(f"  number of Inn-orbits (hands) = {len(orbits)}")
        print(f"  hands by image order: {dict(sorted(by_img_order.items()))}")
        print(f"  hands by orbit size:  {dict(sorted(by_size.items()))}")
        print(f"  diagonal (floor) orbits: {len(diag_orbits)}  sizes={sorted(s for s,_ in diag_orbits)}")
        print(f"  onto-A{n} hands (image order {size}): {len(onto_orbits)}")
        print(f"  free (size {size}) orbits: {sum(1 for s in by_size if s==size)}")
    return total, orbits, by_img_order, by_size, diag_orbits


def orb_to_rep(orb, canonical):
    # any element of the orbit is a valid representative for subgroup_order
    return next(iter(orb))


if __name__ == "__main__":
    for name in ["conway", "kt"]:
        ledger(name, 6)

def identity_check(n=6):
    size, mul, inv, conj, order = build_An(n)
    ident = int(np.where(order == 1)[0][0])
    # identity tuple (e,e,e,e) is always beta-hat-fixed; orbit size 1
    return ident

if __name__ == "__main__" and "--full" in sys.argv:
    import sys
    size, mul, inv, conj, order = build_An(6)
    ident = int(np.where(order == 1)[0][0])
    for name in ["conway", "kt"]:
        total, orbits, by_img, by_size, diag = ledger(name, 6, verbose=False)
        # add the identity tuple
        full_total = total + 1
        print(f"{name}: fixed tuples (incl identity) = {full_total}, orbits = {len(orbits)+1}")
        print(f"   floor (diagonal) orbits incl identity = {len(diag)+1}")
        # free orbits = size 360
        free = sum(v for k,v in by_size.items() if k==360)
        print(f"   free (size-360) hands = {free}")

def detail(name, n=6):
    import itertools
    size, mul, inv, conj, order = build_An(n)
    word, _ = WORDS[name]
    ident = int(np.where(order == 1)[0][0])
    moves = [(abs(g)-1, 1 if g>0 else -1) for g in word]
    def sign(p):
        seen=[False]*n; s=1
        for i in range(n):
            if not seen[i]:
                j=i; l=0
                while not seen[j]:
                    seen[j]=True; j=p[j]; l+=1
                s *= (-1)**(l-1)
        return s
    elems=[p for p in itertools.permutations(range(n)) if sign(p)==1]
    classes={}
    for b in range(size):
        rep=min(int(conj[a,b]) for a in range(size))
        classes.setdefault(rep,[]).append(b)
    orbits={}
    for rep,members in sorted(classes.items(), key=lambda kv:-len(kv[1])):
        m=len(members)
        if m==1: continue
        mem=np.array(members,dtype=np.int64)
        g3=np.repeat(mem,m); g4=np.tile(mem,m)
        for x2 in mem:
            A=np.zeros((m*m,4),dtype=np.int64)
            A[:,0]=rep; A[:,1]=x2; A[:,2]=g3; A[:,3]=g4
            mask=np.all(apply_auto(A.copy(),moves,mul,inv,conj)==A,axis=1)
            for r in np.nonzero(mask)[0]:
                tup=(rep,int(x2),int(g3[r]),int(g4[r]))
                orb=inn_orbit_set(tup,mul,inv,size)
                c=canonical(orb)
                if c not in orbits: orbits[c]=orb
    rows=[]
    for c,orb in orbits.items():
        tup=next(iter(orb))
        im=subgroup_order(list(tup),mul,ident,size)
        osz=len(orb)
        el=tuple(int(conj[0,0])*0 for _ in range(1))  # placeholder
        # meridian = class of tup[0]; get element order of the representative
        mer=order[tup[0]]
        diag=all(x==tup[0] for x in tup)
        rows.append((im,osz,mer,diag,tup))
    return rows

if __name__ == "__main__" and "--detail" in sys.argv:
    for name in ["conway","kt"]:
        rows=detail(name,6)
        from collections import Counter
        # group by (image order, free?, meridian order)
        print(f"== {name} A6 hands ==")
        cnt=Counter()
        for im,osz,mer,diag,tup in rows:
            kind = "floor" if diag else ("onto" if im==360 else "A5")
            cnt[(kind, im, osz, mer)] += 1
        for k in sorted(cnt, key=lambda k:(k[0],k[3],k[1])):
            print(f"   {k[0]:5s} img={k[1]:4d} size={k[2]:4d} mer-order={k[3]}  x{cnt[k]}")
