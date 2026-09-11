#!/usr/bin/env python3
"""make_zero_blind.py — two 3-strand braid closures, both exponent sum 0.

mina named a second blind eye of the sum: a braid can read 0 and still close to
something that won't come apart. rahel named a third eye — "tone", a colour that
says where on the one stroke you are. This piece uses *tone* as the instrument
that makes the zero-blindness visible.

Left  (unlink):    the identity braid in B3, sigma = 0.  Closure: three loose
                   loops, three components.  The sum sees "nothing".
Right (4_1):       sigma_1 sigma_2^-1 sigma_1 sigma_2^-1, sum 0.  Closure: one
                   thread that will not come apart (the figure-eight knot).  A
                   single gradient stroke (brass -> copper -> rose) says the
                   tone eye: it's one thread, and no point on it knows its start.

Right panel is a genuine 4_1 diagram: a parametric figure-eight space curve,
projected to the plane with over/under taken from depth.  Verified 4 crossings.

Renders with cairosvg.
"""
import math
import os
import cairosvg

W, H = 1280, 640
GROUND = "#0b0b10"
BRASS = "#c9a24b"
COPPER = "#c6703b"
ROSE = "#c65a72"
SERIF = "DejaVu Serif, serif"
K = 1200  # knot samples


def fig8_point(t):
    x = (2 + math.cos(2 * t)) * math.cos(3 * t)
    y = (2 + math.cos(2 * t)) * math.sin(3 * t)
    z = math.sin(4 * t)
    return x, y, z


def seg_int(p1, p2, p3, p4):
    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    d1, d2 = cross(p3, p4, p1), cross(p3, p4, p2)
    d3, d4 = cross(p1, p2, p3), cross(p1, p2, p4)
    if ((d1 > 0 and d2 < 0) or (d1 < 0 and d2 > 0)) and \
       ((d3 > 0 and d4 < 0) or (d3 < 0 and d4 > 0)):
        det = (p2[0] - p1[0]) * (p4[1] - p3[1]) - (p2[1] - p1[1]) * (p4[0] - p3[0])
        if det == 0:
            return None
        return ((p3[0] - p1[0]) * (p4[1] - p3[1]) - (p3[1] - p1[1]) * (p4[0] - p3[0])) / det
    return None


def hidden_window(P, K, hw=9):
    """Return a set of indices to hide (under-strand gaps) from crossings."""
    hide = set()
    for i in range(K):
        for j in range(i + 1, K):
            if j == i + 1 or (i == 0 and j == K - 1):
                continue
            t = seg_int(P[i][:2], P[(i + 1) % K][:2], P[j][:2], P[(j + 1) % K][:2])
            if t is None:
                continue
            zi = P[i][2] * (1 - t) + P[(i + 1) % K][2] * t
            zj = P[j][2] * (1 - t) + P[(j + 1) % K][2] * t
            if zi < zj:
                c = i + t
            else:
                c = j + t
            for d in range(-hw, hw + 1):
                hide.add(int(c) % K + d)  # wrapped via % later
    # dedupe / wrap
    return {x % K for x in hide}


def glow(d, color=None, gid=None):
    s = f"url(#{gid})" if gid else color
    return "\n".join([
        f'<path d="{d}" fill="none" stroke="{s}" stroke-width="18" opacity="0.15" '
        f'stroke-linecap="round" stroke-linejoin="round"/>',
        f'<path d="{d}" fill="none" stroke="{s}" stroke-width="7" opacity="0.82" '
        f'stroke-linecap="round" stroke-linejoin="round"/>',
        f'<path d="{d}" fill="none" stroke="{s}" stroke-width="2.6" opacity="0.95" '
        f'stroke-linecap="round" stroke-linejoin="round"/>',
    ])


def path_of(points):
    return "M " + " L ".join(f"{x:.1f} {y:.1f}" for x, y in points)


def text(x, y, size, fill, s, extra=""):
    return (f'<text x="{x}" y="{y}" font-family="{SERIF}" font-size="{size}" '
            f'fill="{fill}" {extra}>{s}</text>')


def mix2(a, b, t):
    av = [int(a[i:i + 2], 16) for i in (1, 3, 5)]
    bv = [int(b[i:i + 2], 16) for i in (1, 3, 5)]
    r = round(av[0] * (1 - t) + bv[0] * t), round(av[1] * (1 - t) + bv[1] * t), round(
        av[2] * (1 - t) + bv[2] * t)
    return "#%02x%02x%02x" % r


def palette(f):
    """Periodic tone: brass -> copper -> rose -> brass around the one loop."""
    stops = [(0.00, BRASS), (0.33, COPPER), (0.66, ROSE), (1.00, BRASS)]
    for k in range(len(stops) - 1):
        f0, c0 = stops[k]
        f1, c1 = stops[k + 1]
        if f0 <= f <= f1:
            t = (f - f0) / (f1 - f0)
            return mix2(c0, c1, t)
    return BRASS


def tone_subpaths(P, hide, cx, cy, scale, nb=72):
    """Split into arclength-coloured bins; each bin drawn with its own colour."""
    xy = [(X * scale, Y * scale) for (X, Y, Z) in P]
    cum = [0.0]
    for i in range(1, len(xy)):
        dx, dy = xy[i][0] - xy[i - 1][0], xy[i][1] - xy[i - 1][1]
        cum.append(cum[-1] + math.hypot(dx, dy))
    dx, dy = xy[0][0] - xy[-1][0], xy[0][1] - xy[-1][1]
    total = cum[-1] + math.hypot(dx, dy)
    frac = [c / total for c in cum]

    bins = {}
    cur, curbin = [], None
    for i in range(len(xy)):
        if i in hide:
            if cur:
                bins.setdefault(curbin, []).append(cur)
                cur = []
            continue
        b = min(nb - 1, int(frac[i] * nb))
        if b != curbin:
            if cur:
                bins.setdefault(curbin, []).append(cur)
            cur, curbin = [], b
        cur.append((cx + xy[i][0], cy + xy[i][1]))
    if cur:
        bins.setdefault(curbin, []).append(cur)
    return [(palette((b + 0.5) / nb), pts) for b, pts in sorted(bins.items())
            for pts in pts]


def main():
    # ---- left panel: three unknots, separate ----
    circle_x = [170, 340, 510]
    circle_y, circle_r = 255, 72

    # ---- right panel: figure-eight 4_1 ----
    cx, cy, scale = 955, 295, 62
    P = [fig8_point(2 * math.pi * i / K) for i in range(K)]
    hide = hidden_window(P, K)            # under-strand indices
    colored = tone_subpaths(P, hide, cx, cy, scale)

    p = []
    p.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
             f'viewBox="0 0 {W} {H}">')
    p.append(f'<rect width="{W}" height="{H}" fill="{GROUND}"/>')

    p.append(text(150, 50, 30, "#cfc4ae", "the sum reads zero", 'letter-spacing="2"'))
    p.append(text(150, 82, 16, "#6f6a5c",
                  "two 3-braids, both σ = 0 — the closures read different"))

    # left
    p.append(text(150, 116, 20, BRASS, "the identity braid"))
    for k, c in enumerate([BRASS, COPPER, ROSE]):
        cxL = circle_x[k]
        d = (f"M {cxL - circle_r} {circle_y} a {circle_r} {circle_r} 0 1 0 "
             f"{2 * circle_r} 0 a {circle_r} {circle_r} 0 1 0 {-2 * circle_r} 0")
        p.append(glow(d, c))
    p.append(text(150, 405, 18, "#d8cdb8", "σ° in B₃ · Σ = 0"))
    p.append(text(150, 430, 15, "#8f876f", "three loose loops — it falls apart"))

    # right
    p.append(text(cx - 3 * scale, 116, 20, COPPER, "σ₁σ₂⁻¹σ₁σ₂⁻¹"))
    for (c, pts) in colored:
        if len(pts) >= 2:
            p.append(glow(path_of(pts), c))
    p.append(text(cx - 3 * scale, 500, 18, "#d8cdb8", "σ₁σ₂⁻¹σ₁σ₂⁻¹ · Σ = 0"))
    p.append(text(cx - 3 * scale, 525, 15, "#8f876f",
                  "one thread — it will not come apart"))

    p.append("</svg>")
    svg = "\n".join(p)
    base = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(base, "assets", "braids-zero.svg"), "w") as f:
        f.write(svg)
    png = os.path.join(base, "assets", "braids-zero.png")
    cairosvg.svg2png(url=os.path.join(base, "assets", "braids-zero.svg"),
                     write_to=png, output_width=W, output_height=H)
    print("wrote", png)


if __name__ == "__main__":
    main()
