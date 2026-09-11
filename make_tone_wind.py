#!/usr/bin/env python3
"""make_tone_wind.py — rahel's tone eye, pushed into its own blind spot.

rahel named a third eye: "tone, a colour that says where on the one stroke you
are."  On a *closed* loop that claim has a seam.  A tone around a loop has a
winding number W — how many times the colour cycles as the strand closes.

  W = 1: the tone is an honest ruler.  Every point has its own colour; the
         on-stroke position is readable.
  W = 2: the tone wraps twice.  Every colour now appears twice, at genuinely
         different places on the same strand.  "You are at copper" is no longer
         one answer.

Which is precisely the shape of the thing we started with: the tone is a count,
and the count was never the blind eye's antidote — it is the blind eye in
colour.  Both panels are the identical figure-eight knot (a genuine 4_1, four
crossings) so the only difference is the winding, i.e. the count.

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
                hide.add(int(c) % K + d)
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


def palette(f, winding):
    """Tone cycling around the loop `winding` times.  winding=1 is rahel's ruler;
    winding=2 doubles every colour."""
    rr = (f * winding) % 1.0
    stops = [(0.00, BRASS), (0.33, COPPER), (0.66, ROSE), (1.00, BRASS)]
    for k in range(len(stops) - 1):
        f0, c0 = stops[k]
        f1, c1 = stops[k + 1]
        if f0 <= rr <= f1:
            t = (rr - f0) / (f1 - f0)
            return mix2(c0, c1, t)
    return BRASS


def tone_subpaths(P, hide, cx, cy, scale, winding, nb=72, markers=()):
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

    # give back the subpaths, and the centroids of the requested marker bins
    subpaths = [(palette((b + 0.5) / nb, winding), pts)
                for b, pts in sorted(bins.items()) for pts in pts]
    cents = {}
    for mbin in markers:
        if mbin in bins:
            allpts = [pt for grp in bins[mbin] for pt in grp]
            mx = sum(p[0] for p in allpts) / len(allpts)
            my = sum(p[1] for p in allpts) / len(allpts)
            cents[mbin] = (mx, my)
    return subpaths, cents


def knot(cx, cy, scale, winding, markers=()):
    P = [fig8_point(2 * math.pi * i / K) for i in range(K)]
    hide = hidden_window(P, K)
    subpaths, cents = tone_subpaths(P, hide, cx, cy, scale, winding, markers=markers)
    out = []
    for (c, pts) in subpaths:
        if len(pts) >= 2:
            out.append(glow(path_of(pts), c))
    return out, cents


def main():
    p = []
    p.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
             f'viewBox="0 0 {W} {H}">')
    p.append(f'<rect width="{W}" height="{H}" fill="{GROUND}"/>')

    p.append(text(80, 52, 30, "#cfc4ae",
                  "the tone is a ruler, until it winds twice",
                  'letter-spacing="2"'))
    p.append(text(80, 84, 16, "#6f6a5c",
                  "the same figure-eight knot, the same strand — only the winding changes"))

    def winding_panel(cx, label, winding, markers=()):
        # returns the list of svg strings
        out = [text(cx - 60, 130, 20, BRASS if winding == 1 else COPPER, label)]
        subs, cents = knot(cx, 360, 62, winding, markers=markers)
        out.extend(subs)
        # markers: two small hollow rings on a chosen colour
        for (mx, my, mcol) in markers:
            out.append(f'<circle cx="{mx:.0f}" cy="{my:.0f}" r="9" fill="none" '
                       f'stroke="{mcol}" stroke-width="2.2" opacity="0.9"/>')
            out.append(f'<circle cx="{mx:.0f}" cy="{my:.0f}" r="2.4" '
                       f'fill="{mcol}" opacity="0.95"/>')
        out.append(text(cx - 60, 545, 18, "#d8cdb8",
                        "winding = 1" if winding == 1 else "winding = 2"))
        return out

    # left: winding 1 — honest ruler, no marker.
    p.extend(winding_panel(330, "one pass", 1))

    # right: winding 2 — two of every colour.  mark the two roses.
    rose_bins = [29, 64]  # the two instances the tone maps to rose when winding=2
    markers = []
    subs, cents = knot(950, 360, 62, 2, markers=rose_bins)
    for mb in rose_bins:
        if mb in cents:
            markers.append((cents[mb][0], cents[mb][1], ROSE))
    p.extend(winding_panel(950, "two passes", 2, markers=markers))

    p.append(text(640, 585, 16, "#9c927b",
                  "rose, in two places — the tone no longer knows "
                  "where on the strand you are",
                  'text-anchor="middle"'))

    p.append("</svg>")
    svg = "\n".join(p)
    base = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(base, "assets", "tone-wind.svg"), "w") as f:
        f.write(svg)
    png = os.path.join(base, "assets", "tone-wind.png")
    cairosvg.svg2png(url=os.path.join(base, "assets", "tone-wind.svg"),
                     write_to=png, output_width=W, output_height=H)
    print("wrote", png)
    print("markers:", markers)


if __name__ == "__main__":
    main()
