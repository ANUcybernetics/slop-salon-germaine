#!/usr/bin/env python3
"""test_iterate.py — can (x3,x4) be recovered by iterating beta_hat on a fixed (x1,x2)?

beta_hat(x3) = c3 x4 c3^-1  and  beta_hat(x4) = c4 x2 c4^-1 (from the conjugator).
So given fixed (x1,x2), the map (x3,x4) -> (beta_hat(x1,x2,x3,x4)_3, beta_hat(...)_4)
is a candidate fixed-point iteration.  Test whether it converges to the known
beta_hat-fixed (x3,x4) for the KT 3^3 witness at A_9.
"""
import itertools
import numpy as np

CONWAY = [-1, 2, -1, 2, -1, 3, -2, -2, -1, 3, 3]
KT = [-1, 2, 2, -3, -3, 2, 1, -2, -2, 3, -2, 3, -2]


def pmul(p, q): return tuple(p[q[i]] for i in range(len(p)))
def pinv(p):
    r = [0]*len(p)
    for i in range(len(p)): r[p[i]] = i
    return tuple(r)
def psign(p):
    n = len(p); seen = [False]*n; s = 1
    for i in range(n):
        if not seen[i]:
            j = i; l = 0
            while not seen[j]: seen[j] = True; j = p[j]; l += 1
            s *= (-1)**(l-1)
    return s
def cyc(p):
    n = len(p); seen = [False]*n; parts = []
    for i in range(n):
        if not seen[i]:
            c = []; j = i
            while not seen[j]: seen[j] = True; c.append(j); j = p[j]
            if len(c) > 1: parts.append("(" + " ".join(str(x) for x in c) + ")")
    return "".join(parts) if parts else "()"


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


def main():
    # KT 3^3 witness at A_9
    x1 = from_cycles([(0, 1, 2), (3, 4, 5), (6, 7, 8)])
    x2 = from_cycles([(0, 1, 3), (2, 6, 5), (4, 8, 7)])
    x3 = from_cycles([(0, 4, 1), (2, 5, 6), (3, 8, 7)])
    x4 = from_cycles([(0, 2, 6), (1, 7, 8), (3, 4, 5)])
    witness = (x1, x2, x3, x4)
    print("witness:", [cyc(p) for p in witness])
    print("beta_hat-fixed?", apply_auto(witness, KT) == witness)

    # iterate (x3,x4) <- (beta_hat(x1,x2,x3,x4)_3, beta_hat(...)_4)
    # start from a random-ish (x3,x4)
    starts = [
        (x3, x4),  # exact
        (from_cycles([(0, 2, 4), (1, 5, 3), (6, 8, 7)]),
         from_cycles([(0, 3, 6), (1, 7, 5), (2, 8, 4)])),
    ]
    for x3s, x4s in starts:
        cur = (x3s, x4s)
        print(f"\nstart (x3,x4) = {cyc(cur[0])}, {cyc(cur[1])}")
        for it in range(12):
            X = (x1, x2, cur[0], cur[1])
            B = apply_auto(X, KT)
            new34 = (B[2], B[3])
            full_fixed = (B == X)
            print(f"  it{it}: x3={cyc(cur[0])} x4={cyc(cur[1])} "
                  f"-> new x3={cyc(new34[0])} x4={cyc(new34[1])} "
                  f"| comp12_fixed={B[0]==x1 and B[1]==x2} full_fixed={full_fixed}")
            if new34 == cur and full_fixed:
                print("  CONVERGED to full fixed point")
                break
            cur = new34


if __name__ == "__main__":
    main()
