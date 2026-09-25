#!/usr/bin/env python3
"""make_a10_sum.py — does seam#seam span A_10?

rahel: "the door is six points wide... two staircases meeting in six points span
only ten — the sum opens A_9 and A_10."

The seam ALONE surjects A_8 (make_a8_search.py): generators x1..x4 in class
3^2 1^2, meridian mu = (0 1 2)(3 4 5) on 6 points, image A_8.

The connected sum pi_1(K#K) = pi_1(K) *_Z pi_1(K): a homomorphism is a pair
(phi1, phi2) agreeing on the meridian; image = <im phi1, im phi2>.  Embed the
A_8-surjection in A_10 fixing 8,9 (im phi1 = A_8 on {0..7}).  Take tau in
C_{A_10}(mu) that moves 6,7 to 8,9; phi2 = tau phi1 tau^-1 agrees on the
meridian, and im phi2 = tau A_8 tau^-1 is a different A_8 (on {0..5,8,9}).  If
<A_8, tau A_8 tau^-1> = A_10, the sum spans the tenth room.

Run: python3 make_a10_sum.py
"""
import itertools

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
def closure(gen):
    gen = list(set(gen)); n = len(gen[0])
    H = set(gen); H.add(tuple(range(n)))
    front = list(H)
    while front:
        a = front.pop()
        for b in gen:
            for c in (pmul(a, b), pmul(b, a), pinv(b)):
                if c not in H:
                    H.add(c); front.append(c)
    return H

# A_8-surjection (Conway), as perms of 8; embed in 10 fixing 8,9
x1 = (1, 2, 0, 4, 5, 3, 6, 7)
x2 = (0, 1, 3, 4, 2, 6, 7, 5)
x3 = (6, 3, 0, 7, 4, 5, 2, 1)
x4 = (0, 5, 4, 2, 3, 7, 6, 1)
emb = lambda p: tuple(list(p) + [8, 9])
X = [emb(p) for p in (x1, x2, x3, x4)]
mu = X[0]
print("A_8-surjection embedded in A_10 (fix 8,9):")
for i, p in enumerate(X):
    print(f"  x{i+1} = {cyc(p)}")
print(f"  meridian mu = {cyc(mu)}")
print(f"  <x1..x4> = |{len(closure(X))}|  (A_8 = 20160)")

# tau in C_{A_10}(mu): even permutations of the fixed points {6,7,8,9}
# that map {6,7} onto {8,9} so the second A_8 covers 8,9.
best = (0, None)
for perm in itertools.permutations([6, 7, 8, 9]):
    tau = tuple(range(10))
    tau = list(range(10))
    for src, dst in zip([6, 7, 8, 9], perm):
        tau[src] = dst
    tau = tuple(tau)
    if psign(tau) != 1:
        continue
    # centralizes mu (fixes 0..5, permutes fixed points)
    assert pmul(pmul(tau, mu), pinv(tau)) == mu
    conj = [pmul(pmul(tau, p), pinv(tau)) for p in X]
    J = closure(X + conj)
    support = sorted(set(itertools.chain.from_iterable(
        (j for j in range(10) if any(p[j] != j for p in conj)) for _ in [0])))
    # support of second A_8
    support2 = sorted({j for j in range(10) if any(p[j] != j for p in conj)})
    if len(J) > best[0]:
        best = (len(J), tau, support2)
    print(f"  tau = {cyc(tau)}  support2 = {support2}  <A_8, tau A_8 tau^-1> = |{len(J)}|"
          f"  {'*** A_10 ***' if len(J) == 1814400 else ''}")
    if len(J) == 1814400:
        break

print("\nRESULT:", f"seam#seam SURJECTS A_10" if best[0] == 1814400 else
      f"max <A_8, tau A_8 tau^-1> = |{best[0]}| (not A_10 = 1814400)")
