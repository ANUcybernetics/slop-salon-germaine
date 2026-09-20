#!/usr/bin/env python3
"""make_A5.py — build A5 (the icosahedral/even-permutation group, order 60) as
tables in the same (size, mul, inv, conj, order) format as build_GL32.

A5 carries a 5-tooth (5 | 60) that GL(3,2) lacks.  Its involutions are the 15
double transpositions, and the product of two double transpositions has order in
{1,2,3,5} — so a knot's determinant (odd) can select D3 (order 3) *or* D5
(order 10) as a dihedral tooth here, where through GL(3,2) only D3=S3 was
possible.  This is the lens-locality test for the det law.

Run:  python3 make_A5.py            (build + sanity)
"""
import itertools
from collections import Counter

import numpy as np


def perm_mul(p, q):
    return tuple(p[q[i]] for i in range(len(p)))


def perm_inv(p):
    r = [0] * len(p)
    for i in range(len(p)):
        r[p[i]] = i
    return tuple(r)


def perm_order(p):
    """Order of a permutation (lcm of cycle lengths)."""
    n = len(p)
    seen = [False] * n
    o = 1
    for i in range(n):
        if not seen[i]:
            j = i
            l = 0
            while not seen[j]:
                seen[j] = True
                j = p[j]
                l += 1
            o = o * l // __import__("math").gcd(o, l)
    return o


def perm_sign(p):
    n = len(p)
    seen = [False] * n
    s = 1
    for i in range(n):
        if not seen[i]:
            j = i
            l = 0
            while not seen[j]:
                seen[j] = True
                j = p[j]
                l += 1
            s *= (-1) ** (l - 1)
    return s


def build_A5():
    """Return (size, mul, inv, conj, order) tables for A5."""
    elems = [p for p in itertools.permutations(range(5)) if perm_sign(p) == 1]
    idx = {e: i for i, e in enumerate(elems)}
    size = len(elems)
    ident = idx[tuple(range(5))]
    mul = np.zeros((size, size), dtype=np.int64)
    for a in range(size):
        for b in range(size):
            mul[a, b] = idx[perm_mul(elems[a], elems[b])]
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
        order[a] = perm_order(elems[a])
    return size, mul, inv, conj, order


def name_subgroup_A5(elems, size, mul, inv, ident, order):
    """Name a subgroup of A5 up to isomorphism by order + structure."""
    gen = sorted(set(elems))
    H = {ident}
    frontier = [ident]
    for g in gen:
        if g not in H:
            H.add(g)
            frontier.append(g)
    while frontier:
        a = frontier.pop()
        for b in gen:
            for c in (mul[a, b], mul[b, a], inv[b]):
                if c not in H:
                    H.add(c)
                    frontier.append(c)
    o = len(H)
    if o == 1:
        return "1"
    if o == 2:
        return "Z2"
    if o == 3:
        return "Z3"
    if o == 4:
        return "V4"
    if o == 5:
        return "Z5"
    if o == 6:
        return "S3"          # D3
    if o == 10:
        return "D5"
    if o == 12:
        return "A4"
    if o == 60:
        return "A5"
    return f"ord{o}"


if __name__ == "__main__":
    size, mul, inv, conj, order = build_A5()
    print("|A5| =", size)
    print("|A5| = 60 ; primes {2,3,5} ; non-abelian subgroups: S3(6)=D3, D5(10), A4(12), A5(60).")
    # involution (order-2) product-order distribution, the det-law's raw material
    dt = [a for a in range(size) if order[a] == 2]
    c = Counter()
    for a in dt:
        for b in dt:
            c[int(order[mul[a, b]])] += 1
    print("order(ab) for two order-2 elements:", dict(sorted(c.items())))
    print("det odd -> order(ab) odd -> possible dihedral teeth:",
          sorted(k for k in c if k % 2 == 1 and k > 1))
