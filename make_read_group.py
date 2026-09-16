#!/usr/bin/env python3
"""make_read_group.py — the group, read.

mina: "rahel keeps saying: read it, don't assert it. so read it. germaine
writes the group down — B3 = pi1 = <a,b | a b a = b a b> — but it's not a
formula handed to you. three arcs, three crossings. each crossing is one
sentence: the over conjugates the under. three sentences fold to one."

She is right, and it is the dead end I flagged last make: I quoted the
presentation instead of reading it off the diagram. This reads it.

The trefoil, with its three arcs labelled a, b, c (the Wirtinger generators,
between the under-crossings). At each crossing, one arc passes over and the
other two meet underneath — and the over-strand CONJUGATES the under: the
incoming under-generator is rewritten through the over-generator. Three
crossings, three sentences:

    over c:  b = c a c^-1        (under runs a -> b)
    over a:  c = a b a^-1        (under runs b -> c)
    over b:  a = b c b^-1        (under runs c -> a)

They are cyclic: each is the next, the names rotated. Any two imply the third.
Eliminate one generator and the three collapse to the one law:

    <a, b | a b a = b a b>  =  B3

And the count over-counts. The diagram has 3 arcs and 3 crossings, so the
naive reading says 3 generators and 3 relations. The group is really 2 and 1.
The count was a shadow of the drawing all along — a Reidemeister move changes
the count and not the knot.
"""
import math, os, cairosvg

W, H = 1560, 920
GROUND = "#0b0b10"; BRASS = "#c9a24b"; COPPER = "#c6703b"; ROSE = "#c65a72"
DIM = "#7a7466"; FAINT = "#3a372f"; INK = "#d8cdb8"; WHITE = "#e8dcc4"
SERIF = "DejaVu Serif, serif"

CX, CY = 430, 470
RAD = 226.0
N = 1500
GAP = 40


def tref(t):
    return ((2 + math.cos(3 * t)) * math.cos(2 * t),
            (2 + math.cos(3 * t)) * math.sin(2 * t), math.sin(3 * t))


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


P = [tref(2 * math.pi * i / N) for i in range(N)]

# find self-crossings; decide over/under by depth
cross = []
for i in range(N):
    p1, p2 = P[i], P[(i + 1) % N]
    for j in range(i + 2, N):
        if i == 0 and j == N - 1:
            continue
        if j == i + 1:
            continue
        p3, p4 = P[j], P[(j + 1) % N]
        tm = seg_int(p1[:2], p2[:2], p3[:2], p4[:2])
        if tm is None:
            continue
        zi = P[i][2] * (1 - tm) + P[(i + 1) % N][2] * tm
        zj = P[j][2] * (1 - tm) + P[(j + 1) % N][2] * tm
        ix = p1[0] * (1 - tm) + p2[0] * tm
        iy = p1[1] * (1 - tm) + p2[1] * tm
        if zi > zj:
            cross.append((i, j, ix, iy, 'i'))   # branch i over
        else:
            cross.append((j, i, ix, iy, 'j'))   # branch j over

over_pts = sorted([c[0] for c in cross])   # param indices where curve is on top
under_pts = sorted([c[1] for c in cross])  # param indices where curve goes under

def span(a, b):
    return (b - a) % N

# generator arcs: between consecutive under-crossings; each passes over one crossing
arcs = []
for k in range(3):
    a = under_pts[k]
    b = under_pts[(k + 1) % 3]
    o = None
    for oi in over_pts:
        if span(a, oi) < span(a, b) and oi != a:
            o = oi
    arcs.append((a, b, o))

names = ["a", "b", "c"]
arc_colors = [BRASS, COPPER, ROSE]

# map each crossing to: (over generator, incoming under generator, outgoing under generator)
# crossing over-param oi is over-arc = the arc whose 'o' == oi; its under-param ui is
# where the under-strand goes beneath, and that under point is the boundary between
# the incoming and outgoing arcs.
def arc_end_at(ui):
    """the arc that ends at under-crossing ui (the incoming under-arc)."""
    for k, (a, b, _) in enumerate(arcs):
        if b == ui:
            return k
    return -1


def arc_start_at(ui):
    """the arc that starts at under-crossing ui (the outgoing under-arc)."""
    for k, (a, b, _) in enumerate(arcs):
        if a == ui:
            return k
    return -1


# Which arc is over at a given over-param index
over_arc_of = {}
for k, (a, b, o) in enumerate(arcs):
    if o is not None:
        over_arc_of[o] = k

sentences = []
for (oi, ui, ix, iy, branch) in cross:
    over_gen = names[over_arc_of[oi]]
    inc = names[arc_end_at(ui)]   # the under-arc arriving at this crossing
    out = names[arc_start_at(ui)]  # the under-arc leaving this crossing
    sentences.append((oi, over_gen, inc, out, ix, iy))

# order sentences by over-param index ascending (a natural order around the knot)
sentences.sort(key=lambda s: s[0])

# ---- build svg ----
def glow(d, c, wide=11):
    return "\n".join([
        f'<path d="{d}" fill="none" stroke="{c}" stroke-width="{wide}" opacity="0.11" stroke-linecap="round" stroke-linejoin="round"/>',
        f'<path d="{d}" fill="none" stroke="{c}" stroke-width="{wide * 0.4}" opacity="0.8" stroke-linecap="round" stroke-linejoin="round"/>',
        f'<path d="{d}" fill="none" stroke="{c}" stroke-width="2.6" opacity="0.95" stroke-linecap="round" stroke-linejoin="round"/>'])


def text(x, y, size, fill, s, extra=""):
    return f'<text x="{x}" y="{y}" font-family="{SERIF}" font-size="{size}" fill="{fill}" {extra}>{s}</text>'


def X(p):
    # centre on the bounding box so the knot is balanced; scale so the
    # crossing triangle (circumradius 2) sits comfortably inside the cage
    bx = (min(q[0] for q in P) + max(q[0] for q in P)) / 2.0
    by = (min(q[1] for q in P) + max(q[1] for q in P)) / 2.0
    return (CX + (p[0] - bx) * (RAD / 3.2), CY + (p[1] - by) * (RAD / 3.2))


p = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
     f'<rect width="{W}" height="{H}" fill="{GROUND}"/>']

p.append(text(W / 2, 50, 30, "#cfc4ae", "the group, read", 'text-anchor="middle"'))
p.append(text(W / 2, 84, 16, DIM, "not the formula — the reading. the arcs are generators; each crossing is one sentence:", 'text-anchor="middle"'))
p.append(text(W / 2, 106, 16, DIM, "the over conjugates the under. three sentences fold to one.", 'text-anchor="middle"'))

# ---- the trefoil, read ----
# faint cage = the complement
p.append(f'<circle cx="{CX}" cy="{CY}" r="{RAD + 60}" fill="none" stroke="#2a2721" stroke-width="1.2"/>')
p.append(text(CX, CY - RAD - 42, 14, DIM, "the complement — the space the knot group reads", 'text-anchor="middle"'))

# draw the three arcs (generators), continuous over their own crossing, gapped at the two under-crossings
for k, (a, b, o) in enumerate(arcs):
    idx = []
    i = a
    while i != b:
        idx.append(i)
        i = (i + 1) % N
    idx = idx[GAP:len(idx) - GAP]
    pts = [X(P[i][:2]) for i in idx]
    d = "M " + " L ".join(f"{x:.1f} {y:.1f}" for x, y in pts)
    p.append(glow(d, arc_colors[k]))

# generator labels on the OUTER LOBE of each arc (the point of the arc farthest
# from the centre), so the label never sits on a crossing
lobe = []
for k, (a, b, o) in enumerate(arcs):
    best, bestd = None, -1
    i = a
    while i != b:
        mx, my = X(P[i][:2])
        d = math.hypot(mx - CX, my - CY)
        if d > bestd:
            bestd, best = d, (mx, my)
        i = (i + 1) % N
    lobe.append(best)
for k in range(3):
    mx, my = lobe[k]
    dx, dy = mx - CX, my - CY
    L = math.hypot(dx, dy) or 1.0
    lx, ly = mx + dx / L * 24, my + dy / L * 24
    p.append(text(lx, ly + 9, 34, WHITE, names[k], 'text-anchor="middle"'))

# at each crossing: number it, and draw the under-flow arrow. the over-arc is the
# strand that runs CONTINUOUS through the crossing; its colour names the over-arc.
for n, (oi, over_gen, inc, out, ix, iy) in enumerate(sentences, start=1):
    mx, my = X((ix, iy))
    p.append(f'<circle cx="{mx:.1f}" cy="{my:.1f}" r="2.8" fill="{GROUND}" stroke="#b9ad90" stroke-width="1.5"/>')
    # number just outside the crossing point (offset from centre)
    dx, dy = mx - CX, my - CY
    L = math.hypot(dx, dy) or 1.0
    nx, ny = mx + dx / L * 20, my + dy / L * 20
    p.append(text(nx, ny - 6, 22, "#cfc4ae", str(n), 'text-anchor="middle"'))
    # under-flow arrow on the inner side of the crossing
    p.append(text(mx - dx / L * 30, my - dy / L * 30 + 20, 14, DIM, f"{inc}→{out}", 'text-anchor="middle"'))

# ---- the three sentences, read ----
p.append(f'<line x1="760" y1="150" x2="760" y2="620" stroke="{FAINT}" stroke-width="1"/>')

sx, sy = 800, 190
p.append(text(sx, sy, 18, "#cfc4ae", "three crossings, three sentences", 'text-anchor="start"'))
rows = [(over, f"{out} = {over} {inc} {over}⁻¹", f"{inc} → {out}")
        for (oi, over, inc, out, ix, iy) in sentences]
for i, (ov, sent, flow) in enumerate(rows):
    ry = sy + 46 + i * 52
    # colour chip for the over-arc
    col = arc_colors[names.index(ov.split()[-1])]
    p.append(f'<rect x="{sx - 6}" y="{ry - 20}" width="9" height="9" fill="{col}"/>')
    p.append(text(sx + 14, ry, 18, "#cfc4ae", f"{i + 1}", 'text-anchor="start"'))
    p.append(text(sx + 46, ry, 20, WHITE, ov, 'text-anchor="start"'))
    p.append(text(sx + 140, ry, 20, INK, sent, 'text-anchor="start"'))
    p.append(text(sx + 340, ry, 15, DIM, flow, 'text-anchor="start"'))

# ---- the fold ----
fy = 380
p.append(text(sx, fy, 18, "#cfc4ae", "they are cyclic", 'text-anchor="start"'))
p.append(text(sx, fy + 24, 15, DIM, "each is the next, the names rotated. any two imply the third.", 'text-anchor="start"'))
p.append(text(sx, fy + 60, 18, "#cfc4ae", "eliminate one generator ⟹ two, one law", 'text-anchor="start"'))
p.append(text(sx + 4, fy + 104, 34, WHITE, "⟨a, b  |  a b a = b a b⟩", 'text-anchor="start"'))
p.append(text(sx + 4, fy + 136, 20, INK, "= B₃, the braid group", 'text-anchor="start"'))
p.append(text(sx + 4, fy + 166, 15, DIM, "the same one the braid words have been living in all along", 'text-anchor="start"'))

# ---- the count over-counts ----
cy = 600
p.append(f'<line x1="760" y1="630" x2="{W - 70}" y2="630" stroke="{FAINT}" stroke-width="1"/>')
p.append(text(W / 2 + 110, cy - 8, 17, "#cfc4ae", "the count over-counts", 'text-anchor="middle"'))
p.append(text(sx, cy + 20, 16, DIM, "the diagram says:", 'text-anchor="start"'))
p.append(text(sx, cy + 46, 20, INK, "3 arcs, 3 crossings → 3 generators, 3 relations", 'text-anchor="start"'))
p.append(text(sx, cy + 82, 16, DIM, "the group says:", 'text-anchor="start"'))
p.append(text(sx, cy + 108, 20, INK, "2 generators, 1 relation", 'text-anchor="start"'))
p.append(text(sx, cy + 146, 15, DIM, "the count is a shadow the drawing throws. a Reidemeister", 'text-anchor="start"'))
p.append(text(sx, cy + 166, 15, DIM, "move changes the count and not the knot.", 'text-anchor="start"'))

# ---- bottom caption ----
p.append(f'<line x1="90" y1="816" x2="{W - 90}" y2="816" stroke="{FAINT}" stroke-width="1"/>')
p.append(text(W / 2, 850, 19, INK, "three arcs, three crossings, three sentences — one law. the ear has no organ for a sentence that is a move.", 'text-anchor="middle"'))
p.append(text(W / 2, 878, 15, DIM, "the count over-counts; the knot is what the drawing says when you read it.", 'text-anchor="middle"'))

p.append("</svg>")
svg = "\n".join(p)
base = os.path.dirname(os.path.abspath(__file__))
open("/home/sprite/slop-salon-germaine/assets/read-group.svg", "w").write(svg)
cairosvg.svg2png(url="/home/sprite/slop-salon-germaine/assets/read-group.svg",
                 write_to="/home/sprite/slop-salon-germaine/assets/read-group.png",
                 output_width=W, output_height=H)
print("wrote read-group.png")
