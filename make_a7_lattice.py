#!/usr/bin/env python3
"""make_a7_lattice.py — the A₇ room's doors, class by class.

mina: "the double-3 (3,3,1) is Conway's alone at A₇."  True at that class.
rahel: "the seventh opens for both — a 5-cycle meridian."  Also true.

Both are exact; the resolution is the class, not the room.  Both mutants reach
A₇ through most meridian classes (3·2², 4·2·1, 5·1², 7).  The weave parts them
at exactly ONE: the double-3 3²·1, which Conway opens (2520) and KT cannot
(caps at PSL(2,7) 168).  Six doors agree; one door divides.

Each row is a meridian class, drawn as its cycle type (a small n-gon per cycle,
a hollow ring per fixed point).  Each cell is a doorway: glowing = that class
surjects A₇, dark = shut.  The dividing row is banded in brass.

Run: python3 make_a7_lattice.py
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
DIM = "#4c4638"
INK = "#cfc4ae"
DARK = "#2a2620"

# rows: (label, cycle lengths, conway state, kt state, image orders)
# state: "open" | "shut" | "cap"
ROWS = [
    ("2²·1³", "two 2-cycles", [2, 2, 1, 1, 1], "shut", "shut", "", ""),
    ("3²·1", "double 3-cycle", [3, 3, 1], "open", "cap", "2520", "→ 168"),
    ("3·1⁴", "one 3-cycle", [3, 1, 1, 1, 1], "shut", "shut", "", ""),
    ("3·2²", "3-cycle · two 2-cycles", [3, 2, 2], "open", "open", "2520", "2520"),
    ("4·2·1", "4-cycle · 2-cycle", [4, 2, 1], "open", "open", "2520", "2520"),
    ("5·1²", "5-cycle", [5, 1, 1], "open", "open", "2520", "2520"),
    ("7", "7-cycle", [7], "open", "open", "2520", "2520"),
]


def text(x, y, size, fill, s, extra=""):
    return (f'<text x="{x}" y="{y}" font-family="{SERIF}" font-size="{size}" '
            f'fill="{fill}" {extra}>{s}</text>')


def ngon(cx, cy, r, n, color):
    """outline of a regular n-gon; n=2 is a short bar, n=1 a hollow ring."""
    if n == 1:
        return (f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r*0.55:.1f}" fill="none" '
                f'stroke="{MUTE}" stroke-width="1.8" opacity="0.8"/>')
    if n == 2:
        return (f'<line x1="{cx-r:.1f}" y1="{cy:.1f}" x2="{cx+r:.1f}" y2="{cy:.1f}" '
                f'stroke="{color}" stroke-width="2.4" opacity="0.85"/>'
                f'<circle cx="{cx-r:.1f}" cy="{cy:.1f}" r="2.6" fill="{color}"/>'
                f'<circle cx="{cx+r:.1f}" cy="{cy:.1f}" r="2.6" fill="{color}"/>')
    pts = []
    for k in range(n):
        ang = -math.pi / 2 + 2 * math.pi * k / n
        pts.append((cx + r * math.cos(ang), cy + r * math.sin(ang)))
    d = "M " + " L ".join(f"{x:.1f},{y:.1f}" for x, y in pts) + " Z"
    return (f'<path d="{d}" fill="none" stroke="{color}" stroke-width="2.2" '
            f'opacity="0.85"/>')


def class_glyph(cx, cy, lengths, color):
    """draw the cycle type as a row of small n-gons centered at (cx, cy)."""
    spacing = 58
    r = 16
    x0 = cx - (len(lengths) - 1) * spacing / 2
    out = []
    for i, n in enumerate(lengths):
        out.append(ngon(x0 + i * spacing, cy, r, n, color))
    return out


def door(cx, cy, state, color, label):
    """an arched doorway.  open = glowing, cap = ajar, shut = dark."""
    out = []
    w, h, rx = 66, 78, 33
    arch = (f'M {cx-w/2:.1f},{cy+h/2:.1f} L {cx-w/2:.1f},{cy-h/2+rx:.1f} '
            f'A {rx},{rx} 0 0 1 {cx+w/2:.1f},{cy-h/2+rx:.1f} '
            f'L {cx+w/2:.1f},{cy+h/2:.1f} Z')
    if state == "open":
        out.append(f'<rect x="{cx-w/2-11:.1f}" y="{cy-h/2-11:.1f}" width="{w+22}" '
                   f'height="{h+22}" rx="15" fill="{color}" opacity="0.09"/>')
        out.append(f'<path d="{arch}" fill="{color}" opacity="0.18" '
                   f'stroke="{color}" stroke-width="2.4"/>')
    elif state == "cap":
        # ajar — opened only partway, into a smaller room
        out.append(f'<path d="{arch}" fill="none" stroke="{color}" '
                   f'stroke-width="1.5" opacity="0.4"/>')
        out.append(f'<line x1="{cx+w/2:.1f}" y1="{cy+h/2:.1f}" x2="{cx+w/2+13:.1f}" '
                   f'y2="{cy+h/2:.1f}" stroke="{color}" stroke-width="1.8" opacity="0.55"/>')
    else:  # shut
        out.append(f'<path d="{arch}" fill="{DARK}" stroke="{DIM}" stroke-width="1.4"/>')
        out.append(f'<line x1="{cx-w/2+9:.1f}" y1="{cy+5:.1f}" x2="{cx+w/2-9:.1f}" '
                   f'y2="{cy+5:.1f}" stroke="{DIM}" stroke-width="1.3"/>')
    out.append(text(cx, cy + h / 2 + 30, 16, MUTE, label, 'text-anchor="middle"'))
    return out


def build():
    W, H = 1760, 1400
    p = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
         f'viewBox="0 0 {W} {H}">']
    p.append(f'<rect width="{W}" height="{H}" fill="{BG}"/>')
    p.append(text(W / 2, 60, 30, INK,
                  "six doors agree, one door divides",
                  'text-anchor="middle" letter-spacing="1"'))
    p.append(text(W / 2, 96, 16, DIM,
                  "A₇, class by class — both mutants reach the room; the weave "
                  "parts them at exactly one meridian class.",
                  'text-anchor="middle"'))
    p.append(text(W / 2, 122, 15, DIM,
                  "each row is a meridian class, drawn as its cycle type (n-gon per "
                  "cycle, ring per fixed point); each doorway is a class's reach.",
                  'text-anchor="middle"'))

    # column headers
    p.append(text(400, 190, 18, INK, "meridian class", 'text-anchor="middle"'))
    p.append(text(1010, 190, 20, BRASS, "Conway 11n34", 'text-anchor="middle"'))
    p.append(text(1460, 190, 20, ROSE, "KT 11n42", 'text-anchor="middle"'))

    # rows
    y0 = 300
    rowh = 130
    for i, (name, note, lengths, cs, ks, cimg, kimg) in enumerate(ROWS):
        cy = y0 + i * rowh
        is_part = (name == "3²·1")
        if is_part:
            p.append(f'<rect x="140" y="{cy-rowh/2+14:.1f}" width="{W-280}" '
                     f'height="{rowh-28}" rx="12" fill="{BRASS}" opacity="0.07"/>')
        # class glyph + label
        color = BRASS if is_part else MUTE
        p.extend(class_glyph(410, cy - 14, lengths, color))
        p.append(text(410, cy + 34, 20, INK if is_part else MUTE, name,
                      'text-anchor="middle"'))
        # conway cell
        c_label = cimg if cs == "open" else "shut"
        cs_color = BRASS if cs == "open" else DIM
        p.extend(door(1010, cy, cs, cs_color, c_label))
        # kt cell
        k_label = kimg if ks == "open" else ("→ 168" if ks == "cap" else "shut")
        ks_color = ROSE if ks == "open" else (COPPER if ks == "cap" else DIM)
        p.extend(door(1460, cy, ks, ks_color, k_label))
        # a small "agrees/divides" tick on the right
        if is_part:
            p.append(text(W - 120, cy + 6, 15, GOLD, "divides",
                          'text-anchor="middle"'))
        else:
            p.append(text(W - 120, cy + 6, 14, DIM, "agrees",
                          'text-anchor="middle"'))

    # legend
    ly = y0 + len(ROWS) * rowh + 30
    p.append(text(W / 2, ly, 15, DIM,
                  "glowing doorway = that class surjects A₇ (2520) · dark = shut · "
                  "ajar = opens only a smaller room (PSL(2,7), 168)",
                  'text-anchor="middle"'))

    # footer
    p.append(text(W / 2, ly + 66, 18, INK,
                  "mina: the double-3 is Conway's alone. rahel: the seventh opens "
                  "for both. yes — and the door is the class, not the room.",
                  'text-anchor="middle"'))
    p.append(text(W / 2, ly + 98, 15, DIM,
                  "both mutants reach A₇ through most doors; the weave parts them "
                  "at the double-3 only. probe_seven.py.",
                  'text-anchor="middle"'))

    p.append('</svg>')
    return "\n".join(p)


def main():
    svg = build()
    base = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(base, "assets", "a7_lattice.svg"), "w") as f:
        f.write(svg)
    png = os.path.join(base, "assets", "a7_lattice.png")
    cairosvg.svg2png(url=os.path.join(base, "assets", "a7_lattice.svg"),
                     write_to=png, output_width=1760, output_height=1400)
    print("wrote", png)


if __name__ == "__main__":
    main()
