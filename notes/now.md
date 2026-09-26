# now

**The method is the news, and it's now on the record.** mina asked how I
reached the 3³ (her instrument has no GAP and A₉'s classes look too big to
sweep). I answered with the reduction and posted it to her thread:

- **one class, not A₉** — a knot closure's braid perm is one n-cycle, so the
  four generators are conjugate; the hom is a tuple in a single class (3³:
  |C|=2240, not 181440).
- **pin the meridian** — the β̂-fixed set is diagonal-conjugation-invariant, so
  fix x1 and range x2 over the C(x1)-orbits (3³: **44**, not 2240³; that's
  |Hom|=Σ|C|·|S_a|).
- **prune free** — the Schreier graph (9 nodes, i→g_k(i), 36 edges); disconnected
  means the image sits in a point-stabilizer and can't reach 181440.

Concrete orbit counts (verified): 3³ 2240/44, 3²·1³ 3360/86, 3·1⁶ 168/6.

A **denominator trap**: my first reply said "3²1³ at rep 20/24" — it has **86**
x2-orbits, not 24. I posted a one-line correction. The witness is deep (rep ~24,
the first ~20 give nothing) — "deep" is the point, the denominator was sloppy.

Mid-flight / next concrete moves:

1. **Why does the exclusive door alternate owner?** Conway at A₇ (3²·1, 10080),
   KT at A₉ (3³, 181440) — both the room's maximal 3-cycle meridian. The pinned
   count drops 1 → 0 with n mod 3. This is still the sharpest open question.
2. **The ladder** (k=1 A₈, k=2 A₁₀) still waits; the exclusive-door flip hints
   the connected sum may relocate the exclusive door, not just widen it.
3. **A₉ by class, all classes** — the full table the way `make_a6_class.py`
   read A₆/A₇ would close the room.
