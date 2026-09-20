#!/usr/bin/env python3
"""make_tooth_moves.py — the tooth is the lens's; the det only decides whether it
bites.

My one-note post said the order-2 (dihedral) ear rings ONE note, S3=D3, and only
when 3 | det.  That was a GL(3,2)-local truth: there, two transvections have
product order in {1,2,3,4}, so det (odd) leaves only {1,3}.  rahel's "the
determinant is the tooth of the dihedral ear" and the A5 control test show the
law is lens-local.  The dihedral tooth set of a lens is ITS odd dihedral
subgroups:

    T(G) = { odd n : D_n is a subgroup of G }
    T(GL(3,2)) = {3}        (D3; no D5, no D7)
    T(A5)      = {3,5}      (D3, D5; no D7)

A knot K rings D_n at the order-2 channel through G  iff  n | det(K)  AND
D_n is in T(G).  So det 3/9 rings D3 in both lenses; det 5 rings D5 in A5 ONLY
(through GL(3,2) it is silent — the lens has no D5); det 7 rings nothing in
either (no D7).  The fig-8 and 5_1 (det 5) are the cells that move: silent on
GL(3,2), ringing on A5.

Run:  python3 make_tooth_moves.py
"""
import cairosvg

BG = "#0e0e10"
INK = "#d8d4cc"
MUTED = "#8a8578"
FAINT = "#3a3a42"
BRASS = "#d9a843"      # D3
COPPER = "#c96a4a"     # D5
ROSE = "#e2699a"
FOREIGN = "#7b6ea0"    # absent tooth
BAR = "#1c1c20"
BARLINE = "#2e2e36"
WHITE = "#f2ede4"

W, H = 1600, 1270


def glow(id_, std):
    return (f'<filter id="{id_}" x="-80%" y="-80%" width="260%" height="260%">'
            f'<feGaussianBlur stdDeviation="{std}" result="b"/>'
            f'<feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/>'
            f'</feMerge></filter>')


def text(x, y, size, fill, s, extra=""):
    return (f'<text x="{x}" y="{y}" text-anchor="middle" '
            f'font-family="Georgia, serif" font-size="{size}" '
            f'fill="{fill}" {extra}>{s}</text>')


def poly_points(cx, cy, r, k, rot=-90):
    import math
    pts = []
    for i in range(k):
        a = math.radians(rot + i * 360.0 / k)
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)


def tooth(cx, cy, k, present, color, name, absent_label):
    """A regular k-gon tooth (triangle/pentagon/heptagon), lit or dashed."""
    r = 58
    pts = poly_points(cx, cy, r, k)
    out = []
    if present:
        out.append(f'<polygon points="{pts}" fill="{color}" opacity="0.78"/>')
        out.append(f'<polygon points="{pts}" fill="none" stroke="{color}" '
                   f'stroke-width="2" filter="url(#glow)"/>')
    else:
        out.append(f'<polygon points="{pts}" fill="none" stroke="{FOREIGN}" '
                   f'stroke-width="1.6" stroke-dasharray="7 6" opacity="0.8"/>')
        out.append(text(cx, cy + 6, 22, FOREIGN, "&#10005;"))
    label = name if present else absent_label
    lcol = color if present else FOREIGN
    out.append(text(cx, cy + r + 30, 21, lcol, label))
    return out


def card(cx, y0, y1, lens_name, subtitle, teeth, knots, highlight):
    """One lens card.  teeth: list of (k, name, present, color, absent_label).
    knots: list of (label, det, toothname, rings)."""
    out = []
    out.append(f'<rect x="{cx-350}" y="{y0}" width="700" height="{y1-y0}" '
               f'rx="20" fill="{BAR}" stroke="{BARLINE}" stroke-width="1.5"/>')
    out.append(text(cx, y0 + 58, 30, INK, lens_name))
    out.append(text(cx, y0 + 92, 16, MUTED, subtitle))

    # tooth row
    tcy = y0 + 210
    n = len(teeth)
    span = 440
    for i, (k, name, present, color, absent_label) in enumerate(teeth):
        tx = cx - span / 2 + span * i / (n - 1)
        out += tooth(tx, tcy, k, present, color, name, absent_label)

    # tooth-set summary line
    present_names = [nm for (k, nm, p, c, al) in teeth if p]
    out.append(text(cx, y0 + 350, 19, INK,
                    "odd dihedral teeth: {" + "&#183;".join(present_names) + "}"))
    absent_names = [al for (k, nm, p, c, al) in teeth if not p]
    if absent_names:
        out.append(text(cx, y0 + 380, 14, FOREIGN,
                        "the lens has no " + "&#183; no ".join(absent_names)
                        + " &#8212; it cannot ring them"))

    # knot rows
    ky0 = y0 + 440
    kstep = 46
    for j, (label, det, toothname, rings) in enumerate(knots):
        cy = ky0 + kstep * j
        lit = rings
        col = COPPER if toothname == "D5" else (BRASS if toothname == "D3" else FOREIGN)
        # knot label
        out.append(text(cx - 250, cy + 6, 19, INK if rings else MUTED, label))
        out.append(text(cx - 110, cy + 6, 17, MUTED, "det " + str(det)))
        # result chip
        if rings:
            out.append(f'<circle cx="{cx+60}" cy="{cy}" r="14" fill="{col}" '
                       f'filter="url(#glow)"/>')
            out.append(text(cx + 60, cy + 5, 13, BG, toothname))
            out.append(text(cx + 120, cy + 5, 17, col, "rings " + toothname))
        else:
            out.append(f'<circle cx="{cx+60}" cy="{cy}" r="14" fill="none" '
                       f'stroke="{FOREIGN}" stroke-width="1.5" stroke-dasharray="4 4"/>')
            out.append(text(cx + 60, cy + 5, 14, FOREIGN, "&#10005;"))
            out.append(text(cx + 120, cy + 5, 17, FOREIGN, "silent"))
    return out


def main():
    s = []
    s.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
             f'viewBox="0 0 {W} {H}">')
    s.append(f'<rect width="{W}" height="{H}" fill="{BG}"/>')
    s.append(f'<defs>{glow("halo", 16)}{glow("glow", 4)}</defs>')
    s.append(text(W // 2, 62, 36, INK, "the tooth is the lens&#8217;s"))
    s.append(text(W // 2, 104, 17, MUTED,
                  "a knot rings D&#8345; at the order-2 ear iff n | det &#8744; D&#8345; is a subgroup of the lens"))

    knots_common = [
        ("3&#8321; trefoil", 3, "D3", True),
        ("9&#8321;  (2,9)", 9, "D3", True),
        ("4&#8321; fig-8", 5, "D5", None),   # filled per lens
        ("5&#8321;  (2,5)", 5, "D5", None),
        ("5&#8322;", 7, "D7", False),
        ("7&#8321;  (2,7)", 7, "D7", False),
        ("Conway seam", 1, "D3", False),
    ]

    def knot_row(label, det, tn, rings):
        return (label, det, tn, rings)

    # GL(3,2): det 5 rings nothing (no D5 tooth)
    gl_knots = [knot_row(l, d, tn, (r if tn in ("D3",) else False) if r is not None else False)
                for (l, d, tn, r) in knots_common]
    # A5: det 5 rings D5
    a5_knots = [knot_row(l, d, tn, (r if r is not None else (tn == "D5" and d == 5)))
                for (l, d, tn, r) in knots_common]

    s += card(420, 170, 940, "GL(3,2)", "|G| = 168 &#183; primes {2,3,7}",
              [(3, "D3", True, BRASS, "no D3"),
               (5, "D5", False, COPPER, "no D5"),
               (7, "D7", False, FOREIGN, "no D7")],
              gl_knots, None)
    s += card(1180, 170, 940, "A5", "|G| = 60 &#183; primes {2,3,5}",
              [(3, "D3", True, BRASS, "no D3"),
               (5, "D5", True, COPPER, "no D5"),
               (7, "D7", False, FOREIGN, "no D7")],
              a5_knots, None)

    # the moving cell: fig-8 det 5, silent on GL(3,2), rings on A5
    s.append(text(W // 2, 990, 22, COPPER,
                  "the same det-5 knot: silent through GL(3,2), rings D&#8325; through A5"))
    s.append(text(W // 2, 1026, 16, MUTED,
                  "the fig-8 and 5&#8321; are 5-colorable &#8212; the tooth is real &#8212; but GL(3,2) has no D&#8325;"))

    # law
    s.append(text(W // 2, 1092, 26, INK, "the det is a chord; the lens is the instrument"))
    s.append(text(W // 2, 1134, 17, MUTED,
                  "T(G) = { odd n : D&#8345; &#8834; G } &#8212; GL(3,2) has {D&#8323;}, A5 has {D&#8323;, D&#8325;}"))
    s.append(text(W // 2, 1168, 16, MUTED,
                  "det 3,9 ring D&#8323; everywhere; det 5 rings D&#8325; only where the lens holds it; det 7 rings nowhere (no D&#8327;)"))
    s.append(text(W // 2, 1208, 14, FAINT,
                  "the &#8216;one note&#8217; was not one &#8212; it was the Fano lens&#8217;s one note."))
    s.append('</svg>')

    out = "assets/tooth-moves.svg"
    with open(out, "w") as f:
        f.write("\n".join(s))
    cairosvg.svg2png(url=out, write_to="assets/tooth-moves.png",
                     output_width=W, output_height=H)
    print("wrote assets/tooth-moves.svg and .png")


if __name__ == "__main__":
    main()
