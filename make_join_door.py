#!/usr/bin/env python3
"""make_join_door.py — the sign is not the door; the join is.

The door of K#K is the JOIN-CLOSURE of the door-set of K: a hom of the connected
sum is two independent homs, and its image is ⟨im φ₁, im φ₂⟩.  So a new door opens
by self-sum iff two images of K generate a room that no single image reaches.

The sign lock (sgn x₁ = sgn x₂) is orthogonal to this.  Verified in S₅ (|G|=120):

    trefoil#trefoil:  A₅ (even) + S₄ (odd)  → S₅   0 → 187920   the sign BREAKS
    fig-8#fig-8:      A₄ + D₅ (both even)   → A₅   0 →  78120   the sign KEEPS
    seam#seam:        A₅ + A₅ (perfect)     → A₅   0 → 0        lock-tight (Δ=1)

The seam is lock-tight because Δ=1 ⟹ every non-abelian image is perfect, so its
images are confined to the perfect part of the lens (in S₅, the room A₅); the join
cannot escape it.  The trefoil and the fig-8 have images in more than one room, so
their join can be a room neither alone reaches.

Run:  python3 make_join_door.py   (renders assets/join_door.png)
"""
import math

import cairosvg

BG = "#08080d"
BRASS = "#d9a84f"
COPPER = "#c47b5a"
ROSE = "#c96767"
DIM = "#4a3f4a"
HOUSE_DARK = "#3a2833"
HOUSE_LIT = "#6a3540"


def poly(cx, cy, r, n, rot=0.0):
    return [(cx + r * math.cos(rot + 2 * math.pi * k / n),
             cy + r * math.sin(rot + 2 * math.pi * k / n)) for k in range(n)]


def pts(p):
    return " ".join(f"{x:.1f},{y:.1f}" for x, y in p)


def house(cx, cy, w, h, roof=0.55):
    hw, hh = w / 2, h / 2
    apex = (cx, cy - hh - roof * hh)
    roofL = (cx - hw, cy - hh)
    roofR = (cx + hw, cy - hh)
    botL = (cx - hw, cy + hh)
    botR = (cx + hw, cy + hh)
    return [apex, roofL, botL, botR, roofR]


def glow_stroke(x1, y1, x2, y2, color, width, blur=0.6):
    return f"""
  <line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}"
        stroke="{color}" stroke-width="{width*3}" stroke-linecap="round"
        opacity="0.18" filter="url(#soft)"/>
  <line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}"
        stroke="{color}" stroke-width="{width}" stroke-linecap="round"/>"""


def glow_path(d, color, width):
    return f"""
  <path d="{d}" fill="none" stroke="{color}" stroke-width="{width*3}"
        stroke-linecap="round" opacity="0.16" filter="url(#soft)"/>
  <path d="{d}" fill="none" stroke="{color}" stroke-width="{width}"
        stroke-linecap="round"/>"""


def glowing_poly(cx, cy, r, n, color, width, rot=0.0, fill=None, opacity=None):
    p = poly(cx, cy, r, n, rot)
    fill_attr = f'fill="{fill}"' if fill else 'fill="none"'
    op_attr = f' opacity="{opacity}"' if opacity else ""
    return f"""
  <polygon points="{pts(p)}" {fill_attr} stroke="{color}" stroke-width="{width*3}"
        stroke-linejoin="round" opacity="0.20" filter="url(#soft)"/>
  <polygon points="{pts(p)}" fill="none" stroke="{color}" stroke-width="{width}"
        stroke-linejoin="round"{op_attr}/>"""


def dashed_poly(cx, cy, r, n, color, width, rot=0.0):
    p = poly(cx, cy, r, n, rot)
    return f"""
  <polygon points="{pts(p)}" fill="none" stroke="{color}" stroke-width="{width}"
        stroke-linejoin="round" stroke-dasharray="6 6" opacity="0.55"/>"""


def house_outline(cx, cy, w, h, color, width, fill=None, opacity=None):
    p = house(cx, cy, w, h)
    fill_attr = f'fill="{fill}"' if fill else 'fill="none"'
    op_attr = f' opacity="{opacity}"' if opacity else ""
    return f"""
  <polygon points="{pts(p)}" {fill_attr} stroke="{color}" stroke-width="{width*3}"
        stroke-linejoin="round" opacity="0.18" filter="url(#soft)"/>
  <polygon points="{pts(p)}" fill="none" stroke="{color}" stroke-width="{width}"
        stroke-linejoin="round"{op_attr}/>"""


def label(cx, y, text, fill=DIM, size=17, anchor="middle"):
    return f'<text x="{cx}" y="{y}" text-anchor="{anchor}" font-family="monospace" font-size="{size}" fill="{fill}">{text}</text>'


def build():
    W, H = 1500, 940
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">']
    s.append(f"""<defs>
      <filter id="soft" x="-40%" y="-40%" width="180%" height="180%">
        <feGaussianBlur stdDeviation="5"/>
      </filter>
    </defs>""")
    s.append(f'<rect width="{W}" height="{H}" fill="{BG}"/>')

    # title
    s.append(label(W / 2, 62, "the sign is not the door", BRASS, 30))
    s.append(label(W / 2, 96, "the door of K#K is ⟨door, door⟩ — the join-closure of the door-set of K", DIM, 18))

    # panel dividers
    for x in (W / 3, 2 * W / 3):
        s.append(glow_stroke(x, 150, x, H - 170, DIM, 1.5))

    centers = [W / 6, W / 2, 5 * W / 6]

    # ============ PANEL 1: trefoil#trefoil → S₅ (sign breaks) ============
    cx = centers[0]
    # the house (S₅) in shadow, then lit by the join
    s.append(house_outline(cx, 500, 320, 250, HOUSE_DARK, 3))
    s.append(house_outline(cx, 500, 304, 234, HOUSE_LIT, 3, fill=HOUSE_LIT, opacity=0.24))
    # doors: A₅ (even, brass pentagon) and S₄ (odd, copper square)
    s.append(glowing_poly(cx - 120, 690, 52, 5, BRASS, 4))
    s.append(glowing_poly(cx + 120, 690, 48, 4, COPPER, 4, math.pi / 4))
    s.append(label(cx - 120, 768, "A₅", BRASS, 17))
    s.append(label(cx + 120, 768, "S₄", COPPER, 17))
    # two arcs (different signs: brass + copper) converge inside the house
    s.append(glow_path(f"M {cx-120:.0f} 690 C {cx-130:.0f} 570, {cx-40:.0f} 540, {cx:.0f} 500", BRASS, 5))
    s.append(glow_path(f"M {cx+120:.0f} 690 C {cx+130:.0f} 570, {cx+40:.0f} 540, {cx:.0f} 500", COPPER, 5))
    s.append(f'<circle cx="{cx:.0f}" cy="500" r="12" fill="{ROSE}"/>')
    s.append(label(cx, 415, "S₅", ROSE, 22))
    s.append(label(cx, 808, "the sign breaks:", ROSE, 16))
    s.append(label(cx, 836, "A₅ (even) + S₄ (odd) → S₅", ROSE, 16))
    s.append(label(cx, 866, "0 → 187920 onto S₅", DIM, 15))

    # ============ PANEL 2: fig-8#fig-8 → A₅ (sign kept) ============
    cx = centers[1]
    s.append(house_outline(cx, 500, 320, 250, HOUSE_DARK, 3))
    # doors: A₄ (brass triangle) and D₅ (brass pentagon) — BOTH even
    s.append(glowing_poly(cx - 120, 690, 50, 3, BRASS, 4, math.pi / 2))  # A4
    s.append(glowing_poly(cx + 120, 690, 48, 5, BRASS, 4))                # D5
    s.append(label(cx - 120, 768, "A₄", BRASS, 17))
    s.append(label(cx + 120, 768, "D₅", BRASS, 17))
    # two arcs (both brass = sign kept) converge and LIGHT the pentagon
    s.append(glow_path(f"M {cx-120:.0f} 690 C {cx-130:.0f} 570, {cx-40:.0f} 540, {cx:.0f} 500", BRASS, 5))
    s.append(glow_path(f"M {cx+120:.0f} 690 C {cx+130:.0f} 570, {cx+40:.0f} 540, {cx:.0f} 500", BRASS, 5))
    s.append(glowing_poly(cx, 500, 62, 5, BRASS, 4, fill="#d9a84f", opacity=0.16))
    s.append(f'<circle cx="{cx:.0f}" cy="500" r="12" fill="{BRASS}"/>')
    s.append(label(cx, 415, "A₅", BRASS, 22))
    s.append(label(cx, 808, "the sign kept:", BRASS, 16))
    s.append(label(cx, 836, "A₄ + D₅ (both even) → A₅", BRASS, 16))
    s.append(label(cx, 866, "0 → 78120 · blind alone", DIM, 15))

    # ============ PANEL 3: seam#seam → A₅ (lock-tight) ============
    cx = centers[2]
    s.append(house_outline(cx, 500, 320, 250, HOUSE_DARK, 3))
    # the seam's only non-abelian image in S₅ is A₅; its join returns to A₅
    s.append(glowing_poly(cx, 690, 52, 5, BRASS, 4))
    s.append(label(cx, 768, "A₅ (perfect)", BRASS, 16))
    s.append(glow_path(f"M {cx-56:.0f} 690 C {cx-66:.0f} 570, {cx-20:.0f} 540, {cx:.0f} 500", BRASS, 4))
    s.append(glow_path(f"M {cx+56:.0f} 690 C {cx+66:.0f} 570, {cx+20:.0f} 540, {cx:.0f} 500", BRASS, 4))
    s.append(f'<circle cx="{cx:.0f}" cy="500" r="9" fill="{DIM}"/>')
    s.append(label(cx, 415, "A₅", DIM, 22))
    s.append(label(cx, 808, "lock-tight:", DIM, 16))
    s.append(label(cx, 836, "A₅ + A₅ → A₅, unchanged", DIM, 16))
    s.append(label(cx, 866, "Δ=1: every image perfect", DIM, 15))

    # footer law
    s.append(label(W / 2, H - 52, "a knot opens a new door by self-sum iff two of its images generate a room no single image reaches", BRASS, 17))
    s.append(label(W / 2, H - 24, "|Hom(K#K, S₅)| = |Hom(K, S₅)|²   ·   the count squares, the room joins", DIM, 15))

    s.append("</svg>")
    return "\n".join(s)


def main():
    svg = build()
    with open("assets/join_door.svg", "w") as f:
        f.write(svg)
    cairosvg.svg2png(url="assets/join_door.svg", write_to="assets/join_door.png",
                     output_width=1500, output_height=940)
    print("rendered assets/join_door.png")


if __name__ == "__main__":
    main()
