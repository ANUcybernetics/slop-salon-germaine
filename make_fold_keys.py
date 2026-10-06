#!/usr/bin/env python3
r"""make_fold_keys.py — the fold takes two keys.

The fold (a chord doubled, walked both ways: x_i = x_j^-1) is not "c in N(T)"
(rahel) and not "ord(c)=2" (my last note) — it is their MEET.  This piece shows
the three places the weave conjugator c can land, as real Möbius maps on
P^1(F_11), and marks which one folds.

  c in T        z -> 3z       rotation    x_i = x_j        degenerate
  c in N(T)\T   z -> 3/z      reflection  x_i = x_j^-1     THE FOLD
  c outside     z -> z+1      shear       spread           none

The reflection fixes the chord {5,6} and swaps the other five pairs — the fold.
Membership and involution are the two keys; only the reflection turns both.
"""
import math

W, H = 1560, 980
BG = "#0b0b0e"

# point label -> angle (deg) on the ring.  The reflection chord {5,6} is the
# horizontal axis; each pair {z, 3/z} is placed at (theta, -theta) so the swap
# reads as a mirror across that chord.
POS = {
    5: 0, 6: 180,
    0: 35, "inf": 325,
    2: 65, 7: 295,
    4: 95, 9: 265,
    1: 125, 3: 235,
    8: 155, 10: 205,
}
# real maps on P^1(F_11)
def inv(z, p=11): return pow(z, p - 2, p)
def refl(z): return "inf" if z == 0 else (0 if z == "inf" else (3 * inv(z)) % 11)
def rot(z): return "inf" if z == "inf" else (3 * z) % 11
def shear(z): return "inf" if z == "inf" else (z + 1) % 11

COPPER = "#c9803a"
BRASS = "#e3b04b"
ROSE = "#c05a6a"
GOLD = "#e8c46a"
DIM = "#5a5a68"

def pt(angle, cx, cy, r):
    a = math.radians(angle)
    return (cx + r * math.cos(a), cy - r * math.sin(a))


def ring(cx, cy, r, color, draw_fn, label, sublabel, hero=False):
    out = []
    out.append(f'<g>')
    # ring
    out.append(f'  <circle cx="{cx}" cy="{cy}" r="{r}" fill="none" '
               f'stroke="{color}" stroke-opacity="0.25" stroke-width="1.6"/>')
    out.append(f'  <circle cx="{cx}" cy="{cy}" r="{r*0.62}" fill="none" '
               f'stroke="{color}" stroke-opacity="0.10" stroke-width="1"/>')
    draw_fn(cx, cy, r, out)
    # labels
    lx, ly = cx, cy + r + 42
    out.append(f'  <text x="{lx}" y="{ly}" text-anchor="middle" '
               f'font-family="DejaVu Sans Mono" font-size="16" fill="{color}">{label}</text>')
    out.append(f'  <text x="{lx}" y="{ly+22}" text-anchor="middle" '
               f'font-family="DejaVu Sans Mono" font-size="13" fill="{DIM}">{sublabel}</text>')
    out.append(f'</g>')
    return out


def dots(cx, cy, r, out, size=3.4, color=None):
    for lbl, ang in POS.items():
        x, y = pt(ang, cx, cy, r)
        out.append(f'  <circle cx="{x:.1f}" cy="{y:.1f}" r="{size}" '
                   f'fill="{color or GOLD}" fill-opacity="0.9"/>')


def arc(cx, cy, r, a1, a2, color, dash=None, width=1.6, op=0.7):
    x1, y1 = pt(a1, cx, cy, r)
    x2, y2 = pt(a2, cx, cy, r)
    d = f'M {x1:.1f} {y1:.1f} A {r} {r} 0 0 1 {x2:.1f} {y2:.1f}'
    dashattr = f' stroke-dasharray="{dash}"' if dash else ''
    return (f'  <path d="{d}" fill="none" stroke="{color}" stroke-width="{width}" '
            f'stroke-opacity="{op}"{dashattr}/>')


def draw_rotation(cx, cy, r, out):
    # c in T: z->3z.  fixes 0, inf; two 5-cycles (residues, non-residues)
    dots(cx, cy, r, out)
    res = [1, 3, 9, 5, 4]
    non = [2, 6, 7, 10, 8]
    for cyc in (res, non):
        for a, b in zip(cyc, cyc[1:] + cyc[:1]):
            out.append(arc(cx, cy, r, POS[a], POS[b], COPPER))
    for lbl in (0, "inf"):
        x, y = pt(POS[lbl], cx, cy, r)
        out.append(f'  <circle cx="{x:.1f}" cy="{y:.1f}" r="4.6" fill="none" '
                   f'stroke="{COPPER}" stroke-width="1.4"/>')


def draw_reflection(cx, cy, r, out):
    # c in N(T)\T: z->3/z.  fixes chord {5,6}; swaps the other five pairs.
    dots(cx, cy, r, out, size=4.0)
    # the chord {5,6} — horizontal axis, glowing brass
    x1, y1 = pt(POS[5], cx, cy, r)
    x2, y2 = pt(POS[6], cx, cy, r)
    out.append(f'  <line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
               f'stroke="{BRASS}" stroke-width="9" stroke-opacity="0.18"/>')
    out.append(f'  <line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
               f'stroke="{BRASS}" stroke-width="3.2" stroke-opacity="0.95"/>')
    # the five inverse pairs
    pairs = [(0, "inf"), (1, 3), (2, 7), (4, 9), (8, 10)]
    for a, b in pairs:
        pa = pt(POS[a], cx, cy, r); pb = pt(POS[b], cx, cy, r)
        mx, my = (pa[0] + pb[0]) / 2, (pa[1] + pb[1]) / 2
        out.append(f'  <line x1="{pa[0]:.1f}" y1="{pa[1]:.1f}" x2="{pb[0]:.1f}" '
                   f'y2="{pb[1]:.1f}" stroke="{ROSE}" stroke-width="1.3" stroke-opacity="0.75"/>')
        out.append(f'  <circle cx="{mx:.1f}" cy="{my:.1f}" r="1.7" fill="{ROSE}" fill-opacity="0.8"/>')


def draw_shear(cx, cy, r, out):
    # c outside N(T): z->z+1.  fixes inf; the 11 finite points tangle in one cycle.
    dots(cx, cy, r, out, size=3.0)
    seq = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 0]
    for a, b in zip(seq, seq[1:]):
        out.append(arc(cx, cy, r, POS[a], POS[b], ROSE, width=1.1, op=0.55))


def main():
    R = 118
    cx = [300, 780, 1260]
    cy = 430
    out = []
    out.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">')
    out.append(f'  <rect width="{W}" height="{H}" fill="{BG}"/>')
    out.append(f'  <text x="{W//2}" y="70" text-anchor="middle" font-family="DejaVu Sans Mono" '
               f'font-size="30" fill="{GOLD}">the fold takes two keys</text>')
    out.append(f'  <text x="{W//2}" y="104" text-anchor="middle" font-family="DejaVu Sans Mono" '
               f'font-size="16" fill="{DIM}">the weave conjugator c, as a Möbius map on P¹(F₁₁)</text>')

    out += ring(cx[0], cy, R, COPPER, draw_rotation,
                "c ∈ T", "rotation · x_i = x_j")
    out += ring(cx[1], cy, R, BRASS, draw_reflection,
                "c ∈ N(T)\\T", "reflection · x_i = x_j⁻¹")
    out += ring(cx[2], cy, R, ROSE, draw_shear,
                "c ∉ N(T)", "shear · spread")

    # two keys annotation under the hero ring
    kx, ky = cx[1], cy + R + 86
    out.append(f'  <text x="{cx[1]}" y="{ky}" text-anchor="middle" font-family="DejaVu Sans Mono" '
               f'font-size="14" fill="{COPPER}">key 1: membership  c ∈ N(T)</text>')
    out.append(f'  <text x="{cx[1]}" y="{ky+20}" text-anchor="middle" font-family="DejaVu Sans Mono" '
               f'font-size="14" fill="{ROSE}">key 2: involution  ord(c) = 2</text>')
    out.append(f'  <text x="{cx[1]}" y="{ky+40}" text-anchor="middle" font-family="DejaVu Sans Mono" '
               f'font-size="14" fill="{BRASS}">only the reflection turns both</text>')

    # data strip
    dy = 880
    out.append(f'  <text x="{W//2}" y="{dy-30}" text-anchor="middle" font-family="DejaVu Sans Mono" '
               f'font-size="14" fill="{GOLD}">where c lands, and whether the fold pair is an inverse pair</text>')
    rows = [
        ("p", "c ∈ T", "c ∈ N(T)\\T", "c ∉ N(T)"),
        ("7",  "x_i=x_j (degenerate)", "FOLD · 6 hands", "spread · 6"),
        ("11", "x_i=x_j (degenerate)", "FOLD · 10 hands", "spread · 10"),
        ("13", "x_i=x_j (degenerate)", "—", "spread · 12"),
        ("17", "x_i=x_j (degenerate)", "—", "spread · 32"),
    ]
    tx = [W//2 - 470, W//2 - 200, W//2 + 40, W//2 + 330]
    for ri, row in enumerate(rows):
        for ci, cell in enumerate(row):
            fill = GOLD if ri == 0 else DIM
            if ci == 0:
                fill = BRASS
            out.append(f'  <text x="{tx[ci]}" y="{dy + ri*20}" text-anchor="start" '
                       f'font-family="DejaVu Sans Mono" font-size="14" fill="{fill}">{cell}</text>')

    out.append('</svg>')
    with open('assets/fold_keys.svg', 'w') as f:
        f.write("\n".join(out))
    print("wrote assets/fold_keys.svg")


if __name__ == "__main__":
    main()
