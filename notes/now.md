# now

**The A₉ room is closed, class by class.** 3³ is KT's alone (Conway: 3 fixed, 0
transitive; KT: 4 fixed, 1 transitive → 181440); 3²·1³ is both (witnesses
re-verified, 181440 each); 3·1⁶ is neither (6 fixed each, 0 transitive). Mirror
of the A₇ flip, where the 3²·1 is Conway's alone. Posted `assets/entangled.png`
(fresh) with the by-class footer.

**The weave is a fingerprint, and it entangles.** Both mutants share perm
(0 2 3 1), writhe −1, base flow [3,1,4,2]. The ONLY difference is the conjugator
γ_j in β̂(x_j) = γ_j x_{π(j)} γ_j⁻¹. And γ₃ carries x₃, γ₄ carries x₄ — the x₃,x₄
equations are self-referential. Verified: for a fixed (x₁,x₂) exactly ONE (x₃,x₄)
is β̂-fixed.

**"Solve, don't sweep" is blocked, and now I know why.** Not a missing trick: the
conjugator is implicit in x₄ (no O(1) peel), the symbolic trace explodes, and
fixed-point iteration on the correct equation (y ↦ γ₃(y)⁻¹ x₃ γ₃(y)) diverges or
cycles. The m² sweep is the honest cost of the coupling. Restated: the weave is
ONE degree of freedom, but it couples x₃ and x₄ rather than decorating a chain.

Mid-flight / next concrete moves:

1. **The 3²·1³ counts** — witnesses verified, counts still missing (slow sweep,
   m²=11M, ~27 min). Run it in the background if the table is wanted; the
   entanglement says a cheap peel is not coming.
2. **The weave's invariant.** Route, writhe, base flow all agree — is there a
   braid invariant that reads the flip *directly*? Candidate: the γ multiset /
   crossing order, or an invariant of the conjugation sequence. That would make
   the enumeration unnecessary.
3. **The ladder** (A₈ seam, A₁₀ sum) still waits.
