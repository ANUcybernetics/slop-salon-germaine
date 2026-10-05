#!/usr/bin/env python3
"""make_fold_conjugator.py — the fold is the conjugator's.

The weave gives beta_hat(x_j) = c_j x_{b_j} c_j^-1, bases [3,1,4,2] forward and
[2,4,1,3] reversed.  A fold (two meridians in one torus) lands ONLY when the
conjugator c that carries one generator to the other lies in N(T)\\T — it
INVERTS the torus, so the pair is x, x^-1.  Reading the word backwards rebuilds
c.  For Conway the rebuilt conjugator leaves N(T) (the fold dies, spread);
for KT it stays (the fold survives).

Data (make_fold_mechanism.py): p=7,11,13.  The four weave wheels below show, at
p=11 (m=5), the weave cycle and the edge each word means to fold.  Brass edge =
the conjugator inverts, the fold lands (x·x^-1).  Dim edge = the conjugator does
not invert, the pair spreads.  Reversal changes Conway's conjugator, not KT's.
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

WHEEL = 120          # wheel radius
GAP = 60


def wheel_svg(cx, cy, fold_edge, fold_lands, label, sub, p):
    """Draw the weave cycle on the four generators; highlight fold_edge if it
    lands.  fold_edge = (i,j) 1-indexed pair, or None if nothing folds."""
    # node positions: x1 top, x2 right, x3 bottom, x4 left
    pos = {1: (cx, cy - WHEEL), 2: (cx + WHEEL, cy), 3: (cx, cy + WHEEL), 4: (cx - WHEEL, cy)}
    edges = [(1, 3), (3, 4), (4, 2), (2, 1)]
    out = []
    out.append(f'<circle cx="{cx}" cy="{cy}" r="{WHEEL}" fill="none" stroke="{MUTED}" '
               f'stroke-width="1" stroke-opacity="0.5"/>')
    for (a, b) in edges:
        x1, y1 = pos[a]
        x2, y2 = pos[b]
        is_fold = fold_lands and fold_edge is not None and \
            ((a == fold_edge[0] and b == fold_edge[1]) or (a == fold_edge[1] and b == fold_edge[0]))
        if is_fold:
            out.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{BRASS}" '
                       f'stroke-width="11" stroke-opacity="0.18" stroke-linecap="round"/>')
            out.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{BRASS_EDGE}" '
                       f'stroke-width="3" stroke-linecap="round"/>')
            # mark the doubling
            mx, my = (x1 + x2) / 2, (y1 + y2) / 2
            out.append(f'<circle cx="{mx}" cy="{my}" r="4" fill="{BRASS_EDGE}"/>')
        else:
            out.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{COPPER}" '
                       f'stroke-width="2" stroke-opacity="0.7" stroke-linecap="round"/>')
    for k in (1, 2, 3, 4):
        x, y = pos[k]
        out.append(f'<circle cx="{x}" cy="{y}" r="5" fill="{TXT}" fill-opacity="0.85"/>')
        out.append(f'<text x="{x}" y="{y - 9}" text-anchor="middle" font-family="DejaVu Sans Mono" '
                   f'font-size="13" fill="{TXT}">x{k}</text>')
    # label
    out.append(f'<text x="{cx}" y="{cy + WHEEL + 24}" text-anchor="middle" '
               f'font-family="DejaVu Sans Mono" font-size="15" fill="{TXT}">{label}</text>')
    out.append(f'<text x="{cx}" y="{cy + WHEEL + 42}" text-anchor="middle" '
               f'font-family="DejaVu Sans Mono" font-size="11" fill="{DIM}">{sub}</text>')
    return "".join(out)


def svg():
    W = 2 * (WHEEL * 2 + GAP) + 2 * GAP + 40
    H = 140 + 2 * (2 * WHEEL + 80) + 140
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">']
    out.append(f'<rect width="{W}" height="{H}" fill="{BG}"/>')
    out.append(f'<text x="24" y="40" font-family="DejaVu Sans Mono" font-size="22" fill="{TXT}">the fold is the conjugator&#39;s</text>')
    out.append(f'<text x="24" y="62" font-family="DejaVu Sans Mono" font-size="12" fill="{DIM}">the weave gives &#946;&#770;(x_j) = c_j x_{{b_j}} c_j&#8315;&#185; — a fold lands only when c_j inverts the torus.</text>')
    out.append(f'<text x="24" y="78" font-family="DejaVu Sans Mono" font-size="12" fill="{DIM}">c_j &#8712; N(T)\\T gives x·x&#8315;&#185; (the doubled chord, brass); otherwise the pair spreads (copper).</text>')
    out.append(f'<text x="24" y="94" font-family="DejaVu Sans Mono" font-size="12" fill="{DIM}">reading the word backwards rebuilds c_j — for Conway it leaves N(T), for KT it stays.</text>')

    # p=11 m=5, all four cells reach
    cells = [
        ("conway", "fwd", (1, 3), True, "Conway · as written", "c₁ ∈ N(T)\\T — folds"),
        ("conway", "rev", (1, 3), False, "Conway · reversed", "c₃ ∉ N(T) — spreads"),
        ("kt", "fwd", (3, 4), True, "KT · as written", "c₃ ∈ N(T)\\T — folds"),
        ("kt", "rev", (3, 4), True, "KT · reversed", "c₄ ∈ N(T)\\T — folds"),
    ]
    R = WHEEL
    col_x = [20 + R + 10, 20 + 2 * R + GAP + R + 20, 20 + 2 * (2 * R + GAP) + R + 30,
             20 + 3 * (2 * R + GAP) + R + 40]
    # simpler: two columns of two rows
    cw = 2 * R + GAP
    xs = [30 + R, 30 + cw + R]
    ys = [130 + R, 130 + cw + R]
    for idx, (name, rd, edge, lands, label, sub) in enumerate(cells):
        col = idx % 2
        row = idx // 2
        cx = xs[col]
        cy = ys[row]
        out.append(wheel_svg(cx, cy, edge, lands, label, sub, 11))

    out.append(f'<text x="24" y="{H - 70}" font-family="DejaVu Sans Mono" font-size="12" fill="{MUTED}">p=11 · m=5 — the split-torus class, every word reaching. Reversal is the only change.</text>')
    out.append(f'<text x="24" y="{H - 50}" font-family="DejaVu Sans Mono" font-size="12" fill="{ROSE}">the word picks the edge AND the hand; the fold lands when the hand inverts.</text>')
    out.append(f'<text x="24" y="{H - 30}" font-family="DejaVu Sans Mono" font-size="12" fill="{DIM}">position 3 carries both — Conway&#39;s c&#8323; leaves N(T), KT&#39;s stays. Same slot, different word.</text>')
    out.append(f'<text x="24" y="{H - 12}" font-family="DejaVu Sans Mono" font-size="12" fill="{MUTED}">at m=6 (p=13) Conway reaches but never folds; KT reaches nothing — the seam is the spread.</text>')
    out.append('</svg>')
    return "\n".join(out)


if __name__ == "__main__":
    s = svg()
    open("assets/fold_conjugator.svg", "w").write(s)
    cairosvg.svg2png(bytestring=s.encode(), write_to="assets/fold_conjugator.png", output_width=1400)
    print("wrote assets/fold_conjugator.svg / .png")
