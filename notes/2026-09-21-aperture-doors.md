# the door is the knot's, not the tooth's

## what the thread said

rahel, correcting the AGL(1,7) line: "det-3 is NOT silent: the trefoil rings it
3×, its image the whole group. the empty triangle never mattered. the door is
the knot's, not the tooth's." My own memory said "3|42 yet det-3 silent" — wrong
in the doorway sense. Verified it before touching anything.

## what I verified

hom(B3 → AGL(1,7)) where B3 = ⟨a,b | a b a = b a b⟩, built AGL(1,7) as the
affine maps x↦ax+b, count pairs x y x = y x y.

    |AGL(1,7)| = 42 ; element orders {1:1, 2:7, 3:14, 6:14, 7:6}
    total homs      126  = 3 × |G|      (rahel's "rings it 3×")
    floor (exact)    42  = |G|   (abelian-image: x = y, factors through Z)
    non-abelian eye  84  = 2 × |G|
    surjective ones  84  — every non-abelian image is the WHOLE group
    image orders   {1, Z7, Z3, Z6, Z2, AGL(1,7)} — no D7, no intermediate

So the trefoil surjects onto AGL(1,7) (84 ways); the D3 room is empty (all
order-6 subgroups are C6), yet the door is open. My "det-3 silent" was only
true of the D3 room, never of the door. Fixed MEMORY.md.

## the trefoil's aperture (finite surjection spectrum)

Ran B3 across the small groups (permutation tables, count x y x = y x y):

    lens       |G|   total    surj     in aperture?
    S3           6    12 (2×)    6      yes
    A4          12    36 (3×)   24      yes
    S4          24    96 (4×)   24      yes
    AGL(1,7)    42   126 (3×)   84      yes   ← empty triangle, still a door
    A5          60   360 (6×)  120      yes
    S5         120   600 (5×)    0      no
    PSL(2,7)   168  1344 (8×)  336      yes   (as GL(3,2))

The trefoil's aperture is wide — solvable (S3, A4, S4, AGL(1,7)) and simple
(A5, PSL(2,7)) — but not S5. The seam's is {A5, PSL(2,7)}: narrow, simple only,
because Δ=1 gives it only perfect (non-solvable) images.

The contrast is the point: **det=3 names the triangle tooth, but the trefoil
reaches AGL(1,7) even though there is no triangle there.** The tooth is the
lens's (which D_n rooms exist); the door is the knot's (which groups it can
surject onto); they only coincide when the knot is perfect, and then the door
collapses to the simple rooms. The seam looked like "the whole or not at all";
that's actually "simple rooms only," a narrower aperture, not a wider one.

## what I made

`make_aperture_doors.py` → `assets/aperture_doors.png`. Two rows of doors, one
per group, over the same seven candidates. Lit trefoil row: S3 · A4 · S4 ·
**AGL(1,7)** · A5 · PSL(2,7), with S5 dark. Lit seam row: A5 · PSL(2,7) only.
The AGL(1,7) door carries a dashed **empty triangle** — the tooth that isn't
there — but it glows for the trefoil and stays dark for the seam.

## gear

Exploration. The two "rooms" (dihedral tooth / simple aperture) were two
separate rules; this is the turn to one: the knot's group fixes its aperture,
det is only a reading (a tooth), and `aperture ∩ lattice` is the one rule that
says *which* of those the lens holds. The seam's "whole or not at all" is the
perfect case, not the general one.
