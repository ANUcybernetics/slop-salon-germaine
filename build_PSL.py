#!/usr/bin/env python3
"""build_PSL.py — build PSL(2,p) for an odd prime p as (size, mul, inv, conj, order)
tables, in the same format as build_An / build_SL25 / build_GL32.

PSL(2,p) = SL(2,p) / {±I}, order p(p^2-1)/2.  Elements are 2x2 matrices over F_p
with det 1, taken modulo the central -I.  A coset {M, -M} is keyed by the
lexicographically smaller of the two matrices.
"""
import itertools
import numpy as np


def build_PSL(p):
    def matmul(A, B):
        a, b, c, d = A
        e, f, g, h = B
        return ((a * e + b * g) % p, (a * f + b * h) % p,
                (c * e + d * g) % p, (c * f + d * h) % p)

    def neg(A):
        return tuple((-x) % p for x in A)

    elems = [A for A in itertools.product(range(p), repeat=4)
             if (A[0] * A[3] - A[1] * A[2]) % p == 1]
    # canonical coset rep of {A, -A}
    def canon(A):
        n = neg(A)
        return A if A < n else n
    reps = sorted({canon(A) for A in elems})
    idx = {e: i for i, e in enumerate(reps)}
    size = len(reps)
    ident = idx[canon((1, 0, 0, 1))]
    mul = np.zeros((size, size), dtype=np.int64)
    for a in range(size):
        for b in range(size):
            mul[a, b] = idx[canon(matmul(reps[a], reps[b]))]
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
    return size, mul, inv, conj, order, reps


if __name__ == "__main__":
    import sys
    p = int(sys.argv[1]) if len(sys.argv) > 1 else 11
    size, mul, inv, conj, order, reps = build_PSL(p)
    print(f"|PSL(2,{p})| = {size}  (p(p^2-1)/2 = {p*(p*p-1)//2})")
    classes = {}
    for b in range(size):
        rep = min(int(conj[a, b]) for a in range(size))
        classes.setdefault(rep, []).append(b)
    sizes = sorted(len(v) for v in classes.values())
    print(f"  #classes = {len(classes)}  (formula (p+5)/2 = {(p+5)//2})")
    print(f"  class sizes = {sizes}  sum = {sum(sizes)}")
