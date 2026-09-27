#!/usr/bin/env python3
"""trace_weave.py — trace the KT word on the witness, move by move.

Goal: see how (x3,x4) is DETERMINED by (x1,x2).  Each move changes two adjacent
coordinates.  By watching which coordinates are free vs pinned as we pass the
word, we find the "peel from the end" solve.
"""
import itertools

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
def from_cycles(cycles, n=9):
    p = list(range(n))
    for c in cycles:
        for k in range(len(c)):
            p[c[k]] = c[(k + 1) % len(c)]
    return tuple(p)


def step(tup, g):
    X = list(tup)
    i = abs(g) - 1
    a, b = X[i], X[i + 1]
    if g > 0:
        X[i] = pmul(pmul(a, b), pinv(a)); X[i + 1] = a
    else:
        X[i] = b; X[i + 1] = pmul(pinv(b), pmul(a, b))
    return tuple(X)


witness = (from_cycles([(0, 1, 2), (3, 4, 5), (6, 7, 8)]),
           from_cycles([(0, 1, 3), (2, 6, 5), (4, 8, 7)]),
           from_cycles([(0, 4, 1), (2, 5, 6), (3, 8, 7)]),
           from_cycles([(0, 2, 6), (1, 7, 8), (3, 4, 5)]))

print("KT word trace on witness (only changed coords shown):")
print("   start x1=%s x2=%s x3=%s x4=%s" % tuple(cyc(p) for p in witness))
T = witness
for k, g in enumerate(KT, 1):
    old = T
    T = step(T, g)
    changed = [j for j in range(4) if old[j] != T[j]]
    i = abs(g) - 1
    print(f"   {k:2d} σ{abs(g)}{'+' if g>0 else '-'} (affects x{i+1},x{i+2})"
          f" -> changed {['x%d'%(j+1) for j in changed]}")
    for j in changed:
        print(f"        x{j+1} = {cyc(T[j])}")
print("   end:", [cyc(p) for p in T])
print("   == start?", T == witness)
