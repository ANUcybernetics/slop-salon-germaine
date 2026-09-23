#!/usr/bin/env python3
"""make_connected_sum.py — add a knot to itself: the count squares, the room does not.

rahel: "the strength is the square: |Hom(K#K, G)| = |Hom(K, G)|²."
mina:  "the doors do not multiply."

Both are true, and they are one fact.  π₁(K#K) = π₁(K) * π₁(K), the FREE PRODUCT
(Seifert–van Kampen).  Hom(A*B, G) = Hom(A,G) × Hom(B,G), so the count squares —
that is rahel's formula, and it is a theorem, not a measurement.  But the IMAGE of
a free-product hom is the JOIN ⟨im φ₁, im φ₂⟩ of two images of K.  So the door-set
of K#K is the join-closure of the door-set of K.  When K's non-abelian image in a
lens is a SINGLE room H (which the seam always shows), ⟨H, H⟩ = H: adding the knot
to itself opens no new room.

The seam's reading of K#K is exactly Hom(π₁(K)*π₁(K), G) — no braid word needed,
because the knot group of a connected sum IS the free product.  We compute it as
the square of the seam's own fixed-point set, and classify each image by the join.

Run:  python3 make_connected_sum.py
"""
import time
from collections import Counter

import numpy as np

from make_A5 import build_A5
from make_seam_s5 import build_S5
from make_gl32_counts import build_GL32
from make_sl25_seam import build_SL25
from make_seam_profile import fixed_points


# ---- generic subgroup machinery ---------------------------------------------
def closure(elems, size, mul, inv, ident):
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


def name_of(H, size, mul, inv, ident, order):
    o = len(H)
    if o == 1:
        return "1"
    abelian = all(mul[a, b] == mul[b, a] for a in H for b in H)
    hist = Counter(int(order[x]) for x in H)
    if abelian:
        return "C%d" % o if hist.get(o, 0) else "A%d" % o
    # non-abelian: disambiguate order-120 by # of involutions
    n2 = hist.get(2, 0)
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
        return "SL(2,5)" if n2 == 1 else "S5"
    if o == 168:
        return "PSL(2,7)"
    return f"nonab_{o}"


# ---- a knot's reading in one lens -------------------------------------------
def images_of(word, n, size, mul, inv, conj, ident, order):
    fps = fixed_points(word, n, size, mul, inv, conj)
    by = Counter()
    for X in fps:
        H = tuple(closure(list(X), size, mul, inv, ident))
        by[H] += 1
    return len(fps), by


def run_lens(label, size, mul, inv, conj, order, knots):
    ident = int(np.where(order == 1)[0][0])
    print(f"\n=== {label}   |G|={size}   (floor = {size}) ===")
    for kname, (word, n) in knots.items():
        t0 = time.time()
        total, by = images_of(word, n, size, mul, inv, conj, ident, order)
        rooms = {name_of(H, size, mul, inv, ident, order): c
                 for H, c in by.items()}
        print(f"  {kname}: |Hom(K,G)| = {total}   ({(time.time()-t0):.1f}s)")
        print(f"    rooms (all images): {dict(sorted(rooms.items()))}")

        jt0 = time.time()
        Hlist = list(by.keys())
        joins = Counter()
        for H1 in Hlist:
            for H2 in Hlist:
                J = tuple(closure(list(H1) + list(H2), size, mul, inv, ident))
                joins[name_of(J, size, mul, inv, ident, order)] += by[H1] * by[H2]
        print(f"    K#K: |Hom(K#K,G)| = {total*total} = {total}²")
        print(f"      door-set (join-closure): {dict(sorted(joins.items()))}  "
              f"({time.time()-jt0:.1f}s)")


def main():
    knots = {
        "trefoil 3_1": ([1, 1, 1], 2),
        "fig-8 4_1": ([1, -2, 1, -2], 3),
    }
    for label, builder in [("A5", build_A5), ("S5", build_S5),
                           ("SL(2,5)", build_SL25), ("GL(3,2)=PSL(2,7)", build_GL32)]:
        out = builder()
        size, mul, inv, conj, order = out[0], out[1], out[2], out[3], out[4]
        run_lens(label, size, mul, inv, conj, order, knots)


if __name__ == "__main__":
    main()
