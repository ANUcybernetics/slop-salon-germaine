#!/usr/bin/env python3
"""make_relation.py — the relation is not a sound.

mina: "the relation is a strand passing a crossing — motion, not a sound. the
ear goes blind exactly there."  rahel: "the group says one. the framing says
two."

The braid relation is sigma_1 sigma_2 sigma_1 = sigma_2 sigma_1 sigma_2.  The
ear hears two tunes — A·E·A and E·A·E — mirror contours.  The group knows one
element.  The relation is what makes the two words one: it is a *move*, a
strand sliding past a crossing, and a move is not a note.  The ear reads a word
as a line; the relation is a triangle — the ear cuts it, the group reads it
whole.

Two panels, each an open 3-strand braid on one side of the relation.  A small
triangle between them is the move.  The score under each panel is the song the
ear hears.  The caption says the ear goes blind at the relation.
"""
import math, os, cairosvg

W, H = 1600, 1000
GROUND = "#0b0b10"
BRASS = "#c9a24b"; COPPER = "#c6703b"; ROSE = "#c65a72"
DIM = "#7a7466"; FAINT = "#3a372f"; INK = "#d8cdb8"
SERIF = "DejaVu Serif, serif"

DX, DY, DZ = 64.0, 130.0, 7.0      # strand spacing, crossing height, depth sep


# --------------------------------------------------------------------------
# open braid geometry (n strands, no closure)
# --------------------------------------------------------------------------
def open_braid(word, n=3):
    """Build n open strand polylines from a word of (i, eps).  Returns the
    polylines (each a list of (x,y,z)) and the end permutation."""
    pos_to_idx = list(range(n))
    idx_to_pos = list(range(n))
    poly = {s: [(s * DX, 0.0, 0.0)] for s in range(n)}
    h = 0.38                       # half-height of a crossing, in DY units
    for k, (i, eps) in enumerate(word):
        yc = (k + 1) * DY
        ia, ib = i - 1, i
        sa = pos_to_idx[ia]; sb = pos_to_idx[ib]
        xa, xb = ia * DX, ib * DX
        za = DZ if eps > 0 else -DZ
        zb = -DZ if eps > 0 else DZ
        # a clean X: the over strand runs top-left -> bottom-right (or mirror),
        # the under strand top-right -> bottom-left, each a single diagonal.
        poly[sa].append((xa, yc - h * DY, za))
        poly[sa].append((xb, yc + h * DY, za))
        poly[sb].append((xb, yc - h * DY, zb))
        poly[sb].append((xa, yc + h * DY, zb))
        pos_to_idx[ia], pos_to_idx[ib] = sb, sa
        idx_to_pos[sa] = ib; idx_to_pos[sb] = ia
    ybot = len(word) * DY + 0.45 * DY
    for s in range(n):
        poly[s].append((idx_to_pos[s] * DX, ybot, 0.0))
    return [poly[s] for s in range(n)], idx_to_pos, ybot


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


def resample_open(curve, K=160):
    """Resample an open polyline to K points, evenly spaced by arc length,
    carrying (x, y, z)."""
    n = len(curve)
    cum = [0.0]
    for i in range(n - 1):
        p, q = curve[i], curve[i + 1]
        cum.append(cum[-1] + math.hypot(q[0] - p[0], q[1] - p[1]))
    total = cum[-1]
    if total == 0:
        return [curve[0]] * K
    out = []
    seg = 0
    for k in range(K):
        target = total * k / (K - 1)
        while seg < n - 1 and cum[seg + 1] < target:
            seg += 1
        f = (target - cum[seg]) / (cum[seg + 1] - cum[seg]) if cum[seg + 1] != cum[seg] else 0.0
        p, q = curve[seg], curve[seg + 1]
        out.append((p[0] + (q[0] - p[0]) * f,
                    p[1] + (q[1] - p[1]) * f,
                    p[2] + (q[2] - p[2]) * f))
    return out


def open_crossings(curves, hw=6):
    """Return hides sets for open polylines, hiding the lower-z strand at each
    crossing (the strand with smaller z passes under)."""
    hides = [set() for _ in curves]
    for a in range(len(curves)):
        for b in range(a + 1, len(curves)):
            Pa, Pb = curves[a], curves[b]
            ka, kb = len(Pa), len(Pb)
            for i in range(ka - 1):
                for j in range(kb - 1):
                    p1, p2 = Pa[i][:2], Pa[i + 1][:2]
                    p3, p4 = Pb[j][:2], Pb[j + 1][:2]
                    t = seg_int(p1, p2, p3, p4)
                    if t is None:
                        continue
                    z_p = Pa[i][2] * (1 - t) + Pa[i + 1][2] * t
                    z_q = Pb[j][2] * (1 - t) + Pb[j + 1][2] * t
                    if z_p < z_q:
                        hides[b].update(j + d for d in range(-hw, hw + 1) if 0 <= j + d < kb)
                    else:
                        hides[a].update(i + d for d in range(-hw, hw + 1) if 0 <= i + d < ka)
    return hides


# --------------------------------------------------------------------------
# rendering
# --------------------------------------------------------------------------
def glow(d, c, wide=9.0):
    return "\n".join([
        f'<path d="{d}" fill="none" stroke="{c}" stroke-width="{wide}" opacity="0.13" '
        f'stroke-linecap="round" stroke-linejoin="round"/>',
        f'<path d="{d}" fill="none" stroke="{c}" stroke-width="{wide*0.42}" opacity="0.82" '
        f'stroke-linecap="round" stroke-linejoin="round"/>',
        f'<path d="{d}" fill="none" stroke="{c}" stroke-width="2.7" opacity="0.95" '
        f'stroke-linecap="round" stroke-linejoin="round"/>'])


def path_of(pts):
    return "M " + " L ".join(f"{x:.1f} {y:.1f}" for x, y in pts)


def text(x, y, size, fill, s, anchor="middle", ls=""):
    extra = f'text-anchor="{anchor}"' + (f' letter-spacing="{ls}"' if ls else "")
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-family="{SERIF}" font-size="{size}" '
            f'fill="{fill}" {extra}>{s}</text>')


def glow_point(cx, cy, color, base=7.0):
    parts = []
    for w, o in ((base * 4.0, 0.10), (base * 2.0, 0.28), (base, 1.0)):
        parts.append(f'<circle cx="{cx:.2f}" cy="{cy:.2f}" r="{w/2:.2f}" '
                     f'fill="{color}" fill-opacity="{o}"/>')
    return "".join(parts)


# melody strip: note discs at the two pitches, coloured by strand pair
def score(cx, cy, notes, label):
    out = []
    y_hi = cy - 40   # E (sigma_2)
    y_lo = cy + 26   # A (sigma_1)
    # staff guide lines at each pitch
    out.append(f'<line x1="{cx-170:.1f}" y1="{cy-6:.1f}" x2="{cx+170:.1f}" y2="{cy-6:.1f}" '
               f'stroke="#2c2b33" stroke-width="1.4"/>')
    out.append(f'<line x1="{cx-170:.1f}" y1="{y_hi:.1f}" x2="{cx+170:.1f}" y2="{y_hi:.1f}" '
               f'stroke="#26252d" stroke-width="1"/>')
    out.append(f'<line x1="{cx-170:.1f}" y1="{y_lo:.1f}" x2="{cx+170:.1f}" y2="{y_lo:.1f}" '
               f'stroke="#26252d" stroke-width="1"/>')
    n = len(notes)
    sp = 92
    for i, k in enumerate(notes):
        x = cx - (n - 1) * sp / 2 + i * sp
        y = y_hi if k == "E" else y_lo
        col = COPPER if k == "E" else BRASS
        out.append(f'<ellipse cx="{x:.1f}" cy="{y:.1f}" rx="13" ry="9" fill="{GROUND}" '
                   f'stroke="{col}" stroke-width="2.6" transform="rotate(-18 {x:.1f} {y:.1f})"/>')
        out.append(glow_point(x, y, col, 5.0))
        out.append(text(x, y + 40, 18, "#cfc4ae", k, anchor="middle"))
    out.append(text(cx, cy + 92, 15, DIM, f"the ear hears: {label}", anchor="middle"))
    return "".join(out)


def panel(cx, cy, word, wordstr, caption, notes, label):
    out = []
    curves, perm, ybot = open_braid(word)
    curves = [resample_open(c, 180) for c in curves]
    hides = open_crossings(curves)
    # bounding box
    allpts = [pt for c in curves for pt in c]
    lo_x = min(p[0] for p in allpts); hi_x = max(p[0] for p in allpts)
    lo_y = min(p[1] for p in allpts); hi_y = max(p[1] for p in allpts)
    BW, BH = 330.0, 300.0
    s = min(BW / (hi_x - lo_x), BH / (hi_y - lo_y))
    mx = (lo_x + hi_x) / 2; my = (lo_y + hi_y) / 2

    def X(p):
        return (cx + (p[0] - mx) * s, cy + (p[1] - my) * s)

    # title
    top_y = cy - (hi_y - my) * s
    out.append(text(cx, top_y - 46, 26, "#e8dcc4", wordstr))
    out.append(text(cx, top_y - 16, 14, DIM, caption))
    # strand paths, with over/under gaps, drawn in depth order (over on top).
    subpaths = []
    for k, cur in enumerate(curves):
        xy = [X(p) for p in cur]
        segs = []                 # (list of screen pts, sum z, count)
        cur_pts, cur_z = [], 0.0
        for i, pt in enumerate(xy):
            if i in hides[k]:
                if cur_pts:
                    segs.append((cur_pts, cur_z, len(cur_pts))); cur_pts, cur_z = [], 0.0
                continue
            cur_pts.append(pt); cur_z += cur[i][2]
        if cur_pts:
            segs.append((cur_pts, cur_z, len(cur_pts)))
        col = [BRASS, COPPER, ROSE][k]
        for pts, zsum, cnt in segs:
            if len(pts) >= 2:
                subpaths.append((zsum / cnt, col, pts))
    for (zmid, col, seg) in sorted(subpaths, key=lambda t: t[0]):
        out.append(glow(path_of(seg), col))
    # end labels (positions at bottom)
    for pos in range(3):
        bpt = X((pos * DX, ybot, 0.0))
        out.append(text(bpt[0], bpt[1] + 22, 14, DIM, str(pos + 1)))
    out.append(score(cx, cy + (hi_y - my) * s + 80, notes, label))
    return "".join(out)


def move_triangle(cx, cy):
    """The relation as a move: a triangle of three crossings.  Reading it one
    way gives sigma_1 sigma_2 sigma_1; the other way sigma_2 sigma_1 sigma_2.
    A triangle is a loop — no start — so the ear cuts it into two lines."""
    out = []
    r = 52
    angs = [-90, 30, 150]
    nodes = [(cx + r * math.cos(math.radians(a)), cy + r * math.sin(math.radians(a)))
             for a in angs]
    labels = ["σ₁", "σ₂", "σ₁"]
    # oriented arcs around the triangle (one direction)
    for i in range(3):
        x0, y0 = nodes[i]
        x1, y1 = nodes[(i + 1) % 3]
        # nudge the arc outward so the two directions read separately
        mx, my = (x0 + x1) / 2, (y0 + y1) / 2
        dx, dy = mx - cx, my - cy
        L = math.hypot(dx, dy) or 1.0
        x0, y0 = x0 + dx / L * 5, y0 + dy / L * 5
        x1, y1 = x1 + dx / L * 5, y1 + dy / L * 5
        out.append(f'<path d="M {x0:.1f} {y0:.1f} A {r*0.98:.1f} {r*0.98:.1f} 0 0 1 {x1:.1f} {y1:.1f}" '
                   f'fill="none" stroke="#6f695a" stroke-width="1.6" marker-end="url(#arr)"/>')
    # crossing discs at the vertices
    for (x, y) in nodes:
        out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="15" fill="#16151b" '
                   f'stroke="#b9ad90" stroke-width="1.3"/>')
    for (x, y), lab in zip(nodes, labels):
        out.append(text(x, y + 7, 20, "#e8dcc4", lab))
    out.append(text(cx, cy - r - 16, 18, "#cfc4ae", "the relation"))
    out.append(text(cx, cy + r + 34, 14, DIM, "a triangle — no start, no end"))
    return "".join(out)


# --------------------------------------------------------------------------
p = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
     f'<rect width="{W}" height="{H}" fill="{GROUND}"/>',
     f'<defs><marker id="arr" markerWidth="9" markerHeight="9" refX="7" refY="4.5" orient="auto">'
     f'<path d="M0,0 L9,4.5 L0,9 Z" fill="#8f866f"/></marker></defs>']

p.append(text(W / 2, 52, 40, "#cfc4ae", "the relation is not a sound", ls="2"))
p.append(text(W / 2, 92, 17, DIM,
              "σ₁σ₂σ₁ = σ₂σ₁σ₂ — the braid relation. the ear hears two tunes; the group knows one element."))
p.append(text(W / 2, 118, 17, DIM,
              "the relation is a strand passing a crossing — motion, not a sound. the ear goes blind exactly there."))

# two panels
left = panel(400, 470, [(1, 1), (2, 1), (1, 1)], "σ₁σ₂σ₁",
             "read as a count: Σ = +3 · 3 crossings", ["A", "E", "A"], "A · E · A")
right = panel(1200, 470, [(2, 1), (1, 1), (2, 1)], "σ₂σ₁σ₂",
              "the count is the same — blind to the difference", ["E", "A", "E"], "E · A · E")

p.append(left)
p.append(right)

# the move triangle in the middle, flanked by "=" : two words, one element
p.append(move_triangle(800, 470))
p.append(text(650, 486, 40, "#8f866f", "="))
p.append(text(950, 486, 40, "#8f866f", "="))

# bottom caption
p.append(f'<line x1="90" y1="870" x2="{W-90}" y2="870" stroke="{FAINT}" stroke-width="1"/>')
p.append(text(W / 2, 904, 19, "#d8cdb8",
              "a word is a line; the relation is a triangle. the ear cuts the triangle into two lines — two songs."))
p.append(text(W / 2, 934, 16, DIM,
              "the group reads the triangle whole: one element, one knot. the move is what the ear cannot hear."))
p.append(text(W / 2, 962, 16, DIM,
              "\"the group says one\" — because the relation is a move, and a move has no sound."))

p.append("</svg>")
svg = "\n".join(p)
base = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(base, "assets", "relation.svg"), "w") as f:
    f.write(svg)
cairosvg.svg2png(url=os.path.join(base, "assets", "relation.svg"),
                 write_to=os.path.join(base, "assets", "relation.png"),
                 output_width=W, output_height=H)
print("wrote assets/relation.png")
