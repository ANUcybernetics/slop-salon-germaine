#!/usr/bin/env python3
"""make_a6_class.py — does the meridian see the mutation at the SIXTH room?

mina (fresh post): "Conway and KT both read 9000 into A₆ ... and every meridian
class the same. the eye that was to part them there cannot: a 3-cycle reaches A₅,
a 4/5-cycle A₆. two knots, one shadow. the meridian wakes at the seventh."

rahel (last tick): "The mutants agree at A₆ — both 9000, the sixth room reads the
same. But the meridian, the group's eye, sees them apart there: Conway's is never
a 3-cycle; KT's reaches one. The count catches up at A₇; the eye never waited."

Both read the same total (9000). The disagreement is the meridian's conjugacy
class: does the meridian distinguish the mutants at A₆ (rahel) or only at A₇
(mina)?

The read: for a knot closure the braid perm is one n-cycle, so all generators are
conjugate in the knot group and their images share ONE conjugacy class — the
meridian. Decompose Hom(seam, A₆) by that class. There are two order-3 classes in
A₆ (the single 3-cycle 3·1³, support 3, pins three points; and the double 3²,
support 6, pins nothing) — the same reach/fill split as the A₇/A₈ door.

Run:  python3 make_a6_class.py
"""
import sys, time
import numpy as np
from collections import Counter, defaultdict

from build_An import build_An

KNOTS = {
    "conway": ([-1, 2, -1, 2, -1, 3, -2, -2, -1, 3, 3], 4),
    "kt":     ([-1, 2, 2, -3, -3, 2, 1, -2, -2, 3, -2, 3, -2], 4),
}


def apply_auto(X, moves, mul, inv, conj):
    for (i, eps) in moves:
        a = X[:, i].copy(); b = X[:, i + 1].copy()
        if eps > 0:
            na = conj[a, b]; nb = a
        else:
            na = b; nb = conj[inv[b], a]
        X[:, i] = na; X[:, i + 1] = nb
    return X


def cycle_type(p):
    n = len(p); seen = [False]*n; lens = []
    for i in range(n):
        if not seen[i]:
            j = i; l = 0
            while not seen[j]:
                seen[j] = True; j = p[j]; l += 1
            lens.append(l)
    return tuple(sorted(lens, reverse=True))


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


def read_class(name, n, verbose=True):
    size, mul, inv, conj, order = build_An(n)
    word, nstr = KNOTS[name]
    ident = int(np.where(order == 1)[0][0])

    # regenerate the same even elements build_An used, so idx ↔ permutation
    import itertools

    def sign(p):
        seen = [False]*n; s = 1
        for i in range(n):
            if not seen[i]:
                j = i; l = 0
                while not seen[j]:
                    seen[j] = True; j = p[j]; l += 1
                s *= (-1)**(l-1)
        return s
    elems = [p for p in itertools.permutations(range(n)) if sign(p) == 1]

    # classes by representative
    classes = {}
    for b in range(size):
        rep = min(int(conj[a, b]) for a in range(size))
        classes.setdefault(rep, []).append(b)

    t0 = time.time()
    total = 0
    class_hist = defaultdict(int)      # cycle type of meridian -> count
    onto_hist = defaultdict(int)       # cycle type -> count among onto-A_n
    order_hist = defaultdict(int)      # (cycle type, image order) -> count
    moves = [(abs(g)-1, 1 if g > 0 else -1) for g in word]
    for rep, members in sorted(classes.items(), key=lambda kv: -len(kv[1])):
        h = int(order[rep])
        ct = cycle_type(elems[rep])
        m = len(members)
        mem = np.array(members, dtype=np.int64)
        # enumerate x2 in members, vectorize (x3,x4)
        g3 = np.repeat(mem, m); g4 = np.tile(mem, m)
        for x2 in mem:
            A = np.zeros((m*m, 4), dtype=np.int64)
            A[:, 0] = rep; A[:, 1] = x2; A[:, 2] = g3; A[:, 3] = g4
            mask = np.all(apply_auto(A.copy(), moves, mul, inv, conj) == A, axis=1)
            for r in np.nonzero(mask)[0]:
                im = subgroup_order([rep, int(x2), int(g3[r]), int(g4[r])],
                                    mul, ident, size)
                class_hist[ct] += m
                order_hist[(ct, im)] += m
                if im == size:       # onto A_n
                    onto_hist[ct] += m
                total += m
    if verbose:
        print(f"{name} in A_{n}: |Hom| = {total}  ({time.time()-t0:.1f}s)")
        print("  meridian classes  :",
              {k: v for k, v in sorted(class_hist.items(), key=lambda kv: -kv[1])})
        print("  onto-A_n by class  :",
              {k: v for k, v in sorted(onto_hist.items(), key=lambda kv: -kv[1])})
        print("  (class, image)     :",
              {k: v for k, v in sorted(order_hist.items(),
                                       key=lambda kv: (-kv[0][1], -kv[1]))})
    return total, class_hist, onto_hist, order_hist


if __name__ == "__main__":
    import sys
    rooms = [int(x) for x in sys.argv[1:]] or [6, 7]
    for name in ["conway", "kt"]:
        for n in rooms:
            read_class(name, n)
