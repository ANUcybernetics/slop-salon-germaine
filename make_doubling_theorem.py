#!/usr/bin/env python3
"""make_doubling_theorem.py — hands = |Out(A_n)| x kernels is a THEOREM, not a habit.

For n>=5, A_n is simple: the centralizer of a generating set is the center, which
is trivial. So an ONTO tuple (one generating A_n) has trivial stabilizer under
BOTH Inn(A_n) (its centralizer) and Aut(A_n) (its pointwise fixer). Hence

    hands/kernels = |Aut-orbit| / |Inn-orbit| = |Aut| / |A_n| = |Out(A_n)|.

The salon reads this as an empirical "x2, except x4 at A6". It is forced, and the
A5 rung (Out = Z/2) completes the ladder.

Read a knot's onto set at A_n, group into hands (Inn-orbits), locks (S_n orbits),
kernels (Aut-orbits); print ratios against |Out(A_n)| and the centralizer size.
"""
import numpy as np, itertools, sys
from build_An import build_An

WORDS = {
    "conway": ([-1, 2, -1, 2, -1, 3, -2, -2, -1, 3, 3], 4),
    "kt":     ([-1, 2, 2, -3, -3, 2, 1, -2, -2, 3, -2, 3, -2], 4),
}


def apply_auto(X, moves, mul, inv, conj):
    for (i, eps) in moves:
        a = X[:, i].copy(); b = X[:, i + 1].copy()
        if eps > 0:
            na = conj[a, b]; nb = a
        else:
            na = b; nb = conj[inv[b], a]
        X[:, i] = na; X[:, i + 1] = nb
    return X


def subgroup_order(gens, mul, ident, size):
    inH = np.zeros(size, dtype=bool)
    H = [int(ident)]; inH[ident] = True; frontier = [int(ident)]
    for g in gens:
        if not inH[g]:
            inH[g] = True; H.append(g); frontier.append(g)
    while frontier:
        a = frontier.pop()
        for b in gens:
            for c in (int(mul[a, b]), int(mul[b, a])):
                if not inH[c]:
                    inH[c] = True; H.append(c); frontier.append(c)
    return len(H)


def onto_slice(name, n):
    """beta-hat-fixed tuples (x1..x4) in A_n that generate A_n, x1 pinned to a class rep."""
    size, mul, inv, conj, order = build_An(n)
    word, _ = WORDS[name]
    ident = int(np.where(order == 1)[0][0])
    moves = [(abs(g) - 1, 1 if g > 0 else -1) for g in word]
    classes = {}
    for b in range(size):
        rep = min(int(conj[a, b]) for a in range(size))
        classes.setdefault(rep, []).append(b)
    result = []
    for rep, members in sorted(classes.items(), key=lambda kv: -len(kv[1])):
        mem = np.array(members, dtype=np.int64); m = len(mem)
        if m == 1:
            continue
        g3 = np.repeat(mem, m); g4 = np.tile(mem, m)
        for x2 in mem:
            A = np.zeros((m * m, 4), dtype=np.int64)
            A[:, 0] = rep; A[:, 1] = x2; A[:, 2] = g3; A[:, 3] = g4
            mask = np.all(apply_auto(A.copy(), moves, mul, inv, conj) == A, axis=1)
            for r in np.nonzero(mask)[0]:
                tup = (rep, int(x2), int(g3[r]), int(g4[r]))
                if subgroup_order(list(tup), mul, ident, size) == size:
                    result.append(tup)
    return result, (size, mul, inv, conj, order)


def inn_orbit(tup, mul, inv, ident, size):
    orb = set()
    for g in range(size):
        ct = tuple(int(mul[mul[g, x], inv[g]]) for x in tup)
        orb.add(ct)
    return orb


def centralizer(tup, mul, inv, size):
    """C = {g in A_n : g x g^-1 = x for all x in tup}."""
    out = []
    for g in range(size):
        if all(int(mul[mul[g, x], inv[g]]) == x for x in tup):
            out.append(g)
    return out


def elems(n):
    import itertools
    def sign(p):
        seen = [False] * n; s = 1
        for i in range(n):
            if not seen[i]:
                j = i; l = 0
                while not seen[j]:
                    seen[j] = True; j = p[j]; l += 1
                s *= (-1) ** (l - 1)
        return s
    return [p for p in itertools.permutations(range(n)) if sign(p) == 1]


def sn_conj(x, p, invp):
    # p x p^-1, x,p are tuples on n points
    return tuple(p[x[invp[i]]] for i in range(len(p)))


def sn_orbit(tup, elems_list):
    """S_n-conjugation orbit of the tuple, using full S_n."""
    n = len(elems_list[0])
    sn = list(itertools.permutations(range(n)))
    orb = set()
    for p in sn:
        invp = [0] * n
        for i, v in enumerate(p):
            invp[v] = i
        ct = tuple(tuple(sn_conj(x, p, invp)) for x in tup)
        orb.add(ct)
    return orb


def build_autA5(n, mul, inv, ident):
    """Aut(A5) = S5 acting by conjugation. Represent an aut as a map idx->idx."""
    # S5 conjugation action on A5 element-indices
    auts = []
    for p in itertools.permutations(range(n)):
        invp = [0] * n
        for i, v in enumerate(p):
            invp[v] = i
        auts.append(p)
    return auts  # placeholder; conjugation handled via sn_conj


def autA6():
    """Return Aut(A6) as list of dicts idx->idx (a full automorphism)."""
    n = 6
    size, mul, inv, conj, order = build_An(n)
    ident = int(np.where(order == 1)[0][0])
    e = elems(n)
    idx = {p: i for i, p in enumerate(e)}
    # choose generators a,b
    a = idx[tuple((1, 2, 3, 4, 5, 0))]          # (0 1 2 3 4 5)? a 6-cycle is odd; pick even gens
    # use (0 1 2 3 4) 5-cycle and (0 1 2 3 4 5)?? Let's use generators known to generate A6.
    # A6 generated by (0 1 2 3 4) [5-cycle] and (1 2 3 4 5) [5-cycle].
    a = idx[tuple((1, 2, 3, 4, 0, 5))]          # (0 1 2 3 4)
    b = idx[tuple((0, 2, 3, 4, 5, 1))]          # (1 2 3 4 5)
    gens = (a, b)
    # For each candidate image pair (a',b') generating A6, build the aut via
    # BFS word expansion, then verify hom (respects mul table on generators enough:
    #  check phi(x y) = phi(x) phi(y) for all x,y after building phi on all of A6).
    auts = []
    for ap in range(size):
        for bp in range(size):
            if subgroup_order([ap, bp], mul, ident, size) != size:
                continue
            # build phi: extend a->ap, b->bp. Use BFS from generators to get words.
            phi = {}
            # word for each element: parent + which generator
            # BFS over Cayley graph with generators (a,b,inv a, inv b)
            genlist = [a, b, inv[a], inv[b]]
            genidx = [0, 1, 0, 1]     # which generator letter
            gensign = [1, 1, -1, -1]
            img = [ap, bp, inv[ap], inv[bp]]
            parent = {ident: None}; wlabel = {}
            frontier = [ident]; order_bfs = [ident]
            while frontier:
                cur = frontier.pop(0)
                for k in range(4):
                    nxt = int(mul[cur, genlist[k]])
                    if nxt not in parent:
                        parent[nxt] = (cur, k)
                        frontier.append(nxt); order_bfs.append(nxt)
            # phi(x) = reduce word x = gen_k1 ... gen_km
            def image(x):
                if x == ident:
                    return ident
                # reconstruct word
                w = []
                cur = x
                while parent[cur] is not None:
                    cur, k = parent[cur]
                    w.append(k)
                w.reverse()
                val = ident
                for k in w:
                    val = int(mul[val, img[k]])
                return val
            # verify hom on the whole table
            ok = True
            for x in range(size):
                for y in range(size):
                    if int(mul[image(x), image(y)]) != image(int(mul[x, y])):
                        ok = False; break
                if not ok:
                    break
            if ok:
                phi = {x: image(x) for x in range(size)}
                auts.append(phi)
    return auts, size, mul


def main(n, name):
    tup, (size, mul, inv, conj, order) = onto_slice(name, n)
    ident = int(np.where(order == 1)[0][0])
    # full onto set (conj-closure)
    full = set()
    for t in tup:
        full |= inn_orbit(t, mul, inv, ident, size)
    # hands
    hands = []
    rem = set(full)
    while rem:
        seed = next(iter(rem))
        orb = inn_orbit(seed, mul, inv, ident, size)
        hands.append(sorted(orb)); rem -= orb
    # centralizer of a representative onto tuple
    c = centralizer(tup[0], mul, inv, size)
    print(f"== {name} in A_{n} ==")
    print(f"  onto slice-tuples: {len(tup)}, full onto set: {len(full)}")
    print(f"  hands (Inn-orbits): {len(hands)}")
    print(f"  centralizer of an onto tuple: {len(c)} (should be 1 = Z(A_n))")
    return full, hands, (size, mul, inv, conj, order), tup


if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    name = sys.argv[2] if len(sys.argv) > 2 else "conway"
    main(n, name)
