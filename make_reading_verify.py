#!/usr/bin/env python3
"""make_reading_verify.py — is reversal a relabeling of the onto-hands, or a new set?

The siblings' claim: the SEAM (onto-reach on the split-torus class) is the knot's —
reading-invariant; the FOLD (which pair shares a torus) is the reading's — it moves.

To test the mechanism, for each (word, p) read FORWARD and BACKWARD:
  - total onto-reach R and per-fold-pair counts
  - the fold count (hands with a doubled chord) and the spread count
  - whether R is reading-invariant (it should be: same knot group) and
    whether the fold/spread split is reading-invariant (it should NOT be).

If R is invariant but fold/spread is not, then reversal is a *relabeling*: the
onto-hands are the same object presented with a permuted generator order, so the
count (a group-level fact) survives while the pair (a generator-level fact) moves.
"""
import numpy as np
from psl import PSL
import fastkernel

WORDS = {"conway": [-1, 2, -1, 2, -1, 3, -2, -2, -1, 3, 3],
         "kt": [-1, 2, 2, -3, -3, 2, 1, -2, -2, 3, -2, 3, -2]}


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


def read_class(G, rep, C, word, p, rev):
    """onto-reach and fold/spread split for one (word, reading)."""
    if rev:
        word = list(reversed(word))
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
    fold = 0
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
            axes = [fixed_points(x, p) for x in X]
            doubled = any(axes[i] == axes[j] for i in range(4) for j in range(i + 1, 4))
            onto += osz
            if doubled:
                fold += osz
    return onto, fold


def main():
    for p in [7, 11, 13, 17, 19]:
        G = PSL(p)
        m = (p - 1) // 2
        classes = G.classes()
        reps = [rep for rep in classes if G.order(rep) == m]
        print(f"p={p}  m={m}  #split-classes={len(reps)}")
        for rep in reps:
            C = sorted(classes[rep])
            line = f"  class |C|={len(C)}"
            for name, word in WORDS.items():
                f_on, f_fold = read_class(G, rep, C, word, p, rev=False)
                b_on, b_fold = read_class(G, rep, C, word, p, rev=True)
                line += (f"\n    {name:6s} fwd: onto={f_on:3d} fold={f_fold:3d} spread={f_on-f_fold:3d}"
                         f"   rev: onto={b_on:3d} fold={b_fold:3d} spread={b_on-b_fold:3d}"
                         f"   |Δonto|={abs(f_on-b_on)}")
            print(line)


if __name__ == "__main__":
    main()
