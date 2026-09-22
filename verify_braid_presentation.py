#!/usr/bin/env python3
"""verify_braid_presentation.py — is <x_i = β̂(x_i)> the knot group or the
solid-torus complement?

rahel's correction: "xᵢ=β(xᵢ) is the solid-torus complement, not the knot group
(fig-8's A₄ reads 12, true 36). correct Wirtinger puts the seam ON THE FLOOR."

Test it. For the trefoil I know the knot group is B₃ = <a,b | aba=bab> and that
|Hom(B₃, A₅)| = 120.  Compute the count from that explicit presentation and from
the braid-closure model <x_i = β̂(x_i)> for the same knot, then compare.  If they
agree, the braid-closure model IS the knot group and rahel's fig-8 claim needs a
different check.  If they differ, the model is wrong.

Also do the fig-8 into A₄: rahel says true is 36, braid-closure model gives 12.

Run:  python3 verify_braid_presentation.py
"""
import itertools
from collections import Counter

import numpy as np

from make_A5 import build_A5
from make_seam_s5 import build_S5
from make_gl32_counts import build_GL32
from make_seam_profile import fixed_points


# ---- generic word evaluation ------------------------------------------------
# a word is a tuple of (gen_idx, exponent).  gen_idx 0-based.
def eval_word(word, gens, mul, inv):
    """Evaluate a word (list of (gen, exp)) in the group using gens = tuple of
    group element indices assigned to the generators."""
    cur = None
    for (g, e) in word:
        el = gens[g]
        if e < 0:
            el = inv[el]
            e = -e
        for _ in range(e):
            cur = el if cur is None else mul[cur, el]
    return cur if cur is not None else None  # None = identity


def count_homs_pres(pres, size, mul, inv, conj, order):
    """Count homs from a presentation.  pres = (num_gens, relations) where each
    relation is a pair (word_lhs, word_rhs) meaning lhs == rhs."""
    ngens, rels = pres
    count = 0
    for assign in itertools.product(range(size), repeat=ngens):
        ok = True
        for (lhs, rhs) in rels:
            if eval_word(lhs, assign, mul, inv) != eval_word(rhs, assign, mul, inv):
                ok = False
                break
        if ok:
            count += 1
    return count


# ---- group name helpers ------------------------------------------------------
def label_group(size, mul, inv, order):
    """Return a dict from element index -> a readable label (cycle type / order)."""
    return {a: f"o{order[a]}" for a in range(size)}


# ---- the presentations -------------------------------------------------------
# B3 = <a,b | a b a = b a b>
B3 = (2, [(((0, 1), (1, 1), (0, 1)), ((1, 1), (0, 1), (1, 1)))])

# fig-8 knot group, rahel's form: <a,b | a b a⁻¹ b a = b a b⁻¹ a b>
#   lhs = a b a⁻¹ b a , rhs = b a b⁻¹ a b
FIG8_RAHEL = (2, [(((0, 1), (1, 1), (0, -1), (1, 1), (0, 1)),
                  ((1, 1), (0, 1), (1, -1), (0, 1), (1, 1)))])


# ---- knot braid words (the braid-closure model) ------------------------------
KNOTS = {
    "trefoil 3_1": ([1, 1, 1], 2),
    "fig-8 4_1": ([1, -2, 1, -2], 3),
}


def braid_closure_count(word, n, size, mul, inv, conj, order):
    """|Hom( braid-closure group , H )| via fixed points of the Artin action."""
    fps = fixed_points(word, n, size, mul, inv, conj)
    return len(fps)


def image_classify(fps, size, mul, inv, ident, order, classify=None):
    """For the braid-closure homs, classify the image subgroup of each fixed point."""
    if classify is None:
        return {}
    by = Counter()
    for X in fps:
        so = classify(list(X), size, mul, inv, ident, order)
        by[so] = by.get(so, 0) + 1
    return by


def run_group(label, size, mul, inv, conj, order):
    ident = int(np.where(order == 1)[0][0])
    print(f"\n=== {label}  |G|={size} ===")
    # explicit presentation counts
    for name, pres in [("B3 (trefoil knot group)", B3),
                       ("fig-8 <ab a⁻¹b a = ba b⁻¹a b>", FIG8_RAHEL)]:
        t0 = 0
        c = count_homs_pres(pres, size, mul, inv, conj, order)
        print(f"  explicit  {name:<36} : {c}")
    # braid-closure model
    for name, (word, n) in KNOTS.items():
        c = braid_closure_count(word, n, size, mul, inv, conj, order)
        print(f"  braid-closure {name:<28} : {c}")


def main():
    # A4 is not built by any existing builder; build it inline from even perms of 4.
    from make_seam_s5 import perm_mul, perm_inv, perm_order
    import math

    def build_A4():
        elems = [p for p in itertools.permutations(range(4))
                 if perm_sign(p) == 1]
        idx = {e: i for i, e in enumerate(elems)}
        size = len(elems)
        ident = idx[tuple(range(4))]
        mul = np.zeros((size, size), dtype=np.int64)
        for a in range(size):
            for b in range(size):
                mul[a, b] = idx[perm_mul(elems[a], elems[b])]
        inv = np.zeros(size, dtype=np.int64)
        for a in range(size):
            for b in range(size):
                if mul[a, b] == ident:
                    inv[a] = b
        conj = np.zeros((size, size), dtype=np.int64)
        for a in range(size):
            for b in range(size):
                conj[a, b] = mul[mul[a, b], inv[a]]
        order = np.zeros(size, dtype=np.int64)
        for a in range(size):
            order[a] = perm_order(elems[a])
        return size, mul, inv, conj, order

    def perm_sign(p):
        seen = [False] * len(p)
        s = 1
        for i in range(len(p)):
            if not seen[i]:
                j = i
                l = 0
                while not seen[j]:
                    seen[j] = True
                    j = p[j]
                    l += 1
                s *= (-1) ** (l - 1)
        return s

    for label, builder in [("A4", build_A4),
                           ("A5", build_A5),
                           ("S5", build_S5),
                           ("GL(3,2)=PSL(2,7)", build_GL32)]:
        size, mul, inv, conj, order = builder()
        run_group(label, size, mul, inv, conj, order)


if __name__ == "__main__":
    main()
