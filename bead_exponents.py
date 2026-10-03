#!/usr/bin/env python3
"""bead_exponents.py — label each split-torus class by the exponent j of a^j.

The split torus of PSL(2,p) is cyclic of order m=(p-1)/2.  An element a of order
m generates it; every order-m element is conjugate to some a^j, gcd(j,m)=1.
Conjugation by the normalizer inverts (a ~ a^-1), so a bead is the pair {j,m-j}.
This prints, for each order-m conjugacy class, the bead label min(j,m-j), so a
per-class reach can be indexed by exponent instead of by iteration order.
"""
import sys
from psl import PSL


def main():
    p = int(sys.argv[1])
    G = PSL(p)
    m = (p - 1) // 2
    a = next(x for x in G.reps if G.order(x) == m)
    # map each conjugate of a^j to j (only the paired label min(j,m-j))
    label = {}
    for j in range(1, m):
        if __import__("math").gcd(j, m) != 1:
            continue
        aj = G.id
        for _ in range(j):
            aj = G.m(aj, a)
        for t in G.reps:
            label.setdefault(G.cj(aj, t), min(j, m - j))
    classes = G.classes()
    cand = [rep for rep in classes if G.order(rep) == m]
    print(f"p={p} |G|={G.n} m={m} beads={len(cand)}  "
          f"bead-labels={sorted(set(label.values()))}")
    for i, rep in enumerate(cand):
        print(f"  class {i}: bead-label(j)={label.get(rep)}  |C|={len(classes[rep])}")


if __name__ == "__main__":
    main()