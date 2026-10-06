#!/usr/bin/env python3
"""make_mobius_fold.py — read the fold conjugator as a Möbius map on P^1(F_p).

The weave gives beta_hat(x_j) = c_j x_{b_j} c_j^-1.  The fold lands iff the
conjugator c that carries one member of the fold pair to the other lies in
N(T)\\T — an INVOLUTION inverting the torus (a reflection of D_m).  This script
takes each onto tuple, conjugates to the diagonal basis of the fold torus (so
T = z -> lambda z, fixing {0,inf}), and reads c's matrix there:

    diagonal      c(z) = lambda z     c in T
    anti-diagonal c(z) = lambda / z   c in N(T)\\T  (inverts -> FOLD)
    neither       c outside N(T)      spread

Then it prints, per p and word/reading, the fold conjugator's form, its order,
and whether it is an involution.  The goal: explain WHY c leaves N(T) at m>=6.
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
                out.append((X, osz))
    return out


def fold_conjugator(G, X, fold_pair, pos):
    i, j = fold_pair
    bases = [pos[k][1] for k in range(4)]
    if bases[i - 1] == j:
        ci = i
    elif bases[j - 1] == i:
        ci = j
    else:
        return None, None
    c = eval_atoms(pos[ci - 1][0], X, G)
    return c, ci


def to_diagonal_basis(G, M):
    """Mobius M on P^1(F_p): return a matrix P so P M P^-1 has the fold torus
    diagonal (fixing {0,inf}), i.e. conjugate the whole picture so the axis of
    M becomes {0,inf}.  We conjugate by the map sending M's fixed points to
    0,inf."""
    p = G.p
    axis = fixed_points(M, p)
    if len(axis) != 2:
        return None
    a, b = axis
    # map z -> (z-a)/(z-b): a->0, b->inf.  matrix [[1,-a],[1,-b]] (up to scale).
    # Normalise det to 1 for PSL: det = -b + a = a-b.
    det = (a - b) % p
    inv = pow(det, p - 2, p)
    P = (inv % p, ((-a) % p * inv) % p, (inv % p), ((-b) % p * inv) % p)
    return P


def mobius_form(c, G):
    """c as matrix tuple; classify diagonal / anti-diagonal / neither on the
    projective line (b=0 -> diagonal-ish; a=0 -> anti-diagonal)."""
    a, b, c_, d = (int(v) % G.p for v in c)
    if b % G.p == 0 and c_ % G.p == 0:
        return "diagonal"
    if a % G.p == 0 and d % G.p == 0:
        return "anti-diagonal"
    return "neither"


def main():
    p = int(sys.argv[1]) if len(sys.argv) > 1 else 11
    G = PSL(p)
    m = (p - 1) // 2
    classes = G.classes()
    cand = [rep for rep in classes if G.order(rep) == m]
    print(f"|PSL(2,{p})| = {G.n}   m={m}   #split-torus classes={len(cand)}")
    for rep in cand:
        C = sorted(classes[rep])
        print(f"\n=== class |C|={len(C)} ===")
        for name, word in WORDS.items():
            for label, w in (("fwd", word), ("rev", reversed_word(word))):
                pos = track_atoms(w)
                i, j = FOLD[name]
                tuples = onto_tuples(G, rep, C, w, p)
                # aggregate
                agg = {}
                for X, osz in tuples:
                    c, ci = fold_conjugator(G, X, (i, j), pos)
                    if c is None:
                        continue
                    # classify in T/N(T) directly
                    base = X[j - 1]
                    T = set(G.centralizer(base))
                    NT = set()
                    for g in G.reps:
                        if G.cj(base, g) in T:
                            NT.add(g)
                    in_T = c in T
                    in_NT = c in NT
                    form = "inT" if in_T else ("norm" if in_NT else "neither")
                    order = G.order(c)
                    # anti-diagonal check in diagonal basis
                    P = to_diagonal_basis(G, X[i - 1])
                    cp = G.cj(c, P) if P else c
                    mf = mobius_form(cp, G)
                    key = (form, order, mf)
                    agg[key] = agg.get(key, 0) + osz
                if agg:
                    print(f"  {name:6s} {label}: onto={sum(t[1] for t in tuples)}")
                    for (form, order, mf), cnt in sorted(agg.items()):
                        print(f"       c {form:8s} order={order:2d} mobius={mf:14s} weight={cnt}")
                    # the fold tuple axes
                    for X, osz in tuples:
                        axes = [fixed_points(x, p) for x in X]
                        fold = "FOLD" if axes[i - 1] == axes[j - 1] else "spread"
                        c, ci = fold_conjugator(G, X, (i, j), pos)
                        o = G.order(c) if c else 0
                        print(f"       e.g. axes={axes} {fold}  c order={o}")


if __name__ == "__main__":
    main()
