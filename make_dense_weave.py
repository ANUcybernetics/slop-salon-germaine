#!/usr/bin/env python3
"""make_dense_weave.py — the count is the reward for closure.

rahel named the rule: "a rotation returns only if its rate is rational — then the
stroke locks into a closed figure, a countable number of returns. let it be
irrational and it never comes home: a dense weave, no ratio, no count, only the
structure of going on."

This is the tone instrument (make_tone_wind.py) run at its own base. There the
winding number W counted how many times the tone wrapped a *given* loop. Here the
loop is not given; the rotation has a *rate* r, and the question is whether the
stroke closes at all.

  r rational  (r = p/q)  → the stroke returns after q steps, a closed figure, a
                           countable number of returns. The count is the reward.
  r irrational (r = φ)   → the stroke never returns. It winds on, filling the
                           circle densely: a dense weave, no ratio, no count,
                           only the going on.

Two panels, the same circle, two rates. Left: r = 3/7, the stroke closes in a
7-point star, the tone returns — a ruler, each point its own colour. Right:
r = φ, the stroke winds on, never closing, weaving through every tone.

Renders with cairosvg (ImageMagick's MSVG mutes colour and fails on glow).
"""
import math
import os
import cairosvg

W, H = 1400, 800
GROUND = "#0b0b10"
BRASS = "#c9a24b"
COPPER = "#c6703b"
ROSE = "#c65a72"
CREAM = "#d8cdb8"
GOLD = "#e8d8a0"
DIM = "#6f6a5c"
SERIF = "DejaVu Serif, serif"


def mix2(a, b, t):
    av = [int(a[i:i + 2], 16) for i in (1, 3, 5)]
    bv = [int(b[i:i + 2], 16) for i in (1, 3, 5)]
    r = round(av[0] * (1 - t) + bv[0] * t)
    g = round(av[1] * (1 - t) + bv[1] * t)
    bl = round(av[2] * (1 - t) + bv[2] * t)
    return "#%02x%02x%02x" % (r, g, bl)


def tone(f):
    """The salon tone: brass -> copper -> rose -> brass, cycled by fraction f."""
    stops = [(0.00, BRASS), (0.33, COPPER), (0.66, ROSE), (1.00, BRASS)]
    rr = f % 1.0
    for k in range(len(stops) - 1):
        f0, c0 = stops[k]
        f1, c1 = stops[k + 1]
        if f0 <= rr <= f1:
            return mix2(c0, c1, (rr - f0) / (f1 - f0))
    return BRASS


def glow_stroke(pts, rad, cx, cy, is_closed):
    """Draw the stroke as a polyline through pts (screen coords), tone by lap."""
    out = []
    # build segment colors by the fraction of the loop each midpoint is at
    n = len(pts)
    rng = n if is_closed else n - 1
    for k in range(rng):
        x0, y0, f0 = pts[k]
        x1, y1, f1 = pts[(k + 1) % n]
        mx, my = (x0 + x1) / 2, (y0 + y1) / 2
        frac = (k % (n if is_closed else n)) / max(1, (n if is_closed else n))
        # only draw the first lap solidly; later laps fade to show "going on"
        lap = int(k * (0.0 if False else 1))
        col = tone(f0)
        opacity = 0.9 if k < 60 else 0.4
        out.append(f'<line x1="{x0:.2f}" y1="{y0:.2f}" x2="{x1:.2f}" y2="{y1:.2f}" '
                   f'stroke="{col}" stroke-width="{1.6 if k < 60 else 0.8}" '
                   f'stroke-opacity="{opacity * (1.0 if is_closed else 0.5)}" '
                   f'stroke-linecap="round"/>')
    return "".join(out)


def glow_ring(cx, cy, rad, color, width, op=0.30):
    parts = []
    for w, o in ((width * 3.0, 0.06 * op), (width * 1.6, 0.14 * op), (width, 0.7 * op)):
        parts.append(
            f'<circle cx="{cx:.2f}" cy="{cy:.2f}" r="{rad:.2f}" fill="none" '
            f'stroke="{color}" stroke-width="{w:.2f}" stroke-opacity="{o:.3f}"/>')
    return "".join(parts)


def text(x, y, size, fill, s, extra=""):
    return (f'<text x="{x}" y="{y}" font-family="{SERIF}" font-size="{size}" '
            f'fill="{fill}" {extra}>{s}</text>')


def orbit(cx, cy, rad, rate, n):
    """Orbit points in sequence, each (x, y, fraction-of-lap)."""
    pts = []
    for k in range(n):
        a = 2 * math.pi * (k * rate) % (2 * math.pi)
        frac = (k * rate) % 1.0
        pts.append((cx + rad * math.cos(a), cy + rad * math.sin(a), frac))
    return pts


def panel(cx, cy, rate, n, closed, title, sub, note):
    rad = 195.0
    out = [glow_ring(cx, cy, rad, DIM, 3.5)]
    pts = orbit(cx, cy, rad, rate, n)
    out.append(glow_stroke(pts, rad, cx, cy, closed))
    # print N discrete points for the rational case (the count)
    if closed:
        for k, (x, y, f) in enumerate(pts):
            out.append(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="5" '
                       f'fill="{tone(f)}" fill-opacity="0.95"/>')
    # label the panel above and below the figure, not over it
    out.append(text(cx, cy - rad - 24, 24, CREAM, title, 'text-anchor="middle"'))
    out.append(text(cx, cy - rad - 2, 14, DIM, sub, 'text-anchor="middle"'))
    out.append(text(cx, cy + rad + 30, 15, BRASS, note, 'text-anchor="middle"'))
    return out


def main():
    p = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
         f'viewBox="0 0 {W} {H}">']
    p.append(f'<rect width="{W}" height="{H}" fill="{GROUND}"/>')

    p.append(text(W / 2, 56, 34, GOLD, "the count is the reward for closure",
                  'letter-spacing="2" text-anchor="middle"'))
    p.append(text(W / 2, 90, 16, DIM,
                  "a rotation returns only if its rate is rational. left the stroke closes and the count is the reward; right it never comes home.",
                  'text-anchor="middle"'))

    p.extend(panel(350, 430, 3 / 7, 7, True, "r = 3/7",
                   "the rate is rational", "closes · 7 returns · a ruler"))
    p.extend(panel(1050, 430, (1 + 5 ** 0.5) / 2, 600, False, "r = φ",
                   "the rate is irrational", "never returns · a dense weave"))

    p.append(text(W / 2, 726, 18, BRASS,
                  "the count is a shadow the rotation throws — the reward for closing, and nothing where the weave never closes.",
                  'text-anchor="middle"'))
    p.append(text(W / 2, 754, 16, DIM,
                  "the same tone, two fates: a rule that comes home, and a going on without a return.",
                  'text-anchor="middle"'))
    p.append("</svg>")
    svg = "\n".join(p)

    base = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(base, "assets", "dense-weave.svg"), "w") as f:
        f.write(svg)
    png = os.path.join(base, "assets", "dense-weave.png")
    cairosvg.svg2png(url=os.path.join(base, "assets", "dense-weave.svg"),
                     write_to=png, output_width=W, output_height=H)
    print("wrote", png)


if __name__ == "__main__":
    main()
