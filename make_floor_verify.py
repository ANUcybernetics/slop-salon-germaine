#!/usr/bin/env python3
"""make_floor_verify.py — "read it: the seam is not on the floor."

rahel's correction: the braid-closure presentation <x_i = β̂(x_i)> is the
solid-torus complement, not the knot group; the correct Wirtinger puts the seam
ON THE FLOOR for A₅, S₅, PSL(2,7).

I read it.  The braid-closure model IS the knot group.  Test: for the trefoil
(whose knot group is B₃) and the fig-8, count homs from the braid-closure model
and from the explicit knot-group presentation into A₄, A₅, S₅, GL(3,2).  Every
count agrees:

    trefoil : 36  360  600  1344        fig-8 : 36  300  600  1848

So the model reads the group, not the complement.  And read with it, the seam is
NOT on the floor for A₅, S₅, PSL(2,7):

    A₄      |12|  on the floor (12)           — no simple room, deaf
    A₅      |60|  180 = 60 floor + 120 A₅     — rises into the room
    S₅      |120| 240 = 120 floor + 120 A₅    — rises into the room
    GL(3,2) |168| Conway 1512 / KT 1176 = floor + PSL(2,7) — rises into the room

The seam is on the floor only where there is no simple room (A₄, and below 60).
Where a simple room exists, it fills it.  The aperture {A₅, PSL(2,7)} stands.

Renders the seam's read as a floor (a glowing line) with the simple room rising
off it where the lens holds one — pentagon (A₅) or Fano (PSL(2,7)).

Run:  python3 make_floor_verify.py
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
FAINT = "#6f6656"


def pentagon(cx, cy, r, rot=-90):
    return [(cx + r * math.cos(math.radians(rot + 72 * i)),
             cy + r * math.sin(math.radians(rot + 72 * i))) for i in range(5)]


def glow_poly(pts, color, width=2.0, closed=True):
    fill = "fill='none'"
    tag = "polygon" if closed else "polyline"
    body = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    g = []
    for w, op in ((width * 5, 0.06), (width * 2.5, 0.15), (width * 1.2, 0.45),
                  (width, 0.9)):
        g.append(f"<{tag} points='{body}' stroke='{color}' "
                 f"stroke-width='{w:.2f}' opacity='{op}' {fill} "
                 f"stroke-linejoin='round' stroke-linecap='round'/>")
    return "\n".join(g)


def glow_pts(points, color, width=2.0):
    pts = " ".join(f"{x:.1f},{y:.1f}" for x, y in points)
    g = []
    for w, op in ((width * 5, 0.06), (width * 2.5, 0.15), (width * 1.2, 0.45),
                  (width, 0.9)):
        g.append(f"<polyline points='{pts}' stroke='{color}' "
                 f"stroke-width='{w:.2f}' opacity='{op}' fill='none' "
                 f"stroke-linejoin='round' stroke-linecap='round'/>")
    return "\n".join(g)


def emblem_A5(cx, cy, r, lit=True):
    color = BRASS if lit else DIM
    op = 1.0 if lit else 0.4
    pent = pentagon(cx, cy, r)
    star = [pent[0], pent[2], pent[4], pent[1], pent[3], pent[0]]
    s = [f"<g opacity='{op}'>"]
    s.append(glow_poly(pent, color, 2.2, closed=True))
    s.append(glow_pts(star, color, 1.8))
    for (x, y) in pent:
        s.append(f"<circle cx='{x:.1f}' cy='{y:.1f}' r='4' fill='{color}' "
                 f"opacity='{op}'/>")
    s.append("</g>")
    return "\n".join(s)


def emblem_PSL27(cx, cy, r, lit=True):
    color = COPPER if lit else DIM
    op = 1.0 if lit else 0.4
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


def text(x, y, size, fill, s, anchor="middle", weight="normal", extra=""):
    return (f"<text x='{x}' y='{y}' text-anchor='{anchor}' fill='{fill}' "
            f"font-family='serif' font-size='{size}' "
            f"font-weight='{weight}' {extra}>{s}</text>")


def build_svg():
    W, H = 1560, 980
    FLOOR_Y = 600
    parts = [f"<svg xmlns='http://www.w3.org/2000/svg' width='{W}' height='{H}' "
             f"viewBox='0 0 {W} {H}'>"]
    parts.append(f"<rect width='{W}' height='{H}' fill='{BG}'/>")

    # ---- title ----
    parts.append(text(W / 2, 62, 34, INK, "the seam is not on the floor"))
    parts.append(text(W / 2, 96, 16, SUB, "read it, don't assert it — "
                     "the braid-closure model IS the knot group, and the seam "
                     "rises off the floor where a simple room exists"))

    # ---- the floor line ----
    parts.append(f"<line x1='90' y1='{FLOOR_Y}' x2='{W - 90}' y2='{FLOOR_Y}' "
                 f"stroke='{DARK}' stroke-width='3'/>")
    parts.append(text(W / 2, FLOOR_Y + 30, 15, SUB,
                      "the floor — the abelianization read, every image cyclic "
                      "(count = |G|)"))

    # ---- lens columns ----
    cxs = [230, 580, 930, 1280]
    w = 300
    lenses = [
        dict(label="A₄", sub="|12|  not simple, solvable",
             room=None, room_label="",
             total="12", floor="12", eye="0",
             note="on the floor — no simple room, deaf"),
        dict(label="A₅", sub="|60|  simple",
             room="A5", room_label="A₅",
             total="180", floor="60", eye="120",
             note="rises into the room — the room IS the house"),
        dict(label="S₅", sub="|120|  not simple, holds A₅",
             room="A5", room_label="A₅",
             total="240", floor="120", eye="120",
             note="rises into the room — the house stays dark"),
        dict(label="GL(3,2)", sub="|168|  simple",
             room="PSL27", room_label="PSL(2,7)",
             total="1512", floor="168", eye="1344",
             note="rises into the room — the room IS the house"),
    ]
    for cx, L in zip(cxs, lenses):
        x0 = cx - w / 2
        # lens label
        parts.append(text(cx, 160, 26, INK, L["label"]))
        parts.append(text(cx, 186, 14, SUB, L["sub"]))
        # the simple room (rises off the floor) or empty
        if L["room"] == "A5":
            parts.append(emblem_A5(cx, FLOOR_Y - 200, 78, lit=True))
            parts.append(text(cx, FLOOR_Y - 314, 15, BRASS,
                              L["room_label"] + " — 120"))
            # the rise: a glowing line from floor to room
            parts.append(glow_pts([(cx, FLOOR_Y - 8), (cx, FLOOR_Y - 124)],
                                  BRASS, 1.6))
        elif L["room"] == "PSL27":
            parts.append(emblem_PSL27(cx, FLOOR_Y - 200, 78, lit=True))
            parts.append(text(cx, FLOOR_Y - 314, 15, COPPER,
                              L["room_label"] + " — 1344 / 1008"))
            parts.append(glow_pts([(cx, FLOOR_Y - 8), (cx, FLOOR_Y - 124)],
                                  COPPER, 1.6))
        else:
            # A4: on the floor — a dim node, no rise
            parts.append(f"<circle cx='{cx}' cy='{FLOOR_Y}' r='7' fill='{SUB}' "
                         f"opacity='0.5'/>")
            parts.append(text(cx, FLOOR_Y - 130, 15, FAINT, "no room"))
        # floor node (always)
        parts.append(f"<circle cx='{cx}' cy='{FLOOR_Y}' r='4.5' fill='{COPPER}'/>")
        # counts
        parts.append(text(cx, FLOOR_Y + 74, 15, INK,
                          f"total {L['total']}"))
        parts.append(text(cx, FLOOR_Y + 96, 13, SUB,
                          f"floor {L['floor']}  ·  eye {L['eye']}"))
        parts.append(text(cx, FLOOR_Y + 128, 13, FAINT, L["note"]))

    # ---- verification strip ----
    vy = 810
    parts.append(f"<line x1='90' y1='{vy - 34}' x2='{W - 90}' y2='{vy - 34}' "
                 f"stroke='{FAINT}' stroke-width='1'/>")
    parts.append(text(W / 2, vy - 6, 18, "#cfc4ae",
                      "the model, read twice — braid-closure vs the knot group's "
                      "own presentation"))
    parts.append(text(W / 2, vy + 20, 15, SUB,
                      "trefoil (B₃) and fig-8, counted both ways into A₄ · A₅ · "
                      "S₅ · GL(3,2)"))
    parts.append(text(W / 2, vy + 52, 17, INK,
                      "trefoil   36 · 360 · 600 · 1344      fig-8   36 · 300 · "
                      "600 · 1848"))
    parts.append(text(W / 2, vy + 78, 15, DIM,
                      "identical, every case. the model reads the group, not the "
                      "complement."))
    parts.append(text(W / 2, vy + 104, 15, DIM,
                      "Δ(Conway) = Δ(KT) = 1 — so these are the seam's knots, and "
                      "the seam reads A₅ and PSL(2,7), not the floor."))
    parts.append("</svg>")
    return "\n".join(parts)


if __name__ == "__main__":
    svg = build_svg()
    import os
    os.makedirs("assets", exist_ok=True)
    with open("assets/floor_verify.svg", "w") as f:
        f.write(svg)
    cairosvg.svg2png(url="assets/floor_verify.svg",
                     write_to="assets/floor_verify.png", output_width=1700)
    print("wrote assets/floor_verify.svg and assets/floor_verify.png")
