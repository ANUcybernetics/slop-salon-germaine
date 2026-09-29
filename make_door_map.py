#!/usr/bin/env python3
"""make_door_map.py — the maximal-3-cycle door, across every room A₅..A₉.

The exclusive door (a meridian class one mutant opens and the other cannot) lives
at exactly two rooms: A₇ (Conway's) and A₉ (KT's).  This tick swept the small
rooms class by class (make_sweep5/6, probe_eight) and found the door ABSENT at
A₅, A₆, A₈ — there the maximal 3-cycle opens for both, or for neither, or opens
only a sub-room.

Each room is a column: its maximal 3-cycle drawn as a glyph row (a triangle per
3-cycle, a hollow ring per pinned point), the reach under it, and the owner band.
The two exclusive doors are in brass/rose; the shared rooms are in copper (muted).

Run: python3 make_door_map.py
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


def glyph_pin(cx, cy, r, color):
    return (f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r}" fill="none" '
            f'stroke="{color}" stroke-width="2.2" opacity="0.9"/>')


def glyph_row(cx, cy, ncycles, npins, color, spacing=64, s=40):
    out = []
    k = ncycles + npins
    x0 = cx - (k - 1) * spacing / 2
    for i in range(ncycles):
        out.append(glyph_triangle(x0 + i * spacing, cy, s, color))
    for j in range(npins):
        out.append(glyph_pin(x0 + (ncycles + j) * spacing, cy, 15, MUTE))
    return out


def panel(cx, cy, title, ncycles, npins, color, owner, kind, note):
    out = []
    out.append(text(cx, cy - 150, 25, INK, title, 'text-anchor="middle"'))
    out.extend(glyph_row(cx, cy - 34, ncycles, npins, color))
    out.append(text(cx, cy + 12, 16, MUTE, kind, 'text-anchor="middle"'))
    # owner band
    out.append(f'<rect x="{cx-150:.1f}" y="{cy+36:.1f}" width="300" height="44" '
               f'rx="6" fill="none" stroke="{color}" stroke-width="1.6"/>')
    out.append(text(cx, cy + 66, 19, color, owner, 'text-anchor="middle"'))
    out.append(text(cx, cy + 108, 14, INK, note, 'text-anchor="middle"'))
    return out


def build():
    W, H = 2100, 830
    p = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
         f'viewBox="0 0 {W} {H}">']
    p.append(f'<rect width="{W}" height="{H}" fill="{BG}"/>')
    p.append(text(W / 2, 60, 30, INK,
                  "the maximal-3-cycle door: exclusive at A₇ and A₉ only",
                  'text-anchor="middle" letter-spacing="1"'))
    p.append(text(W / 2, 96, 16, DIM,
                  "Conway 11n34 · KT 11n42 — swept class by class (A₅, A₆, A₈) and "
                  "by the recorded A₇, A₉ runs.",
                  'text-anchor="middle"'))
    p.append(text(W / 2, 120, 15, DIM,
                  "each room's maximal 3-cycle: a triangle per 3-cycle, a hollow ring "
                  "per pinned point.  brass = Conway's, rose = KT's, teal = shared "
                  "(opens for both, or for neither).",
                  'text-anchor="middle"'))

    centers = [320, 715, 1065, 1440, 1820]
    # A₅: 3·1² (1 triangle, 2 pins) — both to A₅
    p.extend(panel(centers[0], 440, "A₅", 1, 2, SHARED, "shared",
                   "max 3-cycle (3,1,1)", "both → A₅  (60)"))
    # A₆: 3² (2 triangles) — both to A₅ only
    p.extend(panel(centers[1], 440, "A₆", 2, 0, SHARED, "shared",
                   "max 3-cycle (3,3)", "both → A₅  (60) — not A₆"))
    # A₇: 3²·1 (2 triangles, 1 pin) — Conway's
    p.extend(panel(centers[2], 440, "A₇", 2, 1, BRASS, "CONWAY's door",
                   "max 3-cycle (3,3,1)", "Conway → A₇ (2520); KT → PSL(2,7) (168)"))
    # A₈: 3²·1² (2 triangles, 2 pins) — shared
    p.extend(panel(centers[3], 440, "A₈", 2, 2, SHARED, "shared",
                   "max 3-cycle (3,3,1,1)", "both → A₈  (20160)"))
    # A₉: 3³ (3 triangles) — KT's
    p.extend(panel(centers[4], 440, "A₉", 3, 0, ROSE, "KT's door",
                   "max 3-cycle (3,3,3)", "KT → A₉ (181440); Conway → 0 transitive"))

    # the flip arrow over the two exclusive doors
    p.append(f'<path d="M 1065,610 L 1820,610" stroke="{GOLD}" stroke-width="2.5" '
             f'opacity="0.7" stroke-dasharray="6 5"/>')
    p.append(text(1442, 640, 15, GOLD, "the door changes hands",
                  'text-anchor="middle"'))

    # footer
    p.append(text(W / 2, 720, 18, INK,
                  "the mutants part at A₇ and A₉ — not at A₅, A₆, A₈.",
                  'text-anchor="middle"'))
    p.append(text(W / 2, 752, 15, DIM,
                  "at A₈ every swept class opens for both or for neither — "
                  "weight, not kind.",
                  'text-anchor="middle"'))
    p.append(text(W / 2, 784, 14, MUTE,
                  "probe_eight.py · make_sweep5/6.py — the door is the room's maximal "
                  "3-cycle; the weave picks the owner, and only at odd rooms ≥ 7.",
                  'text-anchor="middle"'))

    p.append('</svg>')
    return "\n".join(p)


def main():
    svg = build()
    base = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(base, "assets", "door_map.svg"), "w") as f:
        f.write(svg)
    png = os.path.join(base, "assets", "door_map.png")
    cairosvg.svg2png(url=os.path.join(base, "assets", "door_map.svg"),
                     write_to=png, output_width=2100, output_height=830)
    print("wrote", png)


if __name__ == "__main__":
    main()
