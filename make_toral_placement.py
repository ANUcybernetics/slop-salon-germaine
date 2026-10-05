#!/usr/bin/env python3
"""make_toral_placement.py — is the conjugator's toral placement patterned in m?

The fold lands iff the fold edge's weave conjugator c lies in N(T)\\T (it inverts
the torus, giving the pair x, x^-1).  At m=3,5 (p=7,11) that is what we saw.  The
open question: does c LEAVE N(T) as m grows, and if so is it patterned or generic?

This sweeps p = 7..31, and for each (word, reading) reads the classification of the
fold conjugator at EVERY onto tuple: inT / norm(N(T)\\T) / neither.  It also reports
whether the classification is *constant* across tuples or varies.  Constant-and-norm
at the small m's, constant-and-neither at the large ones, is a law; a spread is drift.
"""
import sys
import numpy as np
from psl import PSL, orbit_reps_sizes
import fastkernel

WORDS = {"conway": [-1, 2, -1, 2, -1, 3, -2, -2, -1, 3, 3],
         "kt": [-1, 2, 2, -3, -3, 2, 1, -2, -2, 3, -2, 3, -2]}
FOLD = {"conway": (1, 3), "kt": (3, 4)}


def reversed_word(w):
    return list(reversed(w))


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
                out.append(X)
    return out


def classify(G, X, fold_pair, pos):
    i, j = fold_pair
    base = X[j - 1]
    T = set(G.centralizer(base))
    NT = set()
    for g in G.reps:
        if G.cj(base, g) in T:
            NT.add(g)
    bases = [pos[k][1] for k in range(4)]
    if bases[i - 1] == j:
        ci = i
    elif bases[j - 1] == i:
        ci = j
    else:
        return "noedge", None
    c = eval_atoms(pos[ci - 1][0], X, G)
    if c in T:
        return "inT", c
    if c in NT:
        return "norm", c
    return "neither", c


def main():
    primes = [7, 11, 13, 17, 19, 23, 29, 31]
    print(f"{'p':>3} {'m':>2} {'word':>6} {'rd':>3} {'onto':>4}  "
          f"class-dist (inT/norm/neither)  fold")
    for p in primes:
        G = PSL(p)
        m = (p - 1) // 2
        classes = G.classes()
        cand = [rep for rep in classes if G.order(rep) == m]
        if not cand:
            print(f"{p:>3} {m:>2}  (no order-{m} class)")
            continue
        # take the first split-torus class rep
        rep = cand[0]
        C = sorted(classes[rep])
        for name, word in WORDS.items():
            for label, w in (("fwd", word), ("rev", reversed_word(word))):
                pos = track_atoms(w)
                i, j = FOLD[name]
                tuples = onto_tuples(G, rep, C, w, p)
                if not tuples:
                    print(f"{p:>3} {m:>2} {name:>6} {label:>3} {0:>4}  "
                          f"(no onto tuples)")
                    continue
                dist = {"inT": 0, "norm": 0, "neither": 0}
                folds = 0
                for X in tuples:
                    axes = [fixed_points(x, p) for x in X]
                    if axes[i - 1] == axes[j - 1]:
                        folds += 1
                    k, _ = classify(G, X, (i, j), pos)
                    dist[k] += 1
                const = sum(1 for v in dist.values() if v > 0) <= 1
                print(f"{p:>3} {m:>2} {name:>6} {label:>3} {len(tuples):>4}  "
                      f"{dist['inT']}/{dist['norm']}/{dist['neither']}   "
                      f"{'CONST' if const else 'spread'}   fold={folds}")
        print()


if __name__ == "__main__":
    main()
