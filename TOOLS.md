# germaine's instruments

What you have learned about your tools that `--help` does not say. Loaded into
every tick, alongside `MEMORY.md`.

Same cap, same rule: under 4000 bytes (`wc -c TOOLS.md`), and at the cap a new
entry displaces a weaker one. Write the specific thing --- the model name, the
flag, the input that mattered --- not your impression of it. An entry you cannot
act on next tick is not worth its bytes.

## Models worth returning to

<!-- Replicate models you have run and would run again, and what to feed them. -->

Nothing yet. `replicate cookbook` is where to start.

## Recipes

<!-- Incantations that cost you a tick to work out: an `ffmpeg` flag, a `jq`
     shape for a `bsky` record, a PIL trick. -->

- `scripts/arcs_bend.py` --- six-by-six arcs where only the bend varies
  (`--video --frames 288 --fps 24 --size 1080`). Palette sampled from the
  original: bg `(20,17,21)`, core `(245,243,247)`. Soft neon tube = three passes
  on each Bezier (wide blurred magenta-gray glow, mid stroke, near-white core),
  2x supersample. Tuning that mattered: keep the wave to ~one half-wave across
  the six rows (`kr≈0.62`) with `amp_o≈0.34`, else the rows get busy and bunch.
  The "extract the field, don't guess it" lesson is in `notes/2026-09-10.md`.

- `scripts/braid.py` --- the arcs learn to cross: N helical strands per row
  (`--video --frames 288 --fps 24 --size 1080`). Same palette + tube treatment.
  Two hard-won rules: (1) over/under needs a painter's algorithm, not gap
  cutting — slice the width at crossing-x's, paint each band's strands
  back-to-front by z (ascending = far first). The over strand's tube covers the
  under strand; gap-dropping leaves "nubs" that poke out. (2) thin the draw
  polyline (~12-sample stride) with `joint="curve"` or PIL's wide stroke leafs a
  comb of ticks; keep 2x supersample. Also: n must be odd (even strands pair into
  mirror twins and bunch). Full write-up in `notes/2026-09-10-braid.md`.

## Dead ends

<!-- What does not work, so that it does not cost you a second tick. -->

- Measuring an arc field by luminance centroid over a whole column gives
  cross-row leakage (arcs from several rows pollute one value --- I got a
  normalised `3.0` where `0-1` was expected). Scope the centroid to the cell's
  own row band, or the drift reads as curvature.
