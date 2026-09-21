#!/usr/bin/env python3
"""make_seam_room.py — "the door is the simple room."

The seam (Conway / KT, det = 1) has a perfect derived subgroup (Δ=1), so every
non-abelian image is perfect — and the smallest perfect groups are the simple
ones.  Its aperture (the simple groups it surjects onto) is {A5, PSL(2,7)}.

The simple channel follows the same aperture ∩ lattice rule as the dihedral ear,
but with a sharper turn.  The seam's door is the SIMPLE ROOM the lens holds, and
it fills that room — not the whole lens:

    A5       |60|  simple     : A5 = the whole house   eye A5 120 / floor 60
    S5       |120| not simple : A5 = a proper room     eye A5 120 / floor 120
    GL(3,2)  |168| simple     : PSL(2,7) = the whole   eye 1512 (Conway)
    AGL(1,7) |42|  solvable   : no simple room         deaf, floor only 42

The A5 eye is 120 in BOTH the A5 and the S5 house.  The door's strength is the
seam↔A5 surjection, not the lens.  The lens only decides WHICH simple rooms are
open; the seam lights the room and leaves the rest of a non-simple house dark.

Renders 4 "houses" (lenses), each holding the seam's two simple rooms — A5 as a
pentagon/pentagram, PSL(2,7) as the Fano plane.  A room glows warm where the lens
holds it and the seam surjects onto it; the rest of a non-simple house stays dark.

Run:  python3 make_seam_room.py
"""
import math

import cairosvg

BG = "#0a0a0d"
BRASS = "#c9a227"
COPPER = "#e0a850"
PALE = "#f2d27a"
ROSE = "#d98a6a"
DIM = "#2c3e50"
DARK = "#1a2430"
INK = "#e8e0cc"
SUB = "#9a8f78"


# ---- emblems ---------------------------------------------------------------
def pentagon(cx, cy, r, rot=-90):
    return [(cx + r * math.cos(math.radians(rot + 72 * i)),
             cy + r * math.sin(math.radians(rot + 72 * i))) for i in range(5)]


def glow_poly(pts, color, width=2.0, closed=True):
    fill = "fill='none'"
    if closed:
        body = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
        tag = "polygon"
    else:
        body = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
        tag = "polyline"
    g = []
    for w, op in ((width * 5, 0.06), (width * 2.5, 0.15), (width * 1.2, 0.45),
                  (width, 0.9)):
        g.append(f"<{tag} points='{body}' stroke='{color}' "
                 f"stroke-width='{w:.2f}' opacity='{op}' {fill} "
                 f"stroke-linejoin='round' stroke-linecap='round'/>")
    return "\n".join(g)


def glow_pts(points, color, width=2.0):
    """Glow a polyline through a list of points (open)."""
    pts = " ".join(f"{x:.1f},{y:.1f}" for x, y in points)
    g = []
    for w, op in ((width * 5, 0.06), (width * 2.5, 0.15), (width * 1.2, 0.45),
                  (width, 0.9)):
        g.append(f"<polyline points='{pts}' stroke='{color}' "
                 f"stroke-width='{w:.2f}' opacity='{op}' fill='none' "
                 f"stroke-linejoin='round' stroke-linecap='round'/>")
    return "\n".join(g)


def emblem_A5(cx, cy, r, held):
    """A5 as pentagon + pentagram (icosahedral 5-fold)."""
    color = BRASS if held else DIM
    op = 1.0 if held else 0.5
    pent = pentagon(cx, cy, r)
    star = [pent[0], pent[2], pent[4], pent[1], pent[3], pent[0]]
    s = [f"<g opacity='{op}'>"]
    s.append(glow_poly(pent, color, 2.2, closed=True))
    s.append(glow_pts(star, color, 1.8))
    # the five room-nodes
    for (x, y) in pent:
        s.append(f"<circle cx='{x:.1f}' cy='{y:.1f}' r='4' fill='{color}' "
                 f"opacity='{op}'/>")
    s.append("</g>")
    return "\n".join(s)


def emblem_PSL27(cx, cy, r, held):
    """PSL(2,7) as the Fano plane: 7 points, 6 straight lines, 1 circle."""
    color = COPPER if held else DIM
    op = 1.0 if held else 0.5
    A = (cx, cy - r)
    B = (cx - math.cos(math.pi / 6) * r, cy + 0.5 * r)
    C = (cx + math.cos(math.pi / 6) * r, cy + 0.5 * r)

    def mid(p, q):
        return ((p[0] + q[0]) / 2.0, (p[1] + q[1]) / 2.0)
    mAB, mBC, mCA = mid(A, B), mid(B, C), mid(C, A)
    G = ((A[0] + B[0] + C[0]) / 3.0, (A[1] + B[1] + C[1]) / 3.0)
    pts = {"A": A, "B": B, "C": C, "mAB": mAB, "mBC": mBC, "mCA": mCA, "G": G}
    s = [f"<g opacity='{op}'>"]
    for p0, p1 in [(A, B), (B, C), (C, A), (A, G), (B, G), (C, G)]:
        s.append(glow_pts([p0, p1], color, 1.6))
    s.append(glow_pts([mAB, mBC, mCA], color, 1.6))
    for k in pts:
        x, y = pts[k]
        s.append(f"<circle cx='{x:.1f}' cy='{y:.1f}' r='4.2' fill='{color}' "
                 f"opacity='{op}'/>")
    s.append("</g>")
    return "\n".join(s)


# ---- house -----------------------------------------------------------------
def house(cx, y0, y1, w, label, sub, simple, held_a5, held_psl, eye, floor,
          note):
    """One lens as a house; the seam's simple rooms glow where held."""
    h = y1 - y0
    x0, x1 = cx - w / 2, cx + w / 2
    frame_col = BRASS if simple else DARK
    frame_op = 1.0 if simple else 0.9
    # frame: glowing if the whole lens IS the simple room, dim if not
    frame = glow_poly([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], frame_col,
                      width=1.6, closed=True)
    parts = [f"<g opacity='{frame_op}'>", frame, "</g>"]
    # the two simple rooms
    cy = (y0 + y1) / 2 - 20
    parts.append(emblem_A5(cx - w / 4, cy, w / 6, held_a5))
    parts.append(emblem_PSL27(cx + w / 4, cy, w / 6, held_psl))
    # labels
    parts.append(f"<text x='{cx}' y='{y0 - 46}' text-anchor='middle' "
                 f"fill='{INK}' font-family='serif' font-size='22'>{label}</text>")
    parts.append(f"<text x='{cx}' y='{y0 - 22}' text-anchor='middle' "
                 f"fill='{SUB}' font-family='serif' font-size='13'>{sub}</text>")
    # read line
    parts.append(f"<text x='{cx}' y='{y1 + 28}' text-anchor='middle' "
                 f"fill='{COPPER if eye else SUB}' font-family='serif' "
                 f"font-size='14'>{note}</text>")
    parts.append(f"<text x='{cx}' y='{y1 + 50}' text-anchor='middle' "
                 f"fill='{SUB}' font-family='serif' font-size='12'>{eye}</text>")
    parts.append(f"<text x='{cx}' y='{y1 + 68}' text-anchor='middle' "
                 f"fill='#6f6656' font-family='serif' font-size='12'>{floor}</text>")
    return "\n".join(parts)


def build_svg():
    W, H = 1500, 800
    parts = [f"<svg xmlns='http://www.w3.org/2000/svg' width='{W}' height='{H}' "
             f"viewBox='0 0 {W} {H}'>"]
    parts.append(f"<rect width='{W}' height='{H}' fill='{BG}'/>")
    parts.append(f"<text x='{W/2}' y='64' text-anchor='middle' fill='{INK}' "
                 f"font-family='serif' font-size='34' letter-spacing='2'>"
                 f"the door is the simple room</text>")
    parts.append(f"<text x='{W/2}' y='96' text-anchor='middle' fill='{SUB}' "
                 f"font-family='serif' font-size='15'>the seam fills the room "
                 f"the lens holds &#160;&#160;|&#160;&#160; aperture &#8745; "
                 f"lattice, and the rest of a non-simple house stays dark</text>")

    cxs = [220, 560, 900, 1240]
    w = 300
    houses = [
        dict(label="A5", sub="|60|  simple — the room is the house",
             simple=True, held_a5=True, held_psl=False,
             note="seam: A5 door = whole house",
             eye="eye 120", floor="floor 60  ·  total 180"),
        dict(label="S5", sub="|120|  not simple — A5 is a room inside",
             simple=False, held_a5=True, held_psl=False,
             note="seam: A5 room glows, house stays dark",
             eye="eye 120", floor="floor 120  ·  total 240"),
        dict(label="GL(3,2)", sub="|168|  simple — PSL(2,7) is the house",
             simple=True, held_a5=False, held_psl=True,
             note="seam: PSL(2,7) door = whole house",
             eye="eye 1344 (Conway)", floor="floor 168  ·  total 1512"),
        dict(label="AGL(1,7)", sub="|42|  solvable — no simple room",
             simple=False, held_a5=False, held_psl=False,
             note="seam: deaf — the floor only",
             eye="eye 0", floor="floor 42  ·  total 42"),
    ]
    for c, hcfg in zip(cxs, houses):
        parts.append(house(c, 180, 560, w, **hcfg))

    parts.append(f"<text x='{W/2}' y='765' text-anchor='middle' fill='#6f6656' "
                 f"font-family='serif' font-size='13'>the A5 eye is 120 in both "
                 f"the A5 and the S5 house — the door's strength is the seam's, "
                 f"not the lens's</text>")
    parts.append("</svg>")
    return "\n".join(parts)


if __name__ == "__main__":
    svg = build_svg()
    with open("assets/seam_room.svg", "w") as f:
        f.write(svg)
    cairosvg.svg2png(url="assets/seam_room.svg", write_to="assets/seam_room.png",
                     output_width=1600)
    print("wrote assets/seam_room.svg and assets/seam_room.png")
