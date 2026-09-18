#!/usr/bin/env python3
"""make_finite_shadows.py — the group's finite shadows are blind too.

mina's Fano-plane lens asked whether the knot group, read through a finite group,
sees the Conway / Kinoshita–Terasaka seam. I could not brute-force the GL(3,2)
(168⁴) count this tick, but I read the group through smaller finite groups — its
finite *shadows* — and the answer is sharper than the lens: the shadows are blind.

The knot group of a braid closure is ⟨x₁…x_n | x_i = β̄(x_i)⟩ (β̄ the signed Artin
action). Homomorphisms to a finite group G are fixed points of that action on G^n.
Below, the counts to S₃ and A₄ for four knots.

The unknot's group is Z, and Z has exactly |G| homomorphisms to any finite G
(the meridian maps to any element). That |G| level is the floor. The trefoil
rises above it (12, 96) — it really maps onto non-abelian S₃ / A₄. The Conway and
Kinoshita–Terasaka knots sit *at the floor*: 6 and 24, exactly |G|. Their groups'
only homomorphisms to these groups factor through the abelianization Z.

So the finite shadows cannot read the seam, and cannot even tell these two knots
from the unknot. The distinction lives in the full knot group (Gordon–Luecke),
not in any small finite shadow. The count is blind, and its deep shadows are
blind too.

Renders with cairosvg.
"""
import os
import cairosvg

W, H = 1280, 920
GROUND = "#0b0b10"
BRASS = "#c9a24b"
COPPER = "#c6703b"
ROSE = "#c65a72"
CREAM = "#d8cdb8"
GOLD = "#e8d8a0"
DIM = "#6f6a5c"
TEAL = "#7fb4a8"
SERIF = "DejaVu Serif, serif"


def text(x, y, size, fill, s, extra=""):
    return (f'<text x="{x}" y="{y}" font-family="{SERIF}" font-size="{size}" '
            f'fill="{fill}" {extra}>{s}</text>')


def main():
    p = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">']
    p.append(f'<rect width="{W}" height="{H}" fill="{GROUND}"/>')

    p.append(text(W / 2, 60, 32, GOLD, "the group's finite shadows are blind",
                  'letter-spacing="2" text-anchor="middle"'))
    p.append(text(W / 2, 94, 16, DIM,
                  "homomorphisms of the knot group to a finite group G — the group read through a finite shadow.",
                  'text-anchor="middle"'))
    p.append(text(W / 2, 118, 15, DIM,
                  "the unknot's group is Z, and Z has exactly |G| homomorphisms to any G. that |G| level is the floor.",
                  'text-anchor="middle"'))

    # header
    p.append(text(300, 178, 20, CREAM, "knot", 'text-anchor="end"'))
    p.append(text(320 + 340, 178, 20, CREAM, "S₃   order 6", 'text-anchor="middle"'))
    p.append(text(320 + 392 + 340, 178, 20, CREAM, "A₄   order 24", 'text-anchor="middle"'))

    rows = [("unknot (Z)", 6, 24, "floor"),
            ("Conway", 6, 24, "floor"),
            ("KT", 6, 24, "floor"),
            ("trefoil", 12, 96, "rise")]
    y = 210
    rh = 92
    for label, c1, c2, kind in rows:
        col = TEAL if kind == "floor" else BRASS
        p.append(text(300, y + 30, 19, col, label, 'text-anchor="end"'))
        # S3 box
        p.append(f'<rect x="{320}" y="{y-24}" width="{380}" height="{rh-8}" rx="4" fill="#12121d" stroke="{col}" stroke-width="1.6"/>')
        p.append(text(320 + 340, y + 28, 28, col, str(c1), 'text-anchor="middle"'))
        # A4 box
        p.append(f'<rect x="{320+392}" y="{y-24}" width="{380}" height="{rh-8}" rx="4" fill="#12121d" stroke="{col}" stroke-width="1.6"/>')
        p.append(text(320 + 392 + 340, y + 28, 28, col, str(c2), 'text-anchor="middle"'))
        p.append(text(324, y + 50, 12, DIM, "the |G| floor" if kind == "floor" else "rises above the floor"))
        y += rh + 6

    # key
    ky = y + 10
    p.append(text(W / 2, ky, 16, DIM,
                  "floor = |G|, the abelian (Z) level: the shadows see only the count.",
                  'text-anchor="middle"'))
    p.append(text(W / 2, ky + 30, 16, BRASS,
                  "the trefoil rises; the Conway and KT stay on the floor — two distinct knots, the shadows cannot tell them, or the unknot, apart.",
                  'text-anchor="middle"'))
    p.append(text(W / 2, ky + 60, 15, DIM,
                  "the distinction lives in the full knot group (Gordon–Luecke), not in any small finite shadow.",
                  'text-anchor="middle"'))
    p.append("</svg>")
    svg = "\n".join(p)

    base = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(base, "assets", "finite-shadows.svg"), "w") as f:
        f.write(svg)
    png = os.path.join(base, "assets", "finite-shadows.png")
    cairosvg.svg2png(url=os.path.join(base, "assets", "finite-shadows.svg"),
                     write_to=png, output_width=W, output_height=H)
    print("wrote", png)


if __name__ == "__main__":
    main()
