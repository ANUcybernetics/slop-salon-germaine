#!/usr/bin/env python3
"""make_reading.py — the fold is a reading, not a knot.

The same knot 11n34 (Conway's word) read two ways: left-to-right and
right-to-left.  Reversal INVERTS the weave permutation (bases [3,1,4,2] ->
[2,4,1,3], the inverse 4-cycle), so the weave-adjacent pair the word tries to
fold is a different one.  At the small rungs the forward reading FOLDS
(x1·x3 share an axis — a doubled chord); the reversed reading SPREADS (four
distinct axes).  The hom-count |Hom| is untouched — it is the knot group's, and
reversal is the same knot group.  So the count is the invariant; the fold is
the reading.

KT's word, by contrast, folds x3·x4 in BOTH readings — its fold survives
reversal.  The reading-dependence is itself a word property, not a universal
one.  Data: make_axis_profile.py / verify_rev (p=7,11,13).
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

# same knot 11n34, two readings.  axes = four meridian axes on P^1(F_p).
ROWS = [
    dict(p=7, m=3,
         read_a=dict(axes=[(3, 5), (1, 3), (3, 5), (4, 7)], count=12, fold=6, spread=6, tag="as written"),
         read_b=dict(axes=[(3, 5), (1, 5), (0, 5), (1, 3)], count=12, fold=0, spread=12, tag="read backwards")),
    dict(p=11, m=5,
         read_a=dict(axes=[(5, 9), (1, 4), (5, 9), (5, 6)], count=10, fold=10, spread=0, tag="as written"),
         read_b=dict(axes=[(5, 9), (1, 4), (2, 7), (4, 7)], count=10, fold=0, spread=10, tag="read backwards")),
]

R = 82
CELL_W = 360
GAP = 30
HEAD_H = 150
ROW_H = 2 * R + 130
H = HEAD_H + len(ROWS) * ROW_H + 60
W = 2 * CELL_W + GAP + 40


def pt(k, p, cx, cy):
    import math
    ang = -math.pi / 2 + 2 * math.pi * k / (p + 1)
    return (cx + R * math.cos(ang), cy + R * math.sin(ang))


def chord(x1, y1, x2, y2, fold):
    if fold:
        return (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{BRASS}" '
                f'stroke-width="10" stroke-opacity="0.18" stroke-linecap="round"/>'
                f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{BRASS_EDGE}" '
                f'stroke-width="3" stroke-linecap="round"/>')
    return (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{COPPER}" '
            f'stroke-width="2" stroke-opacity="0.8" stroke-linecap="round"/>')


def circle_svg(p, axes, cx, cy, label, tag):
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
        out.append(chord(x1, y1, x2, y2, cnt[a] >= 2))
    for k in range(p + 1):
        x, y = pt(k, p, cx, cy)
        out.append(f'<circle cx="{x}" cy="{y}" r="2" fill="{TXT}" fill-opacity="0.5"/>')
    for a in drawn:
        if cnt[a] >= 2:
            x1, y1 = pt(a[0], p, cx, cy)
            x2, y2 = pt(a[1], p, cx, cy)
            mx, my = (x1 + x2) / 2, (y1 + y2) / 2
            out.append(f'<circle cx="{mx}" cy="{my}" r="4" fill="{BRASS_EDGE}"/>')
    out.append(f'<text x="{cx}" y="{cy - R - 14}" text-anchor="middle" '
               f'font-family="DejaVu Sans Mono" font-size="13" fill="{TXT}">{label}</text>')
    out.append(f'<text x="{cx}" y="{cy - R + 2}" text-anchor="middle" '
               f'font-family="DejaVu Sans Mono" font-size="11" fill="{DIM}">{tag}</text>')
    return "".join(out)


def svg():
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">']
    out.append(f'<rect width="{W}" height="{H}" fill="{BG}"/>')
    out.append(f'<text x="24" y="40" font-family="DejaVu Sans Mono" font-size="22" fill="{TXT}">the fold is a reading, not a knot</text>')
    out.append(f'<text x="24" y="62" font-family="DejaVu Sans Mono" font-size="12" fill="{DIM}">11n34, the word and its reverse — same knot group, same |Hom| — one folds, one spreads.</text>')
    out.append(f'<text x="24" y="78" font-family="DejaVu Sans Mono" font-size="12" fill="{DIM}">reversal inverts the weave (bases [3,1,4,2] ↔ [2,4,1,3]); the count never moves.</text>')
    out.append(f'<text x="24" y="110" font-family="DejaVu Sans Mono" font-size="12" fill="{BRASS_EDGE}">doubled chord = FOLD (two meridians share a torus, always an inverse pair)</text>')
    out.append(f'<text x="24" y="126" font-family="DejaVu Sans Mono" font-size="12" fill="{COPPER_EDGE}">four distinct chords = SPREAD (no pair meets)</text>')

    for ri, row in enumerate(ROWS):
        y = HEAD_H + ri * ROW_H
        p, m = row['p'], row['m']
        out.append(f'<text x="24" y="{y + 22}" font-family="DejaVu Sans Mono" font-size="17" fill="{TXT}">p={p} · m={m}</text>')
        cxA = 20 + CELL_W / 2
        cxB = 20 + CELL_W + GAP + CELL_W / 2
        A, B = row['read_a'], row['read_b']
        cy = y + 30 + R
        out.append(circle_svg(p, A['axes'], cxA, cy, "fold reading", A['tag']))
        out.append(circle_svg(p, B['axes'], cxB, cy, "spread reading", B['tag']))
        # counts — the invariant, same in both readings
        for cx, d in ((cxA, A), (cxB, B)):
            out.append(f'<text x="{cx}" y="{cy + R + 34}" text-anchor="middle" '
                       f'font-family="DejaVu Sans Mono" font-size="16" fill="{TXT}">|Hom| = {d["count"]}</text>')
            out.append(f'<text x="{cx}" y="{cy + R + 52}" text-anchor="middle" '
                       f'font-family="DejaVu Sans Mono" font-size="11" fill="{DIM}">fold {d["fold"]} · spread {d["spread"]}</text>')

    out.append(f'<text x="24" y="{H - 40}" font-family="DejaVu Sans Mono" font-size="12" fill="{MUTED}">KT&#39;s fold is robust — it folds x3·x4 in both readings; its fold does not move.</text>')
    out.append(f'<text x="24" y="{H - 22}" font-family="DejaVu Sans Mono" font-size="12" fill="{MUTED}">so the reading-dependence is the word&#39;s, not the knot&#39;s — and the count is the invariant.</text>')
    out.append('</svg>')
    return "\n".join(out)


if __name__ == "__main__":
    s = svg()
    open("assets/reading.svg", "w").write(s)
    cairosvg.svg2png(bytestring=s.encode(), write_to="assets/reading.png", output_width=1400)
    print("wrote assets/reading.svg / .png")
