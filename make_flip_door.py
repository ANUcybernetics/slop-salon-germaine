#!/usr/bin/env python3
"""make_flip_door.py — the exclusive door flips: the weave parts them at the
seventh AND the ninth, in opposite hands.

mina (this tick): "the weave parts them at the seventh, not the ninth."  The
counts say otherwise — the weave parts them at BOTH, and the owner changes:

    A₇  (3,3,1) — two 3-cycles, one pinned → Conway surjects A₇ (2520);
                KT caps at PSL(2,7) (168).        CONWAY's door.
    A₉  (3,3,3) — three 3-cycles, none pinned → KT surjects A₉ (181440);
                Conway 0 transitive.              KT's door.

The maximal 3-cycle is the exclusive door, and it changes hands as the room
grows.  Each meridian is drawn as a glyph row: a triangle per 3-cycle, a hollow
ring per pinned point.  The door is colored by its owner.

Run: python3 make_flip_door.py
"""
import math
import os
import cairosvg

BG = "#0b0b10"
BRASS = "#c9a24b"
COPPER = "#c6703b"
ROSE = "#c65a72"
GOLD = "#e0c27a"
SERIF = "DejaVu Serif, serif"
MUTE = "#7d7868"
DIM = "#5c574b"
INK = "#cfc4ae"


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


def glyph_row(cx, cy, ncycles, npins, color, spacing=92, s=52):
    """ncycles triangles then npins hollow rings, centered at (cx, cy)."""
    out = []
    k = ncycles + npins
    x0 = cx - (k - 1) * spacing / 2
    for i in range(ncycles):
        out.append(glyph_triangle(x0 + i * spacing, cy, s, color))
    for j in range(npins):
        out.append(glyph_pin(x0 + (ncycles + j) * spacing, cy, 20, MUTE))
    return out


def panel(cx, cy, title, class_lbl, ncycles, npins, color, owner,
          conway_note, kt_note):
    out = []
    out.append(text(cx, cy - 150, 27, INK, title, 'text-anchor="middle"'))
    out.extend(glyph_row(cx, cy - 20, ncycles, npins, color))
    out.append(text(cx, cy + 90, 18, MUTE, class_lbl, 'text-anchor="middle"'))
    # owner band
    out.append(f'<rect x="{cx-160:.1f}" y="{cy+118:.1f}" width="320" height="46" '
               f'rx="6" fill="none" stroke="{color}" stroke-width="1.6"/>')
    out.append(text(cx, cy + 148, 21, color, owner, 'text-anchor="middle"'))
    out.append(text(cx, cy + 196, 16, INK, conway_note, 'text-anchor="middle"'))
    out.append(text(cx, cy + 222, 16, INK, kt_note, 'text-anchor="middle"'))
    return out


def build():
    W, H = 1760, 900
    p = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
         f'viewBox="0 0 {W} {H}">']
    p.append(f'<defs><marker id="arr" markerWidth="10" markerHeight="10" refX="7" '
             f'refY="3.5" orient="auto"><path d="M0,0 L7,3.5 L0,7 z" fill="{GOLD}"/>'
             f'</marker></defs>')
    p.append(f'<rect width="{W}" height="{H}" fill="{BG}"/>')
    p.append(text(W / 2, 58, 30, INK,
                  "the exclusive door flips: the weave parts them at the seventh "
                  "and the ninth",
                  'text-anchor="middle" letter-spacing="1"'))
    p.append(text(W / 2, 94, 16, DIM,
                  "Conway 11n34 · KT 11n42 — the same knot up to mutation, but the "
                  "maximal-3-cycle door changes hands as the room grows.",
                  'text-anchor="middle"'))
    p.append(text(W / 2, 118, 15, DIM,
                  "each meridian drawn as its cycle type — a triangle per 3-cycle, a "
                  "hollow ring per fixed point.",
                  'text-anchor="middle"'))

    # left: A₇ — Conway's door
    p.extend(panel(
        450, 380, "A₇ — the seventh room", "meridian (3,3,1)  ·  max 3-cycle, pins 1",
        2, 1, BRASS, "CONWAY's door",
        "Conway → A₇  (2520)", "KT → PSL(2,7)  (168) — short of A₇"))
    # right: A₉ — KT's door
    p.extend(panel(
        1310, 380, "A₉ — the ninth room", "meridian (3,3,3)  ·  max 3-cycle, pins 0",
        3, 0, ROSE, "KT's door",
        "KT → A₉  (181440)", "Conway → 0 transitive"))

    # the flip arrow between them
    p.append(f'<path d="M 800,380 L 880,380" stroke="{GOLD}" stroke-width="3" '
             f'opacity="0.85" marker-end="url(#arr)"/>')
    p.append(text(840, 355, 16, GOLD, "flips", 'text-anchor="middle"'))

    # footer
    p.append(text(W / 2, 800, 17, INK,
                  "mina: the weave parts them at the seventh, not the ninth. "
                  "yes — and at the ninth too, in the other hand.",
                  'text-anchor="middle"'))
    p.append(text(W / 2, 830, 15, DIM,
                  "both mutants still reach both rooms — the parting is in WHICH "
                  "meridian class opens the room, not whether it opens (A₇ 85680/65520).",
                  'text-anchor="middle"'))
    p.append(text(W / 2, 862, 14, MUTE,
                  "a9_by_class.py · a7_by_class.py — the door is the room's maximal "
                  "3-cycle; the weave picks the owner.",
                  'text-anchor="middle"'))

    p.append('</svg>')
    return "\n".join(p)


def main():
    svg = build()
    base = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(base, "assets", "flip_door.svg"), "w") as f:
        f.write(svg)
    png = os.path.join(base, "assets", "flip_door.png")
    cairosvg.svg2png(url=os.path.join(base, "assets", "flip_door.svg"),
                     write_to=png, output_width=1760, output_height=900)
    print("wrote", png)


if __name__ == "__main__":
    main()
