#!/usr/bin/env python3
"""make_a7_ledger.py — the A7 ledger, computed, not asserted.

rahel reads A7: the floor (diagonal) is 9 shards (one per conjugacy class,
sizes 1·70·105·210·280·360·360·504·630), "the only non-free orbits"; the hands
above are each a whole 2520, Conway 74 hands (3 A5 + 20 A6 + 16 PSL(2,7) + 34 A7),
KT 62 (3 + 20 + 12 + 26); "Conway reads 82 orbits, KT 70."

This computes the real decomposition of the beta-hat-fixed set in A7: every
Inn-orbit with its size, its image order, whether it is diagonal (on the floor),
and whether it is free (size 2520).  It checks two claims: (1) the floor shards
are exactly the non-free orbits, and (2) the hands count.

Fast: per meridian class, fix x1 = a and take x2 over the centralizer C(a)-orbit
reps (one per orbit), x3,x4 over the whole class.  Each found tuple's full
Inn-orbit is then computed and deduplicated.

Run: python3 make_a7_ledger.py
"""
import time
import numpy as np
from collections import Counter
from build_An import build_An

WORDS = {"conway": ([-1, 2, -1, 2, -1, 3, -2, -2, -1, 3, 3], 4),
         "kt": ([-1, 2, 2, -3, -3, 2, 1, -2, -2, 3, -2, 3, -2], 4)}
WANT = 2520


def apply_auto(X, moves, mul, inv, conj):
    for (i, eps) in moves:
        a = X[:, i].copy(); b = X[:, i + 1].copy()
        if eps > 0:
            na = conj[a, b]; nb = a
        else:
            na = b; nb = conj[inv[b], a]
        X[:, i] = na; X[:, i + 1] = nb
    return X


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


def inn_orbit_set(tup, mul, inv, size):
    orb = set()
    for g in range(size):
        orb.add(tuple(int(mul[mul[g, x], inv[g]]) for x in tup))
    return orb


def ledger(name, n=7, verbose=True):
    size, mul, inv, conj, order = build_An(n)
    word, _ = WORDS[name]
    ident = int(np.where(order == 1)[0][0])
    moves = [(abs(g) - 1, 1 if g > 0 else -1) for g in word]

    # conjugacy classes by representative
    classes = {}
    for b in range(size):
        rep = min(int(conj[a, b]) for a in range(size))
        classes.setdefault(rep, []).append(b)

    t0 = time.time()
    orbits = {}
    for rep, members in sorted(classes.items(), key=lambda kv: -len(kv[1])):
        m = len(members)
        mem = np.array(members, dtype=np.int64)
        # centralizer of rep; x2 over its C(rep)-orbit reps
        Crep = [g for g in range(size) if conj[g, rep] == rep]
        seen = set(); x2reps = []
        for x2 in sorted(members):
            if x2 in seen: continue
            x2reps.append(x2)
            seen |= {int(conj[h, x2]) for h in Crep}
        g3 = np.repeat(mem, m); g4 = np.tile(mem, m)
        for x2 in x2reps:
            A = np.zeros((m * m, 4), dtype=np.int64)
            A[:, 0] = rep; A[:, 1] = x2; A[:, 2] = g3; A[:, 3] = g4
            mask = np.all(apply_auto(A.copy(), moves, mul, inv, conj) == A, axis=1)
            for r in np.nonzero(mask)[0]:
                tup = (int(rep), int(x2), int(g3[r]), int(g4[r]))
                orb = inn_orbit_set(tup, mul, inv, size)
                c = min(orb)
                if c not in orbits:
                    orbits[c] = orb

    total = 0
    by_size = Counter(); by_img = Counter()
    diag = []; hands = []
    for c, orb in orbits.items():
        tup = next(iter(orb))
        im = subgroup_order(list(tup), mul, ident, size)
        osz = len(orb)
        total += osz
        by_size[osz] += 1
        by_img[im] += 1
        if all(x == tup[0] for x in tup):
            diag.append((osz, im))
        else:
            hands.append((osz, im))
    if verbose:
        print(f"== {name} in A_{n} ==  ({time.time()-t0:.1f}s)")
        print(f"  |Hom| = {total}")
        print(f"  Inn-orbits = {len(orbits)}")
        print(f"  orbits by size: {dict(sorted(by_size.items()))}")
        print(f"  orbits by image order: {dict(sorted(by_img.items()))}")
        print(f"  diagonal (floor) shards = {len(diag)}  sizes={sorted(s for s,_ in diag)}")
        print(f"  hands (non-floor) = {len(hands)}  sizes={sorted(s for s,_ in hands)}")
        print(f"  free (size {WANT}) orbits = {by_size.get(WANT,0)}")
        print(f"  non-free orbits = {sum(v for k,v in by_size.items() if k != WANT)}")
    return total, orbits, by_size, by_img, diag, hands


if __name__ == "__main__":
    for name in ["conway", "kt"]:
        ledger(name, 7)
