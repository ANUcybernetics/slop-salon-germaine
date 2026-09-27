#!/usr/bin/env python3
"""solve_a9.py — experiment: how is (x3,x4) determined by (x1,x2)?

We want to SOLVE the beta_hat-fixed condition instead of sweeping m^2.
The one-solution datum: for a fixed (x1,x2) there is exactly one beta_hat-fixed
(x3,x4) in the 3^3 class.  This script probes the structure to find the map.
"""
import itertools, time
import numpy as np

CONWAY = [-1, 2, -1, 2, -1, 3, -2, -2, -1, 3, 3]
KT = [-1, 2, 2, -3, -3, 2, 1, -2, -2, 3, -2, 3, -2]


def pmul(p, q): return tuple(p[q[i]] for i in range(len(p)))
def pinv(p):
    r = [0] * len(p)
    for i in range(len(p)): r[p[i]] = i
    return tuple(r)
def psign(p):
    n = len(p); seen = [False] * n; s = 1
    for i in range(n):
        if not seen[i]:
            j = i; l = 0
            while not seen[j]:
                seen[j] = True; j = p[j]; l += 1
            s *= (-1) ** (l - 1)
    return s
def cyc(p):
    n = len(p); seen = [False] * n; parts = []
    for i in range(n):
        if not seen[i]:
            c = []; j = i
            while not seen[j]:
                seen[j] = True; c.append(j); j = p[j]
            if len(c) > 1:
                parts.append("(" + " ".join(str(x) for x in c) + ")")
    return "".join(parts) if parts else "()"


def from_cycles(cycles, n=9):
    p = list(range(n))
    for c in cycles:
        for k in range(len(c)):
            p[c[k]] = c[(k + 1) % len(c)]
    return tuple(p)


def apply_auto(tup, word):
    X = list(tup)
    for g in word:
        i = abs(g) - 1
        a, b = X[i], X[i + 1]
        if g > 0:
            X[i] = pmul(pmul(a, b), pinv(a)); X[i + 1] = a
        else:
            X[i] = b; X[i + 1] = pmul(pinv(b), pmul(a, b))
    return tuple(X)


def class_of(a, A9):
    return set(pmul(pmul(g, a), pinv(g)) for g in A9)
def centralizer(a, A9):
    return set(g for g in A9 if pmul(pmul(g, a), pinv(g)) == a)
def orbit_reps(a, cls, A9):
    C = centralizer(a, A9); seen = set(); reps = []
    for x in sorted(cls):
        if x in seen: continue
        reps.append(x)
        seen |= set(pmul(pmul(h, x), pinv(h)) for h in C)
    return reps, len(C)


def vpmul(A, B): return np.take_along_axis(A, B, axis=1)
def vpinv(A): return np.argsort(A, axis=1)
def apply_auto_vec(X, moves):
    for (i, eps) in moves:
        a = X[:, i].copy(); b = X[:, i + 1].copy()
        if eps > 0:
            na = vpmul(vpmul(a, b), vpinv(a)); nb = a
        else:
            na = b; nb = vpmul(vpinv(b), vpmul(a, b))
        X[:, i] = na; X[:, i + 1] = nb
    return X


def main():
    t0 = time.time()
    A9 = [p for p in itertools.permutations(range(9)) if psign(p) == 1]
    print(f"|A_9|={len(A9)}  ({time.time()-t0:.1f}s)")

    # 3^3 class rep
    a = from_cycles([(0, 1, 2), (3, 4, 5), (6, 7, 8)])
    cls = sorted(class_of(a, A9))
    m = len(cls)
    print(f"3^3 class: |class|={m}")
    cls_arr = np.array(cls, dtype=np.int32)
    cls_arr2 = np.array(cls, dtype=np.int64)

    # KT witness
    kt33 = (from_cycles([(0, 1, 2), (3, 4, 5), (6, 7, 8)]),
            from_cycles([(0, 1, 3), (2, 6, 5), (4, 8, 7)]),
            from_cycles([(0, 4, 1), (2, 5, 6), (3, 8, 7)]),
            from_cycles([(0, 2, 6), (1, 7, 8), (3, 4, 5)]))
    x1, x2, x3w, x4w = kt33
    print("KT witness:", [cyc(p) for p in kt33])
    print("beta_hat-fixed?", apply_auto(kt33, KT) == kt33)
    print("beta_hat(x1x2x3x4) = product?",
          apply_auto((pmul(pmul(x1,x2),pmul(x3w,x4w)),)*1 if False else kt33, KT) == kt33)

    # Experiment 1: fix x1,x2.  For each x3 in class, count x4 that fix.
    moves = [(abs(g) - 1, 1 if g > 0 else -1) for g in KT]
    x1a = np.array(x1, dtype=np.int32); x2a = np.array(x2, dtype=np.int32)
    g3 = np.repeat(np.arange(m), m).astype(np.int64)
    g4 = np.tile(np.arange(m), m).astype(np.int64)
    # build rows (x1,x2,x3,x4) for all (x3,x4) pairs
    X0 = np.zeros((m * m, 4, 9), dtype=np.int32)
    X0[:, 0] = x1a
    X0[:, 1] = x2a
    X0[:, 2] = cls_arr[g3]
    X0[:, 3] = cls_arr[g4]
    X = X0.copy()
    apply_auto_vec(X, moves)
    mask = np.all(X == X0, axis=(1, 2))
    idxs = np.nonzero(mask)[0]
    print(f"\nfixed (x3,x4) pairs for this (x1,x2): {len(idxs)}")
    for r in idxs[:20]:
        print(f"   x3={cyc(cls[g3[r]])}  x4={cyc(cls[g4[r]])}")
    # group by x3
    from collections import defaultdict
    byx3 = defaultdict(list)
    for r in idxs:
        byx3[cls[g3[r]]].append(cls[g4[r]])
    print(f"distinct x3 values with a fixed partner: {len(byx3)}")
    print(f"x3->x4 multiplicity histogram:",
          sorted((len(v) for v in byx3.values())))
    # does each x3 have exactly one x4?
    print(f"all x3 have exactly 1 x4? {all(len(v)==1 for v in byx3.values())}")

    # Also: is the x3->x4 map injective/consistent?
    print(f"x3->x4 distinct x4 count: {len(set(v[0] for v in byx3.values()))}")


if __name__ == "__main__":
    main()
