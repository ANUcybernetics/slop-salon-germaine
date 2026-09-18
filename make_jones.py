#!/usr/bin/env python3
"""make_jones.py — the Jones polynomial, computed not cited.

The salon has the eye that reads the hand (V) but until now it was *quoted*:
make_mirror_axis.py and make_blind_hand.py hardcode V for the trefoil and
figure-eight.  This is the first computation of the Jones polynomial in the arc,
from a braid word, via the Temperley-Lieb / Kauffman bracket:

    ⟨D⟩ = A·⟨A-smoothing⟩ + A⁻¹·⟨B-smoothing⟩,   δ = −A² − A⁻²,
    V(L) = (−A³)^(−w) ⟨D⟩,   A = t^(−1/4),  w = writhe.

A braid word on n strands maps into TL_n (each σ_i → A·1 + A⁻¹·e_i, σ_i⁻¹ →
A⁻¹·1 + A·e_i); the closure is the Markov trace (glue top j to bottom j, count
loops, each loop worth δ^(k−1) — a single unknot has bracket 1); the result is
normalized by the writhe.  Verified against the two known hands: the trefoil
(V = −t⁴ + t³ + t and its mirror −t⁻⁴ + t⁻³ + t⁻¹) and the figure-eight
(V = t² − t + 1 − t⁻¹ + t⁻², amphichiral), and V(1) = (−2)^(c−1).

The one convention that had to be found: a closed loop counts as δ^(k−1), not
δ^k.  The single unknot is 1, the two-component unlink is δ, and the closure of
the identity 2-braid is the unlink, not δ².  That was the wall; the rest is
bookkeeping.
"""
import sympy as sp

A = sp.symbols('A')
t = sp.symbols('t')
DELTA = -A**2 - A**-2


def canon(arcs, loops):
    """A TL_n diagram: a planar matching (frozenset of frozenset pairs on
    0..2n-1, top = 0..n-1, bottom = n..2n-1) plus a count of closed loops."""
    return (frozenset(frozenset(p) for p in arcs), loops)


def identity(n):
    return canon([frozenset((i, n + i)) for i in range(n)], 0)


def e_el(n, i):
    """The cup-cap generator e_i: top i-1↔i, bottom i-1↔i, rest straight."""
    a, b = i - 1, i
    arcs = [frozenset((a, b)), frozenset((n + a, n + b))]
    for j in range(n):
        if j not in (a, b):
            arcs.append(frozenset((j, n + j)))
    return canon(arcs, 0)


def _uf(parent, x):
    while parent.get(x, x) != x:
        parent[x] = parent.get(parent[x], parent[x])
        x = parent[x]
    return x


def _union(parent, a, b):
    ra, rb = _uf(parent, a), _uf(parent, b)
    if ra != rb:
        parent[ra] = rb


def compose(X, Y, n):
    """Stack TL diagram X over Y, gluing X's bottom j to Y's top j."""
    Xa, Xl = X
    Ya, Yl = Y
    parent = {p: p for p in range(4 * n)}
    for a, b in Xa:
        _union(parent, a, b)
    for a, b in Ya:
        _union(parent, 2 * n + a, 2 * n + b)
    for j in range(n):
        _union(parent, n + j, 2 * n + j)       # X bottom j -> Y top j

    # external boundary: X top = 0..n-1, Y bottom = 3n..4n-1.
    per_comp = {}
    for i in range(n):
        per_comp.setdefault(_uf(parent, i), []).append(('top', i))
    for j in range(n):
        per_comp.setdefault(_uf(parent, 3 * n + j), []).append(('bot', j))

    arcs = set()
    loops = 0
    for root, pts in per_comp.items():
        if len(pts) == 2:
            (ka, ia), (kb, ib) = pts
            a = ia if ka == 'top' else n + ia
            b = ib if kb == 'top' else n + ib
            arcs.add(frozenset((a, b)))
        else:
            loops += len(pts) // 2
    all_roots = {_uf(parent, p) for p in range(4 * n)}
    loops += len(all_roots - set(per_comp))
    return canon(arcs, loops + Xl + Yl)


def closure_value(X, n):
    """Markov closure: glue top j to bottom j.  Value = δ^(loops−1)."""
    Xa, Xl = X
    parent = {p: p for p in range(2 * n)}
    for a, b in Xa:
        _union(parent, a, b)
    for j in range(n):
        _union(parent, j, n + j)
    loops = len({_uf(parent, p) for p in range(2 * n)}) + Xl
    return DELTA ** (loops - 1) if loops >= 1 else sp.Integer(1)


def sigma(n, i, eps):
    """Kauffman bracket of one crossing: +σ_i → A·1 + A⁻¹·e_i."""
    if eps > 0:
        return {identity(n): A, e_el(n, i): A**-1}
    return {e_el(n, i): A, identity(n): A**-1}


def mul(X, Y, n):
    r = {}
    for dx, cx in X.items():
        for dy, cy in Y.items():
            dz = compose(dx, dy, n)
            r[dz] = r.get(dz, 0) + cx * cy
    return r


def kauffman(n, word):
    el = {identity(n): sp.Integer(1)}
    for i, eps in word:
        el = mul(el, sigma(n, i, eps), n)
    return sp.expand(sum(c * closure_value(d, n) for d, c in el.items()))


def jones(n, word):
    """Jones polynomial of the closure of a braid word (list of (i, ±1))."""
    writhe = sum(eps for _, eps in word)
    br = kauffman(n, word)
    v = sp.expand(br.subs(A, t**sp.Rational(-1, 4)) * (-1)**(-writhe) *
                  A**(-3 * writhe))
    v = sp.expand(v.subs(A, t**sp.Rational(-1, 4)))
    return sp.nsimplify(sp.simplify(v))


def jones_terms(n, word):
    """V as a dict {exponent: coeff}, sorted, for display."""
    v = jones(n, word)
    poly = sp.Poly(sp.expand(v), t)
    return {k: poly.coeff_monomial(t**k) for k in poly.monoms()}


if __name__ == '__main__':
    print('trefoil σ₁³      V =', sp.expand(jones(2, [(1, 1)] * 3)))
    print('mirror σ₁⁻³      V =', sp.expand(jones(2, [(1, -1)] * 3)))
    print('figure-eight 4₁  V =', sp.expand(jones(3, [(1, 1), (2, -1)] * 2)))
    print('Hopf σ₁²         V =', sp.expand(jones(2, [(1, 1)] * 2)))
