#!/usr/bin/env python3
"""make_two_doors.py — the fold and the seam are TWO locks, not one.

The split-torus class is a door with two keyholes.  The FOLD (a chord doubles:
two meridians on one chord, inverses) opens at m=3,5 and is shut at m>=6 -- the
weave conjugator is in N(T)\\T at m=3,5 and leaves N(T) entirely at m>=6.  The
SEAM (Conway's reach != KT's reach) opens at m=3,6 and is shut at m=5,8,9 -- it is
a COUNT difference (Conway has more onto hands), not a fold difference.

They coincide only at m=3.  At m=5 the fold is open and the seam shut; at m=6 the
seam is open and the fold shut.  Neither is the other's shadow.

Renders a two-row keyhole board: brass = fold lock, rose = seam lock, one column
per m.  A keyhole GLOWS where its lock is open, sits dark where shut.
"""
import math

# per-m facts: (fold_open, seam_open, fold_hands_1stclass, C_onto, K_onto, conjugator)
# conjugator placement of the fold edge: "N(T)\\T" (inverts) or "outside N(T)" (spread)
ROWS = [
    (3,  True,  True,  2, 4, 2, "in N(T)\\T"),
    (5,  True,  False, 2, 2, 2, "in N(T)\\T"),
    (6,  False, True,  0, 2, 0, "outside N(T)"),
    (8,  False, False, 0, 4, 4, "outside N(T)"),
    (9,  False, False, 0, 4, 4, "outside N(T)"),
]

W, H = 1300, 700
CX, CY = 240, 330
COLW = 200
ROWH = 190
BRASS = (214, 168, 106)
ROSE = (216, 120, 118)
COPPER = (196, 120, 74)
DIM = (44, 42, 46)

parts = []
parts.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
             f'viewBox="0 0 {W} {H}">')
# background
parts.append(f'<rect width="{W}" height="{H}" fill="#0a0a0c"/>')

# defs: glow filter
parts.append(
    '<defs>'
    '<filter id="glow" x="-80%" y="-80%" width="260%" height="260%">'
    '<feGaussianBlur stdDeviation="7" result="b"/>'
    '<feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>'
    '</filter>'
    '<radialGradient id="halo" cx="50%" cy="50%" r="50%">'
    '<stop offset="0%" stop-color="#fff" stop-opacity="0.85"/>'
    '<stop offset="40%" stop-color="#000" stop-opacity="0"/>'
    '</radialGradient>'
    '</defs>'
)


def rgb(c):
    return f"rgb({c[0]},{c[1]},{c[2]})"


def keyhole(x, y, color, lit):
    """Draw a keyhole: a glowing ring + a key slot. lit => glow, else dim."""
    r = 26
    # halo
    if lit:
        parts.append(f'<circle cx="{x}" cy="{y}" r="{r*2.4}" fill="{rgb(color)}" '
                     f'opacity="0.18" filter="url(#glow)"/>')
    # outer ring
    ring = rgb(color) if lit else rgb(DIM)
    glow_attr = ' filter="url(#glow)"' if lit else ''
    parts.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="none" '
                 f'stroke="{ring}" stroke-width="4"{glow_attr} '
                 f'opacity="{1 if lit else 0.7}"/>')
    # slot below the ring (the keyhole's shaft)
    parts.append(f'<rect x="{x-5}" y="{y}" width="10" height="{r+14}" rx="5" '
                 f'fill="{rgb(color) if lit else rgb(DIM)}"{glow_attr} '
                 f'opacity="{1 if lit else 0.7}"/>')
    # inner dot (the key turns here)
    parts.append(f'<circle cx="{x}" cy="{y}" r="5" fill="#0a0a0c"/>')


def label(x, y, text, size=26, fill="#d8d4cc", weight="normal", anchor="middle", opacity=1):
    parts.append(f'<text x="{x}" y="{y}" font-family="Georgia, serif" font-size="{size}" '
                 f'fill="{fill}" text-anchor="{anchor}" font-weight="{weight}" '
                 f'opacity="{opacity}">{text}</text>')


# ---- title ----
label(W / 2, 70, "two locks on the split-torus door", 34, "#e8e3d8", "bold")
label(W / 2, 104, "the fold and the seam open at different rungs", 20, "#9a948a", "italic")

# ---- row headers ----
label(CX - 120, CY - 16, "FOLD", 30, rgb(BRASS), "bold", "end")
label(CX - 120, CY - 16 + ROWH, "SEAM", 30, rgb(ROSE), "bold", "end")
label(CX - 120, CY + 40, "chord doubles", 17, "#7c766c", "end")
label(CX - 120, CY + 40 + ROWH, "reach differs", 17, "#7c766c", "end")

# ---- column headers (m values) + p ----
x0 = CX + 70
for col, (m, *_rest) in enumerate(ROWS):
    x = x0 + col * COLW
    p = 2 * m + 1
    label(x, 150, f"m = {m}", 24, "#c9c4ba", "bold")
    label(x, 174, f"p = {p}", 16, "#7c766c")

# ---- keyholes ----
for col, (m, fold_open, seam_open, fh, c_on, k_on, cplace) in enumerate(ROWS):
    x = x0 + col * COLW
    # fold keyhole (brass)
    keyhole(x, CY, BRASS, fold_open)
    # seam keyhole (rose)
    keyhole(x, CY + ROWH, ROSE, seam_open)
    # fold caption: conjugator placement + fold hands
    fc = rgb(BRASS) if fold_open else "#8a6a50"
    label(x, CY + 62, f"{fh} hands fold", 15, fc)
    label(x, CY + 82, cplace, 13, fc, opacity=0.85)
    # seam caption: onto counts C vs K
    sc = rgb(ROSE) if seam_open else "#8a6a50"
    label(x, CY + ROWH + 62, f"C {c_on}  ·  K {k_on}", 15, sc)
    label(x, CY + ROWH + 82, "onto hands", 13, sc, opacity=0.85)

# ---- m=5 / m=6 cross-note ----
note_y = 668
label(W / 2, note_y,
      "m=5: the chord doubles, yet the words agree (no seam)   ·   "
      "m=6: the words part, yet no chord doubles (no fold)",
      18, "#b8b2a6", "italic")

parts.append('</svg>')
with open("assets/two_doors.svg", "w") as f:
    f.write("\n".join(parts))
print("wrote assets/two_doors.svg")
