#!/usr/bin/env python3
"""verify_seam.py — what does the seam (Conway, KT) actually read?

rahel's correction: "correct Wirtinger puts the seam ON THE FLOOR for A₅, S₅,
PSL(2,7): |Hom|=|G|, every image cyclic. the aperture isn't A₅ — nor 168."

I verified (verify_braid_presentation.py) that the braid-closure model
<x_i = β̂(x_i)> IS the knot group for the trefoil and fig-8 (it matches explicit
presentations exactly).  So if the Conway/KT braid words are right, this model
gives their correct knot-group reads.  Test rahel's claim directly: count
|Hom(seam, G)| for G in {A4, A5, S5, GL(3,2)} and classify the images — on the
floor (all cyclic, count = |G|) or not?

Run:  python3 verify_seam.py   (n=4 counts into GL(3,2)/S5 take a few min)
"""
import time
from collections import Counter

import numpy as np

from make_A5 import build_A5
from make_seam_s5 import build_S5
from make_gl32_counts import build_GL32
from make_seam_profile import fixed_points


# ---- A4 (inline) ------------------------------------------------------------
def build_A4():
    import itertools
    elems = [p for p in itertools.permutations(range(4)) if perm_sign(p) == 1]
    idx = {e: i for i, e in enumerate(elems)}
    size = len(elems)
    ident = idx[tuple(range(4))]
    mul = np.zeros((size, size), dtype=np.int64)
    for a in range(size):
        for b in range(size):
            mul[a, b] = idx[perm_mul(elems[a], elems[b])]
    inv = np.zeros(size, dtype=np.int64)
    for a in range(size):
        for b in range(size):
            if mul[a, b] == ident:
                inv[a] = b
    conj = np.zeros((size, size), dtype=np.int64)
    for a in range(size):
        for b in range(size):
            conj[a, b] = mul[mul[a, b], inv[a]]
    order = np.zeros(size, dtype=np.int64)
    for a in range(size):
        order[a] = perm_order(elems[a])
    return size, mul, inv, conj, order


def perm_mul(p, q):
    return tuple(p[q[i]] for i in range(len(p)))


def perm_inv(p):
    r = [0] * len(p)
    for i in range(len(p)):
        r[p[i]] = i
    return tuple(r)


def perm_order(p):
    n = len(p)
    seen = [False] * n
    o = 1
    for i in range(n):
        if not seen[i]:
            j = i
            l = 0
            while not seen[j]:
                seen[j] = True
                j = p[j]
                l += 1
            o = o * l // __import__("math").gcd(o, l)
    return o


def perm_sign(p):
    seen = [False] * len(p)
    s = 1
    for i in range(len(p)):
        if not seen[i]:
            j = i
            l = 0
            while not seen[j]:
                seen[j] = True
                j = p[j]
                l += 1
            s *= (-1) ** (l - 1)
    return s


# ---- classify an image subgroup of a generic group --------------------------
def subgroup_closure(elems, size, mul, inv, ident):
    gen = sorted(set(elems))
    if not gen:
        return [ident]
    H = {ident}
    frontier = [ident]
    for g in gen:
        if g not in H:
            H.add(g)
            frontier.append(g)
    while frontier:
        a = frontier.pop()
        for b in gen:
            for c in (mul[a, b], mul[b, a], inv[b]):
                if c not in H:
                    H.add(c)
                    frontier.append(c)
    return sorted(H)


def classify(elems, size, mul, inv, ident, order):
    """Name a subgroup by order + structure (generic version)."""
    H = subgroup_closure(elems, size, mul, inv, ident)
    o = len(H)
    if o == 1:
        return "1"
    abelian = all(mul[a, b] == mul[b, a] for a in H for b in H)
    hist = Counter(int(order[x]) for x in H)
    if abelian:
        # cyclic if some element has order == |H|
        return "C%d" % o if hist.get(o, 0) else "A%d" % o
    # non-abelian small ones
    if o == 6:
        return "S3"
    if o == 10:
        return "D5"
    if o == 12:
        return "A4"
    if o == 20:
        return "F20"
    if o == 24:
        return "S4"
    if o == 60:
        return "A5"
    if o == 120:
        return "S5"
    if o == 168:
        return "PSL(2,7)"
    return f"nonabel_{o}"


SEAM = {
    "Conway 11n34": ([-1, 2, -1, 2, -1, 3, -2, -2, -1, 3, 3], 4),
    "KT 11n42": ([-1, 2, 2, -3, -3, 2, 1, -2, -2, 3, -2, 3, -2], 4),
}


def run(label, size, mul, inv, conj, order):
    ident = int(np.where(order == 1)[0][0])
    print(f"\n=== {label}  |G|={size}  (floor = {size}) ===")
    for name, (word, n) in SEAM.items():
        t0 = time.time()
        fps = fixed_points(word, n, size, mul, inv, conj)
        by = Counter()
        for X in fps:
            by[classify(list(X), size, mul, inv, ident, order)] += 1
        # split abelian vs non-abelian
        nonab = {k: v for k, v in by.items() if not (k.startswith("C") or k == "1")}
        abel = {k: v for k, v in by.items() if k.startswith("C") or k == "1"}
        print(f"  {name}: total={len(fps)}  ({(time.time()-t0):.1f}s)")
        print(f"    non-abelian images: {nonab}")
        print(f"    abelian/cyclic    : {abel}")


def main():
    for label, builder in [("A4", build_A4), ("A5", build_A5),
                           ("S5", build_S5), ("GL(3,2)=PSL(2,7)", build_GL32)]:
        size, mul, inv, conj, order = builder()
        run(label, size, mul, inv, conj, order)


if __name__ == "__main__":
    main()
