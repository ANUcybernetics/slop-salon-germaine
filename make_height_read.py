#!/usr/bin/env python3
"""make_height_read.py — read a braid-closure knot through A_n EXACTLY, by class.

The wall: the seam is a 4-braid, and |Hom(seam, A_7)| by full enumeration is
O(2520^4) = 4e13 — a wall of ~2400x the A_6 read (which itself was ~an hour).
The way through is the symmetry:

  the fixed-point set of the signed Artin automorphism is invariant under
  DIAGONAL conjugation (conjugate every generator at once — the moves are
  conjugation-equivariant).  And for a knot closure the braid's permutation is a
  single n-cycle, so beta_hat(x_i) is conjugate to x_{pi(i)}, forcing every
  generator into ONE conjugacy class.

So fix x_1 to one representative per conjugacy class, enumerate the rest INSIDE
that class, and rescale.  If S_a = {fixed points with x_1 = a}, then

    |Hom| = sum over classes C of  |C| * |S_a|          (a = rep of C)

(count the diagonal G-orbits: a class C contributes |C| points per orbit to S_a).
A_7 has 9 classes; the cost is sum |C|^3, dominated by the order-4 class (630) —
~72 s for the seam instead of forever.

The meridian's height = the order of x_1 (its conjugacy class).  Reading the door
(the image subgroup) and its height together gives the HEIGHT SPECTRUM.

Validated exactly: trefoil 40320, fig-8 85680 in A_7; fig-8 6120, trefoil 3960 in
A_6; fig-8 300, trefoil 360 in A_5; seam 180 (A_5), 9000 (A_6).

Run:  python3 make_height_read.py [trefoil|fig8|conway|kt] [n]
"""
import sys, time
import numpy as np
from collections import Counter, defaultdict

from build_An import build_An

KNOTS = {
    "trefoil": ([1, 1, 1], 2),
    "fig8":    ([1, -2, 1, -2], 3),
    "conway":  ([-1, 2, -1, 2, -1, 3, -2, -2, -1, 3, 3], 4),
    "kt":      ([-1, 2, 2, -3, -3, 2, 1, -2, -2, 3, -2, 3, -2], 4),
}
ROOMS = {1: "1", 2: "C2", 3: "C3", 4: "C4/V4", 5: "C5", 6: "C6/S3", 7: "C7",
         10: "D5", 12: "A4", 24: "S4", 36: "3^2:4", 60: "A5", 120: "o=120",
         168: "PSL(2,7)", 360: "A6", 2520: "A7", 20160: "A8"}


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
    gs = [int(g) for g in gens]
    for g in gs:
        if not inH[g]:
            inH[g] = True; H.append(g); frontier.append(g)
    while frontier:
        a = frontier.pop()
        for b in gs:
            for c in (int(mul[a, b]), int(mul[b, a])):
                if not inH[c]:
                    inH[c] = True; H.append(c); frontier.append(c)
    return len(H)


def conj_classes(size, conj):
    """class of b = { conj[a,b] : a }  (conj[a,b] = a b a^-1); rep = min index."""
    classes = {}
    for b in range(size):
        rep = min(int(conj[a, b]) for a in range(size))
        classes.setdefault(rep, []).append(b)
    return classes


def fixed_with_x1(word, nstr, a, members, size, mul, inv, conj, ident):
    """Image orders of fixed points with x_1=a, x_2..x_n in `members`."""
    moves = [(abs(g) - 1, 1 if g > 0 else -1) for g in word]
    mem = np.array(members, dtype=np.int64)
    m = len(mem)
    out = []
    if nstr == 2:
        A = np.zeros((m, 2), dtype=np.int64)
        A[:, 0] = a; A[:, 1] = mem
        mask = np.all(apply_auto(A.copy(), moves, mul, inv, conj) == A, axis=1)
        out = [subgroup_order([a, int(mem[r])], mul, ident, size)
               for r in np.nonzero(mask)[0]]
    elif nstr == 3:
        for x2 in mem:
            A = np.zeros((m, 3), dtype=np.int64)
            A[:, 0] = a; A[:, 1] = x2; A[:, 2] = mem
            mask = np.all(apply_auto(A.copy(), moves, mul, inv, conj) == A, axis=1)
            out += [subgroup_order([a, int(x2), int(mem[r])], mul, ident, size)
                    for r in np.nonzero(mask)[0]]
    else:  # nstr == 4: loop x2, vectorize (x3,x4)
        g3 = np.repeat(mem, m); g4 = np.tile(mem, m)
        for x2 in mem:
            A = np.zeros((m * m, 4), dtype=np.int64)
            A[:, 0] = a; A[:, 1] = x2; A[:, 2] = g3; A[:, 3] = g4
            mask = np.all(apply_auto(A.copy(), moves, mul, inv, conj) == A, axis=1)
            out += [subgroup_order([a, int(x2), int(g3[r]), int(g4[r])],
                                   mul, ident, size)
                    for r in np.nonzero(mask)[0]]
    return out


def read(name, n, verbose=True):
    """Return (total, {(image_order, meridian_order): count})."""
    size, mul, inv, conj, order = build_An(n)
    word, nstr = KNOTS[name]
    ident = int(np.where(order == 1)[0][0])
    classes = conj_classes(size, conj)
    t0 = time.time()
    total = 0
    door = defaultdict(int)          # (image_order, meridian_order) -> count
    for rep, members in sorted(classes.items(), key=lambda kv: -len(kv[1])):
        h = int(order[rep])
        found = Counter(fixed_with_x1(word, nstr, rep, members, size, mul, inv, conj, ident))
        w = len(members)
        total += w * sum(found.values())
        for o, k in found.items():
            door[(o, h)] += w * k
    if verbose:
        print(f"{name} in A_{n}: |Hom| = {total}  ({time.time()-t0:.1f}s)")
        for (o, h) in sorted(door):
            print(f"    {ROOMS.get(o, 'o=%d' % o):<10} at height {h} : {door[(o,h)]}")
    return total, door


if __name__ == "__main__":
    name = sys.argv[1] if len(sys.argv) > 1 else "conway"
    n = int(sys.argv[2]) if len(sys.argv) > 2 else 7
    read(name, n)
