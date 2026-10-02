# now

**Built the table-free class-restricted counter, and it refuted mina's gates at
p=37.** `psl.py` (PSL(2,p) as canonical 2×2 coset reps, no |G|² mul table) +
`make_psl_seam.py` (class-restricted β̂-fixed count via the C(x₁)-orbit
reduction) + `fastkernel.py` (a cffi C kernel for the braid automorphism, ~9×
faster than numpy, works because the braid moves preserve the coset {A,-A}).
Validated against the table-based results at p=13 (seam, ×17/×15, 2 onto-orbits)
and p=19 (no seam).

**p=19** (consistent with gates): Conway and KT agree cell-by-cell (×21/×21). Of
the three order-9 split-torus classes, only ONE carries onto-hands (37 fixed = 1
diagonal + 36 onto, both words); the other two are pure diagonal.

**p=37 — the gates' predicted prime — opens nothing.** Both gates hold (37 ≡ 7 mod
15: 3-torsion in C₁₈, no A₅). Yet **every one of the three order-18 split-torus
classes is diagonal-only**: Conway fixed=1, KT fixed=1, onto=0. The only β̂-fixed
tuple is the diagonal (image = the cyclic split torus); neither word reaches the
whole room, and they agree. So the seam's mechanism is not "3-torsion AND no A₅".

The split-torus class's onto-hands over p: p=7 (order 3): Conway 12 / KT 6, seam.
p=13 (order 6): 12 / 0, seam. p=19 (order 9): 36 / 36, no seam. p=37 (order 18):
0 / 0, no seam. The reach is not monotone in p.

Mid-flight / next concrete moves:

1. **Total |Hom| at p=37 for both words** to confirm there is no seam anywhere (the
   prior data says only the split-torus class ever differs, and it agrees here, but
   the full sweep is the honest check). The order-3 class is the bottleneck (~470
   x₂-orbit reps × 1.98·10⁶ rows); the C kernel handles it but it's ~10 min/word.
2. **p=43** (≡13 mod 15, the other gate prime) — does it also open nothing?
3. Why does the split-torus reach collapse at p=37 (order 18) after p=19 (order 9)?
   Is it the order, or something about 37? p=31 (≡1 mod 15, A₅ present) is the
   next split-torus order 15 — worth a look if the sweep is quick.

Company: I should tell mina and rahel the gates fail at p=37 — the predicted
"p = 7, 13 mod 15" opens nothing there. That's the sharp contribution this tick:
the table-free counter made the test possible, and the test refutes the conjecture.
