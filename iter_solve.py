#!/usr/bin/env python3
"""iter_solve.py — solve beta_hat(X)=X for (x3,x4) given fixed (x1,x2) by iterating
the conjugator equations.

beta_hat(x_j) = c_j x_{b_j} c_j^-1 where c_j is a conjugator WORD (list of
(base, sign) atoms).  The fixed conditions are:
    x3 = c1^-1 x1 c1     (from x1 = c1 x3 c1^-1)
    x4 = c3^-1 x3 c3     (from x3 = c3 x4 c3^-1)
Iterate: X^k -> x3^{k+1} = c1(X^k)^-1 x1 c1(X^k), x4^{k+1} = c3(...)^-1 x3^{k+1} c3(...).
If it converges to a point where ALL FOUR components of beta_hat(X) equal X, we
have a full beta_hat-fixed tuple — and we've avoided the m^2 grid.
"""
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


def beta_conj(X, word):
    """Return list of (conjugator_atoms, base).  value = c x_base c^-1."""
    pos = [([], i) for i in range(4)]  # (conjugator atoms, base index)
    for g in word:
        i = abs(g) - 1
        (c1, b1) = pos[i]; (c2, b2) = pos[i + 1]
        if g > 0:
            # new pos i = (c1 x_b1 c1^-1 c2) x_b2 (..)^-1
            newc = list(c1) + [(b1, 1)] + [(x, -s) for (x, s) in reversed(c1)] + list(c2)
            pos[i] = (newc, b2)
            pos[i + 1] = (list(c1), b1)
        else:
            pos[i] = (list(c2), b2)
            newc = list(c2) + [(b2, -1)] + [(x, -s) for (x, s) in reversed(c2)] + list(c1)
            pos[i + 1] = (newc, b1)
    return pos


def eval_conj(conj, X):
    """Evaluate a conjugator word (list of (base, sign) atoms) with the tuple X."""
    out = None
    for (b, s) in conj:
        g = X[b] if s > 0 else pinv(X[b])
        out = g if out is None else pmul(out, g)
    return tuple(range(len(X[0]))) if out is None else out


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

    # Get conjugators c1, c3 for the witness (should be the fixed config)
    pos = beta_conj(witness, KT)
    for k, (c, b) in enumerate(pos):
        print(f"  beta_hat(x{k+1}) base={b+1}  conj len={len(c)}")

    # Iterate the solver from a random (x3,x4)
    starts = [
        (x3, x4),
        (from_cycles([(0, 2, 4), (1, 5, 3), (6, 8, 7)]),
         from_cycles([(0, 3, 6), (1, 7, 5), (2, 8, 4)])),
    ]
    for x3s, x4s in starts:
        print(f"\nstart x3={cyc(x3s)} x4={cyc(x4s)}")
        cur = (x3s, x4s)
        for it in range(15):
            X = (x1, x2, cur[0], cur[1])
            pos = beta_conj(X, KT)
            c1 = eval_conj(pos[0][0], X)  # conjugator of beta_hat(x1)
            c3 = eval_conj(pos[2][0], X)  # conjugator of beta_hat(x3)
            c1i = pinv(c1)
            nx3 = pmul(pmul(c1i, x1), c1)     # x3' = c1^-1 x1 c1
            c3i = pinv(c3)
            nx4 = pmul(pmul(c3i, nx3), c3)    # x4' = c3^-1 x3' c3
            B = apply_auto(X, KT)
            full = (B == X)
            print(f"  it{it}: x3={cyc(cur[0])} x4={cyc(cur[1])} -> "
                  f"x3={cyc(nx3)} x4={cyc(nx4)} full_fixed={full}")
            if (nx3, nx4) == cur and full:
                print("  CONVERGED")
                break
            cur = (nx3, nx4)


if __name__ == "__main__":
    main()
