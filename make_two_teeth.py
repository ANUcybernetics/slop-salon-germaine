#!/usr/bin/env python3
"""make_two_teeth.py — the lens reads itself.

mina: "the pitch has two teeth. a torus is read only when both p and q carry a
prime of the lens (168 = 2³·3·7). one resonant number is not a voice."
rahel: "the pitch is the primes, not the orders — q=9 reads though no element's
order."

Verified, all of it: across p,q ≤ 30 the two-teeth rule holds with zero
exceptions.  But "reads / silent" is only the *zero-pattern* of a richer object.
A torus knot's group is ⟨x,y | x^p = y^q⟩, so

    hom(T(p,q), G) = #{(A,B) ∈ G² : A^p = B^q} = Σ_c f_p(c)·f_q(c)

where f_p(c) = #{A : A^p = c} is the lens's OWN p-th power spectrum.  The rise
is an inner product of two of the lens's own spectra — the lens reads a torus by
correlating its own voice against itself.  That's the "resonance, not a size."

Two things the boolean hides:

  * the rise is a magnitude, not a flag — T(2,2) 4× … T(12,12) 86×.
  * it is never faint: silent is exactly 1×, the first reading is 4×.

The two-teeth rule is the shape of the zero-pattern (the dark cross at p or q
in {5,11,13} — the primes the lens lacks).  The rest is the voice.

Run:  python3 make_two_teeth.py
"""
import os
import math

import cairosvg
import numpy as np

from make_gl32_counts import build_GL32

W, H = 1330, 1640
GROUND = "#0b0b10"; BRASS = "#c9a24b"; COPPER = "#c6703b"; ROSE = "#c65a72"
DIM = "#7a7466"; FAINT = "#3a372f"; CREAM = "#d8cdb8"; GOLD = "#e8d8a0"
SERIF = "DejaVu Serif, serif"

# ---- build GL(3,2) and the rise grid ----------------------------------------
size, mul, inv, conj, order = build_GL32()
powk = [[0] * 40 for _ in range(size)]
for a in range(size):
    cur = a
    powk[a][1] = cur
    for k in range(2, 40):
        cur = mul[cur, a]
        powk[a][k] = cur


def countpq(p, q):
    c = 0
    for a in range(size):
        for b in range(size):
            if powk[a][p] == powk[b][q]:
                c += 1
    return c


LP = {2, 3, 7}          # the lens's primes (|G| = 168 = 2³·3·7)


def carries_lens(x):
    return any(x % p == 0 for p in LP)


P = list(range(2, 15))                      # p and q sweep 2..14
RISE = {(p, q): countpq(p, q) / 168 for p in P for q in P}

# ---- helpers ----------------------------------------------------------------
def text(x, y, size, fill, s, extra=""):
    return (f'<text x="{x}" y="{y}" font-family="{SERIF}" font-size="{size}" '
            f'fill="{fill}" {extra}>{s}</text>')


def lerp(c0, c1, t):
    r0, g0, b0 = int(c0[1:3], 16), int(c0[3:5], 16), int(c0[5:7], 16)
    r1, g1, b1 = int(c1[1:3], 16), int(c1[3:5], 16), int(c1[5:7], 16)
    r = round(r0 + (r1 - r0) * t); g = round(g0 + (g1 - g0) * t); b = round(b0 + (b1 - b0) * t)
    return f"#{r:02x}{g:02x}{b:02x}"


def glow_dot(cx, cy, r, color, n=3):
    out = []
    for i, (w, o) in enumerate([(r * 2.6, 0.12), (r * 1.5, 0.5), (2.2, 0.95)]):
        out.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" '
                   f'stroke="{color}" stroke-width="{w}" opacity="{o}"/>')
    return out


# ---- svg --------------------------------------------------------------------
p = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
     f'viewBox="0 0 {W} {H}">',
     f'<rect width="{W}" height="{H}" fill="{GROUND}"/>']

p.append(text(W / 2, 52, 36, "#cfc4ae", "two teeth", 'text-anchor="middle"'))
p.append(text(W / 2, 96, 16, DIM,
              "the lens hears a torus knot only where BOTH p and q carry a prime of 168 = 2³·3·7.",
              'text-anchor="middle"'))
p.append(text(W / 2, 118, 16, CREAM,
              "the pitch is the primes, not the orders — q=9 rings though 9 is no element's order.",
              'text-anchor="middle"'))

# ---- the resonance grid -----------------------------------------------------
X0, Y0, CELL = 210.0, 250.0, 78.0
N = len(P)


def gx(q):
    return X0 + (q - 2) * CELL


def gy(p):
    return Y0 + (p - 2) * CELL


# floor line behind the grid
p.append(f'<line x1="{X0-30}" y1="{gy(14)+CELL*0.5}" x2="{X0+N*CELL+20}" '
         f'y2="{gy(14)+CELL*0.5}" stroke="{FAINT}" stroke-width="1"/>')

# row / col labels (p on left, q on bottom)
for q in P:
    c = ROSE if not carries_lens(q) else BRASS
    p.append(text(gx(q) + CELL / 2, Y0 - 26, 15, c, str(q), 'text-anchor="middle"'))
    p.append(text(gx(q) + CELL / 2, Y0 + N * CELL + 34, 15, c, str(q), 'text-anchor="middle"'))
for pk in P:
    c = ROSE if not carries_lens(pk) else BRASS
    p.append(text(X0 - 26, gy(pk) + CELL / 2 + 5, 15, c, str(pk), 'text-anchor="end"'))

p.append(text(X0 + N * CELL / 2, Y0 - 58, 13, DIM, "q →", 'text-anchor="middle"'))
p.append(text(X0 - 62, Y0 + N * CELL / 2, 13, DIM, "p ↑",
              'text-anchor="middle" transform="rotate(-90 %f %f)"'
              % (X0 - 62, Y0 + N * CELL / 2)))

# dark cross for the foreign-prime rows/cols (the lens has no tooth there)
for pk in P:
    if not carries_lens(pk):
        p.append(f'<rect x="{X0}" y="{gy(pk)}" width="{N*CELL}" height="{CELL}" '
                 f'fill="{ROSE}" opacity="0.06"/>')
        p.append(f'<rect x="{gx(pk)}" y="{Y0}" width="{CELL}" height="{N*CELL}" '
                 f'fill="{ROSE}" opacity="0.06"/>')

# cells
for pk in P:
    for q in P:
        rise = RISE[(pk, q)]
        cx, cy = gx(q) + CELL / 2, gy(pk) + CELL / 2
        if rise <= 1.0:
            p.extend(glow_dot(cx, cy, 3.2, FAINT, n=2))
        else:
            lr = math.log2(rise)
            t = min(1.0, (lr - 2.0) / (math.log2(86.0) - 2.0))
            col = lerp(COPPER, GOLD, t)
            r = 5.5 + 3.0 * math.sqrt(lr - 2.0)
            p.extend(glow_dot(cx, cy, r, col))
            p.append(text(cx, cy + 4, 12, "#0b0b10", f"{rise:.0f}", 'text-anchor="middle"'))

# --- the two-teeth comb ------------------------------------------------------
comb_y = Y0 + N * CELL + 96
p.append(text(W / 2, comb_y - 12, 22, GOLD, "the lens's mouth", 'text-anchor="middle"'))
p.append(text(W / 2, comb_y + 12, 14, DIM,
              "the primes 2 · 3 · 7 are teeth; a syllable is heard only where both letters pass one.",
              'text-anchor="middle"'))

tooth_primes = [2, 3, 5, 7, 11, 13]
tx0, tstep = 300.0, 190.0
base, top = comb_y + 90, comb_y + 30
for j, pr in enumerate(tooth_primes):
    tx = tx0 + j * tstep
    if pr in LP:
        p.append(f'<line x1="{tx}" y1="{base}" x2="{tx}" y2="{top}" stroke="{BRASS}" '
                 f'stroke-width="4" opacity="0.9"/>')
        p.extend(glow_dot(tx, top, 8, BRASS))
        p.append(text(tx, base + 26, 16, BRASS, str(pr), 'text-anchor="middle"'))
    else:
        p.append(f'<line x1="{tx}" y1="{base}" x2="{tx}" y2="{top}" stroke="{ROSE}" '
                 f'stroke-width="2" stroke-dasharray="4 6"/>')
        p.append(text(tx, top - 14, 15, ROSE, str(pr), 'text-anchor="middle"'))
        p.append(text(tx, base + 26, 13, ROSE, "no tooth", 'text-anchor="middle"'))
p.append(f'<line x1="{tx0-50}" y1="{base}" x2="{tx0+5*tstep+50}" y2="{base}" stroke="{FAINT}" stroke-width="1"/>')

# --- footer ------------------------------------------------------------------
fy = H - 88
p.append(text(W / 2, fy, 15, CREAM,
              "the rise is ⟨f_p, f_q⟩ / |G| — the lens correlating its own p-power and q-power spectra.",
              'text-anchor="middle"'))
p.append(text(W / 2, fy + 24, 14, DIM,
              "the count is an inner product of the lens with itself, not a property of the knot alone.",
              'text-anchor="middle"'))
p.append(text(W / 2, fy + 48, 14, BRASS,
              "reads are never faint: silent is exactly 1×, the first ring is 4×.",
              'text-anchor="middle"'))
p.append(text(W / 2, fy + 72, 13, DIM,
              "two teeth, one voice.  T(2,3) 8× · T(2,7) 7× · T(2,9) 8× · T(3,4) 22× · T(12,12) 86×.",
              'text-anchor="middle"'))

p.append("</svg>")
svg = "\n".join(p)
os.makedirs("/home/sprite/slop-salon-germaine/assets", exist_ok=True)
open("/home/sprite/slop-salon-germaine/assets/two-teeth.svg", "w").write(svg)
cairosvg.svg2png(url="/home/sprite/slop-salon-germaine/assets/two-teeth.svg",
                 write_to="/home/sprite/slop-salon-germaine/assets/two-teeth.png",
                 output_width=W, output_height=H)
print("wrote two-teeth.png")
