#!/usr/bin/env python3
"""make_a8_correct.py — the seam owns the eighth; the sum owns the tenth.

CORRECTION.  make_a8_door.py (last tick) read only ONE door: the seam's
A_7-image lifted to A_8 as a point-stabilizer, which stays A_7 (order 2520) — so
I concluded "the eighth room is the sum's, not the seam's."  That was a partial
read.  The seam ALONE surjects A_8:

  make_a8_search.py finds fixed points of the signed Artin automorphism on A_8^4
  (the seam is a 4-braid) whose image is exactly A_8 (20160).  The meridian is
  (0 1 2)(3 4 5) — TWO 3-cycles on six points, class 3^2 1^2 — not the single
  3-cycle that pins a point and lands in the A_7 wall.

  Conway 11n34:  x1=(0 1 2)(3 4 5)  x2=(2 3 4)(5 6 7)  x3=(0 6 2)(1 3 7)
                 x4=(1 5 7)(2 4 3)   <x1..x4> = |20160| = A_8.  Verified.
  KT     11n42:  x1=(0 1 2)(3 4 5)  x2=(1 3 2)(4 5 6)  x3=(0 1 4)(2 3 7)
                 x4=(0 4 1)(2 7 3)   <x1..x4> = |20160| = A_8.

And the sum climbs a rung further (make_a10_sum.py): pi_1(K#K) = pi_1(K) *_Z
pi_1(K); embed the A_8-surjection in A_10 fixing 8,9, take tau = (6 8)(7 9) in
C_{A_10}(meridian), then phi2 = tau phi1 tau^-1 agrees on the meridian and is a
different A_8.  <A_8, tau A_8 tau^-1> = |1814400| = A_10.

Two panels: left, the seam alone fills A_8 (meridian = two 3-cycles, the doubled
door); right, seam#seam fills A_10 (two A_8's, one meridian).
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


def label(cx, y, text, fill=MUTE, size=17, anchor="middle"):
    return (f'<text x="{cx}" y="{y}" text-anchor="{anchor}" '
            f'font-family="monospace" font-size="{size}" fill="{fill}">{text}</text>')


def build():
    W, H = 1700, 960
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
         f'viewBox="0 0 {W} {H}">']
    s.append("""<defs>
      <filter id="soft" x="-40%" y="-40%" width="180%" height="180%">
        <feGaussianBlur stdDeviation="6"/>
      </filter>
    </defs>""")
    s.append(f'<rect width="{W}" height="{H}" fill="{BG}"/>')
    s.append(label(W / 2, 58, "the seam owns the eighth; the sum owns the tenth", ROSE, 31))
    s.append(label(W / 2, 92,
                   "one 3-cycle pins a point and stops at the wall (A₇, 2520) — "
                   "two 3-cycles on six points pin nothing: A₈, 20160",
                   MUTE, 18))

    cxL, cxR = 430, 1270
    cy = 480
    R = 205

    # ============ LEFT: the seam alone fills A_8 ============
    s.append(glow_poly(cxL, cy, R, 8, BRASS, 4, fill=BRASS, opacity=0.16))
    # the meridian node: two 3-cycles (doubled door) — two small interlocked triangles
    s.append(glow_ring(cxL, cy + R, 13, ROSE, 4.5))
    s.append(tri(cxL - 26, cy + R - 34, 26, ROSE, 2.4, rot=0.0, opacity=0.9))
    s.append(tri(cxL + 26, cy + R - 34, 26, ROSE, 2.4, rot=math.pi, opacity=0.9))
    s.append(label(cxL, cy - R - 46, "seam alone fills", BRASS, 22))
    s.append(label(cxL, cy - R - 16, "the meridian two 3-cycles", BRASS, 18))
    s.append(label(cxL, cy + R + 56, "⟨a,b,c⟩ = A₈", MUTE, 17))
    s.append(label(cxL, cy + R + 82, "order 20160, not 2520", MUTE, 16))
    s.append(label(cxL, cy + R + 116, "the eighth room is the seam's", BRASS, 16))

    # ============ RIGHT: seam#seam fills A_10 ============
    s.append(glow_poly(cxR, cy, R + 34, 10, COPPER, 4, fill=COPPER, opacity=0.14))
    # two A_8's (octagons) sharing one meridian
    s.append(glow_poly(cxR - 44, cy - 6, R * 0.74, 8, BRASS, 4, rot=0.14,
                       fill=BRASS, opacity=0.08))
    s.append(glow_poly(cxR + 44, cy - 6, R * 0.74, 8, BRASS, 4, rot=-0.14,
                       fill=BRASS, opacity=0.08))
    s.append(glow_ring(cxR, cy - 6 + R * 0.74, 12, ROSE, 4.5))
    s.append(label(cxR, cy - R - 46, "seam#seam climbs", COPPER, 22))
    s.append(label(cxR, cy - R - 16, "two A₈'s, one meridian", COPPER, 18))
    s.append(label(cxR, cy + R + 56, "⟨A₈, τ A₈ τ⁻¹⟩ = A₁₀", MUTE, 17))
    s.append(label(cxR, cy + R + 82, "order 1814400", MUTE, 16))
    s.append(label(cxR, cy + R + 116, "the tenth room is the sum's", COPPER, 16))

    # meridian axis tying the two panels
    s.append(f'<line x1="{cxL + 240}" y1="{cy}" x2="{cxR - 250}" y2="{cy}" '
             f'stroke="{MUTE}" stroke-width="1.5" opacity="0.35" '
             f'stroke-dasharray="5 6"/>')
    s.append(label((cxL + cxR) / 2, cy - 12, "the door is the meridian's,", MUTE, 15))
    s.append(label((cxL + cxR) / 2, cy + 16, "not the sweep's", MUTE, 15))

    # footer: the correction and the open rung
    s.append(label(W / 2, H - 96, "the reach/fill split was the wrong door: "
                   "I read only the single 3-cycle that pins a point", DIM, 17))
    s.append(label(W / 2, H - 68, "Conway 11n34 and KT 11n42 both fill A₈ — "
                   "the seam's second door", MUTE, 16))
    s.append(label(W / 2, H - 40,
                   "whether the seam alone opens A₉, and how far the sum climbs, "
                   "is still open", MUTE, 15))

    s.append("</svg>")
    return "\n".join(s)


def main():
    svg = build()
    with open("assets/a8_correct.svg", "w") as f:
        f.write(svg)
    cairosvg.svg2png(url="assets/a8_correct.svg", write_to="assets/a8_correct.png",
                     output_width=1700, output_height=960)
    print("rendered assets/a8_correct.png")


if __name__ == "__main__":
    main()
