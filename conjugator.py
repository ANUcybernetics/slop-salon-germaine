#!/usr/bin/env python3
"""conjugator.py — track beta_hat(x_j) as (conjugator c, base b): value = c x_b c^-1.

Each position's value is ALWAYS a single conjugate of one original generator,
because the signed Artin moves keep the form c x_b c^-1:

  sigma_i^+ on (a,b)=(c_i x_{b_i} c_i^-1, c_{i+1} x_{b_{i+1}} c_{i+1}^-1):
     new pos i   = a b a^-1 = (c_i x_{b_i} c_i^-1 c_{i+1}) x_{b_{i+1}} (..)^-1
     new pos i+1 = a = (c_i, b_i)
  sigma_i^- on (a,b):
     new pos i   = b = (c_{i+1}, b_{i+1})
     new pos i+1 = b^-1 a b = (c_{i+1} x_{b_{i+1}}^-1 c_{i+1}^-1 c_i) x_{b_i} (..)^-1

The conjugator c is a free word (list of (base,sign) atoms) but stays bounded by
word length — it does NOT explode like the full reduced words did.
"""
CONWAY = [-1, 2, -1, 2, -1, 3, -2, -2, -1, 3, 3]
KT = [-1, 2, 2, -3, -3, 2, 1, -2, -2, 3, -2, 3, -2]


def atoms_to_str(a):
    return "".join(("x%d" % x if s > 0 else "x%d^-1" % x) for (x, s) in a)


def show(c, b):
    cs = atoms_to_str(c)
    return f"({cs})x{b}({cs})^-1"


def track(name, word):
    # (conjugator list, base); value = c x_b c^-1.  Start: x_j at pos j.
    pos = [([], 1), ([], 2), ([], 3), ([], 4)]
    print(f"===== {name}  (word={word}) =====")
    print("  start:", [show(*pos[k]) for k in range(4)])
    for step, g in enumerate(word, 1):
        i = abs(g) - 1
        (c1, b1) = pos[i]; (c2, b2) = pos[i + 1]
        if g > 0:
            # new pos i = (c1 x_b1 c1^-1 c2) x_b2 (..)^-1
            newc = list(c1) + [(b1, 1)] + [(x, -s) for (x, s) in reversed(c1)] + list(c2)
            pos[i] = (newc, b2)
            pos[i + 1] = (list(c1), b1)
        else:
            # new pos i = b = (c2, b2)
            pos[i] = (list(c2), b2)
            # new pos i+1 = (c2 x_b2^-1 c2^-1 c1) x_b1 (..)^-1
            newc = list(c2) + [(b2, -1)] + [(x, -s) for (x, s) in reversed(c2)] + list(c1)
            pos[i + 1] = (newc, b1)
        # compact print
        print(f"  {step:2d} σ{abs(g)}{'+' if g>0 else '-'}: "
              + "  ".join(show(*pos[k]) for k in range(4)))
    print("\n  FIXED-POINT equations beta_hat(x_j) = x_j:")
    for k in range(4):
        c, b = pos[k]
        cs = atoms_to_str(c)
        print(f"    x{k+1} = ({cs}) x{b} ({cs})^-1")
    print("    bases:", [pos[k][1] for k in range(4)])
    return pos


if __name__ == "__main__":
    track("KT 11n42", KT)
    print()
    track("Conway 11n34", CONWAY)
