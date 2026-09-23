#!/usr/bin/env python3
"""make_sign_lock.py — the connected sum breaks the sign lock.

The trefoil in S₅ is "sign-locked": in a single hom  φ: B₃ → S₅  the two braid
generators share a sign, so the image is either wholly even (inside A₅) or
odd-bearing (a solvable subgroup) — it can never be both, so it can never be the
whole S₅.  0 surjections.

The connected sum K#K has knot group the FREE PRODUCT, so a hom is TWO independent
homs.  One factor can be even (image A₅), the other odd-bearing (image S₄).  Their
JOIN  ⟨A₅, S₄⟩ = S₅.  The house opens.

The count is blind to this (|Hom|=600, no S₅); the free product's two keys see it.

Run:  python3 make_sign_lock.py   (renders assets/sign_lock.png)
"""
import math

import cairosvg

BG = "#08080d"
BRASS = "#d9a84f"
COPPER = "#c47b5a"
ROSE = "#c96767"
DIM = "#4a3f4a"
HOUSE_DARK = "#5a3a44"
HOUSE_LIT = "#9a4a54"


def poly(cx, cy, r, n, rot=0.0):
    return [(cx + r * math.cos(rot + 2 * math.pi * k / n),
             cy + r * math.sin(rot + 2 * math.pi * k / n)) for k in range(n)]


def pts(p):
    return " ".join(f"{x:.1f},{y:.1f}" for x, y in p)


def house(cx, cy, w, h, roof=0.55):
    """A simple house outline (S₅): roof + walls."""
    hw, hh = w / 2, h / 2
    apex = (cx, cy - hh - roof * hh)
    roofL = (cx - hw, cy - hh)
    roofR = (cx + hw, cy - hh)
    botL = (cx - hw, cy + hh)
    botR = (cx + hw, cy + hh)
    return [apex, roofL, botL, botR, roofR]


def glow_stroke(x1, y1, x2, y2, color, width, blur=0.6):
    """A glowing straight stroke (two passes + a soft shadow)."""
    return f"""
  <line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}"
        stroke="{color}" stroke-width="{width*3}" stroke-linecap="round"
        opacity="0.18" filter="url(#soft)"/>
  <line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}"
        stroke="{color}" stroke-width="{width}" stroke-linecap="round"/>"""


def glowing_poly(cx, cy, r, n, color, width, rot=0.0):
    p = poly(cx, cy, r, n, rot)
    return f"""
  <polygon points="{pts(p)}" fill="none" stroke="{color}" stroke-width="{width*3}"
        stroke-linejoin="round" opacity="0.20" filter="url(#soft)"/>
  <polygon points="{pts(p)}" fill="none" stroke="{color}" stroke-width="{width}"
        stroke-linejoin="round"/>"""


def house_outline(cx, cy, w, h, color, width):
    p = house(cx, cy, w, h)
    return f"""
  <polygon points="{pts(p)}" fill="none" stroke="{color}" stroke-width="{width*3}"
        stroke-linejoin="round" opacity="0.18" filter="url(#soft)"/>
  <polygon points="{pts(p)}" fill="none" stroke="{color}" stroke-width="{width}"
        stroke-linejoin="round"/>"""


def panel_caption(cx, y, lines, fill="#8f8f9a"):
    t = ""
    for i, ln in enumerate(lines):
        t += f'<text x="{cx}" y="{y + i*30}" text-anchor="middle" font-family="monospace" font-size="21" fill="{fill}">{ln}</text>'
    return t


def build():
    W, H = 1480, 900
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">']
    s.append(f"""<defs>
      <filter id="soft" x="-40%" y="-40%" width="180%" height="180%">
        <feGaussianBlur stdDeviation="5"/>
      </filter>
    </defs>""")
    s.append(f'<rect width="{W}" height="{H}" fill="{BG}"/>')

    # titles
    s.append(f'<text x="{W/2}" y="70" text-anchor="middle" font-family="monospace" font-size="30" fill="{BRASS}">the sign lock, and its breaking</text>')
    s.append(f'<text x="{W/2}" y="104" text-anchor="middle" font-family="monospace" font-size="19" fill="{DIM}">trefoil in S₅ — one hom, one sign; the connected sum is two</text>')

    # vertical divider
    s.append(glow_stroke(W / 2, 150, W / 2, H - 150, DIM, 1.5))

    # ---------- LEFT: single trefoil (one hom) ----------
    cxL = W * 0.27
    houseL = house_outline(cxL, 430, 360, 300, HOUSE_DARK, 3)
    s.append(houseL)

    # the house interior stays dark; the two doors in front
    s.append(glowing_poly(cxL - 70, 560, 52, 5, BRASS, 4))          # A5 pentagon
    s.append(glowing_poly(cxL + 70, 560, 48, 4, COPPER, 4, math.pi/4))  # S4 square
    # S4 square is closed by a sign bar
    s.append(glow_stroke(cxL + 34, 524, cxL + 106, 524, COPPER, 6))
    s.append(glow_stroke(cxL + 34, 596, cxL + 106, 596, COPPER, 6))

    # one strand threads the pentagon (even) and rises, blocked before the house
    s.append(f'<path d="M {cxL-200:.0f} 560 C {cxL-130:.0f} 600, {cxL-90:.0f} 540, {cxL-70:.0f} 560'
             f' C {cxL-50:.0f} 580, {cxL-55:.0f} 450, {cxL-40:.0f} 415" fill="none" '
             f'stroke="{BRASS}" stroke-width="5" stroke-linecap="round"/>')
    s.append(f'<circle cx="{cxL-40:.0f}" cy="415" r="6" fill="{BRASS}"/>')
    # a copper lock bar across the strand's path, with the unreachable-house mark
    s.append(glow_stroke(cxL - 78, 400, cxL - 2, 400, COPPER, 5))
    s.append(f'<text x="{cxL}" y="408" text-anchor="middle" font-family="monospace" font-size="26" fill="{ROSE}">✕</text>')
    s.append(f'<text x="{cxL}" y="330" text-anchor="middle" font-family="monospace" font-size="18" fill="{DIM}">S₅</text>')

    s.append(panel_caption(cxL, 700, ["one hom, one sign:", "even, or odd — never both.", "the house stays dark. 0 surjections."], ROSE))

    # ---------- RIGHT: connected sum (two independent homs) ----------
    cxR = W * 0.73
    houseR = house_outline(cxR, 430, 360, 300, HOUSE_LIT, 3)
    s.append(houseR)
    # lit interior
    s.append(f'<polygon points="{pts(house(cxR, 430, 340, 280))}" fill="{HOUSE_LIT}" opacity="0.22" filter="url(#soft)"/>')

    s.append(glowing_poly(cxR - 70, 560, 52, 5, BRASS, 4))          # A5
    s.append(glowing_poly(cxR + 70, 560, 48, 4, COPPER, 4, math.pi/4))  # S4
    # two strands: one even (pentagon), one odd (square), converging inside
    s.append(f'<path d="M {cxR-200:.0f} 560 C {cxR-130:.0f} 600, {cxR-90:.0f} 540, {cxR-70:.0f} 560'
             f' C {cxR-50:.0f} 580, {cxR-55:.0f} 430, {cxR} 400" fill="none" '
             f'stroke="{BRASS}" stroke-width="5" stroke-linecap="round"/>')
    s.append(f'<path d="M {cxR+200:.0f} 560 C {cxR+130:.0f} 600, {cxR+90:.0f} 540, {cxR+70:.0f} 560'
             f' C {cxR+50:.0f} 580, {cxR+55:.0f} 430, {cxR} 400" fill="none" '
             f'stroke="{COPPER}" stroke-width="5" stroke-linecap="round"/>')
    s.append(f'<circle cx="{cxR}" cy="400" r="8" fill="{ROSE}"/>')

    s.append(f'<text x="{cxR}" y="330" text-anchor="middle" font-family="monospace" font-size="18" fill="{ROSE}">S₅</text>')
    s.append(panel_caption(cxR, 700, ["the connected sum — two homs.", "one even (A₅), one odd (S₄).", "⟨A₅, S₄⟩ = S₅: the house opens."], BRASS))

    # footer
    s.append(f'<text x="{W/2}" y="{H-40}" text-anchor="middle" font-family="monospace" font-size="18" fill="{DIM}">|Hom(trefoil, S₅)| = 600, no S₅ · |Hom(trefoil#trefoil, S₅)| = 600², S₅ joins the reach</text>')

    s.append("</svg>")
    return "\n".join(s)


def main():
    svg = build()
    with open("assets/sign_lock.svg", "w") as f:
        f.write(svg)
    cairosvg.svg2png(url="assets/sign_lock.svg", write_to="assets/sign_lock.png",
                     output_width=1480, output_height=900)
    print("rendered assets/sign_lock.png")


if __name__ == "__main__":
    main()
