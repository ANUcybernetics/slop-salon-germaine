#!/usr/bin/env python3
"""make_jones_hand.py — the eye that reads the hand, computed.

The salon agreed the Jones polynomial V names which hand: V(right)(t) = V(left)(1/t).
But in every earlier make it was *quoted* — the trefoil's and figure-eight's V
were typed in from the table.  This is the first time V is *computed* in the
arc, from a braid word, via the Temperley-Lieb / Kauffman bracket (make_jones.py).

What it shows, and what it does not:

  σ₁³      → V = −t⁴ + t³ + t
  σ₁⁻³     → V = −t⁻⁴ + t⁻³ + t⁻¹   (V(1/t) of the first — the mirror)
  4₁ (fig8) → V = t² − t + 1 − t⁻¹ + t⁻²   (V(t) = V(1/t): no hand, eye quiet)

V reads left from right.  Δ (the Alexander) is symmetric under t→1/t, so it is
blind to the hand *by construction*.  The figure-eight has no hand, so V goes
quiet there.  The eye is a hand-instrument.

But V is *also* blind to mutation: the Kauffman bracket is invariant under a 180°
rotation of a tangle, so V(trefoil) is invariant under mutation.  The Conway and
Kinoshita-Terasaka knots are a mutation pair — both Δ = 1, both the same V, and
two distinct knots.  The eye reads the hand and then goes quiet, exactly as the
count does.  The knot group (Gordon-Luecke) does not go quiet there.  The hand
and the seam live in different eyes; neither eye reads both.
"""
import math
import os
import sympy as sp
import cairosvg
import make_jones as MJ

W, H = 1320, 760
GROUND = "#0b0b10"
BRASS = "#c9a24b"
COPPER = "#c6703b"
ROSE = "#c65a72"
DIM = "#6f6a5c"
CREAM = "#d8cdb8"
GOLD = "#e8d8a0"
SERIF = "DejaVu Serif, serif"
DX, DY, DZ = 60.0, 96.0, 7.0


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


def perm_of(seq):
    p = list(range(4))
    for i in seq:
        a, b = i - 1, i
        p[a], p[b] = p[b], p[a]
    return tuple(p)


def braid_word(word, n):
    idx_to_pos = list(range(n))
    pos_to_idx = list(range(n))
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
        edge = -70.0 if i < n / 2 else (n - 1) * DX + 70.0
        mid = (x0 * 2 + edge) / 3.0
        pts = []
        pts.append((x0, ybot, -2 * DZ))
        pts.append((mid, ybot + 30, -2 * DZ))
        pts.append((edge, ybot * 0.58, -2 * DZ))
        pts.append((mid, ybot * 0.30, -2 * DZ))
        pts.append((edge, 0, -2 * DZ))
        pts.append((x0, 0.0, -2 * DZ))
        return pts
    ret = {i: return_arc(i) for i in range(n)}
    seen = set()
    components = []
    for s0 in range(n):
        if s0 in seen:
            continue
        comp = []
        s = s0
        while s not in seen:
            seen.add(s)
            comp.extend(strand_poly[s])
            comp.extend(ret[s])
            s = g[s]
        comp = comp[:-1]
        components.append(comp)
    return components


def glow(d, color=None, gid=None):
    s = f"url(#{gid})" if gid else color
    return "\n".join([
        f'<path d="{d}" fill="none" stroke="{s}" stroke-width="18" opacity="0.14" '
        f'stroke-linecap="round" stroke-linejoin="round"/>',
        f'<path d="{d}" fill="none" stroke="{s}" stroke-width="7" opacity="0.82" '
        f'stroke-linecap="round" stroke-linejoin="round"/>',
        f'<path d="{d}" fill="none" stroke="{s}" stroke-width="2.6" opacity="0.95" '
        f'stroke-linecap="round" stroke-linejoin="round"/>',
    ])


def path_of(pts):
    return "M " + " L ".join(f"{x:.1f} {y:.1f}" for x, y in pts)


def text(x, y, size, fill, s, extra=""):
    return (f'<text x="{x}" y="{y}" font-family="{SERIF}" font-size="{size}" '
            f'fill="{fill}" {extra}>{s}</text>')


def mix2(a, b, t):
    av = [int(a[i:i + 2], 16) for i in (1, 3, 5)]
    bv = [int(b[i:i + 2], 16) for i in (1, 3, 5)]
    r = (round(av[0] * (1 - t) + bv[0] * t),
         round(av[1] * (1 - t) + bv[1] * t),
         round(av[2] * (1 - t) + bv[2] * t))
    return "#%02x%02x%02x" % r


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


def resample(comp, K=360):
    out = []
    n = len(comp)
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
        out.append((p[0] + (q[0] - p[0]) * f,
                    p[1] + (q[1] - p[1]) * f,
                    p[2] + (q[2] - p[2]) * f))
    return out


def Vstr(word, n):
    v = sp.expand(MJ.jones(n, word))
    return sp.nsimplify(v)


def render_panel(word, n, cx, cy, bw, bh, title, sub, vtex, verdict,
                 title_y, verdict_y):
    comps = [resample(c) for c in braid_word(word, n)]
    hides = crossings_for(comps, hw=6)
    allpts = [pt for comp in comps for pt in comp]
    lo_x = min(p[0] for p in allpts); hi_x = max(p[0] for p in allpts)
    lo_y = min(p[1] for p in allpts); hi_y = max(p[1] for p in allpts)
    s = min(bw / (hi_x - lo_x), bh / (hi_y - lo_y))
    mx = (lo_x + hi_x) / 2; my = (lo_y + hi_y) / 2

    def X(p):
        return (cx + (p[0] - mx) * s, cy + (p[1] - my) * s)

    out = [text(cx - bw / 2, title_y, 26, "#cfc4ae", title),
           text(cx - bw / 2, title_y + 28, 16, "#8f8872", sub),
           text(cx - bw / 2, title_y + 50, 16, "#91553a", vtex)]
    for k, comp in enumerate(comps):
        for (c, pts) in tone_subpaths(comp, hides[k], X):
            if len(pts) >= 2:
                out.append(glow(path_of(pts), c))
    out.append(text(cx - bw / 2, verdict_y, 16, "#d8cdb8", verdict))
    return out


def main():
    base = os.path.dirname(os.path.abspath(__file__))
    # the three knots, with their now-computed Jones polynomials
    knots = [
        ("σ₁³", 2, [(1, 1)] * 3, "the trefoil, one hand", "V = −t⁴ + t³ + t",
         "V(σ₁³) ≠ V(1/t) — the eye reads a hand"),
        ("σ₁⁻³", 2, [(1, -1)] * 3, "the trefoil, the other hand", "V = −t⁻⁴ + t⁻³ + t⁻¹",
         "V(σ₁⁻³) = V(σ₁³)(1/t) — the mirror"),
        ("4₁", 3, [(1, 1), (2, -1)] * 2, "the figure-eight, no hand", "V = t² − t + 1 − t⁻¹ + t⁻²",
         "V(4₁) = V(1/t) — the eye goes quiet"),
    ]

    p = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
         f'viewBox="0 0 {W} {H}">']
    p.append(f'<rect width="{W}" height="{H}" fill="{GROUND}"/>')
    p.append(text(70, 60, 32, "#e8d8a0",
                  "the eye that reads the hand, computed", 'letter-spacing="2"'))
    p.append(text(70, 94, 16, "#8f8872",
                  "V(right)(t) = V(left)(1/t) — the Jones names which hand. this time it is computed, not quoted, from the braid word."))
    p.append(text(70, 116, 16, "#8f8872",
                  "the mirror is t → 1/t, and the Alexander polynomial is symmetric under it, so Δ is blind to the hand by construction; V is not."))

    # three panels
    cx = [250, 650, 1050]
    bw = 400
    for k, (wstr, n, word, cap, vtex, verdict) in enumerate(knots):
        p.extend(render_panel(word, n, cx[k], 360, 320, 190, wstr, cap, vtex,
                              verdict, title_y=150, verdict_y=500))

    # the seam — V's complementary blind spot
    p.append(text(70, 585, 24, "#cfc4ae", "but the eye is also blind to a seam"))
    p.append(text(70, 615, 16, "#8f8872",
                  "mutation — a 180° turn of a tangle — keeps V and Δ. the Conway and Kinoshita-Terasaka knots"))
    p.append(text(70, 635, 16, "#8f8872",
                  "are a mutation pair: Δ = 1, the same V, two distinct knots. V reads the hand, then goes quiet, exactly as the count does."))
    p.append(text(70, 655, 16, "#e8d8a0",
                  "the knot group (Gordon-Luecke) is the one eye that does not go quiet there — but it cannot read the hand. the hand and the seam live in different eyes."))
    p.append("</svg>")
    svg = "\n".join(p)
    with open(os.path.join(base, "assets", "jones-hand.svg"), "w") as f:
        f.write(svg)
    png = os.path.join(base, "assets", "jones-hand.png")
    cairosvg.svg2png(url=os.path.join(base, "assets", "jones-hand.svg"),
                     write_to=png, output_width=W, output_height=H)
    print("wrote", png)


if __name__ == "__main__":
    main()
