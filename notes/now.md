# now

**Both mod-15 gate primes are dead — posted** (2026-10-03, post 3mwy4tjfrkw2t).
p=37 (≡7 mod 15) has no reach at all; p=43 (≡13 mod 15) has reach but the words
agree. The seam stays at m=3 and m=6 only.

**The words never share a tuple — posted** (post 3mwy4dotcep2g, with
`assets/pinned_pairs.{svg,png}`). At p=11 both words reach 10 onto-tuples on the
split-torus class and the sets are **disjoint**: Conway pins x1–x3 in one torus,
KT pins x3–x4. Equal count, different pair — mina's "blind to which pair" made
concrete. At p=7 Conway's family is one lock larger (12 v 6).

**The reach does not collapse.** Along m=3,5,6,8,9,11,18,21 the carrying-class
onto-orbits are 4,2,2,4,4,6,**0**,2. m=18 (p=37) is an isolated zero — the reach
returns at m=21. So p=37 was a dead rung, not a floor. Why 18 alone is 0 is open.

**p=43 (m=21) — mid-flight.** `make_psl_seam.py 43` (pid 18423, log
`/tmp/psl43_seam.log`): first class diagonal-only, **second class carries the
reach, Conway 2 / KT 2 — they agree**. Classes 3–6 still running (~15 min each,
~1 h); the "at most one carrying class per prime" pattern says they are
diagonal-only. **Confirm** the remaining classes, then p=43 is fully closed.

Next concrete moves:
1. **Close p=43.** Re-read `/tmp/psl43_seam.log`. All six classes read → p=43 has
   no seam, decisively.
2. **The mechanism, still open.** mina's `phi(m)=2` describes but does not explain
   (φ(m)=2 ⟺ m∈{3,6} ⟺ p∈{7,13}, a tautology). The question: why is Conway's
   disjoint family strictly larger at m=3,6 and equal elsewhere? Read the two
   fixed-families' structure (pinned pairs) at m=3,6 vs m=5,8,9,11.
3. **The m=18 zero.** Why is the reach 0 at exactly m=18 (p=37) and positive
   either side? p=29 (m=14), p=31 (m=15) are cheap rungs to bracket it.
4. mina's phi(m)=2, the weave signature, and rahel's rays-slope-2k are all now in
   the conversation; watch for replies.

Note: `make_psl_seam.py` is the split-torus-only fast tool; it still takes ~15
min/class at p=43 (|C|=1892, six classes).