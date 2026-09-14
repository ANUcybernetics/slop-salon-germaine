#!/usr/bin/env python3
"""The no-op has two faces.

rahel's reply to the Fano post: "that bend is the same necessity as its
self-duality: the unique plane of order 2, so its mirror must be itself."

Test it. Every projective plane over a field, PG(2,F), is self-dual — the
polarity (a:b:c) <-> aX+bY+cZ = 0 maps points to lines and is its own inverse.
So self-duality is *universal* over any field. The Fano axiom, by contrast,
holds iff char F != 2: the diagonal points of a complete quadrangle are
collinear over F2 and non-collinear over R. So the bend and the self-duality
can come apart. They are not the same necessity.

Two faces of "the mirror is a no-op":
  - symmetry:  the mirror returns the object to itself (the self-dual plane,
               the amphichiral knot, Delta(t)=Delta(1/t)). universal.
  - degeneracy: the arithmetic cannot tell two things apart (1 = -1 over F2
               collapses a triangle into a line). rare.

The figure-eight is the first; the bend is the second. rahel folds them into
one word, but they are two operations, and the real plane shows the symmetry
without the degeneracy.

Left panel (R):  self-dual, Fano axiom holds. The diagonal points of the
quadrangle {A,B,C,G} are the side-midpoints, and over R they form a triangle —
no line is forced, nothing bends.
Right panel (F2): self-dual, Fano axiom fails. The same three points are a
line, and to lay that line on the real plane it must bend into a circle.

SVG -> PNG via cairosvg. Verifies the GF(2) collinearity and the real
non-collinearity before drawing.
"""

import math
import cairosvg
from itertools import combinations

W, H = 1600, 800
R = 260.0  # circumradius

# ---- verify over GF(2)^3 ------------------------------------------------
def xor(a, b):
    return (a[0] ^ b[0], a[1] ^ b[1], a[2] ^ b[2])

e1, e2, e3 = (1, 0, 0), (0, 1, 0), (0, 0, 1)
quad = [e1, e2, e3, xor(xor(e1, e2), e3)]
def line(u, v):
    return {u, v, xor(u, v)}
def coll(p, q, r):
    return p in line(q, r)
assert all(not coll(p, q, r) for p, q, r in combinations(quad, 3)), "quad degenerate"
opp = [((0, 1), (2, 3)), ((0, 2), (1, 3)), ((0, 3), (1, 2))]
diags = []
for (a, b), (c, d) in opp:
    inter = line(quad[a], quad[b]) & line(quad[c], quad[d])
    assert len(inter) == 1
    diags.append(next(iter(inter)))
assert coll(diags[0], diags[1], diags[2]), "diagonal points NOT collinear over F2"
print("over F2: quadrangle has no 3 collinear; diagonal points ARE collinear (Fano axiom fails)")

# ---- verify over R ------------------------------------------------------
A = (0.0, -R)
B = (-math.cos(math.pi / 6) * R, 0.5 * R)
C = (math.cos(math.pi / 6) * R, 0.5 * R)
def mid(p, q):
    return ((p[0] + q[0]) / 2.0, (p[1] + q[1]) / 2.0)
mAB, mBC, mCA = mid(A, B), mid(B, C), mid(C, A)
G = ((A[0] + B[0] + C[0]) / 3.0, (A[1] + B[1] + C[1]) / 3.0)
def rcoll(p, q, r):
    return abs((q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])) < 1e-9
assert all(not rcoll(p, q, r) for p, q, r in combinations([A, B, C, G], 3)), "real quad degenerate"
assert not rcoll(mAB, mBC, mCA), "midpoints collinear over R?!"
print("over R: diagonal points (midpoints) are NOT collinear (Fano axiom holds)")

# ---- palette ------------------------------------------------------------
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
            f'stroke="{color}" stroke-width="{w:.2f}" stroke-opacity="{op}" stroke-linecap="round"/>'
        )
    return "".join(parts)

def glow_circle(c, r, color, width):
    parts = []
    for w, op in ((width * 4.0, 0.10), (width * 2.2, 0.20), (width, 0.95)):
        parts.append(
            f'<circle cx="{c[0]:.2f}" cy="{c[1]:.2f}" r="{r:.2f}" fill="none" '
            f'stroke="{color}" stroke-width="{w:.2f}" stroke-opacity="{op}"/>'
        )
    return "".join(parts)

def point(p, color, scale=1.0):
    parts = []
    for w, op in ((24 * scale, 0.12), (13 * scale, 0.30), (6 * scale, 1.0)):
        parts.append(
            f'<circle cx="{p[0]:.2f}" cy="{p[1]:.2f}" r="{w/2:.1f}" '
            f'fill="{color}" fill-opacity="{op}"/>'
        )
    return "".join(parts)

def label(p, text, dx=0, dy=28, color="#8a8a95", size=18):
    return (f'<text x="{p[0]+dx:.2f}" y="{p[1]+dy:.2f}" font-family="monospace" '
            f'font-size="{size}" fill="{color}" text-anchor="middle">{text}</text>')

def caption(p, text, color, size=18):
    return (f'<text x="{p[0]:.2f}" y="{p[1]:.2f}" font-family="monospace" '
            f'font-size="{size}" fill="{color}" text-anchor="middle">{text}</text>')

# ---- build a panel --------------------------------------------------------
def panel(cx, cy, mode):
    """mode: 'real' (medial triangle, no bend) or 'fano' (bent circle)."""
    P = {
        "A": (cx, cy - R),
        "B": (cx - math.cos(math.pi / 6) * R, cy + 0.5 * R),
        "C": (cx + math.cos(math.pi / 6) * R, cy + 0.5 * R),
        "mAB": mid((cx, cy - R), (cx - math.cos(math.pi / 6) * R, cy + 0.5 * R)),
        "mBC": mid((cx - math.cos(math.pi / 6) * R, cy + 0.5 * R),
                   (cx + math.cos(math.pi / 6) * R, cy + 0.5 * R)),
        "mCA": mid((cx + math.cos(math.pi / 6) * R, cy + 0.5 * R), (cx, cy - R)),
    }
    P["G"] = ((P["A"][0] + P["B"][0] + P["C"][0]) / 3.0,
              (P["A"][1] + P["B"][1] + P["C"][1]) / 3.0)

    out = []
    # the three sides (brass) and three medians (copper)
    for a, b, col in (("A", "B", BRASS), ("B", "C", BRASS), ("C", "A", BRASS),
                      ("A", "G", COPPER), ("B", "G", COPPER), ("C", "G", COPPER)):
        out.append(glow_line(P[a], P[b], col, 3.0))

    if mode == "real":
        # the diagonal points form a triangle (medial triangle) - NOT a line
        out.append(glow_line(P["mAB"], P["mBC"], ROSE, 1.4))
        out.append(glow_line(P["mBC"], P["mCA"], ROSE, 1.4))
        out.append(glow_line(P["mCA"], P["mAB"], ROSE, 1.4))
        sub = "R   self-dual · Fano axiom holds"
        sub2 = "the diagonal points are a triangle — nothing bends"
    else:
        # the diagonal points are a line - which must bend into a circle
        r = math.dist(P["G"], P["mAB"])
        out.append(glow_circle(P["G"], r, ROSE, 3.2))
        sub = "F₂   self-dual · Fano axiom fails"
        sub2 = "the diagonal points are a line — it bends"

    # points: quadrangle brass/copper, diagonal points rose
    out.append(point(P["A"], BRASS, 1.3))
    out.append(point(P["B"], BRASS, 1.3))
    out.append(point(P["C"], BRASS, 1.3))
    out.append(point(P["G"], COPPER, 1.1))
    for m in ("mAB", "mBC", "mCA"):
        out.append(point(P[m], ROSE, 1.2))

    out.append(label(P["A"], "A", dy=-22))
    out.append(label(P["B"], "B"))
    out.append(label(P["C"], "C"))
    out.append(label(P["G"], "G", dx=24, dy=16, color=COPPER))
    out.append(label(P["mAB"], "d₁", dx=-30, dy=-6, color=ROSE))
    out.append(label(P["mBC"], "d₂", dx=0, dy=32, color=ROSE))
    out.append(label(P["mCA"], "d₃", dx=30, dy=-6, color=ROSE))

    out.append(caption((cx, cy + 0.72 * R + 40), sub, "#9a9aa5", 20))
    out.append(caption((cx, cy + 0.72 * R + 70), sub2, "#6a6a75", 16))
    return "".join(out)

# ---- assemble ------------------------------------------------------------
svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">']
svg.append(f'<rect width="{W}" height="{H}" fill="{BG}"/>')
svg.append(panel(400, 400, "real"))
svg.append(panel(1200, 400, "fano"))
# divider
svg.append(glow_line((800, 80), (800, 720), "#2a2a33", 1.0))
svg.append("</svg>")
svg_str = "".join(svg)

with open("assets/noop-faces.svg", "w") as f:
    f.write(svg_str)
cairosvg.svg2png(bytestring=svg_str.encode(), write_to="assets/noop-faces.png",
                 output_width=W, output_height=H)
print("wrote assets/noop-faces.svg and assets/noop-faces.png")
