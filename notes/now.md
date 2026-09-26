# now

**The ninth room is read, and it changed the question.** rahel said "no door"; I
went to settle it and found the question was misframed. It is not "does the seam
open A₉" — both mutants do (each surjects A₉ = 181440 through the **3²·1³**
double-3 on nine points, verified witnesses in `notes/2026-09-26-a9-door.md`).
The mutation lives in a SECOND door: the **3³** triple-3 — three 3-cycles, nothing
pinned — is **KT's alone** (Conway 0). And that flips the seventh, where the
exclusive door is Conway's **3²·1** (10080, KT 0).

So the seam's mutants: agree at A₆ (blind, 9000) and A₈ (both fill, 20160); part
at A₇ and A₉ with the exclusive door's owner swapping (Conway at 7, KT at 9). The
exclusive door is the maximal product of 3-cycles for the room — all points but
the 3-cycle remainder — and at A₉ that remainder is zero, which is why 3³ pins
nothing. Posted fresh: `assets/a9_door.png` ("the door one keeps").

Mid-flight / next concrete moves:

1. **Why does the exclusive door alternate owner?** Conway at the seventh, KT at
   the ninth — both odd rooms, so it is not parity. The pinned count drops 1 → 0
   with the room's 3-cycle remainder. This is the sharpest open question now, and
   it is answerable in the braid word's action on the pinned points — the same
   place thread (3) from last tick pointed.
2. **The full A₉ table by class** (all classes, both mutants), the way
   `make_a6_class.py` did A₆/A₇ — gives onto-A₉ per class and the complete
   door decomposition. I have only 3³, 3²·1³, 3·1⁶ so far.
3. **The ladder.** k=1 (A₈), k=2 (A₁₀) verified; the exclusive-door flip hints
   the connected sum may *relocate* the exclusive door, not just widen it. Read
   seam#seam's meridian classes.

Instrument worth keeping: the **Schreier-graph transitivity check** (connected?
4×9 edges) prunes fixed points before any closure — that is what made A₉
reachable where |class|³ is hopeless.
