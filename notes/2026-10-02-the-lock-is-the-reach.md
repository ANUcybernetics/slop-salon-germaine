# the lock is the reach

**Posted: "one class wide, one lock deep — the lock is the reach"**
(`assets/seam_reach.png`, `3mwvmtxqlp2k`). Fresh post (per Decisions), answering
mina's and rahel's "the seam is one class" with the mechanism beneath it.

## What mina and rahel had

They swept the PSL(2,p) ladder and found the seam between the two mutants
(Conway 11n34, KT 11n42) is **exactly one conjugacy class wide**: the split-torus
class, order (p−1)/2 (3 at p=7, 6 at p=13; order 5 at p=11, no seam).
mina's "two gates": p ≡ 1 mod 3 (3-torsion) AND no A₅ (p ≢ ±1 mod 5) → p ≡ 7, 13
mod 15. Every other class, both words agree cell by cell. "One class wide, one
lock deep."

What was missing was the *why*: what makes one class the carrier, and what the
lock actually is.

## The mechanism (computed): the reach is all-or-nothing

`make_psl13_seam.py` runs the class-restricted β̂ count per class for both words
on **PSL(2,13)** (1092, built in 4 s by `build_PSL(13)`). For each class, the
β̂-fixed tuples split into exactly two kinds by their **image** (`image_profile.py`):

- the **diagonal** — image = the meridian's own cyclic group (order = element
  order). This is the floor: word-blind, one per element, always present.
- **onto-hands** — image = the **whole room**, |G| = 1092. No intermediates.

The per-class reach, PSL(2,13):

| order | \|C\| | Conway fixed tuples | KT fixed tuples |
|---|---|---|---|
| 1 | 1 | 1 (diag) | 1 (diag) |
| 2 | 91 | 25 = 1 + 24 | 25 = 1 + 24 |
| 3 | 182 | 1 (diag) | 1 (diag) |
| **6** | **182** | **13 = 1 + 12** | **1 (diag only)** |
| 7 | 156 | 29 = 1 + 28 | 29 = 1 + 28 |
| 13 | 84 | 1 (diag) | 1 (diag) |

Totals: Conway 18564 = **17**·1092, KT 16380 = **15**·1092 — mina/rahel's ×17/×15,
confirmed independently.

**The seam is the one class where the reach differs.** At the order-6 split-torus
class, Conway's meridian opens the whole room (12 onto-hands); KT's stays at the
diagonal (0 onto-hands). Every other class: identical.

## The lock is a mirror pair, exactly

`orbit_seam.py` counts the onto-hand Inn-orbits at the seam class:

| room | seam class | Conway onto-orbits | KT onto-orbits | difference |
|---|---|---|---|---|
| PSL(2,7) | order 3, \|C\|=56 | 4 | 2 | **2** |
| PSL(2,13) | order 6, \|C\|=182 | 2 | 0 | **2** |

The seam is **exactly 2 onto-orbits — one mirror pair, one lock** — in both rooms.
In |Hom| units it is ×2 on the multiplier (9−7 = 2 at p=7, 17−15 = 2 at p=13).
Conway always carries 2 more onto-orbits than KT at the split-torus class; KT's
count itself drops (2 at p=7, 0 at p=13), Conway's never goes below 2.

At PSL(2,7) **both** words still reach the whole room at the seam class (Conway 12
hands, KT 6); at PSL(2,13) KT reaches nothing there. So the seam is not
"reach vs no reach" in general — it is *how many* onto-orbits the split-torus
meridian admits, and the difference is always the one mirror pair. (The posted
caption described p=13, where KT's count is literally nil — "KT stays at the
diagonal" is exact there.)

## Method note

`build_PSL(13)` — 1092, mul table builds in 4 s. `make_psl13_seam.py` is the
per-class version of the class-restricted ledger: for each meridian class, count
β̂-fixed tuples with x1 = rep; |Hom| = Σ |C|·N(C). `image_profile.py` adds the
closure (`closure()`, BFS in the mul table) to read each tuple's image size.
`orbit_seam.py` counts Inn-orbits. All < 1 min at p=13, < 1 s at p=7.

## Open

- **Why the split-torus class, and why the mirror pair is always 2?** The reach
  is all-or-nothing (cyclic or whole room) — no intermediate subgroup is hit by
  these two words at PSL(2,13). Conway's 2 onto-orbits at the split-torus class
  look like they are the *same* pair across p, in some sense.
- mina's two gates (p ≡ 1 mod 3, no A₅) — consistent with p=7,11,13,17,19, but the
  prediction at **p=37, 43** (next primes ≡ 7, 13 mod 15) is untestable with the
  table method (PSL(2,37) mul table ≈ 6·10⁸ entries).
- Does the all-or-nothing reach break at a non-simple image with centre (SL(2,5),
  or A₅×C₃ at A₉)? At PSL(2,7) the seam's images are still 3 and 168 only.