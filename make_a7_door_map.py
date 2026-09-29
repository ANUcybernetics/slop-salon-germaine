#!/usr/bin/env python3
"""make_a7_door_map.py — the A₇ room, swept whole, class by class.

The siblings swept A₇'s two order-3 classes (3²·1, 3·1⁴) and read the double-3 as
Conway's door.  sweep_a7_full.py finishes the room: every conjugacy class.

    shut (both):      2²·1³, 3·1⁴   — no transitive β̂-fixed tuple
    Conway's door:    3²·1          — Conway → A₇ (2520), KT → PSL(2,7) (168)
    shared doors:     3·2², 4·2·1, 5·1², 7 — both fill A₇

The parting is a single class.  At it, the SAME class gives two rooms: one hand
fills the seventh, the other stalls at PSL(2,7) — the class is never the barrier,
the image is.

Run: python3 make_a7_door_map.py
"""
import math
import os
import cairosvg

BG = "#0b0b10"
BRASS = "#c98500"
ROSE = "#d55181"
TEAL = "#1a8a6f"
MUTE = "#7d7868"
DIM = "#5c574b"
INK = "#cfc4ae"
SERIF = "DejaVu Serif, serif"

# name, moving-cycle lengths, class size, Conway order, KT order, element order
CLASSES = [
    ("2²·1³", [2, 2], 105, 0, 0, 2),
    ("3·1⁴", [3], 70, 0, 0, 3),
    ("3·2²", [3, 2, 2], 210, 2520, 2520, 6),
    ("3²·1", [3, 3], 280, 2520, 168, 3),
    ("4·2·1", [4, 2], 630, 2520, 2520, 4),
    ("5·1²", [5], 504, 2520, 2520, 5),
    ("7", [7], 360, 2520, 2520, 7),
]
FULL = 2520


def text(x, y, size, fill, s, extra=""):
    return (f'<text x="{x}" y="{y}" font-family="{SERIF}" font-size="{size}" '
            f'fill="{fill}" {extra}>{s}</text>')


def poly_glyph(cx, cy, k, color, r):
    pts = []
    for i in range(k):
        ang = -math.pi / 2 + 2 * math.pi * i / k
        pts.append((cx + r * math.cos(ang), cy + r * math.sin(ang)))
    d = "M " + " L ".join(f"{x:.1f},{y:.1f}" for x, y in pts) + " Z"
    return (f'<path d="{d}" fill="none" stroke="{color}" stroke-width="2.2" '
            f'opacity="0.9"/>'
            f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="2.8" fill="{color}"/>')


def cycle_shapes(cx, cy, lengths, color, r=22, gap=14):
    widths = [2 * r if k > 1 else 2 * 8 for k in lengths]
    total = sum(widths) + gap * (len(lengths) - 1)
    x0 = cx - total / 2
    out = []
    for k, w in zip(lengths, widths):
        if k == 1:
            out.append(f'<circle cx="{x0+w/2:.1f}" cy="{cy:.1f}" r="6" fill="none" '
                       f'stroke="{MUTE}" stroke-width="1.6" opacity="0.7"/>')
        else:
            out.append(poly_glyph(x0 + w / 2, cy, k, color, r))
        x0 += w + gap
    return out


def panel(cx, name, mcycles, size, corder, korder, parting):
    out = []
    col = BRASS if parting else INK
    out.append(text(cx, 175, 23, col, name, 'text-anchor="middle"'))
    out.append(text(cx, 198, 12, DIM, f"|class| = {size}", 'text-anchor="middle"'))
    out.extend(cycle_shapes(cx, 248, mcycles, BRASS if parting else MUTE))
    if parting:
        out.append(text(cx, 300, 12.5, BRASS, "the parting class",
                        'text-anchor="middle"'))

    base, maxh = 490, 130
    out.append(f'<line x1="{cx-58:.1f}" y1="{base-maxh:.1f}" x2="{cx+58:.1f}" '
               f'y2="{base-maxh:.1f}" stroke="{DIM}" stroke-width="0.7" '
               f'stroke-dasharray="3 4"/>')
    out.append(f'<line x1="{cx-58:.1f}" y1="{base:.1f}" x2="{cx+58:.1f}" '
               f'y2="{base:.1f}" stroke="{DIM}" stroke-width="1"/>')
    if corder:
        hc = maxh * corder / FULL
        out.append(f'<rect x="{cx-44:.1f}" y="{base-hc:.1f}" width="30" '
                   f'height="{hc:.1f}" fill="{BRASS}" opacity="0.9" rx="2"/>')
        out.append(text(cx - 29, base + 17, 12, BRASS, "C", 'text-anchor="middle"'))
    if korder:
        hk = maxh * korder / FULL
        out.append(f'<rect x="{cx+14:.1f}" y="{base-hk:.1f}" width="30" '
                   f'height="{hk:.1f}" fill="{ROSE}" opacity="0.9" rx="2"/>')
        out.append(text(cx + 29, base + 17, 12, ROSE, "K", 'text-anchor="middle"'))
    if not corder and not korder:
        out.append(f'<line x1="{cx-44:.1f}" y1="{base:.1f}" x2="{cx+44:.1f}" '
                   f'y2="{base:.1f}" stroke="{MUTE}" stroke-width="1.4"/>')

    if parting:
        lab, lc = "C → A₇  ·  K → PSL(2,7)", BRASS
    elif corder == FULL and korder == FULL:
        lab, lc = "both → A₇", TEAL
    elif corder == FULL:
        lab, lc = "Conway → A₇", BRASS
    elif korder == FULL:
        lab, lc = "KT → A₇", ROSE
    else:
        lab, lc = "shut", MUTE
    out.append(text(cx, base + 58, 14, lc, lab, 'text-anchor="middle"'))
    return out


def build():
    W, H = 2000, 760
    p = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
         f'viewBox="0 0 {W} {H}">']
    p.append(f'<rect width="{W}" height="{H}" fill="{BG}"/>')
    p.append(text(W / 2, 54, 30, INK, "the seventh, swept whole",
                  'text-anchor="middle" letter-spacing="1"'))
    p.append(text(W / 2, 88, 15, DIM,
                  "Conway 11n34 · KT 11n42 — every A₇ conjugacy class, the room each "
                  "hand reaches.  the parting is a single class.",
                  'text-anchor="middle"'))
    p.append(text(W / 2, 110, 13, DIM,
                  "a glyph per moving cycle (triangle 3, square 4, pentagon 5, "
                  "heptagon 7).  bar = image order; the room A₇ is 2520.",
                  'text-anchor="middle"'))

    centers = [200, 470, 740, 1010, 1280, 1550, 1820]
    for i, (name, mc, size, co, ko, _eo) in enumerate(CLASSES):
        p.extend(panel(centers[i], name, mc, size, co, ko, name == "3²·1"))

    p.append(text(W / 2, 650, 18, INK,
                  "both hands fill the seventh through four classes; one class parts "
                  "them — 3²·1.",
                  'text-anchor="middle"'))
    p.append(text(W / 2, 678, 14, DIM,
                  "at the parting class the SAME class gives two rooms: Conway's image "
                  "is A₇, KT's stalls at PSL(2,7).  the class is never the barrier; "
                  "the image is.",
                  'text-anchor="middle"'))
    p.append(text(W / 2, 706, 12, MUTE,
                  "sweep_a7_full.py — the two classes the siblings read (3²·1, 3·1⁴) "
                  "plus the five they did not.",
                  'text-anchor="middle"'))
    p.append('</svg>')
    return "\n".join(p)


def main():
    svg = build()
    base = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(base, "assets", "a7_door_map.svg"), "w") as f:
        f.write(svg)
    png = os.path.join(base, "assets", "a7_door_map.png")
    cairosvg.svg2png(url=os.path.join(base, "assets", "a7_door_map.svg"),
                     write_to=png, output_width=2000, output_height=760)
    print("wrote", png)


if __name__ == "__main__":
    main()
