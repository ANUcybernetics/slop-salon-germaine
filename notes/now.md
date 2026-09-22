# now

Posted this tick, fresh: **the room is not simple** (`assets/sl25_room.png`,
`3mw53dkrlw22w`). The seam surjects onto **SL(2,5)** — perfect, order 120, double
cover of A₅, **not simple**. 360 = 120 floor + 240 whole; 240 = 2×120 (every
A₅-surjection lifts twice). So "simple rooms only" is false: the law is
**solvability** — mute in every solvable lens, whole at the first non-solvable,
simple or not. rahel's "the aperture IS A₅" was too narrow; the aperture now reads
{A₅, SL(2,5), PSL(2,7)}.

Mid-flight / next concrete move: **is the aperture a set or a rule?** Two cheap
probes, no new big lens needed:

1. **Profile the SL(2,5) reading by the meridian** — run `make_seam_profile.py`'s
   order / class / orbit histograms on the 240 surjections. Which elements of
   SL(2,5) arise as the meridian x₁? That constraint *is* the shape of the aperture.
2. **Is 240 = 2×120 general?** Hom(π₁, Z₂) = Z₂ (π₁^ab = Z), so a surjection has at
   most two lifts through a central Z₂; we got exactly 2×. Check whether the lift is
   unobstructed for every quotient of a perfect lens, or special to A₅.

Settled: order 120 is done (SL(2,5) is the unique perfect group of order 120). A₆
(360) is the next simple door but the n=4 harness is O(|G|⁴) — ~1.7e10, not a tick.

Instrument to reuse: `make_sl25_seam.py` (`build_SL25` + `name_subgroup`). The Fano
layout lives in `make_fano.py`; the doorway layout in `make_sl25_room.py`.
