#!/usr/bin/env python3
"""make_seam_spectra.py — the Fano lens, shown as shadow spectra.

Each knot's group, held up to the GL(3,2) lens, splits into a spectrum of the
subgroups it surjects onto (one glowing mark per conjugation orbit).  The floor —
the cyclic shadows (orders 1,2,3,4,7), the abelianization — is the same faint
baseline for every knot and reads nothing.  The surjection marks are the real
shadow.

The seam (Conway vs KT): both reach only the top (GL(3,2) itself).  Their marks
there split by meridian order — the order-7 marks (dim rose) are 4 and 4,
*blind*; the order-3 marks (bright brass) are 4 and 2, and that is the seam.

The no-hand knot (fig-8) rises highest: it reaches GL(3,2) in 8 ways (order-4
copper + order-7 rose) and, alone of these, also reaches a proper subgroup (A₄).
"""
import subprocess

# data: (name, label_x, [(subgroup_order, n_orbits, colour)], extra note)
# colour codes: brass="e0b060" copper="c87a48" rose="c06070" dimrose="8a4a56"
# floor baseline drawn faintly under every row.
BRASS = "#e8b868"
COPPER = "#d08050"
ROSE = "#d06078"
DIMROSE = "#8a4a56"
GREY = "#4a4a52"

ROWS = [
    ("unknot", "unknot", []),
    ("trefoil", "3₁ trefoil", [
        (6, 1, COPPER), (12, 2, COPPER), (24, 2, ROSE), (168, 2, ROSE),
    ]),
    ("fig8", "4₁ fig-8", [
        (12, 2, COPPER), (168, 8, ROSE),
    ]),
    ("conway", "Conway 11n34", [(168, 8, ROSE)]),
    ("kt", "KT 11n42", [(168, 6, ROSE)]),
]

# x positions for the subgroup-order columns
COLX = {6: 330, 12: 480, 24: 630, 168: 810}

# For the 168 column, split into meridian-order sub-marks so the seam is visible.
# each mark is (colour, is_order3).  We render order-3 marks bright-brass and
# order-7 marks dim-rose; order-4 marks copper.  This is the seeing/blind split.
SPLIT_168 = {
    "unknot": [],
    "trefoil": [(DIMROSE, False)] * 2,                     # 2 order-7 orbits onto GL(3,2)
    "fig8": [(COPPER, False)] * 4 + [(DIMROSE, False)] * 4,  # 4 order-4 + 4 order-7
    "conway": [(BRASS, True)] * 4 + [(DIMROSE, False)] * 4,  # 4 order-3 + 4 order-7
    "kt": [(BRASS, True)] * 2 + [(DIMROSE, False)] * 4,      # 2 order-3 + 4 order-7
}

W, H = 1040, 600
ROWH = 108
Y0 = 70


def glow_dash(cx, cy, colour, n=1):
    """A single glowing vertical dash (layered strokes, no blur filter)."""
    parts = []
    for w, op in ((13, 0.12), (7, 0.35), (3, 1.0)):
        parts.append(
            f'<line x1="{cx}" y1="{cy-11}" x2="{cx}" y2="{cy+11}" '
            f'stroke="{colour}" stroke-width="{w}" stroke-opacity="{op}" '
            f'stroke-linecap="round"/>')
    return "\n".join(parts)


def mark_cluster(x, y, marks, spacing=16):
    """Render a horizontal cluster of glowing marks centred at x."""
    n = len(marks)
    out = []
    for i, (colour, _is3) in enumerate(marks):
        cx = x - (n - 1) * spacing / 2 + i * spacing
        out.append(glow_dash(cx, y, colour))
    return "\n".join(out)


def main():
    svg = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
           f'width="{W}" height="{H}">']
    svg.append(f'<rect width="{W}" height="{H}" fill="#0a0a0d"/>')
    # column guide lines (very faint)
    for k, x in COLX.items():
        svg.append(f'<line x1="{x}" y1="{Y0-30}" x2="{x}" y2="{Y0+5*ROWH+10}" '
                   f'stroke="#202028" stroke-width="1" stroke-dasharray="3 7"/>')
        svg.append(f'<text x="{x}" y="{Y0-38}" fill="#4a4a52" font-size="13" '
                   f'text-anchor="middle" font-family="monospace">{k}</text>')
    # row labels
    for r, (name, label, marks) in enumerate(ROWS):
        y = Y0 + r * ROWH + ROWH / 2
        svg.append(f'<text x="30" y="{y+5}" fill="#b8b8c0" font-size="17" '
                   f'font-family="monospace">{label}</text>')
        # the floor: one faint continuous baseline across the spectrum
        svg.append(f'<line x1="250" y1="{y}" x2="970" y2="{y}" '
                   f'stroke="{GREY}" stroke-width="1" stroke-opacity="0.35"/>')
        # surjection marks
        for k, n, colour in marks:
            if k == 168:
                # split by meridian order (the seeing/blind story)
                splits = SPLIT_168.get(name, [(colour, False)] * n)
                svg.append(mark_cluster(COLX[k], y, splits))
            else:
                svg.append(mark_cluster(COLX[k], y, [(colour, False)] * n))
    svg.append("</svg>")
    svg = "\n".join(svg)
    with open("assets/seam-spectra.svg", "w") as f:
        f.write(svg)
    subprocess.run(
        ["python3", "-c", f"import cairosvg; cairosvg.svg2png("
         f"url='assets/seam-spectra.svg', write_to='assets/seam-spectra.png', "
         f"output_width={W}, output_height={H})"], check=True)
    print("wrote assets/seam-spectra.png")


if __name__ == "__main__":
    main()
