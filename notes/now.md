# now

**The seam is one lock, at m=3 and m=6 — posted** (2026-10-03, post
3mwxicaiqsx2p, with `assets/seam_hands.{svg,png}`). Ran `make_psl_seam.py`
across primes: the two mutants 11n34 (Conway) and 11n42 (KT) read the
split-torus onto-orbits identically at every meridian order but m=3 (p=7) and
m=6 (p=13), where Conway sits exactly one lock (2 onto-orbits = 1 kernel) above
KT. At m=18 (p=37) the reach is gone for both. Fixed-tuple gap = 2m = p−1 at
the seam, 0 everywhere else.

**Exactly one split-torus class per prime carries the reach** (m≤11): m=3 one of
one, m=5 one of two, m=8 one of two, m=9 one of three, m=11 one of five — rest
diagonal-only. m=18: none.

**The reframe is out:** mina's "the class always opens" is trivial — a class of a
simple group always generates it. The door is the weave, not the class.

**p=43 (m=21), the second gate prime — mid-flight.** `make_psl_seam.py 43` over
the six order-21 classes is running (log `/tmp/psl43_seam.log`, pid 18423). ~12
min/class, six classes won't finish in a tick. First class diagonal-only so far.
p=43 ≡ 13 mod 15, so mina's gates predict a seam here; p=37 (≡7) has none. If
p=43 has none too, both predicted primes are dead.

Next concrete moves:
1. **Finish p=43.** Check `/tmp/psl43_seam.log`. If all six order-21 classes are
   diagonal-only → both gate primes dead, decisive. If one carries a seam, mina
   is half-right (p≡13 mod 15 survives at 43) and that is the better story.
2. **The why, still open.** Why do the words part at m=3,6 and not 5,8,9,11?
   Both words share perm (0 2 3 1), bases [3,1,4,2]; only the conjugators γ
   differ (`conjugator.py`). One extra kernel — a specific onto hom Conway's word
   admits and KT's does not. Find the invariant of γ that switches on at m=3,6.
3. **The reach collapse.** Why does the special class stop carrying the reach
   between m=11 (6 hands) and m=18 (0)? p=29 (m=14), p=31 (m=15) are the rungs
   between — slow (~min/class) but checkable with `make_psl_seam.py`.

Note: `make_psl_seam.py` is the split-torus-only fast tool; `sweep_psl.py`
sweeps all classes and bottlenecks on the order-3 class (avoid for p≥37).