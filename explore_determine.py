#!/usr/bin/env python3
"""explore_determine.py — is x4 determined by (x1,x2,x3)?

For a fixed (x1,x2,x3) in the class, sweep x4 over the WHOLE class (m options,
not m^2) and count beta_hat-fixed tuples.  Confirms the "exactly one" claim and
shows whether x4 is pinned by x1,x2,x3.
"""
import itertools, time
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
            while not seen[j]:
                seen[j] = True; j = p[j]; l += 1
            s *= (-1)**(l-1)
    return s
def cyc(p):
    n = len(p); seen = [False]*n; parts = []
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
            p[c[k]] = c[(k+1) % len(c)]
    return tuple(p)


def apply_auto(tup, word):
    X = list(tup)
    for g in word:
        i = abs(g)-1
        a, b = X[i], X[i+1]
        if g > 0:
            X[i] = pmul(pmul(a, b), pinv(a)); X[i+1] = a
        else:
            X[i] = b; X[i+1] = pmul(pinv(b), pmul(a, b))
    return tuple(X)


def class_of(a, A9):
    return set(pmul(pmul(g, a), pinv(g)) for g in A9)


def main():
    A9 = [p for p in itertools.permutations(range(9)) if psign(p) == 1]
    print(f"|A9|={len(A9)}")
    rep = (1,2,0,4,5,3,7,8,6)            # 3^3
    cls = sorted(class_of(rep, A9))
    m = len(cls)
    print(f"3^3 class: |class|={m}")
    cls_arr = np.array(cls, dtype=np.int8)
    # witness from make_a9_door (KT 3^3)
    w = (from_cycles([(0,1,2),(3,4,5),(6,7,8)]),
         from_cycles([(0,1,3),(2,6,5),(4,8,7)]),
         from_cycles([(0,4,1),(2,5,6),(3,8,7)]),
         from_cycles([(0,2,6),(1,7,8),(3,4,5)]))
    print("KT witness:", [cyc(p) for p in w])
    print("  fixed?", apply_auto(w, KT) == w)
    print("  CONWAY fixed?", apply_auto(w, CONWAY) == w)
    # fix (x1,x2,x3)=witness, sweep x4 over whole class
    for wordname, word in [("KT", KT), ("CONWAY", CONWAY)]:
        x1, x2, x3 = w[0], w[1], w[2]
        X0 = np.zeros((m, 4, 9), dtype=np.int8)
        X0[:, 0] = np.array(x1, dtype=np.int8)
        X0[:, 1] = np.array(x2, dtype=np.int8)
        X0[:, 2] = np.array(x3, dtype=np.int8)
        X0[:, 3] = cls_arr
        X = X0.copy()
        for g in word:
            i = abs(g)-1
            a = X[:, i].copy(); b = X[:, i+1].copy()
            if g > 0:
                na = np.take_along_axis(np.take_along_axis(a, b, axis=1), np.argsort(a, axis=1), axis=1)
                nb = a
            else:
                na = b
                nb = np.take_along_axis(np.argsort(b, axis=1), np.take_along_axis(a, b, axis=1), axis=1)
            X[:, i] = na; X[:, i+1] = nb
        mask = np.all(X == X0, axis=(1,2))
        idxs = np.nonzero(mask)[0]
        print(f"  {wordname}: fixing (x1,x2,x3)=witness, x4 in class -> {len(idxs)} fixed x4")
        for r in idxs:
            print(f"       x4 = {cyc(cls[r])}")
        # also fix (x1,x2) and sweep (x3,x4) full — too big for 3^3 (m^2=5M), do via x3 outer
        print(f"  {wordname}: fix (x1,x2)=witness, iterate x3 over class, sweep x4 (full)")
        t0 = time.time()
        total = 0
        sols = []
        for x3i, x3 in enumerate(cls):
            X0 = np.zeros((m, 4, 9), dtype=np.int8)
            X0[:, 0] = np.array(x1, dtype=np.int8)
            X0[:, 1] = np.array(x2, dtype=np.int8)
            X0[:, 2] = np.array(x3, dtype=np.int8)
            X0[:, 3] = cls_arr
            X = X0.copy()
            for g in word:
                i = abs(g)-1
                a = X[:, i].copy(); b = X[:, i+1].copy()
                if g > 0:
                    na = np.take_along_axis(np.take_along_axis(a, b, axis=1), np.argsort(a, axis=1), axis=1)
                    nb = a
                else:
                    na = b
                    nb = np.take_along_axis(np.argsort(b, axis=1), np.take_along_axis(a, b, axis=1), axis=1)
                X[:, i] = na; X[:, i+1] = nb
            mask = np.all(X == X0, axis=(1,2))
            for r in np.nonzero(mask)[0]:
                total += 1
                sols.append((x3, cls[r]))
        print(f"       -> {total} fixed tuples (x1,x2 fixed); each x3 gives {total/m if m else 0:.3f} avg")
        for (s3, s4) in sols[:8]:
            print(f"       x3={cyc(s3)} x4={cyc(s4)}")
        print(f"       ({time.time()-t0:.1f}s)")


if __name__ == "__main__":
    main()
