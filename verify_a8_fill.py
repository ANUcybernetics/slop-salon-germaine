#!/usr/bin/env python3
"""verify_a8_fill.py — standalone check of the A_8-surjection witness.

Does NOT reuse make_a8_search.py's machinery; recompute from scratch.

1. The seam is a 4-braid closure; the knot group is <x_i = β̂(x_i)> where β̂ is
   the Artin automorphism of the free group:  σ_i : x_i -> x_i x_{i+1} x_i^-1,
   x_{i+1} -> x_i, others fixed.  A hom to A_8 is a fixed point (x1..x4) in
   A_8^4 of β̂(word).

2. For the witness tuple, verify:
   - every generator is even (in A_8) and has cycle type 3^2 1^2 (two 3-cycles,
     no fixed point) — the "paired 3-cycle" meridian;
   - applying the braid word's β̂ returns the tuple unchanged (a genuine hom);
   - <x1..x4> has order exactly 20160 (a surjection onto A_8).

3. Then the A_10 sum: embed the witness in A_10 fixing 8,9; tau=(6 8)(7 9)
   centralizes the meridian; phi2 = tau phi1 tau^-1 agrees on the meridian and
   <A_8, tau A_8 tau^-1> should be A_10 (1814400).

Run: python3 verify_a8_fill.py
"""
import itertools
import math

N = 8


def pmul(p, q): return tuple(p[q[i]] for i in range(len(p)))


def pinv(p):
    r = [0] * len(p)
    for i in range(len(p)):
        r[p[i]] = i
    return tuple(r)


def psign(p):
    seen = [False] * len(p); s = 1
    for i in range(len(p)):
        if not seen[i]:
            j = i; l = 0
            while not seen[j]:
                seen[j] = True; j = p[j]; l += 1
            s *= (-1) ** (l - 1)
    return s


def cyc(p):
    seen = [False] * len(p); parts = []
    for i in range(len(p)):
        if not seen[i]:
            c = []; j = i
            while not seen[j]:
                seen[j] = True; c.append(j); j = p[j]
            if len(c) > 1:
                parts.append("(" + " ".join(str(x) for x in c) + ")")
    return "".join(parts) if parts else "()"


def cycle_type(p):
    seen = [False] * len(p); t = []
    for i in range(len(p)):
        if not seen[i]:
            j = i; l = 0
            while not seen[j]:
                seen[j] = True; j = p[j]; l += 1
            t.append(l)
    return tuple(sorted(t, reverse=True))


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


# ---- braid words (1-based generators, sign = direction) ---------------------
CONWAY = [-1, 2, -1, 2, -1, 3, -2, -2, -1, 3, 3]      # 11n34, 4-braid
KT = [-1, 2, 2, -3, -3, 2, 1, -2, -2, 3, -2, 3, -2]   # 11n42, 4-braid


def artin_apply(tup, word):
    """Apply the Artin automorphism β̂(word) to a tuple of permutations.
    Returns the transformed tuple."""
    X = list(tup)
    for g in word:
        i = abs(g) - 1            # 0-based generator index
        a = X[i]; b = X[i + 1]
        if g > 0:                 # σ_i : x_i -> x_i x_{i+1} x_i^-1, x_{i+1} -> x_i
            na = pmul(pmul(a, b), pinv(a))
            nb = a
        else:                     # σ_i^-1 : x_i -> x_{i+1}, x_{i+1} -> x_{i+1}^-1 x_i x_{i+1}
            na = b
            nb = pmul(pinv(b), pmul(a, b))
        X[i] = na; X[i + 1] = nb
    return tuple(X)


WITNESSES = {
    "Conway 11n34": (
        (0, 1, 2, 3, 4, 5, 6, 7),
        (0, 1, 2, 3, 4, 5, 6, 7),
        (0, 1, 2, 3, 4, 5, 6, 7),
        (0, 1, 2, 3, 4, 5, 6, 7),
    ),
}
# exact witness tuples from make_a8_search.py output (cycle -> tuple)
WITNESSES["Conway 11n34"] = (
    (1, 2, 0, 4, 5, 3, 6, 7),      # (0 1 2)(3 4 5)
    (0, 1, 3, 4, 2, 6, 7, 5),      # (2 3 4)(5 6 7)
    (6, 3, 0, 7, 4, 5, 2, 1),      # (0 6 2)(1 3 7)
    (0, 5, 4, 2, 3, 7, 6, 1),      # (1 5 7)(2 4 3)
)
WITNESSES["KT 11n42"] = (
    (1, 2, 0, 4, 5, 3, 6, 7),      # (0 1 2)(3 4 5)
    (0, 3, 1, 2, 5, 6, 4, 7),      # (1 3 2)(4 5 6)
    (1, 4, 3, 7, 0, 5, 6, 2),      # (0 1 4)(2 3 7)
    (4, 0, 7, 2, 1, 5, 6, 3),      # (0 4 1)(2 7 3)
)


def cyc_of(t):
    return [cyc(p) for p in t]


def check(name, tup, word):
    print(f"\n=== {name} ===")
    ok = True
    for k, p in enumerate(tup):
        even = psign(p) == 1
        ct = cycle_type(p)
        print(f"  x{k+1} = {cyc(p)}   even={even}  type={ct}")
        if not even:
            ok = False
        if ct != (3, 3, 1, 1):
            ok = False
    # Artin fixed point?
    out = artin_apply(tup, word)
    fixed = out == tup
    print(f"  β̂(word) fixed point? {fixed}")
    if not fixed:
        print("    transformed:", cyc_of(out))
    # subgroup order
    H = closure(list(tup))
    print(f"  <x1..x4> order = {len(H)}  ({'A_8 = 20160' if len(H) == 20160 else 'NOT A_8'})")
    ok = ok and fixed and (len(H) == 20160)
    return ok


def a10():
    print("\n=== seam#seam -> A_10 ===")
    tup = WITNESSES["Conway 11n34"]
    emb = lambda p: tuple(list(p) + [8, 9])
    X = [emb(p) for p in tup]
    mu = X[0]
    A8 = closure(X)
    print(f"  A_8 (embedded, fix 8,9) = |{len(A8)}|, meridian μ = {cyc(mu)}")
    # tau in C_{A_10}(mu) mapping {6,7} onto {8,9}: even perm of fixed pts
    best = (0, None, None)
    for perm in itertools.permutations([6, 7, 8, 9]):
        tau = list(range(10))
        for src, dst in zip([6, 7, 8, 9], perm):
            tau[src] = dst
        tau = tuple(tau)
        if psign(tau) != 1:
            continue
        assert pmul(pmul(tau, mu), pinv(tau)) == mu, "tau does not centralize mu"
        conj = [pmul(pmul(tau, p), pinv(tau)) for p in X]
        J = closure(X + conj)
        sup2 = sorted({j for j in range(10) if any(p[j] != j for p in conj)})
        if len(J) > best[0]:
            best = (len(J), tau, sup2)
        tag = " *** A_10 ***" if len(J) == 1814400 else ""
        print(f"  τ = {cyc(tau)}  im φ2 on {sup2}  <A_8, τA_8τ^-1> = |{len(J)}|{tag}")
        if len(J) == 1814400:
            break
    print(f"  RESULT: {'A_10 SURJECTED' if best[0] == 1814400 else 'not A_10'}")


if __name__ == "__main__":
    allok = True
    allok &= check("Conway 11n34", WITNESSES["Conway 11n34"], CONWAY)
    allok &= check("KT 11n42", WITNESSES["KT 11n42"], KT)
    print("\n=== SUMMARY ===")
    print("A_8-surjection witnesses all valid?" , allok)
    a10()
