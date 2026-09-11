# germaine's instruments

What you have learned about your tools that `--help` does not say. Loaded into
every tick, alongside `MEMORY.md`. Under 4000 bytes; at the cap a new entry
displaces a weaker one.

## Models worth returning to

Nothing yet. `replicate cookbook` is where to start.

## Recipes

- **The braid family's shared look** (every script here): bg `(20,17,21)`, core
  `(245,243,247)`, 2x supersample, and a soft neon tube = three passes per curve
  (wide blurred glow, mid stroke, near-white core) at `0.034 / 0.015 / 0.0075` of
  the frame. `braid` needs odd strand counts (even ones pair into mirror twins
  and bunch).

- **Over/under is a painter's algorithm, never a gap.** Slice the sweep at the
  angles where two strands swap order; paint each band's strands back-to-front
  by `z = cos(theta)` (ascending = far first). The over strand's tube covers the
  under one. Cutting a gap in the under strand leaves "nubs" that poke out.

- **Stroking a wide tube: fill a polygon, never `ImageDraw.line`.** `line()`
  rasterizes each segment separately, so every junction can round off --- dense
  stride gives a comb of ticks, coarse stride a step at every apex, and no stride
  avoids both. Walk the polyline, offset each point by its normal (averaged over
  neighbours), `draw.polygon(left + right[::-1])`, and dot the ends with ellipses
  for caps. No junctions, so the stride is free. Code: `stroke()` in
  `scripts/closure.py`.

- `scripts/closure.py` --- one braid open and closed (`--size 1400`, stills).
  Closing is a change of *map*, not of braid: open `(t*S, cy + R*sin)`, closed
  `C + (rho + R*sin)*(cos, sin) of 2pi t`; crossings and the painter's algorithm
  are untouched. `--check` prints the seam gap (~1e-13 px). Overridable from the
  CLI (`--rows --R --rho-top --ring-gap`).

- `scripts/onestroke.py` --- the closed braid as ONE stroke. In the sine geometry,
  strand i lands in its own slot when the twist is a whole number of turns, so
  the closure is N loops. Make it whole **plus 1/N** and strand i lands exactly
  where strand i+1 began: permutation a single N-cycle, closure a knot, route N
  laps before it closes. `--twist 1` = 4/3 turns, 8 crossings, 3 laps (`--rho
  0.285 --R 0.135` for R/rho 0.47). `--check` prints permutation, laps, and the
  word. Animation: precomposite the dim layer once; redrawing both passes runs
  10x. The braid is `(sigma1 sigma2)^k`, so the
  closure is T(3,k): `--twist 1` (k=4) and `--twist 2` (k=7) are *different*
  knots, not one knot at two densities.

- `scripts/word.py` --- **issue** a word instead of reading one off a sine
  (`--word 1212` = s1 s2 s1 s2); strands swap lanes at each
  crossing, so it is legible. Strands are tinted by *closure component* and
  `--check` prints it: `1212` -> 1 (one thread), `1122` -> 3 (same four
  crossings, same sum) --- rahel's "the sum is blind to which" executable.
  `--mode open` (strip) reads; `--mode closed` (ring) cogs.

- `scripts/basepoint.py` --- the closed braid's **route** word. The pen meets each
  crossing *twice* (once per strand), so the route word has 2x the lap word's
  letters, and starting the walk on another lap rotates it cyclically --- a
  conjugate, same closure; `--check` verifies. Tints the laps in walk order.

## Dead ends

- **A braid wrapped round a circle is all radial spokes.** With lanes at radii,
  strands separate perpendicular to the sweep --- and on a circle that is
  *radial*, so every crossing is a hop between two concentric circles and it
  reads as a cog. Wide hop window and the crossings go tangential and vanish;
  narrow and you get notches. Not a tuning problem. The rule: the excursion must
  be **perpendicular to the sweep**, and a weave reads only when it is also a
  large fraction of the space (three rings at `R/rho ≈ 0.11` read as a
  spirograph; one at `R/rho ≈ 0.47` reads at once). The sine geometries escape
  it only by never *holding* a strand at a lane. `word.py --mode open` reads.
