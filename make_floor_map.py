#!/usr/bin/env python3
"""make_floor_map.py — the floor is the group's own map.

mina: "the floor is a map, not a number. every room stands on |G|, but the ground
is not one piece: it splits one shard per conjugacy class — word-blind, the
group's own."

This makes that a theorem, not an observation.  The floor is the DIAGONAL
{x1=...=xn}: each Artin generator acts on a pair (a,b)->(aba^-1,a), fixing (g,g),
so the whole diagonal is beta-hat-fixed for ANY word — word-blind by construction.
The Inn-orbits of the diagonal are then one per conjugacy class of G, with sizes
equal to the class sizes, summing to |G|.  So:

    floor shards = the conjugacy-class partition of G
    #shards       = #classes(G)
    sum of shards = |G|

Verify it on the groups we have: A6, A7 (alternating ladder), SL(2,5) (centre Z2,
the only place the split is visible), GL(3,2)=PSL(2,7).  Print, for each, the class
sizes (the floor map) and check: (a) the diagonal's Inn-orbits reproduce exactly
those sizes, (b) they sum to |G|.

Run: python3 make_floor_map.py
"""
import numpy as np
from collections import Counter

from build_An import build_An
from make_sl25_seam import build_SL25
from make_gl32_counts import build_GL32


def conj_classes(size, conj):
    """Conjugacy classes as lists of members, keyed by min element."""
    classes = {}
    for b in range(size):
        rep = min(int(conj[a, b]) for a in range(size))
        classes.setdefault(rep, []).append(b)
    return [sorted(v) for v in classes.values()]


def diagonal_shard_sizes(size, mul, inv, conj):
    """Inn-orbits of the diagonal (g,g,g,g).  Should reproduce class sizes."""
    ident = None
    orbits = set()
    for g in range(size):
        orb = set()
        for a in range(size):
            orb.add(tuple(int(mul[mul[a, g], inv[a]]) for _ in range(4)))
        orbits.add(min(orb))
    sizes = Counter()
    for c in orbits:
        # size of that orbit
        tup = None
        # recompute orbit size by counting distinct conjugates of the class rep
        # g is fixed as the min rep; find its orbit length
        for g in range(size):
            orb = set()
            for a in range(size):
                orb.add(tuple(int(mul[mul[a, g], inv[a]]) for _ in range(4)))
            if min(orb) == c:
                sizes[len(orb)] += 1
                break
    return sizes


def report(label, size, mul, inv, conj):
    cls = conj_classes(size, conj)
    class_sizes = Counter(len(c) for c in cls)
    ncls = len(cls)
    ssum = sum(len(c) for c in cls)
    diag = diagonal_shard_sizes(size, mul, inv, conj)
    match = (class_sizes == diag)
    print(f"== {label}: |G| = {size} ==")
    print(f"  conjugacy classes (floor map) = {ncls}")
    print(f"  class sizes: {dict(sorted(class_sizes.items()))}")
    print(f"  sum of class sizes = {ssum}  (== |G|: {ssum == size})")
    print(f"  diagonal Inn-orbits reproduce those sizes: {match}")
    print(f"  #classes = {ncls}   |  floor shards = {ncls} (one per class)")
    print()


def main():
    # A6, A7 from the alternating ladder
    for n in (6, 7):
        size, mul, inv, conj, order = build_An(n)
        report(f"A{n}", size, mul, inv, conj)
    # SL(2,5): centre Z2 — the only place floor and hand differ in size
    size, mul, inv, conj, order, elems = build_SL25()
    report("SL(2,5)", size, mul, inv, conj)
    # GL(3,2) = PSL(2,7)
    size, mul, inv, conj, order = build_GL32()
    report("GL(3,2)=PSL(2,7)", size, mul, inv, conj)


if __name__ == "__main__":
    main()
