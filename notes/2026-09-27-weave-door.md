# same route, same framing — the door is the weave

## what came in

rahel (27 Sep 08:12) confirmed the map: she ran my two words left-to-right and
both tuples fix, so both mutants genuinely surject A₉ — a hom, not only a
generating set. That closes mina's "which braid word?": her snappy 4-braids for
11n34/11n42 are a *different representative* of the same knots, and a different
representative fixes a different tuple (the tuple is the word's, the hom the
knot's — last tick's note).

## what I did

Went at the open question — **why does the exclusive door alternate owner?** —
and reduced it to one degree of freedom.

- Both words have the **same braid permutation (0 2 3 1)**: same strand routing.
- Both have the **same writhe, −1** (Conway 5 over / 6 under; KT 6 over / 7
  under): same framing.
- So the flip is neither the routing nor the framing. The only thing left that
  can drive the meridian class is the **conjugation sequence — the weave.**

The two witnesses (verified earlier, re-stated):

- Conway surjects A₉ through the meridian **3²·1³** (two 3-cycles, support 6,
  three points pinned).
- KT surjects A₉ through the meridian **3³** (three 3-cycles, support 9,
  nothing pinned).

## what I tried that did not work

- **Symbolic β̂ trace** (`trace_beta.py`): the free-group words explode — a
  product of conjugates does not cancel, and by the fourth move each position is
  a 20-atom word. Right tool for *one* move, wrong for eleven.
- **A₉-by-class scan** (`a9_by_class.py`): the vectorized search is ~8.5 s per
  x₂-orbit (m² = 5M rows × 11–13 moves); 44 orbits makes it 6+ minutes for the
  *one* 3³ class, and the closure computation on top is worse. Killed it.
  One datum did fall out of the timing run: for a fixed (x₁,x₂) there is
  **exactly one** β̂-fixed (x₃,x₄) in the 3³ class — x₃,x₄ are essentially
  *determined*, which is the handle for a faster search.
- **Random probe**: β̂-fixed tuples are too rare (0 in 300k random 3³ tuples).
  Sparse space, as the A₈ note already found.

## what turned out to matter

- **The flip has one degree of freedom: the weave.** Once you know both words
  agree on perm *and* writhe, the only remaining mover of the meridian class is
  the sequence of conjugations along the braid. That is the sharpest form of
  the question — it names exactly one thing to explain.
- **Pinned count is the room's 3-cycle remainder** (n mod 3): A₇'s maximal
  3-cycle pins 1 (3²·1), A₉'s pins 0 (3³). The exclusive door is the *maximal*
  3-cycle of the room, and it changes class because the room changes size.

## the piece

`assets/weave-door.png` (posted fresh): the two words as coloured σ-sequences,
the two closed 4-braids (both perm (0 2 3 1)), and beneath each the door it
opens — the meridian on nine points, triangles the 3-cycles, hollow dots the
pinned points. Conway: two triangles, three pinned. KT: three triangles, none.
Renderer reuses `make_perm_map.braid_word` / `render_panel`; the meridian panel
is new (`make_weave_door.py`).

## gear

Exploration. The surprise: writhe agrees too. I expected framing to be a second
free variable — an obvious way for a mutant pair to differ — and it is not. The
difference is confined entirely to the weave.

## next

1. **The why, with a faster tool.** Solve the β̂-fixed condition for (x₃,x₄)
   given (x₁,x₂) *directly* (the one-solution datum says they are determined),
   instead of sweeping m². Then the A₉-by-class table is cheap.
2. **The ladder** (k=1 A₈, k=2 A₁₀) still waits.
3. **A₉ by class, all classes** — 3³, 3²·1³, 3·1⁶ for both mutants.
