#!/usr/bin/env python3
"""make_amalgam_sum.py — the CONNECTED SUM, amalgamated over the meridian.

mina's correction:  π₁(K#K) = π₁(K) *_{Z} π₁(K)  (amalgamated free product over
the meridian μ = x₁).  So Hom(K#K, G) is NOT the free square |Hom(K,G)|²; it is
  { (φ₁,φ₂) : φ₁(x₁) = φ₂(x₁) }
and the image of the sum-hom is  ⟨im φ₁, im φ₂⟩.

mina, fresh: "the sum opens the room the knot is blind to.  trefoil fills the
five, blind to the six; two of its fives, joined, fill the six.  12,960 in, from
none.  fig-8 fills the six, blind to the five; two of its images, joined, say the
five.  840 from none."

Verify it: read the fixed points of the braid closure, bucket by meridian, and
for each pair in the SAME meridian bucket compute the join.  Report the door-set
of K#K and the count of sum-homs landing on each room.

Run:  python3 /tmp/make_amalgam_sum.py
"""
import time
from collections import Counter

import numpy as np

from build_An import build_An
from make_seam_profile import fixed_points


def name_of(H, size, mul, inv, ident, order):
    o = len(H)
    if o == 1:
        return "1"
    abelian = all(mul[a, b] == mul[b, a] for a in H for b in H)
    hist = Counter(int(order[x]) for x in H)
    n2 = hist.get(2, 0)
    if abelian:
        if o == 3:
            return "C3"
        if o == 4:
            return "V4"
        if o == 5:
            return "C5"
        if o == 6:
            return "C6"
        return "C%d" % o
    # non-abelian
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
    if o == 36:
        return "3^2:4"
    if o == 60:
        return "A5"
    if o == 120:
        return "SL(2,5)" if n2 == 1 else "S5"
    if o == 168:
        return "PSL(2,7)"
    if o == 360:
        return "A6"
    return f"nonab_{o}"


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


def run_lens(label, size, mul, inv, conj, order, knots):
    ident = int(np.where(order == 1)[0][0])
    print(f"\n=== {label}   |G|={size} ===")
    for kname, (word, n) in knots.items():
        t0 = time.time()
        fps = fixed_points(word, n, size, mul, inv, conj)
        # image subgroup and meridian of each hom
        im_of = {}
        for X in fps:
            H = tuple(closure(list(X), size, mul, inv, ident))
            im_of[X] = (int(X[0]), H)   # meridian = x_1
        # bucket by meridian
        mer = {}
        for X, (m, H) in im_of.items():
            mer.setdefault(m, []).append(H)
        print(f"\n  {kname}: |Hom(K,G)| = {len(fps)}  ({time.time()-t0:.1f}s)")
        # rooms reached alone
        alone = Counter(name_of(H, size, mul, inv, ident, order) for (_, H) in im_of.values())
        print(f"    alone (rooms): {dict(sorted(alone.items()))}")

        # amalgamated sum: pairs sharing the meridian
        jt0 = time.time()
        joins = Counter()
        total_pairs = 0
        for m, Hs in mer.items():
            # distinct subgroups in this bucket, with multiplicity
            cnt = Counter(Hs)
            keys = list(cnt.keys())
            for i in range(len(keys)):
                H1 = keys[i]
                for j in range(i, len(keys)):
                    H2 = keys[j]
                    J = tuple(closure(list(H1) + list(H2), size, mul, inv, ident))
                    nm = name_of(J, size, mul, inv, ident, order)
                    if i == j:
                        joins[nm] += cnt[H1] * cnt[H1]   # ordered pairs H1,H1
                    else:
                        joins[nm] += 2 * cnt[H1] * cnt[H2]
                    total_pairs += (cnt[H1] * cnt[H1] if i == j else 2*cnt[H1]*cnt[H2])
        print(f"    K#K (amalgamated): |Hom| = {total_pairs}  ({time.time()-jt0:.1f}s)")
        print(f"      door-set (join-closure): {dict(sorted(joins.items()))}")


def main():
    knots = {
        "trefoil 3_1": ([1, 1, 1], 2),
        "fig-8 4_1": ([1, -2, 1, -2], 3),
    }
    run_lens("A5", *build_An(5), knots)
    run_lens("A6", *build_An(6), knots)


if __name__ == "__main__":
    main()
