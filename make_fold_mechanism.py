#!/usr/bin/env python3
"""make_fold_mechanism.py — WHY is Conway's fold fragile, KT's robust?

The weave gives beta_hat(x_j) = c_j x_{b_j} c_j^-1, bases [3,1,4,2] forward,
[2,4,1,3] reversed.  A fold (two meridians in one torus) lands iff the
conjugator c that carries one to the other is in N(T)\\T — it inverts, so the
pair is x, x^-1.  This script tracks each position's conjugator as an atom word,
evaluates it at the ONTO fixed tuples, and reads whether it lies in T (centralizer
of the torus), N(T)\\T, or neither.  It shows the fold's fate is the conjugator's.
"""
import sys
import numpy as np
from psl import PSL, orbit_reps_sizes
import fastkernel

WORDS = {"conway": [-1, 2, -1, 2, -1, 3, -2, -2, -1, 3, 3],
         "kt": [-1, 2, 2, -3, -3, 2, 1, -2, -2, 3, -2, 3, -2]}


def reversed_word(w):
    return list(reversed(w))


def track_atoms(word):
    """Return list per position of (atoms, base).  atoms = [(gen, sign), ...]."""
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
    """evaluate an atom word in the generators X=[x1,x2,x3,x4]."""
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
    """Given an onto tuple and the fold edge (i,j), evaluate the conjugator
    that carries one to the other and classify: inT / norm(N(T)\\T) / neither.
    The relevant conjugator is at whichever position has the other as its base."""
    i, j = fold_pair
    base = X[j - 1]
    T = set(G.centralizer(base))
    NT = set()
    for g in G.reps:
        if G.cj(base, g) in T:          # g normalizes T
            NT.add(g)
    # pick the position whose base is the other index
    bases = [pos[k][1] for k in range(4)]
    if bases[i - 1] == j:
        ci = i
    elif bases[j - 1] == i:
        ci = j
    else:
        return "neither", None
    c = eval_atoms(pos[ci - 1][0], X, G)
    if c in T:
        return "inT", c
    if c in NT:
        return "norm", c
    return "neither", c


def main():
    p = int(sys.argv[1]) if len(sys.argv) > 1 else 11
    G = PSL(p)
    m = (p - 1) // 2
    classes = G.classes()
    cand = [rep for rep in classes if G.order(rep) == m]
    print(f"|PSL(2,{p})| = {G.n}   m={m}   #split-torus classes={len(cand)}")
    # Which fold edge each word means: conway (1,3), kt (3,4) -- (i, base(i))
    FOLD = {"conway": (1, 3), "kt": (3, 4)}
    for rep in cand:
        C = sorted(classes[rep])
        print(f"\n=== class |C|={len(C)} ===")
        for name, word in WORDS.items():
            for label, w in (("fwd", word), ("rev", reversed_word(word))):
                pos = track_atoms(w)
                bases = [pos[k][1] for k in range(4)]
                i, j = FOLD[name]
                # does the fold edge still exist in this reading's weave?
                # (i,j) is a base-edge iff base[i-1]==j  OR  base[j-1]==i
                edge = (bases[i - 1] == j) or (bases[j - 1] == i)
                tuples = onto_tuples(G, rep, C, w, p)
                counts = {"inT": 0, "norm": 0, "neither": 0}
                fold_hands = 0
                for X in tuples:
                    axes = [fixed_points(x, p) for x in X]
                    is_fold = axes[i - 1] == axes[j - 1]
                    if is_fold:
                        fold_hands += 1
                    k, _ = classify(G, X, (i, j), pos)
                    counts[k] += 1
                print(f"  {name:6s} {label}: onto={len(tuples)} bases={bases} "
                      f"edge={edge} fold_hands={fold_hands} "
                      f"conj: inT={counts['inT']} norm={counts['norm']} neither={counts['neither']}")


if __name__ == "__main__":
    main()
