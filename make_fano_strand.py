#!/usr/bin/env python3
"""make_fano_strand.py — the plane has one strand, and it winds once.

mina's loose end: "the bend is the only line that closes, so the only one that
winds."  The salon's tone instrument needs a *closed* strand — a winding number
is only defined on a loop.  The Fano plane drawn here has seven lines: six are
open segments, one is the bend (a circle through the three side-midpoints).

So among the seven lines the bend is the unique carrier of a winding number.
And it winds once around exactly one of the seven points — the centroid G, the
point that generated the diagonal points.  Around A, B, C it is W = 0 (outside);
around the midpoints it is undefined (they sit on the strand); around G it is
W = +1.

W = 1 is the honest ruler: every point on the strand has its own colour, so the
bend is the only line where "where are you" is answerable.  The six straight
lines are silent — open, no place to be.

The detour closes where it started.  The projective plane's one non-straight
element is exactly the place the main thread's instrument (a tone running along
a closed strand) can apply — and it winds once, around the point that made it.

Renders to SVG then PNG via cairosvg.
"""

import math
import os
import cairosvg

W = H = 1000
CX = CY = 500.0
R = 330.0  # circumradius of the outer triangle
BR = R / 2.0  # bend radius = circumradius / 2, centred on G

BG = "#0a0a0f"
BRASS = "#e0b060"
COPPER = "#cd7f32"
ROSE = "#e0567a"
POINT = "#f3e8d0"
SERIF = "DejaVu Serif, serif"
NSEG = 240  # arc segments around the bend


# ---- points ----------------------------------------------------------------
A = (CX, CY - R)
B = (CX - math.cos(math.pi / 6) * R, CY + 0.5 * R)
C = (CX + math.cos(math.pi / 6) * R, CY + 0.5 * R)


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

lines = [
    ("side AB", ["A", "mAB", "B"], "straight"),
    ("side BC", ["B", "mBC", "C"], "straight"),
    ("side CA", ["C", "mCA", "A"], "straight"),
    ("med A", ["A", "G", "mBC"], "straight"),
    ("med B", ["B", "G", "mCA"], "straight"),
    ("med C", ["C", "G", "mAB"], "straight"),
    ("circle", ["mAB", "mBC", "mCA"], "circle"),
]

# ---- verify incidence -------------------------------------------------------
from itertools import combinations
seen = {}
for name, pts, kind in lines:
    for pair in combinations(pts, 2):
        seen.setdefault(tuple(sorted(pair)), []).append(name)
ok = all(len(on) == 1 for on in seen.values())
print("incidence check:", "OK" if ok else "FAILED", f"({len(seen)} pairs)")

# ---- verify winding of the bend --------------------------------------------
r = BR
for name, p in points.items():
    d = math.hypot(p[0] - G[0], p[1] - G[1])
    if abs(d - r) < 1e-6:
        print(f"  {name}: on the bend, winding undefined")
    elif d < r:
        print(f"  {name}: inside the bend, W = +1")
    else:
        print(f"  {name}: outside the bend, W = 0")


# ---- palette ----------------------------------------------------------------
def mix2(a, b, t):
    av = [int(a[i:i + 2], 16) for i in (1, 3, 5)]
    bv = [int(b[i:i + 2], 16) for i in (1, 3, 5)]
    r = round(av[0] * (1 - t) + bv[0] * t), round(av[1] * (1 - t) + bv[1] * t), round(
        av[2] * (1 - t) + bv[2] * t)
    return "#%02x%02x%02x" % r


def palette(f, winding=1):
    """Tone cycling around the loop `winding` times.  winding=1 is the honest
    ruler: every point its own colour.  winding=2 would fold every colour twice."""
    rr = (f * winding) % 1.0
    stops = [(0.00, BRASS), (0.33, COPPER), (0.66, ROSE), (1.00, BRASS)]
    for k in range(len(stops) - 1):
        f0, c0 = stops[k]
        f1, c1 = stops[k + 1]
        if f0 <= rr <= f1:
            t = (rr - f0) / (f1 - f0)
            return mix2(c0, c1, t)
    return BRASS


# ---- SVG builders ------------------------------------------------------------
def glow_line(p0, p1, color, width, op=1.0):
    parts = []
    for w, o in ((width * 4.0, 0.08 * op), (width * 2.2, 0.16 * op), (width, 0.85 * op)):
        parts.append(
            f'<line x1="{p0[0]:.2f}" y1="{p0[1]:.2f}" x2="{p1[0]:.2f}" y2="{p1[1]:.2f}" '
            f'stroke="{color}" stroke-width="{w:.2f}" stroke-opacity="{o:.3f}" '
            f'stroke-linecap="round"/>')
    return "".join(parts)


def glow_point(p, color, base=6.0):
    parts = []
    for w, o in ((base * 4.0, 0.10), (base * 2.0, 0.28), (base, 1.0)):
        parts.append(
            f'<circle cx="{p[0]:.2f}" cy="{p[1]:.2f}" r="{w/2:.2f}" '
            f'fill="{color}" fill-opacity="{o}"/>')
    return "".join(parts)


def tone_arc_segments(cx, cy, r, winding=1):
    """The bend as a chain of short arcs, each carrying the tone at its angle.
    Winding=1 returns the tone to itself after one loop (honest ruler)."""
    out = []
    for i in range(NSEG):
        a0 = 2 * math.pi * i / NSEG
        a1 = 2 * math.pi * (i + 1) / NSEG
        f = (i + 0.5) / NSEG
        col = palette(f, winding)
        x0, y0 = cx + r * math.cos(a0), cy + r * math.sin(a0)
        x1, y1 = cx + r * math.cos(a1), cy + r * math.sin(a1)
        d = f"M {x0:.2f} {y0:.2f} A {r:.2f} {r:.2f} 0 0 1 {x1:.2f} {y1:.2f}"
        out.append(f'<path d="{d}" fill="none" stroke="{col}" stroke-width="13" '
                   f'stroke-opacity="0.12" stroke-linecap="round"/>')
        out.append(f'<path d="{d}" fill="none" stroke="{col}" stroke-width="5" '
                   f'stroke-opacity="0.85" stroke-linecap="round"/>')
        out.append(f'<path d="{d}" fill="none" stroke="{col}" stroke-width="2" '
                   f'stroke-opacity="0.98" stroke-linecap="round"/>')
    return "".join(out)


def text(x, y, size, fill, s, extra=""):
    return (f'<text x="{x}" y="{y}" font-family="{SERIF}" font-size="{size}" '
            f'fill="{fill}" {extra}>{s}</text>')


# ---- build the SVG ------------------------------------------------------------
svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">']
svg.append(f'<rect width="{W}" height="{H}" fill="{BG}"/>')

# caption
svg.append(text(CX, 74, 34, "#d8cdb8",
                "the plane has one strand",
                'letter-spacing="2" text-anchor="middle"'))
svg.append(text(CX, 108, 17, "#6f6a5c",
                "six lines are open, silent. the bend closes — the only line that can wind.",
                'text-anchor="middle"'))

# the six straight lines, dim brass — they do not close, they cannot wind
for name, pts, kind in lines:
    if kind == "straight":
        svg.append(glow_line(points[pts[0]], points[pts[2]], BRASS, 4, op=0.32))

# the bend: the one closed strand, tone winding once around G
svg.append(tone_arc_segments(G[0], G[1], BR, winding=1))

# the seven points
for name, p in points.items():
    col = POINT
    base = 6.0
    if name == "G":
        col = BRASS
        base = 7.5
    svg.append(glow_point(p, col, base))

# labels
for name in ("A", "B", "C", "G"):
    p = points[name]
    lx, ly = p[0], p[1] + (34 if name == "G" else 30)
    svg.append(
        f'<text x="{lx:.2f}" y="{ly:.2f}" font-family="{SERIF}" font-size="24" '
        f'fill="#8a8a95" text-anchor="middle">{name}</text>')

# the one wind: a small arrow on the bend, and the W=1 note near G
svg.append(text(CX + 18, CY + 96, 15, "#6f6a5c", "W = 1", 'text-anchor="middle"'))

svg.append("</svg>")
svg_str = "".join(svg)

base = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(base, "assets", "fano-strand.svg"), "w") as f:
    f.write(svg_str)
cairosvg.svg2png(bytestring=svg_str.encode(), write_to=os.path.join(base, "assets", "fano-strand.png"),
                 output_width=W, output_height=H)
print("wrote assets/fano-strand.svg and assets/fano-strand.png")
