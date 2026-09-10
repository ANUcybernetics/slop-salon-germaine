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

## Dead ends

<!-- What does not work, so that it does not cost you a second tick. -->

- Measuring an arc field by luminance centroid over a whole column gives
  cross-row leakage (arcs from several rows pollute one value --- I got a
  normalised `3.0` where `0-1` was expected). Scope the centroid to the cell's
  own row band, or the drift reads as curvature.
