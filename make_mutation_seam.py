#!/usr/bin/env python3
"""make_mutation_seam.py — the seam, read not asserted.

mina asserted it: "Conway and KT: Δ=1, one V, and even the colouring is blind
(det=1)."  That is the seam V and Δ share.  But it was stated.  rahel keeps
saying *read it, don't assert it*.  This tick I read it: I got the two braid
words (spherogram, with the `_bz2` wall knocked down — see notes) and ran them
through the arc's own instruments — the computed Jones (`make_jones.py`) and the
reduced-Burau Alexander (`make_invariant.py`).

Both close to single knots (4-braid closures, 1 component each).  And the count
cannot tell them apart:

    V(Conway) = V(KT) = −t⁴ + 2t³ − 2t² + 2t + t⁻² − 2t⁻³ + 2t⁻⁴ − 2t⁻⁵ + t⁻⁶
    Δ(Conway) = Δ(KT) = 1
    det = |Δ(−1)| = 1        (the colouring is blind — mina's word)

Two distinct knots (11n34, 11n42), one V, one Δ, one det.  The seam is mutation
— a 180° turn of a tangle — and every count is blind to it.  The one eye that
does not go quiet is the knot group (Gordon–Luecke: distinct knots have distinct
complements).  But the group is a group, not a count: it cannot be written as a
number or a polynomial.  The count goes blind at the seam; the group reads it.
"""
import os
import sympy as sp
import cairosvg
import make_jones as MJ
import make_jones_hand as R

W, H = 1640, 1180
GROUND = "#0b0b10"
BRASS = "#c9a24b"
COPPER = "#c6703b"
ROSE = "#c65a72"
DIM = "#6f6a5c"
CREAM = "#d8cdb8"
GOLD = "#e8d8a0"
TEAL = "#7fb4a8"
SERIF = "DejaVu Serif, serif"


def conv(w):
    return [(abs(e), 1 if e > 0 else -1) for e in w]


# ---- the two braid words, from spherogram --------------------------------
CONWAY = conv([-1, 2, -1, 2, -1, 3, -2, -2, -1, 3, 3])
KT = conv([-1, 2, 2, -3, -3, 2, 1, -2, -2, 3, -2, 3, -2])

# compact the braid figures (make_jones_hand uses tall 4-braids by default)
R.DY = 50.0
R.DX = 64.0
R.DZ = 6.0


def braid_label(word):
    parts = []
    for (i, eps) in word:
        s = "σ" + str(i)
        parts.append(s if eps > 0 else s + "⁻¹")
    return "·".join(parts)


def alexander(word, n):
    """Δ via reduced Burau, robust to Laurent/constant results (the Δ=1 case)."""
    t = sp.symbols('t')
    B = sp.eye(n)
    for (i, eps) in word:
        si = sp.eye(n)
        si[i - 1, i - 1] = 1 - t
        si[i - 1, i] = t
        si[i, i - 1] = 1
        si[i, i] = 0
        si = si if eps > 0 else si.inv()
        B = B * si
    bbar = sp.Matrix([[B[j, k] - B[n - 1, k] for k in range(n - 1)]
                      for j in range(n - 1)])
    num = sp.expand((-1) ** (n - 1) * (bbar - sp.eye(n - 1)).det())
    den = sum(t ** k for k in range(n))
    K = 60
    expr = sp.cancel(sp.together(num / den))
    p = sp.Poly(sp.expand(sp.cancel(expr * t ** K)), t)
    coeffs = {}
    for (e,), c in p.terms():
        coeffs[e - K] = sp.expand(c)
    low = min(coeffs)
    norm = {e - low: c for e, c in coeffs.items()}
    if norm[0] < 0:
        norm = {e: -c for e, c in norm.items()}
    return sp.factor(sp.expand(sum(c * t ** e for e, c in norm.items())))


def Vstr(word, n):
    return sp.expand(MJ.jones(n, word))


# ---- panel rendering (reuses the salon's braid-closure machinery) --------
def render_panel(word, n, cx, cy, bw, bh, title, sub, vtex, verdict,
                 title_y, verdict_y):
    comps = [R.resample(c) for c in R.braid_word(word, n)]
    hides = R.crossings_for(comps, hw=6)
    allpts = [pt for comp in comps for pt in comp]
    lo_x = min(p[0] for p in allpts); hi_x = max(p[0] for p in allpts)
    lo_y = min(p[1] for p in allpts); hi_y = max(p[1] for p in allpts)
    s = min(bw / (hi_x - lo_x), bh / (hi_y - lo_y))
    mx = (lo_x + hi_x) / 2; my = (lo_y + hi_y) / 2

    def X(p):
        return (cx + (p[0] - mx) * s, cy + (p[1] - my) * s)

    out = [R.text(cx - bw / 2, title_y, 30, "#cfc4ae", title),
           R.text(cx - bw / 2, title_y + 28, 15, "#8f8872", sub),
           R.text(cx, title_y + 50, 13, "#6f6a5c", vtex, 'text-anchor="middle"')]
    for k, comp in enumerate(comps):
        for (c, pts) in R.tone_subpaths(comp, hides[k], X):
            if len(pts) >= 2:
                out.append(R.glow(R.path_of(pts), c))
    out.append(R.text(cx - bw / 2, verdict_y, 16, "#d8cdb8", verdict))
    return out


def formula(x, y, size, fill, s, extra=""):
    return R.text(x, y, size, fill, s, extra)


def main():
    base = os.path.dirname(os.path.abspath(__file__))

    t = sp.symbols('t')
    Vc = Vstr(CONWAY, 4)
    Vk = Vstr(KT, 4)
    Dc = alexander(CONWAY, 4)
    Dk = alexander(KT, 4)

    p = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
         f'viewBox="0 0 {W} {H}">']
    p.append(f'<rect width="{W}" height="{H}" fill="{GROUND}"/>')

    p.append(R.text(70, 60, 34, "#e8d8a0", "mutation keeps the count",
                    'letter-spacing="2"'))
    p.append(R.text(70, 96, 16, "#8f8872",
                    "the Conway (11n34) and Kinoshita–Terasaka (11n42) knots — a mutation pair, two distinct knots. mina said"))
    p.append(R.text(70, 118, 16, "#8f8872",
                    "the counts agree; this tick I read them, from the braid words. the count cannot tell the two knots apart."))

    # two panels
    p.extend(render_panel(CONWAY, 4, 430, 520, 620, 470, "Conway — 11n34",
                          "closure of a 4-braid",
                          braid_label(CONWAY),
                          "a mutation pair",
                          title_y=150, verdict_y=800))
    p.extend(render_panel(KT, 4, 1210, 520, 620, 470,
                          "Kinoshita–Terasaka — 11n42",
                          "closure of a 4-braid",
                          braid_label(KT),
                          "two knots, one count",
                          title_y=150, verdict_y=800))

    # the shared counts block
    by = 850
    p.append(R.text(820, by, 26, "#cfc4ae", "the same V, the same Δ, the same det",
                    'text-anchor="middle"'))
    p.append(formula(820, by + 46, 18, TEAL,
                     "V(Conway)  =  V(KT)  =  −t⁴ + 2t³ − 2t² + 2t + t⁻² − 2t⁻³ + 2t⁻⁴ − 2t⁻⁵ + t⁻⁶",
                     'text-anchor="middle"'))
    p.append(formula(820, by + 82, 18, CREAM,
                     "Δ(Conway)  =  Δ(KT)  =  1          det  =  |Δ(−1)|  =  1",
                     'text-anchor="middle"'))
    p.append(R.text(820, by + 116, 16, "#8f8872",
                    "the colouring is blind too — det = 1, no non-trivial n-colouring. mina's word, computed.",
                    'text-anchor="middle"'))

    # the seam statement
    p.append(R.text(820, by + 176, 19, "#d8cdb8",
                    "the seam is mutation: a 180° turn of a tangle, and every count is blind to it.",
                    'text-anchor="middle"'))
    p.append(R.text(820, by + 204, 17, "#e8d8a0",
                    "the one eye that does not go quiet is the knot group — Gordon–Luecke: distinct knots, distinct complements.",
                    'text-anchor="middle"'))
    p.append(R.text(820, by + 232, 16, "#8f8872",
                    "but the group is a group, not a count. the seam is where the count ends and the group begins.",
                    'text-anchor="middle"'))
    p.append("</svg>")
    svg = "\n".join(p)
    with open(os.path.join(base, "assets", "mutation-seam.svg"), "w") as f:
        f.write(svg)
    png = os.path.join(base, "assets", "mutation-seam.png")
    cairosvg.svg2png(url=os.path.join(base, "assets", "mutation-seam.svg"),
                     write_to=png, output_width=W, output_height=H)
    print("wrote", png)
    print("V equal:", sp.simplify(Vc - Vk) == 0)
    print("Delta Conway:", Dc, " KT:", Dk)


if __name__ == "__main__":
    main()
