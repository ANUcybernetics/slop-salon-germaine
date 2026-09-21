#!/usr/bin/env python3
"""make_AGL17_reach.py — the D7 test: do det-7 knots ring the lens's D7 tooth?

AGL(1,7) is the discriminating lens.  Its tooth set is T(G) = {D7} (no D3),
while |G| = 42 = 2·3·7 keeps the *prime* law honest.  So:

  det-3 knot (trefoil): rings D3 only under the PRIME law (3|42) — the
                        structural law says the order-6 subgroups are all Z6,
                        so it must stay silent (only cyclic/abelian images).
  det-7 knots (5₂, 7₁): ring D7 under BOTH laws (7 tooth present).
  det-5 knots (fig-8, 5₁): silent under both (no D5 tooth, 5 ∤ 42).
  det-1 seam: Δ=1, perfect derived subgroup — deaf to this *solvable* lens
                        (AGL(1,7) is solvable), collapses to the floor.

If the det-3 knot does NOT ring D3 here while det-7 DOES ring D7, the tooth is
structural — T(G) = the odd dihedral subgroups of G, not the primes of |G|.

Run:  python3 make_AGL17_reach.py
"""
import time

import numpy as np

from make_AGL17 import build_AGL17, name_subgroup_AGL17
from make_seam_profile import fixed_points
from make_seam_why import subgroup_order


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


NONABEL = ("Z2", "Z3", "Z4", "Z5", "Z6", "Z7", "Z2^2", "V4", "1")


def show(by):
    for o in sorted(by):
        subs = by[o]
        nonabel = {k: v for k, v in subs.items() if k not in NONABEL}
        line = " ".join(f"{k}:{v}" for k, v in sorted(nonabel.items()))
        print(f"      meridian order {o}: {line if line else '— (only cyclic/abelian)'}")


def main():
    size, mul, inv, conj, order = build_AGL17()
    ident = int(np.where(order == 1)[0][0])
    print("|AGL(1,7)| =", size, "= 2·3·7 ; T(G) = {D7} (no D3)")
    print("  order-6 subgroups are all Z6 (cyclic) — the structural test\n")

    knots = {
        "3_1  trefoil  det 3": ([1, 1, 1], 2),
        "4_1  fig-8    det 5": ([1, -2, 1, -2], 3),
        "5_1  (2,5)    det 5": ([1, 1, 1, 1, 1], 2),
        "5_2           det 7": ([1, 2, 2, 2, 1, -2], 3),
        "7_1  (2,7)    det 7": ([1, 1, 1, 1, 1, 1, 1], 2),
        "Conway seam   det 1": ([-1, 2, -1, 2, -1, 3, -2, -2, -1, 3, 3], 4),
    }
    for name, (word, n) in knots.items():
        t0 = time.time()
        by = reach_by_order(word, n, size, mul, inv, conj, ident, order,
                            name_subgroup_AGL17)
        print(f"  {name}   ({(time.time()-t0):.1f}s)")
        show(by)
        print()


if __name__ == "__main__":
    main()
