#!/usr/bin/env python3
"""make_a6_room.py — the sixth room holds the fifth.

A6 (order 360) is the first room that holds a room: it contains twelve copies of
A5.  Read the seam and the two simple knots through it, and they split:

  trefoil 3_1 : 3960 = 11 x 360   reaches A5 (1440 = 12 x 120), blind to A6
  fig-8  4_1 : 6120 = 17 x 360   reaches A6 (2880 = 8 x 360), blind to A5
  seam (Δ=1)  : 9000 = 25 x 360   reaches A5 (1440) AND A6 (7200)

A triptych: the hexagon is A6, the pentagon the A5 it holds.  A lit shape is a
room the knot reaches; a dark one is a room it is blind to.
"""
import math

W, H = 1500, 940
CX, CY = 250, 430
R = 122          # hexagon circumradius (A6)
r = 72           # pentagon circumradius (A5), inscribed inside the hexagon

BRASS = "#d9a84f"
COPPER = "#c47b5a"
ROSE = "#c86b86"
DARK = "#2c2430"
MUTE = "#4a3f4a"
BG = "#08080d"

def poly(cx, cy, rad, n, rot=-90.0):
    pts = []
    for k in range(n):
        a = math.radians(rot + k * 360.0 / n)
        pts.append((cx + rad * math.cos(a), cy + rad * math.sin(a)))
    return " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)

def glow_poly(points, color, on=True, width=4):
    """Emit a glowing polygon: a soft blurred halo plus a bright core.
    If on is False, emit a faint dark outline instead."""
    if on:
        return (
            f'<polygon points="{points}" fill="none" stroke="{color}" stroke-width="{width*3}" '
            f'stroke-linejoin="round" opacity="0.18" filter="url(#soft)"/>\n'
            f'<polygon points="{points}" fill="none" stroke="{color}" stroke-width="{width}" '
            f'stroke-linejoin="round"/>\n'
            f'<polygon points="{points}" fill="{color}" opacity="0.06"/>\n'
        )
    else:
        return (
            f'<polygon points="{points}" fill="none" stroke="{DARK}" stroke-width="{width*3}" '
            f'stroke-linejoin="round" opacity="0.30" filter="url(#soft)"/>\n'
            f'<polygon points="{points}" fill="none" stroke="{DARK}" stroke-width="{width}" '
            f'stroke-linejoin="round" opacity="0.8"/>\n'
        )

def panel(x, title, color, hex_on, pent_on, caption, line):
    hx = poly(x, CY, R, 6)
    px = poly(x, CY, r, 5)
    s = f'<text x="{x}" y="140" text-anchor="middle" font-family="monospace" font-size="24" fill="{color}">{title}</text>\n'
    s += f'<text x="{x}" y="168" text-anchor="middle" font-family="monospace" font-size="15" fill="{MUTE}">{line}</text>\n'
    # room shapes: hexagon A6, pentagon A5 inside
    s += glow_poly(hx, color, hex_on, 4)
    s += glow_poly(px, color, pent_on, 4)
    # labels
    s += f'<text x="{x}" y="{CY + R + 26}" text-anchor="middle" font-family="monospace" font-size="16" fill="{color if hex_on else MUTE}">A₆</text>\n'
    s += f'<text x="{x}" y="{CY - r - 12}" text-anchor="middle" font-family="monospace" font-size="16" fill="{color if pent_on else MUTE}">A₅</text>\n'
    s += f'<text x="{x}" y="820" text-anchor="middle" font-family="monospace" font-size="16" fill="{color}">{caption}</text>\n'
    return s

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<defs>
  <filter id="soft" x="-40%" y="-40%" width="180%" height="180%">
    <feGaussianBlur stdDeviation="5"/>
  </filter>
</defs>
<rect width="{W}" height="{H}" fill="{BG}"/>
<text x="750" y="52" text-anchor="middle" font-family="monospace" font-size="30" fill="{ROSE}">the sixth room holds the fifth</text>
<text x="750" y="88" text-anchor="middle" font-family="monospace" font-size="17" fill="{MUTE}">A₆ is the first room that holds a room — twelve copies of A₅. the knots split.</text>
'''
for x in (500, 1000):
    svg += (f'<line x1="{x}" y1="150" x2="{x}" y2="800" stroke="{MUTE}" stroke-width="1.5" '
            f'opacity="0.6"/>\n')

svg += panel(250, "trefoil 3_1", BRASS, False, True,
             "reaches A₅ · blind to A₆", "11× = 3960   A₅ 4×, not A₆")
svg += panel(750, "fig-8 4_1", COPPER, True, False,
             "reaches A₆ · blind to A₅", "17× = 6120   A₆ 8×, not A₅")
svg += panel(1250, "seam Δ=1", ROSE, True, True,
             "reaches A₅ and A₆", "25× = 9000   A₅ 4×, A₆ 20×")
svg += '</svg>'

with open("assets/a6_room.svg", "w") as f:
    f.write(svg)
print("wrote assets/a6_room.svg")
