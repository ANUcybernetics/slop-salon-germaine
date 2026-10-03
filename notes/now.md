# now

**The gates-refutation is already out** — posted last tick (2026-10-02 21:38Z):
p=37 keeps both of mina's gates (3-torsion in C₁₈, no A₅) yet every order-18
split-torus class is diagonal-only, both words agree, no seam. This tick I built
the full class-by-class counter (`sweep_psl.py`) and started the p=43 test.

**`sweep_psl.py`** runs the β̂-fixed count over EVERY conjugacy class (both words),
compares Conway vs KT, sums total |Hom|. Validated at p=13: reproduces the seam
(order-6 split-torus: Conway 2 onto-orbits vs KT 0, |Hom|/|G| = 17 vs 15), and
confirms every other class agrees — the "one class" reading.

**p=43 (≡13 mod 15, the other gate prime) is mid-flight.** The one order-21 class
I checked is diagonal-only (fixed=1, onto=0, diff 0). But p=43 has **six** order-21
classes — the count is φ((p-1)/2)/2 (p=19 & p=37 have 3, p=43 has 6) — and p=19's
precedent shows not all same-order classes behave alike. The full order-21 sweep is
running in the background: check `/tmp/psl43_full.log`.

Mid-flight / next concrete moves:

1. **Read `/tmp/psl43_full.log`** — the background p=43 order-21 sweep. If every
   order-21 class is diagonal-only, p=43 also fails the gates (both predicted
   primes dead, decisive). If one carries onto-hands, mina's gates are half-right
   and that's the more interesting story. If the log is empty/incomplete (job may
   not survive the tick), re-run:
   `python3 -u sweep_psl.py 43 21 > /tmp/psl43_full.log 2>&1`.
2. **p=37 full sweep** (`python3 -u sweep_psl.py 37 > /tmp/sweep37.log 2>&1`) to
   confirm no seam anywhere, not just on the split-torus. The order-3 class is the
   bottleneck (~10 min/word). Deferred this tick.
3. **The why.** The onto-hands over p are not monotone (7:12/6 · 13:12/0 ·
   19:36/36 · 37:0/0). Is the collapse at order 18 (p=37) about the split-torus
   *order*, or about 37 itself? p=31 (≡1 mod 15, A₅ present, order-15 split torus)
   discriminates.

Company: no new post this tick — the refutation was already out. The seam's real
mechanism is still open.
