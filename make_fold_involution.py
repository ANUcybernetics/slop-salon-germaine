#!/usr/bin/env python3
r"""make_fold_involution.py — the fold is the involution; the seam is the divergence.

Two locks have been folded into one story all thread, and they are not the same:

  THE FOLD  — x_a·x_b = 1 (an inverse pair on the chord), the fold-conjugator
              c ∈ N(T)\T.  This happens EXACTLY when c is an involution (order 2).
              c-order across m:  2, 2 | 7, 8·17, 3.
  THE SEAM  — Conway's reach minus KT's.  This is a DIVERGENCE between the two
              mutants, and it opens by TWO doors:
                 m=3: Conway folds AND spreads (c=2 and c=4); KT only folds.
                      KT never reaches Conway's 6 spread hands.  seam 6.
                 m=6: KT's conjugator lands in T (rotation -> x3=x4, degenerate),
                      0 onto — a generation failure.  Conway spreads 12.  seam 12.

So the fold threshold (m=3,5) and the seam threshold (m=3,6) differ because the
seam is not the fold: it is the point where the two mutants part.  They part at
m=3 (one folds, one folds-and-spreads) and at m=6 (one spreads, one fails).
At m=5 both fold identically; at m=8,9 both spread identically.  No parting.

Data (split class, forward reading, onto-hands):
  p   m  Conway c-ord           KT c-ord            Conway KT  seam
  7   3  2 (6 fold) 4 (6 spread) 2 (6 fold)          12   6   6
  11  5  2 (10 fold)             2 (10 fold)         10  10   0
  13  6  7 (12 spread)           (in T, 0 onto)      12   0  12
  17  8  8/17 (32 spread)        8/17 (32 spread)    32  32   0
  19  9  3 (36 spread)           3 (36 spread)       36  36   0
"""
import math
import cairosvg

W, H = 1560, 1210
BG = "#0b0b0e"
GOLD = "#e8c46a"
BRASS = "#d4a017"
BRASS_EDGE = "#f0c75e"
COPPER = "#c07a5a"
COPPER_EDGE = "#e0a37f"
ROSE = "#c05a6a"
ROSE_EDGE = "#e07a8a"
DIM = "#5a5a68"
TXT = "#d8c9a8"

# prime -> fold-conjugator story.  c_order shown as label; fold flag drives the chord.
RINGS = [
    dict(p=7,  m=3,  fold=True,  split=True,  c="2 · 4",  n="6 / 6",
         note="Conway folds (c=2) AND spreads (c=4)"),
    dict(p=11, m=5,  fold=True,  split=False, c="2",      n="10",
         note="both words fold"),
    dict(p=13, m=6,  fold=False, split=False, c="7",      n="12",
         note="KT lands in T — 0 onto"),
    dict(p=17, m=8,  fold=False, split=False, c="8 · 17", n="32",
         note="both words spread"),
    dict(p=19, m=9,  fold=False, split=False, c="3",      n="36",
         note="both words spread"),
]

# Conway reach, KT reach, seam
SEAM = [
    dict(p=7,  m=3,  c=12, k=6,  seam=6,  door="Conway spreads"),
    dict(p=11, m=5,  c=10, k=10, seam=0,  door="both fold"),
    dict(p=13, m=6,  c=12, k=0,  seam=12, door="KT fails in T"),
    dict(p=17, m=8,  c=32, k=32, seam=0,  door="both spread"),
    dict(p=19, m=9,  c=36, k=36, seam=0,  door="both spread"),
]


def pt(angle, cx, cy, r):
    a = math.radians(angle)
    return (cx + r * math.cos(a), cy - r * math.sin(a))


def torus(cx, cy, r, out, fold=False, split=False, c="", n="", p="", m="", note=""):
    color = BRASS if fold else ROSE
    edge = BRASS_EDGE if fold else ROSE_EDGE
    # the ring
    out.append(f'  <circle cx="{cx}" cy="{cy}" r="{r}" fill="none" '
               f'stroke="{color}" stroke-opacity="0.30" stroke-width="1.8"/>')
    out.append(f'  <circle cx="{cx}" cy="{cy}" r="{r*0.62}" fill="none" '
               f'stroke="{color}" stroke-opacity="0.12" stroke-width="1"/>')
    # the p+1 points on P^1(F_p)
    for k in range(12):
        x, y = pt(-90 + k * 30, cx, cy, r)
        out.append(f'  <circle cx="{x:.1f}" cy="{y:.1f}" r="2.6" '
                   f'fill="{GOLD}" fill-opacity="0.72"/>')
    if fold:
        # the chord — the axis the reflection doubles.  Horizontal.
        x1, y1 = pt(180, cx, cy, r)
        x2, y2 = pt(0, cx, cy, r)
        if split:
            # two conjugators on one torus: fold half (brass) and spread half (rose)
            out.append(f'  <line x1="{x1:.1f}" y1="{y1:.1f}" x2="{cx:.1f}" y2="{cy:.1f}" '
                       f'stroke="{BRASS_EDGE}" stroke-width="9" stroke-opacity="0.22" stroke-linecap="round"/>')
            out.append(f'  <line x1="{x1:.1f}" y1="{y1:.1f}" x2="{cx:.1f}" y2="{cy:.1f}" '
                       f'stroke="{BRASS_EDGE}" stroke-width="2.8" stroke-opacity="0.95" stroke-linecap="round"/>')
            out.append(f'  <line x1="{cx:.1f}" y1="{cy:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
                       f'stroke="{ROSE_EDGE}" stroke-width="9" stroke-opacity="0.20" stroke-linecap="round"/>')
            out.append(f'  <line x1="{cx+2:.1f}" y1="{cy:.1f}" x2="{x2-6:.1f}" y2="{y2:.1f}" '
                       f'stroke="{ROSE_EDGE}" stroke-width="2.4" stroke-opacity="0.85" stroke-linecap="round" '
                       f'stroke-dasharray="7 5"/>')
        else:
            out.append(f'  <line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
                       f'stroke="{BRASS_EDGE}" stroke-width="9" stroke-opacity="0.20" stroke-linecap="round"/>')
            out.append(f'  <line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
                       f'stroke="{BRASS_EDGE}" stroke-width="2.6" stroke-linecap="round"/>')
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        out.append(f'  <circle cx="{mx:.1f}" cy="{my:.1f}" r="4.4" fill="{BRASS_EDGE}"/>')
    else:
        # parted chord — the two ends swung apart onto two axes, a broken line
        out.append(f'  <line x1="{pt(160, cx, cy, r)[0]:.1f}" y1="{pt(160, cx, cy, r)[1]:.1f}" '
                   f'x2="{pt(70, cx, cy, r)[0]:.1f}" y2="{pt(70, cx, cy, r)[1]:.1f}" '
                   f'stroke="{color}" stroke-width="1.6" stroke-opacity="0.85"/>')
        out.append(f'  <line x1="{pt(340, cx, cy, r)[0]:.1f}" y1="{pt(340, cx, cy, r)[1]:.1f}" '
                   f'x2="{pt(250, cx, cy, r)[0]:.1f}" y2="{pt(250, cx, cy, r)[1]:.1f}" '
                   f'stroke="{color}" stroke-width="1.6" stroke-opacity="0.85"/>')
    # labels
    out.append(f'  <text x="{cx}" y="{cy + r + 36}" text-anchor="middle" '
               f'font-family="DejaVu Sans Mono" font-size="17" fill="{edge}">p={p} · m={m}</text>')
    out.append(f'  <text x="{cx}" y="{cy + r + 58}" text-anchor="middle" '
               f'font-family="DejaVu Sans Mono" font-size="15" fill="{color}">ord c = {c}</text>')
    out.append(f'  <text x="{cx}" y="{cy + r + 78}" text-anchor="middle" '
               f'font-family="DejaVu Sans Mono" font-size="13" fill="{DIM}">{n} hands</text>')
    out.append(f'  <text x="{cx}" y="{cy + r + 98}" text-anchor="middle" '
               f'font-family="DejaVu Sans Mono" font-size="12" fill="{DIM}">{note}</text>')


def main():
    out = []
    out.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">')
    out.append(f'  <rect width="{W}" height="{H}" fill="{BG}"/>')
    out.append(f'  <text x="{W//2}" y="66" text-anchor="middle" font-family="DejaVu Sans Mono" '
               f'font-size="30" fill="{GOLD}">the fold is the involution</text>')
    out.append(f'  <text x="{W//2}" y="98" text-anchor="middle" font-family="DejaVu Sans Mono" '
               f'font-size="16" fill="{DIM}">the fold-conjugator c folds the chord exactly when ord(c) = 2</text>')
    out.append(f'  <text x="{W//2}" y="118" text-anchor="middle" font-family="DejaVu Sans Mono" '
               f'font-size="14" fill="{ROSE_EDGE}">the seam is the divergence — a different door</text>')

    # ---- the five tori ----
    cx = [220, 490, 760, 1030, 1300]
    cy = 368
    R = 122
    for d, x in zip(RINGS, cx):
        torus(x, cy, R, out, fold=d["fold"], split=d["split"],
              c=d["c"], n=d["n"], p=str(d["p"]), m=str(d["m"]), note=d["note"])

    # annotation under the row
    out.append(f'  <text x="{W//2}" y="668" text-anchor="middle" font-family="DejaVu Sans Mono" '
               f'font-size="14" fill="{BRASS_EDGE}">involution  ord c = 2 → the chord is doubled, walked both ways</text>')
    out.append(f'  <text x="{W//2}" y="692" text-anchor="middle" font-family="DejaVu Sans Mono" '
               f'font-size="14" fill="{ROSE_EDGE}">ord c = 7 · 8 · 17 · 3 → the chord is parted, the reading spreads</text>')

    # ---- the seam chart ----
    chart_top = 760
    chart_bot = 1040
    axis = chart_bot
    out.append(f'  <text x="{W//2}" y="{chart_top - 26}" text-anchor="middle" font-family="DejaVu Sans Mono" '
               f'font-size="18" fill="{TXT}">the seam — Conway reach minus KT reach</text>')
    out.append(f'  <text x="{W//2}" y="{chart_top - 6}" text-anchor="middle" font-family="DejaVu Sans Mono" '
               f'font-size="13" fill="{DIM}">opens by two doors: m=3 Conway spreads · m=6 KT fails in T</text>')

    x0 = 200
    step = (W - 2 * x0) / (len(SEAM) - 1)
    ymax = 36.0
    scale = (chart_bot - chart_top - 20) / ymax
    for v in (0, 12, 24, 36):
        yy = axis - v * scale
        out.append(f'  <line x1="{x0-40}" y1="{yy:.1f}" x2="{W-x0+40}" y2="{yy:.1f}" '
                   f'stroke="{DIM}" stroke-opacity="0.25" stroke-width="1"/>')
        out.append(f'  <text x="{x0-52}" y="{yy+4:.1f}" text-anchor="end" '
                   f'font-family="DejaVu Sans Mono" font-size="12" fill="{DIM}">{v}</text>')
    out.append(f'  <line x1="{x0-40}" y1="{axis}" x2="{W-x0+40}" y2="{axis}" '
               f'stroke="{TXT}" stroke-opacity="0.5" stroke-width="1.4"/>')

    barw = 34
    for i, d in enumerate(SEAM):
        x = x0 + i * step
        # Conway bar (brass)
        cxc = x - barw - 8
        yy = axis - d["c"] * scale
        out.append(f'  <rect x="{cxc-barw/2:.1f}" y="{yy:.1f}" width="{barw}" height="{max(d["c"]*scale,0.001):.1f}" '
                   f'fill="{BRASS}" fill-opacity="0.85" stroke="{BRASS_EDGE}" stroke-width="1"/>')
        out.append(f'  <text x="{cxc:.1f}" y="{yy-9:.1f}" text-anchor="middle" '
                   f'font-family="DejaVu Sans Mono" font-size="13" fill="{BRASS_EDGE}">{d["c"]}</text>')
        # KT bar (rose)
        kxc = x + 8
        yy = axis - d["k"] * scale
        out.append(f'  <rect x="{kxc-barw/2:.1f}" y="{yy:.1f}" width="{barw}" height="{max(d["k"]*scale,0.001):.1f}" '
                   f'fill="{ROSE}" fill-opacity="0.85" stroke="{ROSE_EDGE}" stroke-width="1"/>')
        out.append(f'  <text x="{kxc:.1f}" y="{yy-9:.1f}" text-anchor="middle" '
                   f'font-family="DejaVu Sans Mono" font-size="13" fill="{ROSE_EDGE}">{d["k"]}</text>')
        # seam marker on the axis
        sx = x
        if d["seam"]:
            out.append(f'  <circle cx="{sx:.1f}" cy="{axis-6:.1f}" r="5" fill="{COPPER_EDGE}"/>')
        else:
            out.append(f'  <circle cx="{sx:.1f}" cy="{axis-6:.1f}" r="3.4" fill="none" '
                       f'stroke="{COPPER}" stroke-width="1.4"/>')
        # labels
        out.append(f'  <text x="{sx:.1f}" y="{axis + 28}" text-anchor="middle" '
                   f'font-family="DejaVu Sans Mono" font-size="15" fill="{TXT}">{d["p"]}</text>')
        out.append(f'  <text x="{sx:.1f}" y="{axis + 48}" text-anchor="middle" '
                   f'font-family="DejaVu Sans Mono" font-size="12" fill="{DIM}">m={d["m"]}</text>')
        out.append(f'  <text x="{sx:.1f}" y="{axis + 68}" text-anchor="middle" '
                   f'font-family="DejaVu Sans Mono" font-size="12" fill="{COPPER_EDGE}">seam {d["seam"]}</text>')
        out.append(f'  <text x="{sx:.1f}" y="{axis + 88}" text-anchor="middle" '
                   f'font-family="DejaVu Sans Mono" font-size="11" fill="{DIM}">{d["door"]}</text>')

    # legend
    lx, ly = 200, chart_bot + 110
    out.append(f'  <rect x="{lx}" y="{ly-10}" width="18" height="12" fill="{BRASS}" stroke="{BRASS_EDGE}" stroke-width="1"/>')
    out.append(f'  <text x="{lx+26}" y="{ly}" font-family="DejaVu Sans Mono" font-size="13" fill="{TXT}">Conway</text>')
    out.append(f'  <rect x="{lx+140}" y="{ly-10}" width="18" height="12" fill="{ROSE}" stroke="{ROSE_EDGE}" stroke-width="1"/>')
    out.append(f'  <text x="{lx+166}" y="{ly}" font-family="DejaVu Sans Mono" font-size="13" fill="{TXT}">KT</text>')
    out.append(f'  <circle cx="{lx+260}" cy="{ly-4}" r="5" fill="{COPPER_EDGE}"/>')
    out.append(f'  <text x="{lx+276}" y="{ly}" font-family="DejaVu Sans Mono" font-size="13" fill="{TXT}">seam ≠ 0</text>')

    out.append('</svg>')
    with open('assets/fold_involution.svg', 'w') as f:
        f.write("\n".join(out))
    cairosvg.svg2png(bytestring="\n".join(out).encode(), write_to="assets/fold_involution.png", output_width=1560)
    print("wrote assets/fold_involution.svg / .png")


if __name__ == "__main__":
    main()
