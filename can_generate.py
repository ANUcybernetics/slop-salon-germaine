#!/usr/bin/env python3
"""can_generate.py — can 4 conjugate elements of a class C generate A_8 at all?

This is a cheap NECESSARY test for whether C can be an exclusive A₈ door.  If
random 4-tuples from C (all in the same conjugacy class, as a braid closure
forces) never generate A₈, then no β̂-fixed tuple in C⁴ can either — the class is
"shut" for both mutants, not a door.  If they often DO generate A₈, the class is
capable, and the only question is whether a β̂-fixed such tuple exists.

Run: python3 can_generate.py
"""
import itertools, random
import numpy as np

N = 8; WANT = 20160
CLASSES = {
    "3^2 1^2": (1, 2, 0, 4, 5, 3, 6, 7),
    "3 2^2 1": (1, 2, 0, 4, 3, 6, 5, 7),
    "4 2 1^2": (1, 2, 3, 0, 5, 4, 6, 7),
    "4 4":     (1, 2, 3, 0, 5, 6, 7, 4),
    "5 1^3":   (1, 2, 3, 4, 0, 5, 6, 7),
    "5 3":     (1, 2, 3, 4, 0, 6, 7, 5),
    "6 2":     (1, 2, 3, 4, 5, 0, 7, 6),
    "7 1":     (1, 2, 3, 4, 5, 6, 0, 7),
}


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
def class_of(a, A8): return set(pmul(pmul(g, a), pinv(g)) for g in A8)
def closure_order(gen, cap=WANT):
    gen = list(set(gen)); n = len(gen[0]); H = set(gen); H.add(tuple(range(n)))
    front = list(H)
    while front:
        a = front.pop()
        for b in gen:
            for c in (pmul(a, b), pmul(b, a), pinv(b)):
                if c not in H:
                    H.add(c); front.append(c)
                    if len(H) > cap: return -1
    return len(H)


def main():
    random.seed(7)
    A8 = [p for p in itertools.permutations(range(N)) if psign(p) == 1]
    for name, a in CLASSES.items():
        cls = sorted(class_of(a, A8))
        m = len(cls)
        # sample 200 random 4-tuples from the class
        surj = 0; maxord = 0; trans = 0
        for _ in range(200):
            tup = [random.choice(cls) for _ in range(4)]
            # transitivity (Schreier)
            adj = [set() for _ in range(N)]
            for g in tup:
                for i in range(N):
                    adj[i].add(g[i]); adj[g[i]].add(i)
            seen = {0}; front = [0]
            while front:
                x = front.pop()
                for y in adj[x]:
                    if y not in seen: seen.add(y); front.append(y)
            if len(seen) != N: continue
            trans += 1
            o = closure_order(tup)
            if o > maxord: maxord = o
            if o == WANT: surj += 1
        print(f"{name:10s} |class|={m:5d}  random-4-tuples (200): "
              f"transitive={trans:3d}  surject A_8 = {surj:3d}  max|<x1..x4>|={maxord}")


if __name__ == "__main__":
    main()
