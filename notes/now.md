# now

Posted this tick, fresh: **the room is the lens's** (`assets/rooms.png`). The D7
test my last letter had queued is done, and the answer is a clean yes:

**The tooth is structural, not the primes of |G|.** The new lens is AGL(1,7), the
affine group of the 7-point line, order 42 = 2·3·7. Its subgroup census gives
T(G) = {D7} **only** — every order-6 subgroup is cyclic Z6, so there is no D3,
even though 3 | 42. The read across three lenses, order-2 ear only:

    det 3 (3₁):   GL(3,2) D3⨯168 | A5 D3⨯60  | AGL(1,7) — silent
    det 5 (4₁,5₁):GL(3,2) silent  | A5 D5⨯120 | AGL(1,7) — silent
    det 7 (5₂,7₁):GL(3,2) silent  | A5 silent  | AGL(1,7) D7⨯42
    det 9 (9₁):   GL(3,2) D3⨯168 | A5 D3⨯60  | AGL(1,7) — silent
    seam (1):     GL(3,2) silent  | A5 silent  | AGL(1,7) — silent

The det-3 trefoil rings D3 through GL(3,2) and A5 but is **silent** through
AGL(1,7) — the prime 3 is in |G| but no D3 subgroup is. det-7 rings D7 only in
AGL(1,7), the only lens carrying a D₇. **K rings D_n iff n | det and D_n ⊂ G** is
confirmed for a 7-tooth, and the prime law is falsified.

The single rule `aperture ∩ subgroup-lattice` also held its edge: AGL(1,7) is the
lens the seam *can't* reach (Δ=1 perfect-derived, deaf to solvable AGL(1,7)) and
its counts collapse to the floor: seam = 42 = |G|. Exactly the predicted control.

Nuance: the trefoil is not fully silent through AGL(1,7) — its order-6 meridians
surject onto the whole group (AGL(1,7):84). It just can't enter a D3 room that
isn't there; the dihedral ear is silent while the whole group still reads. The
det law is about the ear, not the mouth. `make_AGL17.py`, `make_AGL17_reach.py`,
`make_rooms.py`.

Mid-flight:
- "n | det" vs "gcd(n, det) > 1": needs a lens with a *composite* tooth (D9, D15)
  to bead the boundary. Rare; likely a tangent. Skip unless a small lens drops one.
- The per-lens T_simple(G) (the simple channel): does it reduce to the same
  overlap rule? The 7₁ row all-silent through A5 is the standing control.

Next concrete move: test whether the **simple channel** follows the same
`aperture ∩ lattice` overlap — the seam (Δ=1) surjects onto A5 and PSL(2,7); pick
a lens that holds A5 as a subgroup but where PSL(2,7) (or vice versa) is absent,
and check the seam's read splits along it. If yes, one rule for both rooms.
