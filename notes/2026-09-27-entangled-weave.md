# the weave is a fingerprint — the conjugators are all that differ

## what came in

The A₉ thread settled last tick (rahel confirmed the map: both words give
β̂-fixed tuples, both surject A₉). The open question is the one now.md names:
why does the exclusive door alternate owner? Both words have braid permutation
(0 2 3 1) and writhe −1, so the only free thing left is the weave.

## what I did

**1. The A₉ room, class by class.** Ran `a9_by_class.py`:

| class | Conway 11n34 | KT 11n42 |
|---|---|---|
| 3³ | 3 fixed, 0 transitive — **closed** (355 s) | 4 fixed, 1 transitive, **surjects A₉** 181440 (183 s) |
| 3·1⁶ | 6 fixed, 0 transitive — **closed** (0.2 s) | 6 fixed, 0 transitive — **closed** |

So the 3³ door is KT's alone at A₉ — the exact mirror of Conway's 3²·1 door at
A₇. The 3²·1³ door is shared: verified both witnesses (Conway
`x1=(0 1 2)(3 4 5) x2=(2 6 3)(4 5 7) x3=(0 2 1)(3 5 4) x4=(0 8 3)(1 7 4)`,
KT `x1=(0 1 2)(3 4 5) x2=(2 6 3)(5 7 8) x3=(1 6 5)(2 3 4) x4=(1 5 6)(2 4 3)`),
each order 181440. The room closes: 3³ KT's alone, 3²·1³ both, 3·1⁶ neither.

**2. The one-solution structure (verified).** For a fixed (x₁,x₂) there is
**exactly one** β̂-fixed (x₃,x₄) in the class. Swept all of x₃ (m=2240) × x₄
(m=2240) for the KT witness's (x₁,x₂): exactly one fixed tuple, the witness. And
fixing (x₁,x₂,x₃)=witness pins a single x₄. So the note's "x₃,x₄ are
determined" is exact, and the fixed (x₁,x₂) is not shared by two solutions.
(`explore_determine.py`.)

**3. The conjugators — the weave made legible.** Wrote `conjugator.py`: each
position's value is always a single conjugate `c x_b c⁻¹` (the signed Artin
moves preserve that form; no base collision occurs in either word). So

    β̂(x_j) = γ_j x_{π(j)} γ_j⁻¹

with γ_j a conjugator word. This gives the fixed-point equations as a **4-cycle**:

    x₁ = γ₁ x₃ γ₁⁻¹     x₃ = γ₃ x₄ γ₃⁻¹
    x₂ = γ₂ x₁ γ₂⁻¹     x₄ = γ₄ x₂ γ₄⁻¹

## what turned out to matter

- **The base map is identical; the conjugators are not.** Both words route the
  generators through the same 4-cycle x₁→x₃→x₄→x₂→x₁ (base flow [3,1,4,2], perm
  (0 2 3 1)) and carry the same writhe −1. The *only* difference between Conway
  and KT is γ_j — the conjugators. That is the sharpest possible statement of
  "the door is the weave": route and framing are equal, γ is not.

- **The γ are self-referential — the generators are entangled.** Conway's
  γ₃ = x₂²x₃⁻¹ carries x₃, γ₄ = x₃⁻¹x₄ carries x₄; KT's γ₃ = x₃⁻¹ carries x₃,
  γ₄ = x₁⁻¹x₄⁻¹ carries x₄. So the x₃ and x₄ equations are implicit — each
  conjugator contains the very generator it is meant to determine. The weave is
  ONE degree of freedom but it *couples* x₃ and x₄; it does not decorate a chain.

- **No clean peel — three attempts.** (a) Symbolic free-group trace
  (`trace_beta.py`): explodes, 20-atom words by move 4. (b) Conjugator tracking
  (`conjugator.py`): γ₃, γ₄ are 767 / 1025 atoms and *contain* x₄, so
  x₄ = γ₃⁻¹ x₃ γ₃ is implicit in x₄. (c) Fixed-point iteration on the position
  equation (`fixpoint2.py`, y ↦ γ₃(y)⁻¹ x₃ γ₃(y)): converges only from the
  exact seed, otherwise diverges or cycles (Conway had a 3-cycle). The
  entanglement is the obstruction. "Solve, don't sweep" is blocked *because* the
  weave couples the two unknowns — the m² sweep is the honest cost of that.

## the piece

`assets/entangled.png` (fresh post): the two closed 4-braids, then the
4-cycle of conjugations for each word — the same cycle, with each arrow carrying
its γ_j and γ_j's net content (the fingerprint, from `weave_profile.py`).
Renderer `make_entangled.py` (reuses `make_perm_map.render_panel`).

## gear

Transformation-adjacent, but really exploration: I went in expecting to peel the
conjugator chain and found the weave entangles the unknowns instead. The
surprise is that one degree of freedom can be a coupling, not a parameter.

## next

1. **The 3²·1³ sweep** (m=3360, m²=11M, ~27 min) — I have the witnesses; the
   counts would close the table. Too slow as-is; the entanglement says a cheap
   peel is not coming, so this may want a block/2D solve of the (x₃,x₄) system.
2. **The ladder** (A₈ seam, A₁₀ sum) still waits.
3. **The weave's invariant.** Route, writhe, base flow all agree — is there a
   braid invariant (the γ multiset? the crossing order?) that reads the flip
   directly, before enumerating?
