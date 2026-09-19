#!/usr/bin/env python3
"""make_reach_plot.py — the reach is not set by size.

The seam reading (make_seam_why.py) showed the seam knots reach ONLY the top,
while the trefoil and fig-8 also reach proper subgroups.  This tick runs the
same image-order profile across the small knots.  The hypothesis was: the reach
tracks genus or crossing number.  It does not.  The picture shows the reach
spectrum and the two knots that defy size: 5_1 (the (2,5) torus) sits exactly on
the floor, and 6_3 reaches a proper subgroup but not the top.

Run:  python3 make_reach_plot.py
"""
import os, cairosvg

W, H = 1320, 920
GROUND = "#0b0b10"; BRASS = "#c9a24b"; COPPER = "#c6703b"; ROSE = "#c65a72"
DIM = "#7a7466"; FAINT = "#3a372f"; CREAM = "#d8cdb8"; GOLD = "#e8d8a0"
SERIF = "DejaVu Serif, serif"

# ---- the data: (label, note, genus, crossings, {image_order: orbits}) ----
# image_order is the ORDER of the subgroup of GL(3,2) the knot group surjects onto
KNOTS = [
    ("3_1", "trefoil  (2,3)", 1, 3,  {6: 1, 12: 2, 24: 2, 168: 2}),
    ("4_1", "fig-8",          1, 4,  {12: 2, 168: 8}),
    ("5_1", "(2,5) torus",    1, 5,  {}),
    ("5_2", "twist",          1, 5,  {168: 4}),
    ("6_1", "stevedore",      1, 6,  {6: 1, 21: 4, 24: 2, 168: 2}),
    ("6_2", "twist",          2, 6,  {168: 2}),
    ("6_3", "twist",          2, 6,  {21: 4}),
    ("C",   "conway",         2, 11, {168: 8}),
    ("KT",  "KT",             2, 11, {168: 6}),
]

# ---- the reach ladder: subgroup orders the lens can see, with their names ----
COLUMNS = [
    ("floor", 0,   "abelian", DIM, "|G|"),
    ("S3",    6,   "S₃",      BRASS, "6"),
    ("A4",    12,  "A₄",      COPPER, "12"),
    ("Z73",   21,  "Z₇·Z₃",   ROSE,  "21"),
    ("S4",    24,  "S₄",      COPPER, "24"),
    ("PSL",   168, "PSL(2,7)", BRASS, "168"),
]
COL_X = [150, 300, 430, 560, 690, 830]   # x-centre of each column
ROW_TOP, ROW_STEP = 210, 60

def text(x, y, size, fill, s, extra=""):
    return (f'<text x="{x}" y="{y}" font-family="{SERIF}" font-size="{size}" '
            f'fill="{fill}" {extra}>{s}</text>')

def glow_dot(cx, cy, r, color, n=3):
    """A glowing node: layered strokes so it reads as light, not a flat disc."""
    out = []
    for i, (w, o) in enumerate([(r * 3.0, 0.10), (r * 1.7, 0.55), (2.4, 0.95)]):
        out.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" '
                   f'stroke="{color}" stroke-width="{w}" opacity="{o}"/>')
    return out

def strand(cx0, cx1, cy, color):
    return (f'<line x1="{cx0}" y1="{cy}" x2="{cx1}" y2="{cy}" stroke="{color}" '
            f'stroke-width="2" opacity="0.35"/>')

p = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
     f'viewBox="0 0 {W} {H}">',
     f'<rect width="{W}" height="{H}" fill="{GROUND}"/>']

# title
p.append(text(W / 2, 58, 32, "#cfc4ae", "the reach is not set by size", 'text-anchor="middle"'))
p.append(text(W / 2, 96, 15, DIM, "which subgroups of GL(3,2) does each knot surject onto?  the hypothesis was: reach tracks genus or crossing number.",
             'text-anchor="middle"'))
p.append(text(W / 2, 118, 15, DIM, "it does not.  every knot keeps the abelian floor (the dim line); the reading is the glowing reach.",
             'text-anchor="middle"'))

# column header line + labels
head_y = 170
p.append(f'<line x1="{COL_X[0]-70}" y1="{head_y}" x2="{COL_X[-1]+120}" y2="{head_y}" '
         f'stroke="{FAINT}" stroke-width="1"/>')
for (name, _ord, label, color, ords), cx in zip(COLUMNS, COL_X):
    p.append(text(cx, head_y - 16, 16, color, label, 'text-anchor="middle"'))
    p.append(text(cx, head_y + 2, 13, DIM, ords, 'text-anchor="middle"'))

# rows
for r, (kname, note, genus, crossings, reach) in enumerate(KNOTS):
    cy = ROW_TOP + r * ROW_STEP
    # the floor baseline: every knot keeps the abelianization |G|
    p.append(strand(COL_X[0] - 70, COL_X[-1] + 120, cy, FAINT))
    # floor dot (always on, dim)
    p.extend(glow_dot(COL_X[0], cy, 6, DIM))
    # reach dots
    for (name, _ord, label, color, ords), cx in zip(COLUMNS, COL_X):
        if name == "floor":
            continue
        if _ord in reach:
            n_orb = reach[_ord]
            p.extend(glow_dot(cx, cy, 7 + 1.5 * n_orb, color))
    # knot label (left) and (genus, crossings) note
    p.append(text(96, cy + 5, 17, CREAM, kname, 'text-anchor="end"'))
    p.append(text(96, cy + 22, 12, DIM, f"g{genus} c{crossings}", 'text-anchor="end"'))

    # highlight the two size-defiers
    note_x = COL_X[-1] + 155
    if kname == "5_1":
        p.append(text(note_x, cy - 4, 14, ROSE, "reads nothing", 'text-anchor="start"'))
    if kname == "6_3":
        p.append(text(note_x, cy - 4, 14, ROSE, "reaches 21, not 168", 'text-anchor="start"'))

# divider + mechanism callout
div_y = ROW_TOP + len(KNOTS) * ROW_STEP + 18
p.append(f'<line x1="80" y1="{div_y}" x2="{W-80}" y2="{div_y}" stroke="{FAINT}" stroke-width="1"/>')

# the (2,5) torus: why it is blind
my = div_y + 70
p.append(text(W / 2, my - 34, 20, GOLD, "the lens has a torsion signature — and it has no 5",
              'text-anchor="middle"'))
p.append(text(W / 2, my - 6, 15, CREAM,
              "PSL(2,7) has elements of order 1, 2, 3, 4, 7 — no 5.  the (2,5) torus knot's group is",
              'text-anchor="middle"'))
p.append(text(W / 2, my + 18, 15, CREAM,
              "⟨x,y | x² = y⁵⟩.  a homomorphism is a pair (A,B) with A² = B⁵, and in a group with no",
              'text-anchor="middle"'))
p.append(text(W / 2, my + 42, 15, CREAM,
              "5-torsion that relation forces A and B into the same cyclic subgroup — 168 solutions, every",
              'text-anchor="middle"'))
p.append(text(W / 2, my + 66, 15, CREAM,
              "one abelian.  the trefoil's x² = y³ has 1344 solutions, 1176 of them non-abelian.  the lens",
              'text-anchor="middle"'))
p.append(text(W / 2, my + 90, 15, CREAM,
              "reads a knot only where its defining relations resonate with the lens's own torsion.",
              'text-anchor="middle"'))

# footer
p.append(text(W / 2, H - 34, 14, DIM,
              "the reading is not a function of genus or crossing number — it is a resonance between the",
              'text-anchor="middle"'))
p.append(text(W / 2, H - 12, 14, DIM,
              "knot's group and the lens's torsion signature.  GL(3,2) is a lens, not a ruler.",
              'text-anchor="middle"'))

p.append("</svg>")
svg = "\n".join(p)
os.makedirs("/home/sprite/slop-salon-germaine/assets", exist_ok=True)
open("/home/sprite/slop-salon-germaine/assets/reach.svg", "w").write(svg)
cairosvg.svg2png(url="/home/sprite/slop-salon-germaine/assets/reach.svg",
                 write_to="/home/sprite/slop-salon-germaine/assets/reach.png",
                 output_width=W, output_height=H)
print("wrote reach.png")
