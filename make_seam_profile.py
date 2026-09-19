#!/usr/bin/env python3
"""make_seam_profile.py — decompose each knot's Hom(π₁, GL(3,2)) by the meridian's
conjugacy class and by the conjugation-orbit size (the centralizer of the image).

A homomorphism φ: π₁ → GL(3,2) is a fixed point of the signed Artin action on G^n.
Conjugation by G acts on these fixed points; the orbit of φ has size
|G| / |C_G(im φ)|.  The meridian is the first generator x₁, so its conjugacy class
and its order are the first shadow of φ.  The seam (Conway 1512 vs KT 1176) and the
fig-8's rise (1848) both have to live somewhere in this decomposition.

Run:  python3 make_seam_profile.py     (the n=4 counts take ~3 min each)
"""
import time

import numpy as np

from make_gl32_counts import build_GL32, apply_auto


def fixed_points(word, n, size, mul, inv, conj):
    """Return the list of fixed-point n-tuples (indices into G) of the Artin action."""
    gg = np.arange(size, dtype=np.int64)
    moves = [(abs(g) - 1, 1 if g > 0 else -1) for g in word]
    fps = []
    if n == 1:
        # single strand, no crossings: every group element is a fixed point
        fps = [(g,) for g in range(size)]
    elif n == 2:
        for g1 in range(size):
            A = np.zeros((size, n), dtype=np.int64)
            A[:, 0] = g1
            A[:, 1] = gg
            X = apply_auto(A.copy(), moves, mul, inv, conj)
            m = np.all(X == A, axis=1)
            for i in np.nonzero(m)[0]:
                fps.append((int(A[i, 0]), int(A[i, 1])))
    elif n == 3:
        for g1 in range(size):
            for g2 in range(size):
                A = np.zeros((size, n), dtype=np.int64)
                A[:, 0] = g1; A[:, 1] = g2; A[:, 2] = gg
                X = apply_auto(A.copy(), moves, mul, inv, conj)
                m = np.all(X == A, axis=1)
                for i in np.nonzero(m)[0]:
                    fps.append((int(A[i, 0]), int(A[i, 1]), int(A[i, 2])))
    else:  # n == 4
        for g1 in range(size):
            for g2 in range(size):
                A = np.zeros((size * size, n), dtype=np.int64)
                A[:, 0] = g1; A[:, 1] = g2
                A[:, 2] = np.repeat(gg, size); A[:, 3] = np.tile(gg, size)
                X = apply_auto(A.copy(), moves, mul, inv, conj)
                m = np.all(X == A, axis=1)
                for i in np.nonzero(m)[0]:
                    fps.append((int(A[i, 0]), int(A[i, 1]),
                                int(A[i, 2]), int(A[i, 3])))
    return fps


def conj_classes(size, conj):
    """Label each element by its conjugacy class (canonical = min index in class)."""
    label = np.zeros(size, dtype=np.int64)
    seen = {}
    for a in range(size):
        cls = sorted({int(conj[a, b]) for b in range(size)})
        rep = cls[0]
        label[a] = rep
    return label


def class_size(size, conj, label, a):
    return int((label == label[a]).sum())


def centralizer_order(X, size, conj):
    """|C_G(image)| = # of h conjugating every coordinate of X to itself."""
    c = 0
    for h in range(size):
        if all(conj[h, g] == g for g in X):
            c += 1
    return c


def main():
    size, mul, inv, conj, order = build_GL32()
    label = conj_classes(size, conj)
    print("|GL(3,2)| =", size)
    knots = {
        "unknot (Z)": ([], 1),
        "trefoil 3_1": ([1, 1, 1], 2),
        "fig-8 4_1": ([1, -2, 1, -2], 3),
        "Conway 11n34": ([-1, 2, -1, 2, -1, 3, -2, -2, -1, 3, 3], 4),
        "KT 11n42": ([-1, 2, 2, -3, -3, 2, 1, -2, -2, 3, -2, 3, -2], 4),
    }
    for name, (word, n) in knots.items():
        t0 = time.time()
        fps = fixed_points(word, n, size, mul, inv, conj)
        # meridian order histogram
        mer_ord = {}
        for X in fps:
            o = int(order[X[0]])
            mer_ord[o] = mer_ord.get(o, 0) + 1
        # meridian conjugacy-class histogram (class of x_1, by order and size)
        cls_hist = {}
        for X in fps:
            l = int(label[X[0]])
            o = int(order[X[0]])
            cs = class_size(size, conj, label, l)
            key = (o, cs)
            cls_hist[key] = cls_hist.get(key, 0) + 1
        # orbit-size histogram (|G|/|C_G(im)|)
        orb_hist = {}
        for X in fps:
            c = centralizer_order(X, size, conj)
            orb = size // c
            orb_hist[orb] = orb_hist.get(orb, 0) + 1
        print(f"\n{name}: total={len(fps)}  ({(time.time()-t0):.1f}s)")
        print("  meridian order :", dict(sorted(mer_ord.items())))
        print("  meridian class :", dict(sorted(cls_hist.items())))
        print("  orbit size     :", dict(sorted(orb_hist.items())))


if __name__ == "__main__":
    main()
