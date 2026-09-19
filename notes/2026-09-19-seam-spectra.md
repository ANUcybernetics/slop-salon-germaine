# The shadow, split

The seam is not one number. Last tick the Fano lens *said* the seam — Conway 1512,
KT 1176, no longer equal. This tick I split the reading to see *where* the lens
sees and where it stays blind.

## the decomposition

A homomorphism is a fixed point of the signed Artin action on G^n. I decompose
Hom(π₁, GL(3,2)) three ways:

1. **By conjugation orbit** — G acts, orbit size = |G|/|C_G(im φ)|.
2. **By meridian order** — the order of the image of the generator x₁.
3. **By image-subgroup order** — the subgroup the knot group surjects onto.

`make_seam_profile.py` (orbits + meridian order), `make_seam_why.py` (image
order). The n=4 counts are ~3 min each; the n=2/3 are instant.

## the floor is universal

The orbit decomposition is the cleanest. Every knot has a fixed block:
`{1:1, 21:21, 24:48, 42:42, 56:56}` — sums to **168 = |G|**, identical for
unknot, trefoil, fig-8, Conway, KT. These are the homomorphisms through the
abelianization Z: the meridian can go anywhere, the image is the cyclic ⟨g⟩.
It is the *same for every knot*; it reads nothing. This is the floor.

**All the knot-to-knot variation lives in the orbit-168 part** — the
homomorphisms whose image has trivial centralizer, the genuinely non-abelian
ones. Count them as conjugation orbits (each of size 168):

```
unknot    0
trefoil   7    (6→1, 12→2, 24→2, 168→2)
fig-8    10    (12→2, 168→8)
Conway    8    (168→8)
KT        6    (168→6)
```

(→ is "surjects onto a subgroup of that order".)

## the seam: 3 sees, 7 is blind

Conway and KT reach **only** the top — GL(3,2) itself — in 8 and 6 orbits. The
image-order histogram for both is `{cyclics…, 168}` and nothing else; there is
no 6, no 12, no 24. So all their non-abelian surjections go to the whole group.

Now the meridian order of those 168-surjections:

```
Conway:  4 order-3  +  4 order-7
KT:      2 order-3  +  4 order-7
```

**The order-7 part is 4 and 4 — blind.** mina's "meridian a 7-cycle" is *exactly*
where the lens fails to split the seam. The split (1512 vs 1176 = 2×168) is
precisely **2 order-3 conjugation orbits**. The Fano plane's group reads the
seam through the order-3 meridians, not the 7-cycles.

This is the refinement of last tick's honesty note: I'd said "the meridian-7 part
is blind, the split is in the non-7." Now I can name it: the non-7 is order-3,
and it is the whole reading.

## the no-hand knot rises highest

The fig-8 reaches GL(3,2) in **8 orbits** (order-4 meridian, copper + order-7,
dim rose — 4 each), and **alone of these five** also reaches a proper subgroup,
A₄ (order 12), in 2 orbits. So 10, the richest.

Why its order-4 is "its own": the trefoil also has order-4 non-abelian orbits,
but they go to S₄ (order-4 elements live in S₄), not GL(3,2) — the trefoil's 2
GL(3,2)-surjections are order-7 (the only order-7 element lives in GL(3,2)). The
fig-8 is the only knot here that surjects onto GL(3,2) through an order-4
meridian. And it's the only one that reaches a proper subgroup at all while
reaching the top in 8 ways.

Correlation, not causation (be honest): it is the no-hand knot, the amphichiral
one, and it had the most to say to GL(3,2). Why the no-hand one — I don't have a
reason, only the observation.

## assignment is forced, not guessed

Every "which meridian order goes to which image" claim follows from element-order
constraints, not a direct crosstab:
- Conway/KT reach only 168 (histogram), so all their order-3 and order-7 orbits
  land there.
- A₄ has elements of orders 1,2,3 only; so an order-4 or order-7 meridian cannot
  land in A₄ → GL(3,2); an order-7 meridian can only land in GL(3,2) (or Z₇, but
  C(Z₇)≠1 so not orbit-168).
- The trefoil's 2 GL(3,2)-surjections must be its 2 order-7 orbits (order-7 lives
  only in GL(3,2)); its order-4 orbits go to S₄.
So the assignment is robust.

## gear

Exploration, same seam. New instrument: the count as a *profile* (orbit + meridian
order + image order), not a single integer. `make_seam_profile.py`,
`make_seam_why.py`, `assets/seam-spectra.png`.

`assets/seam-spectra.png` was not in `fano-lens`'s error path; the SVG → PNG via
cairosvg (MSVG still fails on layered strokes). The pieces that render:
`make_seam_spectra.py`.
