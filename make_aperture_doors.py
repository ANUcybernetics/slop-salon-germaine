#!/usr/bin/env python3
"""make_aperture_doors.py — the door is the knot's, not the tooth's.

The trefoil's aperture (the finite groups it surjects onto) is wide:
    S3, A4, S4, AGL(1,7), A5, PSL(2,7)  —  but NOT S5.
The seam's (delta=1, perfect-derived) is narrow: A5, PSL(2,7) only.

AGL(1,7) is the hinge: det=3 said "triangle" (D3), but AGL(1,7) has no D3
subgroup — the tooth is empty.  Yet the trefoil walks straight through it
(84 surjections onto the whole lens).  The empty triangle never mattered.

Each group is a door.  Lit = in the aperture.  The AGL(1,7) door carries a
dashed empty triangle.  Render SVG -> PNG via cairosvg.
"""
import cairosvg

GROUPS = [
    ("S3",     6,  True,  False),
    ("A4",    12,  True,  False),
    ("S4",    24,  True,  False),
    ("AGL(1,7)", 42, True,  False),
    ("A5",    60,  True,  True),
    ("S5",   120,  False, False),
    ("PSL(2,7)", 168, True, True),
]
LOOKUP = {g[0]: g for g in GROUPS}

BG     = "#0b0709"
LIT    = "#d0864a"   # copper
LIT2   = "#e8c27a"   # brass highlight
ROSE   = "#c85a6e"
DARKL  = "#3a2b2e"
TRI    = "#5a3f3f"

W, H = 1400, 900
door_w, door_h = 150, 250
gap = 26
total_w = len(GROUPS)*door_w + (len(GROUPS)-1)*gap
x0 = (W - total_w)/2
row_top = 330
row_bot = 700

parts = []
parts.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">')
parts.append(f'<rect width="{W}" height="{H}" fill="{BG}"/>')

def door(x, ybase, lit, accent=False):
    xl, xr = x, x + door_w
    yt = ybase - (door_h - door_w/2)
    r = door_w/2
    d = (f"M {xl} {ybase} L {xl} {yt} A {r} {r} 0 0 1 {xr} {yt} L {xr} {ybase}")
    if lit:
        parts.append(f'<path d="{d}" fill="none" stroke="{LIT}" stroke-width="28" stroke-opacity="0.13" stroke-linecap="round"/>')
        parts.append(f'<path d="{d}" fill="none" stroke="{LIT}" stroke-width="12" stroke-opacity="0.35" stroke-linecap="round"/>')
        col = ROSE if accent else LIT2
        parts.append(f'<path d="{d}" fill="none" stroke="{col}" stroke-width="4.5" stroke-linecap="round"/>')
    else:
        parts.append(f'<path d="{d}" fill="none" stroke="{DARKL}" stroke-width="4" stroke-linecap="round"/>')

def triangle(cx, cy, lit):
    s = 30
    tri = f"M {cx-s} {cy+s*0.6} L {cx} {cy-s*0.6} L {cx+s} {cy+s*0.6} Z"
    col = "#6a4a4a" if lit else TRI
    parts.append(f'<path d="{tri}" fill="none" stroke="{col}" stroke-width="2.5" stroke-dasharray="6 5" stroke-linecap="round"/>')

def label(x, ybase, name, order, lit):
    ly = ybase + 34
    parts.append(f'<text x="{x+door_w/2}" y="{ly}" text-anchor="middle" font-family="monospace" font-size="25" fill="{LIT2 if lit else DARKL}">{name}</text>')
    parts.append(f'<text x="{x+door_w/2}" y="{ly+28}" text-anchor="middle" font-family="monospace" font-size="17" fill="{("#6a4a3a" if lit else DARKL)}">|{order}|</text>')

def row(ybase, surj_fn, header, sub):
    parts.append(f'<text x="{W/2}" y="{ybase-door_h-36}" text-anchor="middle" font-family="monospace" font-size="30" fill="{LIT}">{header}</text>')
    parts.append(f'<text x="{W/2}" y="{ybase-door_h-6}" text-anchor="middle" font-family="monospace" font-size="18" fill="#5a4030">{sub}</text>')
    for i, (name, order, ts, ss) in enumerate(GROUPS):
        x = x0 + i*(door_w+gap)
        lit = surj_fn(name)
        door(x, ybase, lit, accent=(lit and name in ("AGL(1,7)","A5","PSL(2,7)")))
        if name == "AGL(1,7)":
            triangle(x+door_w/2, ybase-door_h*0.45, lit)
        label(x, ybase, name, order, lit)

row(row_top, lambda n: LOOKUP[n][2], "trefoil", "det 3")
row(row_bot, lambda n: LOOKUP[n][3], "seam", "&#916; = 1")

parts.append(f'<text x="{W/2}" y="{H-34}" text-anchor="middle" font-family="monospace" font-size="21" fill="#8a6a4a">the door is the knot&#8217;s, not the tooth&#8217;s &#8212; the empty triangle never mattered</text>')
parts.append('</svg>')
svg = "".join(parts)
open("assets/aperture_doors.svg","w").write(svg)
cairosvg.svg2png(bytestring=svg.encode(), write_to="assets/aperture_doors.png",
                 output_width=1400, output_height=900)
print("wrote assets/aperture_doors.png")
