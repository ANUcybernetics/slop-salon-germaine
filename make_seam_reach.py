#!/usr/bin/env python3
"""make_seam_reach.py — the seam is one lock: a reach ladder of PSL(2,13)'s classes.

For each conjugacy class of PSL(2,13), a knot's meridian (the braid closure's
beta-hat) splits the beta-hat-fixed tuples into:
  - the DIAGONAL  (image = the meridian's own cyclic group — the floor, word-blind)
  - ONTO-HANDS    (image = the WHOLE room, |G| = 1092 — the reach)
Both words (Conway, KT) agree on this split for every class BUT the order-6
split-torus class, where Conway's meridian reaches the whole room (12 onto-hands,
a mirror pair) and KT's stays locked at the diagonal (order 6).  One class wide,
one lock deep.

Renders an SVG (glowing stroke-work on near-black) -> PNG via cairosvg.
"""
import cairosvg

# per-class (element order, class size, (floor, hands) for Conway, (floor, hands) for KT)
DATA = [
    ("1",   1, (1, 0), (1, 0)),
    ("2",  91, (1, 24), (1, 24)),
    ("3", 182, (1, 0), (1, 0)),
    ("6", 182, (1, 12), (1, 0)),      # <- the SEAM
    ("7", 156, (1, 28), (1, 28)),
    ("7", 156, (1, 28), (1, 28)),
    ("7", 156, (1, 28), (1, 28)),
    ("13", 84, (1, 0), (1, 0)),
    ("13", 84, (1, 0), (1, 0)),
]
SEAM_COL = 3

W, H = 1500, 960
BG = "#0b0906"
BRASS = "#e9b64e"      # Conway  (hands)
BRASS_D = "#5f4c2c"    # Conway  (floor)
COPPER = "#d8874f"     # KT      (hands)
COPPER_D = "#573f2c"   # KT      (floor)
ROSE = "#e88ca0"
INK = "#e6dccb"
MUTED = "#877b6a"
GRID = "#241d15"

maxv = 28.0
baseline = 760
top = 150
span = baseline - top
def y(v): return baseline - (v / maxv) * span

ncol = len(DATA)
cw = W / ncol
bw = 46          # bar width
gap = 16

def bar(x, floor, hands, c_floor, c_hands, glow):
    yf = y(floor)
    yh = y(floor + hands)
    s = []
    # hands (bright, glowing) from yf up to yh
    s.append(f'<rect x="{x:.1f}" y="{yh:.1f}" width="{bw}" height="{yf-yh:.1f}" rx="3" fill="{c_hands}" filter="url(#glow{c_hands[1:]})"/>')
    # floor (dim) from baseline up to yf
    s.append(f'<rect x="{x:.1f}" y="{yf:.1f}" width="{bw}" height="{baseline-yf:.1f}" rx="2" fill="{c_floor}"/>')
    return "".join(s)

svg = []
svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">')
svg.append(f'<defs>')
svg.append(f'<filter id="gbr" x="-80%" y="-80%" width="260%" height="260%">'
           f'<feGaussianBlur stdDeviation="9" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>')
svg.append(f'<filter id="gco" x="-80%" y="-80%" width="260%" height="260%">'
           f'<feGaussianBlur stdDeviation="9" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>')
svg.append(f'<filter id="gro" x="-80%" y="-80%" width="260%" height="260%">'
           f'<feGaussianBlur stdDeviation="9" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>')
svg.append('</defs>')

svg.append(f'<rect width="{W}" height="{H}" fill="{BG}"/>')

# faint horizontal gridlines
for v in (0, 7, 14, 21, 28):
    yy = y(v)
    svg.append(f'<line x1="0" y1="{yy:.1f}" x2="{W}" y2="{yy:.1f}" stroke="{GRID}" stroke-width="1"/>')
    if v == 0:
        svg.append(f'<text x="{W-24}" y="{yy-10:.1f}" text-anchor="end" fill="{MUTED}" font-size="20" font-family="serif">0</text>')
# whole-room reference line
yr = y(28)
svg.append(f'<line x1="0" y1="{yr:.1f}" x2="{W}" y2="{yr:.1f}" stroke="{MUTED}" stroke-width="1.5" stroke-dasharray="3 6"/>')
svg.append(f'<text x="{W-24}" y="{yr-30:.1f}" text-anchor="end" fill="{MUTED}" font-size="19" font-family="serif" font-style="italic">the whole room · |G| = 1092</text>')

# seam column vertical rose band
seam_x = SEAM_COL * cw
svg.append(f'<rect x="{seam_x+cw*0.08:.1f}" y="{top-30:.1f}" width="{cw*0.84:.1f}" height="{baseline-top+30:.1f}" fill="{ROSE}" opacity="0.06"/>')
svg.append(f'<line x1="{seam_x}" y1="{top-30:.1f}" x2="{seam_x}" y2="{baseline+18:.1f}" stroke="{ROSE}" stroke-width="2" filter="url(#gro)" opacity="0.55"/>')
svg.append(f'<line x1="{seam_x+cw:.1f}" y1="{top-30:.1f}" x2="{seam_x+cw:.1f}" y2="{baseline+18:.1f}" stroke="{ROSE}" stroke-width="2" filter="url(#gro)" opacity="0.55"/>')

# bars
for i, (order, csz, (fc, hc), (fk, hk)) in enumerate(DATA):
    cx = i * cw + cw / 2
    bx_c = cx - gap / 2 - bw
    bx_k = cx + gap / 2
    svg.append(bar(bx_c, fc, hc, BRASS_D, BRASS, "gbr"))
    svg.append(bar(bx_k, fk, hk, COPPER_D, COPPER, "gco"))
    # class label
    yy = baseline + 40
    svg.append(f'<text x="{cx:.1f}" y="{yy:.1f}" text-anchor="middle" fill="{INK}" font-size="26" font-family="serif">order {order}</text>')
    svg.append(f'<text x="{cx:.1f}" y="{yy+26:.1f}" text-anchor="middle" fill="{MUTED}" font-size="17" font-family="serif">|C|={csz}</text>')

# word legend
lx = 70
svg.append(f'<text x="{lx}" y="912" fill="{BRASS}" font-size="22" font-family="serif" filter="url(#gbr)">\u25a0</text>')
svg.append(f'<text x="{lx+22}" y="912" fill="{INK}" font-size="20" font-family="serif">Conway</text>')
svg.append(f'<text x="{lx+180}" y="912" fill="{COPPER}" font-size="22" font-family="serif" filter="url(#gco)">\u25a0</text>')
svg.append(f'<text x="{lx+202}" y="912" fill="{INK}" font-size="20" font-family="serif">KT</text>')
svg.append(f'<text x="{lx+320}" y="912" fill="{MUTED}" font-size="19" font-family="serif">bright = onto-hands (image = the whole room)   \u00b7   dim = the diagonal (the floor)</text>')

# seam marker: a small rose ring under the seam column, labelled
sx = seam_x + cw / 2
svg.append(f'<circle cx="{sx:.1f}" cy="862" r="9" fill="none" stroke="{ROSE}" stroke-width="2.5" filter="url(#gro)"/>')

svg.append('</svg>')
out = "".join(svg)
with open("assets/seam_reach.svg", "w") as f:
    f.write(out)
cairosvg.svg2png(url="assets/seam_reach.svg", write_to="assets/seam_reach.png",
                 output_width=1500, output_height=960)
print("wrote assets/seam_reach.svg / .png")
