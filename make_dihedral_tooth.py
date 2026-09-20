#!/usr/bin/env python3
"""make_dihedral_tooth.py — is the det law (one dihedral tooth per lens) local?

rahel: "the determinant is the tooth of the dihedral ear, not the knot's whole
mouth."  Through GL(3,2) my one-note law found exactly ONE order-2 tooth (S3=D3),
because two transvections there have product order in {1,2,3,4} (never 5, never
7), and det is odd -> order(ab) in {1,3}.  A5 is the control lens: it carries a
5-tooth, its involutions are double transpositions, and two of them have product
order in {1,2,3,5}.  If the det is truly the dihedral tooth, then through A5 a
det-5 knot should ring D5, a det-3 knot D3, and a det-7 knot (7 coprime to 15)
should collapse.  Same knots, GL(3,2) vs A5, the tooth moves with the lens.

Run:  python3 make_dihedral_tooth.py     (n=4 seam rows take ~1 min each)
"""
import time

import numpy as np

from make_gl32_counts import build_GL32
from make_A5 import build_A5, name_subgroup_A5
from make_seam_profile import fixed_points
from make_seam_why import subgroup_order
from make_knot_reach import name_subgroup as name_subgroup_GL32


def reach_by_order(word, n, size, mul, inv, conj, ident, order, name_fn):
    """Return {meridian_order: {subgroup_name: count}} for non-abelian images."""
    fps = fixed_points(word, n, size, mul, inv, conj)
    by = {}
    for X in fps:
        o = int(order[X[0]])
        if o == 1:
            continue
        so = subgroup_order(list(X), mul, inv, ident)
        if so == 1:
            continue
        nm = name_fn(list(X), size, mul, inv, ident, order)
        by.setdefault(o, {})
        by[o][nm] = by[o].get(nm, 0) + 1
    return by


NONABEL = ("Z2", "Z3", "Z4", "Z5", "Z7", "Z2^2", "V4", "Z6", "1")


def show(by):
    for o in sorted(by):
        subs = by[o]
        nonabel = {k: v for k, v in subs.items() if k not in NONABEL}
        line = " ".join(f"{k}:{v}" for k, v in sorted(nonabel.items()))
        print(f"      meridian order {o}: {line if line else '— (only abelian/cyclic)'}")


def main():
    knots = {
        "3_1  trefoil  det 3": ([1, 1, 1], 2),
        "4_1  fig-8    det 5": ([1, -2, 1, -2], 3),
        "5_1  (2,5)    det 5": ([1, 1, 1, 1, 1], 2),
        "5_2           det 7": ([1, 2, 2, 2, 1, -2], 3),
        "7_1  (2,7)    det 7": ([1, 1, 1, 1, 1, 1, 1], 2),
        "9_1  (2,9)    det 9": ([1] * 9, 2),
        "Conway seam   det 1": ([-1, 2, -1, 2, -1, 3, -2, -2, -1, 3, 3], 4),
    }

    for lens_name, (build, name_fn) in (
        ("GL(3,2) |168|  primes {2,3,7}", (build_GL32, name_subgroup_GL32)),
        ("A5      |60|   primes {2,3,5}", (build_A5, name_subgroup_A5)),
    ):
        size, mul, inv, conj, order = build()
        ident = int(np.where(order == 1)[0][0])
        print(f"\n===== {lens_name} =====")
        print("  non-abelian subgroups: " + (
            "S3(6), A4(12), S4(24), F21(21), GL(3,2)=PSL(2,7)(168)"
            if lens_name.startswith("GL") else
            "S3(6)=D3, D5(10), A4(12), A5(60)"
        ))
        for name, (word, n) in knots.items():
            t0 = time.time()
            by = reach_by_order(word, n, size, mul, inv, conj, ident, order,
                                name_fn)
            print(f"  {name}   ({(time.time()-t0):.1f}s)")
            show(by)
        print()


if __name__ == "__main__":
    main()
