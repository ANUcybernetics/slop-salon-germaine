#!/usr/bin/env python3
"""reach8_reduced.py — A_8 door sweep with the centralizer-orbit reduction.

β̂ is the Artin action of the braid word on the tuple of images, and it is
conjugation-equivariant: β̂(hXh⁻¹) = h β̂(X) h⁻¹.  So the β̂-fixed tuples with
x1 pinned to `a` are invariant under the diagonal conjugation action of
H = C(a) ∩ C(x2) on (x3,x4): one fixed pair drags its whole H-orbit along.  We
enumerate one rep per H-orbit of (x3,x4) instead of the full |class|² grid.

This is the "faster fixed-point finder" the notes keep asking for.  Validated
against the known answer for 3·2²·1 (Conway 7 fixed / 1 transitive / surj; KT
5 fixed / 0 transitive).

Run: python3 reach8_reduced.py [class-name ...]
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


def conj_orbits(elements_sorted, group, cache):
    """[(rep, stabilizer), ...] for `elements_sorted` (pre-sorted!) under conjugation
    by `group` (list).  `cache` is keyed by the group so repeated stabilizers are free."""
    gkey = tuple(group)
    hit = cache.get(gkey)
    if hit is not None: return hit
    reps = []; seen = set()
    pe = pinv
    for x in elements_sorted:
        if x in seen: continue
        orb = set(); stab = []
        for h in group:
            y = pmul(pmul(h, x), pe(h))
            orb.add(y)
            if y == x: stab.append(h)
        reps.append((x, stab))
        seen |= orb
    cache[gkey] = reps
    return reps


def scan_reduced(word, a, cls, A8, label):
    moves = [(abs(g)-1, 1 if g > 0 else -1) for g in word]
    cls = sorted(cls); m = len(cls)
    Ca = list(centralizer(a, A8))
    cache = {}
    t0 = time.time()
    total_fixed = 0; trans = 0; maxord = 0; surj = False; surj_tup = None
    x2_reps = conj_orbits(cls, Ca, cache)
    nr = len(x2_reps)
    for k, (x2, H) in enumerate(x2_reps):
        # the stabilizer of x2 under C(a) IS H = C(a) ∩ C(x2) — no recompute
        u_reps = conj_orbits(cls, H, cache)
        pairs = []
        for (u, stab) in u_reps:
            for (v, _) in conj_orbits(cls, stab, cache):
                pairs.append((u, v))
        P = np.array(pairs, dtype=np.int64)
        R = len(pairs)
        X0 = np.zeros((R, 4, N), dtype=np.int8)
        X0[:, 0] = np.array(a, dtype=np.int8)
        X0[:, 1] = np.array(x2, dtype=np.int8)
        X0[:, 2] = P[:, 0]; X0[:, 3] = P[:, 1]
        X = X0.copy(); apply_auto_vec(X, moves)
        mask = np.all(X == X0, axis=(1, 2))
        idxs = np.nonzero(mask)[0]
        total_fixed += len(idxs)
        for r in idxs:
            tup = (a, x2, tuple(P[r, 0]), tuple(P[r, 1]))
            if not transitive(tup): continue
            trans += 1
            o = subgroup_order(list(tup))
            if o > maxord: maxord = o
            if o == WANT:
                surj = True; surj_tup = tup; break
        if k % 40 == 0 or surj:
            print(f"    [{label}] x2-rep {k+1}/{nr}  fixed={total_fixed} trans={trans} "
                  f"max={maxord} ({time.time()-t0:.0f}s)", flush=True)
        if surj: break
    print(f"    {label}: |class|={m}, x2-reps={nr}: fixed={total_fixed}, "
          f"trans={trans}, max|<x1..x4>|={maxord}, surj_A8={surj}"
          + (f"  x1={cyc(a)}" if surj_tup else "") + f"  ({time.time()-t0:.1f}s)", flush=True)
    return dict(fixed=total_fixed, trans=trans, maxord=maxord, surj=surj)


def main():
    A8 = [p for p in itertools.permutations(range(N)) if psign(p) == 1]
    which = sys.argv[1:] or ["3 2^2 1"]
    for name in which:
        if name not in CLASSES: continue
        a = CLASSES[name]
        cls = class_of(a, A8)
        print(f"\n=== {name} (|class|={len(cls)}, ord={porder(a)}, {cyc(a)}) ===", flush=True)
        for label, word in (("Conway", CONWAY), ("KT", KT)):
            scan_reduced(word, a, cls, A8, label)


if __name__ == "__main__":
    main()
