#!/usr/bin/env python3
"""make_psl11_ledger.py — the PSL(2,11) ledger, computed.

mina: "PSL(2,11), order 660: floor 660 in 8 shards, one per class. |Out|=2 there,
so hands = 2 x locks, your theorem intact."  and "both cross PSL(2,11) at x11."

This runs the same class-restricted beta-hat ledger as A7, on the PSL(2,11) room.
It checks: (1) the floor is the 8 conjugacy-class shards summing to 660 (word-
blind), (2) every hand is a free orbit of size |Inn| = 660, (3) |Hom| = 11 x 660
for BOTH words (the crossing), and (4) the seam reads the floor the same.

Run: python3 make_psl11_ledger.py
"""
import time
import numpy as np
from collections import Counter
from build_PSL import build_PSL

WORDS = {"conway": ([-1, 2, -1, 2, -1, 3, -2, -2, -1, 3, 3], 4),
         "kt": ([-1, 2, 2, -3, -3, 2, 1, -2, -2, 3, -2, 3, -2], 4)}


def apply_auto(X, moves, mul, inv, conj):
    for (i, eps) in moves:
        a = X[:, i].copy(); b = X[:, i + 1].copy()
        if eps > 0:
            na = conj[a, b]; nb = a
        else:
            na = b; nb = conj[inv[b], a]
        X[:, i] = na; X[:, i + 1] = nb
    return X


def inn_orbit_set(tup, mul, inv, size):
    orb = set()
    for g in range(size):
        orb.add(tuple(int(mul[mul[g, x], inv[g]]) for x in tup))
    return orb


def ledger(name, size, mul, inv, conj):
    word, _ = WORDS[name]
    ident = int(np.where(np.sum(conj == np.arange(size)[:, None], axis=1) == 0)[0]) if False else None
    moves = [(abs(g) - 1, 1 if g > 0 else -1) for g in word]
    classes = {}
    for b in range(size):
        rep = min(int(conj[a, b]) for a in range(size))
        classes.setdefault(rep, []).append(b)
    t0 = time.time()
    orbits = {}
    for rep, members in sorted(classes.items(), key=lambda kv: -len(kv[1])):
        m = len(members)
        mem = np.array(members, dtype=np.int64)
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
    by_size = Counter()
    diag = []; hands = []
    for c, orb in orbits.items():
        tup = next(iter(orb))
        osz = len(orb)
        total += osz
        by_size[osz] += 1
        if all(x == tup[0] for x in tup):
            diag.append(osz)
        else:
            hands.append(osz)
    return total, len(orbits), by_size, sorted(diag), sorted(hands), time.time() - t0


def main():
    size, mul, inv, conj, order, reps = build_PSL(11)
    print(f"|PSL(2,11)| = {size},  |Inn| = {size}  (simple, |Z|=1)\n")
    for name in ["conway", "kt"]:
        total, norbit, by_size, diag, hands, dt = ledger(name, size, mul, inv, conj)
        print(f"== {name} in PSL(2,11) ==  ({dt:.1f}s)")
        print(f"  |Hom| = {total}   (x{total // size} in |G|)")
        print(f"  Inn-orbits = {norbit}")
        print(f"  orbits by size: {dict(sorted(by_size.items()))}")
        print(f"  floor shards = {len(diag)}   sizes = {diag}   sum = {sum(diag)}")
        print(f"  hands = {len(hands)}   sizes = {set(hands)}")
        print(f"  floor/hand same size: {set(diag) == set(hands)}")
        print()


if __name__ == "__main__":
    main()
