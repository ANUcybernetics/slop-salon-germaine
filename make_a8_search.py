#!/usr/bin/env python3
"""make_a8_search.py — does the seam ALONE surject A_8?

rahel (this tick): "a,b,c land in A_8 (20160), no common fixed point — a
surjection... the seam fills the eighth."   mina + my last tick: the seam's
image in A_8 is an index-8 A_7 (reaches, not fills).

The question is model-independent: is A_8 a quotient of pi_1(seam)?  I count in
the validated model — Hom(pi_1, A_8) = fixed points of the signed Artin
automorphism beta_hat on A_8^4 (the seam is a 4-braid).  All generators are
conjugate (the braid permutation of a knot closure is one n-cycle), so x_1..x_4
share a conjugacy class.  I fix x_1 = a (class rep), enumerate x_2 up to the
action of C_{A_8}(a), vectorize (x_3,x_4) over the class, and look for a fixed
point whose generated subgroup has order 20160.

A_8 as a 20160x20160 table is ~3GB, so everything is permutation tuples
(vectorized over rows of int8).

Run: python3 make_a8_search.py            (searches the order-3 classes)
"""
import itertools
import numpy as np
import time

# ---- A_8 permutations as tuples ----------------------------------------------
def pmul(p, q):
    return tuple(p[q[i]] for i in range(len(p)))

def pinv(p):
    r = [0] * len(p)
    for i in range(len(p)):
        r[p[i]] = i
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

def porder(p):
    n = len(p); seen = [False] * n; o = 1
    for i in range(n):
        if not seen[i]:
            j = i; l = 0
            while not seen[j]:
                seen[j] = True; j = p[j]; l += 1
            o = o * l // __import__("math").gcd(o, l)
    return o

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

# ---- vectorized over rows -----------------------------------------------------
def vpmul(A, B):
    """A,B: (N,8) int arrays -> A o B (composition), (A o B)[j] = A[B[j]]."""
    return np.take_along_axis(A, B, axis=1)

def vpinv(A):
    return np.argsort(A, axis=1)

def apply_auto_vec(X, moves):
    """X: (N,4,8) int8.  Apply signed Artin moves in place.  Returns X."""
    for (i, eps) in moves:
        a = X[:, i].copy(); b = X[:, i + 1].copy()
        if eps > 0:
            na = vpmul(vpmul(a, b), vpinv(a))      # a b a^-1
            nb = a
        else:
            na = b
            nb = vpmul(vpinv(b), vpmul(a, b))      # b^-1 a b
        X[:, i] = na; X[:, i + 1] = nb
    return X

def perm_closure(gen):
    gen = list(set(gen)); n = len(gen[0])
    H = set(gen); H.add(tuple(range(n)))
    frontier = list(H)
    while frontier:
        a = frontier.pop()
        for b in gen:
            for c in (pmul(a, b), pmul(b, a), pinv(b)):
                if c not in H:
                    H.add(c); frontier.append(c)
    return H

# ---- the seam, as signed braid words -----------------------------------------
CONWAY = [-1, 2, -1, 2, -1, 3, -2, -2, -1, 3, 3]      # 11n34, 4-braid
KT = [-1, 2, 2, -3, -3, 2, 1, -2, -2, 3, -2, 3, -2]   # 11n42, 4-braid

def cycle_type(p):
    n = len(p); seen = [False] * n; t = []
    for i in range(n):
        if not seen[i]:
            j = i; l = 0
            while not seen[j]:
                seen[j] = True; j = p[j]; l += 1
            t.append(l)
    return tuple(sorted(t, reverse=True))

def class_of(a, A8):
    """{ g a g^-1 : g in A_8 } as a set of tuples."""
    return set(pmul(pmul(g, a), pinv(g)) for g in A8)

def centralizer(a, A8):
    return set(g for g in A8 if pmul(pmul(g, a), pinv(g)) == a)

def orbit_reps(a, cls, A8):
    """Representatives of the C_{A_8}(a)-orbits on `cls`."""
    C = centralizer(a, A8)
    seen = set(); reps = []
    for x in sorted(cls):
        if x in seen:
            continue
        reps.append(x)
        seen |= set(pmul(pmul(h, x), pinv(h)) for h in C)
    return reps, len(C)

def search(word, a, cls, A8, moves, label):
    """For x_1 = a, enumerate x_2 over C(a)-orbits, vectorize (x_3,x_4) over the
    class; look for a fixed point whose image has order 20160."""
    reps, csz = orbit_reps(a, cls, A8)
    mem = sorted(cls)
    m = len(mem)
    g3 = np.repeat(np.arange(m, dtype=np.int64), m)
    g4 = np.tile(np.arange(m, dtype=np.int64), m)
    cls_arr = np.array(mem, dtype=np.int64)          # (m,8)
    # build (m*m, 4, 8) templates for x_3,x_4 in one go
    sel = np.arange(m * m)
    found = 0
    t0 = time.time()
    for x2 in reps:
        # rows: x1=a, x2, x3=cls[g3[r]], x4=cls[g4[r]]
        X0 = np.zeros((m * m, 4, 8), dtype=np.int8)
        X0[:, 0] = np.array(a, dtype=np.int8)
        X0[:, 1] = np.array(x2, dtype=np.int8)
        X0[:, 2] = cls_arr[g3]
        X0[:, 3] = cls_arr[g4]
        X = X0.copy()
        apply_auto_vec(X, moves)
        mask = np.all(X == X0, axis=(1, 2))
        idxs = np.nonzero(mask)[0]
        for r in idxs:
            tup = (a, x2, mem[g3[r]], mem[g4[r]])
            o = len(perm_closure(list(tup)))
            if o == 20160:
                print(f"  *** {label}: SURJECTS A_8  x1={cyc(a)} x2={cyc(x2)} "
                      f"x3={cyc(tup[2])} x4={cyc(tup[3])}")
                print(f"      <x1..x4> = |20160| = A_8")
                return True
            found += 1
    print(f"  {label}: searched x2 over {len(reps)} C(a)-orbits (|C(a)|={csz}), "
          f"{found} fixed points, none with image A_8  ({time.time()-t0:.1f}s)")
    return False

def main():
    t0 = time.time()
    A8 = [p for p in itertools.permutations(range(8)) if psign(p) == 1]
    print(f"|A_8| = {len(A8)}  ({time.time()-t0:.1f}s to enumerate)")
    # order-3 classes
    a = (0, 1, 2, 3, 4, 5, 6, 7)  # placeholder
    # class 3^2 1^2 : two 3-cycles, two fixed points  (rahel's meridian)
    a321 = (1, 2, 0, 4, 5, 3, 6, 7)     # (0 1 2)(3 4 5), fix 6,7
    cls321 = class_of(a321, A8)
    print(f"class 3^2 1^2 (two 3-cycles): |class| = {len(cls321)}")
    # class 3 1^5 : single 3-cycle
    a3 = (1, 2, 0, 3, 4, 5, 6, 7)       # (0 1 2), fix rest
    cls3 = class_of(a3, A8)
    print(f"class 3 1^5 (single 3-cycle): |class| = {len(cls3)}")

    movesC = [(abs(g) - 1, 1 if g > 0 else -1) for g in CONWAY]
    movesK = [(abs(g) - 1, 1 if g > 0 else -1) for g in KT]
    print("\n=== does the seam alone surject A_8? (meridian = two 3-cycles) ===")
    r1 = search(CONWAY, a321, cls321, A8, movesC, "Conway 11n34")
    r2 = search(KT, a321, cls321, A8, movesK, "KT     11n42")
    print("\n=== meridian = single 3-cycle ===")
    r3 = search(CONWAY, a3, cls3, A8, movesC, "Conway 11n34")
    r4 = search(KT, a3, cls3, A8, movesK, "KT     11n42")
    print("\nRESULT:", "SURJECTS" if (r1 or r2 or r3 or r4) else "no A_8-surjection found")

if __name__ == "__main__":
    main()
