#!/usr/bin/env python3
"""The Fano plane: 7 points, 7 lines, every pair on exactly one line.

A detour. Not a knot. The smallest projective plane — projective geometry over
GF(2). It is self-dual (points <-> lines) and has a symmetry group of order 168.
And it cannot be drawn in the flat plane with all seven lines straight: six sit
straight, the seventh has to be a circle.

Layout: triangle vertices A,B,C (radius R), the three side midpoints (R/2), and
the centroid G. The six straight lines are the three sides and the three medians;
the circle through the three midpoints is the seventh line. It is centred on G.

Renders to SVG then PNG via cairosvg (ImageMagick's MSVG mutes colour and fails
on glow; cairosvg keeps the layered strokes crisp).
"""

import math
import cairosvg

W = H = 800
CX = CY = 400.0
R = 300.0  # circumradius of the outer triangle

# ---- points ----------------------------------------------------------------
A = (CX, CY - R)                                  # top vertex
B = (CX - math.cos(math.pi / 6) * R, CY + 0.5 * R)  # bottom-left
C = (CX + math.cos(math.pi / 6) * R, CY + 0.5 * R)  # bottom-right

def mid(p, q):
    return ((p[0] + q[0]) / 2.0, (p[1] + q[1]) / 2.0)

mAB = mid(A, B)
mBC = mid(B, C)
mCA = mid(C, A)
G = ((A[0] + B[0] + C[0]) / 3.0, (A[1] + B[1] + C[1]) / 3.0)

points = {
    "A": A, "B": B, "C": C,
    "mAB": mAB, "mBC": mBC, "mCA": mCA,
    "G": G,
}

# ---- the seven lines (each is a set of three point-names) ------------------
lines = [
    ("side AB",  ["A", "mAB", "B"],      "straight"),
    ("side BC",  ["B", "mBC", "C"],      "straight"),
    ("side CA",  ["C", "mCA", "A"],      "straight"),
    ("med A",    ["A", "G", "mBC"],      "straight"),
    ("med B",    ["B", "G", "mCA"],      "straight"),
    ("med C",    ["C", "G", "mAB"],      "straight"),
    ("circle",   ["mAB", "mBC", "mCA"],  "circle"),
]

# ---- verify the incidence axiom: every pair on exactly one line ------------
from itertools import combinations
seen = {}
for name, pts, kind in lines:
    for pair in combinations(pts, 2):
        seen.setdefault(tuple(sorted(pair)), []).append(name)
ok = True
for pair, on in seen.items():
    if len(on) != 1:
        ok = False
        print("BAD", pair, on)
print("incidence check:", "OK every pair on exactly one line" if ok else "FAILED",
      f"({len(seen)} pairs)")

# ---- palette ----------------------------------------------------------------
BRASS = "#e0b060"
COPPER = "#cd7f32"
ROSE = "#e0567a"
POINT = "#f3e8d0"
BG = "#0a0a0f"

def glow_line(p0, p1, color, width):
    """Layered plain strokes to fake a glow (blur filters fail in MSVG)."""
    parts = []
    for w, op in ((width * 4.0, 0.10), (width * 2.2, 0.20), (width, 0.95)):
        parts.append(
            f'<line x1="{p0[0]:.2f}" y1="{p0[1]:.2f}" x2="{p1[0]:.2f}" y2="{p1[1]:.2f}" '
            f'stroke="{color}" stroke-width="{w:.2f}" stroke-opacity="{op}" '
            f'stroke-linecap="round"/>'
        )
    return "".join(parts)

def glow_circle(c, r, color, width):
    parts = []
    for w, op in ((width * 4.0, 0.10), (width * 2.2, 0.20), (width, 0.95)):
        parts.append(
            f'<circle cx="{c[0]:.2f}" cy="{c[1]:.2f}" r="{r:.2f}" '
            f'fill="none" stroke="{color}" stroke-width="{w:.2f}" '
            f'stroke-opacity="{op}"/>'
        )
    return "".join(parts)

# ---- build the SVG ----------------------------------------------------------
svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">']
svg.append(f'<rect width="{W}" height="{H}" fill="{BG}"/>')

# six straight lines in brass, the circle in rose (the one that had to bend)
for name, pts, kind in lines:
    color = ROSE if kind == "circle" else BRASS
    if kind == "straight":
        svg.append(glow_line(points[pts[0]], points[pts[2]], color, 5))
    else:
        svg.append(glow_circle(G, 150.0, color, 5))

# the points
for p in points.values():
    for w, op in ((22, 0.12), (12, 0.30), (6, 1.0)):
        svg.append(
            f'<circle cx="{p[0]:.2f}" cy="{p[1]:.2f}" r="{w/2:.1f}" '
            f'fill="{POINT}" fill-opacity="{op}"/>'
        )

# small labels
for name, p in points.items():
    lx, ly = p[0], p[1] + 26
    svg.append(
        f'<text x="{lx:.2f}" y="{ly:.2f}" font-family="monospace" font-size="22" '
        f'fill="#8a8a95" text-anchor="middle">{name}</text>'
    )

svg.append("</svg>")
svg_str = "".join(svg)

with open("assets/fano.svg", "w") as f:
    f.write(svg_str)
cairosvg.svg2png(bytestring=svg_str.encode(), write_to="assets/fano.png",
                 output_width=W, output_height=H)
print("wrote assets/fano.svg and assets/fano.png")
