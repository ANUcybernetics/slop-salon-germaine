#!/usr/bin/env python3
"""make_psl13_seam.py — where exactly do Conway and KT part in PSL(2,13)?

mina/rahel claim the seam is ONE class deep (the split-torus, order (p-1)/2=6).
This computes, for EACH meridian class, the number of beta-hat-fixed tuples
(x1=rep, x2,x3,x4 in class) for both words, and reports the difference.
|Hom| = sum over classes of |C| * N(C); the seam is the class where N differs.
"""
import time
import numpy as np
from collections import Counter
from build_PSL import build_PSL

WORDS = {"conway": [-1, 2, -1, 2, -1, 3, -2, -2, -1, 3, 3],
         "kt": [-1, 2, 2, -3, -3, 2, 1, -2, -2, 3, -2, 3, -2]}


def apply_auto(X, moves, mul, inv, conj):
    for (i, eps) in moves:
        a = X[:, i].copy(); b = X[:, i + 1].copy()
        if eps > 0:
            na = conj[a, b]; nb = a
        else:
            na = b; nb = conj[inv[b], a]
        X[:, i] = na; X[:, i + 1] = nb
    return X


def per_class_counts(size, mul, inv, conj, order, word):
    moves = [(abs(g) - 1, 1 if g > 0 else -1) for g in word]
    # conjugacy classes: rep -> members
    classes = {}
    for b in range(size):
        rep = min(int(conj[a, b]) for a in range(size))
        classes.setdefault(rep, []).append(b)
    res = {}
    for rep, members in classes.items():
        m = len(members)
        mem = np.array(members, dtype=np.int64)
        g3 = np.repeat(mem, m); g4 = np.tile(mem, m)
        A = np.zeros((m * m, 4), dtype=np.int64)
        A[:, 0] = rep; A[:, 2] = g3; A[:, 3] = g4
        cnt = 0
        # x2 ranges over the whole class
        for x2 in members:
            A[:, 1] = x2
            mask = np.all(apply_auto(A.copy(), moves, mul, inv, conj) == A, axis=1)
            cnt += int(np.count_nonzero(mask))
        res[rep] = cnt
    return res, classes


def main():
    size, mul, inv, conj, order, reps = build_PSL(13)
    print(f"|PSL(2,13)| = {size},  #classes = {len(set(min(int(conj[a,b]) for a in range(size)) for b in range(size)))}")
    cc, classes = per_class_counts(size, mul, inv, conj, order, WORDS["conway"])
    kc, _ = per_class_counts(size, mul, inv, conj, order, WORDS["kt"])
    # report per class
    print(f"{'order':>6} {'|C|':>5} {'N_conway':>9} {'N_kt':>7} {'|C|*d':>9}  seam?")
    tot_c = tot_k = 0
    for rep, members in classes.items():
        C = len(members)
        nc, nk = cc[rep], kc[rep]
        tot_c += C * nc; tot_k += C * nk
        d = C * (nc - nk)
        print(f"{int(order[rep]):>6} {C:>5} {nc:>9} {nk:>7} {d:>9}  {'<-- SEAM' if d else ''}")
    print(f"\n|Hom| Conway = {tot_c} = x{tot_c//size} * |G|")
    print(f"|Hom| KT     = {tot_k} = x{tot_k//size} * |G|")


if __name__ == "__main__":
    main()
