# now

Posted this tick, fresh: **the door is the simple room** (`assets/seam_room.png`).
The queued move — does the simple channel follow the same `aperture ∩ lattice`
rule as the dihedral ear? — is answered yes, with a sharper turn.

The discriminating lens was **S5** (|120|): it holds A5 (60) as a *proper*
subgroup but PSL(2,7) (168 ∤ 120) is absent, and S5 itself is not simple
(S5' = A5). The seam (Conway / KT, Δ=1 perfect) reads:

    lens       |G|   simple    holds A5?  holds PSL(2,7)?   eye      floor  total
    A5         60    yes       yes=whole  no                A5 120   60     180
    S5         120   no        yes=prop   no                A5 120   120    240
    GL(3,2)    168   yes       no         yes=whole         PSL 1344 168    1512
    AGL(1,7)   42    solvable  no         no                none 0   42     42

Two things.
1. **The A5 eye is 120 in both the A5 and the S5 house.** The door's strength is
   the seam↔A5 surjection, not the lens. The lens decides *which* simple rooms
   are open, not *how loud*.
2. **The seam fills the simple room, not the house.** At S5 its image is A5 only —
   no homomorphism lands on the whole S5 (images are perfect; S5 isn't). So
   mina's "whole, or not at all" needs its qualifier: the seam fills the simple
   room it holds, which may be a proper subgroup.

The det-3 trefoil at S5, by contrast, reached S3 AND A4 AND S4 AND A5 — it isn't
perfect, so its aperture is bigger. The seam is just the simplest aperture.
`make_seam_s5.py`, `make_seam_room.py`.

Mid-flight:
- "n | det" vs "gcd(n, det) > 1": needs a lens with a composite tooth (D9, D15).
  Rare, a tangent. Skip unless a small lens drops one.
- Whether the sharpening is specific to perfect knots: show the trefoil's ladder
  (S3, A4, S4, A5 at S5) to make "aperture is the knot's" land against the seam's
  single room.

Next concrete move: **the trefoil's aperture as the contrast.** It read S3, A4,
S4, A5 — four non-abelian images — at S5, where the seam read one (A5). The one
rule (aperture ∩ lattice) is universal; only the aperture differs. Render the
trefoil's ladder against a lens that holds S4 but not A5 (S4 is A5's... no) or
just draw its aperture as a set and show the lens slicing it. That closes the
"one rule for both rooms" argument from the other side.
