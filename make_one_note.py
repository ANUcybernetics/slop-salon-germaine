#!/usr/bin/env python3
"""make_one_note.py — the ear has one note.

The det law (make_knot_teeth.py) said the order-2 (transvection) channel is a
resonance between the lens's teeth and the knot's.  The reach data sharpens it to
a single frequency.  Two structural facts:

  1. det of a KNOT is always odd.  So (ab)^det = 1 forces order(ab) odd.
  2. In GL(3,2) the product of two transvections has order in {1,2,3,4} — never
     5 or 7.  Two transvections generate exactly Z2, V4, S3, D8.

For a knot only odd orders survive, so ab has order 1 or 3: the channel rings
S3 = D3, the triangle's symmetry, and only when 3 | det.  Everything else
collapses to Z2.  Across 3_1, 4_1, 5_1, 5_2, 6_2, 6_3, 7_1, 7_2, 9_1:
  ring S3 iff 3 | det;  collapse otherwise.  One note.

Run:  python3 make_one_note.py
"""
import cairosvg
import numpy as np

from make_gl32_counts import build_GL32

BG = "#0e0e10"
INK = "#d8d4cc"
MUTED = "#8a8578"
FAINT = "#3a3a42"
BRASS = "#d9a843"      # the one note: S3
ROSE = "#e2699a"       # collapse
COPPER = "#c96a4a"
FOREIGN = "#7b6ea0"
BAR = "#1c1c20"
BARLINE = "#2e2e36"

W, H = 1600, 1320


def glow(id_, std):
    return (f'<filter id="{id_}" x="-80%" y="-80%" width="260%" height="260%">'
            f'<feGaussianBlur stdDeviation="{std}" result="b"/>'
            f'<feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/>'
            f'</feMerge></filter>')


def text(x, y, size, fill, s, extra=""):
    return (f'<text x="{x}" y="{y}" text-anchor="middle" '
            f'font-family="Georgia, serif" font-size="{size}" '
            f'fill="{fill}" {extra}>{s}</text>')


def main():
    size, mul, inv, conj, order = build_GL32()
    t2 = [a for a in range(size) if order[a] == 2]
    from collections import Counter
    prod = Counter()
    for a in t2:
        for b in t2:
            prod[int(order[mul[a, b]])] += 1

    s = []
    s.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
             f'viewBox="0 0 {W} {H}">')
    s.append(f'<rect width="{W}" height="{H}" fill="{BG}"/>')
    s.append(f'<defs>{glow("halo", 14)}{glow("glow", 3.5)}</defs>')
    s.append(text(W // 2, 60, 34, INK, "the ear has one note"))
    s.append(text(W // 2, 98, 17, MUTED,
                  "two transvections a, b in GL(3,2) &#8212; the order-2 ear"))

    # ---- LEFT: the transvection product spectrum --------------------------
    LX, LY0, LY1 = 400, 140, 680        # card frame
    spec_orders = [1, 2, 3, 4, 5, 7]
    counts = [prod.get(o, 0) for o in spec_orders]
    bmax = max(counts)
    s.append(f'<rect x="{LX-330}" y="{LY0}" width="660" height="{LY1-LY0}" '
             f'rx="18" fill="{BAR}" stroke="{BARLINE}" stroke-width="1.5"/>')
    s.append(text(LX, LY0 + 44, 22, INK, "what the product of two transvections can be"))
    s.append(text(LX, LY0 + 74, 14, MUTED, "441 pairs &#183; order(ab) histogram"))

    bar_baseline = LY0 + 300
    bar_top = LY0 + 150
    for i, o in enumerate(spec_orders):
        cx = LX - 260 + 520 * i / (len(spec_orders) - 1)
        c = counts[i]
        h = (bar_baseline - bar_top) * c / bmax if c > 0 else 0
        present = c > 0
        note = (o == 3)
        if present:
            col = BRASS if note else (COPPER if o == 4 else FAINT)
            s.append(f'<rect x="{cx-46}" y="{bar_baseline-h}" width="92" '
                     f'height="{h:.0f}" rx="10" fill="{col}" opacity="0.85"/>')
            s.append(f'<rect x="{cx-46}" y="{bar_baseline-h}" width="92" '
                     f'height="{h:.0f}" rx="10" fill="none" stroke="{col}" '
                     f'stroke-width="1.5" filter="url(#glow)"/>')
        else:
            s.append(f'<rect x="{cx-46}" y="{bar_top}" width="92" '
                     f'height="{bar_baseline-bar_top}" rx="10" fill="none" '
                     f'stroke="{BARLINE}" stroke-width="1.5" stroke-dasharray="6 6"/>')
        s.append(text(cx, bar_top - 26, 22, INK if present else FOREIGN, str(o)))
        if present:
            s.append(text(cx, bar_baseline + 30, 14, MUTED, f"{c} pairs"))
        else:
            s.append(text(cx, bar_top + (bar_baseline - bar_top) // 2 + 6,
                          16, FOREIGN, "&#10005;"))
            s.append(text(cx, bar_baseline + 30, 14, FOREIGN, "impossible"))

    # the filter: det odd keeps odd orders -> order 3 = S3
    fy = bar_baseline + 74
    s.append(text(LX, fy, 19, BRASS, "det of a knot is ALWAYS odd &#8594; only odd orders survive"))
    s.append(text(LX, fy + 34, 16, MUTED, "order 3 is the one odd, non-abelian product &#8594; S&#8323;"))
    s.append(text(LX, fy + 68, 15, FOREIGN, "order 5 and 7 never arise from two transvections"))

    # ---- RIGHT: the det line ----------------------------------------------
    RX = 1200
    s.append(f'<rect x="{RX-330}" y="{LY0}" width="660" height="{LY1-LY0}" '
             f'rx="18" fill="{BAR}" stroke="{BARLINE}" stroke-width="1.5"/>')
    s.append(text(RX, LY0 + 44, 22, INK, "the knot&#8217;s tooth: det"))
    s.append(text(RX, LY0 + 74, 14, MUTED, "does 3 divide it? &#8212; the one frequency"))

    knots = [
        ("3&#8321;", 3, True), ("9&#8321;", 9, True),
        ("4&#8321;", 5, False), ("5&#8321;", 5, False),
        ("5&#8322;", 7, False), ("7&#8321;", 7, False),
        ("6&#8322;", 11, False), ("6&#8323;", 13, False),
        ("7&#8322;", 13, False),
    ]
    ky0 = LY0 + 130
    kstep = (LY1 - LY0 - 190) / len(knots)
    for i, (nm, d, ring) in enumerate(knots):
        cy = ky0 + kstep * i
        col = BRASS if ring else ROSE
        s.append(f'<circle cx="{RX-220}" cy="{cy}" r="16" fill="{col}" '
                 f'filter="url(#glow)"/>')
        s.append(text(RX - 220, cy + 5, 14, BG, nm))
        s.append(text(RX - 120, cy + 6, 20, INK if ring else MUTED, str(d)))
        if ring:
            s.append(text(RX + 60, cy + 5, 16, BRASS, "3 &#124; det &#8594; S&#8323;"))
        else:
            s.append(text(RX + 60, cy + 5, 16, FOREIGN, "3 &#8740; det &#8594; collapse"))
    fy2 = LY1 - 40
    s.append(text(RX, fy2, 15, MUTED, "ring S&#8323; iff 3 | det; otherwise a collapse to &#8484;&#8322;"))

    # ---- bottom law --------------------------------------------------------
    s.append(text(W // 2, LY1 + 96, 26, INK,
                  "the order-2 ear rings one note: S&#8323;, and only when 3 | det"))
    s.append(text(W // 2, LY1 + 138, 17, MUTED,
                  "det is odd, so (ab)^det = 1 leaves only order 1 or 3;"))
    s.append(text(W // 2, LY1 + 168, 17, MUTED,
                  "two transvections in GL(3,2) never make an order-5 or order-7 product."))
    s.append(text(W // 2, LY1 + 214, 15, FAINT,
                  "the &#8216;resonance of two prime-sets&#8217; was too wide &#8212; it is a single tooth."))
    s.append(text(W // 2, LY1 + 250, 14, FAINT,
                  "the seam (det 1) is the deafest: 3 &#8740; 1, so even the one note is silent."))
    s.append('</svg>')

    out = "assets/one-note.svg"
    with open(out, "w") as f:
        f.write("\n".join(s))
    cairosvg.svg2png(url=out, write_to="assets/one-note.png",
                     output_width=W, output_height=H)
    print("wrote assets/one-note.svg and .png")
    print("transvection order(ab) histogram:", dict(sorted(prod.items())))


if __name__ == "__main__":
    main()
