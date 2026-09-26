#!/usr/bin/env python3
"""make_a9_door.py — the doors cross: Conway the seventh, KT the ninth.

The A8/A10 dispute settled, the open question was the ninth room: does the seam
open A_9?  rahel said "no door"; I had no door but no proof.

The answer (make_a9_search.py) is a door — and it is KT's, not Conway's:
the KT 11n42 knot SURJECTS A_9 (181440) through the TRIPLE-3 meridian
(three 3-cycles, support 9, fixes nothing), and the Conway 11n34 twin has NO
such hom — its triple-3 door is closed.

This flips the A_7 polarity: there, the DOUBLE-3 (two 3-cycles, support 6, one
pinned) opens for Conway (10080) and not for KT (0).  So the mutants agree at
A_6 (blind) and A_8 (both fill), and part at A_7 (Conway's double-3) and A_9
(KT's triple-3) — the doors cross.

Two rows (the seventh, the ninth), two columns (Conway, KT).  Each cell is the
meridian door: the double-3 or the triple-3.  An open door glows in its owner's
light; a closed one is dim.  The two open doors lie on a diagonal.
"""
import math

import cairosvg

BG = "#08080d"
MUTE = "#4a3f4a"
DARK = "#2c2430"
BRASS = "#d9a84f"
COPPER = "#c47b5a"
ROSE = "#c96767"
DIM = "#5a4c54"
DIMD = "#3a3238"


def label(cx, y, text, fill=MUTE, size=17, anchor="middle"):
    return (f'<text x="{cx:.1f}" y="{y:.1f}" text-anchor="{anchor}" '
            f'font-family="monospace" font-size="{size}" fill="{fill}">{text}</text>')


def poly(cx, cy, r, n, rot=0.0):
    return [(cx + r * math.cos(rot + 2 * math.pi * k / n),
             cy + r * math.sin(rot + 2 * math.pi * k / n)) for k in range(n)]


def pts(p):
    return " ".join(f"{x:.1f},{y:.1f}" for x, y in p)


def tri_ring(cx, cy, r, rot, color, width, op=1.0, fill=None):
    p = poly(cx, cy, r, 3, rot)
    fill_attr = f'fill="{fill}"' if fill else 'fill="none"'
    return f"""  <polygon points="{pts(p)}" {fill_attr} stroke="{color}"
        stroke-width="{width}" stroke-linejoin="round" opacity="{op}"/>"""


def meridian_door(cx, cy, r, k, color, open_=False, owner=None):
    """The meridian as k interlocked 3-cycles (k=2 the double-3, k=3 the triple-3).
    open_=True: the door glows in `color`; False: it is dim and closed."""
    if open_:
        main = color
        halo_op = 0.34
        inner = "#f0d9a0"
    else:
        main = DIM
        halo_op = 0.06
        inner = DIMD
    s = ""
    # halo
    s += f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r*1.35:.1f}" fill="none" ' \
         f'stroke="{main}" stroke-width="{5 if open_ else 2}" opacity="{halo_op}" ' \
         f'filter="url(#soft)"/>'
    s += f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r*1.35:.1f}" fill="none" ' \
         f'stroke="{main}" stroke-width="1.6" opacity="{0.5 if open_ else 0.22}"/>'
    # the k interlocked triangles (3-cycles)
    ring_r = r * 0.74
    for i in range(k):
        rot = -math.pi / 2 + 2 * math.pi * i / k
        # offset each triangle toward its own corner so they interlock
        ox = cx + math.cos(rot) * r * 0.28
        oy = cy + math.sin(rot) * r * 0.28
        s += tri_ring(ox, oy, ring_r, rot, main, 2.4 if open_ else 1.4,
                      op=1.0 if open_ else 0.55, fill=None)
    # hub
    s += f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r*0.16:.1f}" fill="{inner}" ' \
         f'opacity="{0.9 if open_ else 0.35}"/>'
    if not open_:
        # a closed door: a crossbar
        s += (f'<line x1="{cx-r*0.5:.1f}" y1="{cy-r*0.5:.1f}" '
              f'x2="{cx+r*0.5:.1f}" y2="{cy+r*0.5:.1f}" stroke="{DIM}" '
              f'stroke-width="1.6" opacity="0.8"/>')
        s += (f'<line x1="{cx-r*0.5:.1f}" y1="{cy+r*0.5:.1f}" '
              f'x2="{cx+r*0.5:.1f}" y2="{cy-r*0.5:.1f}" stroke="{DIM}" '
              f'stroke-width="1.6" opacity="0.8"/>')
    return s


def build():
    W, H = 1700, 1180
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
         f'viewBox="0 0 {W} {H}">']
    s.append("""<defs>
      <filter id="soft" x="-50%" y="-50%" width="200%" height="200%">
        <feGaussianBlur stdDeviation="9"/>
      </filter>
    </defs>""")
    s.append(f'<rect width="{W}" height="{H}" fill="{BG}"/>')
    s.append(label(W / 2, 52, "the door one keeps", ROSE, 38))
    s.append(label(W / 2, 88, "the exclusive door crosses: Conway's seventh, KT's ninth", MUTE, 19))

    # grid
    cxL, cxR = 500, 1200
    cyTop, cyBot = 320, 690
    r = 132

    # column headers
    s.append(label(cxL, 150, "Conway  11n34", BRASS, 26))
    s.append(label(cxR, 150, "KT  11n42", ROSE, 26))
    # row labels
    s.append(label(cxL - 360, cyTop, "the seventh room", BRASS, 24))
    s.append(label(cxL - 360, cyTop + 32, "the double-3", MUTE, 16))
    s.append(label(cxL - 360, cyBot, "the ninth room", ROSE, 24))
    s.append(label(cxL - 360, cyBot + 32, "the triple-3", MUTE, 16))

    # cells: (cx, cy, k, color, open?, label, count)
    cells = [
        (cxL, cyTop, 2, BRASS, True,  "Conway", "10080"),   # A7 Conway open
        (cxR, cyTop, 2, ROSE,  False, "KT",     "0"),       # A7 KT closed
        (cxL, cyBot, 3, BRASS, False, "Conway", "0"),       # A9 Conway closed
        (cxR, cyBot, 3, ROSE,  True,  "KT",     "181440"),  # A9 KT open
    ]
    for (cx, cy, k, color, open_, owner, count) in cells:
        s.append(meridian_door(cx, cy, r, k, color, open_=open_))
        s.append(label(cx, cy + r + 46, count, color if open_ else DIM, 22))
        s.append(label(cx, cy + r + 74,
                       "through the triple-3" if k == 3 else "through the double-3",
                       MUTE, 15))

    # the crossing diagonals
    # open door path: (cxL,cyTop) -> (cxR,cyBot)  (Conway A7, KT A9)
    s.append(f'<line x1="{cxL}" y1="{cyTop}" x2="{cxR}" y2="{cyBot}" '
             f'stroke="{COPPER}" stroke-width="3" opacity="0.55" '
             f'stroke-linecap="round" filter="url(#soft)"/>')
    s.append(f'<line x1="{cxL}" y1="{cyTop}" x2="{cxR}" y2="{cyBot}" '
             f'stroke="#f0d9a0" stroke-width="1.4" opacity="0.6" stroke-dasharray="2 6"/>')
    # closed door path: (cxR,cyTop) -> (cxL,cyBot) (KT A7, Conway A9) -- broken
    s.append(f'<line x1="{cxR}" y1="{cyTop}" x2="{cxL}" y2="{cyBot}" '
             f'stroke="{DIM}" stroke-width="2" opacity="0.35" stroke-dasharray="7 8"/>')
    s.append(label((cxL + cxR) / 2, (cyTop + cyBot) / 2 - 14,
                   "the light travels the diagonal", MUTE, 16))
    s.append(label((cxL + cxR) / 2, (cyTop + cyBot) / 2 + 12,
                   "the closed diagonal stays dark", MUTE, 16))

    # footer
    s.append(label(W / 2, H - 212,
                   "each cell is one DOOR, not the room. the ninth opens for both mutants "
                   "(the double-3 on nine points, 3²·1³, surjects A₉ = 181440 in each);", DIM, 17))
    s.append(label(W / 2, H - 184,
                   "the seventh opens for both too (Conway 85680, KT 65520 onto-A₇). "
                   "what crosses is the door one keeps for itself:", DIM, 17))
    s.append(label(W / 2, H - 152,
                   "the seventh's 3²·1 (two 3-cycles, one pinned) is Conway's alone — 10080, KT 0. "
                   "the ninth's 3³ (three 3-cycles, none pinned) is KT's alone — 0, Conway.", COPPER, 17))
    s.append(label(W / 2, H - 118,
                   "the mutants agree at the sixth (blind, 9000 each) and the eighth "
                   "(both fill, 20160); they part where one has a door the other cannot use.", MUTE, 16))
    s.append(label(W / 2, H - 86,
                   "KT's triple-3 witness: ⟨(0 1 2)(3 4 5)(6 7 8), (0 1 3)(2 6 5)(4 8 7), "
                   "(0 4 1)(2 5 6)(3 8 7), (0 2 6)(1 7 8)(3 4 5)⟩ = A₉.", MUTE, 15))
    s.append(label(W / 2, H - 56,
                   "rahel said no door. the ninth opens — for both. but the meridian that "
                   "pins nothing (3³) is KT's, and KT's alone.", MUTE, 15))

    s.append("</svg>")
    return "\n".join(s)


def main():
    svg = build()
    with open("assets/a9_door.svg", "w") as f:
        f.write(svg)
    cairosvg.svg2png(url="assets/a9_door.svg", write_to="assets/a9_door.png",
                     output_width=1700, output_height=1080)
    print("rendered assets/a9_door.png")


if __name__ == "__main__":
    main()
