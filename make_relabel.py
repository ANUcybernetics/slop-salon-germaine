#!/usr/bin/env python3
"""make_relabel.py — is reversal a relabeling of the onto-homomorphisms?

The siblings' claim: the SEAM (onto-reach) is the knot's — reading-invariant; the
FOLD (which pair shares a torus) is the reading's — it moves.  The sharpest
mechanism would be: the set of onto-homomorphisms is the SAME object read forward
and backward, just with the generator coordinates PERMUTED.  Then the count is
trivially invariant (it's a property of the set, not the labels) and the fold
(which names a coordinate PAIR) moves with the permutation.

We enumerate the onto-tuples for Conway's word at p=7 and p=11, forward and
backward, as sets of 4-tuples of PSL(2,p) elements.  We then ask: is there a
fixed permutation s of {0,1,2,3} such that backward-set == { s·X : X in
forward-set }?  If yes, reversal is a relabeling.  We also report which fold
pair each reading names, to show the fold moves exactly with s.
"""
import itertools
import numpy as np
from psl import PSL
import fastkernel

WORDS = {"conway": [-1, 2, -1, 2, -1, 3, -2, -2, -1, 3, 3],
         "kt": [-1, 2, 2, -3, -3, 2, 1, -2, -2, 3, -2, 3, -2]}


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


def onto_tuples(G, rep, C, word, p, rev):
    """set of onto-homomorphism 4-tuples (canonical reps), as frozenset of tuples."""
    if rev:
        word = list(reversed(word))
    moves = [(abs(g) - 1, 1 if g > 0 else -1) for g in word]
    T = [G.id]
    cur = rep
    while cur != G.id:
        T.append(cur)
        cur = G.m(cur, rep)
    x2reps, x2sizes = orbit_reps_sizes(G, C, T)
    nc = len(C)
    mem = np.array(C, dtype=np.int64)
    g3 = np.repeat(mem, nc, axis=0)
    g4 = np.tile(mem, (nc, 1))
    rep_arr = np.array(rep, dtype=np.int64)
    out = set()
    for x2, osz in zip(x2reps, x2sizes):
        A = np.zeros((nc * nc, 4, 4), dtype=np.int64)
        A[:, 0, :] = rep_arr
        A[:, 1, :] = x2
        A[:, 2, :] = g3
        A[:, 3, :] = g4
        F = fastkernel.apply_auto_fast(A.copy(), moves, p)
        mask = np.ones(nc * nc, dtype=bool)
        for j in range(4):
            o = F[:, j, :]
            i_ = A[:, j, :]
            mask &= np.all((o - i_) % p == 0, axis=1) | np.all((o + i_) % p == 0, axis=1)
        for r in np.nonzero(mask)[0]:
            X = (rep, x2, tuple(g3[r]), tuple(g4[r]))
            if closure(list(X), G) == G.n:
                out.add(X)
    return out


def apply_perm(X, s):
    return tuple(X[s[k]] for k in range(4))


def main():
    for p in [7, 11]:
        G = PSL(p)
        m = (p - 1) // 2
        classes = G.classes()
        reps = [rep for rep in classes if G.order(rep) == m]
        for rep in reps:
            C = sorted(classes[rep])
            # only classes with nonempty onto
            for name, word in WORDS.items():
                fwd = onto_tuples(G, rep, C, word, p, rev=False)
                rev = onto_tuples(G, rep, C, word, p, rev=True)
                print(f"p={p} {name:6s} class|C|={len(C)}: fwd={len(fwd)} rev={len(rev)}")
                if not fwd or not rev:
                    continue
                # find the permutation mapping fwd set to rev set
                matches = []
                for s in itertools.permutations(range(4)):
                    img = {apply_perm(X, s) for X in fwd}
                    if img == rev:
                        matches.append(s)
                print(f"    permutations mapping fwd->rev: {matches}")
                # report the fold pair in each reading (which two coords share an axis)
                def fold_pair(X):
                    from make_axis_profile import fixed_points
                    axes = [fixed_points(x, p) for x in X]
                    return [(i, j) for i in range(4) for j in range(i + 1, 4) if axes[i] == axes[j]]
                # sample one tuple
                fx = next(iter(fwd))
                rx = next(iter(rev))
                print(f"    sample fwd fold-pair: {fold_pair(fx)}   rev fold-pair: {fold_pair(rx)}")


if __name__ == "__main__":
    main()
