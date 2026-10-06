#!/usr/bin/env python3
r"""make_door_room.py — the door is the split torus; the elliptic room is blind.

The whole two-lock thread lives on the SPLIT class (order m=(p-1)/2): the fold
needs a chord, and only split elements have a chord (two fixed points on P^1(F_p)).
The seam is the fold's shadow (seam = Conway_reach - KT_reach = Conway's spread).

New data: the ELLIPTIC class (order e=(p+1)/2) has NO chord (axis = ()), and its
reach NEVER differs between the words — seam = 0 at every prime and every elliptic
class.  The elliptic room has hands at some primes (p=13: 28, p=17: 18, p=23: 24)
but distributes them evenly: Conway = KT always.

split seam:  p=7 +6, p=11 0, p=13 +12, p=17 0, p=19 0, p=23 0
ell  seam:    0 everywhere
"""
import math
import cairosvg

W, H = 1560, 1080
BG = "#0b0b0e"
GOLD = "#e8c46a"
BRASS = "#d4a017"
BRASS_EDGE = "#f0c75e"
COPPER = "#c07a5a"
COPPER_EDGE = "#e0a37f"
ROSE = "#c05a6a"
DIM = "#5a5a68"
TXT = "#d8c9a8"

# p -> (split seam, elliptic seam); split reach (Conway, KT) and elliptic reach
DATA = [
    dict(p=7,  m=3,  s_seam=6,  e_seam=0, s_reach=(12, 6), e_reach=(0, 0)),
    dict(p=11, m=5,  s_seam=0,  e_seam=0, s_reach=(10, 10), e_reach=(0, 0)),
    dict(p=13, m=6,  s_seam=12, e_seam=0, s_reach=(12, 0), e_reach=(28, 28)),
    dict(p=17, m=8,  s_seam=0,  e_seam=0, s_reach=(32, 32), e_reach=(18, 18)),
    dict(p=19, m=9,  s_seam=0,  e_seam=0, s_reach=(36, 36), e_reach=(0, 0)),
    dict(p=23, m=11, s_seam=0,  e_seam=0, s_reach=(66, 66), e_reach=(24, 24)),
]


def pt(angle, cx, cy, r):
    a = math.radians(angle)
    return (cx + r * math.cos(a), cy - r * math.sin(a))


def ring(cx, cy, r, out, chord=None, label="", sub="", color=BRASS, fold=False):
    out.append(f'  <circle cx="{cx}" cy="{cy}" r="{r}" fill="none" '
               f'stroke="{color}" stroke-opacity="0.30" stroke-width="1.6"/>')
    out.append(f'  <circle cx="{cx}" cy="{cy}" r="{r*0.60}" fill="none" '
               f'stroke="{color}" stroke-opacity="0.12" stroke-width="1"/>')
    # the p+1 points on the circle
    for k in range(12):
        x, y = pt(-90 + k * 30, cx, cy, r)
        out.append(f'  <circle cx="{x:.1f}" cy="{y:.1f}" r="2.6" '
                   f'fill="{GOLD}" fill-opacity="0.75"/>')
    if chord:
        x1, y1 = pt(chord[0], cx, cy, r)
        x2, y2 = pt(chord[1], cx, cy, r)
        if fold:
            out.append(f'  <line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
                       f'stroke="{color}" stroke-width="10" stroke-opacity="0.20" stroke-linecap="round"/>')
            out.append(f'  <line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
                       f'stroke="{BRASS_EDGE}" stroke-width="3" stroke-linecap="round"/>')
            mx, my = (x1 + x2) / 2, (y1 + y2) / 2
            out.append(f'  <circle cx="{mx:.1f}" cy="{my:.1f}" r="4" fill="{BRASS_EDGE}"/>')
        else:
            out.append(f'  <line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
                       f'stroke="{color}" stroke-width="2" stroke-opacity="0.85"/>')
    else:
        # no chord — a hollow room.  Draw a faint vanishing point marker.
        out.append(f'  <circle cx="{cx}" cy="{cy}" r="2.6" fill="{ROSE}" fill-opacity="0.6"/>')
    out.append(f'  <text x="{cx}" y="{cy + r + 34}" text-anchor="middle" '
               f'font-family="DejaVu Sans Mono" font-size="17" fill="{color}">{label}</text>')
    out.append(f'  <text x="{cx}" y="{cy + r + 54}" text-anchor="middle" '
               f'font-family="DejaVu Sans Mono" font-size="13" fill="{DIM}">{sub}</text>')


def main():
    out = []
    out.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">')
    out.append(f'  <rect width="{W}" height="{H}" fill="{BG}"/>')
    out.append(f'  <text x="{W//2}" y="66" text-anchor="middle" font-family="DejaVu Sans Mono" '
               f'font-size="30" fill="{GOLD}">the door is the split torus</text>')
    out.append(f'  <text x="{W//2}" y="98" text-anchor="middle" font-family="DejaVu Sans Mono" '
               f'font-size="16" fill="{DIM}">the elliptic room is blind to both locks — no chord, no fold, no seam</text>')

    # ---- the two rooms, side by side ----
    ring(300, 350, 120, out, chord=(150, 330), label="split room",
         sub="has a chord → the fold", color=BRASS, fold=True)
    ring(1260, 350, 120, out, chord=None, label="elliptic room",
         sub="no chord → blind", color=ROSE)

    # caption under the rooms
    out.append(f'  <text x="300" y="560" text-anchor="middle" font-family="DejaVu Sans Mono" '
               f'font-size="13" fill="{COPPER}">the split torus carries the axis</text>')
    out.append(f'  <text x="300" y="580" text-anchor="middle" font-family="DejaVu Sans Mono" '
               f'font-size="13" fill="{DIM}">fold = chord doubled (c ∈ N(T)\\T)</text>')
    out.append(f'  <text x="1260" y="560" text-anchor="middle" font-family="DejaVu Sans Mono" '
               f'font-size="13" fill="{ROSE}">elliptic elements fix no point of P¹(F_p)</text>')
    out.append(f'  <text x="1260" y="580" text-anchor="middle" font-family="DejaVu Sans Mono" '
               f'font-size="13" fill="{DIM}">so the seam stays 0 — the words agree</text>')

    # ---- the seam chart ----
    chart_top = 660
    chart_bot = 960
    cy = (chart_top + chart_bot) / 2
    axis = chart_bot
    out.append(f'  <text x="{W//2}" y="{chart_top - 24}" text-anchor="middle" font-family="DejaVu Sans Mono" '
               f'font-size="17" fill="{TXT}">the seam — Conway&#39;s reach minus KT&#39;s — by prime</text>')
    out.append(f'  <text x="{W//2}" y="{chart_top - 4}" text-anchor="middle" font-family="DejaVu Sans Mono" '
               f'font-size="13" fill="{DIM}">split room (brass) opens at m=3,6 · elliptic room (rose) is flat 0</text>')

    x0 = 200
    step = (W - 2 * x0) / (len(DATA) - 1)
    ymax = 12.0
    scale = (chart_bot - chart_top - 20) / ymax
    # gridlines
    for v in (0, 6, 12):
        yy = axis - v * scale
        out.append(f'  <line x1="{x0-40}" y1="{yy:.1f}" x2="{W-x0+40}" y2="{yy:.1f}" '
                   f'stroke="{DIM}" stroke-opacity="0.25" stroke-width="1"/>')
        out.append(f'  <text x="{x0-52}" y="{yy+4:.1f}" text-anchor="end" '
                   f'font-family="DejaVu Sans Mono" font-size="12" fill="{DIM}">{v}</text>')
    out.append(f'  <line x1="{x0-40}" y1="{axis}" x2="{W-x0+40}" y2="{axis}" '
               f'stroke="{TXT}" stroke-opacity="0.5" stroke-width="1.4"/>')

    barw = 30
    for i, d in enumerate(DATA):
        x = x0 + i * step
        # split bar (centered at x-21)
        sv = d['s_seam']
        sxc = x - barw / 2 - 6
        yy = axis - sv * scale
        out.append(f'  <rect x="{sxc-barw/2:.1f}" y="{yy:.1f}" width="{barw}" height="{max(sv*scale,0.001):.1f}" '
                   f'fill="{BRASS}" fill-opacity="{0.9 if sv else 0.0}" stroke="{BRASS_EDGE}" '
                   f'stroke-width="{1.2 if sv else 0}"/>')
        if sv:
            out.append(f'  <text x="{sxc:.1f}" y="{yy-11:.1f}" text-anchor="middle" '
                       f'font-family="DejaVu Sans Mono" font-size="15" fill="{BRASS_EDGE}">{sv}</text>')
        # elliptic bar (centered at x+21) — always 0; mark with a rose bead on the axis
        exc = x + barw / 2 + 6
        ev = d['e_seam']
        if ev:
            yy = axis - ev * scale
            out.append(f'  <rect x="{exc-barw/2:.1f}" y="{yy:.1f}" width="{barw}" height="{max(ev*scale,0.001):.1f}" '
                       f'fill="{ROSE}" fill-opacity="0.9"/>')
        else:
            out.append(f'  <circle cx="{exc:.1f}" cy="{axis-5:.1f}" r="4.2" '
                       f'fill="none" stroke="{ROSE}" stroke-width="1.6"/>')
        # p label
        out.append(f'  <text x="{x:.1f}" y="{axis + 26}" text-anchor="middle" '
                   f'font-family="DejaVu Sans Mono" font-size="15" fill="{TXT}">{d["p"]}</text>')
        out.append(f'  <text x="{x:.1f}" y="{axis + 46}" text-anchor="middle" '
                   f'font-family="DejaVu Sans Mono" font-size="12" fill="{DIM}">m={d["m"]}</text>')

    # legend
    lx, ly = 200, chart_bot + 76
    out.append(f'  <rect x="{lx}" y="{ly-10}" width="18" height="12" fill="{BRASS}" stroke="{BRASS_EDGE}" stroke-width="1"/>')
    out.append(f'  <text x="{lx+26}" y="{ly}" font-family="DejaVu Sans Mono" font-size="13" fill="{TXT}">split seam</text>')
    out.append(f'  <rect x="{lx+180}" y="{ly-10}" width="18" height="12" fill="{ROSE}"/>')
    out.append(f'  <text x="{lx+206}" y="{ly}" font-family="DejaVu Sans Mono" font-size="13" fill="{TXT}">elliptic seam</text>')
    out.append(f'  <text x="{lx+380}" y="{ly}" font-family="DejaVu Sans Mono" font-size="13" fill="{DIM}">'
               f'elliptic reach always ties: 0,0 / 28,28 / 18,18 / 24,24</text>')

    out.append('</svg>')
    with open('assets/door_room.svg', 'w') as f:
        f.write("\n".join(out))
    cairosvg.svg2png(bytestring="\n".join(out).encode(), write_to="assets/door_room.png", output_width=1560)
    print("wrote assets/door_room.svg / .png")


if __name__ == "__main__":
    main()
