#!/usr/bin/env python3
"""make_fold_order_p.py — fold conjugator order spectrum for one prime p.

Avoids PSL.classes() (O(|G|^2), the bottleneck).  Instead find ONE order-m
split-torus element, compute its conjugacy class directly by conjugation, and run
the fold-order check on the beta_hat-fixed tuples.  Reaches p=23, 29.
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


def fixed_tuples(G, rep, C, word, p):
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
            out.append(([rep, x2, tuple(g3[r]), tuple(g4[r])], osz))
    return out


def main():
    p = int(sys.argv[1])
    G = PSL(p)
    m = (p - 1) // 2
    # one order-m element
    rep = next(x for x in G.reps if G.order(x) == m)
    C = sorted({G.cj(rep, g) for g in G.reps})
    print(f"p={p}  m={m}  |G|={G.n}  split-class |C|={len(C)}")
    for name, word in WORDS.items():
        for label, w in (("fwd", word), ("rev", reversed_word(word))):
            pos = track_atoms(w)
            i, j = FOLD[name]
            tups = fixed_tuples(G, rep, C, w, p)
            orders = {}
            fold_hands = 0
            for X, osz in tups:
                c, ci = fold_conjugator(G, X, (i, j), pos)
                if c is None:
                    continue
                o = G.order(c)
                orders[o] = orders.get(o, 0) + osz
                axes = [fixed_points(x, p) for x in X]
                if axes[i - 1] == axes[j - 1]:
                    fold_hands += osz
            print(f"    {name:6s} {label}: fixed={sum(t[1] for t in tups)} "
                  f"c-orders={dict(sorted(orders.items()))} "
                  f"c=2:{orders.get(2, 0)}  fold-hands={fold_hands}")


if __name__ == "__main__":
    main()
