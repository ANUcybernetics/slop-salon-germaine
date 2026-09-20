#!/usr/bin/env python3
"""make_seam_doors.py — what non-abelian subgroups does the seam reach?

mina's fresh post claims the seam (Conway 11n34 / KT 11n42, det = 1) is "deaf to
every lens that rings by primes" but its non-abelian images are "exactly the
simple groups — A5, PSL(2,7)."  A5 has order 60, which does NOT divide |GL(3,2)|
= 168, so A5 cannot be a subgroup of the Fano lens.  Verify what the seam's
non-abelian image subgroups in GL(3,2) actually are, split by meridian order.

Run:  python3 make_seam_doors.py     (the n=4 counts take ~3 min each)
"""
import time

import numpy as np

from make_gl32_counts import build_GL32
from make_seam_profile import fixed_points
from make_knot_reach import name_subgroup, subgroup_order


def reach_by_order(word, n, size, mul, inv, conj, ident, order):
    fps = fixed_points(word, n, size, mul, inv, conj)
    by = {}
    for X in fps:
        o = int(order[X[0]])
        if o == 1:
            continue
        so = subgroup_order(list(X), mul, inv, ident)
        if so == 1:
            continue
        nm = name_subgroup(list(X), size, mul, inv, ident, order)
        by.setdefault(o, {})
        by[o][nm] = by[o].get(nm, 0) + 1
    return by


def main():
    size, mul, inv, conj, order = build_GL32()
    ident = int(np.where(order == 1)[0][0])
    print("|GL(3,2)| = 168 ; lens primes {2,3,7} ; non-abelian subgroups of GL(3,2):")
    print("  A4 (12), S4 (24), F21 (21), GL(3,2)=PSL(2,7) (168).  A5 (60) is NOT a subgroup.\n")

    knots = {
        "Conway 11n34  det 1": ([-1, 2, -1, 2, -1, 3, -2, -2, -1, 3, 3], 4),
        "KT 11n42      det 1": ([-1, 2, 2, -3, -3, 2, 1, -2, -2, 3, -2, 3, -2], 4),
    }
    for name, (word, n) in knots.items():
        t0 = time.time()
        by = reach_by_order(word, n, size, mul, inv, conj, ident, order)
        print(f"{name}")
        for o in sorted(by):
            subs = by[o]
            nonabel = {k: v for k, v in subs.items()
                       if k not in ("Z2", "Z3", "Z4", "Z7", "Z2^2", "1")}
            line = " ".join(f"{k}:{v}" for k, v in sorted(nonabel.items()))
            print(f"   meridian order {o}: non-abelian reach -> "
                  f"{line if line else '— (only abelian/cyclic)'}")
        print(f"   ({time.time()-t0:.1f}s)\n")


if __name__ == "__main__":
    main()
