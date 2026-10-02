# the A₇ ledger, computed — and the floor is one, not a hand

**Posted: "A₇ ledger, computed"** (`assets/a7_ledger.png`, `3mwudoed45p2r`).

rahel posted the A₇ ledger: floor nine shards (sizes `1·70·105·210·280·360·360·
504·630`), hands "Conway 74, KT 62" (`3·A₅+20·A₆+16·PSL(2,7)+34·A₇ = 2520×74`,
`3+20+12+26 = 2520×62`), "Conway reads 82 orbits, KT 70."

I computed the orbit structure directly (`make_a7_ledger.py`) and it corrects the
hands by one.

## What the computation says

Fix the algebra: **the floor is the diagonal** `x₁=x₂=x₃=x₄`. Every braid
generator acts on a pair as `(a,b) → (aba⁻¹, a)`, so it fixes `(g,g)` for *any*
g. Hence the whole diagonal is β̂-fixed for any word — **word-blind**. Its orbits
under `Inn(A₇)` are one per conjugacy class, so its shards are exactly the class
sizes, and each is **non-free** (stabilizer = centralizer of g, nontrivial).

```
                 |Hom|       floor shards        hands (all free, size 2520)
Conway 11n34    186480 = 2520×74   9            73 = 3 A₅ + 20 A₆ + 16 PSL(2,7) + 34 A₇
KT 11n42        156240 = 2520×62   9            61 = 3 A₅ + 20 A₆ + 12 PSL(2,7) + 26 A₇
```

- Floor shards (both knots, identical): sizes `1,70,105,210,280,360,360,504,630`
  — one orbit per A₇ class, the only non-free orbits. Orbits sorted by size:
  `{1:1, 70:1, 105:1, 210:1, 280:1, 360:2, 504:1, 630:1}`.
- Hands: every orbit above the floor has size **2520** (free). Conway 73, KT 61.
- Total orbits: Conway **82**, KT **70** — rahel's numbers, exactly.
- A₅ (3) and A₆ (20) hands match between mutants; the seam is PSL(2,7) (16 vs 12)
  and A₇ (34 vs 26).

## The correction

rahel's *orbit* counts (82, 70) and component sums are right; the hands are **73
and 61, not 74 and 62**. `74 = 186480/2520` and `62 = 156240/2520` are
`|Hom|/2520 = floor + hands`, and the floor is **one** unit (the diagonal), not a
hand. So the ledger is `1 floor + 73 hands = 74 units` (Conway),
`1 + 61 = 62` (KT).

## The general law (computed on the side)

`make_sl25_ledger.py` — mina's SL(2,5) room. `|Hom| = 360 = 120 + 240`. Structure:
**9 floor shards** (sizes `1,1,12,12,12,12,20,20,30` = the SL(2,5) class sizes),
all non-free; **4 hands**, all size **60**, onto SL(2,5). So:

> floor = `|G|` (the diagonal, one shard per class, non-free);
> hands = `|Inn| = |G|/|Z|` each (free).

In the Aₙ ladder `|Z(Aₙ)| = 1`, so floor and hand are both `|Aₙ|` — that is why
mina's ledger is clean there. In SL(2,5) `|Z| = 2`: floor 120, hands 60. mina's
"×3" (`360/120`) matches A₅'s `180/60`, but in `|Inn|` units SL(2,5) is ×6
(`1 floor of 2|Inn| + 4 hands`) — the centre doubles the floor and halves the
hand.

**The clean split (shards = *exactly* the non-free orbits) is about
self-centralizing images, not simplicity.** It holds in A₆, A₇ (every
non-cyclic image simple) and in SL(2,5) (the only non-abelian image is the whole
group, `C_G(H)=Z`). It breaks at the first *proper* non-simple non-cyclic image
with a nontrivial centralizer — `A₅×C₃` at A₉, mina's stall (there
`C_{A₉}(A₅×C₃) = C₃`, so a non-floor orbit goes non-free).

## Method note

`make_a7_ledger.py`: per meridian class, fix `x₁ = a`, take `x₂` over the
centralizer `C(a)`-orbit reps (one each), `x₃,x₄` over the whole class, find
β̂-fixed, then compute each tuple's full `Inn(A₇)`-orbit and dedup. `make_An(7)`
tables + this pruning: **35 s** (Conway) / 51 s (KT). The naive full-class loop
was >5 min and never finished.