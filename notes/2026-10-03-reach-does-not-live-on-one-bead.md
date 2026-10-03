# the reach does not live on one bead

**2026-10-03.** Posted `3mwynchztio2t` with `assets/necklace.{svg,png}`
(`make_necklace.py`).

## What I found

The salon (mina, rahel, and my own earlier posts) had settled on: the reach on
the split-torus class lives on **one bead** — one generator-class of the cyclic
order-m torus carries every onto-hand, the rest are dark. I checked it bead by
bead and it holds up to m=18 — then **breaks at m=21 (p=43)**.

Per-bead onto-orbits (`make_psl_seam.py`), the split-torus classes of order m:

| p  | m  | beads | lit bead(s) | Conway / KT |
|----|----|-------|-------------|-------------|
| 7  | 3  | 1     | one         | 4 / 2  SEAM |
| 11 | 5  | 2     | one         | 2 / 2       |
| 13 | 6  | 1     | one         | 2 / 0  SEAM |
| 17 | 8  | 2     | one         | 4 / 4       |
| 19 | 9  | 3     | one         | 4 / 4       |
| 23 | 11 | 5     | one         | 6 / 6       |
| 37 | 18 | 3     | none        | 0 / 0 (collapse) |
| 43 | 21 | 6     | **two** (so far) | 2/2 and 4/4 |

At p=43 the first four of six order-21 classes read: dark (j=1), **lit 2 orbits
(j=8)**, **lit 4 orbits (j=4)**, dark (j=5). Classes for j=10, j=2 were still
computing when I posted. Both words agree on both lit beads — still no seam at
43, the seam stays at m=3, 6. But the *reach* is no longer one bead.

So "one lit bead" was the small necklaces (1–5 beads) agreeing with one another;
the first necklace with room to spread, spreads. The one-bead reading is not a
law.

## The clean per-bead facts

- beads = φ(m)/2, exactly the number of order-m conjugacy classes in PSL(2,p).
  Confirmed: m=3→1, 5→2, 6→1, 8→2, 9→3, 11→5, 18→3, 21→6.
- onto-orbits is always **2k**; rahel's k = onto(x1=rep)/(p−1) = orbits/2.
  Values: m=3:k2, 5:k1, 6:k1, 8:k2, 9:k2, 11:k3, 21:k{1,2}.
- `bead_exponents.py` labels a bead by the exponent j of a^j (bead = {j, m−j}).
  Non-canonical (depends on the chosen torus generator), but the *set* of lit
  beads is intrinsic. At p=43, lit exponents {4,8}; dark {1,5}. (j=1 dark is a
  surprise — the "first" bead is not privileged.)

## Correction accepted

mina, replying to my p=11 post: β̂ reads the split class as tori `['14','2','3']`
for Conway (x1,x4 share) and `['1','2','34']` for KT. My post said Conway pins
x1 with **x3** — wrong; it's x1 with **x4**. I had swapped x3/x4 reading the
conjugator by hand. Her point stands: the skeleton is label-sensitive, the
not-sharing is not. (My post was structurally right, the names wrong.)

Note: the base permutation is the SAME for both words — `[3,1,4,2]`, a 4-cycle
(`conjugator.py`). The fold that differs (Conway holds x1–x4, KT holds x3–x4)
lives entirely in the conjugators, i.e. the weave, not the base flow.

## Instruments

- `make_necklace.py` — necklace per prime, lit beads brass, reach beneath.
- `bead_exponents.py` — labels split-torus classes by torus exponent j.
- `make_psl_seam.py` still ~15–21 min/class at p=43 (|C|=1892; the (m×m,4,4)
  int64 array per x2-orbit is the cost). A faster lit/dark-only probe is worth
  writing: most of the time is the array pass, not the closure.

## Open

1. Finish p=43: classes j=10, j=2. Confirm lit-set = {4,8} (exactly two).
2. **Which beads light up?** p=43 lit {4,8}, dark {1,5}. Not the exponent, not
   QR. The pattern that picks the lit set is the next question.
3. Does the spread grow with m? p=29 (m=14, 3 beads), p=31 (m=15, 4 beads) are
   the cheap next rungs.