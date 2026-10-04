#!/usr/bin/env python3
"""verify_fold_inverse.py — test the fold lemma: in every onto-hand, two
meridians lie in one torus (share an axis) ONLY IF they are inverses.

Why it should hold: the weave gives beta_hat(x_j) = c_j x_{b_j} c_j^-1 with
bases [3,1,4,2], so all four meridians are mutually conjugate.  If two of them
x_i, x_j lie in a common torus T (their centralizer), then the weave word w with
x_j = w x_i w^-1 sends T to itself, so w in N(T) = D_{2m}, which acts on T by
identity (w in T -> x_j = x_i) or inversion (w in N(T)\\T -> x_j = x_i^-1).
Distinct meridians -> inverse.

The probe also records WHICH pair folds, and whether it is a weave-adjacent
pair (x_j with x_{b_j}, the direct base of the fixed-point equation).
"""
import sys
import numpy as np
from psl import PSL
import fastkernel

WORDS = {"conway": [-1, 2, -1, 2, -1, 3, -2, -2, -1, 3, 3],
         "kt": [-1, 2, 2, -3, -3, 2, 1, -2, -2, 3, -2, 3, -2]}
BASES = [3, 1, 4, 2]          # beta_hat(x_j) is conjugate to x_{bases[j-1]}


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


def run(G, rep, C, word, p):
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
    onto = 0
    fold_inverse = 0
    fold_noninv = 0
    pairs_seen = {}
    noninv_example = None
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
            if closure(list(X), G) != G.n:
                continue
            onto += osz
            axes = [fixed_points(x, p) for x in X]
            for i in range(4):
                for j in range(i + 1, 4):
                    if axes[i] == axes[j]:
                        inv = G.m(X[i], X[j]) == G.id
                        adjacent = (j + 1 == BASES[i]) or (i + 1 == BASES[j])
                        key = (i + 1, j + 1)
                        pairs_seen.setdefault(key, [0, 0, 0])
                        pairs_seen[key][0] += osz
                        if inv:
                            pairs_seen[key][1] += osz
                            fold_inverse += osz
                        else:
                            pairs_seen[key][2] += osz
                            fold_noninv += osz
                            if noninv_example is None:
                                noninv_example = (X, (i + 1, j + 1))
    return onto, fold_inverse, fold_noninv, pairs_seen, noninv_example


def main():
    p = int(sys.argv[1]) if len(sys.argv) > 1 else 11
    G = PSL(p)
    print(f"|PSL(2,{p})| = {G.n}   m=(p-1)/2 = {(p - 1) // 2}")
    m = (p - 1) // 2
    classes = G.classes()
    cand = [rep for rep in classes if G.order(rep) == m]
    for rep in cand:
        C = sorted(classes[rep])
        print(f"\n  class order {m}  |C|={len(C)}")
        for name, word in WORDS.items():
            onto, inv, noninv, pairs, ex = run(G, rep, C, word, p)
            print(f"    {name:6s}: onto={onto}  fold-inverse={inv}  fold-NONinverse={noninv}")
            for key in sorted(pairs):
                print(f"        pair x{key[0]}·x{key[1]}: {pairs[key][0]} hands, "
                      f"{pairs[key][1]} inverse, {pairs[key][2]} non-inverse")


if __name__ == "__main__":
    main()
