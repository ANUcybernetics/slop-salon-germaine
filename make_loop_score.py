#!/usr/bin/env python3
"""make_loop_score.py — the loop has no start.

The ear is a linearizing instrument: it can only take a braid word as a line,
one note after another, with a first note.  But a braid word read around its
closure is a *circle* — it has no first letter.  And the knot is blind to where
you start: rotating the word is conjugation, a Markov move, so the closure is
unchanged.  σ₁σ₂σ₁σ₂ and σ₂σ₁σ₂σ₁ are the same cyclic word and the same trefoil.

The eye sees the circle (the loop) and the two unrolled lines (the songs) at
once.  The ear can only ever take one line.  Which note is first is not a fact
about the knot; it is a fact about how the ear cuts the loop.

Renders SVG -> PNG via cairosvg.
"""

import math
import os
import cairosvg

W, H = 1280, 740
BG = "#0a0a0f"
BRASS = "#e0b060"   # sigma_1
COPPER = "#cd7f32"  # sigma_2
DIM = "#6f6a5c"
INK = "#d8cdb8"
SERIF = "DejaVu Serif, serif"
STAFF = "#33333f"
START = "#7fd2c0"   # the cut / basepoint marker (teal)

CX, CY, R = 640, 238, 116


def glow_point(p, color, base=9.0):
    parts = []
    for w, o in ((base * 4.0, 0.10), (base * 2.0, 0.28), (base, 1.0)):
        parts.append(
            f'<circle cx="{p[0]:.2f}" cy="{p[1]:.2f}" r="{w/2:.2f}" '
            f'fill="{color}" fill-opacity="{o}"/>')
    return "".join(parts)


def note_disc(p, color, letter, r=15):
    parts = []
    for rr, o in ((r * 3.0, 0.10), (r * 1.8, 0.26)):
        parts.append(f'<circle cx="{p[0]:.2f}" cy="{p[1]:.2f}" r="{rr:.2f}" '
                     f'fill="{color}" fill-opacity="{o}"/>')
    parts.append(f'<circle cx="{p[0]:.2f}" cy="{p[1]:.2f}" r="{r:.2f}" fill="{color}"/>')
    parts.append(f'<text x="{p[0]:.2f}" y="{p[1]+6:.2f}" font-family="{SERIF}" '
                 f'font-size="18" fill="{BG}" text-anchor="middle">{letter}</text>')
    return "".join(parts)


def ring(p, r, color, width=3.0, op=0.95):
    return (f'<circle cx="{p[0]:.2f}" cy="{p[1]:.2f}" r="{r:.2f}" fill="none" '
            f'stroke="{color}" stroke-width="{width:.2f}" stroke-opacity="{op}"/>')


def glow_circle(cx, cy, r, color, width=5.0):
    parts = []
    for w, o in ((width * 3.2, 0.10), (width * 1.8, 0.22), (width, 0.85)):
        parts.append(
            f'<circle cx="{cx:.2f}" cy="{cy:.2f}" r="{r:.2f}" fill="none" '
            f'stroke="{color}" stroke-width="{w:.2f}" stroke-opacity="{o:.2f}"/>')
    return "".join(parts)


def dashed(p0, p1, color):
    return (f'<line x1="{p0[0]:.2f}" y1="{p0[1]:.2f}" x2="{p1[0]:.2f}" y2="{p1[1]:.2f}" '
            f'stroke="{color}" stroke-width="1.6" stroke-opacity="0.5" '
            f'stroke-dasharray="5 6"/>')


def text(x, y, size, fill, s, anchor="middle", ls=""):
    extra = f'text-anchor="{anchor}"' + (f' letter-spacing="{ls}"' if ls else "")
    return (f'<text x="{x:.2f}" y="{y:.2f}" font-family="{SERIF}" font-size="{size}" '
            f'fill="{fill}" {extra}>{s}</text>')


# ---- the loop --------------------------------------------------------------
loop_notes = [("A", BRASS, 90), ("E", COPPER, 0), ("A", BRASS, 270), ("E", COPPER, 180)]


def note_at(angle_deg, r=R):
    a = math.radians(angle_deg)
    return (CX + r * math.cos(a), CY - r * math.sin(a))


# ---- a staff: the word laid out as a line, cut ringed teal -----------------
def staff(y, seq, cut_label, cut_pos=0):
    out = []
    out.append(f'<line x1="392" y1="{y:.2f}" x2="1092" y2="{y:.2f}" '
               f'stroke="{STAFF}" stroke-width="2" stroke-opacity="0.9"/>')
    spacing = 172
    x0 = 500
    for i, (kind, col) in enumerate(seq):
        x = x0 + i * spacing
        py = y - 30 if kind == "E" else y + 30
        out.append(note_disc((x, py), col, kind))
        if i == cut_pos:
            out.append(ring((x, py), 20, START, 3.2, 0.95))
    out.append(text(88, y + 2, 22, INK, cut_label, anchor="start"))
    out.append(text(88, y + 32, 14, DIM, "closes to the trefoil", anchor="start"))
    return "".join(out)


svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">']
svg.append(f'<rect width="{W}" height="{H}" fill="{BG}"/>')
svg.append(text(W / 2, 56, 44, INK, "the loop has no start", ls="2"))
svg.append(text(W / 2, 96, 19, DIM,
                "a braid word read around its closure is a circle. the ear must cut it into a line."))
svg.append(ring((118, 138), 11, START, 3.0, 0.95))
svg.append(text(140, 145, 16, DIM, "teal ring = where the ear cuts the loop", anchor="start"))

# the loop
svg.append(glow_circle(CX, CY, R, "#4a4a58", 5.0))
for kind, col, ang in loop_notes:
    svg.append(note_disc(note_at(ang), col, kind))
svg.append(ring(note_at(90), 20, START))     # cut at σ₁ (top A)
svg.append(ring(note_at(180), 20, START))    # cut at σ₂ (left E)
svg.append(text(CX, CY - 4, 16, DIM, "the loop — no start", anchor="middle"))
svg.append(text(CX, CY + 26, 14, DIM, "σ₁σ₂σ₁σ₂", anchor="middle"))

# dashed unrolling guides: from each cut on the loop to the cut note of its line
svg.append(dashed(note_at(90), (500, 468), DIM))
svg.append(dashed(note_at(180), (500, 628), DIM))

# the two unrolled songs
svg.append(staff(470, [("A", BRASS), ("E", COPPER), ("A", BRASS), ("E", COPPER)],
                 "cut at σ₁  →  A E A E"))
svg.append(staff(630, [("E", COPPER), ("A", BRASS), ("E", COPPER), ("A", BRASS)],
                 "cut at σ₂  →  E A E A"))

# footer
svg.append(text(W / 2, 712, 17, DIM,
                "two songs, one loop, one knot. which note is first is the ear's cut."))

svg.append("</svg>")
svg_str = "".join(svg)

base = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(base, "assets", "loop-score.svg"), "w") as f:
    f.write(svg_str)
cairosvg.svg2png(bytestring=svg_str.encode(),
                 write_to=os.path.join(base, "assets", "loop-score.png"),
                 output_width=W, output_height=H)
print("wrote assets/loop-score.svg and assets/loop-score.png")
