#!/usr/bin/env python3
"""make_reach.py — the reach: which subgroups of GL(3,2) does each knot surject onto?

The seam reading (make_seam_why.py) showed the seam knots (Conway, KT) reach ONLY
the whole group GL(3,2), while the trefoil and fig-8 also reach proper subgroups
(6, 12, 24).  Is that a function of the knot's size — genus or crossing number?

Run the same image-order profile across the small knots.  They come in a
convenient ladder:
  genus 1, crossings 3-6 : 3_1, 4_1, 5_1, 5_2, 6_1
  genus 2, crossings 6-11: 6_2, 6_3, Conway 11n34, KT 11n42
If the reach (which subgroup orders appear, and in how many conjugation-orbits)
tracks genus, the genus-2 knots should reach only the top.  If it tracks
crossing number, the 6-crossing knots should straddle.

Run:  python3 make_reach.py     (6_1 is a 4-braid, ~3 min; the rest are fast)
"""
import time

import numpy as np

from make_gl32_counts import build_GL32, apply_auto
from make_seam_profile import fixed_points, conj_classes
from make_seam_why import subgroup_order


def orbits(fps, size, conj):
    """Dedupe fixed points into conjugation orbits; return (canonical, orbit_size)."""
    canon = set()
    for X in fps:
        best = X
        for h in range(size):
            Y = tuple(int(conj[h, x]) for x in X)
            if Y < best:
                best = Y
        canon.add(best)
    return canon


def main():
    size, mul, inv, conj, order = build_GL32()
    ident = int(np.where(order == 1)[0][0])
    label = conj_classes(size, conj)
    print("|GL(3,2)| =", size)

    knots = {
        "3_1   (g1,c3)": ([1, 1, 1], 2),
        "4_1   (g1,c4)": ([1, -2, 1, -2], 3),
        "5_1   (g1,c5)": ([1, 1, 1, 1, 1], 2),
        "5_2   (g1,c5)": ([1, 2, 2, 2, 1, -2], 3),
        "6_1   (g1,c6)": ([-1, -1, -2, 1, 3, -2, 3], 4),
        "6_2   (g2,c6)": ([1, -2, 1, 1, 1, -2], 3),
        "6_3   (g2,c6)": ([-1, -1, 2, -1, 2, 2], 3),
        "Conway(g2,c11)": ([-1, 2, -1, 2, -1, 3, -2, -2, -1, 3, 3], 4),
        "KT    (g2,c11)": ([-1, 2, 2, -3, -3, 2, 1, -2, -2, 3, -2, 3, -2], 4),
    }

    for name, (word, n) in knots.items():
        t0 = time.time()
        fps = fixed_points(word, n, size, mul, inv, conj)
        canon = orbits(fps, size, conj)
        # reach: for each orbit, its image-subgroup order, split by meridian order
        reach = {}          # image_order -> {meridian_order -> #orbits}
        for X in canon:
            so = subgroup_order(list(X), mul, inv, ident)
            mo = int(order[X[0]])
            reach.setdefault(so, {})
            reach[so][mo] = reach[so].get(mo, 0) + 1
        # total fixed points and total non-abelian orbits
        total_orbits = len(canon)
        nonabel = sum(v for so, d in reach.items() if so > 1
                      for v in d.values())
        # summarize reach as "order: #orbits"
        reach_str = "  ".join(f"{so}:{sum(d.values())}" for so, d in
                              sorted(reach.items()) if so > 1)
        print(f"\n{name:<13} fixed={len(fps):>5} orbits={total_orbits:>4} "
              f"nonabel-orbits={nonabel:>3}  ({(time.time()-t0):.1f}s)")
        print(f"  reach (image_order:orbits) : {reach_str}")
        # meridian split for the top (168) only
        if 168 in reach:
            print(f"  split to 168              : "
                  f"{dict(sorted(reach[168].items()))}")


if __name__ == "__main__":
    main()
