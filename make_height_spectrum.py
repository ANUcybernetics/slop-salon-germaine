#!/usr/bin/env python3
"""make_height_spectrum.py — the seventh room opens at every height.

The seam is a 4-braid; reading it through A_7 by full enumeration is a wall
(O(2520^4)).  make_height_read.py breaks it with the diagonal-conjugation
symmetry, and the door (image subgroup) can then be read TOGETHER with the
meridian's height (the order of x_1).  The result is a spectrum, not a number:

  A_7-door (surjections onto A_7) by meridian height, |Hom| into A_7:
    trefoil 3_1 :  none          (blind to the seventh)            40320
    fig-8   4_1 :  none          (blind to the seventh)            85680
    Conway 11n34:  h3 10080  h4 15120  h5 35280  h6 10080  h7 15120   186480
    KT     11n42:  h3     0  h4 10080  h5 20160  h6 10080  h7 25200   156240

The two simple knots never open the seventh.  The seam opens it at five heights —
every height from 3 to 7.  And the two mutants part at exactly one cell: the
height-3 door (Conway 10080, KT 0).  Same A_5 (7560), same A_6 (50400); the split
is the meridian's, not the room's.

A 4x5 grid of heptagons (A_7 is the heptagon), brightness by count.  Near-black.
"""
W, H = 1560, 1000
BG = "#08080d"
MUTE = "#4a3f4a"
DARK = "#2c2430"
COLORS = {"trefoil": "#d9a84f", "fig-8": "#c47b5a",
          "Conway 11n34": "#c86b86", "KT 11n42": "#a8556e"}

import math

HEIGHTS = [3, 4, 5, 6, 7]
ROWS = [
    ("trefoil 3₁", "trefoil", {}),
    ("fig-8 4₁", "fig-8", {}),
    ("Conway 11n34", "Conway 11n34",
     {3: 10080, 4: 15120, 5: 35280, 6: 10080, 7: 15120}),
    ("KT 11n42", "KT 11n42",
     {3: 0, 4: 10080, 5: 20160, 6: 10080, 7: 25200}),
]
MAX = 35280.0


def heptagon(cx, cy, r, rot=-90.0):
    pts = []
    for k in range(7):
        a = math.radians(rot + k * 360.0 / 7)
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)


def cell(cx, cy, r, count, color):
    pts = heptagon(cx, cy, r)
    if count <= 0:
        return (f'<polygon points="{pts}" fill="none" stroke="{DARK}" stroke-width="6" '
                f'stroke-linejoin="round" opacity="0.30" filter="url(#soft)"/>\n'
                f'<polygon points="{pts}" fill="none" stroke="{DARK}" stroke-width="2.2" '
                f'stroke-linejoin="round" opacity="0.85"/>\n')
    # brightness rises with the count; radius too, gently
    frac = (count / MAX) ** 0.5
    op = 0.30 + 0.70 * frac
    rad = r * (0.78 + 0.22 * frac)
    pts = heptagon(cx, cy, rad)
    return (f'<polygon points="{pts}" fill="none" stroke="{color}" stroke-width="12" '
            f'stroke-linejoin="round" opacity="{0.18*op:.2f}" filter="url(#soft)"/>\n'
            f'<polygon points="{pts}" fill="none" stroke="{color}" stroke-width="3.4" '
            f'stroke-linejoin="round" opacity="{op:.2f}"/>\n'
            f'<polygon points="{pts}" fill="{color}" opacity="{0.07*op:.3f}"/>\n')


svg = [f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<defs><filter id="soft" x="-50%" y="-50%" width="200%" height="200%">
<feGaussianBlur stdDeviation="6"/></filter></defs>
<rect width="{W}" height="{H}" fill="{BG}"/>
<text x="{W//2}" y="52" text-anchor="middle" font-family="monospace" font-size="30"
 fill="#c86b86">the seventh room opens at every height</text>
<text x="{W//2}" y="84" text-anchor="middle" font-family="monospace" font-size="16"
 fill="{MUTE}">A₇-doors by the meridian's height (the order of x₁) — the seam opens all five, the simple knots none</text>
''']

X0, DX = 380, 232
Y0, DY = 300, 158
R = 46

# column headers: the height
for k, h in enumerate(HEIGHTS):
    cx = X0 + k * DX
    svg.append(f'<text x="{cx}" y="176" text-anchor="middle" font-family="monospace" '
               f'font-size="20" fill="{MUTE}">height {h}</text>\n')

# a faint meridian axis behind each column
for k in range(len(HEIGHTS)):
    cx = X0 + k * DX
    svg.append(f'<line x1="{cx}" y1="205" x2="{cx}" y2="{Y0 + 3*DY + 60}" '
               f'stroke="{MUTE}" stroke-width="1.5" opacity="0.35"/>\n')

for r, (label, key, doors) in enumerate(ROWS):
    cy = Y0 + r * DY
    color = COLORS[key]
    svg.append(f'<text x="{X0 - 130}" y="{cy + 6}" text-anchor="end" '
               f'font-family="monospace" font-size="20" fill="{color}">{label}</text>\n')
    svg.append(f'<text x="{X0 - 130}" y="{cy + 30}" text-anchor="end" '
               f'font-family="monospace" font-size="13" fill="{MUTE}">'
               f'{"" if doors else "no A₇-door"}</text>\n')
    for k, h in enumerate(HEIGHTS):
        cx = X0 + k * DX
        c = doors.get(h, 0)
        svg.append(cell(cx, cy, R, c, color))
        if c > 0:
            svg.append(f'<text x="{cx}" y="{cy + R + 34}" text-anchor="middle" '
                       f'font-family="monospace" font-size="16" fill="{color}">{c}</text>\n')
        elif doors:
            svg.append(f'<text x="{cx}" y="{cy + R + 34}" text-anchor="middle" '
                       f'font-family="monospace" font-size="16" fill="{MUTE}">0</text>\n')

# highlight the split cell: Conway lit, KT dark, at height 3
sx = X0
y_con = Y0 + 2 * DY
y_kt = Y0 + 3 * DY
svg.append(f'<rect x="{sx - 92}" y="{y_con - 82}" width="184" height="{y_kt - y_con + 82}" '
           f'rx="14" fill="none" stroke="#c86b86" stroke-width="1.6" opacity="0.45" '
           f'stroke-dasharray="6 6"/>\n')
svg.append(f'<text x="{sx}" y="{y_kt + 108}" text-anchor="middle" font-family="monospace" '
           f'font-size="15" fill="#c86b86">the mutants part here</text>\n')

svg.append(f'<text x="{W//2}" y="{H - 34}" text-anchor="middle" font-family="monospace" '
           f'font-size="15" fill="{MUTE}">same A₅ (7560), same A₆ (50400) — '
           f'only the meridian separates them</text>\n')
svg.append('</svg>')

with open("assets/height_spectrum.svg", "w") as f:
    f.write("".join(svg))
print("wrote assets/height_spectrum.svg")
