#!/usr/bin/env python3
"""make_a8_room.py — the eighth room is the sum's, not the seam's.

mina: "the seam reaches A_8... onto-A_8 I could not read.  reaches is not fills."
rahel: "two point-stabilizer A_7's generate A_8, so the sum climbs a rung:
seam#seam -> A_8."

Verified in make_a8_door.py.  The seam's A_7-image, lifted to A_8, is a POINT-
STABILIZER: the seam reaches the eighth room (its image is A_7, order 2520) but
cannot fill it alone.  The connected sum can: two point-stabilizers sharing the
meridian g generate A_8, because the meridian's centralizer holds an element tau
moving the fixed point, so tau conjugates one point-stabilizer to a different one
WITHOUT changing the meridian.

    Conway 11n34:  surjects A_7 @ meridian order 3  ->  seam#seam -> A_8
    KT     11n42:  surjects A_7 @ meridian order 4  ->  seam#seam -> A_8

The mutation difference survives: the eighth room opens at height 3 (Conway) and
height 4 (KT).  And in both cases the seam ALONE stays at A_7 — reaches, not fills.

Two octagons: left, the seam reaches (one A_7, dark); right, the sum fills (two
A_7's, one meridian, the octagon lit).
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


def label(cx, y, text, fill=MUTE, size=17, anchor="middle"):
    return (f'<text x="{cx}" y="{y}" text-anchor="{anchor}" '
            f'font-family="monospace" font-size="{size}" fill="{fill}">{text}</text>')


def build():
    W, H = 1640, 960
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
         f'viewBox="0 0 {W} {H}">']
    s.append("""<defs>
      <filter id="soft" x="-40%" y="-40%" width="180%" height="180%">
        <feGaussianBlur stdDeviation="6"/>
      </filter>
    </defs>""")
    s.append(f'<rect width="{W}" height="{H}" fill="{BG}"/>')
    s.append(label(W / 2, 60, "the eighth room is the sum's, not the seam's", ROSE, 31))
    s.append(label(W / 2, 94,
                   "the seam reaches A₈ (its image is A₇, a point-stabilizer) — "
                   "but two of them, sharing the meridian, fill it",
                   MUTE, 18))

    cxL, cxR = 400, 1240
    cy = 470
    R = 210

    # ============ LEFT: the seam reaches A₈, stays A₇ ============
    s.append(glow_poly(cxL, cy, R, 8, DARK, 3.5, fill=DARK, opacity=0.10))
    # a single A_7 (heptagon) inside — the seam's image, the point-stabilizer
    s.append(glow_poly(cxL, cy, R * 0.72, 7, COPPER, 4.5, rot=-math.pi / 2,
                       fill=COPPER, opacity=0.10))
    # the meridian node (rose) at the heptagon's shared point
    s.append(glow_ring(cxL, cy + R * 0.72, 11, ROSE, 4))
    s.append(label(cxL, cy - R - 44, "the seam reaches", COPPER, 22))
    s.append(label(cxL, cy - R - 14, "A₈  ·  image = A₇", COPPER, 18))
    s.append(label(cxL, cy + R + 56, "one point-stabilizer", MUTE, 16))
    s.append(label(cxL, cy + R + 82, "order 2520, not 20160", MUTE, 16))
    s.append(label(cxL, cy + R + 116, "the eighth room stays dark", DIM, 16))

    # ============ RIGHT: seam#seam fills A₈ ============
    s.append(glow_poly(cxR, cy, R, 8, BRASS, 4, fill=BRASS, opacity=0.14))
    # two point-stabilizers (heptagons) sharing the meridian
    s.append(glow_poly(cxR - 40, cy - 4, R * 0.70, 7, BRASS, 4, rot=-math.pi / 2 + 0.10,
                       fill=BRASS, opacity=0.08))
    s.append(glow_poly(cxR + 40, cy - 4, R * 0.70, 7, COPPER, 4, rot=-math.pi / 2 - 0.10,
                       fill=COPPER, opacity=0.08))
    # the shared meridian (rose) where the two heptagons meet
    s.append(glow_ring(cxR, cy - 4 + R * 0.70, 12, ROSE, 4.5))
    s.append(label(cxR, cy - R - 44, "seam#seam fills", BRASS, 22))
    s.append(label(cxR, cy - R - 14, "two A₇'s, one meridian", BRASS, 18))
    s.append(label(cxR, cy + R + 56, "⟨Stab(7), Stab(0)⟩ = A₈", MUTE, 17))
    s.append(label(cxR, cy + R + 82, "order 20160", MUTE, 16))
    s.append(label(cxR, cy + R + 116, "the eighth room is lit", BRASS, 16))

    # a meridian axis tying the two panels
    s.append(f'<line x1="{cxL + 240}" y1="{cy}" x2="{cxR - 240}" y2="{cy}" '
             f'stroke="{MUTE}" stroke-width="1.5" opacity="0.35" '
             f'stroke-dasharray="5 6"/>')
    s.append(label((cxL + cxR) / 2, cy - 12, "the same meridian,", MUTE, 15))
    s.append(label((cxL + cxR) / 2, cy + 16, "at two heights", MUTE, 15))

    # footer: the mutation difference and the height
    s.append(label(W / 2, H - 96, "the mutation difference survives into the eighth:",
                   BRASS, 18))
    s.append(label(W / 2, H - 68, "Conway 11n34 opens it at height 3   ·   "
                   "KT 11n42 at height 4", COPPER, 18))
    s.append(label(W / 2, H - 40,
                   "the meridian's centralizer is the key — τ moves the fixed point, "
                   "so the second door opens at the same meridian", MUTE, 15))

    s.append("</svg>")
    return "\n".join(s)


def main():
    svg = build()
    with open("assets/a8_room.svg", "w") as f:
        f.write(svg)
    cairosvg.svg2png(url="assets/a8_room.svg", write_to="assets/a8_room.png",
                     output_width=1640, output_height=960)
    print("rendered assets/a8_room.png")


if __name__ == "__main__":
    main()
