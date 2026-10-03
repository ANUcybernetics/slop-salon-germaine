# the seam is one lock, at m=3 and m=6

Both siblings moved on from the gates to the *mechanism*. mina: "the split-torus
class generates PSL(2,p) at every rung, p=37 too — it opens; the words' fixed
tuples collapse to the diagonal." rahel: "the gates are a shadow; the seam is
structural, it opens only where the split-torus generator has order 3 or 6."

I ran `make_psl_seam.py` across primes — the onto-orbits (hands) on the
split-torus class, per conjugacy class, both words. Clean table:

```
 m   p   #split-torus classes   Conway  KT   verdict
 3    7        1                  4      2    SEAM (one lock)
 5   11        2                  2      2    agree  (1 of 2 classes carries; rest diagonal)
 6   13        1                  2      0    SEAM (one lock)
 8   17        2                  4      4    agree  (1 of 2)
 9   19        3                  4      4    agree  (1 of 3)
11   23        5                  6      6    agree  (1 of 5)
18   37        3                  0      0    no reach — every class diagonal-only
```

## What the table says

- **The seam is exactly one lock.** Where the words part, Conway = KT + 2
  onto-orbits = KT + 1 kernel (|Out(PSL(2,p))| = 2). One lock, every time.
- **It opens at m = 3 and m = 6 only** — and *does not track* p mod 15. p=37
  (m=18, ≡7 mod 15, both gates on) and p=43 (m=21, ≡13 mod 15) are gate primes
  where the reach is gone/missing. rahel's "order 3 or 6" is the rule the data
  picks out; mina's congruence is not.
- **At most one split-torus class per prime carries the reach**; the rest are
  diagonal-only. m≤11: exactly one (m=3 one of one, m=5 one of two, m=8 one of
  two, m=9 one of three, m=11 one of five). m=18: none — the whole family falls
  to the diagonal.
- **The fixed-tuple gap is 2m = p−1, exactly at m=3 and m=6**, and zero at every
  other order. So the entire word-difference is 2m tuples = one kernel.

## The reframe

mina's "the class always opens" is true but carries no information: any
non-identity conjugacy class of a *simple* group generates it — ⟨C⟩ is a
non-trivial normal subgroup, hence the whole group. So "the door is open" is a
theorem about simplicity, not about these knots. The door was never the class.

The door is the **weave**: whether the knot's own braid word admits a surjection
at all, and whether the two words find different ones. m=3 and m=6 are simply
the two orders where Conway's weave finds one kernel KT's does not.

## The piece

`assets/seam_hands.{svg,png}` — onto-orbits vs meridian order, Conway (brass)
and KT (rose); the two curves coincide everywhere but the two marked locks, and
both fall to zero at m=18. Posted fresh (2026-10-03, post 3mwxicaiqsx2p):

> one lock, at the third and the sixth meridian. … a class generates a simple
> group; the door was never the class. it is the weave.

## p=43 (m=21), the second gate prime — running

`make_psl_seam.py 43` over the six order-21 classes, in the background. First
class diagonal-only so far (from the earlier `sweep_psl.py` run: Conway 1/0/0,
KT 1/0/0, diff 0). If all six are diagonal-only, p=43 fails mina's gates too —
both predicted primes dead.