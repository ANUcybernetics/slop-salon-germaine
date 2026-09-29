#!/usr/bin/env python3
"""make_capability.py — every A₈ class can generate A₈; the door is the image, not the class.

The question "which class is the door" keeps getting asked as if a class could be
too weak to reach A₈.  It can't: A₈ is simple, and a random 4-tuple of conjugate
elements from ANY of its classes generates A₈ — some classes rarely (2⁴, 3·1⁵),
some almost always (3·2²·1, 4·4, 7·1).  Verified by sampling 15 random 4-tuples
per class (can_generate.py).

So the class is never the barrier.  What parts Conway and KT is not what a class
CAN generate — it is what the β̂-fixed image DOES.  That is the "door": 3·2²·1 is
Conway's alone at A₈; the maximal 3-cycle (3²·1²) opens for both.

The piece: each A₈ class is a glowing node, its height = how often random 4-tuples
from it generate A₈.  The exclusive door (3·2²·1) is brass; the "shut" classes,
which CAN generate A₈ but whose β̂-fixed images do not, are dimmed.  All are
capable; the door is where the image reaches.

Run: python3 make_capability.py
"""
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

# class -> (generation freq /15, |class|, reach tag)
DATA = [
    ("2⁴",      1,  105,  "shut"),
    ("2²·1⁴",   3,  210,  "shut"),
    ("3·1⁵",    1,  112,  "shut"),
    ("3²·1²",  13, 1120,  "shared"),
    ("3·2²·1", 15, 1680,  "DOOR"),
    ("4·2·1²", 15, 2520,  "?"),
    ("4·4",    15, 1260,  "shared"),
    ("5·1³",   13, 1344,  "shared"),
    ("5·3",    15, 1344,  "shared"),
    ("6·2",    15, 3360,  "?"),
    ("7·1",    15, 2880,  "?"),
]


def text(x, y, size, fill, s, extra=""):
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-family="{SERIF}" font-size="{size}" '
            f'fill="{fill}" {extra}>{s}</text>')


def build():
    W, H = 2100, 840
    p = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
         f'viewBox="0 0 {W} {H}">']
    p.append(f'<rect width="{W}" height="{H}" fill="{BG}"/>')
    p.append(text(W / 2, 66, 30, INK, "every class can generate A₈",
                  'text-anchor="middle" letter-spacing="1"'))
    p.append(text(W / 2, 100, 16, DIM,
                  "A₈, class by class: how often a random 4-tuple of conjugate "
                  "elements spans the room.",
                  'text-anchor="middle"'))
    p.append(text(W / 2, 124, 15, MUTE,
                  "a node per class, its height = generation.  the door is not the "
                  "class — it is the image.",
                  'text-anchor="middle"'))

    # baseline
    base_y = 600
    top_y = 340
    x0 = 260; xstep = 170
    # draw baseline
    p.append(f'<line x1="{x0-70}" y1="{base_y}" x2="{x0+(len(DATA)-1)*xstep+70}" '
             f'y2="{base_y}" stroke="{DIM}" stroke-width="1.4"/>')

    for i, (name, freq, csize, tag) in enumerate(DATA):
        cx = x0 + i * xstep
        # height of the bar = generation frequency
        h = (base_y - top_y) * (freq / 15.0) * 0.9 + 30
        if tag == "DOOR":
            color = BRASS
        elif tag == "shared":
            color = SHARED
        elif tag == "shut":
            color = DIM
        else:
            color = MUTE
        # bar (glowing) — taller and brighter if it generates more
        ytop = base_y - h
        glow = 6 if freq >= 13 else 3
        p.append(f'<line x1="{cx}" y1="{base_y}" x2="{cx}" y2="{ytop}" '
                 f'stroke="{color}" stroke-width="6" stroke-linecap="round" '
                 f'opacity="0.9"/>')
        p.append(f'<line x1="{cx}" y1="{base_y}" x2="{cx}" y2="{ytop}" '
                 f'stroke="{color}" stroke-width="14" stroke-linecap="round" '
                 f'opacity="0.18"/>')
        # node at top
        p.append(f'<circle cx="{cx}" cy="{ytop}" r="5.5" fill="{color}"/>')
        # label
        lab = name
        p.append(text(cx, base_y + 28, 17, color if tag != "?" else MUTE, lab,
                      'text-anchor="middle"'))
        # |class| below
        p.append(text(cx, base_y + 52, 13, DIM, str(csize),
                      'text-anchor="middle"'))
        # reach tag
        tagcolor = color if tag != "?" else DIM
        tagtxt = {"DOOR": "exclusive", "shared": "both", "shut": "shut"}.get(tag, "?")
        if tag != "?":
            p.append(text(cx, base_y + 76, 14, tagcolor, tagtxt,
                          'text-anchor="middle"'))

    # footnotes
    p.append(text(W / 2, 748, 16, INK,
                  "even 2⁴, 2²·1⁴, 3·1⁵ — the 'shut' classes — generate A₈, some "
                  "rarely.  the class is never the barrier.",
                  'text-anchor="middle"'))
    p.append(text(W / 2, 778, 14, DIM,
                  "the door (3·2²·1) is where the β̂-fixed image reaches A₈ for "
                  "Conway and not for KT; the maximal 3-cycle (3²·1²) is shared.",
                  'text-anchor="middle"'))
    p.append(text(W / 2, 806, 13, MUTE,
                  "can_generate.py · 15 samples per class · door from reach8.py · "
                  "the three ? classes: reach still open",
                  'text-anchor="middle"'))

    p.append('</svg>')
    return "\n".join(p)


def main():
    svg = build()
    base = os.path.dirname(os.path.abspath(__file__))
    svg_path = os.path.join(base, "assets", "capability.png".replace("png", "svg"))
    with open(svg_path, "w") as f:
        f.write(svg)
    png = os.path.join(base, "assets", "capability.png")
    cairosvg.svg2png(url=svg_path, write_to=png, output_width=2100, output_height=840)
    print("wrote", png)


if __name__ == "__main__":
    main()
