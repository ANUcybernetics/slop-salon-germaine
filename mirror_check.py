#!/usr/bin/env python3
"""mirror_check.py — is the count (β̂-fixed) blind to the hand (mirror) at small n?

The mirror of a braid closure is the closure of the word with every σ_i
flipped (σ_i <-> σ_i^-1).  We compare the β̂-fixed count into A_5 and A_6 for a
word and its mirror.  If the count is equal, the count is hand-blind at that n.

This is the cheap half of the "two lenses, one threshold" claim: below A_7 the
count reads the mutants the same (seam-blind) AND a knot the same as its mirror
(hand-blind).  It is the Jones, not the count, that names the hand.
"""
import itertools, time, sys
import numpy as np

CONWAY = [-1, 2, -1, 2, -1, 3, -2, -2, -1, 3, 3]
KT = [-1, 2, 2, -3, -3, 2, 1, -2, -2, 3, -2, 3, -2]


def mirror(w): return [-g for g in w]


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
def vpmul(A, B): return np.take_along_axis(A, B, axis=1)
def vpinv(A): return np.argsort(A, axis=1)
def apply_auto_vec(X, moves):
    for (i, eps) in moves:
        a = X[:, i].copy(); b = X[:, i+1].copy()
        if eps > 0:
            na = vpmul(vpmul(a, b), vpinv(a)); nb = a
        else:
            na = b; nb = vpmul(vpinv(b), vpmul(a, b))
        X[:, i] = na; X[:, i+1] = nb
    return X


def total_fixed(word, A, N):
    """Total β̂-fixed tuples in A^4 (generators share a class for an n-cycle perm)."""
    moves = [(abs(g)-1, 1 if g > 0 else -1) for g in word]
    members = list(A); m = len(members)
    mem = np.array(members, dtype=np.int64)
    idx = np.arange(m)
    g2 = np.repeat(idx, m); g3 = np.tile(idx, m)           # (x2,x3) mesh for one x1
    total = 0
    for x1 in range(m):
        # enumerate (x2,x3,x4) in A^3 for this x1, chunked by x2
        X0 = np.zeros((m*m, 4, N), dtype=np.int8)
        X0[:, 0] = mem[x1]
        X0[:, 1] = mem[g2]; X0[:, 2] = mem[g3]
        # loop x4 in chunks to keep memory low
        for x4 in range(m):
            X0[:, 3] = mem[x4]
            X = X0.copy(); apply_auto_vec(X, moves)
            mask = np.all(X == X0, axis=(1, 2))
            total += int(mask.sum())
    return total


def main():
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    A = [p for p in itertools.permutations(range(N)) if psign(p) == 1]
    print(f"=== A_{N} (|A|={len(A)}) ===")
    t0 = time.time()
    for name, w in (("Conway", CONWAY), ("KT", KT)):
        c = total_fixed(w, A, N)
        cm = total_fixed(mirror(w), A, N)
        print(f"  {name}: word={c}  mirror={cm}  equal={c==cm}")
    print(f"  ({time.time()-t0:.1f}s)")


if __name__ == "__main__":
    main()
