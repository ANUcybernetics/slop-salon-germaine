#!/usr/bin/env python3
"""make_gl32_counts.py — count homomorphisms of a braid-closure knot group into G.

The knot group of a braid closure <x_1…x_n | x_i = β̄(x_i)>, β̄ the signed Artin
action of the braid on the free group.  Homomorphisms to a finite group G are the
fixed points of β̄ acting on G^n.  To count them we never expand the words (the
expanded β̄(x_i) for a 13-letter braid is a wall of letters); instead we apply the
elementary Artin moves to an *array* of n-tuples, move by move, and count fixed
points with numpy:

  σ_i : (g_i, g_{i+1}) → (g_i g_{i+1} g_i⁻¹, g_i)
  σ_i⁻¹: (g_i, g_{i+1}) → (g_{i+1}, g_{i+1}⁻¹ g_i g_{i+1})

N.B. the σ_i⁻¹ move is the one that makes or breaks it: `g_{i+1}⁻¹ g_i g_{i+1}`,
NOT `g_i g_{i+1} g_i⁻¹`.  A count that lands *exactly* on |G| for two distinct
knots is a red flag, not a pass — that is exactly what the wrong move produced.

GL(3,2), the Fano plane's group (order 168), is the finite shadow that reads the
Conway / Kinoshita–Terasaka seam:

  Conway 11n34 : 1512  = 9 × 168
  KT     11n42 : 1176  = 7 × 168

while every group of order ≤ 24 (S₃, A₄, D₈, S₄) gives both exactly |G|, the
abelianization floor.  `make_fano_lens.py` draws the reading.

Run:  python3 make_gl32_counts.py            (the n=4 counts take ~3min each)
"""
import itertools
import time

import numpy as np

# ---- GL(3,2) as tables -------------------------------------------------------
def build_GL32():
    def matmul(A, B):
        return tuple(tuple(sum(A[i][k] * B[k][j] for k in range(3)) % 2
                           for j in range(3)) for i in range(3))

    def is_inv(A):
        (a, b, c), (d, e, f), (g, h, i) = A
        det = (a * (e * i - f * h) - b * (d * i - f * g) + c * (d * h - e * g)) % 2
        return det == 1

    elems = []
    for A in itertools.product(itertools.product((0, 1), repeat=3), repeat=3):
        if is_inv(A):
            elems.append(A)
    idx = {e: i for i, e in enumerate(elems)}
    size = len(elems)
    ident = idx[tuple(tuple(1 if r == c else 0 for c in range(3)) for r in range(3))]
    mul = np.zeros((size, size), dtype=np.int64)
    for a in range(size):
        for b in range(size):
            mul[a, b] = idx[matmul(elems[a], elems[b])]
    inv = np.zeros(size, dtype=np.int64)
    for a in range(size):
        for b in range(size):
            if mul[a, b] == ident:
                inv[a] = b
    conj = np.zeros((size, size), dtype=np.int64)
    for a in range(size):
        for b in range(size):
            conj[a, b] = mul[mul[a, b], inv[a]]
    order = np.zeros(size, dtype=np.int64)
    for a in range(size):
        o = 1
        cur = a
        while cur != ident:
            cur = mul[cur, a]
            o += 1
            if o > size + 1:
                break
        order[a] = o
    return size, mul, inv, conj, order


def apply_auto(X, moves, mul, inv, conj):
    """Apply the signed Artin automorphism move-by-move to rows of X (each row a
    tuple of group indices).  X is modified in place."""
    for (i, eps) in moves:
        a = X[:, i].copy()
        b = X[:, i + 1].copy()
        if eps > 0:
            na = conj[a, b]        # g_i g_{i+1} g_i⁻¹
            nb = a
        else:
            na = b
            nb = conj[inv[b], a]   # g_{i+1}⁻¹ g_i g_{i+1}
        X[:, i] = na
        X[:, i + 1] = nb
    return X


def count(word, n, size, mul, inv, conj, order, mer_ord=None):
    """Return (total, meridian_order_mer_ord) homomorphisms."""
    gg = np.arange(size, dtype=np.int64)
    moves = [(abs(g) - 1, 1 if g > 0 else -1) for g in word]
    total = c_mer = 0
    if n == 2:
        for g1 in range(size):
            A = np.zeros((size, n), dtype=np.int64)
            A[:, 0] = g1; A[:, 1] = gg
            X = apply_auto(A.copy(), moves, mul, inv, conj)
            m = np.all(X == A, axis=1)
            total += int(m.sum())
            if mer_ord is not None:
                c_mer += int((m & (order[A[:, 0]] == mer_ord)).sum())
    elif n == 3:
        for g1 in range(size):
            for g2 in range(size):
                A = np.zeros((size, n), dtype=np.int64)
                A[:, 0] = g1; A[:, 1] = g2; A[:, 2] = gg
                X = apply_auto(A.copy(), moves, mul, inv, conj)
                m = np.all(X == A, axis=1)
                total += int(m.sum())
                if mer_ord is not None:
                    c_mer += int((m & (order[A[:, 0]] == mer_ord)).sum())
    else:  # n == 4
        for g1 in range(size):
            for g2 in range(size):
                A = np.zeros((size * size, n), dtype=np.int64)
                A[:, 0] = g1; A[:, 1] = g2
                A[:, 2] = np.repeat(gg, size); A[:, 3] = np.tile(gg, size)
                X = apply_auto(A.copy(), moves, mul, inv, conj)
                m = np.all(X == A, axis=1)
                total += int(m.sum())
                if mer_ord is not None:
                    c_mer += int((m & (order[A[:, 0]] == mer_ord)).sum())
    return total, c_mer


def main():
    size, mul, inv, conj, order = build_GL32()
    print("|GL(3,2)| =", size)
    # braid words (signed generator indices, n = max index + 1)
    knots = {
        "unknot (Z)": ([], 1),
        "trefoil 3_1": ([1, 1, 1], 2),
        "fig-8 4_1": ([1, -2, 1, -2], 3),
        "Conway 11n34": ([-1, 2, -1, 2, -1, 3, -2, -2, -1, 3, 3], 4),
        "KT 11n42": ([-1, 2, 2, -3, -3, 2, 1, -2, -2, 3, -2, 3, -2], 4),
    }
    for name, (word, n) in knots.items():
        t0 = time.time()
        tot, c7 = count(word, n, size, mul, inv, conj, order, mer_ord=7)
        print(f"  {name:<16} total={tot:>6}  mer7={c7:>6}  ({(time.time()-t0):.1f}s)")


if __name__ == "__main__":
    main()
