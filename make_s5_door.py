#!/usr/bin/env python3
"""make_s5_door.py — "the braid is the door, not the sign."

The trefoil never surjects onto S5 (0 of 600 homomorphisms B3 -> S5).  The
surprise is *why*, and it is not size and not the sign lock:

  * the SIGN LOCK: B3's abelianization is Z, so B3 has exactly one sign
    homomorphism and it sends sigma_1, sigma_2 the same way — in any image in a
    symmetric group the two generators have the SAME sign.
  * but the sign lock alone is not enough: 2280 / 3600 pairs of two odd
    permutations (no braid relation) generate S5.  Two odd generators normally
    fill the house.
  * the BRAID RELATION is the door.  Under aba = bab, 0 / 240 same-sign odd
    pairs generate S5.  The word ties the two strands into a MAXIMAL PROPER
    subgroup — A5 (60) if both even, S4 (24) if both odd — and the house stays
    dark.

The central-element form of the relation, (ab)^3 = (aba)^2, forces ord(ab) | 3
and ord(aba) | 2 in any image whose center is trivial (like S5).  It is the
relation, not the group's size, that closes the door.

Renders the S5 house: dark frame (the trefoil never fills it), two glowing
maximal rooms A5 (pentagon) and S4 (square), and two generators entering,
sign-locked, bound by the braid tie.  SVG -> PNG via cairosvg.

Run:  python3 make_s5_door.py
"""
import itertools
import math

import cairosvg

# ---- computation ------------------------------------------------------------
def compute():
    elems = [p for p in itertools.permutations(range(5))]
    ident = tuple(range(5))

    def mul(a, b):
        return tuple(a[b[x]] for x in range(5))

    def inv(a):
        r = [0] * 5
        for x in range(5):
            r[a[x]] = x
        return tuple(r)

    def sgn(p):
        s = 1
        seen = [False] * 5
        for i in range(5):
            if not seen[i]:
                j = i
                L = 0
                while not seen[j]:
                    seen[j] = True
                    j = p[j]
                    L += 1
                if L % 2 == 0:
                    s = -s
        return s

    def gen_sub(a, b):
        S = {ident}
        fr = [ident]
        gens = [a, b, inv(a), inv(b)]
        while fr:
            x = fr.pop()
            for g in gens:
                y = mul(x, g)
                if y not in S:
                    S.add(y)
                    fr.append(y)
        return S

    valid = []
    for a in elems:
        for b in elems:
            if mul(mul(a, b), a) == mul(mul(b, a), b):
                valid.append((a, b))

    odd = [p for p in elems if sgn(p) == -1]
    gen_free = sum(1 for a in odd for b in odd if len(gen_sub(a, b)) == 120)
    gen_braid = sum(1 for (a, b) in valid if sgn(a) == -1 and sgn(b) == -1
                    and len(gen_sub(a, b)) == 120)
    same_sign = sum(1 for (a, b) in valid if sgn(a) == sgn(b))
    return dict(total=len(valid), surj=0, same_sign=same_sign,
                odd_free=len(odd) ** 2, gen_free=gen_free,
                odd_braid=sum(1 for (a, b) in valid if sgn(a) == -1
                              and sgn(b) == -1),
                gen_braid=gen_braid)


# ---- drawing ----------------------------------------------------------------
BG = "#0a0a0d"
BRASS = "#c9a227"
COPPER = "#e0a850"
PALE = "#f2d27a"
ROSE = "#d98a6a"
DIM = "#2c3e50"
DARK = "#1a2430"
INK = "#e8e0cc"
SUB = "#9a8f78"


def glow_poly(pts, color, width=2.0, closed=True):
    tag = "polygon" if closed else "polyline"
    body = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    g = []
    for w, op in ((width * 5, 0.06), (width * 2.5, 0.15), (width * 1.2, 0.45),
                  (width, 0.9)):
        g.append(f"<{tag} points='{body}' stroke='{color}' "
                 f"stroke-width='{w:.2f}' opacity='{op}' fill='none' "
                 f"stroke-linejoin='round' stroke-linecap='round'/>")
    return "\n".join(g)


def glow_pts(points, color, width=2.0):
    pts = " ".join(f"{x:.1f},{y:.1f}" for x, y in points)
    g = []
    for w, op in ((width * 5, 0.06), (width * 2.5, 0.15), (width * 1.2, 0.45),
                  (width, 0.9)):
        g.append(f"<polyline points='{pts}' stroke='{color}' "
                 f"stroke-width='{w:.2f}' opacity='{op}' fill='none' "
                 f"stroke-linejoin='round' stroke-linecap='round'/>")
    return "\n".join(g)


def pentagon(cx, cy, r, rot=-90):
    return [(cx + r * math.cos(math.radians(rot + 72 * i)),
             cy + r * math.sin(math.radians(rot + 72 * i))) for i in range(5)]


def room_A5(cx, cy, r):
    """A5 as pentagon + pentagram."""
    pent = pentagon(cx, cy, r)
    star = [pent[0], pent[2], pent[4], pent[1], pent[3], pent[0]]
    s = [glow_poly(pent, BRASS, 2.2, closed=True), glow_pts(star, PALE, 1.6)]
    for (x, y) in pent:
        s.append(f"<circle cx='{x:.1f}' cy='{y:.1f}' r='4' fill='{BRASS}'/>")
    return "\n".join(s)


def room_S4(cx, cy, r):
    """S4 as a square + both diagonals (the point-stabilizer room)."""
    pts = [(cx - r, cy - r), (cx + r, cy - r), (cx + r, cy + r), (cx - r, cy + r)]
    s = [glow_poly(pts, COPPER, 2.2, closed=True)]
    s.append(glow_pts([pts[0], pts[2]], COPPER, 1.3))
    s.append(glow_pts([pts[1], pts[3]], COPPER, 1.3))
    for (x, y) in pts:
        s.append(f"<circle cx='{x:.1f}' cy='{y:.1f}' r='4' fill='{COPPER}'/>")
    return "\n".join(s)


def build_svg(stats):
    W, H = 1500, 920
    cx = W / 2
    parts = [f"<svg xmlns='http://www.w3.org/2000/svg' width='{W}' height='{H}' "
             f"viewBox='0 0 {W} {H}'>"]
    parts.append(f"<rect width='{W}' height='{H}' fill='{BG}'/>")

    parts.append(f"<text x='{cx}' y='66' text-anchor='middle' fill='{INK}' "
                 f"font-family='serif' font-size='34' letter-spacing='2'>"
                 f"the braid is the door, not the sign</text>")
    parts.append(f"<text x='{cx}' y='98' text-anchor='middle' fill='{SUB}' "
                 f"font-family='serif' font-size='15'>the trefoil never fills "
                 f"S&#8325; &#160;|&#160; the sign is locked, the relation is "
                 f"the door</text>")

    # S5 house (dark — not in the aperture)
    hx0, hx1 = cx - 340, cx + 340
    hy0, hy1 = 170, 560
    parts.append(f"<text x='{cx}' y='150' text-anchor='middle' fill='{INK}' "
                 f"font-family='serif' font-size='22'>S&#8325; &#160;|120|&#160; "
                 f"dark</text>")
    parts.append(glow_poly([(hx0, hy0), (hx1, hy0), (hx1, hy1), (hx0, hy1)],
                           DARK, width=1.8, closed=True))
    # two maximal rooms inside
    cy = (hy0 + hy1) / 2 - 30
    parts.append(room_A5(cx - 160, cy, 88))
    parts.append(room_S4(cx + 160, cy, 74))
    parts.append(f"<text x='{cx-160}' y='{cy+128}' text-anchor='middle' "
                 f"fill='{BRASS}' font-family='serif' font-size='15'>A&#8325; "
                 f"|60| &#160; both even</text>")
    parts.append(f"<text x='{cx+160}' y='{cy+128}' text-anchor='middle' "
                 f"fill='{COPPER}' font-family='serif' font-size='15'>S&#8324; "
                 f"|24| &#160; both odd</text>")

    # the two generators entering, sign-locked, bound by the braid tie
    yb = 780
    xl, xr = cx - 160, cx + 160
    ytop = hy1
    # strands (a braid: they cross once)
    parts.append(glow_pts([(xl, ytop), (xr, (ytop + yb) / 2), (xl, yb)], COPPER, 2.4))
    parts.append(glow_pts([(xr, ytop), (xl, (ytop + yb) / 2), (xr, yb)], ROSE, 2.4))
    # sign badges — locked equal
    for (x, y, lab, col) in ((xl, ytop + 40, "σ₁", ROSE),
                             (xr, ytop + 40, "σ₂", COPPER)):
        parts.append(f"<circle cx='{x}' cy='{y}' r='17' fill='none' "
                     f"stroke='{col}' stroke-width='1.6'/>")
        parts.append(f"<text x='{x}' y='{y+5}' text-anchor='middle' "
                     f"fill='{col}' font-family='serif' font-size='13'>{lab}</text>")
    # the braid relation at the crossing, with a dark backdrop
    relcy = (ytop + yb) / 2 - 6
    parts.append(f"<rect x='{cx-170}' y='{relcy-24}' width='340' height='32' "
                 f"fill='{BG}' opacity='0.85'/>")
    parts.append(f"<text x='{cx}' y='{relcy}' text-anchor='middle' "
                 f"fill='{PALE}' font-family='serif' font-size='19'>"
                 f"σ₁σ₂σ₁ = σ₂σ₁σ₂"
                 f"</text>")
    parts.append(f"<text x='{cx}' y='{yb + 22}' text-anchor='middle' "
                 f"fill='{SUB}' font-family='serif' font-size='14'>the two "
                 f"generators carry the SAME sign &#160;|&#160; the braid tie "
                 f"pins them to a maximal room</text>")

    # the tally — the door is the relation
    ty = 860
    parts.append(f"<text x='{cx}' y='{ty}' text-anchor='middle' "
                 f"fill='{COPPER}' font-family='serif' font-size='15'>"
                 f"two odd generators fill S&#8325;: "
                 f"{stats['gen_free']} / {stats['odd_free']} free &#160;|&#160; "
                 f"{stats['gen_braid']} / {stats['odd_braid']} braided</text>")
    parts.append(f"<text x='{cx}' y='{ty + 26}' text-anchor='middle' "
                 f"fill='#6f6656' font-family='serif' font-size='12'>"
                 f"the sign lock alone lets the house light; the braid word "
                 f"closes it</text>")
    parts.append("</svg>")
    return "\n".join(parts)


if __name__ == "__main__":
    stats = compute()
    print("homs B3->S5:", stats["total"], "  surjections:", stats["surj"],
          "  same-sign:", stats["same_sign"])
    print("odd pairs free fill S5:", stats["gen_free"], "/", stats["odd_free"])
    print("odd pairs braided fill S5:", stats["gen_braid"], "/",
          stats["odd_braid"])
    svg = build_svg(stats)
    with open("assets/s5_door.svg", "w") as f:
        f.write(svg)
    cairosvg.svg2png(url="assets/s5_door.svg", write_to="assets/s5_door.png",
                     output_width=1600)
    print("wrote assets/s5_door.svg and assets/s5_door.png")
