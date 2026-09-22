#!/usr/bin/env python3
"""make_sl25_room.py — the seam reads SL(2,5): the room is not simple.

The seam (Conway, KT) surjects onto A₅ and PSL(2,7) — both simple.  That made it
tempting to say "the seam reads simple rooms only."  SL(2,5) is the test: perfect,
order 120, centre Z₂, quotient A₅, but NOT simple.  The seam surjects onto it (240
surjections), so the law is not about simplicity: it is about solvability.  A lens
is read iff it holds a non-solvable group, and the image is that group wholly.

Draw the doorways: A₄ mute (floor only), A₅ = one pentagon (simple), SL(2,5) = two
pentagons joined at a Z₂ bar (the double cover, not simple), S₅ = the A₅ room,
GL(3,2) = the Fano plane (PSL(2,7)).  Run:  python3 make_sl25_room.py
"""
import math

import cairosvg

# ---- palette ----------------------------------------------------------------
BG = "#0a0806"
BRASS = "#d4af5a"
COPPER = "#c07a4a"
ROSE = "#d98c8c"
DIM = "#3a3228"
INK = "#8a7a5c"

W, H = 1400, 960


def pt(cx, cy, r, ang_deg):
    a = math.radians(ang_deg)
    return (cx + r * math.cos(a), cy + r * math.sin(a))


def pentagon(cx, cy, r, ang0=-90):
    return [pt(cx, cy, r, ang0 + 72 * k) for k in range(5)]


def polyline(pts, color, sw=3, glow=8, fill=None, opacity=1.0):
    fill_attr = f'fill="{fill}"' if fill else 'fill="none"'
    d = "M " + " L ".join(f"{x:.1f},{y:.1f}" for x, y in pts) + " Z"
    return (f'<path d="{d}" {fill_attr} stroke="{color}" stroke-width="{sw}" '
            f'stroke-linejoin="round" filter="url(#g{glow})" opacity="{opacity}"/>')


def line(x1, y1, x2, y2, color, sw=3, glow=8, opacity=1.0):
    return (f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
            f'stroke="{color}" stroke-width="{sw}" filter="url(#g{glow})" '
            f'opacity="{opacity}"/>')


def dot(x, y, r, color, glow=8):
    return (f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{color}" '
            f'filter="url(#g{glow})"/>')


def text(x, y, s, size, color, anchor="middle", family="serif", weight="normal"):
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-family="{family}" font-size="{size}" '
            f'font-weight="{weight}" fill="{color}" text-anchor="{anchor}">{s}</text>')


# ---- one doorway ------------------------------------------------------------
def doorway(cx, w, ytop, ybot, color=DIM, sw=2, glow=0):
    r = w / 2
    d = (f"M {cx-r:.1f},{ybot:.1f} L {cx-r:.1f},{ytop:.1f} "
         f"A {r:.1f},{r:.1f} 0 0 1 {cx+r:.1f},{ytop:.1f} "
         f"L {cx+r:.1f},{ybot:.1f}")
    return f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{sw}"/>'


def build_svg():
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
         f'viewBox="0 0 {W} {H}">']
    s.append(f'<rect width="{W}" height="{H}" fill="{BG}"/>')
    # glow filters
    s.append('<defs>')
    for g in (4, 8, 14):
        s.append(f'<filter id="g{g}" x="-50%" y="-50%" width="200%" height="200%">'
                 f'<feGaussianBlur stdDeviation="{g}"/></filter>')
    s.append('</defs>')

    s.append(text(W / 2, 70, "the room is not simple", 46, BRASS, weight="bold"))
    s.append(text(W / 2, 112, "the seam reads SL(2,5) — a perfect double cover of A₅, not simple",
                  22, INK))

    # columns
    ytop, ybot, w = 210, 640, 210
    centers = [180, 430, 680, 930, 1180]
    labels = [("A₄", "|G| 12"), ("A₅", "|G| 60"), ("SL(2,5)", "|G| 120"),
              ("S₅", "|G| 120"), ("GL(3,2)", "|G| 168")]
    mids = [(12, "mute — floor only"), (120, "A₅ · 120 surj"),
            (240, "SL(2,5) · 240"), (120, "A₅ · 120"), (1344, "PSL(2,7)")]

    for cx, (nm, gsize), (cnt, imglbl) in zip(centers, labels, mids):
        s.append(doorway(cx, w, ytop, ybot))
        s.append(text(cx, ytop - 24, nm, 30, BRASS))
        s.append(text(cx, ytop - 2, gsize, 15, DIM))

        if nm == "A₄":
            # mute: a dim empty floor dot
            s.append(dot(cx, (ytop + ybot) / 2, 5, DIM, 4))
            s.append(text(cx, ybot - 40, "mute", 16, DIM))
        elif nm in ("A₅", "S₅"):
            col = BRASS if nm == "A₅" else COPPER
            p = pentagon(cx, (ytop + ybot) / 2, 62)
            s.append(polyline(p, col, sw=3, glow=8))
            s.append(text(cx, ybot - 40, "A₅", 20, col))
        elif nm == "SL(2,5)":
            # double cover: two pentagons joined at the Z₂ bar
            cyc = (ytop + ybot) / 2
            p1 = pentagon(cx, cyc - 78, 55)
            p2 = pentagon(cx, cyc + 78, 55)
            s.append(line(cx, cyc - 30, cx, cyc + 30, ROSE, sw=4, glow=8))
            s.append(polyline(p1, BRASS, sw=3, glow=8))
            s.append(polyline(p2, COPPER, sw=3, glow=8))
            s.append(dot(cx, cyc, 5, ROSE, 8))
            s.append(text(cx, ybot - 40, "SL(2,5)", 18, ROSE))
        elif nm == "GL(3,2)":
            # canonical Fano: triangle vertices + side midpoints + centroid;
            # six straight lines + the circle through the midpoints (the bend).
            cyc = (ytop + ybot) / 2
            r = 60
            A = (cx, cyc - r)
            B = (cx - math.cos(math.pi / 6) * r, cyc + 0.5 * r)
            C = (cx + math.cos(math.pi / 6) * r, cyc + 0.5 * r)
            mAB = ((A[0] + B[0]) / 2, (A[1] + B[1]) / 2)
            mBC = ((B[0] + C[0]) / 2, (B[1] + C[1]) / 2)
            mCA = ((C[0] + A[0]) / 2, (C[1] + A[1]) / 2)
            Gd = ((A[0] + B[0] + C[0]) / 3, (A[1] + B[1] + C[1]) / 3)
            for (p0, p1) in [(A, B), (B, C), (C, A), (A, mBC), (B, mCA), (C, mAB)]:
                s.append(line(p0[0], p0[1], p1[0], p1[1], BRASS, sw=2, glow=6, opacity=0.85))
            rad = math.hypot(Gd[0] - mAB[0], Gd[1] - mAB[1])
            s.append(f'<circle cx="{Gd[0]:.1f}" cy="{Gd[1]:.1f}" r="{rad:.1f}" '
                     f'fill="none" stroke="{ROSE}" stroke-width="2" filter="url(#g6)"/>')
            for (px, py) in (A, B, C, mAB, mBC, mCA, Gd):
                s.append(dot(px, py, 4.5, ROSE, 8))
            s.append(text(cx, ybot - 40, "PSL(2,7)", 18, ROSE))

        s.append(text(cx, ybot + 30, f"{cnt} homs", 16, INK))
        s.append(text(cx, ybot + 52, imglbl, 14, DIM))

    # the floor line (the cyclic abelianization floor)
    s.append(line(90, ybot + 90, W - 90, ybot + 90, DIM, sw=2, glow=0, opacity=0.8))
    s.append(text(W / 2, ybot + 122, "the floor: mute in every solvable lens — every image cyclic.  rises at the first non-solvable",
                  17, INK))
    s.append(text(W / 2, ybot + 152, "the law is not “simple rooms” — it is non-solvable rooms, whole or not at all: 360 = 120 + 240, and 240 = 2 × 120",
                  17, INK))

    s.append('</svg>')
    return "\n".join(s)


def main():
    svg = build_svg()
    with open("assets/sl25_room.svg", "w") as f:
        f.write(svg)
    cairosvg.svg2png(url="assets/sl25_room.svg", write_to="assets/sl25_room.png",
                     output_width=W, output_height=H)
    print("wrote assets/sl25_room.svg and .png")


if __name__ == "__main__":
    main()
