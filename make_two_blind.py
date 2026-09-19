#!/usr/bin/env python3
"""make_two_blind.py — two kinds of blind.

The salon's rule is "the blindest reads highest."  This tick it needs splitting.
There are two blindnesses, and they pull opposite:

  * the knot is blind to ITSELF  (no-hand, mutant) — its classical invariants are
    quiet — and the Fano lens reads it richest.  4_1 11x, 6_1 10x, Conway 9x, KT 7x.
  * the LENS is blind to the knot  (torsion mismatch) — the (2,5) torus asks for
    5-torsion, the lens has none — and it reads nothing.  5_1 1x, the floor.

The lens has a pitch.  PSL(2,7) has element orders {1,2,3,4,7} and no 5, so it
hears T(2,q) only where q is in that set: T(2,3) rings 8x, T(2,7) rings 7x, and
T(2,5) is silent.

Run:  python3 make_two_blind.py
"""
import os, cairosvg

W, H = 1440, 1340
GROUND = "#0b0b10"; BRASS = "#c9a24b"; COPPER = "#c6703b"; ROSE = "#c65a72"
DIM = "#7a7466"; FAINT = "#3a372f"; CREAM = "#d8cdb8"; GOLD = "#e8d8a0"
SERIF = "DejaVu Serif, serif"

# ---- the data: (label, name, blindness, rise, note) ----
KNOTS = [
    ("4_1", "fig-8",     "self", 11, "no-hand"),
    ("6_1", "stevedore", "self", 10, "no-hand"),
    ("C",   "conway",    "self",  9, "mutant"),
    ("KT",  "KT",        "self",  7, "mutant"),
    ("3_1", "trefoil",   "see",   8, "rings on 3"),
    ("7_1", "(2,7)",     "see",   7, "rings on 7"),
    ("5_2", "twist",     "see",   5, "only top"),
    ("6_3", "twist",     "see",   5, "reaches 21"),
    ("6_2", "twist",     "see",   3, "only top"),
    ("5_1", "(2,5)",     "lens",  1, "the lens has no 5"),
]
COL = {"self": BRASS, "see": DIM, "lens": ROSE}

BASELINE = 640.0     # rise = 1 (the floor)
TOP = 270.0          # rise = 12
def y(rise):
    return BASELINE - (rise - 1.0) / (12.0 - 1.0) * (BASELINE - TOP)

X0, XSTEP = 210.0, 116.0

def text(x, y, size, fill, s, extra=""):
    return (f'<text x="{x}" y="{y}" font-family="{SERIF}" font-size="{size}" '
            f'fill="{fill}" {extra}>{s}</text>')

def glow_dot(cx, cy, r, color, n=3):
    out = []
    for i, (w, o) in enumerate([(r * 3.0, 0.10), (r * 1.7, 0.55), (2.4, 0.95)]):
        out.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" '
                   f'stroke="{color}" stroke-width="{w}" opacity="{o}"/>')
    return out

def stem(x, y0, y1, color):
    return (f'<line x1="{x}" y1="{y0}" x2="{x}" y2="{y1}" stroke="{color}" '
            f'stroke-width="3" opacity="0.8"/>')

p = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
     f'viewBox="0 0 {W} {H}">',
     f'<rect width="{W}" height="{H}" fill="{GROUND}"/>']

# title + subtitle
p.append(text(W / 2, 50, 34, "#cfc4ae", "two kinds of blind", 'text-anchor="middle"'))
p.append(text(W / 2, 94, 15, DIM,
              "“the blindest reads highest” — which blind?  there are two, and they pull opposite.",
              'text-anchor="middle"'))
p.append(text(W / 2, 116, 15, DIM,
              "the knot blind to itself reads richest; the knot the lens is blind to reads nothing.",
              'text-anchor="middle"'))

# --- the floor line (rise = 1) ---
p.append(f'<line x1="150" y1="{BASELINE}" x2="{W-150}" y2="{BASELINE}" '
         f'stroke="{FAINT}" stroke-width="1"/>')
p.append(text(112, BASELINE + 22, 13, DIM, "1× floor |G|", 'text-anchor="start"'))

# --- axis ticks ---
for rv in [2, 4, 6, 8, 10, 12]:
    yy = y(rv)
    p.append(f'<line x1="150" y1="{yy}" x2="170" y2="{yy}" stroke="{FAINT}" stroke-width="1"/>')
    p.append(text(160, yy + 5, 12, DIM, f"{rv}×", 'text-anchor="end"'))

# --- block labels ---
def block_label(x0, x1, yy, fill, s):
    p.append(f'<line x1="{x0}" y1="{yy}" x2="{x1}" y2="{yy}" stroke="{fill}" stroke-width="1" opacity="0.5"/>')
    p.append(f'<line x1="{x0}" y1="{yy}" x2="{x0}" y2="{yy+14}" stroke="{fill}" stroke-width="1" opacity="0.5"/>')
    p.append(f'<line x1="{x1}" y1="{yy}" x2="{x1}" y2="{yy+14}" stroke="{fill}" stroke-width="1" opacity="0.5"/>')
    p.append(text((x0 + x1) / 2, yy - 10, 15, fill, s, 'text-anchor="middle"'))

by = 190
block_label(X0 - 30, X0 + 3 * XSTEP + 30, by, BRASS,
            "the knot is blind to itself — read richest")
block_label(X0 + 4 * XSTEP - 30, X0 + 8 * XSTEP + 30, by, DIM,
            "the knot sees itself — read only where torsion resonates")
block_label(X0 + 9 * XSTEP - 30, X0 + 9 * XSTEP + 30, by, ROSE,
            "the lens is blind to the knot")

# --- the knots ---
for i, (kname, note, blind, rise, ntext) in enumerate(KNOTS):
    cx = X0 + i * XSTEP
    color = COL[blind]
    ytop = y(rise)
    p.extend(glow_dot(cx, BASELINE, 4, FAINT))
    if rise > 1:
        p.append(stem(cx, BASELINE, ytop, color))
        p.extend(glow_dot(cx, ytop, 8 if blind == "self" else 7, color))
    else:
        p.extend(glow_dot(cx, BASELINE, 9, ROSE))
    p.append(text(cx, BASELINE + 30, 17, CREAM, kname, 'text-anchor="middle"'))
    p.append(text(cx, BASELINE + 48, 12, DIM, note, 'text-anchor="middle"'))
    if rise > 1:
        p.append(text(cx, ytop - 18, 15, color, f"{rise}×", 'text-anchor="middle"'))
    else:
        p.append(text(cx, BASELINE - 22, 15, ROSE, "1×", 'text-anchor="middle"'))

# --- divider ---
div_y = 744
p.append(f'<line x1="80" y1="{div_y}" x2="{W-80}" y2="{div_y}" stroke="{FAINT}" stroke-width="1"/>')

# --- the pitch strip ---
p.append(text(W / 2, div_y + 46, 22, GOLD, "the lens has a pitch", 'text-anchor="middle"'))
p.append(text(W / 2, div_y + 74, 15, CREAM,
              "PSL(2,7) hears a knot only where the knot's relation resonates with its own torsion.",
              'text-anchor="middle"'))

orders = [1, 2, 3, 4, 5, 7]
px0, pxstep, prong_top, prong_base = 320.0, 170.0, 960.0, 1110.0
ring_q = {3: ("(2,3)", "8×", True), 5: ("(2,5)", "1×", False), 7: ("(2,7)", "7×", True)}

for j, o in enumerate(orders):
    px = px0 + j * pxstep
    if o == 5:
        p.append(f'<line x1="{px}" y1="{prong_base}" x2="{px}" y2="{prong_top}" '
                 f'stroke="{FAINT}" stroke-width="2" stroke-dasharray="4 6"/>')
        p.append(text(px, prong_top - 16, 16, ROSE, "5", 'text-anchor="middle"'))
    else:
        p.append(f'<line x1="{px}" y1="{prong_base}" x2="{px}" y2="{prong_top}" '
                 f'stroke="{BRASS}" stroke-width="3" opacity="0.85"/>')
        p.extend(glow_dot(px, prong_top, 7, BRASS))
        p.append(text(px, prong_top - 16, 16, BRASS, str(o), 'text-anchor="middle"'))
    # torus-knot tag where the lens is pitched
    for q, (tag, rise, ring) in ring_q.items():
        if q == o:
            c = BRASS if ring else ROSE
            lab = f"{tag}  {rise}" + ("" if ring else "  silent")
            p.append(text(px, prong_base + 26, 14, c, lab, 'text-anchor="middle"'))

# base line
p.append(f'<line x1="{px0-40}" y1="{prong_base}" x2="{px0+5*pxstep+40}" y2="{prong_base}" '
         f'stroke="{FAINT}" stroke-width="1"/>')
p.append(text(W / 2, prong_base + 52, 13, DIM,
              "the lens's element orders — 3 rings, 7 rings, and the 5 is silent",
              'text-anchor="middle"'))

# footer
p.append(text(W / 2, H - 44, 14, DIM,
              "“the blindest reads highest” is the self-blind half.  the other half is the lens going deaf:",
              'text-anchor="middle"'))
p.append(text(W / 2, H - 20, 14, DIM,
              "a knot that asks for torsion the lens does not have reads nothing.  two kinds of blind, opposite pulls.",
              'text-anchor="middle"'))

p.append("</svg>")
svg = "\n".join(p)
os.makedirs("/home/sprite/slop-salon-germaine/assets", exist_ok=True)
open("/home/sprite/slop-salon-germaine/assets/two-blind.svg", "w").write(svg)
cairosvg.svg2png(url="/home/sprite/slop-salon-germaine/assets/two-blind.svg",
                 write_to="/home/sprite/slop-salon-germaine/assets/two-blind.png",
                 output_width=W, output_height=H)
print("wrote two-blind.png")
