#!/usr/bin/env python3
"""make_sl25_seam.py — does the seam read SL(2,5)?

The seam (Conway, KT) is a Δ=1 knot, so π₁' is perfect and every non-abelian
image of π₁ is non-solvable.  Up to now the seam has only been read into *simple*
lenses (A₅, PSL(2,7)), and "whole or not at all" was phrased about simple rooms.
SL(2,5) is the sharp test of that: perfect, order 120, centre Z₂, quotient A₅ —
but NOT simple.  If the seam surjects onto it, "the seam reads simple rooms only"
is false; it reads *non-solvable* rooms.  If it does not, "whole or not at all"
survives even against a non-simple perfect group.

Run:  python3 make_sl25_seam.py    (n=4 counts take ~1 min each)
"""
import itertools
import time
from collections import Counter

import numpy as np

from make_seam_profile import fixed_points
from make_seam_s5 import build_S5


# ---- SL(2,5) as tables ------------------------------------------------------
def build_SL25():
    def matmul(A, B):
        a, b, c, d = A
        e, f, g, h = B
        return ((a * e + b * g) % 5, (a * f + b * h) % 5,
                (c * e + d * g) % 5, (c * f + d * h) % 5)

    elems = [A for A in itertools.product(range(5), repeat=4)
             if (A[0] * A[3] - A[1] * A[2]) % 5 == 1]
    idx = {e: i for i, e in enumerate(elems)}
    size = len(elems)
    ident = idx[(1, 0, 0, 1)]
    mul = np.zeros((size, size), dtype=np.int64)
    for a in range(size):
        for b in range(size):
            mul[a, b] = idx[matmul(elems[a], elems[b])]
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
        o = 1
        cur = a
        while cur != ident:
            cur = mul[cur, a]
            o += 1
        order[a] = o
    return size, mul, inv, conj, order, elems


# ---- subgroup naming --------------------------------------------------------
def subgroup_closure(elems, size, mul, inv, ident):
    gen = sorted(set(elems))
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


def name_subgroup(elems, size, mul, inv, ident, order):
    """Name a subgroup of SL(2,5) by order + structure."""
    H = subgroup_closure(elems, size, mul, inv, ident)
    o = len(H)
    if o == 1:
        return "1"
    abelian = all(mul[a, b] == mul[b, a] for a in H for b in H)
    hist = Counter(int(order[x]) for x in H)
    if abelian:
        return "C%d" % o if hist.get(o, 0) else "A%d" % o
    # order-2 element count: SL(2,5) has exactly 1 (central -I); S5 has 25.
    n2 = hist.get(2, 0)
    if o == 6:
        return "S3"
    if o == 12:
        return "A4"
    if o == 24:
        return "2.A4 (binary tetra)"
    if o == 40:
        return "2.D10" if n2 == 1 else "nonab_40"
    if o == 60:
        return "A5"
    if o == 120:
        return "SL(2,5)" if n2 == 1 else "S5"
    return f"nonab_{o}"


# ---- the seam ---------------------------------------------------------------
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
            by[name_subgroup(list(X), size, mul, inv, ident, order)] += 1
        nonab = {k: v for k, v in by.items() if not (k.startswith("C") or k == "1")}
        abel = {k: v for k, v in by.items() if k.startswith("C") or k == "1"}
        print(f"  {name}: total={len(fps)}  ({(time.time()-t0):.1f}s)")
        print(f"    non-abelian images: {nonab}")
        print(f"    abelian/cyclic    : {abel}")


def main():
    size, mul, inv, conj, order, elems = build_SL25()
    print("|SL(2,5)| =", size)
    run("SL(2,5)", size, mul, inv, conj, order)
    # sanity: the floor for the unknot should be exactly |G|, all cyclic.
    fps0 = fixed_points([], 1, size, mul, inv, conj)
    print(f"\n  unknot (Z): total={len(fps0)} (should be {size})")


if __name__ == "__main__":
    main()
