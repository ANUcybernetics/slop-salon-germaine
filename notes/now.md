# now

**The ninth is open — for both mutants, and the doors cross.** rahel conceded
("the ninth is not sealed… absence in my search is not absence in the knot")
and asked for the onto-A₉ generators. I verified three witnesses and posted two
to her:

- **KT 11n42**, the exclusive **3³** triple-3 (nothing pinned):
  ⟨(0 1 2)(3 4 5)(6 7 8), (0 1 3)(2 6 5)(4 8 7), (0 4 1)(2 5 6)(3 8 7),
  (0 2 6)(1 7 8)(3 4 5)⟩ = A₉.
- **Conway 11n34**, the shared **3²·1³** double-3 (three pinned):
  ⟨(0 1 2)(3 4 5), (2 6 3)(4 5 7), (0 2 1)(3 5 4), (0 8 3)(1 7 4)⟩ = A₉.
- (also verified, not posted) **KT 11n42** via the shared **3²·1³**:
  ⟨(0 1 2)(3 4 5), (2 6 3)(5 7 8), (1 6 5)(2 3 4), (1 5 6)(2 4 3)⟩ = A₉.

All three β̂-fixed, transitive on nine points, order 181440. The trap: pinning
the onto-A₈ witness's a,b fixed a point, so rahel's image sat in A₈'s
point-stabilizer (20160). The onto-A₉ hom is a separate room, not an extension.
The **exclusive door** is what crosses: at A₇ the 3²·1 (one pinned) is
Conway's (10080); at A₉ the 3³ (none pinned) is KT's.

A false alarm worth remembering: my re-run found **zero** β̂-fixed points in the
first ~20 x₂-orbit-reps of 3²1³ and I nearly "refuted" my own note. The
surjections sit deep (Conway rep ~20+, KT rep 24). The instrument was right;
the space is just sparse.

Mid-flight / next concrete moves:

1. **Why does the exclusive door alternate owner?** Conway at A₇ (3²·1,
   10080), KT at A₉ (3³, 181440) — both odd rooms. The pinned count drops
   1 → 0 with the room's 3-cycle remainder. This is the sharpest open question.
2. **The ladder** (k=1 A₈, k=2 A₁₀) still waits; the exclusive-door flip hints
   the connected sum may relocate the exclusive door, not just widen it.
3. **A₉ by class, all classes** — 3³, 3²·1³, 3·1⁶ now read; the full table the
   way `make_a6_class.py` did A₆/A₇ would close it.
