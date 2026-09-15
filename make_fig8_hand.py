#!/usr/bin/env python3
"""make_fig8_hand.py — the ear reports a hand where there is none.

The eye's chirality-sense is a *knot* instrument.  The Jones polynomial is
asymmetric under the mirror, t -> 1/t, so it names the hand — and for an
amphichiral knot it is *palindromic*, so it goes quiet.  The figure-eight is
amphichiral:  its mirror is a no-op.  The eye reads it and finds no hand.

The ear's chirality-sense is a *word* instrument.  It never goes quiet, because
a word always has a mirror, and a mirror word always sounds different.  The
figure-eight has two mirror words,

    w  = σ₁σ₂⁻¹σ₁σ₂⁻¹      and      w̄ = σ₁⁻¹σ₂σ₁⁻¹σ₂,

and they close to the SAME knot — the mirror is a no-op.  Yet the ear hears
two songs (A E⁻ A E⁻  and  A⁻ E A⁻ E).  For a chiral knot like the trefoil this
coincidence works out: the two mirror words ARE the two hands.  For the eight it
is a lie:  two songs, one knot, no hand to be lost.

The eye goes silent when there is no hand; the ear never does.
"""

import math
import os
import cairosvg

W, H = 1300, 1040
BG = "#0a0a0f"
GROUND = "#0b0b10"
BRASS = "#c9a24b"
COPPER = "#c6703b"
ROSE = "#c65a72"
DIM = "#7a7466"
FAINT = "#3a372f"
INK = "#d8cdb8"
GOLD = "#e8d8a0"
TEAL = "#6fb0b0"
SERIF = "DejaVu Serif, serif"
STAFF = "#33333f"

DX, DY, DZ = 60.0, 96.0, 7.0
XL, XR = 390.0, 910.0
YB = 320.0


# ---------------- braid-closure renderer (shared with the salon) -------------
def seg_int(p1, p2, p3, p4):
    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    d1, d2 = cross(p3, p4, p1), cross(p3, p4, p2)
    d3, d4 = cross(p1, p2, p3), cross(p1, p2, p4)
    if ((d1 > 0 and d2 < 0) or (d1 < 0 and d2 > 0)) and ((d3 > 0 and d4 < 0) or (d3 < 0 and d4 > 0)):
        det = (p2[0] - p1[0]) * (p4[1] - p3[1]) - (p2[1] - p1[1]) * (p4[0] - p3[0])
        if det == 0:
            return None
        return ((p3[0] - p1[0]) * (p4[1] - p3[1]) - (p3[1] - p1[1]) * (p4[0] - p3[0])) / det
    return None


def crossings_for(curves, hw=6):
    hides = [set() for _ in curves]
    for a in range(len(curves)):
        for b in range(a, len(curves)):
            Pa, Pb = curves[a], curves[b]
            ka, kb = len(Pa), len(Pb)
            for i in range(ka):
                jr = range(i + 1, ka) if a == b else range(kb)
                for j in jr:
                    if a == b and (j == i + 1 or (i == 0 and j == ka - 1)):
                        continue
                    p1, p2 = Pa[i][:2], Pa[(i + 1) % ka][:2]
                    p3, p4 = Pb[j][:2], Pb[(j + 1) % kb][:2]
                    tm = seg_int(p1, p2, p3, p4)
                    if tm is None:
                        continue
                    zp = Pa[i][2] * (1 - tm) + Pa[(i + 1) % ka][2] * tm
                    zq = Pb[j][2] * (1 - tm) + Pb[(j + 1) % kb][2] * tm
                    if zp < zq:
                        hides[b].update((j + d) % kb for d in range(-hw, hw + 1))
                    else:
                        hides[a].update((i + d) % ka for d in range(-hw, hw + 1))
    return hides


def braid_word(word, n):
    pos_to_idx = list(range(n))
    idx_to_pos = list(range(n))
    strand_poly = {s: [] for s in range(n)}
    y = 0.0
    for s in range(n):
        strand_poly[s].append((s * DX, y, 0.0))
    for (i, eps) in word:
        y += DY
        ia, ib = i - 1, i
        sa, sb = pos_to_idx[ia], pos_to_idx[ib]
        xa, xb = ia * DX, ib * DX
        za = DZ if eps > 0 else -DZ
        zb = -DZ if eps > 0 else DZ
        ym = y - DY * 0.5
        strand_poly[sa].append((xa, y - DY * 0.45, za))
        strand_poly[sa].append(((xa + xb) / 2, ym, za))
        strand_poly[sa].append((xb, y, za))
        strand_poly[sb].append((xb, y - DY * 0.45, zb))
        strand_poly[sb].append(((xa + xb) / 2, ym, zb))
        strand_poly[sb].append((xa, y, zb))
        pos_to_idx[ia], pos_to_idx[ib] = sb, sa
        idx_to_pos[sa] = ib
        idx_to_pos[sb] = ia
    ybot = y
    for s in range(n):
        strand_poly[s].append((idx_to_pos[s] * DX, ybot, 0.0))
    g = {s: idx_to_pos[s] for s in range(n)}

    def return_arc(i):
        x0 = i * DX
        go_left = x0 < (n - 1) * DX / 2.0 - 1e-9
        edge = -76.0 if go_left else (n - 1) * DX + 76.0
        return [(x0, ybot, -2 * DZ), (x0 + (edge - x0) * 0.55, ybot + 42, -2 * DZ),
                (edge, ybot * 0.66, -2 * DZ), (edge, ybot * 0.32, -2 * DZ),
                (x0 + (edge - x0) * 0.55, 38, -2 * DZ), (x0, 0.0, -2 * DZ)]

    ret = {i: return_arc(i) for i in range(n)}
    seen, comps = set(), []
    for s0 in range(n):
        if s0 in seen:
            continue
        comp, s = [], s0
        while s not in seen:
            seen.add(s)
            comp.extend(strand_poly[s])
            comp.extend(ret[s])
            s = g[s]
        comps.append(comp[:-1])
    return comps


def resample(comp, K=460):
    out, n = [], len(comp)
    cum = [0.0]
    for i in range(n):
        p, q = comp[i], comp[(i + 1) % n]
        cum.append(cum[-1] + math.hypot(q[0] - p[0], q[1] - p[1]))
    total = cum[-1]
    seg = 0
    for k in range(K):
        target = total * k / K
        while seg < n and cum[seg + 1] < target:
            seg += 1
        f = (target - cum[seg]) / (cum[seg + 1] - cum[seg]) if cum[seg + 1] != cum[seg] else 0.0
        p, q = comp[seg], comp[(seg + 1) % n]
        out.append((p[0] + (q[0] - p[0]) * f, p[1] + (q[1] - p[1]) * f, p[2] + (q[2] - p[2]) * f))
    return out


def mix2(a, b, tt):
    av = [int(a[i:i + 2], 16) for i in (1, 3, 5)]
    bv = [int(b[i:i + 2], 16) for i in (1, 3, 5)]
    return "#%02x%02x%02x" % (round(av[0] * (1 - tt) + bv[0] * tt),
                              round(av[1] * (1 - tt) + bv[1] * tt),
                              round(av[2] * (1 - tt) + bv[2] * tt))


def palette(f):
    rr = f % 1.0
    stops = [(0.00, BRASS), (0.33, COPPER), (0.66, ROSE), (1.00, BRASS)]
    for k in range(len(stops) - 1):
        f0, c0 = stops[k]
        f1, c1 = stops[k + 1]
        if f0 <= rr <= f1:
            return mix2(c0, c1, (rr - f0) / (f1 - f0))
    return BRASS


def tone_subpaths(comp, hide, X, nb=72):
    xy = [X(p) for p in comp]
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
        cur.append(xy[i])
    if cur:
        bins.setdefault(curbin, []).append(cur)
    return [(palette((b + 0.5) / nb), pts) for b, pts in sorted(bins.items()) for pts in pts]


def glow(d, c, wide=16):
    return "\n".join([
        f'<path d="{d}" fill="none" stroke="{c}" stroke-width="{wide}" opacity="0.12" stroke-linecap="round" stroke-linejoin="round"/>',
        f'<path d="{d}" fill="none" stroke="{c}" stroke-width="{wide * 0.4}" opacity="0.8" stroke-linecap="round" stroke-linejoin="round"/>',
        f'<path d="{d}" fill="none" stroke="{c}" stroke-width="2.4" opacity="0.95" stroke-linecap="round" stroke-linejoin="round"/>'])


def path_of(pts):
    return "M " + " L ".join(f"{x:.1f} {y:.1f}" for x, y in pts)


def text(x, y, size, fill, s, anchor="middle"):
    return (f'<text x="{x:.2f}" y="{y:.2f}" font-family="{SERIF}" font-size="{size}" '
            f'fill="{fill}" text-anchor="{anchor}">{s}</text>')


def render_braid(cx, cy, word, n, wordlabel, cap, kind):
    """Draw one braid closure.  wordlabel above (with the kind tag), cap below."""
    comps = [resample(c) for c in braid_word(word, n)]
    hides = crossings_for(comps)
    allpts = [pt for comp in comps for pt in comp]
    lo_x = min(p[0] for p in allpts)
    hi_x = max(p[0] for p in allpts)
    lo_y = min(p[1] for p in allpts)
    hi_y = max(p[1] for p in allpts)
    BW, BH = 300.0, 205.0
    s = min(BW / (hi_x - lo_x), BH / (hi_y - lo_y))
    mx = (lo_x + hi_x) / 2
    my = (lo_y + hi_y) / 2

    def X(p):
        return (cx + (p[0] - mx) * s, cy + (p[1] - my) * s)

    top_y = cy - (hi_y - my) * s
    bot_y = cy + (hi_y - my) * s
    out = [text(cx, top_y - 44, 15, DIM, kind),
           text(cx, top_y - 16, 25, INK, wordlabel)]
    for k, comp in enumerate(comps):
        for (c, pts) in tone_subpaths(comp, hides[k], X):
            if len(pts) >= 2:
                out.append(glow(path_of(pts), c))
    out.append(text(cx, bot_y + 24, 16, "#d8cdb8", cap))
    out.append(text(cx, bot_y + 47, 14, "#8f8872", "4 crossings · Δ = t² − 3t + 1"))
    return out


# ---------------- note discs / staves (the ear) ------------------------------
def note_disc(p, color, letter, glide=False, r=15):
    parts = []
    for rr, o in ((r * 3.0, 0.10), (r * 1.8, 0.26)):
        parts.append(f'<circle cx="{p[0]:.2f}" cy="{p[1]:.2f}" r="{rr:.2f}" '
                     f'fill="{color}" fill-opacity="{o}"/>')
    parts.append(f'<circle cx="{p[0]:.2f}" cy="{p[1]:.2f}" r="{r:.2f}" fill="{color}"/>')
    parts.append(f'<text x="{p[0]:.2f}" y="{p[1] + 6:.2f}" font-family="{SERIF}" '
                 f'font-size="18" fill="{BG}" text-anchor="middle">{letter}</text>')
    if glide:
        # a small descending arrow under the disc: the note glides down a fifth
        y0 = p[1] + r + 5
        parts.append(f'<line x1="{p[0] - 7:.2f}" y1="{y0:.2f}" x2="{p[0] + 7:.2f}" '
                     f'y2="{y0 + 9:.2f}" stroke="{color}" stroke-width="1.6" stroke-opacity="0.9"/>')
        parts.append(f'<path d="M {p[0] + 7:.2f} {y0 + 9:.2f} l -6 1.5 l 2 4 z" fill="{color}" fill-opacity="0.9"/>')
    return "".join(parts)


def staff(y, seq, label, cap):
    """seq: list of (letter, color, glide_bool).  Draws a line of note discs."""
    out = []
    out.append(f'<line x1="392" y1="{y:.2f}" x2="1092" y2="{y:.2f}" '
               f'stroke="{STAFF}" stroke-width="2" stroke-opacity="0.9"/>')
    spacing = 152
    x0 = 500
    for i, (letter, col, glide) in enumerate(seq):
        x = x0 + i * spacing
        py = y - 34 if letter.startswith("E") else y + 34
        out.append(note_disc((x, py), col, letter, glide=glide))
    out.append(text(88, y + 2, 22, INK, label, anchor="start"))
    out.append(text(88, y + 34, 14, DIM, cap, anchor="start"))
    return "".join(out)


# ---------------- build ------------------------------------------------------
svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">']
svg.append(f'<rect width="{W}" height="{H}" fill="{BG}"/>')
svg.append(text(W / 2, 56, 34, INK, "the ear reports a hand where there is none"))
svg.append(text(W / 2, 92, 18, DIM,
                "the figure-eight is its own mirror. the eye reads it and finds no hand — the ear reads the word and hears two."))

# the two mirror closures: the word and its mirror word, both the figure-eight
svg.extend(render_braid(XL, YB, [(1, 1), (2, -1), (1, 1), (2, -1)], 3,
                        "σ₁σ₂⁻¹σ₁σ₂⁻¹", "closes to the figure-eight", "the word"))

svg.extend(render_braid(XR, YB, [(1, -1), (2, 1), (1, -1), (2, 1)], 3,
                        "σ₁⁻¹σ₂σ₁⁻¹σ₂", "closes to the SAME figure-eight", "the mirror word"))

# the no-op: an equals between the two closures
svg.append(f'<line x1="{XL + 150}" y1="{YB}" x2="{XR - 150}" y2="{YB}" '
           f'stroke="{FAINT}" stroke-width="2" stroke-opacity="0.8"/>')
svg.append(text((XL + XR) / 2, YB - 10, 22, INK, "one knot", anchor="middle"))
svg.append(text((XL + XR) / 2, YB + 20, 14, DIM, "the mirror is a no-op — the same figure-eight", anchor="middle"))

# ---- the invariant shelf: the eye is silent --------------------------------
SH_Y = 560.0
svg.append(f'<line x1="{XL - 40}" y1="{SH_Y}" x2="{XR + 40}" y2="{SH_Y}" '
           f'stroke="{GOLD}" stroke-width="26" opacity="0.10" stroke-linecap="round"/>')
svg.append(f'<line x1="{XL - 40}" y1="{SH_Y}" x2="{XR + 40}" y2="{SH_Y}" '
           f'stroke="{GOLD}" stroke-width="9" opacity="0.55" stroke-linecap="round"/>')
svg.append(f'<line x1="{XL - 40}" y1="{SH_Y}" x2="{XR + 40}" y2="{SH_Y}" '
           f'stroke="{GOLD}" stroke-width="2.6" opacity="0.95" stroke-linecap="round"/>')
svg.append(text(W / 2, SH_Y - 60, 16, DIM, "the eye's chirality-sense — the Jones polynomial"))
svg.append(text(W / 2, SH_Y - 24, 28, "#f2e9c8", "V(4₁)  =  t⁻² − t⁻¹ + 1 − t + t²"))
svg.append(text(W / 2, SH_Y + 36, 17, INK, "palindromic — Δ(t) = Δ(1/t), V(t) = V(1/t)"))
svg.append(text(W / 2, SH_Y + 64, 16, DIM, "the mirror is a no-op, so the eye goes quiet. no hand to name."))

# ---- the ear: two songs -----------------------------------------------------
svg.append(text(W / 2, 664, 18, INK, "the ear's chirality-sense — the word"))
svg.append(text(W / 2, 692, 16, DIM, "a word always has a mirror, and the mirror word always sounds different."))

svg.append(staff(738, [("A", BRASS, False), ("E", COPPER, True), ("A", BRASS, False), ("E", COPPER, True)],
                 "the ear hears (word):      A   E⁻   A   E⁻",
                 "closes to the figure-eight"))
svg.append(staff(872, [("A", BRASS, True), ("E", COPPER, False), ("A", BRASS, True), ("E", COPPER, False)],
                 "the ear hears (mirror):    A⁻   E   A⁻   E",
                 "closes to the SAME figure-eight"))

# footer
svg.append(text(W / 2, 968, 17, INK,
                "two songs, one knot, no hand. the ear's mirror-sense is a word-instrument and never goes quiet."))
svg.append(text(W / 2, 1000, 14, DIM,
                "for the trefoil it works by accident — the two mirror words ARE the two hands. for the eight it is a lie."))

svg.append("</svg>")
svg_str = "".join(svg)

base = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(base, "assets", "fig8-hand.svg"), "w") as f:
    f.write(svg_str)
cairosvg.svg2png(bytestring=svg_str.encode(),
                 write_to=os.path.join(base, "assets", "fig8-hand.png"),
                 output_width=W, output_height=H)
print("wrote assets/fig8-hand.svg and assets/fig8-hand.png")
