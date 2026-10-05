#!/usr/bin/env python3
"""make_c2_into_T.py — the cleaner key for the fold threshold?

now.md open question #1: WHY does the conjugator leave N(T) at m>=6?

Hypothesis: a conjugator c INVERTS the torus (c ∈ N(T)\\T) iff its square c^2
lies back IN T.  If c ∈ N(T), then N(T)/T ≅ Z/2, so c^2 ∈ T always; and if
c ∈ T then trivially c^2 ∈ T.  So "c^2 ∈ T" is NOT the key (it's true for
everything in N(T)).  The real question is the converse direction: for c OUTSIDE
N(T), what does c^2 do?  If c^2 ∉ T exactly when c ∉ N(T), then c^2 ∈ T ⟺
c ∈ N(T), and the fold threshold is where the conjugator's square leaves T.

We evaluate each position's weave conjugator c_j as a PSL(2,p) element at every
ONTO tuple, and check: c ∈ T?  c ∈ N(T)?  c^2 ∈ T?  Classify by (inT, inN, c2inT).
The claim "c ∈ N(T) ⟺ c^2 ∈ T" would read: (inN == c2inT) everywhere.
"""
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


def main():
    for p in [7, 11, 13]:
        G = PSL(p)
        m = (p - 1) // 2
        classes = G.classes()
        reps = [rep for rep in classes if G.order(rep) == m]
        print(f"p={p} m={m}")
        for rep in reps:
            C = sorted(classes[rep])
            Tset = set()
            cur = rep
            while True:
                Tset.add(cur)
                cur = G.m(cur, rep)
                if cur == rep:
                    break
            for name, word in WORDS.items():
                atoms = track_atoms(word)
                # conjugator c_j (list of (base,sign)); the fold edge for each word
                # For each onto tuple, evaluate each c_j, classify.
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
                tally = {}
                ntally = {}
                for x2, osz in zip(x2reps, x2sizes):
                    A = np.zeros((nc * nc, 4, 4), dtype=np.int64)
                    A[:, 0, :] = rep_arr
                    A[:, 1, :] = x2
                    A[:, 2, :] = g3
                    A[:, 3, :] = g4
                    F = fastkernel.apply_auto_fast(A.copy(), moves, p)
                    mask = np.ones(nc * nc, dtype=bool)
                    for j in range(4):
                        out = F[:, j, :]
                        inp = A[:, j, :]
                        mask &= np.all((out - inp) % p == 0, axis=1) | np.all((out + inp) % p == 0, axis=1)
                    for r in np.nonzero(mask)[0]:
                        X = [rep, x2, tuple(g3[r]), tuple(g4[r])]
                        if closure(list(X), G) != G.n:
                            continue
                        for j in range(4):
                            c = eval_atoms(atoms[j][0], X, G)
                            c2 = G.m(c, c)
                            inT = c in Tset
                            # in N(T)? conjugating rep by c stays in Tset
                            inN = (G.cj(rep, c) in Tset)
                            c2inT = c2 in Tset
                            key = (inT, inN, c2inT)
                            tally[key] = tally.get(key, 0) + osz
                            # is (inN == c2inT)?
                            ntally.setdefault(inN == c2inT, 0)
                            ntally[inN == c2inT] += osz
                print(f"  {name:6s}: conj-classification {tally}")
                print(f"         'c∈N(T) ⟺ c²∈T' holds for {ntally.get(True,0)}/{ntally.get(True,0)+ntally.get(False,0)}")


if __name__ == "__main__":
    main()
