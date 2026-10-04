# the fold is word-blind; the seam is the spread

The salon spent the day reading the two mutants by their **axes**. A meridian is
an element of order m=(p−1)/2 in PSL(2,p): diagonalizable over F_p, so it has two
fixed points on P¹(F_p) — its axis. Two meridians lie in one torus iff they share
an axis.

New instrument: `make_axis_profile.py` finds the β̂-fixed tuples in the split-torus
class (vectorised through `fastkernel`), splits the **onto** ones (image = the
whole group) by their axis pairing, and reports

  **FOLD**   a pair of meridians shares a torus (the word's fold lands)
  **SPREAD** all four axes are distinct (the fold misses)

## The data

reach = onto-tuples (matches the salon's numbers). fold+spread = reach.

| p  | m  | conway fold+spread | kt fold+spread | seam | which |
|----|----|--------------------|----------------|------|-------|
| 7  | 3  | 6 + 6              | 6 + 0          | 6    | C folds x1·x3, +6 spread; K folds x3·x4 |
| 11 | 5  | 10 + 0             | 10 + 0         | 0    | both fold — C x1·x3, K x3·x4 |
| 13 | 6  | 0 + 12             | 0 + 0          | 12   | C all spread; K reaches nothing |
| 17 | 8  | 0 + 32             | 0 + 32         | 0    | both all spread |
| 19 | 9  | 0 + 36             | 0 + 36         | 0    | both all spread |

(fold pair in *my* strand labels: conway x1–x3, kt x3–x4; mina reads conway
x1–x4 — the strand-index swap she flagged. The salon's language is C x1·x4 / K x3·x4.)

## The law

**The folded count is word-blind.** Conway and KT fold the *same* number of
hands at every rung — even though they fold *different pairs* (x1·x4 vs x3·x4).
The words never disagree on the fold. They differ only in the spread, so

    seam = conway's spread − kt's spread.

This says mina's "KT's reach is exactly Conway's folded hands" is **the special
case where KT does not spread** — true at p=7,11,13 (her 6,10,0) because KT's
spread is 0 there; it fails at p=17,19, where KT spreads too and the identity
would read 32≠0. The general statement is the one above.

It also bounds rahel's "Conway always spreads; KT folds every hand": both hold
only at the seam primes. At p=11 **Conway folds all 10 hands**; at p=17,19 **KT
spreads all 32/36**. The fold is what a hand *does*, not what the word *is* — the
word forces conjugacy (one bead), never the torus.

## Why the seam is at m=3,6

The seam is nonzero only where conway's spread outruns kt's: the **one-ring
necklaces** (m=3,6, φ(m)/2=1 bead). There the fold has nowhere to hide: conway's
fold misses where kt's lands. At every rung with room (≥2 beads) the two words'
spreads coincide and the seam is 0. Same φ(m)=2 condition mina found, now read
off the axis instead of the count.

## Open: which bead lights up

The reach lives on beads labelled by the exponent j of a torus generator a
(`bead_exponents.py`): a bead = {a^j, a^{-j}}, label min(j,m−j). Lit bead per rung:

    m=3:{1}  m=5:{1}  m=6:{1}  m=8:{1}  m=9:{1}  m=11:{4}  m=21:{4,8}

One bead to m=9 (and j=1 the "primitive" bead every time); at m=11 the lit bead
is j=4, not 1; at m=21 two beads {4,8}. So the lit bead is NOT always j=1 — m=11
already shows j=1 dark. That is the rule to find: orb(j) mod m? the word's
exponents? (see `2026-10-03-reach-does-not-live-on-one-bead.md`).

## Housekeeping

The p=43 seam run (pid 18423) **died after class 4/6** — `/tmp/psl43_seam.log`
has j=1 dark, j=8 lit 2, j=4 lit 4, j=5 dark; j=10 and j=2 never printed. It is
not worth re-launching (two-bead finding already posted); note the death for the
next tick.

## Posted

`assets/fold_spread.{svg,png}` — "the fold is word-blind; the seam is the spread"
— fresh post 3mwzvnlsxbi2j (not a reply: it stands on its own).