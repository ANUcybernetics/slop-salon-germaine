#!/usr/bin/env python3
"""explore_beta.py — write β̂ as explicit free-group words.

The braid word β in B₄ induces an automorphism β̂ of F₄=⟨x₁,x₂,x₃,x₄⟩.
A hom π₁(K)→A₉ is a tuple T=(x₁,x₂,x₃,x₄) with β̂(T)=T.  To SOLVE for the
fixed tuple (not sweep it) we need β̂ written out: what does β̂ send each
generator to, as a reduced word?

Apply the moves left-to-right to the formal basis tuple (x₁,x₂,x₃,x₄).
For move (i,eps) on (u_i,u_{i+1}):
    eps>0: u_i -> u_i·u_{i+1}·u_i⁻¹,  u_{i+1} -> u_i
    eps<0: u_i -> u_{i+1},             u_{i+1} -> u_{i+1}⁻¹·u_i·u_{i+1}
"""
CONWAY = [-1, 2, -1, 2, -1, 3, -2, -2, -1, 3, 3]      # 11n34
KT = [-1, 2, 2, -3, -3, 2, 1, -2, -2, 3, -2, 3, -2]   # 11n42

# word = tuple of (gen_index0, exp).  Reduced means no adjacent (i,e),(i,-e).
def mul(a, b):
    out = list(a) + list(b)
    return tuple(reduce(out))

def reduce(w):
    stack = []
    for (i, e) in w:
        if stack and stack[-1] == (i, -e):
            stack.pop()
        else:
            stack.append((i, e))
    return stack

def inv(w):
    return tuple((i, -e) for (i, e) in reversed(w))

def gens_tuple():
    return tuple(((k, 1),) for k in range(4))

def apply_move(T, i, eps):
    u = list(T)
    a = u[i]; b = u[i + 1]
    if eps > 0:
        u[i] = mul(mul(a, b), inv(a))   # a·b·a⁻¹
        u[i + 1] = a
    else:
        u[i] = b
        u[i + 1] = mul(mul(inv(b), a), b)  # b⁻¹·a·b
    return tuple(u)

def beta_hat(word):
    T = gens_tuple()
    for g in word:
        i = abs(g) - 1
        eps = 1 if g > 0 else -1
        T = apply_move(T, i, eps)
    return T

def fmt(w):
    return "".join(("x%d" % (i + 1)) if e > 0 else ("x%d⁻¹" % (i + 1))
                   for (i, e) in w)

for name, word in (("Conway", CONWAY), ("KT", KT)):
    print(f"=== {name} ({len(word)} letters) ===")
    for j, wj in enumerate(beta_hat(word)):
        print(f"  β̂(x{j+1}) = {fmt(wj) or '∅'}")
    print()
