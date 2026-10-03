#!/usr/bin/env python3
"""make_necklace.py — the split-torus necklace: how many beads carry the reach.

The split-torus class of PSL(2,p) has order m=(p-1)/2.  Its generators fall into
phi(m)/2 conjugacy classes — the beads of a necklace.  Reading the reach
(beta-hat-fixed onto-orbits) bead by bead:

  every rung up to p=37 puts the reach on exactly ONE bead (or none, at p=37);
  p=43 puts it on TWO — order-21 classes carrying 2 and 4 onto-orbits.

So the 'one lit bead' the salon read off the small rungs is not a law: it holds
to m=18 and breaks at m=21.  Lit beads filled brass; the reach printed beneath.
p=43's last three beads were still computing when this was drawn (dashed).
"""
import cairosvg

# (p, m, list of per-bead reach in onto-orbits (None=pending), seam)
ROWS = [
    (7,  3,  [4],                    True),
    (11, 5,  [2, 0],                 False),
    (13, 6,  [2],                    True),
    (17, 8,  [4, 0],                 False),
    (19, 9,  [4, 0, 0],              False),
    (23, 11, [0, 0, 0, 6, 0],        False),
    (37, 18, [0, 0, 0],              False),
    (43, 21, [0, 2, 4, None, None, None], False),
]

BG = "#0b0907"
BRASS = "#d4a017"
BRASS_EDGE = "#f0c75e"
DARK = "#14100c"
DARK_EDGE = "#3a332c"
PEND_EDGE = "#4a4238"
TXT = "#d8c9a8"
DIM = "#8a7d63"
COPPER = "#c07a5a"

W, H = 1180, 108 + len(ROWS) * 88 + 30
row_h = 88
x0 = 210
bead_sp = 46
r = 17


def svg():
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">']
    out.append(f'<rect width="{W}" height="{H}" fill="{BG}"/>')
    out.append(f'<text x="24" y="42" font-family="DejaVu Sans Mono" font-size="25" fill="{TXT}">the reach climbs one bead — until p=43</text>')
    out.append(f'<text x="24" y="70" font-family="DejaVu Sans Mono" font-size="14" fill="{DIM}">split-torus necklace: φ(m)/2 generator-classes · the reach (β̂-fixed onto-orbits) lives on the lit beads</text>')
    out.append(f'<text x="24" y="90" font-family="DejaVu Sans Mono" font-size="14" fill="{DIM}">one lit bead at every rung to m=18 — two at m=21.  the one-bead reading is not a law.</text>')

    for i, (p, m, orbits, seam) in enumerate(ROWS):
        y = 130 + i * row_h
        out.append(f'<text x="24" y="{y+6}" font-family="DejaVu Sans Mono" font-size="19" fill="{TXT}">p={p}</text>')
        nb = len(orbits)
        lit = sum(1 for o in orbits if o)
        total = sum(o for o in orbits if o)
        out.append(f'<text x="24" y="{y+27}" font-family="DejaVu Sans Mono" font-size="13" fill="{DIM}">m={m} · {nb} bead{"s" if nb!=1 else ""} · {lit} lit</text>')
        for b, o in enumerate(orbits):
            cx = x0 + b * bead_sp
            if o is None:
                out.append(f'<circle cx="{cx}" cy="{y+10}" r="{r}" fill="none" stroke="{PEND_EDGE}" stroke-width="1.5" stroke-dasharray="3 4"/>')
                out.append(f'<text x="{cx}" y="{y+15}" font-family="DejaVu Sans Mono" font-size="14" fill="{PEND_EDGE}" text-anchor="middle">?</text>')
            elif o > 0:
                out.append(f'<circle cx="{cx}" cy="{y+10}" r="{r}" fill="{BRASS}" stroke="{BRASS_EDGE}" stroke-width="2.5"/>')
                out.append(f'<text x="{cx}" y="{y+38}" font-family="DejaVu Sans Mono" font-size="13" fill="{BRASS_EDGE}" text-anchor="middle">{o}</text>')
            else:
                out.append(f'<circle cx="{cx}" cy="{y+10}" r="{r}" fill="{DARK}" stroke="{DARK_EDGE}" stroke-width="1.5"/>')
                out.append(f'<text x="{cx}" y="{y+38}" font-family="DejaVu Sans Mono" font-size="13" fill="{DARK_EDGE}" text-anchor="middle">0</text>')
        rx = x0 + nb * bead_sp + 30
        if seam:
            out.append(f'<text x="{rx}" y="{y+14}" font-family="DejaVu Sans Mono" font-size="16" fill="{COPPER}" font-weight="bold">SEAM · Conway &gt; KT</text>')
        elif total == 0:
            out.append(f'<text x="{rx}" y="{y+14}" font-family="DejaVu Sans Mono" font-size="15" fill="{DIM}">collapse · door open, empty</text>')
        else:
            out.append(f'<text x="{rx}" y="{y+14}" font-family="DejaVu Sans Mono" font-size="15" fill="{DIM}">agree</text>')

    out.append('</svg>')
    return "\n".join(out)


if __name__ == "__main__":
    with open("assets/necklace.svg", "w") as f:
        f.write(svg())
    cairosvg.svg2png(url="assets/necklace.svg", write_to="assets/necklace.png", output_width=1180)
    print("wrote assets/necklace.svg / .png")