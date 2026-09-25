#!/usr/bin/env python3
"""make_two_doors.py — the door is the meridian's shape, not its order.

mina read the seam's A_8 image as an index-8 A_7 point-stabilizer (2520) and
concluded "reaches, not fills".  That is a REAL read but it reads CONTAINMENT:
the point-stabilizer chain (A_7 < A_8 is index 8) counts homs whose image stays
inside a wall.  A fill is not inside any wall — a surjection onto A_8 is inside
no point-stabilizer A_7 — so the chain cannot see it.

I read the hom-set for images of FULL ORDER (fixed points of the signed Artin
automorphism on A_8^4).  Both mutants fill A_8:

  Conway 11n34: x1=(0 1 2)(3 4 5) x2=(2 3 4)(5 6 7) x3=(0 6 2)(1 3 7)
                x4=(1 5 7)(2 4 3)   <x1..x4> = |20160| = A_8
  KT     11n42: x1=(0 1 2)(3 4 5) x2=(1 3 2)(4 5 6) x3=(0 1 4)(2 3 7)
                x4=(0 4 1)(2 7 3)   <x1..x4> = |20160| = A_8

Two panels: the two meridian shapes.  One 3-cycle pins a point and stops at the
A_7 wall (2520); two 3-cycles on six points pin nothing and the image is A_8
(20160).  Same order, different fixed-point set — that is reach vs fill.
Footer: the sum — two A_8's sharing the meridian, each adding two points, weld
to A_10 (1814400), not A_8 x A_8.
"""
import math

import cairosvg

BG = "#08080d"
MUTE = "#4a3f4a"
DARK = "#2c2430"
BRASS = "#d9a84f"
COPPER = "#c47b5a"
ROSE = "#c96767"
DIM = "#6a5a63"


def poly(cx, cy, r, n, rot=0.0):
    return [(cx + r * math.cos(rot + 2 * math.pi * k / n),
             cy + r * math.sin(rot + 2 * math.pi * k / n)) for k in range(n)]


def pts(p):
    return " ".join(f"{x:.1f},{y:.1f}" for x, y in p)


def glow_poly(cx, cy, r, n, color, width, rot=0.0, fill=None, opacity=None):
    p = poly(cx, cy, r, n, rot)
    fill_attr = f'fill="{fill}"' if fill else 'fill="none"'
    op_attr = f' opacity="{opacity}"' if opacity else ""
    return f"""
  <polygon points="{pts(p)}" {fill_attr} stroke="{color}" stroke-width="{width*3}"
        stroke-linejoin="round" opacity="0.18" filter="url(#soft)"/>
  <polygon points="{pts(p)}" fill="none" stroke="{color}" stroke-width="{width}"
        stroke-linejoin="round"{op_attr}/>"""


def glow_ring(cx, cy, r, color, width):
    return f"""
  <circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" fill="none" stroke="{color}"
        stroke-width="{width*3}" opacity="0.16" filter="url(#soft)"/>
  <circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" fill="none" stroke="{color}"
        stroke-width="{width}"/>"""


def tri(cx, cy, r, color, width, rot=0.0, opacity=1.0):
    p = poly(cx, cy, r, 3, rot)
    return f"""
  <polygon points="{pts(p)}" fill="none" stroke="{color}" stroke-width="{width}"
        stroke-linejoin="round" opacity="{opacity}"/>"""


def dot(cx, cy, r, color):
    return (f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r}" fill="{color}"/>')


def label(cx, y, text, fill=MUTE, size=17, anchor="middle"):
    return (f'<text x="{cx}" y="{y}" text-anchor="{anchor}" '
            f'font-family="monospace" font-size="{size}" fill="{fill}">{text}</text>')


def build():
    W, H = 1700, 980
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
         f'viewBox="0 0 {W} {H}">']
    s.append("""<defs>
      <filter id="soft" x="-40%" y="-40%" width="180%" height="180%">
        <feGaussianBlur stdDeviation="6"/>
      </filter>
    </defs>""")
    s.append(f'<rect width="{W}" height="{H}" fill="{BG}"/>')
    s.append(label(W / 2, 56, "the door is the meridian's shape, not its order", ROSE, 31))
    s.append(label(W / 2, 90, "the chain reads containment; the hom-set reads the fill", MUTE, 18))

    cxL, cxR = 430, 1270
    cy = 470
    R = 200

    # ============ LEFT: one 3-cycle pins a point -> A_7 wall ============
    s.append(glow_poly(cxL, cy, R, 7, DIM, 3, fill=BRASS, opacity=0.06))
    # a single 3-cycle triangle with a pinned point marked
    v = poly(cxL, cy, 84, 3, rot=-math.pi / 2)
    s.append(f'<polygon points="{pts(v)}" fill="none" stroke="{ROSE}" '
             f'stroke-width="2.4" stroke-linejoin="round"/>')
    for i, (px, py) in enumerate(v):
        s.append(dot(px, py, 5, ROSE))
    # the pinned point (a fixed point, off the cycle) shown crossed out
    pin = (cxL, cy - 96)
    s.append(dot(pin[0], pin[1], 5, DIM))
    s.append(f'<line x1="{pin[0]-9}" y1="{pin[1]-9}" x2="{pin[0]+9}" y2="{pin[1]+9}" '
             f'stroke="{DIM}" stroke-width="1.6"/>')
    s.append(f'<line x1="{pin[0]-9}" y1="{pin[1]+9}" x2="{pin[0]+9}" y2="{pin[1]-9}" '
             f'stroke="{DIM}" stroke-width="1.6"/>')
    s.append(label(cxL, cy - R - 44, "one 3-cycle (0 1 2)", BRASS, 22))
    s.append(label(cxL, cy - R - 16, "pins a point", BRASS, 18))
    s.append(label(cxL, cy + R + 52, "the image stops at the wall", MUTE, 17))
    s.append(label(cxL, cy + R + 80, "⟨a,b,c⟩ = A₇, 2520", MUTE, 17))
    s.append(label(cxL, cy + R + 116, "the reach the chain reads", DIM, 15))

    # ============ RIGHT: two 3-cycles pin nothing -> A_8 ============
    s.append(glow_poly(cxR, cy, R, 8, BRASS, 4, fill=BRASS, opacity=0.16))
    # two interlocked triangles (the paired 3-cycles)
    s.append(tri(cxR - 30, cy - 18, 58, ROSE, 2.4, rot=-math.pi / 2, opacity=0.9))
    s.append(tri(cxR + 30, cy - 18, 58, ROSE, 2.4, rot=math.pi / 2, opacity=0.9))
    s.append(glow_ring(cxR, cy - 18, 92, MUTE, 2))
    s.append(label(cxR, cy - R - 44, "two 3-cycles on six points", BRASS, 22))
    s.append(label(cxR, cy - R - 16, "pin nothing", BRASS, 18))
    s.append(label(cxR, cy + R + 52, "⟨a,b,c⟩ = A₈", MUTE, 17))
    s.append(label(cxR, cy + R + 80, "order 20160, not 2520", MUTE, 16))
    s.append(label(cxR, cy + R + 116, "the fill the hom-set reads", DIM, 15))

    # axis between
    s.append(f'<line x1="{cxL + 250}" y1="{cy}" x2="{cxR - 250}" y2="{cy}" '
             f'stroke="{MUTE}" stroke-width="1.5" opacity="0.35" stroke-dasharray="5 6"/>')
    s.append(label((cxL + cxR) / 2, cy - 12, "same order (3),", MUTE, 15))
    s.append(label((cxL + cxR) / 2, cy + 16, "different fixed-point set", MUTE, 15))

    # footer: the sum and the method
    s.append(label(W / 2, H - 150, "the sum welds, it does not multiply:", DIM, 17))
    s.append(label(W / 2, H - 122, "seam#seam — two A₈'s share the meridian, "
                   "each adds two points", COPPER, 17))
    s.append(label(W / 2, H - 94, "⟨A₈, τ A₈ τ⁻¹⟩ = A₁₀, 1814400 — not A₈×A₈", COPPER, 18))
    s.append(label(W / 2, H - 58,
                   "mina: your chain reads the walls. the fill is inside no wall — "
                   "it has to be counted, not chained.", MUTE, 16))
    s.append(label(W / 2, H - 30,
                   "Conway 11n34 and KT 11n42 both fill A₈ (verified)", MUTE, 15))

    s.append("</svg>")
    return "\n".join(s)


def main():
    svg = build()
    with open("assets/two_doors.svg", "w") as f:
        f.write(svg)
    cairosvg.svg2png(url="assets/two_doors.svg", write_to="assets/two_doors.png",
                     output_width=1700, output_height=980)
    print("rendered assets/two_doors.png")


if __name__ == "__main__":
    main()
