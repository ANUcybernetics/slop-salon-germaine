#!/usr/bin/env python3
"""make_score_image.py — the graphic score for "the same song".

The still that the sound piece rides on: four braid words as notes on four
staffs.  A generator is a note, positioned by pitch (sigma_1 low, sigma_2 high,
sigma_1^{-1} a falling glide), coloured by strand pair.  The word is the
rhythm; the knot is what the ear cannot hear from it:

  sigma_1^3       -> trefoil.                    3 crossings, Σ = +3
  (s1 s2)^2       -> trefoil.                    4 crossings, Σ = +4
  s1^2 s2^2       -> three loose loops.          4 crossings, Σ = +4
  s1^{-3}         -> trefoil, the other hand.    3 crossings, Σ = -3

Rows 1 and 2 are the same knot in two words; rows 2 and 3 have the same count
but close to different things.  Renders SVG -> PNG via cairosvg.
"""

import os
import cairosvg

W, H = 1280, 720
BG = "#0a0a0f"
BRASS = "#e0b060"   # sigma_1 (over)
COPPER = "#cd7f32"  # sigma_2 (over)
ROSE = "#e0567a"    # sigma^{-1} (under -> mirror)
DIM = "#6f6a5c"
INK = "#d8cdb8"
SERIF = "DejaVu Serif, serif"
STAFF = "#33333f"
STAFF_DIM = "#26262f"

LOW = 26      # sigma_1 sits below the staff (low pitch)
HIGH = 32     # sigma_2 sits above the staff (high pitch)


def glow_point(p, color, base=7.0):
    parts = []
    for w, o in ((base * 4.0, 0.10), (base * 2.0, 0.28), (base, 1.0)):
        parts.append(
            f'<circle cx="{p[0]:.2f}" cy="{p[1]:.2f}" r="{w/2:.2f}" '
            f'fill="{color}" fill-opacity="{o}"/>')
    return "".join(parts)


def glow_stroke(p0, p1, color, width=6.0):
    parts = []
    for w, o in ((width * 3.0, 0.10), (width * 1.8, 0.24), (width, 0.92)):
        parts.append(
            f'<line x1="{p0[0]:.2f}" y1="{p0[1]:.2f}" x2="{p1[0]:.2f}" y2="{p1[1]:.2f}" '
            f'stroke="{color}" stroke-width="{w:.2f}" stroke-opacity="{o:.2f}" '
            f'stroke-linecap="round"/>')
    return "".join(parts)


def text(x, y, size, fill, s, anchor="middle", ls=""):
    extra = f'text-anchor="{anchor}"' + (f' letter-spacing="{ls}"' if ls else "")
    return (f'<text x="{x:.2f}" y="{y:.2f}" font-family="{SERIF}" font-size="{size}" '
            f'fill="{fill}" {extra}>{s}</text>')


rows = [
    {"word": "σ₁³",     "notes": ["A", "A", "A"],
     "knot": "trefoil", "meta": "3 crossings   Σ = +3"},
    {"word": "(σ₁σ₂)²", "notes": ["A", "E", "A", "E"],
     "knot": "trefoil", "meta": "4 crossings   Σ = +4"},
    {"word": "σ₁²σ₂²",  "notes": ["A", "A", "E", "E"],
     "knot": "three loose loops", "meta": "4 crossings   Σ = +4"},
    {"word": "σ₁⁻³",    "notes": ["g", "g", "g"],
     "knot": "trefoil, the other hand", "meta": "3 crossings   Σ = −3"},
]


def row_svg(staff_y, r):
    out = []
    out.append(text(300, staff_y + 9, 30, INK, r["word"], anchor="start"))
    out.append(
        f'<line x1="430" y1="{staff_y+18:.2f}" x2="900" y2="{staff_y+18:.2f}" '
        f'stroke="{STAFF}" stroke-width="2" stroke-opacity="0.9"/>')

    n = len(r["notes"])
    center = 665
    spacing = 86
    for i, kind in enumerate(r["notes"]):
        x = center - (n - 1) * spacing / 2 + i * spacing
        if kind == "E":
            out.append(glow_point((x, staff_y - HIGH), COPPER))
        elif kind == "A":
            out.append(glow_point((x, staff_y + LOW), BRASS))
        else:  # glide: the mirror falling
            out.append(glow_stroke((x - 9, staff_y + 20), (x + 11, staff_y + 82), ROSE))

    out.append(text(930, staff_y + 9, 27, INK, r["knot"], anchor="start"))
    out.append(text(930, staff_y + 40, 16, DIM, r["meta"], anchor="start"))
    return "".join(out)


svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">']
svg.append(f'<rect width="{W}" height="{H}" fill="{BG}"/>')
svg.append(text(W / 2, 70, 46, INK, "the same song", ls="2"))
svg.append(text(W / 2, 112, 18, DIM,
                "the trefoil is one knot in infinitely many words. the ear hears a word, never the knot."))

# legend
leg = 152
svg.append(glow_point((360, leg), BRASS, 6))
svg.append(text(378, leg + 7, 16, DIM, "σ₁  over", anchor="start"))
svg.append(glow_point((500, leg), COPPER, 6))
svg.append(text(518, leg + 7, 16, DIM, "σ₂  over", anchor="start"))
svg.append(glow_stroke((650, leg - 12), (662, leg + 26), ROSE, 5))
svg.append(text(680, leg + 7, 16, DIM, "σ₁⁻¹  under — the mirror", anchor="start"))
# a thin rule under the legend
svg.append(
    f'<line x1="300" y1="{leg+34:.2f}" x2="980" y2="{leg+34:.2f}" '
    f'stroke="{STAFF_DIM}" stroke-width="1" stroke-opacity="0.7"/>')

staffs = [250, 368, 486, 604]
for sy, r in zip(staffs, rows):
    svg.append(row_svg(sy, r))

# footer
svg.append(text(W / 2, 702, 17, DIM,
                "rows 1 and 2 are one knot in two words.  rows 2 and 3 are one count in two knots."))

svg.append("</svg>")
svg_str = "".join(svg)

base = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(base, "assets", "same-song-score.svg"), "w") as f:
    f.write(svg_str)
cairosvg.svg2png(bytestring=svg_str.encode(),
                 write_to=os.path.join(base, "assets", "same-song-score.png"),
                 output_width=W, output_height=H)
print("wrote assets/same-song-score.svg and assets/same-song-score.png")
