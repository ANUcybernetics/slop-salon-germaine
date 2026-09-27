#!/usr/bin/env python3
"""probe_product.py — is P = x1 x2 x3 x4 a structural invariant of the weave?

beta_hat preserves P.  If P is (up to conjugacy or exactly) a function of the
word and the meridian class, it may be the clean handle on the weave's door.
"""
import itertools
import numpy as np

CONWAY = [-1, 2, -1, 2, -1, 3, -2, -2, -1, 3, 3]
KT = [-1, 2, 2, -3, -3, 2, 1, -2, -2, 3, -2, 3, -2]


def pmul(p, q): return tuple(p[q[i]] for i in range(len(p)))
def pinv(p):
    r = [0] * len(p)
    for i in range(len(p)): r[p[i]] = i
    return tuple(r)
def psign(p):
    n = len(p); seen = [False] * n; s = 1
    for i in range(n):
        if not seen[i]:
            j = i; l = 0
            while not seen[j]:
                seen[j] = True; j = p[j]; l += 1
            s *= (-1) ** (l - 1)
    return s
def cyc(p):
    n = len(p); seen = [False] * n; parts = []
    for i in range(n):
        if not seen[i]:
            c = []; j = i
            while not seen[j]:
                seen[j] = True; c.append(j); j = p[j]
            if len(c) > 1:
                parts.append("(" + " ".join(str(x) for x in c) + ")")
    return "".join(parts) if parts else "()"
def order(p):
    n = len(p); o = 1; seen = [False] * n
    for i in range(n):
        if not seen[i]:
            j = i; l = 0
            while not seen[j]:
                seen[j] = True; j = p[j]; l += 1
            o = (o * l) // __import__('math').gcd(o, l)
    return o
def from_cycles(cycles, n=9):
    p = list(range(n))
    for c in cycles:
        for k in range(len(c)):
            p[c[k]] = c[(k + 1) % len(c)]
    return tuple(p)


def apply_auto(tup, word):
    X = list(tup)
    for g in word:
        i = abs(g) - 1
        a, b = X[i], X[i + 1]
        if g > 0:
            X[i] = pmul(pmul(a, b), pinv(a)); X[i + 1] = a
        else:
            X[i] = b; X[i + 1] = pmul(pinv(b), pmul(a, b))
    return tuple(X)


def prod(tup):
    return pmul(pmul(tup[0], tup[1]), pmul(tup[2], tup[3]))


def class_of(a, A9):
    return set(pmul(pmul(g, a), pinv(g)) for g in A9)
def centralizer(a, A9):
    return set(g for g in A9 if pmul(pmul(g, a), pinv(g)) == a)


def vpmul(A, B): return np.take_along_axis(A, B, axis=1)
def vpinv(A): return np.argsort(A, axis=1)
def apply_auto_vec(X, moves):
    for (i, eps) in moves:
        a = X[:, i].copy(); b = X[:, i + 1].copy()
        if eps > 0:
            na = vpmul(vpmul(a, b), vpinv(a)); nb = a
        else:
            na = b; nb = vpmul(vpinv(b), vpmul(a, b))
        X[:, i] = na; X[:, i + 1] = nb
    return X


def fixed_tuples(word, a, cls, A9):
    """All beta_hat-fixed tuples with x1=a, x2,x3,x4 in cls (vectorized)."""
    moves = [(abs(g) - 1, 1 if g > 0 else -1) for g in word]
    mem = sorted(cls); m = len(mem)
    cls_arr = np.array(mem, dtype=np.int32)
    g3 = np.repeat(np.arange(m), m)
    g4 = np.tile(np.arange(m), m)
    # iterate x2 over the class too (full, not just reps, to catch all fixed)
    out = []
    a_arr = np.array(a, dtype=np.int32)
    for x2 in mem:
        x2_arr = np.array(x2, dtype=np.int32)
        X0 = np.zeros((m * m, 4, 9), dtype=np.int32)
        X0[:, 0] = a_arr; X0[:, 1] = x2_arr
        X0[:, 2] = cls_arr[g3]; X0[:, 3] = cls_arr[g4]
        X = X0.copy(); apply_auto_vec(X, moves)
        mask = np.all(X == X0, axis=(1, 2))
        for r in np.nonzero(mask)[0]:
            out.append((a, x2, mem[g3[r]], mem[g4[r]]))
    return out


def main():
    A9 = [p for p in itertools.permutations(range(9)) if psign(p) == 1]
    kt33 = (from_cycles([(0, 1, 2), (3, 4, 5), (6, 7, 8)]),
            from_cycles([(0, 1, 3), (2, 6, 5), (4, 8, 7)]),
            from_cycles([(0, 4, 1), (2, 5, 6), (3, 8, 7)]),
            from_cycles([(0, 2, 6), (1, 7, 8), (3, 4, 5)]))
    P = prod(kt33)
    print("KT witness P =", cyc(P), " order", order(P))

    # all KT fixed tuples with x1=a (the 3^3 rep), to test if P is constant
    a = kt33[0]
    cls = sorted(class_of(a, A9))
    print(f"class size {len(cls)}; sweeping for all fixed tuples ...")
    tup = fixed_tuples(KT, a, cls, A9)
    print(f"found {len(tup)} beta_hat-fixed tuples with x1=a")
    Ps = set(prod(t) for t in tup)
    print(f"distinct P values: {len(Ps)}")
    for p in sorted(Ps, key=lambda x: cyc(x))[:8]:
        print(f"   P={cyc(p)} order {order(p)}")
    # are all P conjugate? (class)
    p0 = next(iter(Ps))
    pcls = class_of(p0, A9)
    print(f"all P in one conjugacy class? {Ps <= pcls}")
    # check x4 is determined by (x1,x2,x3): count distinct (x1,x2,x3) -> x4
    from collections import defaultdict
    d = defaultdict(set)
    for t in tup:
        d[(t[0], t[1], t[2])].add(t[3])
    print(f"distinct (x1,x2,x3) with a solution: {len(d)}; "
          f"all have exactly 1 x4? {all(len(v)==1 for v in d.values())}")
    # and is x3,x4 jointly determined by (x1,x2)? i.e. distinct (x1,x2) count
    d2 = defaultdict(set)
    for t in tup:
        d2[(t[0], t[1])].add((t[2], t[3]))
    print(f"distinct (x1,x2) with a solution: {len(d2)}; "
          f"all have exactly 1 (x3,x4)? {all(len(v)==1 for v in d2.values())}")


if __name__ == "__main__":
    main()
