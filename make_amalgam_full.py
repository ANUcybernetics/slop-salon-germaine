#!/usr/bin/env python3
"""make_amalgam_full.py — the amalgamated connected sum, all numbers.

π₁(K#K) = π₁(K) *_{Z} π₁(K)  over the meridian μ = x₁.  Hom(K#K,G) =
{ (φ₁,φ₂) : φ₁(x₁)=φ₂(x₁) }  (NOT the free square |Hom|²).  The image of the
sum-hom is ⟨im φ₁, im φ₂⟩.

Key correction to my earlier work: the count is  Σ_g n_g²   where n_g = #{φ: φ(x₁)=g}
(the "amalgamated square"), NOT |Hom(K,G)|².  And the door-set is the join-closure
over meridian-sharing pairs.

Run:  python3 make_amalgam_full.py
"""
import time
from collections import Counter

import numpy as np

from build_An import build_An
from make_seam_s5 import build_S5
from make_seam_profile import fixed_points


def name_of(H, size, mul, inv, ident, order):
    o = len(H)
    if o == 1:
        return "1"
    abelian = all(mul[a, b] == mul[b, a] for a in H for b in H)
    hist = Counter(int(order[x]) for x in H)
    n2 = hist.get(2, 0)
    if abelian:
        if o == 3: return "C3"
        if o == 4: return "V4"
        if o == 5: return "C5"
        if o == 6: return "C6"
        return "C%d" % o
    if o == 6: return "S3"
    if o == 10: return "D5"
    if o == 12: return "A4"
    if o == 20: return "F20"
    if o == 24: return "S4"
    if o == 36: return "3^2:4"
    if o == 60: return "A5"
    if o == 120: return "SL(2,5)" if n2 == 1 else "S5"
    if o == 168: return "PSL(2,7)"
    if o == 360: return "A6"
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


def report(label, size, mul, inv, conj, order, kname, word, n):
    ident = int(np.where(order == 1)[0][0])
    print(f"\n### {label} : {kname}")
    fps = fixed_points(word, n, size, mul, inv, conj)
    # meridian buckets + image subgroup per hom
    mer = {}   # m -> Counter of image-subgroups
    im_names = Counter()
    for X in fps:
        H = tuple(closure(list(X), size, mul, inv, ident))
        m = int(X[0])
        mer.setdefault(m, Counter())[H] += 1
        im_names[name_of(H, size, mul, inv, ident, order)] += 1
    # count formula
    n_g = {m: sum(c.values()) for m, c in mer.items()}
    amalg_count = sum(nv * nv for nv in n_g.values())
    free_count = len(fps) ** 2
    print(f"  |Hom(K,G)| = {len(fps)}")
    print(f"  FREE product count |Hom|²          = {free_count}")
    print(f"  AMALGAMATED count Σ_g n_g²         = {amalg_count}")
    print(f"  alone rooms: {dict(sorted(im_names.items()))}")

    # door-set of the amalgamated sum
    joins = Counter()
    for m, c in mer.items():
        keys = list(c.keys())
        for i in range(len(keys)):
            H1 = keys[i]
            for j in range(i, len(keys)):
                H2 = keys[j]
                J = tuple(closure(list(H1) + list(H2), size, mul, inv, ident))
                nm = name_of(J, size, mul, inv, ident, order)
                mult = c[H1] * c[H1] if i == j else 2 * c[H1] * c[H2]
                joins[nm] += mult
    print(f"  K#K door-set (amalgamated): {dict(sorted(joins.items()))}")
    return im_names, joins


if __name__ == "__main__":
    # the two simple knots across the key lenses
    report("A5", *build_An(5), "trefoil 3_1", [1, 1, 1], 2)
    report("A5", *build_An(5), "fig-8 4_1", [1, -2, 1, -2], 3)
    report("A6", *build_An(6), "trefoil 3_1", [1, 1, 1], 2)
    report("A6", *build_An(6), "fig-8 4_1", [1, -2, 1, -2], 3)
    report("S5", *build_S5(), "trefoil 3_1", [1, 1, 1], 2)
    report("S5", *build_S5(), "fig-8 4_1", [1, -2, 1, -2], 3)
