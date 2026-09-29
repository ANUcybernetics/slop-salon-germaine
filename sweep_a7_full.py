#!/usr/bin/env python3
"""sweep_a7_full.py — the COMPLETE A₇ door map, every meridian class.

a7_by_class.py only swept the two order-3 classes (3²·1, 3·1⁴). This sweeps all
eight A₇ conjugacy classes and reports, for Conway and KT, the β̂-fixed count,
the transitive count, the max image order, and whether it surjects A₇ (2520).

This closes the A₇ room: which classes are the shared doors, which is the
exclusive door, and whether any "mixed" class (3·2², 4·2·1) opens a door the
order-3 sweep missed.

Run: python3 sweep_a7_full.py
"""
import itertools, time
import numpy as np

CONWAY = [-1, 2, -1, 2, -1, 3, -2, -2, -1, 3, 3]      # 11n34
KT = [-1, 2, 2, -3, -3, 2, 1, -2, -2, 3, -2, 3, -2]   # 11n42
WANT = 2520


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
def porder(p):
    n = len(p); seen = [False]*n; o = 1
    for i in range(n):
        if not seen[i]:
            j = i; l = 0
            while not seen[j]:
                seen[j] = True; j = p[j]; l += 1
            o = o*l//__import__("math").gcd(o, l)
    return o
def cycle_type(p):
    n = len(p); seen = [False]*n; t = []
    for i in range(n):
        if not seen[i]:
            j = i; l = 0
            while not seen[j]:
                seen[j] = True; j = p[j]; l += 1
            t.append(l)
    return tuple(sorted(t, reverse=True))


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


def transitive(gen):
    n = len(gen[0])
    adj = [set() for _ in range(n)]
    for g in gen:
        for i in range(n):
            adj[i].add(g[i]); adj[g[i]].add(i)
    seen = {0}; front = [0]
    while front:
        a = front.pop()
        for b in adj[a]:
            if b not in seen:
                seen.add(b); front.append(b)
    return len(seen) == n


def closure_order(gen, cap=100000):
    gen = list(set(gen)); n = len(gen[0])
    H = set(gen); H.add(tuple(range(n)))
    front = list(H)
    while front:
        a = front.pop()
        for b in gen:
            for c in (pmul(a, b), pmul(b, a), pinv(b)):
                if c not in H:
                    H.add(c); front.append(c)
                    if len(H) > cap:
                        return -1
    return len(H)


def class_of(a, G): return set(pmul(pmul(g, a), pinv(g)) for g in G)
def centralizer(a, G): return set(g for g in G if pmul(pmul(g, a), pinv(g)) == a)
def orbit_reps(a, cls, G):
    C = centralizer(a, G); seen = set(); reps = []
    for x in sorted(cls):
        if x in seen: continue
        reps.append(x)
        seen |= set(pmul(pmul(h, x), pinv(h)) for h in C)
    return reps, len(C)


def scan_class(word, a, cls, G, label, n, want):
    moves = [(abs(g)-1, 1 if g > 0 else -1) for g in word]
    reps, csz = orbit_reps(a, cls, G)
    mem = sorted(cls); m = len(mem)
    mem_arr = np.array(mem, dtype=np.int64)
    g3 = np.repeat(np.arange(m, dtype=np.int64), m)
    g4 = np.tile(np.arange(m, dtype=np.int64), m)
    total_fixed = 0; trans = 0; maxord = 0; surj = False; surj_tup = None
    t0 = time.time()
    for x2 in reps:
        X0 = np.zeros((m*m, 4, n), dtype=np.int8)
        X0[:, 0] = np.array(a, dtype=np.int8)
        X0[:, 1] = np.array(x2, dtype=np.int8)
        X0[:, 2] = mem_arr[g3]
        X0[:, 3] = mem_arr[g4]
        X = X0.copy()
        apply_auto_vec(X, moves)
        mask = np.all(X == X0, axis=(1, 2))
        idxs = np.nonzero(mask)[0]
        total_fixed += len(idxs)
        for r in idxs:
            tup = (a, x2, mem[g3[r]], mem[g4[r]])
            if not transitive(tup):
                continue
            trans += 1
            o = closure_order(list(tup))
            if o > maxord:
                maxord = o
            if o == want:
                surj = True; surj_tup = tup
                break
        if surj:
            break
    return dict(cls=m, orbits=len(reps), fixed=total_fixed, trans=trans,
                maxord=maxord, surj=surj, tup=surj_tup, secs=time.time()-t0)


def main():
    t0 = time.time()
    A7 = [p for p in itertools.permutations(range(7)) if psign(p) == 1]
    # one representative per non-identity A₇ conjugacy class
    reps = {
        "2²·1³": (1, 0, 3, 2, 4, 5, 6),
        "3·1⁴":  (1, 2, 0, 3, 4, 5, 6),
        "3²·1":  (1, 2, 0, 4, 5, 3, 6),
        "3·2²":  (1, 2, 0, 4, 3, 6, 5),     # (0 1 2)(3 4)(5 6)
        "4·2·1": (1, 2, 3, 0, 5, 4, 6),     # (0 1 2 3)(4 5)
        "5·1²":  (1, 2, 3, 4, 0, 5, 6),
        "7":     (1, 2, 3, 4, 5, 6, 0),
    }
    print(f"|A₇| = {len(A7)}  ({time.time()-t0:.1f}s)\n")
    print(f"{'class':8s} {'|cls|':>6s} {'word':9s} {'β̂fix':>5s} {'trans':>5s} "
          f"{'maxord':>7s} {'surj':>5s}  time")
    for name in sorted(reps):
        a = reps[name]
        cls = class_of(a, A7)
        row = []
        for label, word in (("Conway", CONWAY), ("KT", KT)):
            r = scan_class(word, a, cls, A7, label, 7, WANT)
            row.append((label, r))
        for label, r in row:
            flag = "A₇!" if r['surj'] else ("—" if r['maxord'] < WANT else "?")
            print(f"{name:8s} {r['cls']:6d} {label:9s} {r['fixed']:5d} {r['trans']:5d} "
                  f"{r['maxord']:7d} {flag:>5s}  {r['secs']:5.1f}s")
        # witness
        for label, r in row:
            if r['surj'] and r['tup']:
                print(f"         {label} witness: x1={cyc(a)} x2={cyc(r['tup'][1])} "
                      f"x3={cyc(r['tup'][2])} x4={cyc(r['tup'][3])}")
        print()


if __name__ == "__main__":
    main()
