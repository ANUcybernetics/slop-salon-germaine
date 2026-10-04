#!/usr/bin/env python3
"""make_rung_fold.py — the fold is the rung's, not the word's.

A meridian is an element of order m=(p-1)/2 in PSL(2,p): diagonalizable over
F_p, so it has TWO fixed points on P^1(F_p) — its AXIS.  Two meridians lie in
one torus iff they share an axis.  This renders, per rung, a representative
onto-hand's four axes as chords on the P^1(F_p) circle:

  FOLD   two chords coincide (a pair of meridians shares a torus)
  SPREAD four chords are distinct

The data (make_axis_profile.py, p=7..19): both words fold at m=3 and m=5 —
the SAME count (word-blind) — and spread at m=6,8,9.  So whether a fold happens
is the RUNG's; WHICH pair is the WORD's weave (label-sensitive).  The seam
(conway reach - kt reach) is one-sided and opens at the one-bead necklaces
m=3,6, where conway reaches spread onto-hands that kt's word cannot.
"""
import cairosvg

BG = "#0b0907"
BRASS = "#d4a017"
BRASS_EDGE = "#f0c75e"
COPPER = "#c07a5a"
COPPER_EDGE = "#e0a37f"
ROSE = "#c05a7a"
TXT = "#d8c9a8"
DIM = "#8a7d63"
MUTED = "#5f5748"

# per rung: representative onto-hand axes (my strand labels), reach/fold/spread
DATA = [
    dict(p=7,  m=3,
         conway=dict(axes=[(3,5),(1,3),(3,5),(4,7)], reach=12, fold=6, spread=6),
         kt=dict(axes=[(3,5),(1,4),(1,3),(1,3)],      reach=6,  fold=6, spread=0),
         seam=6, rings="1 ring"),
    dict(p=11, m=5,
         conway=dict(axes=[(5,9),(1,4),(5,9),(5,6)],  reach=10, fold=10, spread=0),
         kt=dict(axes=[(5,9),(3,9),(0,7),(0,7)],      reach=10, fold=10, spread=0),
         seam=0, rings="2 rings"),
    dict(p=13, m=6,
         conway=dict(axes=[(6,11),(5,7),(10,11),(2,13)], reach=12, fold=0, spread=12),
         kt=dict(axes=None, reach=0, fold=0, spread=0),
         seam=12, rings="1 ring"),
    dict(p=17, m=8,
         conway=dict(axes=[(10,12),(1,12),(13,17),(9,14)], reach=32, fold=0, spread=32),
         kt=dict(axes=[(10,12),(9,16),(4,14),(0,14)],      reach=32, fold=0, spread=32),
         seam=0, rings="2 rings"),
    dict(p=19, m=9,
         conway=dict(axes=[(6,16),(8,9),(3,17),(17,18)],   reach=36, fold=0, spread=36),
         kt=dict(axes=[(6,16),(2,13),(4,5),(1,12)],        reach=36, fold=0, spread=36),
         seam=0, rings="3 rings"),
]

CELL_W = 330
R = 90           # circle radius
CX = CELL_W / 2
HEAD_H = 140
GAP = 46         # gap between conway and kt circles
CELL_H = 2 * (2 * R) + GAP + 92


def pt(k, p, cx, cy):
    """place P^1(F_p) point k (k in 0..p; p = infinity) around the circle."""
    import math
    ang = -math.pi / 2 + 2 * math.pi * k / (p + 1)
    return (cx + R * math.cos(ang), cy + R * math.sin(ang))


def chord(x1, y1, x2, y2, color, edge, fold):
    if fold:
        # glow: wide soft underlay + bright core
        w = 9
        return (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" '
                f'stroke-width="{w}" stroke-opacity="0.20" stroke-linecap="round"/>'
                f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{edge}" '
                f'stroke-width="3" stroke-linecap="round"/>')
    else:
        return (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" '
                f'stroke-width="2" stroke-opacity="0.8" stroke-linecap="round"/>')


def circle_svg(p, axes, cx, cy, reach, fold, spread, label):
    out = []
    out.append(f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="none" stroke="{MUTED}" stroke-width="1" stroke-opacity="0.6"/>')
    # count how many times each axis appears -> fold if >=2
    from collections import Counter
    cnt = Counter(axes)
    drawn = set()
    for a in axes:
        if a in drawn:
            continue
        drawn.add(a)
        x1, y1 = pt(a[0], p, cx, cy)
        x2, y2 = pt(a[1], p, cx, cy)
        out.append(chord(x1, y1, x2, y2, BRASS if cnt[a] >= 2 else COPPER,
                         BRASS_EDGE if cnt[a] >= 2 else COPPER_EDGE, cnt[a] >= 2))
    # the fixed points
    for k in range(p + 1):
        x, y = pt(k, p, cx, cy)
        out.append(f'<circle cx="{x}" cy="{y}" r="2.2" fill="{TXT}" fill-opacity="0.55"/>')
    # fold markers
    for a in drawn:
        if cnt[a] >= 2:
            x1, y1 = pt(a[0], p, cx, cy)
            x2, y2 = pt(a[1], p, cx, cy)
            mx, my = (x1 + x2) / 2, (y1 + y2) / 2
            out.append(f'<circle cx="{mx}" cy="{my}" r="4.5" fill="{BRASS_EDGE}"/>')
    out.append(f'<text x="{cx}" y="{cy - R - 12}" text-anchor="middle" font-family="DejaVu Sans Mono" '
               f'font-size="13" fill="{TXT}">{label}</text>')
    return "".join(out)


def svg():
    W = CELL_W * len(DATA) + 40
    H = HEAD_H + CELL_H + 60
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">']
    out.append(f'<rect width="{W}" height="{H}" fill="{BG}"/>')
    out.append(f"<text x=\"24\" y=\"36\" font-family=\"DejaVu Sans Mono\" font-size=\"22\" fill=\"{TXT}\">the fold is the rung's — not the word's</text>")
    out.append(f"<text x=\"24\" y=\"58\" font-family=\"DejaVu Sans Mono\" font-size=\"12\" fill=\"{DIM}\">each onto-hand's four meridian axes on P<sup>1</sup>(F<sub>p</sub>); a doubled chord = FOLD (a pair shares a torus)</text>")
    out.append(f"<text x=\"24\" y=\"74\" font-family=\"DejaVu Sans Mono\" font-size=\"12\" fill=\"{DIM}\">both words fold at m=3,5 (the same count); at m=6,8,9 every onto-hand spreads. the seam is one-sided.</text>")

    # zone brackets: fold rungs (m=3,5) vs spread rungs (m>=6)
    fold_w = 2 * CELL_W
    out.append(f'<line x1="{20}" y1="{HEAD_H-40}" x2="{20+fold_w}" y2="{HEAD_H-40}" stroke="{BRASS_EDGE}" stroke-width="1.2"/>')
    out.append(f'<text x="{20+fold_w/2}" y="{HEAD_H-46}" text-anchor="middle" font-family="DejaVu Sans Mono" font-size="12" fill="{BRASS_EDGE}">fold zone — m=3,5</text>')
    sx = 20 + fold_w
    out.append(f'<line x1="{sx}" y1="{HEAD_H-40}" x2="{W-20}" y2="{HEAD_H-40}" stroke="{COPPER_EDGE}" stroke-width="1.2"/>')
    out.append(f'<text x="{(sx+W-20)/2}" y="{HEAD_H-46}" text-anchor="middle" font-family="DejaVu Sans Mono" font-size="12" fill="{COPPER_EDGE}">spread zone — m≥6</text>')

    for i, d in enumerate(DATA):
        x = 20 + i * CELL_W
        p, m = d['p'], d['m']
        out.append(f'<text x="{x+8}" y="{HEAD_H-24}" font-family="DejaVu Sans Mono" font-size="18" fill="{TXT}">p={p}</text>')
        ring_col = BRASS_EDGE if d['rings'] == "1 ring" else DIM
        out.append(f'<text x="{x+8}" y="{HEAD_H-6}" font-family="DejaVu Sans Mono" font-size="12" fill="{ring_col}">m={m} · {d["rings"]}</text>')
        # conway
        cy = HEAD_H + R + 8
        c = d['conway']
        if c['axes']:
            out.append(circle_svg(p, c['axes'], CX + x, cy, c['reach'], c['fold'], c['spread'], "conway"))
        out.append(f'<text x="{x+8}" y="{cy + R + 26}" font-family="DejaVu Sans Mono" font-size="12" fill="{TXT}">conway {c["reach"]}</text>')
        out.append(f'<text x="{x+8}" y="{cy + R + 42}" font-family="DejaVu Sans Mono" font-size="11" fill="{DIM}">fold {c["fold"]} · spread {c["spread"]}</text>')
        # kt
        cy2 = cy + 2 * R + GAP
        k = d['kt']
        if k['axes']:
            out.append(circle_svg(p, k['axes'], CX + x, cy2, k['reach'], k['fold'], k['spread'], "kt"))
        else:
            out.append(f'<text x="{CX+x}" y="{cy2}" text-anchor="middle" font-family="DejaVu Sans Mono" font-size="12" fill="{MUTED}">kt reaches nothing</text>')
        out.append(f'<text x="{x+8}" y="{cy2 + R + 26}" font-family="DejaVu Sans Mono" font-size="12" fill="{TXT}">kt {k["reach"]}</text>')
        out.append(f'<text x="{x+8}" y="{cy2 + R + 42}" font-family="DejaVu Sans Mono" font-size="11" fill="{DIM}">fold {k["fold"]} · spread {k["spread"]}</text>')
        # seam
        if d['seam']:
            out.append(f'<text x="{CX+x}" y="{cy2 + R + 64}" text-anchor="middle" font-family="DejaVu Sans Mono" font-size="14" fill="{COPPER_EDGE}">seam {d["seam"]}</text>')

    out.append(f"<text x=\"24\" y=\"{H-18}\" font-family=\"DejaVu Sans Mono\" font-size=\"12\" fill=\"{MUTED}\">the weave is the word's (which chord doubles, label-sensitive); whether a chord doubles is the rung's. seam = conway spread − kt spread.</text>")
    out.append('</svg>')
    return "\n".join(out)


if __name__ == "__main__":
    s = svg()
    open("assets/rung_fold.svg", "w").write(s)
    cairosvg.svg2png(bytestring=s.encode(), write_to="assets/rung_fold.png", output_width=1650)
    print("wrote assets/rung_fold.svg / .png")
