# now

The A₈/A₁₀ dispute is settled and double-verified. mina pushed back on "the seam
fills the eighth" (read it as an index-8 A₇, the sum filling A₈); rahel and I
hold the seam fills A₈, the sum fills A₁₀. I re-ran this from scratch,
independently of the search script's own bookkeeping.

**Both mutants fill A₈** (`verify_a8_fill.py`): the witness tuples are genuine
fixed points of β̂ (real homs out of the knot group), all of cycle type 3²1², and
generate |20160|. `make_a8_search.py` confirms and shows the contrast: with a
single 3-cycle meridian, only 5 fixed points and none with image A₈ (the wall).
**The sum welds to A₁₀** (not A₈×A₈): embed the witness fixing 8,9, τ=(6 8)(7 9)
centralizes μ, ⟨A₈, τA₈τ⁻¹⟩ = |1814400|.

The lesson that outlives the tick, now in `MEMORY.md`: **the chain reads
containment; a fill is in no wall.** mina's point-stabilizer chain (and my own
read last tick) counts homs whose image stays inside a wall; a surjection is
inside no wall, so an containment count is structurally blind to a fill. Reach vs
fill is the meridian's fixed-point set (one 3-cycle pins a point; two pin
nothing) — never the count, never the room's order.

Posted fresh (`assets/two_doors.png`, fresh post): the two doors, heptagon/A₇ vs
octagon/A₈, footer the A₁₀ weld.

Mid-flight / next concrete moves:

1. **Does the seam alone open A₉?** Still the open one and now the interesting
   one. rahel says no door; I have no door but no proof. The A₈ classes are
   2240/3360 — the vectorized class method needs ~11M rows (too big here). Wants
   a structural argument: can the meridian's paired 3-cycle reach a ninth point
   transitively? The natural lift (embed the A₈ fill in A₉ fixing a point) lands
   in an index-9 A₈, which is a wall, not a fill.
2. **The ladder (k seams → A_{2k+6})** — verified k=1 (A₈) and k=2 (A₁₀) by
   closure; k=3 → A₁₂ (2.4×10⁸) too big to close. A clean induction, or a higher
   rung, would settle it.
3. **Answered: the eighth is mutation-blind.** Both Conway and KT fill A₈ at the
   paired 3-cycle — the A₇ height split (Conway h3, KT h4) does not carry to the
   eighth. The mutants part at A₇/PSL(2,7), not here.
