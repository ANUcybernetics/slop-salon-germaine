#!/usr/bin/env python3
"""weave_profile.py — the conjugator's x-dependence (the weave, made legible).

beta_hat(x_j) = gamma_j x_{pi(j)} gamma_j^-1.  The conjugator gamma_j is built
from the crossings strand j participates in.  For each word, record, for each
target x_j, the MULTISET of original generators appearing in gamma_j and how
many times each appears (signed).  This is the weave fingerprint: both words
share perm and base flow, so the difference is entirely here.
"""
CONWAY = [-1, 2, -1, 2, -1, 3, -2, -2, -1, 3, 3]
KT = [-1, 2, 2, -3, -3, 2, 1, -2, -2, 3, -2, 3, -2]


def profile(name, word):
    # (conjugator list, base); value = c x_b c^-1
    pos = [([], 1), ([], 2), ([], 3), ([], 4)]
    for g in word:
        i = abs(g) - 1
        (c1, b1) = pos[i]; (c2, b2) = pos[i + 1]
        if g > 0:
            pos[i] = (list(c1) + [(b1, 1)] + [(x, -s) for (x, s) in reversed(c1)] + list(c2), b2)
            pos[i + 1] = (list(c1), b1)
        else:
            pos[i] = (list(c2), b2)
            pos[i + 1] = (list(c2) + [(b2, -1)] + [(x, -s) for (x, s) in reversed(c2)] + list(c1), b1)
    print(f"===== {name} (len {len(word)}) =====")
    for k in range(4):
        c, b = pos[k]
        # count signed occurrences of each generator in the conjugator c
        from collections import Counter
        cnt = Counter()
        for (x, s) in c:
            cnt[x] += s
        # generators whose NET count in the conjugator is nonzero
        nets = {x: v for x, v in cnt.items() if v != 0}
        total = len(c)
        print(f"  β̂(x{k+1}) = γ x{b} γ⁻¹, |γ|={total} atoms, "
              f"net per generator: {dict(sorted(nets.items()))}")


if __name__ == "__main__":
    profile("Conway 11n34", CONWAY)
    profile("KT 11n42", KT)
