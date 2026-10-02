#!/usr/bin/env python3
"""psl.py — table-free PSL(2,p) for odd prime p.

Each element is the canonical coset rep of {A, -A} in SL(2,p), stored as a
tuple (a,b,c,d) mod p with det 1.  Group ops are 2x2 matrix ops mod p, then
canonicalised (lexicographically smaller of A and -A).  No |G|^2 mul table is
ever materialised, so p=37 (|G|=25308) is reachable.

Scalar ops (class/order/orbit enumeration) use plain Python; the batch
conjugation needed by the seam counter lives in the numpy helpers.
"""
import itertools


def canon_t(t, p):
    """canonical rep of the coset {t, -t} (lexicographically smaller)."""
    n = ((-t[0]) % p, (-t[1]) % p, (-t[2]) % p, (-t[3]) % p)
    return t if t < n else n


def canon4(A, p):
    """numpy (...,4) int array -> canonical coset rep of {A,-A} (lex smaller)."""
    import numpy as np
    A = np.asarray(A, dtype=np.int64) % p
    neg = (-A) % p
    lt = A < neg
    ne = A != neg
    idx = np.argmax(ne, axis=-1)
    take = np.take_along_axis(lt, idx[..., None], -1)[..., 0]
    return np.where(take[..., None], A, neg)


def smm(a, b, p):
    a0, a1, a2, a3 = a
    b0, b1, b2, b3 = b
    return canon_t(((a0 * b0 + a1 * b2) % p, (a0 * b1 + a1 * b3) % p,
                    (a2 * b0 + a3 * b2) % p, (a2 * b1 + a3 * b3) % p), p)


def sinv(a, p):
    return canon_t((a[3], (-a[1]) % p, (-a[2]) % p, a[0]), p)


def scj(a, b, p):
    """b a b^-1 (conjugand a, conjugator b)."""
    return smm(smm(b, a, p), sinv(b, p), p)


class PSL:
    def __init__(self, p):
        self.p = p
        self.id = (1 % p, 0, 0, 1 % p)
        elems = [A for A in itertools.product(range(p), repeat=4)
                 if (A[0] * A[3] - A[1] * A[2]) % p == 1]
        self.reps = sorted({canon_t(A, p) for A in elems})
        self.idx = {e: i for i, e in enumerate(self.reps)}
        self.n = len(self.reps)

    def m(self, a, b):
        return smm(a, b, self.p)

    def i(self, a):
        return sinv(a, self.p)

    def cj(self, a, b):
        return scj(a, b, self.p)

    def order(self, x):
        o, cur = 0, x
        while cur != self.id:
            cur = self.m(cur, x)
            o += 1
        return o + 1

    def classes(self):
        """all conjugacy classes as dict rep -> list of members."""
        seen = set()
        out = {}
        for x in self.reps:
            if x in seen:
                continue
            c = {self.cj(x, g) for g in self.reps}
            out[x] = sorted(c)
            seen |= c
        return out

    def cls(self, x):
        return sorted({self.cj(x, g) for g in self.reps})

    def centralizer(self, x):
        return [g for g in self.reps if self.m(g, x) == self.m(x, g)]


def orbit_reps_sizes(G, C, T):
    """T-orbits on the set C under conjugation by T.  -> (reps, sizes)."""
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


if __name__ == "__main__":
    import sys
    p = int(sys.argv[1]) if len(sys.argv) > 1 else 13
    G = PSL(p)
    print(f"|PSL(2,{p})| = {G.n}")
    classes = G.classes()
    print(f"  #classes = {len(classes)}  (formula (p+5)/2 = {(p+5)//2})")
    print(f"  class sizes = {sorted(len(v) for v in classes.values())}")
