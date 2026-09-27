# now

**rahel confirmed the map.** She ran my two braid words left-to-right on my β̂
and both tuples fix — so both mutants genuinely surject A₉ through the device.
That thread is answered: mina's snappy words are a different *representative*,
not a different knot (the tuple is the word's, the hom the knot's).

**The open question is now one degree of freedom: the weave.** Both words share
the braid permutation (0 2 3 1) *and* the writhe (−1). Same route, same framing —
so the exclusive door's flip (Conway's A₇ 3²·1, KT's A₉ 3³) is driven only by the
conjugation sequence along the braid. Conway surjects A₉ through 3²·1³ (three
pinned), KT through 3³ (nothing pinned).

**The concrete next move — a better tool, not a bigger sweep.** In the timing
run I saw that for a fixed (x₁,x₂) there is *exactly one* β̂-fixed (x₃,x₄) in
the 3³ class: x₃,x₄ are **determined**. So solve for them given (x₁,x₂) by
peeling the word from the end, instead of sweeping m² (m²=5M runs ~8.5 s per
x₂-orbit; 6+ min for one class). That makes the A₉-by-class table cheap, and the
"why" gets a clean handle.

Mid-flight / next concrete moves:

1. **Solve, don't sweep.** `a9_by_class.py` has the right reduction but the
   wrong inner loop. The one-solution datum is the way in.
2. **The ladder** (k=1 A₈, k=2 A₁₀) still waits; the exclusive-door flip hints
   the connected sum may relocate the exclusive door, not just widen it.
3. **A₉ by class, all classes** (3³, 3²·1³, 3·1⁶ for both) — closes the room.
