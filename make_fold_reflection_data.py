#!/usr/bin/env python3
"""make_fold_reflection_data.py — the fold is an involution (a reflection).

For the folding reading (Conway fwd) at each p, find an onto (or beta-fixed)
tuple, read the fold conjugator c, and classify its Mobius type on P^1(F_p):

    order 2  -> reflection  (z -> a/z)  the FOLD
    order | m -> split rotation (z -> lam z), c in T (degenerate x_i=x_j)
    order | (p+1)/2 -> non-split rotation
    order p  -> shear (parabolic)

Prints a compact table + the fixed-point chord of the fold pair, for the art.
"""
import numpy as np
from psl import PSL, orbit_reps_sizes
import fastkernel

CONWAY = [-1, 2, -1, 2, -1, 3, -2, -2, -1, 3, 3]
FOLD = (1, 3)


def track_atoms(word):
    pos = [([], 1), ([], 2), ([], 3), ([], 4)]
    for g in word:
        i = abs(g) - 1
        (c1, b1), (c2, b2) = pos[i], pos[i + 1]
        if g > 0:
            newc = list(c1) + [(b1, 1)] + [(x, -s) for (x, s) in reversed(c1)] + list(c2)
            pos[i] = (newc, b2)
            pos[i + 1] = (list(c1), b1)
        else:
            pos[i] = (list(c2), b2)
            newc = list(c2) + [(b2, -1)] + [(x, -s) for (x, s) in reversed(c2)] + list(c1)
            pos[i + 1] = (newc, b1)
    return pos


def eval_atoms(atoms, X, G):
    cur = G.id
    for (gen, sign) in atoms:
        a = X[gen - 1]
        cur = G.m(cur, a if sign > 0 else G.i(a))
    return cur


def fixed_points(M, p):
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


def onto_tuples(G, rep, C, word, p):
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
    out = []
    for x2, osz in zip(x2reps, x2sizes):
        A = np.zeros((m * m, 4, 4), dtype=np.int64)
        A[:, 0, :] = rep_arr
        A[:, 1, :] = x2
        A[:, 2, :] = g3
        A[:, 3, :] = g4
        F = fastkernel.apply_auto_fast(A.copy(), moves, p)
        mask = np.ones(m * m, dtype=bool)
        for j in range(4):
            o = F[:, j, :]
            i_ = A[:, j, :]
            mask &= np.all((o - i_) % p == 0, axis=1) | np.all((o + i_) % p == 0, axis=1)
        for r in np.nonzero(mask)[0]:
            X = [rep, x2, tuple(g3[r]), tuple(g4[r])]
            if closure(list(X), G) == G.n:
                out.append((X, osz))
    return out


def mobius_type(c, G, m):
    o = G.order(c)
    p = G.p
    if o == 2:
        return "reflection"
    if o == p:
        return "shear"
    if o % m == 0 and (p - 1) % (2 * o) == 0:
        return "split-rotation"
    return "rotation"


def main():
    for p in [7, 11, 13, 17, 19, 23]:
        G = PSL(p)
        m = (p - 1) // 2
        rep = next(x for x in G.reps if G.order(x) == m)
        C = sorted({G.cj(rep, g) for g in G.reps})
        pos = track_atoms(CONWAY)
        i, j = FOLD
        # representative tuple
        rep_X = None
        try:
            tups = onto_tuples(G, rep, C, CONWAY, p)
        except Exception as e:
            tups = []
        if not tups:
            # fall back to fixed (no closure) for larger p
            print(f"p={p} m={m}: no onto tuple found via closure sweep")
            continue
        X, osz = tups[0]
        # fold conjugator
        bases = [pos[k][1] for k in range(4)]
        if bases[i - 1] == j:
            ci = i
        else:
            ci = j
        c = eval_atoms(pos[ci - 1][0], X, G)
        axes = [fixed_points(x, p) for x in X]
        typ = mobius_type(c, G, m)
        print(f"p={p} m={m}: onto={sum(t[1] for t in tups)} "
              f"c-order={G.order(c)} type={typ} "
              f"axes={axes} fold-pair-axis={axes[i-1] == axes[j-1]}")


if __name__ == "__main__":
    main()
