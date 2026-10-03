#!/usr/bin/env python3
"""sweep_psl.py — full class-by-class beta-hat-fixed sweep onto PSL(2,p).

For EVERY conjugacy class of PSL(2,p), count beta-hat-fixed tuples (x1=rep,
x2,x3,x4 in the class) for each word, split into onto-hands vs floor, and compare
Conway vs KT.  Prints a per-class table and flags any class where the two words
differ.  Also reports total |Hom| per word.

The order-3 class is the bottleneck at p=37 (many C(x1)-orbits, large |C|); the C
kernel in fastkernel handles it but the sweep is minutes/word.
"""
import sys
import time
import numpy as np
from psl import PSL
from make_psl_seam import WORDS, class_seam


def main():
    p = int(sys.argv[1]) if len(sys.argv) > 1 else 13
    only_order = int(sys.argv[2]) if len(sys.argv) > 2 else None  # optional filter
    t0 = time.time()
    G = PSL(p)
    print(f"|PSL(2,{p})| = {G.n}  (built {time.time()-t0:.1f}s)")
    classes = G.classes()
    print(f"  #classes = {len(classes)}")

    rows = []
    total_hom = {"conway": 0, "kt": 0}
    seam_classes = []
    for rep, C in classes.items():
        if only_order is not None and G.order(rep) != only_order:
            continue
        o = G.order(rep)
        m = len(C)
        res = {}
        for name, word in WORDS.items():
            nf, no, noo = class_seam(G, rep, C, word, p)
            res[name] = (nf, no, noo)
            total_hom[name] += m * nf
        d = res["conway"][2] - res["kt"][2]
        flag = "  <-- SEAM" if d else ""
        if d:
            seam_classes.append((rep, o, res["conway"], res["kt"]))
        rows.append((o, m, res["conway"], res["kt"], d, flag))
        print(f"  order {o:2d} |C|={m:5d}: "
              f"C {res['conway'][0]:7d}/{res['conway'][1]:6d}/{res['conway'][2]:4d} "
              f"K {res['kt'][0]:7d}/{res['kt'][1]:6d}/{res['kt'][2]:4d} diff {d:4d}{flag}")

    print(f"\n  total |Hom|: Conway {total_hom['conway']}  KT {total_hom['kt']}  "
          f"(|G|={G.n}, /|G| = {total_hom['conway']/G.n:.4f} vs {total_hom['kt']/G.n:.4f})")
    print(f"  seams: {len(seam_classes)} class(es)")
    for rep, o, c, k in seam_classes:
        print(f"    order {o}: Conway onto-orbits {c[2]} vs KT {k[2]}")


if __name__ == "__main__":
    main()
