#!/usr/bin/env python3
"""make_count_is_group.py — the count is the group's, the fold is the reading's.

The siblings' claim: the seam (onto-reach) is a knot invariant — reading-invariant;
the fold (which pair shares a torus) is the reading's — it moves.  Confirmed.

The mechanism is NOT a relabeling.  Reading the word backward gives a DIFFERENT set
of onto-homomorphisms (no permutation of the four generator coordinates maps the
forward set to the backward set — verified p=7,11).  Yet the count |onto| is
identical.  So the seam's invariance is not "the same object, renamed": it is a
property of the KNOT GROUP, which is unchanged by the reading (the group is the
knot, Gordon-Luecke completeness).  The fold names a COORDINATIZATION (which
meridian is x1..x4), so it moves when the coordinatization does.

Board: Conway 11n34 at p=11 (m=5), the onto-hands as rows of four meridian axes.
Brass = x1·x3 share an axis (the doubled chord — a fold).  Forward folds both
hands; read backward, no chord doubles.  |onto| = 10 under both.
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

# Conway 11n34, p=11, the onto-hands as (x1,x2,x3,x4) axis pairs.
# fwd: both hands fold x1·x3 (x1 and x3 both on axis (5,9)).
# rev: neither folds (all four axes distinct).
FWD = [
    [(5, 9), (1, 4), (5, 9), (5, 6)],
    [(5, 9), (1, 3), (5, 9), (5, 11)],
]
REV = [
    [(5, 9), (1, 4), (2, 7), (4, 7)],
    [(5, 9), (1, 3), (0, 10), (0, 1)],
]

CELL_W = 150
CELL_H = 66
LABEL_W = 120
GAP = 40
HEAD = 230
COUNT_H = 120

def axis_str(a):
    return "{" + ",".join(str(v) for v in a) + "}"


def hand_svg(y, xs, x0, is_fold, label):
    """one onto-hand: label then four axis cells; brass where x1·x3 share."""
    out = []
    out.append(f'<text x="{x0}" y="{y + CELL_H / 2 + 5}" font-family="DejaVu Sans Mono" '
               f'font-size="12" fill="{DIM}">{label}</text>')
    for k in range(4):
        cx = x0 + LABEL_W + k * CELL_W
        a = xs[k]
        # x1 (k=0) and x3 (k=2) fold when their axes agree
        folded = is_fold and k in (0, 2) and xs[0] == xs[2]
        edge = BRASS_EDGE if folded else COPPER_EDGE
        stroke = BRASS if folded else COPPER
        op = 0.95 if folded else 0.8
        out.append(f'<rect x="{cx}" y="{y}" width="{CELL_W}" height="{CELL_H}" '
                   f'fill="{BG}" stroke="{stroke}" stroke-width="{2 if folded else 1.4}" '
                   f'stroke-opacity="{op}" rx="6"/>')
        out.append(f'<text x="{cx + CELL_W / 2}" y="{y + CELL_H / 2 + 5}" text-anchor="middle" '
                   f'font-family="DejaVu Sans Mono" font-size="13" '
                   f'fill="{BRASS_EDGE if folded else TXT}">x{k + 1} {axis_str(a)}</text>')
        if folded:
            # doubling marker on the shared axis
            out.append(f'<circle cx="{cx + CELL_W / 2}" cy="{y + 10}" r="3.2" fill="{BRASS_EDGE}"/>')
    return "".join(out)


def column_svg(x0, hands, fold, title, sub, count, top):
    out = []
    out.append(f'<text x="{x0}" y="{top}" font-family="DejaVu Sans Mono" font-size="18" fill="{TXT}">{title}</text>')
    out.append(f'<text x="{x0}" y="{top + 20}" font-family="DejaVu Sans Mono" font-size="11" fill="{DIM}">{sub}</text>')
    for i, xs in enumerate(hands):
        out.append(hand_svg(top + 40 + i * CELL_H, xs, x0, fold, f"hand {i+1}"))
    # count — the invariant
    cy = top + 40 + len(hands) * CELL_H + 60
    out.append(f'<text x="{x0}" y="{cy}" font-family="DejaVu Sans Mono" font-size="22" fill="{TXT}">|onto| = {count}</text>')
    out.append(f'<text x="{x0}" y="{cy + 24}" font-family="DejaVu Sans Mono" font-size="11" fill="{DIM}">'
               f'the count is the knot&#39;s — the same both ways</text>')
    return "".join(out)


def svg():
    W = 2 * (LABEL_W + 4 * CELL_W) + GAP + 80
    H = HEAD + len(FWD) * CELL_H + 170
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">']
    out.append(f'<rect width="{W}" height="{H}" fill="{BG}"/>')
    out.append(f'<text x="40" y="48" font-family="DejaVu Sans Mono" font-size="22" fill="{TXT}">the count is the group&#39;s</text>')
    out.append(f'<text x="40" y="72" font-family="DejaVu Sans Mono" font-size="13" fill="{DIM}">Conway 11n34, p=11, the split-torus class — the onto-hands, read two ways.</text>')
    out.append(f'<text x="40" y="90" font-family="DejaVu Sans Mono" font-size="12" fill="{MUTED}">brass = x1·x3 share an axis (a doubled chord, a fold). no chord doubles = spread.</text>')
    out.append(f'<text x="40" y="118" font-family="DejaVu Sans Mono" font-size="12" fill="{ROSE}">NOT a relabeling: no permutation of the four columns maps fwd → rev — the hands genuinely differ.</text>')
    out.append(f'<text x="40" y="136" font-family="DejaVu Sans Mono" font-size="12" fill="{DIM}">yet |onto| is the same. the count is a property of the knot group (the group is the knot); the fold is a property of the reading.</text>')

    xA = 40
    xB = 40 + (LABEL_W + 4 * CELL_W) + GAP
    out.append(column_svg(xA, FWD, True, "as written", "folds x1·x3 (6→0 read back)", 10, 185))
    out.append(column_svg(xB, REV, False, "read backward", "spreads — no chord doubles", 10, 185))

    out.append(f'<text x="40" y="{H - 36}" font-family="DejaVu Sans Mono" font-size="12" fill="{MUTED}">the seam is the knot&#39;s (|onto| survives the reading); the fold is the reading&#39;s (the pair moves).</text>')
    out.append(f'<text x="40" y="{H - 18}" font-family="DejaVu Sans Mono" font-size="12" fill="{MUTED}">and the reading is not a relabeling — so the count&#39;s invariance is the group&#39;s, not the label&#39;s.</text>')
    out.append('</svg>')
    return "\n".join(out)


if __name__ == "__main__":
    s = svg()
    open("assets/count_is_group.svg", "w").write(s)
    cairosvg.svg2png(bytestring=s.encode(), write_to="assets/count_is_group.png", output_width=1500)
    print("wrote assets/count_is_group.svg / .png")
