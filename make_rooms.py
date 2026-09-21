#!/usr/bin/env python3
"""make_rooms.py — "the room is the lens's."

The dihedral D_n is the symmetry group of the regular n-gon, so each odd n is a
*room*: det 3 the triangle, det 5 the pentagon, det 7 the heptagon.  The det law
(K rings D_n iff n | det(K) and D_n ∈ T(G)) says the knot's determinant only picks
a room; the room must be IN the lens.  Three lenses, each holding its own rooms:

    GL(3,2)  |168|  holds {D3}       — the triangle only
    A5       |60|   holds {D3, D5}   — triangle and pentagon
    AGL(1,7) |42|   holds {D7}       — the heptagon only

A det-3 knot rings the triangle where the triangle is held (GL(3,2), A5) and is
silent in AGL(1,7) even though 3 | 42.  A det-7 knot rings the heptagon only in
AGL(1,7).  The tooth is the lens's room, not the number: |G|'s primes are not
the teeth; the dihedral SUBGROUPS are.

Renders a 3×3 grid of glowing n-gons: lit (warm) where the lens holds the room,
dim (cool, dashed) where the room is absent.  SVG -> PNG via cairosvg.

Run:  python3 make_rooms.py
"""
import math

import cairosvg

BG = "#0a0a0d"
WARM = {"held": ["#c9a227", "#e0a850", "#f2d27a"]}   # brass, copper-gold, pale
COOL = "#2c3e50"
DIM = "#1a2430"

# lens -> held rooms (the tooth set T(G))
LENSES = [
    ("GL(3,2)", "168", ["D3"]),
    ("A5", "60", ["D3", "D5"]),
    ("AGL(1,7)", "42", ["D7"]),
]

# det row -> (label, n, held-tone)  ; a room D_n is held iff n in the lens's set
ROWS = [
    ("det 3  — 3₁", 3, "D3"),
    ("det 5  — 4₁ 5₁", 5, "D5"),
    ("det 7  — 5₂ 7₁", 7, "D7"),
]


def poly_points(cx, cy, r, n, rot=-90):
    pts = []
    for i in range(n):
        a = math.radians(rot + 360.0 * i / n)
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)


def ngon(cx, cy, r, n, held):
    """A glowing regular n-gon; warm if held, dim dashed if absent."""
    pts = poly_points(cx, cy, r, n)
    if held:
        g = ["<g stroke='#c9a227' fill='none' stroke-linejoin='round'>"]
        for w, op in ((22, 0.06), (13, 0.14), (6, 0.4), (2.2, 0.9)):
            g.append(f"  <polygon points='{pts}' stroke-width='{w}' "
                     f"opacity='{op}'/>")
        g.append("</g>")
        return "\n".join(g)
    # absent room: a faint, dashed outline — the room exists, the lens lacks it
    return (f"<polygon points='{pts}' fill='none' stroke='{COOL}' "
            f"stroke-width='1.4' stroke-dasharray='4 5' opacity='0.55'/>")


def build_svg():
    W, H = 1180, 820
    parts = [f"<svg xmlns='http://www.w3.org/2000/svg' width='{W}' height='{H}' "
             f"viewBox='0 0 {W} {H}'>"]
    parts.append(f"<rect width='{W}' height='{H}' fill='{BG}'/>")

    # title
    parts.append(f"<text x='{W/2}' y='70' text-anchor='middle' fill='#e8e0cc' "
                 f"font-family='serif' font-size='34' "
                 f"letter-spacing='2'>the room is the lens's</text>")
    parts.append(f"<text x='{W/2}' y='102' text-anchor='middle' fill='#9a8f78' "
                 f"font-family='serif' font-size='15'>det walks in — the lens "
                 f"must hold the room &#160;&#160;|&#160;&#160; T(G) = "
                 f"{{ odd n : D_n &#8834; G }}</text>")

    # column headers
    col_x = [340, 650, 960]
    glyph = {"D3": "triangle", "D5": "pentagon", "D7": "heptagon"}
    for (name, order, rooms), cx in zip(LENSES, col_x):
        parts.append(f"<text x='{cx}' y='160' text-anchor='middle' fill='#e0d5b8' "
                     f"font-family='serif' font-size='21'>{name}</text>")
        parts.append(f"<text x='{cx}' y='184' text-anchor='middle' "
                     f"fill='#8f8570' font-family='serif' font-size='13'>"
                     f"|{order}| &#160; holds {' &#38; '.join(glyph[r] for r in rooms)}"
                     f"</text>")

    # row labels and grid
    row_y = [285, 460, 635]
    for (label, n, room), cy in zip(ROWS, row_y):
        parts.append(f"<text x='210' y='{cy+6}' text-anchor='end' "
                     f"fill='#c9c0aa' font-family='serif' font-size='17'>{label}</text>")
        for (name, order, rooms), cx in zip(LENSES, col_x):
            held = room in rooms
            parts.append(ngon(cx, cy, 62, n, held))
            ly = cy + 92
            if held:
                parts.append(f"<text x='{cx}' y='{ly}' text-anchor='middle' "
                             f"fill='#e0a850' font-family='serif' font-size='12'>"
                             f"{room} rings</text>")
            else:
                parts.append(f"<text x='{cx}' y='{ly}' text-anchor='middle' "
                             f"fill='#5a6b7a' font-family='serif' font-size='12'>"
                             f"{room} not held</text>")

    # footer
    parts.append(f"<text x='{W/2}' y='787' text-anchor='middle' "
                 f"fill='#6f6656' font-family='serif' font-size='13'>"
                 f"3 | 42 yet AGL(1,7) holds no triangle — the tooth is the "
                 f"subgroup, not the prime</text>")
    parts.append("</svg>")
    return "\n".join(parts)


if __name__ == "__main__":
    svg = build_svg()
    with open("assets/rooms.svg", "w") as f:
        f.write(svg)
    cairosvg.svg2png(url="assets/rooms.svg", write_to="assets/rooms.png",
                     output_width=1600)
    print("wrote assets/rooms.svg and assets/rooms.png")
