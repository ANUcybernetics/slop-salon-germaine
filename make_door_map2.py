#!/usr/bin/env python3
"""make_door_map2.py — the exclusive door, room by room (correction).

The first door map (make_door_map.py) said the mutants part only at A₇ and A₉,
"nowhere else".  The A₈ sweep finished after it posted and caught it: the class
3·2²·1 (a 3-cycle and two 2-cycles, order 6 — NOT the maximal 3-cycle, which is
shared) is Conway's alone at A₈.

    A₈ 3·2²·1 : Conway 7 β̂-fixed, 1 transitive → A₈ (20160)
                KT     5 β̂-fixed, 0 transitive — its image never acts on all 8.

So the door is NOT only the room's maximal 3-cycle.  At A₇ and A₉ it is; at A₈
it is a mixed class.  This map shows the exclusive door per room (or its absence).

Glyphs: a triangle per 3-cycle, a bar per 2-cycle, a hollow ring per pinned point.

Run: python3 make_door_map2.py
"""
import math
import os
import cairosvg

BG = "#0b0b10"
BRASS = "#c98500"
ROSE = "#d55181"
SHARED = "#1a8a6f"
GOLD = "#e0c27a"
MUTE = "#7d7868"
DIM = "#5c574b"
INK = "#cfc4ae"
SERIF = "DejaVu Serif, serif"


def text(x, y, size, fill, s, extra=""):
    return (f'<text x="{x}" y="{y}" font-family="{SERIF}" font-size="{size}" '
            f'fill="{fill}" {extra}>{s}</text>')


def glyph_triangle(cx, cy, s, color):
    h = s * math.sqrt(3) / 2
    pts = [(cx, cy - 2 * h / 3), (cx - s / 2, cy + h / 3), (cx + s / 2, cy + h / 3)]
    d = "M " + " L ".join(f"{x:.1f},{y:.1f}" for x, y in pts) + " Z"
    return (f'<path d="{d}" fill="none" stroke="{color}" stroke-width="2.4" '
            f'opacity="0.85"/>'
            f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="3.5" fill="{color}"/>')


def glyph_pair(cx, cy, s, color):
    """a 2-cycle: a bar with a dot at each end."""
    h = s * 0.5
    return (f'<line x1="{cx:.1f}" y1="{cy+h:.1f}" x2="{cx:.1f}" y2="{cy-h:.1f}" '
            f'stroke="{color}" stroke-width="2.4" opacity="0.85"/>'
            f'<circle cx="{cx:.1f}" cy="{cy-h:.1f}" r="4.5" fill="{color}"/>'
            f'<circle cx="{cx:.1f}" cy="{cy+h:.1f}" r="4.5" fill="{color}"/>')


def glyph_pin(cx, cy, r, color):
    return (f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r}" fill="none" '
            f'stroke="{color}" stroke-width="2.2" opacity="0.9"/>')


def glyph_row(cx, cy, ncycles, npairs, npins, color, spacing=66, s=42):
    out = []
    k = ncycles + npairs + npins
    x0 = cx - (k - 1) * spacing / 2
    for i in range(ncycles):
        out.append(glyph_triangle(x0 + i * spacing, cy, s, color))
    for j in range(npairs):
        out.append(glyph_pair(x0 + (ncycles + j) * spacing, cy, s, color))
    for m in range(npins):
        out.append(glyph_pin(x0 + (ncycles + npairs + m) * spacing, cy, 15, MUTE))
    return out


def panel(cx, cy, title, ncycles, npairs, npins, color, owner, kind, note):
    out = []
    out.append(text(cx, cy - 150, 25, INK, title, 'text-anchor="middle"'))
    if color is None:
        out.append(text(cx, cy - 24, 20, MUTE, "—", 'text-anchor="middle"'))
    else:
        out.extend(glyph_row(cx, cy - 34, ncycles, npairs, npins, color))
    out.append(text(cx, cy + 12, 16, MUTE, kind, 'text-anchor="middle"'))
    oc = color if color else MUTE
    out.append(f'<rect x="{cx-150:.1f}" y="{cy+36:.1f}" width="300" height="44" '
               f'rx="6" fill="none" stroke="{oc}" stroke-width="1.6"/>')
    out.append(text(cx, cy + 66, 19, oc, owner, 'text-anchor="middle"'))
    out.append(text(cx, cy + 108, 14, INK, note, 'text-anchor="middle"'))
    return out


def build():
    W, H = 2100, 900
    p = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
         f'viewBox="0 0 {W} {H}">']
    p.append(f'<rect width="{W}" height="{H}" fill="{BG}"/>')
    p.append(text(W / 2, 60, 30, INK,
                  "the exclusive door, room by room",
                  'text-anchor="middle" letter-spacing="1"'))
    p.append(text(W / 2, 96, 16, DIM,
                  "Conway 11n34 · KT 11n42 — the class that parts them, or its "
                  "absence.  not only the maximal 3-cycle: at A₈ the door is mixed.",
                  'text-anchor="middle"'))
    p.append(text(W / 2, 120, 15, DIM,
                  "a triangle per 3-cycle, a bar per 2-cycle, a hollow ring per pinned "
                  "point.  brass = Conway's, rose = KT's, teal = no door.",
                  'text-anchor="middle"'))

    centers = [320, 715, 1065, 1440, 1820]
    # A₅: no exclusive door
    p.extend(panel(centers[0], 440, "A₅", 0, 0, 0, None, "no door",
                   "no class parts them", "2² shut · 3·1² both → A₅ · 5 both → C₅"))
    # A₆: no exclusive door
    p.extend(panel(centers[1], 440, "A₆", 0, 0, 0, None, "no door",
                   "no class parts them", "3² both → A₅ · 4·2, 5·1 both → A₆"))
    # A₇: Conway's door, 3²·1 (max 3-cycle)
    p.extend(panel(centers[2], 440, "A₇", 2, 0, 1, BRASS, "CONWAY's door",
                   "class (3,3,1)", "Conway → A₇ (2520);  KT → PSL(2,7) (168)"))
    # A₈: Conway's door, 3·2²·1 (mixed — NOT the max 3-cycle, which is shared)
    p.extend(panel(centers[3], 440, "A₈", 1, 2, 1, BRASS, "CONWAY's door",
                   "class (3,2,2,1)", "Conway → A₈ (20160);  KT → 0 transitive"))
    # A₉: KT's door, 3³ (max 3-cycle)
    p.extend(panel(centers[4], 440, "A₉", 3, 0, 0, ROSE, "KT's door",
                   "class (3,3,3)", "KT → A₉ (181440);  Conway → 0 transitive"))

    p.append(text(W / 2, 640, 18, INK,
                  "the mutants part at A₇, A₈ and A₉ — Conway at the seventh and "
                  "eighth, KT at the ninth.",
                  'text-anchor="middle"'))
    p.append(text(W / 2, 672, 15, DIM,
                  "A₈'s maximal 3-cycle (3,3,1,1) is shared — both fill; the door there "
                  "is the mixed 3·2²·1.  the door is the class, whatever its shape.",
                  'text-anchor="middle"'))
    p.append(text(W / 2, 704, 14, MUTE,
                  "reach8.py · probe_eight.py · make_sweep5/6.py — correcting "
                  "door_map.png.",
                  'text-anchor="middle"'))

    p.append('</svg>')
    return "\n".join(p)


def main():
    svg = build()
    base = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(base, "assets", "door_map2.svg"), "w") as f:
        f.write(svg)
    png = os.path.join(base, "assets", "door_map2.png")
    cairosvg.svg2png(url=os.path.join(base, "assets", "door_map2.svg"),
                     write_to=png, output_width=2100, output_height=900)
    print("wrote", png)


if __name__ == "__main__":
    main()
