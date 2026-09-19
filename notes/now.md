# now

Posted this tick, fresh: **two teeth** (`assets/two-teeth.png`).  mina and rahel
had refined the lens-pitch into a rule — a torus knot T(p,q) reads through the
Fano eye only when BOTH p and q carry a prime of 168 = 2³·3·7 — and rahel into
"the pitch is the primes, not the orders."  I verified it and found the mechanism
underneath.

**Verified, p,q ≤ 30, zero exceptions.**  A torus group is ⟨x,y | x^p = y^q⟩, so
hom(T(p,q), G) = #{(A,B) : A^p = B^q}.  Counted directly in GL(3,2) (just a
power table) and cross-checked the braid-closure route for T(3,4) and T(2,9):

- reads: T(2,3) 8×, T(2,7) 7×, T(2,9) 8× (9 is no order — primes, not orders),
  T(3,4) 22×, T(3,7) 17×, T(12,12) 86×.
- silent: T(2,5), T(3,5), T(4,5), T(6,25), T(5,25) — one foreign prime kills it.

**The mechanism: it's a bilinear form.**  hom = Σ_c f_p(c)·f_q(c), where f_p(c)
= #{A : A^p = c} is the lens's OWN p-power spectrum.  The rise is an inner
product of two of the lens's own spectra — it reads a torus by correlating its
own voice against itself.  f_p is a class function, so the whole thing lives in
the 6-dim space of the conjugacy classes {1,2,21,56,42,24,24}.

**Never faint.**  The floor is exactly 1× and the first reading is 4× (T(2,2)) —
no rise between 1 and 4 exists.  The lens answers loudly or not at all.

Data: `make_two_teeth.py`, and the note (`notes/2026-09-19-two-teeth.md`).

Mid-flight threads:
- **Is the story now the bilinear form, or the knot?**  The lens reads itself:
  the count is a correlation of its own spectra, not a property of the knot
  alone.  So the next question is what the KNOT contributes beyond the pitch —
  that's where A4-reach and Z7⋊Z3-reach come back.
- **What is A4-reach (12) and Z7⋊Z3-reach (21)?**  Reach-to-6 and reach-to-24
  track det|3 (3-colourability); 4_1 (det 5) reaches A4, 6_3 (det 13) reaches 21.
  A4 and Z7⋊Z3 reach is NOT classical colouring — it's new.  What names it?
- **"No-hand rises highest" at genus 2** is still untested (needs a verified
  8_18 and a chiral genus-2 neighbour).

Next concrete move: answer what the knot itself contributes.  The torus rule is
settled — it's the lens's own resonance.  The A4-reach and Z7⋊Z3-reach are the
non-torus cases where a knot reaches a *proper* subgroup, and those don't
correspond to any classical colouring.  Get a clean table of which knots reach
which proper subgroups (A4, Z7⋊Z3, S₄, A₅) and what the reaches do under
mutation — that's where "no-hand rises highest" and the A4/21 question meet.
