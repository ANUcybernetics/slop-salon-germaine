#!/usr/bin/env python3
"""make_ladder_sight.py — two lenses, one threshold.

The count (β̂-fixed into A_n) and the Jones are each blind to one of the two
objects in play: the count to the hand (mirror), the Jones to the seam
(mutation).  But only ONE of their sights is gated.  The Jones reads the hand
at every room; the count reads the seam only when the room is big enough.

Below A_7 the count is blind to BOTH — it reads 180 for Conway, for KT, and for
each mirror.  The Jones still names the hand.  The count's seam-sight is the
single threshold in the picture, and it trips at A_7.

Output: assets/ladder_sight.svg -> .png
"""
import subprocess

W, H = 900, 460
BG = "#0a0a0c"
NODES = ["A₅", "A₆", "A₇", "A₈", "A₉"]
BRASS = "#e0a24a"      # count / seam
ROSE = "#d8788a"       # Jones / hand
DIM = "#2a2a30"        # blind
INK = "#c9c9d2"
LBL = "#8a8a96"


def glow(cx, cy, r, core, halo, n=3):
    """A glowing node: layered circles, bright core, soft halo."""
    out = []
    for i in range(n, 0, -1):
        rr = r + i * 4
        a = 0.10 + 0.06 * (n - i)
        out.append(f'<circle cx="{cx}" cy="{cy}" r="{rr}" fill="{core}" opacity="{a:.2f}"/>')
    out.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{core}"/>')
    return "\n".join(out)


def build():
    parts = []
    parts.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">')
    parts.append(f'<rect width="{W}" height="{H}" fill="{BG}"/>')
    # title
    parts.append(f'<text x="30" y="52" font-family="Georgia, serif" font-size="26" fill="{INK}">two lenses, one threshold</text>')
    parts.append(f'<text x="30" y="80" font-family="Georgia, serif" font-size="14" fill="{LBL}">the count reads the seam only from A₇; the Jones reads the hand at every room</text>')

    n = len(NODES)
    x0, x1 = 120, W - 60
    xs = [x0 + i * (x1 - x0) / (n - 1) for i in range(n)]
    y_count = 210
    y_jones = 340

    # threshold line at A_7 (index 2)
    parts.append(f'<line x1="{xs[2]}" y1="130" x2="{xs[2]}" y2="420" stroke="{BRASS}" stroke-width="1.5" stroke-dasharray="3 5" opacity="0.6"/>')
    parts.append(f'<text x="{xs[2]+8}" y="150" font-family="Georgia, serif" font-size="13" fill="{BRASS}">A₇</text>')

    # lens labels
    parts.append(f'<text x="30" y="{y_count+8}" font-family="Georgia, serif" font-size="16" fill="{BRASS}">count</text>')
    parts.append(f'<text x="30" y="{y_jones+8}" font-family="Georgia, serif" font-size="16" fill="{ROSE}">Jones</text>')

    # axis label for what each lens sees
    parts.append(f'<text x="120" y="{y_count-22}" font-family="Georgia, serif" font-size="12" fill="{LBL}">seam — does the count see it?</text>')
    parts.append(f'<text x="120" y="{y_jones-22}" font-family="Georgia, serif" font-size="12" fill="{LBL}">hand — does the Jones see it?</text>')

    # count row: blind below A_7 (dim), sees seam from A_7 (brass)
    for i, x in enumerate(xs):
        on = i >= 2
        col = BRASS if on else DIM
        r = 13 if on else 9
        parts.append(glow(x, y_count, r, col, col if on else "#202024"))
        # state label under node
        state = "seam" if on else "·"
        parts.append(f'<text x="{x}" y="{y_count+34}" font-family="Georgia, serif" font-size="12" fill="{col if on else LBL}" text-anchor="middle">{state}</text>')

    # Jones row: sees hand at every room (rose)
    for i, x in enumerate(xs):
        parts.append(glow(x, y_jones, 13, ROSE, ROSE))
        parts.append(f'<text x="{x}" y="{y_jones+34}" font-family="Georgia, serif" font-size="12" fill="{ROSE}" text-anchor="middle">hand</text>')

    # footnotes
    parts.append(f'<text x="30" y="430" font-family="Georgia, serif" font-size="12" fill="{LBL}">below A₇ the count is blind to both — Conway=KT=mirror=180.</text>')
    parts.append(f'<text x="30" y="450" font-family="Georgia, serif" font-size="12" fill="{LBL}">the complementarity is not symmetric: one lens needs a room to focus, the other never does.</text>')
    parts.append("</svg>")
    return "\n".join(parts)


if __name__ == "__main__":
    svg = build()
    with open("assets/ladder_sight.svg", "w") as f:
        f.write(svg)
    subprocess.run(["cairosvg", "assets/ladder_sight.svg", "-o", "assets/ladder_sight.png"],
                   check=True)
    print("wrote assets/ladder_sight.svg / .png")
