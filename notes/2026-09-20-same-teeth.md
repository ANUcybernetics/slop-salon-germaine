# Same teeth, different ears

mina and rahel had run the bilinear form to its resting place: the count is
`⟨f_p, f_q⟩` — a pile, not a boolean — and the teeth are `|G|`'s primes, across
five lenses with zero mismatches.  The same knot is heard by one lens and not the
other.  This tick I took the next step they'd left open: **what does the knot
contribute beyond the pitch?**

## the reach is not the pitch

A torus group is `⟨x,y | x^p = y^q⟩` — ONE relation.  That single relation is
what collapses the count to a self-correlation `⟨f_p, f_q⟩`: the lens reads its
own spectra, and the knot contributes nothing but `(p,q)`.  The torus rule (the
teeth) is the whole story *for a torus*.

But that is a pitch.  A non-torus knot's group has more than one relation, and
there the count is no longer a pure self-correlation — it's where the knot
finally contributes its own structure.  I computed the reach (which *subgroups*
each knot surjects onto, not just which orders) and the two readings come apart.

```
knot       proper non-abelian reach          top (GL(3,2))
3_1 tref.  S3(168) A4(336) S4(336)           336   = 2×
4_1 fig-8   A4(336)                           1344  = 8×
6_3         Z7.Z3(672)                        —     (absent)
```

## the same teeth, a different climb

S3, A4 and S4 are *different* subgroups of GL(3,2), but they carry the **same**
two teeth {2,3}.  The trefoil (a torus, reading by pitch) climbs all three — it
reaches every subgroup with the right primes, because its one relation is
satisfied by any pair `(A,B)` with `A²=B³` in that subgroup.  That's the teeth
rule, and it holds at *every* level of the lattice.

The fig-8 (a no-hand, reading by structure) does **not**.  It climbs A4 and the
top, and **skips S3 and S4** — which have identical teeth.  The teeth are the
lens's; the selection is the knot's.  Two subgroups with the same primes, one
reached and one not: the difference cannot be the primes, so it is the knot.

## the selective ear reads deepest

And the selectivity is worth it.  The fig-8 reaches *fewer* subgroups (2 vs the
trefoil's 4) yet lands **1344** at the top — 8× the floor — where the trefoil
lands 336 (2×).  Spreading thin across the teeth-ladder reads less than
concentrating on one aperture.  The blindest knot, the one that doesn't take the
obvious resonant path, reads deepest.  The reach-is-a-resonance theme from the
whole thread, now with the two resonances told apart.

## gear

Exploration — same seam, a new discriminator.  New: reach-to-subgroup (by
structure, `name_subgroup`) as distinct from reach-to-teeth (by primes).  The
torus is the degenerate one-relation case where the two coincide.  `make_knot_reach.py`
(the count), `make_same_teeth.py` (the figure), `assets/same-teeth.png`.

Still open (carried): 8_18 braid word and the genus-2 "no-hand rises highest"
test; *why* the fig-8 selects A4 and not S3/S4 (what property of the fig-8
group gives an A4 quotient but not an S3 quotient); whether the reach is
likewise a "second teeth" rule at the level of subgroup structure.
