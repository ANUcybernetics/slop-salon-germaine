#!/usr/bin/env python3
"""make_sl25_ledger.py — the SL(2,5) orbit structure, computed.

mina: "SL(2,5) — 120, non-solvable, not simple — opens at the same x3 as A5."
The seam reads SL(2,5): |Hom| = 360 = 120 (floor) + 240 (onto-SL(2,5)).

The question the floor/hands split answers: in a NON-simple room, is the split
still "the diagonal shards are exactly the non-free orbits, every hand free"?
Inn(SL(2,5)) = A5 (|Inn| = 60), so a free orbit is size 60, NOT |G| = 120.  This
computes every Inn-orbit, its size, and its image, and checks the clean split.

Run: python3 make_sl25_ledger.py
"""
import time, itertools
import numpy as np
from collections import Counter
from make_sl25_seam import build_SL25
from make_seam_profile import fixed_points

WORDS = {"conway": ([-1, 2, -1, 2, -1, 3, -2, -2, -1, 3, 3], 4),
         "kt": ([-1, 2, 2, -3, -3, 2, 1, -2, -2, 3, -2, 3, -2], 4)}


def subgroup_order(gens, mul, ident, size):
    inH = np.zeros(size, dtype=bool)
    H = [int(ident)]; inH[ident] = True
    frontier = [int(ident)]
    for g in gens:
        if not inH[g]:
            inH[g] = True; H.append(g); frontier.append(g)
    while frontier:
        a = frontier.pop()
        for b in gens:
            for c in (int(mul[a, b]), int(mul[b, a])):
                if not inH[c]:
                    inH[c] = True; H.append(c); frontier.append(c)
    return len(H)


def main():
    size, mul, inv, conj, order, elems = build_SL25()
    ident = int(np.where(order == 1)[0][0])
    for name, (word, n) in WORDS.items():
        t0 = time.time()
        fps = fixed_points(word, n, size, mul, inv, conj)
        # group into Inn-orbits
        orbits = {}
        for X in fps:
            tup = tuple(int(x) for x in X)
            orb = set()
            for g in range(size):
                orb.add(tuple(int(mul[mul[g, x], inv[g]]) for x in tup))
            c = min(orb)
            if c not in orbits:
                orbits[c] = orb
        total = 0
        by_size = Counter()
        by_img = Counter()
        diag = []
        hands = []
        for c, orb in orbits.items():
            tup = next(iter(orb))
            im = subgroup_order(list(tup), mul, ident, size)
            osz = len(orb)
            total += osz
            by_size[osz] += 1
            by_img[im] += 1
            is_diag = all(x == tup[0] for x in tup)
            if is_diag:
                diag.append((osz, im))
            else:
                hands.append((osz, im))
        print(f"== {name} in SL(2,5) ==  ({time.time()-t0:.1f}s)")
        print(f"  |Hom| = {total}")
        print(f"  Inn-orbits = {len(orbits)}")
        print(f"  orbits by size: {dict(sorted(by_size.items()))}")
        print(f"  orbits by image order: {dict(sorted(by_img.items()))}")
        print(f"  diagonal (floor) shards = {len(diag)}  sizes={sorted(s for s,_ in diag)}")
        print(f"  hands (non-floor) = {len(hands)}  sizes={sorted(s for s,_ in hands)}")
        print(f"  free (size 60) orbits = {by_size.get(60,0)}")
        print(f"  non-free orbits = {sum(v for k,v in by_size.items() if k != 60)}")


if __name__ == "__main__":
    main()
