#!/usr/bin/env python3
"""make_amalgam_pairs.py — WHICH pairs open the blind room, under the amalgamated
(meridian-shared) connected sum.

mina: "the pair is A₄+A₄ / D₅+D₅, not A₄+D₅."  Verify: for the fig-8 in A₅, which
pairs (sharing the meridian) actually generate A₅?  And recheck trefoil in S₅:
does trefoil#trefoil still reach S₅ (breaking the sign) under amalgamation, or
does the meridian lock it?

Run:  python3 make_amalgam_pairs.py
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


def run(label, size, mul, inv, conj, order, kname, word, n, target):
    ident = int(np.where(order == 1)[0][0])
    print(f"\n=== {label}: {kname} → {target} ===")
    fps = fixed_points(word, n, size, mul, inv, conj)
    im_of = {}
    for X in fps:
        H = tuple(closure(list(X), size, mul, inv, ident))
        im_of[X] = (int(X[0]), H)
    mer = {}
    for X, (m, H) in im_of.items():
        mer.setdefault(m, []).append(H)
    # alone
    alone = Counter(name_of(H, size, mul, inv, ident, order) for (_, H) in im_of.values())
    print(f"  |Hom(K,G)| = {len(fps)}   alone: {dict(sorted(alone.items()))}")

    # which pairs (by subgroup-name pair) generate the target?
    pair_names = Counter()
    for m, Hs in mer.items():
        cnt = Counter(Hs)
        keys = list(cnt.keys())
        for i in range(len(keys)):
            for j in range(i, len(keys)):
                H1, H2 = keys[i], keys[j]
                J = tuple(closure(list(H1) + list(H2), size, mul, inv, ident))
                nmJ = name_of(J, size, mul, inv, ident, order)
                if nmJ == target:
                    n1 = name_of(H1, size, mul, inv, ident, order)
                    n2 = name_of(H2, size, mul, inv, ident, order)
                    key = (n1, n2)
                    pair_names[key] += (cnt[H1]*cnt[H1] if i == j else 2*cnt[H1]*cnt[H2])
    print(f"  pairs sharing a meridian that open {target}:")
    for (n1, n2), c in sorted(pair_names.items(), key=lambda kv: -kv[1]):
        print(f"    {n1:>8} + {n2:<8}  → {c}")


if __name__ == "__main__":
    # fig-8 in A5: which pairs open A5?
    run("A5", *build_An(5), "fig-8 4_1", [1, -2, 1, -2], 3, "A5")
    # trefoil in A5: which pairs open A5 (already reached alone)?
    run("A5", *build_An(5), "trefoil 3_1", [1, 1, 1], 2, "A5")
    # trefoil in S5: does the sign lock hold under amalgamation? does it reach S5?
    run("S5", *build_S5(), "trefoil 3_1", [1, 1, 1], 2, "S5")
    # fig-8 in S5: reach A5?
    run("S5", *build_S5(), "fig-8 4_1", [1, -2, 1, -2], 3, "A5")
