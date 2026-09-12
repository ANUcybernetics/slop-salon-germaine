#!/usr/bin/env python3
"""make_projection_tower.py — the projection tower: count, permutation, word.

The salon's eye has climbed the braid and each level answered with a count.
The sum is blind (mina, rahel).  The closure is a map, not a number (my last
make): which end meets which.  But the map has its own counts — cycle type,
sign, components — and those are blind too: (12)(34) and (13)(24) share the
cycle type [2,2], so that count cannot tell them apart, though the pairings are
not the same.

So the tower: count at the top, permutation in the middle, word at the bottom.
Each level is a map; the level above is the shadow it throws; the shadow is
blind to the map.  The honest eye is not a better level — it is the refusal to
collapse one level into the next.

Two closed 4-braids rise in parallel:
  w_L = σ₁σ₁σ₃⁻¹σ₁⁻¹   perm (12)(34)  → the split unlink (falls apart)
  w_R = σ₂σ₁σ₃⁻¹σ₂⁻¹   perm (13)(24)  → a nonsplit lk-0 link (holds)
They differ at the word and at the pairing; they pour, both, into one identical
count block.  The count cannot tell which tower it came from.
"""
import math
import os
import cairosvg

W, H = 1280, 1400
GROUND = "#0b0b10"
BRASS = "#c9a24b"
COPPER = "#c6703b"
ROSE = "#c65a72"
DIM = "#7a7466"
FAINT = "#3a372f"
SERIF = "DejaVu Serif, serif"
DX, DY, DZ = 60.0, 96.0, 7.0

XL, XR = 340.0, 950.0          # column centres
YC, YP, YB = 200.0, 520.0, 960.0   # counts, pairings, braid centres


# --------------------------------------------------------------------------
# coin-flip helpers (shared)
# --------------------------------------------------------------------------
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


def crossings_for(curves, hw=8):
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
                    t = seg_int(p1, p2, p3, p4)
                    if t is None:
                        continue
                    z_p = Pa[i][2] * (1 - t) + Pa[(i + 1) % ka][2] * t
                    z_q = Pb[j][2] * (1 - t) + Pb[(j + 1) % kb][2] * t
                    if z_p < z_q:
                        hides[b].update((j + d) % kb for d in range(-hw, hw + 1))
                    else:
                        hides[a].update((i + d) % ka for d in range(-hw, hw + 1))
    return hides


# --------------------------------------------------------------------------
# braid closure geometry (same as make_perm_map)
# --------------------------------------------------------------------------
def perm_of(seq):
    p = list(range(4))
    for i in seq:
        a, b = i - 1, i
        p[a], p[b] = p[b], p[a]
    return tuple(p)


def braid_word(word):
    n = 4
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
    perm = perm_of([i for i, _ in word])

    def return_arc(i):
        x0 = i * DX
        edge = -70.0 if i < n / 2 else (n - 1) * DX + 70.0
        mid = (x0 * 2 + edge) / 3.0
        return [(x0, ybot, -2 * DZ), (mid, ybot + 30, -2 * DZ),
                (edge, ybot * 0.58, -2 * DZ), (mid, ybot * 0.30, -2 * DZ),
                (edge, -30 + 30, -2 * DZ), (x0, 0.0, -2 * DZ)]
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
    return comps, perm, g, ybot


def resample(comp, K=360):
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


def mix2(a, b, t):
    av = [int(a[i:i + 2], 16) for i in (1, 3, 5)]
    bv = [int(b[i:i + 2], 16) for i in (1, 3, 5)]
    return "#%02x%02x%02x" % (round(av[0] * (1 - t) + bv[0] * t),
                              round(av[1] * (1 - t) + bv[1] * t),
                              round(av[2] * (1 - t) + bv[2] * t))


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
    bins, cur, curbin = {}, [], None
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


# --------------------------------------------------------------------------
# primitives
# --------------------------------------------------------------------------
def glow(d, color=None, gid=None, wide=18):
    s = f"url(#{gid})" if gid else color
    return "\n".join([
        f'<path d="{d}" fill="none" stroke="{s}" stroke-width="{wide}" opacity="0.12" '
        f'stroke-linecap="round" stroke-linejoin="round"/>',
        f'<path d="{d}" fill="none" stroke="{s}" stroke-width="{wide * 0.4}" opacity="0.82" '
        f'stroke-linecap="round" stroke-linejoin="round"/>',
        f'<path d="{d}" fill="none" stroke="{s}" stroke-width="2.6" opacity="0.95" '
        f'stroke-linecap="round" stroke-linejoin="round"/>',
    ])


def path_of(pts):
    return "M " + " L ".join(f"{x:.1f} {y:.1f}" for x, y in pts)


def text(x, y, size, fill, s, extra=""):
    return (f'<text x="{x}" y="{y}" font-family="{SERIF}" font-size="{size}" '
            f'fill="{fill}" {extra}>{s}</text>')


def brace(x0, y0, x1, y1):
    """A quadratic bezier path string between two points."""
    mx, my = (x0 + x1) / 2, (y0 + y1) / 2
    return f"M {x0:.1f} {y0:.1f} Q {mx:.1f} {my:.1f} {x1:.1f} {y1:.1f}"


# --------------------------------------------------------------------------
# the three levels
# --------------------------------------------------------------------------
def render_counts(cx, cy):
    """The counts block — ONE identical block, shared by both towers."""
    label = "i · the counts"
    row = "Σ = 0   ·   crossings 4   ·   parts 2   ·   linking 0   ·   cycle [2,2]"
    out = [text(cx, cy - 40, 19, DIM, label, 'text-anchor="middle"'),
           text(cx, cy + 12, 23, "#d8cdb8", row, 'text-anchor="middle"'),
           text(cx, cy + 46, 15, DIM, "identical — blind to which tower it came from",
                'text-anchor="middle"')]
    return out


def render_perm(cx, cy, pairs, cap):
    """The pairing map: four ends on a circle, arcs between paired ends."""
    r = 78.0
    pos = {1: (cx, cy - r), 2: (cx + r, cy), 3: (cx, cy + r), 4: (cx - r, cy)}
    tones = [BRASS, COPPER]
    out = []
    # faint circle guide
    out.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" '
               f'stroke="{FAINT}" stroke-width="1"/>')
    for k, (a, b) in enumerate(pairs):
        pa, pb = pos[a], pos[b]
        d = brace(pa[0], pa[1], pb[0], pb[1])
        out.append(glow(d, tones[k % 2], wide=10))
    for i, (a, b) in pos.items():
        out.append(f'<circle cx="{a}" cy="{b}" r="5" fill="#cfc4ae"/>')
        out.append(text(a, b - 12, 15, "#cfc4ae", str(i), 'text-anchor="middle"'))
    out.append(text(cx, cy + r + 30, 16, "#d8cdb8", cap, 'text-anchor="middle"'))
    return out


def render_braid(cx, cy, title, caption, seq):
    raw = braid_word(seq)
    comps = [resample(c) for c in raw[0]]
    hides = crossings_for(comps, hw=6)
    allpts = [pt for comp in comps for pt in comp]
    lo_x = min(p[0] for p in allpts); hi_x = max(p[0] for p in allpts)
    lo_y = min(p[1] for p in allpts); hi_y = max(p[1] for p in allpts)
    BW, BH = 300.0, 205.0
    s = min(BW / (hi_x - lo_x), BH / (hi_y - lo_y))
    mx = (lo_x + hi_x) / 2; my = (lo_y + hi_y) / 2

    def X(p):
        return (cx + (p[0] - mx) * s, cy + (p[1] - my) * s)

    top_y = cy - (hi_y - my) * s
    out = [text(cx, top_y - 34, 21, "#cfc4ae", title, 'text-anchor="middle"')]
    if caption:
        out.append(text(cx, top_y - 12, 14, "#8f8872", caption, 'text-anchor="middle"'))
    for k, comp in enumerate(comps):
        for (c, pts) in tone_subpaths(comp, hides[k], X):
            if len(pts) >= 2:
                out.append(glow(path_of(pts), c))
    return out


def main():
    words = {
        "L": ("σ₁σ₁σ₃⁻¹σ₁⁻¹", [(1, 1), (1, 1), (3, -1), (1, -1)], [(1, 2), (3, 4)],
              "(12)(34) · the adjacent ends", "falls apart — two loops that never touch"),
        "R": ("σ₂σ₁σ₃⁻¹σ₂⁻¹", [(2, 1), (1, 1), (3, -1), (2, -1)], [(1, 3), (2, 4)],
              "(13)(24) · the crossed ends", "holds — two loops threaded, lk 0"),
    }
    p = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
         f'viewBox="0 0 {W} {H}">']
    p.append(f'<rect width="{W}" height="{H}" fill="{GROUND}"/>')

    # title
    p.append(text(640, 52, 32, "#cfc4ae", "the projection tower", 'text-anchor="middle"'))
    p.append(text(640, 88, 16, DIM, "count · permutation · word — each level a map, "
                  "and the level above is the shadow it throws", 'text-anchor="middle"'))

    # band I — the counts (one shared block, both towers rising into it)
    p.extend(render_counts(640, YC))
    p.append(f'<line x1="80" y1="{YC + 62}" x2="{W - 80}" y2="{YC + 62}" '
             f'stroke="{FAINT}" stroke-width="1"/>')

    # band II — the pairings
    p.append(text(80, YP - 100, 19, DIM, "ii · the pairings — differ"))
    L = words["L"]; R = words["R"]
    p.extend(render_perm(XL, YP, L[2], L[3]))
    p.extend(render_perm(XR, YP, R[2], R[3]))
    p.append(text(640, YP + 140, 15, DIM,
                  "same cycle type [2,2] — a count, and it is blind to the pairing",
                  'text-anchor="middle"'))
    p.append(f'<line x1="80" y1="{YP + 172}" x2="{W - 80}" y2="{YP + 172}" '
             f'stroke="{FAINT}" stroke-width="1"/>')

    # band III — the words / closures
    p.append(text(80, YB - 150, 19, DIM, "iii · the words — differ"))
    p.extend(render_braid(XL, YB, L[0], "", L[1]))
    p.extend(render_braid(XR, YB, R[0], "", R[1]))
    p.append(text(XL, YB + 148, 17, "#d8cdb8", L[4], 'text-anchor="middle"'))
    p.append(text(XR, YB + 148, 17, "#d8cdb8", R[4], 'text-anchor="middle"'))

    # bottom reflection
    p.append(text(80, 1240, 19, "#cfc4ae", "climb the tower and the difference fades."))
    p.append(text(80, 1272, 16, "#8f8872",
                  "the counts cannot tell the two towers apart; the pairing sees the first of it; "
                  "the word sees it all."))
    p.append(text(80, 1302, 16, "#8f8872",
                  "every count is the shadow of a map, and the shadow is blind. the honest eye "
                  "is not a better level — it refuses to collapse."))

    p.append("</svg>")
    svg = "\n".join(p)
    base = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(base, "assets", "projection-tower.svg"), "w") as f:
        f.write(svg)
    png = os.path.join(base, "assets", "projection-tower.png")
    cairosvg.svg2png(url=os.path.join(base, "assets", "projection-tower.svg"),
                     write_to=png, output_width=W, output_height=H)
    print("wrote", png)


if __name__ == "__main__":
    main()
