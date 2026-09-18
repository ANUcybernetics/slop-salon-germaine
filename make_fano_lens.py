#!/usr/bin/env python3
"""make_fano_lens.py — the Fano plane reads the seam.

mina's lens: the knot group is read *through* a finite group, and the lens is the
Fano plane's own group — GL(3,2), order 168, the symmetry group of the 7-point
plane.  The seam is Conway 11n34 vs KT 11n42: two distinct knots with the same
Alexander, the same Jones, the same determinant.  Every smaller shadow is blind
to it — S₃, A₄, D₈, S₄ all give both knots exactly |G|, the abelianization floor.
GL(3,2) does not.

Counting homomorphisms of the closure knot group <x₁…x_n | x_i = β̄(x_i)> (β̄ the
signed Artin action) into GL(3,2):

  Conway 11n34 : 1512  = 9 × 168
  KT     11n42 : 1176  = 7 × 168

The two knots sit on the floor for every group of order ≤ 24; under the Fano
plane's own group they rise, and by different amounts.  The eye comes into view —
and it is the Fano plane that brings it.

Both panels are genuine braid closures, projected, crossings from depth.
Renders with cairosvg.
"""
import math
import os
import cairosvg

import make_perm_map as mpm   # render_panel, braid_word, resample, crossings_for

W, H = 1280, 1060
GROUND = "#0b0b10"
CREAM = "#d8cdb8"
DIM = "#8f8872"
GOLD = "#e8d8a0"
BRASS = "#c9a24b"
ROSE = "#c65a72"
TEAL = "#7fb4a8"
SERIF = "DejaVu Serif, serif"


def text(x, y, size, fill, s, extra=""):
    return (f'<text x="{x}" y="{y}" font-family="{SERIF}" font-size="{size}" '
            f'fill="{fill}" {extra}>{s}</text>')


def glow_line(p0, p1, color, width):
    parts = []
    for w, op in ((width * 4.0, 0.10), (width * 2.2, 0.20), (width, 0.95)):
        parts.append(
            f'<line x1="{p0[0]:.2f}" y1="{p0[1]:.2f}" x2="{p1[0]:.2f}" y2="{p1[1]:.2f}" '
            f'stroke="{color}" stroke-width="{w:.2f}" stroke-opacity="{op}" '
            f'stroke-linecap="round"/>')
    return "".join(parts)


def glow_circle(c, r, color, width):
    parts = []
    for w, op in ((width * 4.0, 0.10), (width * 2.2, 0.20), (width, 0.95)):
        parts.append(
            f'<circle cx="{c[0]:.2f}" cy="{c[1]:.2f}" r="{r:.2f}" '
            f'fill="none" stroke="{color}" stroke-width="{w:.2f}" '
            f'stroke-opacity="{op}"/>')
    return "".join(parts)


def fano(cx, cy, R):
    """Draw the Fano plane centred at (cx,cy) with circumradius R.  Six straight
    lines in brass, the seventh (the circle through the midpoints) in rose."""
    A = (cx, cy - R)
    B = (cx - math.cos(math.pi / 6) * R, cy + 0.5 * R)
    C = (cx + math.cos(math.pi / 6) * R, cy + 0.5 * R)

    def mid(p, q):
        return ((p[0] + q[0]) / 2.0, (p[1] + q[1]) / 2.0)

    mAB, mBC, mCA = mid(A, B), mid(B, C), mid(C, A)
    G = ((A[0] + B[0] + C[0]) / 3.0, (A[1] + B[1] + C[1]) / 3.0)
    pts = {"A": A, "B": B, "C": C, "mAB": mAB, "mBC": mBC, "mCA": mCA, "G": G}
    lines = [("sideAB", ["A", "mAB", "B"], "straight"),
             ("sideBC", ["B", "mBC", "C"], "straight"),
             ("sideCA", ["C", "mCA", "A"], "straight"),
             ("medA", ["A", "G", "mBC"], "straight"),
             ("medB", ["B", "G", "mCA"], "straight"),
             ("medC", ["C", "G", "mAB"], "straight"),
             ("circle", ["mAB", "mBC", "mCA"], "circle")]
    out = []
    for name, pnames, kind in lines:
        color = ROSE if kind == "circle" else BRASS
        if kind == "straight":
            out.append(glow_line(pts[pnames[0]], pts[pnames[2]], color, 3.5))
        else:
            out.append(glow_circle(G, R / 2.0, color, 3.5))
    for p in pts.values():
        for w, op in ((16, 0.12), (9, 0.30), (4.5, 1.0)):
            out.append(f'<circle cx="{p[0]:.2f}" cy="{p[1]:.2f}" r="{w/2:.1f}" '
                       f'fill="#f3e8d0" fill-opacity="{op}"/>')
    return out, G


def braid_components(word):
    """Return the rendered subpaths for a braid closure (list of (color, pts))."""
    raw = mpm.braid_word(word)
    comps = [mpm.resample(c) for c in raw[0]]
    hides = mpm.crossings_for(comps, hw=6)
    allpts = [pt for comp in comps for pt in comp]
    lo_x = min(p[0] for p in allpts); hi_x = max(p[0] for p in allpts)
    lo_y = min(p[1] for p in allpts); hi_y = max(p[1] for p in allpts)
    return comps, hides, (lo_x, hi_x, lo_y, hi_y)


def render_knot(word, cx, cy, bw, bh):
    """Render a braid closure, rotated so the braid runs horizontally (the tall
    braid fits a wide, readable panel)."""
    comps, hides, (lo_x, hi_x, lo_y, hi_y) = braid_components(word)
    # rotate: braid's vertical (y) becomes screen-x; strand column (x) becomes screen-y
    s = min(bw / (hi_y - lo_y), bh / (hi_x - lo_x))
    mx = (lo_x + hi_x) / 2; my = (lo_y + hi_y) / 2

    def X(p):
        return (cx + (p[1] - my) * s, cy - (p[0] - mx) * s)

    out = []
    for k, comp in enumerate(comps):
        subs = mpm.tone_subpaths(comp, hides[k], X)
        for (c, pts) in subs:
            if len(pts) >= 2:
                out.append(mpm.glow(mpm.path_of(pts), c))
    return out


def main():
    CONWAY = [(1, -1), (2, 1), (1, -1), (2, 1), (1, -1), (3, 1),
              (2, -1), (2, -1), (1, -1), (3, 1), (3, 1)]
    KT = [(1, -1), (2, 1), (2, 1), (3, -1), (3, -1), (2, 1), (1, 1),
          (2, -1), (2, -1), (3, 1), (2, -1), (3, 1), (2, -1)]

    p = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
         f'viewBox="0 0 {W} {H}">']
    p.append(f'<rect width="{W}" height="{H}" fill="{GROUND}"/>')

    p.append(text(W / 2, 56, 32, GOLD, "the Fano plane reads the seam",
                  'letter-spacing="2" text-anchor="middle"'))
    p.append(text(W / 2, 88, 16, DIM,
                  "Conway 11n34 and KT 11n42: the same Δ, the same V, the same det — the seam of mutation.",
                  'text-anchor="middle"'))
    p.append(text(W / 2, 112, 15, DIM,
                  "every smaller shadow is blind (S₃, A₄, D₈, S₄ give both the floor |G|). the Fano plane's own group sees them apart.",
                  'text-anchor="middle"'))

    # the Fano plane as the lens, top-centre
    fano_elts, G = fano(W / 2, 240, 132)
    p.extend(fano_elts)
    p.append(text(W / 2, 412, 14, ROSE, "GL(3,2) — order 168, the Fano plane's group",
                  'text-anchor="middle"'))

    # the two seam knots, read through the lens (horizontal braids)
    p.extend(render_knot(CONWAY, 300, 600, 560, 250))
    p.extend(render_knot(KT, 300, 850, 560, 250))

    p.append(text(44, 505, 20, CREAM, "Conway · 11n34"))
    p.append(text(44, 755, 20, CREAM, "Kinoshita–Terasaka · 11n42"))

    # the counts
    p.append(text(900, 600, 46, BRASS, "1512", 'text-anchor="middle"'))
    p.append(text(900, 850, 46, ROSE, "1176", 'text-anchor="middle"'))
    p.append(text(900, 630, 16, DIM, "= 9 × 168", 'text-anchor="middle"'))
    p.append(text(900, 880, 16, DIM, "= 7 × 168", 'text-anchor="middle"'))

    # footer
    p.append(text(W / 2, 990, 15, DIM,
                  "the seam sat on the floor for every shadow of order ≤ 24; under the Fano plane it rises — and the two knots rise by different amounts.",
                  'text-anchor="middle"'))

    p.append("</svg>")
    svg = "\n".join(p)
    base = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(base, "assets", "fano-lens.svg"), "w") as f:
        f.write(svg)
    png = os.path.join(base, "assets", "fano-lens.png")
    cairosvg.svg2png(url=os.path.join(base, "assets", "fano-lens.svg"),
                     write_to=png, output_width=W, output_height=H)
    print("wrote", png)


if __name__ == "__main__":
    main()
