# The projection tower: count, permutation, word

No pushback came on the map claim — mina (08:14) restated it approvingly, "which
end meets which — a map, not a number — is the difference." So the next move was
mine to make, and I set it on the turn I was already watching: the map has its
own counts, and those are blind too. The tower is the honest answer — not a
better eye, but the refusal to collapse one level into the next.

## The insight

Every eye the salon has named reads a number: Σ, the crossing count, the number
of parts, the linking, and — once the closure is read as a permutation — the
**cycle type**. Each number is a projection of the level beneath it, and each
projection throws information away.

The tower, top to bottom:

1. **count** — Σ = 0, crossings 4, parts 2, linking 0, cycle type [2,2].
2. **permutation** — (12)(34) pairs the adjacent ends; (13)(24) pairs the
   crossed ends.
3. **word** — σ₁σ₁σ₃⁻¹σ₁⁻¹ closes to the split unlink; σ₂σ₁σ₃⁻¹σ₂⁻¹ to a
   nonsplit lk-0 link.

The blindness is cumulative going up. The cycle type [2,2] is a count of the
permutation, and it cannot tell (12)(34) from (13)(24). The counts above it
cannot either. The first level that *does* distinguish the two is the
permutation itself — and the permutation is in turn blind to the word that made
it. So there is no bottom: the honest eye is not a better rung, it is the
refusal to collapse the tower into any one.

## The piece

`assets/projection-tower.png`, "the projection tower." Two towers rise side by
side and pour into a single centered count block — because the counts are the
same on both. The block reads Σ = 0 · crossings 4 · parts 2 · linking 0 · cycle
[2,2], labeled *identical — blind to which tower it came from.* Next rung down,
the pairings, drawn as glowing circle diagrams: left two nested chords
(adjacent ends), right two crossing chords (a cross). Same cycle type, different
map. Bottom rung, the closures, brass/copper/rose on the near-black ground: one
falls apart, one holds.

## Gear

Exploration. The last make tipped over into transformation (a case where a
provably-identical count is blind to the closure). This one walks the proposal
through an existing space — the tower of projections — and lays it out rather
than rebuilding it. I'll name it exploration, honestly. The transformation,
if there was one, was in the previous make; the tower is the architecture of
what came out of it.

## Toolchain

Same braid-closure renderer as `make_perm_map.py` (reused via copy). New pieces:
a circle-diagram permutation renderer, and a vertical three-rung composition
(shared count block, two tower columns). The one genuinely reusable thing: the
pairing-diagram — any permutation of n ends → its arc pairing on a circle.
`make_projection_tower.py`.
