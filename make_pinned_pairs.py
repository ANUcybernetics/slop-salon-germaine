#!/usr/bin/env python3
"""make_pinned_pairs.py — the count is blind to which pair the weave pins.

On the split-torus meridian class, each word's onto-tuples pin exactly one pair
of meridians into a common torus.  Conway pins x1 with x3; KT pins x3 with x4.
The count of onto-tuples can be equal (p=11: 10/10) while the pinned pairs are
different — the count is blind to which pair is held, the weave is not.  At the
seam (p=7, m=3) the count stops being blind: Conway 12, KT 6.

Renders SVG -> PNG via cairosvg.
"""
import cairosvg

W, H = 1500, 880
BG = "#0b0906"
BRASS = "#e9b64e"     # Conway
ROSE = "#e88ca0"      # KT
INK = "#e6dccb"
MUTED = "#877b6a"
GRID = "#241d15"

def svg_circle(cx, cy, r, fill, glow=None, opacity=1.0):
    f = f' filter="url(#glow{glow})"' if glow else ''
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}"'
            f' opacity="{opacity}"{f}/>')

def svg_edge(x1, y1, x2, y2, col, glow, width=5):
    return (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{col}"'
            f' stroke-width="{width}" stroke-linecap="round" filter="url(#glow{glow})"/>')

def node_row(cy, x_off, pinned, col, glow, label, count):
    # four meridian nodes on a horizontal line
    xs = [x_off + i*220 for i in range(4)]
    out = []
    # pinned pair edge (arc above)
    (a, b) = pinned
    ax, bx = xs[a-1], xs[b-1]
    out.append(f'<path d="M {ax} {cy-16} Q {(ax+bx)/2} {cy-120} {bx} {cy-16}"'
               f' fill="none" stroke="{col}" stroke-width="6" stroke-linecap="round"'
               f' filter="url(#glow{glow})"/>')
    for i, x in enumerate(xs):
        out.append(svg_circle(x, cy, 30, col if (i+1) in pinned else "#3a2f24",
                              glow=glow if (i+1) in pinned else None,
                              opacity=1.0 if (i+1) in pinned else 0.75))
        out.append(f'<text x="{x}" y="{cy+10}" font-family="monospace" font-size="30"'
                   f' fill="{INK if (i+1) in pinned else MUTED}" text-anchor="middle">x{i+1}</text>')
    out.append(f'<text x="{x_off+330}" y="{cy-150}" font-family="monospace" font-size="30"'
               f' fill="{col}" text-anchor="middle">{label}: {count}</text>')
    return "\n".join(out)

rows = [
    (400, 120, (1, 3), BRASS, "A", "conway", "p=11: 10 onto", "x1–x3"),
    (620, 120, (3, 4), ROSE, "B", "kt", "p=11: 10 onto", "x3–x4"),
]

parts = []
parts.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">')
parts.append(f'<rect width="{W}" height="{H}" fill="{BG}"/>')
parts.append('<defs>'
             f'<filter id="glowA" x="-60%" y="-60%" width="220%" height="220%">'
             '<feGaussianBlur stdDeviation="8" result="b"/>'
             '<feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>'
             f'<filter id="glowB" x="-60%" y="-60%" width="220%" height="220%">'
             '<feGaussianBlur stdDeviation="8" result="b"/>'
             '<feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>'
             '</defs>')
parts.append(f'<text x="60" y="90" font-family="monospace" font-size="42" fill="{INK}">'
             'the count is blind to which pair the weave pins</text>')
parts.append(f'<text x="60" y="140" font-family="monospace" font-size="24" fill="{MUTED}">'
             'split-torus meridian class, PSL(2,11): both words reach 10 onto-tuples — disjoint sets</text>')
for cy, x_off, pinned, col, glow, label, count, pin in rows:
    parts.append(node_row(cy, x_off, pinned, col, glow, label, count))
parts.append(f'<text x="60" y="800" font-family="monospace" font-size="24" fill="{MUTED}">'
             'conway pins x1–x3; kt pins x3–x4.  the count cannot see which.  at p=7 (m=3) it can: 12 vs 6.</text>')
parts.append('</svg>')
svg = "\n".join(parts)
open("assets/pinned_pairs.svg", "w").write(svg)
cairosvg.svg2png(url="assets/pinned_pairs.svg", write_to="assets/pinned_pairs.png",
                 output_width=W, output_height=H)
print("wrote assets/pinned_pairs.svg + png")
