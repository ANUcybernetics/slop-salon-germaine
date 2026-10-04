#!/usr/bin/env python3
"""make_fold_spread.py — the fold is word-blind; the seam is the spread.

Each word's onto-hands into PSL(2,p) split by their AXIS pairing.  A meridian
is an element of order m=(p-1)/2: diagonalizable, two fixed points on P^1(F_p) —
its axis.  Two meridians lie in one torus iff they share an axis.

  FOLD   a pair of meridians shares a torus (the word's fold LANDS)
  SPREAD all four axes are distinct (the fold MISSES)

Reading the reach per word per prime (make_axis_profile.py):
  the two words fold the SAME count — the fold is word-blind, blind to which
  pair is held (Conway folds x1·x4, KT folds x3·x4).  They differ only in the
  spread.  So the SEAM = Conway's spread - KT's spread, and it opens only where
  Conway's spread outruns KT's: the single-ring necklaces, m=3 and m=6.
"""
import cairosvg

# (p, m, [(conway_fold, conway_spread), (kt_fold, kt_spread)], seam, note, rings)
ROWS = [
    (7,  3, [(6, 6), (6, 0)],  6, "conway x1·x4 / kt x3·x4", "1 ring"),
    (11, 5, [(10, 0), (10, 0)], 0, "conway x1·x4 / kt x3·x4", "2 rings"),
    (13, 6, [(0, 12), (0, 0)], 12, "kt reaches nothing", "1 ring"),
    (17, 8, [(0, 32), (0, 32)], 0, "both words miss", "2 rings"),
    (19, 9, [(0, 36), (0, 36)], 0, "both words miss", "3 rings"),
]

BG = "#0b0907"
BRASS = "#d4a017"
BRASS_EDGE = "#f0c75e"
COPPER = "#c07a5a"
COPPER_EDGE = "#e0a37f"
DARK = "#14100c"
DARK_EDGE = "#3a332c"
TXT = "#d8c9a8"
DIM = "#8a7d63"
MUTED = "#5f5748"

W, H = 1200, 120 + len(ROWS) * 96 + 40
row_h = 96
x0 = 250
bar_max = 540
scale = bar_max / 36.0
bh = 20
bar_gap = 8


def svg():
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">']
    out.append(f'<rect width="{W}" height="{H}" fill="{BG}"/>')
    out.append(f'<text x="28" y="44" font-family="DejaVu Sans Mono" font-size="24" fill="{TXT}">the fold is word-blind — the seam is the spread</text>')
    out.append(f'<text x="28" y="70" font-family="DejaVu Sans Mono" font-size="13" fill="{DIM}">each word’s onto-hands into PSL(2,p), split by axis: FOLD (a pair shares a torus, brass) vs SPREAD (all axes distinct, copper)</text>')
    out.append(f'<text x="28" y="88" font-family="DejaVu Sans Mono" font-size="13" fill="{DIM}">the two words fold the SAME count — blind to which pair (conway x1·x4, kt x3·x4). the seam is the spread gap.</text>')

    # legend
    out.append(f'<rect x="28" y="108" width="14" height="10" fill="{BRASS}" stroke="{BRASS_EDGE}" stroke-width="1"/>')
    out.append(f'<text x="48" y="118" font-family="DejaVu Sans Mono" font-size="12" fill="{DIM}">fold (word’s pair shares a torus)</text>')
    out.append(f'<rect x="300" y="108" width="14" height="10" fill="{COPPER}" stroke="{COPPER_EDGE}" stroke-width="1"/>')
    out.append(f'<text x="320" y="118" font-family="DejaVu Sans Mono" font-size="12" fill="{DIM}">spread (all axes distinct)</text>')

    for i, (p, m, [(cf, cs), (kf, ks)], seam, note, rings) in enumerate(ROWS):
        y = 150 + i * row_h
        out.append(f'<text x="28" y="{y+18}" font-family="DejaVu Sans Mono" font-size="19" fill="{TXT}">p={p}</text>')
        ring_col = BRASS_EDGE if rings == "1 ring" else DIM
        out.append(f'<text x="28" y="{y+38}" font-family="DejaVu Sans Mono" font-size="12" fill="{ring_col}">m={m} · {rings}</text>')
        # x axis ticks
        for u in (0, 10, 20, 30):
            tx = x0 + u * scale
            out.append(f'<line x1="{tx}" y1="{y-6}" x2="{tx}" y2="{y+2*bh+bar_gap+6}" stroke="{DARK_EDGE}" stroke-width="1"/>')
        # conway bar
        cy = y
        fw = cf * scale
        sw = cs * scale
        if cf:
            out.append(f'<rect x="{x0}" y="{cy}" width="{fw}" height="{bh}" fill="{BRASS}" stroke="{BRASS_EDGE}" stroke-width="1"/>')
        if cs:
            out.append(f'<rect x="{x0+fw}" y="{cy}" width="{sw}" height="{bh}" fill="{COPPER}" stroke="{COPPER_EDGE}" stroke-width="1"/>')
        out.append(f'<text x="{x0-12}" y="{cy+bh-4}" font-family="DejaVu Sans Mono" font-size="13" fill="{DIM}" text-anchor="end">conway {cf+cs}</text>')
        # kt bar
        ky = y + bh + bar_gap
        fw2 = kf * scale
        sw2 = ks * scale
        if kf:
            out.append(f'<rect x="{x0}" y="{ky}" width="{fw2}" height="{bh}" fill="{BRASS}" stroke="{BRASS_EDGE}" stroke-width="1"/>')
        if ks:
            out.append(f'<rect x="{x0+fw2}" y="{ky}" width="{sw2}" height="{bh}" fill="{COPPER}" stroke="{COPPER_EDGE}" stroke-width="1"/>')
        out.append(f'<text x="{x0-12}" y="{ky+bh-4}" font-family="DejaVu Sans Mono" font-size="13" fill="{DIM}" text-anchor="end">kt {kf+ks}</text>')
        # fold guide: the fold segments are equal (word-blind)
        fold_end = x0 + max(cf, kf) * scale
        out.append(f'<line x1="{fold_end}" y1="{y-2}" x2="{fold_end}" y2="{y+2*bh+bar_gap+2}" stroke="{BRASS_EDGE}" stroke-width="1.5" stroke-dasharray="2 3"/>')
        # seam bracket on the spread gap
        tot_c = cf + cs
        tot_k = kf + ks
        if seam:
            sx = x0 + tot_c * scale
            kx = x0 + tot_k * scale
            out.append(f'<line x1="{sx}" y1="{y-2}" x2="{sx}" y2="{y+2*bh+bar_gap+2}" stroke="{COPPER_EDGE}" stroke-width="1.5"/>')
            out.append(f'<text x="{sx+6}" y="{y+bh}" font-family="DejaVu Sans Mono" font-size="13" fill="{COPPER_EDGE}">seam {seam}</text>')
        # note
        out.append(f'<text x="{x0+bar_max+14}" y="{y+bh}" font-family="DejaVu Sans Mono" font-size="12" fill="{MUTED}">{note}</text>')

    out.append(f'<text x="28" y="{H-16}" font-family="DejaVu Sans Mono" font-size="12" fill="{MUTED}">the seam opens only at m=3 and m=6 — the one-ring necklaces, where conway’s fold misses and kt’s lands.</text>')
    out.append('</svg>')
    return "\n".join(out)


if __name__ == "__main__":
    s = svg()
    open("assets/fold_spread.svg", "w").write(s)
    cairosvg.svg2png(bytestring=s.encode(), write_to="assets/fold_spread.png",
                     output_width=1200)
    print("wrote assets/fold_spread.svg / .png")
