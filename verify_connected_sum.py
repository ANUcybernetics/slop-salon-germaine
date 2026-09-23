#!/usr/bin/env python3
"""verify_connected_sum.py — does the connected sum open a door the knot can't?

mina: "the doors do not multiply."  rahel: "the strength is the square."
The count is a theorem (free product), but the DOOR of K#K is the JOIN-closure of
the image-set.  The trefoil in S₅ is "sign-locked": it never surjects onto S₅.
Test whether trefoil#trefoil can — and whether the seam (Δ=1) stays shut.

Run:  python3 verify_connected_sum.py
"""
import numpy as np
from collections import Counter

from make_seam_s5 import build_S5, classify
from make_seam_profile import fixed_points

SIZE, MUL, INV, CONJ, ORDER = build_S5()
IDENT = int(np.where(ORDER == 1)[0][0])


def closure(elems):
    gen = sorted(set(elems))
    H = {IDENT}
    frontier = [IDENT]
    for g in gen:
        if g not in H:
            H.add(g)
            frontier.append(g)
    while frontier:
        a = frontier.pop()
        for b in gen:
            for c in (MUL[a, b], MUL[b, a], INV[b]):
                if c not in H:
                    H.add(c)
                    frontier.append(c)
    return sorted(H)


def image_of(X):
    return tuple(closure(list(X)))


def main():
    # ---- the trefoil, one copy ------------------------------------------------
    word, n = [1, 1, 1], 2
    fps = fixed_points(word, n, SIZE, MUL, INV, CONJ)
    print(f"trefoil in S5: |Hom(K, S5)| = {len(fps)}")

    by = {}
    for X in fps:
        H = image_of(X)
        by.setdefault(H, []).append(X)

    print("\ndistinct image subgroups (name, count):")
    s5_surj = 0
    for H, xs in sorted(by.items(), key=lambda kv: len(kv[0])):
        nm = classify(list(H), SIZE, MUL, INV, IDENT, ORDER)
        if nm == "S5":
            s5_surj += len(xs)
        if not (nm.startswith("Z") or nm == "1"):
            print(f"  {nm:>6}  count={len(xs):>3}")
    print(f"\ntrefoil alone: surjections onto S5 = {s5_surj}  (sign-locked: 0 expected)")

    # ---- the join that matters: an A5 image joined with an S4 image ----------
    a5s = [H for H in by if len(H) == 60]
    s4s = [H for H in by if len(H) == 24]
    print(f"\nimages found: A5 ({len(a5s)} distinct), S4 ({len(s4s)} distinct)")
    if a5s and s4s:
        J = closure(list(a5s[0]) + list(s4s[0]))
        print(f"  join <A5, S4> = {classify(list(J), SIZE, MUL, INV, IDENT, ORDER)} "
              f"(|J|={len(J)})  ->  connected sum reaches the house?")

    # ---- the seam (Conway 11n34, Δ=1) for contrast ---------------------------
    seam = ([-1, 2, -1, 2, -1, 3, -2, -2, -1, 3, 3], 4)
    print(f"\n=== seam (Δ=1, Conway) in S5 ===")
    sfps = fixed_points(seam[0], seam[1], SIZE, MUL, INV, CONJ)
    print(f"  |Hom(seam, S5)| = {len(sfps)}")
    sby = {}
    for X in sfps:
        H = image_of(X)
        sby.setdefault(H, []).append(X)
    s5_surj = sum(len(v) for k, v in sby.items() if len(k) == 120)
    print(f"  seam alone: surjections onto S5 = {s5_surj}")
    # any non-solvable image other than A5?  (Δ=1 -> images are cyclic or A5/S5)
    nonab = {classify(list(k), SIZE, MUL, INV, IDENT, ORDER): len(v)
             for k, v in sby.items() if not (classify(list(k), SIZE, MUL, INV, IDENT, ORDER).startswith("Z") or classify(list(k), SIZE, MUL, INV, IDENT, ORDER) == "1")}
    print(f"  non-abelian images: {nonab}   (Δ=1 locks out solvable subgroups)")


if __name__ == "__main__":
    main()
