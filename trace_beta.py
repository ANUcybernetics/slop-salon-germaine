#!/usr/bin/env python3
"""trace_beta.py — what does the β̂ fixed-point condition actually force?

A hom φ: π₁(K) → G is a β̂-fixed tuple.  β̂ is the Artin automorphism of the
free group F₄ that the braid word induces.  Applying β̂_w to the generator tuple
(x1,x2,x3,x4) and requiring the result to equal the tuple gives the knot-group
relations.  Here I trace the word symbolically (as reduced free-group words) so
I can SEE the conjugation pattern: which generator ends where, and conjugated by
what.  That is the thing that differs between the two mutants at the same braid
permutation (0 2 3 1).

Run: python3 trace_beta.py
"""
from functools import lru_cache

# each element is a tuple of (idx, sign); reduced: no x x^-1 adjacent.
# idx 1..4 = x1..x4


def reduce(w):
    out = []
    for (i, s) in w:
        if out and out[-1] == (i, -s):
            out.pop()
        else:
            out.append((i, s))
    return tuple(out)


def mul(a, b):
    return reduce(list(a) + list(b))


def inv(a):
    return tuple((i, -s) for (i, s) in reversed(a))


# beta_hat moves on a tuple of 4 words (positions 1..4).
# sigma_i^+ : (x_i, x_{i+1}) -> (x_i x_{i+1} x_i^-1, x_i)
# sigma_i^- : (x_i, x_{i+1}) -> (x_{i+1}, x_{i+1}^-1 x_i x_{i+1})
def apply_move(tup, i, eps):
    t = list(tup)
    a, b = t[i - 1], t[i]
    if eps > 0:
        t[i - 1] = mul(mul(a, b), inv(a))
        t[i] = a
    else:
        t[i - 1] = b
        t[i] = mul(mul(inv(b), a), b)
    return tuple(t)


def word_to_moves(word):
    return [(abs(g), 1 if g > 0 else -1) for g in word]


CONWAY = [-1, 2, -1, 2, -1, 3, -2, -2, -1, 3, 3]
KT = [-1, 2, 2, -3, -3, 2, 1, -2, -2, 3, -2, 3, -2]


def show(w):
    # prettify reduced word
    if not w:
        return "1"
    s = ""
    for (i, sg) in w:
        s += f"x{i}" if sg > 0 else f"x{i}^-1"
    return s


def braid_perm(word):
    # braid perm: product of transpositions (i,i+1) for each sigma_i (sign-free)
    n = 4
    p = list(range(n))
    for g in word:
        i = abs(g) - 1  # 0-indexed
        p[i], p[i + 1] = p[i + 1], p[i]
    return tuple(p)


def trace(name, word):
    print(f"\n===== {name}  word={word} =====")
    print("  braid perm:", braid_perm(word))
    tup = tuple((((i, 1),) for i in range(1, 5)))
    start = tup
    for step, (i, eps) in enumerate(word_to_moves(word)):
        tup = apply_move(tup, i, eps)
        print(f"  after σ{i}{'+' if eps>0 else '-'}: "
              + "  ".join(f"[{k}]={show(tup[k-1])}" for k in range(1, 5)))
    # fixed point equations: position k must equal x_k
    print("  FIXED-POINT EQUATIONS (β̂(x) = x):")
    for k in range(1, 5):
        eq = tup[k - 1]
        print(f"    x{k} = {show(eq)}")
    return tup


if __name__ == "__main__":
    trace("Conway 11n34", CONWAY)
    trace("KT 11n42", KT)
