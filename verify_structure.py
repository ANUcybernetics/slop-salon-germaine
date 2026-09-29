#!/usr/bin/env python3
"""verify_structure.py — is (x3,x4) determined by (x1,x2) for a beta-hat-fixed tuple?

For a fixed meridian class C, enumerate ALL beta-hat-fixed tuples (x1,x2,x3,x4)
with x1=a pinned, and group them by (x1,x2).  If every (x1,x2) has exactly one
(x3,x4), then the fixed set is a GRAPH over (x1,x2), and the m^2 grid is hugely
wasteful — we only need to find the (x1,x2) pairs that admit a solution.

Run: python3 verify_structure.py <class-name>
"""
import itertools, time, sys
import numpy as np

N = 8; WANT = 20160
CONWAY = [-1, 2, -1, 2, -1, 3, -2, -2, -1, 3, 3]
KT = [-1, 2, 2, -3, -3, 2, 1, -2, -2, 3, -2, 3, -2]
CLASSES = {
    "3^2 1^2": (1, 2, 0, 4, 5, 3, 6, 7),
    "3 2^2 1": (1, 2, 0, 4, 3, 6, 5, 7),
    "4 2 1^2": (1, 2, 3, 0, 5, 4, 6, 7),
    "4 4":     (1, 2, 3, 0, 5, 6, 7, 4),
    "5 1^3":   (1, 2, 3, 4, 0, 5, 6, 7),
    "5 3":     (1, 2, 3, 4, 0, 6, 7, 5),
    "6 2":     (1, 2, 3, 4, 5, 0, 7, 6),
    "7 1":     (1, 2, 3, 4, 5, 6, 0, 7),
}


def pmul(p, q): return tuple(p[q[i]] for i in range(len(p)))
def pinv(p):
    r = [0]*len(p)
    for i in range(len(p)): r[p[i]] = i
    return tuple(r)
def psign(p):
    n = len(p); seen = [False]*n; s = 1
    for i in range(n):
        if not seen[i]:
            j = i; l = 0
            while not seen[j]: seen[j] = True; j = p[j]; l += 1
            s *= (-1)**(l-1)
    return s
def cyc(p):
    n = len(p); seen = [False]*n; parts = []
    for i in range(n):
        if not seen[i]:
            c = []; j = i
            while not seen[j]: seen[j] = True; c.append(j); j = p[j]
            if len(c) > 1: parts.append("(" + " ".join(str(x) for x in c) + ")")
    return "".join(parts) if parts else "()"
def porder(p):
    import math
    n = len(p); seen = [False]*n; o = 1
    for i in range(n):
        if not seen[i]:
            j = i; l = 0
            while not seen[j]: seen[j] = True; j = p[j]; l += 1
            o = o*l//math.gcd(o, l)
    return o
def vpmul(A, B): return np.take_along_axis(A, B, axis=1)
def vpinv(A): return np.argsort(A, axis=1)
def apply_auto_vec(X, moves):
    for (i, eps) in moves:
        a = X[:, i].copy(); b = X[:, i+1].copy()
        if eps > 0:
            na = vpmul(vpmul(a, b), vpinv(a)); nb = a
        else:
            na = b; nb = vpmul(vpinv(b), vpmul(a, b))
        X[:, i] = na; X[:, i+1] = nb
    return X
def transitive(gen):
    n = len(gen[0]); adj = [set() for _ in range(n)]
    for g in gen:
        for i in range(n):
            adj[i].add(g[i]); adj[g[i]].add(i)
    seen = {0}; front = [0]
    while front:
        a = front.pop()
        for b in adj[a]:
            if b not in seen: seen.add(b); front.append(b)
    return len(seen) == n
def subgroup_order(gen, cap=WANT):
    gen = list(set(gen)); n = len(gen[0]); H = set(gen); H.add(tuple(range(n)))
    front = list(H)
    while front:
        a = front.pop()
        for b in gen:
            for c in (pmul(a, b), pmul(b, a), pinv(b)):
                if c not in H:
                    H.add(c); front.append(c)
                    if len(H) > cap: return -1
    return len(H)
def class_of(a, A8): return set(pmul(pmul(g, a), pinv(g)) for g in A8)
def centralizer(a, A8): return set(g for g in A8 if pmul(pmul(g, a), pinv(g)) == a)
def orbit_reps(a, cls, A8):
    C = centralizer(a, A8); seen = set(); reps = []
    for x in sorted(cls):
        if x in seen: continue
        reps.append(x)
        seen |= set(pmul(pmul(h, x), pinv(h)) for h in C)
    return reps, len(C)


def main():
    t0 = time.time()
    A8 = [p for p in itertools.permutations(range(N)) if psign(p) == 1]
    which = sys.argv[1] or "3 2^2 1"
    a = CLASSES[which]
    cls = class_of(a, A8)
    m = len(cls)
    print(f"class {which}: |class|={m}, order={porder(a)}, {cyc(a)}")
    for label, word in (("Conway", CONWAY), ("KT", KT)):
        moves = [(abs(g)-1, 1 if g > 0 else -1) for g in word]
        reps, csz = orbit_reps(a, cls, A8)
        mem = sorted(cls); mem_arr = np.array(mem, dtype=np.int64)
        g3 = np.repeat(np.arange(m, dtype=np.int64), m)
        g4 = np.tile(np.arange(m, dtype=np.int64), m)
        from collections import defaultdict
        by_pair = defaultdict(list)
        total_fixed = 0; surj = False
        t1 = time.time()
        for x2 in reps:
            X0 = np.zeros((m*m, 4, N), dtype=np.int8)
            X0[:, 0] = np.array(a, dtype=np.int8)
            X0[:, 1] = np.array(x2, dtype=np.int8)
            X0[:, 2] = mem_arr[g3]; X0[:, 3] = mem_arr[g4]
            X = X0.copy(); apply_auto_vec(X, moves)
            mask = np.all(X == X0, axis=(1, 2))
            idxs = np.nonzero(mask)[0]
            total_fixed += len(idxs)
            for r in idxs:
                tup = (a, x2, mem[g3[r]], mem[g4[r]])
                by_pair[(a, x2)].append(tup[2:])
                if transitive(tup):
                    o = subgroup_order(list(tup))
                    if o == WANT: surj = True
        print(f"  {label}: fixed={total_fixed}, distinct (x1,x2)={len(by_pair)}, "
              f"surj_A8={surj}, multi={[len(v) for v in by_pair.values() if len(v)>1]} ({time.time()-t1:.0f}s)")
        print(f"    #(x1,x2) with exactly 1 (x3,x4): "
              f"{sum(1 for v in by_pair.values() if len(v)==1)}/{len(by_pair)}")


if __name__ == "__main__":
    main()
