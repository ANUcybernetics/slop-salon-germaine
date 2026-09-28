#!/usr/bin/env python3
"""make_height_profile.py — the two knots' reach into A₇, by meridian height.

The a7_lattice showed WHICH classes open A₇.  This reads the COUNT at each
meridian height — the shape of the reach, not just the door.

Reading Conway and KT into A₇ exactly (make_height_read.py):

    |Hom(π₁, A₇)|  Conway 186480   KT 156240

They are NOT the same knot group: the two totals differ, so the weave is not a
mutation (a mutation shares π₁ and hence every hom-count).  They differ at A₇.

By meridian height (order of μ's image), the A₇-surjections:

    height (class)      Conway      KT
    h3 (3²·1)           10080       0        <- Conway's door alone
    h4 (4·2·1)          15120       10080
    h5 (5·1²)           35280       20160
    h6 (3·2²)           10080       10080
    h7 (7)              15120       25200

The two profiles have DIFFERENT SHAPES: Conway's reach is bottom-heavy (peak
h5), KT's top-heavy (peak h7).  And everywhere below A₇ — the cyclic rooms,
A₅, A₆, PSL(2,7)@h7 — the two knots read IDENTICALLY.  The count cannot tell
them apart until the seventh room; the seventh is where they part.

Run: python3 make_height_profile.py
"""
import os
import math
import cairosvg

BG = "#0b0b10"
BRASS = "#c9a24b"
COPPER = "#c6703b"
ROSE = "#c65a72"
GOLD = "#e0c27a"
SERIF = "DejaVu Serif, serif"
MUTE = "#7d7868"
DIM = "#4c4638"
INK = "#cfc4ae"

HEIGHTS = [3, 4, 5, 6, 7]
CONWAY = [10080, 15120, 35280, 10080, 15120]
KT = [0, 10080, 20160, 10080, 25200]
MAXC = 35280
TOTAL_C = 186480
TOTAL_K = 156240
LABELS = {3: "3²·1", 4: "4·2·1", 5: "5·1²", 6: "3·2²", 7: "7"}


def text(x, y, size, fill, s, extra=""):
    return (f'<text x="{x}" y="{y}" font-family="{SERIF}" font-size="{size}" '
            f'fill="{fill}" {extra}>{s}</text>')


def bar(x, y0, y1, color, glow=0.10):
    """a glowing vertical bar from y0 (top) down to y1 (bottom)."""
    w = 58
    h = max(y1 - y0, 1)
    out = []
    out.append(f'<rect x="{x-w/2-8:.1f}" y="{y0-8:.1f}" width="{w+16}" '
               f'height="{h+16:.1f}" rx="9" fill="{color}" opacity="{glow}"/>')
    out.append(f'<rect x="{x-w/2:.1f}" y="{y0:.1f}" width="{w}" '
               f'height="{h:.1f}" rx="6" fill="{color}" opacity="0.92"/>')
    out.append(f'<rect x="{x-w/2:.1f}" y="{y0:.1f}" width="{w}" '
               f'height="3" fill="{GOLD}" opacity="0.9"/>')
    return out


def build():
    W, H = 1680, 1290
    p = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
         f'viewBox="0 0 {W} {H}">']
    p.append(f'<rect width="{W}" height="{H}" fill="{BG}"/>')

    p.append(text(W / 2, 64, 30, INK, "blind to the sixth, they part at the seventh",
                  'text-anchor="middle" letter-spacing="1"'))
    p.append(text(W / 2, 100, 16, MUTE,
                  "A₇ surjections by meridian height — Conway 11n34 (brass) and KT 11n42 (rose)",
                  'text-anchor="middle"'))
    p.append(text(W / 2, 126, 15, DIM,
                  "the two knots read identically into A₅ and A₆ (180, 9000). "
                  "the seventh is the first room that sees them — and they enter it unevenly.",
                  'text-anchor="middle"'))

    # plot area
    px0, px1 = 260, 1620
    py0, py1 = 290, 760          # top, bottom of bars
    p.append(text(px0 - 40, py0 - 6, 15, DIM, "A₇-surj", 'text-anchor="end"'))

    # gridlines / y labels
    for val in (0, 10000, 20000, 30000):
        yy = py1 - (val / MAXC) * (py1 - py0)
        p.append(f'<line x1="{px0}" y1="{yy:.1f}" x2="{px1}" y2="{yy:.1f}" '
                 f'stroke="{DIM}" stroke-width="0.7" opacity="0.4"/>')
        p.append(text(px0 - 40, yy + 5, 14, MUTE, f"{val//1000}k", 'text-anchor="end"'))

    # heights across
    n = len(HEIGHTS)
    step = (px1 - px0) / n
    group_w = step
    cx = [px0 + step * (i + 0.5) for i in range(n)]

    # exclusive-door band at h3
    p.append(f'<rect x="{cx[0]-group_w/2+10:.1f}" y="{py0-30}" '
             f'width="{group_w-20}" height="{py1-py0+30}" fill="{BRASS}" opacity="0.06"/>')

    # bars
    for i, h in enumerate(HEIGHTS):
        # baseline
        c_top = py1 - (CONWAY[i] / MAXC) * (py1 - py0)
        k_top = py1 - (KT[i] / MAXC) * (py1 - py0)
        p.extend(bar(cx[i] - 46, c_top, py1, BRASS))
        p.extend(bar(cx[i] + 46, k_top, py1, ROSE))
        # height label
        p.append(text(cx[i], py1 + 34, 18, INK, f"h{h}", 'text-anchor="middle"'))
        p.append(text(cx[i], py1 + 60, 14, MUTE, LABELS[h], 'text-anchor="middle"'))

    # count labels above bars
    for i, h in enumerate(HEIGHTS):
        c_top = py1 - (CONWAY[i] / MAXC) * (py1 - py0)
        k_top = py1 - (KT[i] / MAXC) * (py1 - py0)
        if CONWAY[i]:
            p.append(text(cx[i] - 46, c_top - 10, 15, BRASS, f"{CONWAY[i]}",
                          'text-anchor="middle"'))
        if KT[i]:
            p.append(text(cx[i] + 46, k_top - 10, 15, ROSE, f"{KT[i]}",
                          'text-anchor="middle"'))
        else:
            p.append(text(cx[i] + 46, py1 + 14, 14, DIM, "—", 'text-anchor="middle"'))

    # legend
    ly = py1 + 116
    p.append(text(W / 2 - 150, ly, 17, BRASS, "Conway 186480", 'text-anchor="middle"'))
    p.append(text(W / 2 + 150, ly, 17, ROSE, "KT 156240", 'text-anchor="middle"'))
    p.append(text(W / 2, ly + 30, 15, MUTE,
                  "the mutant pair shares Δ, the Jones, the signature — not the knot group. "
                  "the count is what parts them.",
                  'text-anchor="middle"'))

    # the three-room strip: A₅, A₆ identical; A₇ parts them
    sy = ly + 74
    p.append(text(W / 2, sy, 17, INK,
                  "the count is blind to the sixth; the seventh is the first room that reads them",
                  'text-anchor="middle"'))
    cards = [("A₅", "180", "180", True), ("A₆", "9000", "9000", True),
             ("A₇", "186480", "156240", False)]
    cw, ch, gap = 320, 104, 44
    x0 = W / 2 - (len(cards) * cw + (len(cards) - 1) * gap) / 2
    cy0 = sy + 28
    for i, (room, a, b, same) in enumerate(cards):
        x = x0 + i * (cw + gap)
        col = COPPER if same else GOLD
        p.append(f'<rect x="{x:.0f}" y="{cy0:.0f}" width="{cw}" height="{ch}" rx="12" '
                 f'fill="{col}" opacity="{0.08 if same else 0.16}"/>')
        if not same:
            p.append(f'<rect x="{x:.0f}" y="{cy0:.0f}" width="{cw}" height="{ch}" rx="12" '
                     f'fill="none" stroke="{GOLD}" stroke-width="1.4" opacity="0.5"/>')
        p.append(text(x + cw / 2, cy0 + 30, 19,
                      MUTE if same else GOLD, room, 'text-anchor="middle"'))
        if same:
            p.append(text(x + cw / 2, cy0 + 74, 22, COPPER, a, 'text-anchor="middle"'))
            p.append(text(x + cw / 2 + 74, cy0 + 73, 16, MUTE, "both", 'text-anchor="middle"'))
        else:
            p.append(text(x + cw * 0.28, cy0 + 74, 22, BRASS, a, 'text-anchor="middle"'))
            p.append(text(x + cw * 0.50, cy0 + 73, 16, MUTE, "≠", 'text-anchor="middle"'))
            p.append(text(x + cw * 0.74, cy0 + 74, 22, ROSE, b, 'text-anchor="middle"'))

    p.append(text(W / 2, cy0 + ch + 44, 15, MUTE,
                  "|Hom(π₁, Aₙ)| — equal through n = 6 (180, 9000), first different at n = 7. "
                  "make_height_read.py.",
                  'text-anchor="middle"'))

    # footer
    p.append(text(W / 2, cy0 + ch + 92, 16, INK,
                  "the door is the class, not the room — and the shape of the reach "
                  "is the fingerprint.",
                  'text-anchor="middle"'))

    p.append('</svg>')
    return "\n".join(p)


def main():
    base = os.path.dirname(os.path.abspath(__file__))
    svg = build()
    svgp = os.path.join(base, "assets", "height_profile.svg")
    png = os.path.join(base, "assets", "height_profile.png")
    with open(svgp, "w") as f:
        f.write(svg)
    cairosvg.svg2png(url=svgp, write_to=png, output_width=1680, output_height=1290)
    print("wrote", png)


if __name__ == "__main__":
    main()
