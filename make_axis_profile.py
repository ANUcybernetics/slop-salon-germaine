#!/usr/bin/env python3
"""make_axis_profile.py — the axes of the meridians in the onto-hands.

A meridian is an element of order m=(p-1)/2 in PSL(2,p): diagonalizable over
F_p, so it has TWO fixed points on P^1(F_p) — its AXIS.  Two meridians lie in
one torus (a Cartan) iff they have the SAME axis (same pair of fixed points).

For each word, find the beta-hat-fixed tuples in the split-torus class (vectorised
via fastkernel), and for the ONTO ones read the axis-pairing.  The claim to test:
KT always FOLDS x3,x4 (same axis); Conway's skeleton fold is never realised —
its onto-hands SPREAD (or fold a DIFFERENT pair).  And: KT's reach = the count of
Conway's folded hands, so the seam is Conway's spread.
"""
import sys
import numpy as np
from psl import PSL
import fastkernel

WORDS = {"conway": [-1, 2, -1, 2, -1, 3, -2, -2, -1, 3, 3],
         "kt": [-1, 2, 2, -3, -3, 2, 1, -2, -2, 3, -2, 3, -2]}


def fixed_points(M, p):
    """the fixed points of M on P^1(F_p); sorted tuple, p encodes infinity."""
    a, b, c, d = (int(v) for v in M)
    pts = set()
    if c % p == 0:
        if (d - a) % p != 0:
            pts.add((b * pow((d - a) % p, p - 2, p)) % p)
        pts.add(p)
    else:
        A, B, C = c % p, (d - a) % p, (-b) % p
        disc = (B * B - 4 * A * C) % p
        if disc == 0 or pow(disc, (p - 1) // 2, p) == 1:
            r = next(z for z in range(p) if (z * z) % p == disc)
            iden = pow((2 * A) % p, p - 2, p)
            for sgn in (1, -1):
                pts.add(((-B + sgn * r) % p * iden) % p)
    return tuple(sorted(pts))


def closure(gens, G):
    S = {G.id}
    frontier = [G.id]
    while frontier:
        ng = []
        for f in frontier:
            for g in gens:
                h = G.m(f, g)
                if h not in S:
                    S.add(h)
                    ng.append(h)
        frontier = ng
    return len(S)


def orbit_reps_sizes(G, C, T):
    seen = set()
    reps, sizes = [], []
    for y in C:
        if y in seen:
            continue
        orb = {G.cj(y, t) for t in T}
        seen |= orb
        reps.append(y)
        sizes.append(len(orb))
    return reps, sizes


def class_axis_profile(G, rep, C, word, p):
    """Return counts of ONTO hands by axis-pairing pattern, and floor count."""
    moves = [(abs(g) - 1, 1 if g > 0 else -1) for g in word]
    T = [G.id]
    cur = rep
    while cur != G.id:
        T.append(cur)
        cur = G.m(cur, rep)
    x2reps, x2sizes = orbit_reps_sizes(G, C, T)
    m = len(C)
    mem = np.array(C, dtype=np.int64)
    g3 = np.repeat(mem, m, axis=0)
    g4 = np.tile(mem, (m, 1))
    rep_arr = np.array(rep, dtype=np.int64)
    onto = {}
    floor = {}
    for x2, osz in zip(x2reps, x2sizes):
        A = np.zeros((m * m, 4, 4), dtype=np.int64)
        A[:, 0, :] = rep_arr
        A[:, 1, :] = x2
        A[:, 2, :] = g3
        A[:, 3, :] = g4
        F = fastkernel.apply_auto_fast(A.copy(), moves, p)
        mask = np.ones(m * m, dtype=bool)
        for j in range(4):
            out = F[:, j, :]
            inp = A[:, j, :]
            mask &= np.all((out - inp) % p == 0, axis=1) | np.all((out + inp) % p == 0, axis=1)
        for r in np.nonzero(mask)[0]:
            X = [rep, x2, tuple(g3[r]), tuple(g4[r])]
            axes = [fixed_points(x, p) for x in X]
            pairs = tuple((i + 1, j + 1) for i in range(4) for j in range(i + 1, 4)
                          if axes[i] == axes[j])
            full = closure(list(X), G) == G.n
            d = onto if full else floor
            d[pairs] = d.get(pairs, 0) + osz
    return onto, floor


def bead_labels(G, m):
    """map each order-m class rep to its exponent label min(j, m-j)."""
    import math
    a = next(x for x in G.reps if G.order(x) == m)
    label = {}
    for j in range(1, m):
        if math.gcd(j, m) != 1:
            continue
        aj = G.id
        for _ in range(j):
            aj = G.m(aj, a)
        for t in G.reps:
            label.setdefault(G.cj(aj, t), min(j, m - j))
    return label


def main():
    p = int(sys.argv[1]) if len(sys.argv) > 1 else 13
    G = PSL(p)
    print(f"|PSL(2,{p})| = {G.n}")
    m = (p - 1) // 2
    classes = G.classes()
    cand = [rep for rep in classes if G.order(rep) == m]
    lab = bead_labels(G, m)
    print(f"  split-torus class(es) order {m}: {len(cand)}")
    for rep in cand:
        C = sorted(classes[rep])
        print(f"  class |C|={len(C)}  bead j={lab.get(rep)}")
        for name, word in WORDS.items():
            onto, floor = class_axis_profile(G, rep, C, word, p)
            print(f"    {name:6s}: ONTO={sum(onto.values())}  floor={sum(floor.values())}")
            for key in sorted(onto):
                print(f"        onto {key}: {onto[key]}")
            for key in sorted(floor):
                print(f"        floor {key}: {floor[key]}")


if __name__ == "__main__":
    main()
