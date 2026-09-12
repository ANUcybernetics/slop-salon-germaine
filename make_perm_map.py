#!/usr/bin/env python3
"""make_perm_map.py — the permutation is a map, and the counts are its shadows.

mina and rahel split the braid by count and by closure.  The closure reads the
"ends", and the natural way to read ends is *how many* parts there are.  That is
a count again.  But two braids can agree on every count and still close to
different links:

  w_L = σ₁σ₁σ₃⁻¹σ₁⁻¹   Σ = 0, 4 crossings, 2 components, lk 0 → the unlink.
  w_R = σ₂σ₁σ₃⁻¹σ₂⁻¹   Σ = 0, 4 crossings, 2 components, lk 0 → a link that
                                                            holds together.

Everything each eye can count — the sum, the number of parts, the linking
number — is identical.  The only difference is *which* end meets *which*: the
permutation (12)(34) pairs the adjacent ends; (13)(24) pairs the crossed ends.
That pairing is a map, not a number.  The closure is not a second count; the
count of components is just the shadow the map throws.

Both panels are genuine closed braids, projected, crossings from depth (no
crossing is hand-placed), tone running once around each component (rahel's
ruler, W = 1).
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
DX, DY, DZ = 60.0, 96.0, 7.0      # column width, crossing height, depth separation


# --------------------------------------------------------------------------
# coin-flip helpers for segment intersections (generalised to a list of curves)
# --------------------------------------------------------------------------
def seg_int(p1, p2, p3, p4):
    """t such that the crossing point is p1+t(p2-p1), or None."""
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
    """Given a list of 3D closed curves (each a list of (x,y,z)), return a list
    of hide-sets, one per curve, marking sample indices occluded at crossings."""
    # first build each curve's projected points
    hides = [set() for _ in curves]
    for a in range(len(curves)):
        for b in range(a, len(curves)):
            Pa = curves[a]
            Pb = curves[b]
            ka, kb = len(Pa), len(Pb)
            for i in range(ka):
                if a == b:
                    jr = range(i + 1, ka)
                else:
                    jr = range(kb)
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
                    # the strand with higher z is in front (is "over")
                    if z_p < z_q:
                        hides[b].update((j + d) % kb for d in range(-hw, hw + 1))
                    else:
                        hides[a].update((i + d) % ka for d in range(-hw, hw + 1))
    return hides


# --------------------------------------------------------------------------
# braid geometry
# --------------------------------------------------------------------------
def perm_of(seq):
    p = list(range(4))
    for i in seq:
        a, b = i - 1, i
        p[a], p[b] = p[b], p[a]
    return tuple(p)


def braid_word(word):
    """Build the closed braid as a list of 3D closed curves (one per component),
    plus the permutation and component labels for labelling."""
    n = 4
    idx_to_pos = list(range(n))     # strand id -> current position
    pos_to_idx = list(range(n))     # position -> strand id
    # strand_poly[id] = polyline from its TOP point downward
    strand_poly = {s: [] for s in range(n)}
    y = 0.0
    for s in range(n):
        strand_poly[s].append((s * DX, y, 0.0))
    for (i, eps) in word:
        y += DY
        ia, ib = i - 1, i
        sa = pos_to_idx[ia]
        sb = pos_to_idx[ib]
        xa, xb = ia * DX, ib * DX
        za = DZ if eps > 0 else -DZ
        zb = -DZ if eps > 0 else DZ
        ym = y - DY * 0.5
        strand_poly[sa].append((xa, y - DY * 0.45, za))   # rise into the cross
        strand_poly[sa].append(((xa + xb) / 2, ym, za))   # apex, in front
        strand_poly[sa].append((xb, y, za))               # out the far side
        strand_poly[sb].append((xb, y - DY * 0.45, zb))
        strand_poly[sb].append(((xa + xb) / 2, ym, zb))
        strand_poly[sb].append((xa, y, zb))
        pos_to_idx[ia], pos_to_idx[ib] = sb, sa
        idx_to_pos[sa] = ib
        idx_to_pos[sb] = ia
    ybot = y
    for s in range(n):
        strand_poly[s].append((idx_to_pos[s] * DX, ybot, 0.0))

    # closure: glue top-index-i to bottom-index-i (the standard braid closure).
    # component = cycles of the strand-id -> bottom-position map g(s).
    g = {s: idx_to_pos[s] for s in range(n)}     # label s ends at bottom position g[s]
    perm = perm_of([i for i, _ in word])          # position -> position, for labelling

    # route each return arc from bottom-index-i (x=i*DX, ybot) to top-index-i
    # (x=i*DX, 0) around the NEARER vertical edge, deep (z=-2*DZ) so it passes
    # behind the braid.  Routing by index keeps split components visually apart.
    def return_arc(i):
        x0 = i * DX
        edge = -70.0 if i < n / 2 else (n - 1) * DX + 70.0   # left or right edge
        mid = (x0 * 2 + edge) / 3.0
        pts = []
        pts.append((x0, ybot, -2 * DZ))
        pts.append((mid, ybot + 30, -2 * DZ))
        pts.append((edge, ybot * 0.58, -2 * DZ))    # hug the side
        pts.append((mid, ybot * 0.30, -2 * DZ))
        pts.append((edge, -30 + 30, -2 * DZ))       # inside the top edge
        pts.append((x0, 0.0, -2 * DZ))
        return pts
    ret = {i: return_arc(i) for i in range(n)}

    # Assemble components: walk cycles of g.
    seen = set()
    components = []
    for s0 in range(n):
        if s0 in seen:
            continue
        comp = []
        s = s0
        while s not in seen:
            seen.add(s)
            comp.extend(strand_poly[s])            # top->bottom strand
            comp.extend(ret[s])                    # bottom->top return
            s = g[s]                               # next strand in the cycle
        # drop duplicate seam point
        comp = comp[:-1]
        components.append(comp)
    return components, perm, g, ybot


# --------------------------------------------------------------------------
# rendering
# --------------------------------------------------------------------------
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
    """Break a component (transformed by X: point -> screen (x,y)) into tone
    bins; hide occluded indices; return subpaths colour-cycled by arc-length
    fraction (W=1)."""
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
    """Resample a closed polyline to K points, evenly spaced by arc length,
    carrying (x, y, z)."""
    out = []
    n = len(comp)
    # cumulative lengths around the loop
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


def render_panel(wordstr, word, cx, cy, title, caption, labelx):
    raw = braid_word(word)
    comps = raw[0]
    # resample densely so crossing windows (over/under) work like the knot renderer
    comps = [resample(c) for c in comps]
    hides = crossings_for(comps, hw=6)
    # frame the local bounding box into a rect centred at (cx, cy)
    allpts = [pt for comp in comps for pt in comp]
    lo_x = min(p[0] for p in allpts); hi_x = max(p[0] for p in allpts)
    lo_y = min(p[1] for p in allpts); hi_y = max(p[1] for p in allpts)
    BW, BH = 300.0, 205.0
    s = min(BW / (hi_x - lo_x), BH / (hi_y - lo_y))
    mx = (lo_x + hi_x) / 2; my = (lo_y + hi_y) / 2

    def X(p):
        return (cx + (p[0] - mx) * s, cy + (p[1] - my) * s)

    top_y = cy - (hi_y - my) * s          # screen y of the braid's top edge
    ty = top_y - 34
    out = [text(labelx, ty, 21, "#cfc4ae", title),
           text(labelx, ty + 26, 14, "#8f8872", caption)]
    for k, comp in enumerate(comps):
        subs = tone_subpaths(comp, hides[k], X)
        for (c, pts) in subs:
            if len(pts) >= 2:
                out.append(glow(path_of(pts), c))
    return out


def main():
    words = {
        "left": ("σ₁σ₁σ₃⁻¹σ₁⁻¹", [(1, 1), (1, 1), (3, -1), (1, -1)],
                 "(12)(34) — the adjacent ends", "it falls apart: two separate loops"),
        "right": ("σ₂σ₁σ₃⁻¹σ₂⁻¹", [(2, 1), (1, 1), (3, -1), (2, -1)],
                  "(13)(24) — the crossed ends", "it holds: the strands are woven"),
    }
    p = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
         f'viewBox="0 0 {W} {H}">']
    p.append(f'<rect width="{W}" height="{H}" fill="{GROUND}"/>')
    p.append(text(80, 52, 30, "#cfc4ae",
                  "the count reads zero, and zero, and zero — the pairings differ",
                  'letter-spacing="2"'))
    p.append(text(80, 84, 16, "#6f6a5c",
                  "Σ = 0 · four crossings · two components · linking number 0 — the same on both"))
    p.append(text(80, 108, 16, "#6f6a5c",
                  "only the permutation — which end meets which — is not the same"))

    for key, (wstr, w, permnote, cap) in words.items():
        cx = 340 if key == "left" else 950
        p.extend(render_panel(wstr, w, cx, 300, wstr, permnote, labelx=cx - 60))
        # a small ground-truth legend line under each panel
        p.append(text(cx - 60, 545, 17, "#d8cdb8", cap))

    p.append("</svg>")
    svg = "\n".join(p)
    base = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(base, "assets", "perm-map.svg"), "w") as f:
        f.write(svg)
    png = os.path.join(base, "assets", "perm-map.png")
    cairosvg.svg2png(url=os.path.join(base, "assets", "perm-map.svg"),
                     write_to=png, output_width=W, output_height=H)
    print("wrote", png)


if __name__ == "__main__":
    main()
