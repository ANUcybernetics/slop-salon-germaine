#!/usr/bin/env python3
"""verify_rung_fold.py — direct check of the fold claim, no axis machinery.

The axis reading says: an onto-hand FOLDS iff two of its four meridians
commute (lie in one torus).  Verify the sharp cases by hand:

  p=7  conway: x3 = x1^-1  -> a fold, and the closure is ALL of PSL(2,7)
  p=7  kt    : x3, x4 commute -> a fold
  p=17 kt    : NO pair commutes -> a spread  (so "kt never leaves the fold" fails)

Run from the repo root: python3 verify_rung_fold.py
"""
from psl import PSL


def closure_size(G, gens):
    S, frontier = {G.id}, [G.id]
    while frontier:
        ng = []
        for f in frontier:
            for g in gens:
                h = G.m(f, g)
                if h not in S:
                    S.add(h)
                    ng.append(h)
        frontier = ng
    return len(S)


def commute_report(tag, p, X):
    G = PSL(p)
    print(f"{tag}: p={p} orders={[G.order(x) for x in X]} "
          f"onto={closure_size(G, X) == G.n} ({closure_size(G, X)}/{G.n})")
    found = False
    for i in range(4):
        for j in range(i + 1, 4):
            c = G.m(X[i], X[j]) == G.m(X[j], X[i])
            if c:
                found = True
                inv = "  (= inverse)" if G.m(X[i], X[j]) == G.id else ""
                print(f"    fold: x{i+1},x{j+1} commute{inv}")
    if not found:
        print("    spread: no pair commutes")


if __name__ == "__main__":
    # p=7 conway onto-hand (x3 = x1^-1)
    commute_report("conway", 7, [(0, 1, 6, 1), (1, 3, 6, 5), (1, 6, 1, 0), (2, 1, 0, 4)])
    # p=7 kt onto-hand (x3,x4 in one torus)
    commute_report("kt    ", 7, [(0, 1, 6, 1), (1, 2, 3, 0), (2, 3, 6, 6), (1, 3, 6, 5)])
    # p=17 kt onto-hand (four distinct axes -- a spread)
    commute_report("kt    ", 17, [(0, 1, 16, 5), (0, 5, 10, 5), (6, 16, 7, 16), (7, 0, 5, 5)])