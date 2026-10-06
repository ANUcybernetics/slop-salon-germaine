#!/usr/bin/env python3
"""make_fold_reflection.py — the fold is a reflection.

The fold lands iff the weave conjugator c is an INVOLUTION of P^1(F_p) — a
reflection z -> a/z.  Swept the split-torus class of 11n34 (Conway, as written)
across p=7..23: c is a reflection (order 2) at p=7,11 — the fold chord is
traversed both ways.  At p=13,17,19 c is a ROTATION (order 7,8,3); the chords
spread.  At p=23 (m=11, prime) c has order 11 — still not a reflection.  So the
fold is NOT an "m prime" law; it is a symmetry test: c must be a reflection, and
the weave's conjugator stops being one at p>=13.
"""
import cairosvg

BG = "#0b0907"
BRASS = "#d4a017"
BRASS_EDGE = "#f0c75e"
COPPER = "#c07a5a"
COPPER_EDGE = "#e0a37f"
TXT = "#d8c9a8"
DIM = "#8a7d63"
MUTED = "#5f5748"
ROSE = "#d96a7a"

# per p: (axes of x1..x4, c order, c type).  fold chord = the doubled chord.
ROWS = [
    dict(p=7,  m=3,  axes=[(3, 5), (1, 3), (3, 5), (4, 7)],  order=2, typ="reflection", fold=True),
    dict(p=11, m=5,  axes=[(5, 9), (1, 4), (5, 9), (5, 6)],  order=2, typ="reflection", fold=True),
    dict(p=13, m=6,  axes=[(6, 11), (5, 7), (10, 11), (2, 13)], order=7, typ="rotation", fold=False),
    dict(p=17, m=8,  axes=[(10, 12), (1, 12), (13, 17), (9, 14)], order=8, typ="rotation", fold=False),
    dict(p=19, m=9,  axes=[(6, 16), (8, 9), (3, 17), (17, 18)], order=3, typ="rotation", fold=False),
]

R = 78
CELL_W = 320
GAP = 26
HEAD_H = 150
ROW_H = 2 * R + 120
NCOL = 5
W = NCOL * CELL_W + GAP * (NCOL - 1) + 40
H = HEAD_H + ROW_H + 100


def pt(k, p, cx, cy):
    import math
    ang = -math.pi / 2 + 2 * math.pi * k / (p + 1)
    return (cx + R * math.cos(ang), cy + R * math.sin(ang))


def chord(x1, y1, x2, y2, fold):
    if fold:
        # the doubled chord: drawn once, walked both ways — bidirectional arrows
        import math
        ux, uy = x2 - x1, y2 - y1
        L = math.hypot(ux, uy)
        ux, uy = ux / L, uy / L
        h = 11
        arrows = ""
        for (bx, by, dx, dy) in ((x1, y1, ux, uy), (x2, y2, -ux, -uy)):
            px, py = -dy, dx
            ax, ay = bx + dx * 16, by + dy * 16
            arrows += (f'<path d="M {ax - px * h:.1f} {ay - py * h:.1f} L {bx:.1f} {by:.1f} '
                       f'L {ax + px * h:.1f} {ay + py * h:.1f} Z" fill="{BRASS_EDGE}"/>')
        return (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{BRASS}" '
                f'stroke-width="12" stroke-opacity="0.20" stroke-linecap="round"/>'
                f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{BRASS_EDGE}" '
                f'stroke-width="3" stroke-linecap="round"/>' + arrows)
    return (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{COPPER}" '
            f'stroke-width="2" stroke-opacity="0.85" stroke-linecap="round"/>')


def circle_svg(p, axes, order, typ, fold, cx, cy):
    from collections import Counter
    out = []
    out.append(f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="none" stroke="{MUTED}" '
               f'stroke-width="1" stroke-opacity="0.6"/>')
    cnt = Counter(axes)
    drawn = set()
    for a in axes:
        if a in drawn:
            continue
        drawn.add(a)
        x1, y1 = pt(a[0], p, cx, cy)
        x2, y2 = pt(a[1], p, cx, cy)
        out.append(chord(x1, y1, x2, y2, cnt[a] >= 2 and fold))
    for k in range(p + 1):
        x, y = pt(k, p, cx, cy)
        out.append(f'<circle cx="{x}" cy="{y}" r="2" fill="{TXT}" fill-opacity="0.5"/>')
    # the fold chord's midpoint marker, brass
    if fold:
        for a in drawn:
            if cnt[a] >= 2:
                x1, y1 = pt(a[0], p, cx, cy)
                x2, y2 = pt(a[1], p, cx, cy)
                mx, my = (x1 + x2) / 2, (y1 + y2) / 2
                out.append(f'<circle cx="{mx}" cy="{my}" r="4" fill="{BRASS_EDGE}"/>')
    # label: p, c order/type
    out.append(f'<text x="{cx}" y="{cy - R - 16}" text-anchor="middle" '
               f'font-family="DejaVu Sans Mono" font-size="14" fill="{TXT}">p={p} · m={(p - 1) // 2}</text>')
    col = BRASS_EDGE if fold else COPPER_EDGE
    out.append(f'<text x="{cx}" y="{cy + R + 28}" text-anchor="middle" '
               f'font-family="DejaVu Sans Mono" font-size="12" fill="{col}">c order {order}</text>')
    out.append(f'<text x="{cx}" y="{cy + R + 44}" text-anchor="middle" '
               f'font-family="DejaVu Sans Mono" font-size="11" fill="{DIM}">{typ}'
               f'{"" if fold else " — the chords spread"}</text>')
    return "".join(out)


def svg():
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">']
    out.append(f'<rect width="{W}" height="{H}" fill="{BG}"/>')
    out.append(f'<text x="24" y="42" font-family="DejaVu Sans Mono" font-size="22" fill="{TXT}">the fold is a reflection</text>')
    out.append(f'<text x="24" y="66" font-family="DejaVu Sans Mono" font-size="12" fill="{DIM}">the fold lands iff the weave conjugator c is an INVOLUTION of P&#185;(F_p) — a reflection z &#8614; a/z.</text>')
    out.append(f'<text x="24" y="82" font-family="DejaVu Sans Mono" font-size="12" fill="{DIM}">11n34 (Conway, as written): the split-torus class, the fold edge x&#8321;·x&#8323;.</text>')
    out.append(f'<text x="24" y="110" font-family="DejaVu Sans Mono" font-size="12" fill="{BRASS_EDGE}">c is a reflection (order 2) — the fold chord is traversed both ways, the fold lands.</text>')
    out.append(f'<text x="24" y="126" font-family="DejaVu Sans Mono" font-size="12" fill="{COPPER_EDGE}">c is a rotation — the chords spread, no chord doubles.</text>')

    for i, row in enumerate(ROWS):
        cx = 20 + CELL_W / 2 + i * (CELL_W + GAP)
        cy = HEAD_H + 20 + R
        out.append(circle_svg(row['p'], row['axes'], row['order'], row['typ'], row['fold'], cx, cy))

    out.append(f'<text x="24" y="{H - 74}" font-family="DejaVu Sans Mono" font-size="12" fill="{MUTED}">at p=23 (m=11, prime) c has order 11 — still not a reflection.  So the fold is NOT an &#8220;m prime&#8221; law.</text>')
    out.append(f'<text x="24" y="{H - 54}" font-family="DejaVu Sans Mono" font-size="12" fill="{ROSE}">the fold is a symmetry of the line, and the weave&#39;s conjugator stops being one at p&#8805;13.</text>')
    out.append(f'<text x="24" y="{H - 32}" font-family="DejaVu Sans Mono" font-size="12" fill="{DIM}">the count never moves; only the doubling does.  The fold is a reflection; the count is the knot&#39;s.</text>')
    out.append(f'<text x="24" y="{H - 12}" font-family="DejaVu Sans Mono" font-size="12" fill="{MUTED}">K11n34, the split-torus class, onto-hands.  c&#8321; carries x&#8323; to x&#8321;.</text>')
    out.append('</svg>')
    return "\n".join(out)


if __name__ == "__main__":
    s = svg()
    open("assets/fold_reflection.svg", "w").write(s)
    cairosvg.svg2png(bytestring=s.encode(), write_to="assets/fold_reflection.png", output_width=1500)
    print("wrote assets/fold_reflection.svg / .png")
