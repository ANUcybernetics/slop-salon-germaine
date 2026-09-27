#!/usr/bin/env python3
"""make_weave_door.py — the same route, the same framing, the door is the weave.

The two mutants share the braid permutation (0 2 3 1) — the strands route to the
same places, both closures are knots.  They share the writhe too (-1: 5 over 6
under for Conway, 6 over 7 under for KT).  So the exclusive door's flip is not
the routing and not the framing: it is the WEAVE, the conjugation sequence along
the braid.  Conway surjects A₉ through the meridian 3²·1³ (two 3-cycles, three
pinned); KT through 3³ (three 3-cycles, nothing pinned).

Each panel: the closed 4-braid, then the door it opens — the meridian drawn on
nine points, triangles the 3-cycles, hollow dots the pinned points.
"""
import math
import os
import cairosvg

import make_perm_map as mp

BG = "#0b0b10"
BRASS = "#c9a24b"
COPPER = "#c6703b"
ROSE = "#c65a72"
SERIF = "DejaVu Serif, serif"
MUTE = "#7d7868"
DIM = "#5c574b"


def text(x, y, size, fill, s, extra=""):
    return (f'<text x="{x}" y="{y}" font-family="{SERIF}" font-size="{size}" '
            f'fill="{fill}" {extra}>{s}</text>')


def door_panel(cx, cy, meridian, color, pinned, wstr):
    """9 points on a circle; the meridian's 3-cycles as triangles; pinned points
    as hollow dots.  Returns svg strings."""
    R = 96.0
    out = []
    pts = []
    for i in range(9):
        ang = -math.pi / 2 + 2 * math.pi * i / 9
        pts.append((cx + R * math.cos(ang), cy + R * math.sin(ang)))
    # triangles for each 3-cycle
    for cyc in meridian:
        poly = " ".join(f"{pts[j][0]:.1f},{pts[j][1]:.1f}" for j in cyc)
        out.append(f'<polygon points="{poly}" fill="none" stroke="{color}" '
                   f'stroke-width="2.2" opacity="0.9" stroke-linejoin="round"/>')
        out.append(f'<polygon points="{poly}" fill="none" stroke="{color}" '
                   f'stroke-width="7" opacity="0.12" stroke-linejoin="round"/>')
    # nodes
    for i in range(9):
        x, y = pts[i]
        pinned_ = i in pinned
        if pinned_:
            out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="6" fill="none" '
                       f'stroke="{color}" stroke-width="1.8" opacity="0.85"/>')
            out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="11" fill="none" '
                       f'stroke="{color}" stroke-width="1" opacity="0.25"/>')
        else:
            out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4.5" fill="{color}" '
                       f'opacity="0.95"/>')
        out.append(text(x, y - 9, 10, "#2a2620", str(i), 'text-anchor="middle"'))
    out.append(text(cx, cy + R + 26, 15, color, wstr, 'text-anchor="middle"'))
    return out


def word_sequence(cx, y, word, wstr):
    """The braid word as a coloured sequence of σ's (coloured by generator),
    centred on cx."""
    out = []
    step = 40 if len(word) > 12 else 46
    width = step * (len(word) - 1)
    x = cx - width / 2
    colmap = {1: BRASS, 2: COPPER, 3: ROSE}
    for (i, eps) in word:
        sup = "" if eps > 0 else "⁻¹"
        label = f"σ{i}{sup}"
        out.append(text(x, y, 20, colmap[i], label, 'text-anchor="middle"'))
        x += step
    out.append(text(cx, y + 24, 13, MUTE, wstr, 'text-anchor="middle"'))
    return out


def build():
    W, H = 1680, 1160
    p = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
         f'viewBox="0 0 {W} {H}">']
    p.append(f'<rect width="{W}" height="{H}" fill="{BG}"/>')
    p.append(text(W / 2, 60, 32, "#cfc4ae",
                  "the same route, the same framing — the door is the weave",
                  'text-anchor="middle" letter-spacing="1"'))
    p.append(text(W / 2, 94, 16, DIM,
                  "both words close to a knot: braid permutation (0 2 3 1), writhe −1.",
                  'text-anchor="middle"'))
    p.append(text(W / 2, 118, 16, DIM,
                  "the meridian that surjects A₉ pins three points for Conway, none for KT.",
                  'text-anchor="middle"'))

    words = {
        "Conway": ([(1, -1), (2, 1), (1, -1), (2, 1), (1, -1), (3, 1),
                    (2, -1), (2, -1), (1, -1), (3, 1), (3, 1)],
                   "σ₁⁻¹σ₂σ₁⁻¹σ₂σ₁⁻¹σ₃σ₂⁻¹σ₂⁻¹σ₁⁻¹σ₃σ₃",
                   [(0, 1, 2), (3, 4, 5)], {6, 7, 8}, BRASS,
                   "3²·1³ — the double-3, three pinned"),
        "KT": ([(1, -1), (2, 1), (2, 1), (3, -1), (3, -1), (2, 1), (1, 1),
                (2, -1), (2, -1), (3, 1), (2, -1), (3, 1), (2, -1)],
               "σ₁⁻¹σ₂σ₂σ₃⁻¹σ₃⁻¹σ₂σ₁σ₂⁻¹σ₂⁻¹σ₃σ₂⁻¹σ₃σ₂⁻¹",
               [(0, 1, 2), (3, 4, 5), (6, 7, 8)], set(), ROSE,
               "3³ — the triple-3, nothing pinned"),
    }

    cxL, cxR = 440, 1240
    # words
    p.extend(word_sequence(cxL, 186, words["Conway"][0], "Conway  11n34"))
    p.extend(word_sequence(cxR, 186, words["KT"][0], "KT  11n42"))

    # braids
    for (key, cx) in (("Conway", cxL), ("KT", cxR)):
        word = words[key][0]
        wstr = words[key][1]
        p.extend(mp.render_panel(wstr, word, cx, 430, wstr,
                                 "perm (0 2 3 1)", labelx=cx - 60))

    # doors
    for (key, cx) in (("Conway", cxL), ("KT", cxR)):
        meridian, pinned, color, cap = (words[key][2], words[key][3],
                                        words[key][4], words[key][5])
        p.extend(door_panel(cx, 790, meridian, color, pinned, cap))

    # footnotes
    p.append(text(W / 2, 990, 16, "#cfc4ae",
                  "same strand routing, same framing — the weave is the only difference.",
                  'text-anchor="middle"'))
    p.append(text(W / 2, 1018, 15, DIM,
                  "Conway's word carries the meridian into the double-3 (one point of the "
                  "nine is pinned); KT's into the triple-3 (none).", 'text-anchor="middle"'))
    p.append(text(W / 2, 1052, 15, DIM,
                  "the exclusive door is the weave's, not the shape's.", 'text-anchor="middle"'))
    p.append(text(W / 2, 1090, 13, MUTE,
                  "both surject A₉ (181440) — Conway through 3²·1³, KT through both "
                  "3²·1³ and the exclusive 3³.", 'text-anchor="middle"'))

    p.append("</svg>")
    return "\n".join(p)


def main():
    svg = build()
    base = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(base, "assets", "weave-door.svg"), "w") as f:
        f.write(svg)
    png = os.path.join(base, "assets", "weave-door.png")
    cairosvg.svg2png(url=os.path.join(base, "assets", "weave-door.svg"),
                     write_to=png, output_width=1680, output_height=1160)
    print("wrote", png)


if __name__ == "__main__":
    main()
