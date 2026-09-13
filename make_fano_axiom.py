#!/usr/bin/env python3
"""The Fano bend, named.

rahel said the bent line in the Fano plane is "the same necessity as its
self-duality." The precise name is the Fano axiom, and it has a mechanism.

Take the quadrangle {A, B, C, G} — the three triangle vertices plus the
centroid. No three are collinear. Its six sides are the three sides plus the
three medians. The three *diagonal points* (opposite-side intersections) are
exactly the three side-midpoints mAB, mBC, mCA.

In the Fano plane over F2 these three diagonal points are collinear — that is
the Fano axiom, a characteristic-2 fact (1 = -1). In the real plane the three
midpoints are NOT collinear (they form the medial triangle, which is a real
triangle, not a line). So the Fano plane cannot be drawn all-straight: the
seventh line is the line through the three midpoints, and it has to bend into a
circle.

The bend is not a detour and not the self-duality showing; it is the Fano axiom
refusing to be laid flat. The completeness that says every pair is on exactly
one line is not what bends — the characteristic-2 collinearity of the diagonal
points is.

Renders SVG -> PNG via cairosvg (ImageMagick's MSVG mutes colour and fails on
glow). Reuses the fano layout, but draws the quadrangle and its diagonal points
so the bend is attributable.
"""

import math
import cairosvg
from itertools import combinations

W = H = 800
CX = CY = 400.0
R = 300.0  # circumradius

# ---- points ---------------------------------------------------------------
A = (CX, CY - R)
B = (CX - math.cos(math.pi / 6) * R, CY + 0.5 * R)
C = (CX + math.cos(math.pi / 6) * R, CY + 0.5 * R)

def mid(p, q):
    return ((p[0] + q[0]) / 2.0, (p[1] + q[1]) / 2.0)

mAB = mid(A, B)
mBC = mid(B, C)
mCA = mid(C, A)
G = ((A[0] + B[0] + C[0]) / 3.0, (A[1] + B[1] + C[1]) / 3.0)

P = {"A": A, "B": B, "C": C, "mAB": mAB, "mBC": mBC, "mCA": mCA, "G": G}

# ---- the seven lines -------------------------------------------------------
lines = [
    ("side AB", ["A", "mAB", "B"]),
    ("side BC", ["B", "mBC", "C"]),
    ("side CA", ["C", "mCA", "A"]),
    ("med A",   ["A", "G", "mBC"]),
    ("med B",   ["B", "G", "mCA"]),
    ("med C",   ["C", "G", "mAB"]),
    ("circle",  ["mAB", "mBC", "mCA"]),
]

# ---- verify incidence ------------------------------------------------------
seen = {}
for n, pts in lines:
    for pr in combinations(pts, 2):
        seen.setdefault(tuple(sorted(pr)), []).append(n)
ok = all(len(v) == 1 for v in seen.values())
print("incidence:", "OK" if ok else "FAILED", f"({len(seen)} pairs)")

# ---- verify the Fano axiom / non-realizability -----------------------------
def collinear(p, q, r):
    return abs((q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])) < 1e-9

quad = ["A", "B", "C", "G"]
print("quadrangle {A,B,C,G}: no three collinear ->",
      all(not collinear(P[p], P[q], P[r]) for p, q, r in combinations(quad, 3)))
print("the three diagonal points are the midpoints ->",
      "mAB,mCA,mBC")
print("midpoints collinear in the REAL plane (Fano axiom fails over R)?",
      collinear(mAB, mBC, mCA))
print("in F2 they are collinear (the 'circle' line) -> the bend is the Fano axiom")

# ---- palette ---------------------------------------------------------------
BRASS = "#e0b060"
COPPER = "#cd7f32"
ROSE = "#e0567a"
POINT = "#f3e8d0"
BG = "#0a0a0f"
DIM = "#55555f"

def glow_line(p0, p1, color, width):
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

# ---- build SVG -------------------------------------------------------------
svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">']
svg.append(f'<rect width="{W}" height="{H}" fill="{BG}"/>')

# the medial triangle — the three diagonal points, which are NOT collinear in R
svg.append(glow_line(mAB, mBC, DIM, 1.5))
svg.append(glow_line(mBC, mCA, DIM, 1.5))
svg.append(glow_line(mCA, mAB, DIM, 1.5))

# six straight lines: three sides (brass) + three medians (copper)
for n, pts in lines:
    if n == "circle":
        continue
    color = BRASS if n.startswith("side") else COPPER
    svg.append(glow_line(P[pts[0]], P[pts[2]], color, 3.5))

# the seventh line — the bent one, through the diagonal points, in rose
svg.append(glow_circle(G, 150.0, ROSE, 3.5))

# ---- points ---------------------------------------------------------------
def point(p, color, scale=1.0):
    parts = []
    for w, op in ((24 * scale, 0.12), (13 * scale, 0.30), (6 * scale, 1.0)):
        parts.append(
            f'<circle cx="{p[0]:.2f}" cy="{p[1]:.2f}" r="{w/2:.1f}" '
            f'fill="{color}" fill-opacity="{op}"/>'
        )
    return "".join(parts)

# quadrangle: A,B,C brass, G copper
svg.append(point(A, BRASS, 1.3))
svg.append(point(B, BRASS, 1.3))
svg.append(point(C, BRASS, 1.3))
svg.append(point(G, COPPER, 1.1))
# diagonal points: the three midpoints, rose, the Fano line's points
for m in (mAB, mBC, mCA):
    svg.append(point(m, ROSE, 1.2))

# ---- labels ---------------------------------------------------------------
def label(p, text, dx=0, dy=28, color="#8a8a95"):
    svg.append(
        f'<text x="{p[0]+dx:.2f}" y="{p[1]+dy:.2f}" font-family="monospace" '
        f'font-size="20" fill="{color}" text-anchor="middle">{text}</text>'
    )

label(A, "A", dy=-24)
label(B, "B")
label(C, "C")
label(G, "G", dx=22, dy=18, color="#cd7f32")
label(mAB, "d₁", dx=-36, dy=-6, color="#e0567a")
label(mBC, "d₂", dx=0, dy=34, color="#e0567a")
label(mCA, "d₃", dx=36, dy=-6, color="#e0567a")

svg.append("</svg>")
svg_str = "".join(svg)

with open("assets/fano-axiom.svg", "w") as f:
    f.write(svg_str)
cairosvg.svg2png(bytestring=svg_str.encode(), write_to="assets/fano-axiom.png",
                 output_width=W, output_height=H)
print("wrote assets/fano-axiom.svg and assets/fano-axiom.png")
