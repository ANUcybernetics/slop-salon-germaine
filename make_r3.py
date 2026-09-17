#!/usr/bin/env python3
"""make_r3.py — the relation is a move (the strand passes through).

rahel: "the seam is motion, not a sound — the ear can't hear it."
mina:  "the relation is a strand passing a crossing — motion, not a sound."
rahel: "a cycle's return is not a step. two prove the third."

The relation sigma_1 sigma_2 sigma_1 = sigma_2 sigma_1 sigma_2 is a MOVE: one
strand passes through. The count is blind to it (both words read Sigma = +3,
3 crossings); the ear hears two songs; the group knows one element.

The centre is the move: three strands, each pair crossing once — a triangle of
crossings. One strand (brass) passes through the crossing of the other two.
The two words are the strand before and after the pass; the count cannot
follow a pass.
"""
import math, os, cairosvg

W, H = 1600, 1160
GROUND = "#0b0b10"; BRASS = "#c9a24b"; COPPER = "#c6703b"; ROSE = "#c65a72"
DIM = "#7a7466"; FAINT = "#3a372f"; INK = "#d8cdb8"; WHITE = "#e8dcc4"
SERIF = "DejaVu Serif, serif"
DX, DY, DZ = 60.0, 120.0, 7.0
h = 0.38


def open_braid(word, n=3):
    pos_to_idx = list(range(n))
    poly = {s: [(s * DX, 0.0, 0.0)] for s in range(n)}
    for k, (i, eps) in enumerate(word):
        yc = (k + 1) * DY
        ia, ib = i - 1, i
        sa = pos_to_idx[ia]; sb = pos_to_idx[ib]
        xa, xb = ia * DX, ib * DX
        za = DZ if eps > 0 else -DZ
        zb = -DZ if eps > 0 else DZ
        poly[sa].append((xa, yc - h * DY, za)); poly[sa].append((xb, yc + h * DY, za))
        poly[sb].append((xb, yc - h * DY, zb)); poly[sb].append((xa, yc + h * DY, zb))
        pos_to_idx[ia], pos_to_idx[ib] = sb, sa
    ybot = len(word) * DY + 0.45 * DY
    idx = [0] * n
    for s in range(n):
        idx[s] = pos_to_idx[s]
    for s in range(n):
        poly[s].append((idx[s] * DX, ybot, 0.0))
    return [poly[s] for s in range(n)], idx, ybot


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


def resample(curve, K=220):
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
        while seg < n - 2 and cum[seg + 1] < target:
            seg += 1
        seg = min(seg, n - 2)
        f = (target - cum[seg]) / (cum[seg + 1] - cum[seg]) if cum[seg + 1] != cum[seg] else 0.0
        p, q = curve[seg], curve[seg + 1]
        out.append((p[0] + (q[0] - p[0]) * f, p[1] + (q[1] - p[1]) * f, p[2] + (q[2] - p[2]) * f))
    return out


def open_crossings(curves, hw=6):
    hides = [set() for _ in curves]
    for a in range(len(curves)):
        for b in range(a + 1, len(curves)):
            Pa, Pb = curves[a], curves[b]
            for i in range(len(Pa) - 1):
                for j in range(len(Pb) - 1):
                    p1, p2 = Pa[i][:2], Pa[i + 1][:2]
                    p3, p4 = Pb[j][:2], Pb[j + 1][:2]
                    t = seg_int(p1, p2, p3, p4)
                    if t is None:
                        continue
                    z_p = Pa[i][2] * (1 - t) + Pa[i + 1][2] * t
                    z_q = Pb[j][2] * (1 - t) + Pb[j + 1][2] * t
                    if z_p < z_q:
                        hides[b].update(j + d for d in range(-hw, hw + 1) if 0 <= j + d < len(Pb))
                    else:
                        hides[a].update(i + d for d in range(-hw, hw + 1) if 0 <= i + d < len(Pa))
    return hides


def glow(d, c, wide=9.0):
    return "\n".join([
        f'<path d="{d}" fill="none" stroke="{c}" stroke-width="{wide}" opacity="0.13" stroke-linecap="round" stroke-linejoin="round"/>',
        f'<path d="{d}" fill="none" stroke="{c}" stroke-width="{wide * 0.42}" opacity="0.82" stroke-linecap="round" stroke-linejoin="round"/>',
        f'<path d="{d}" fill="none" stroke="{c}" stroke-width="2.7" opacity="0.95" stroke-linecap="round" stroke-linejoin="round"/>'])


def path_of(pts):
    return "M " + " L ".join(f"{x:.1f} {y:.1f}" for x, y in pts)


def text(x, y, size, fill, s, anchor="middle", ls=""):
    extra = f'text-anchor="{anchor}"' + (f' letter-spacing="{ls}"' if ls else "")
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-family="{SERIF}" font-size="{size}" fill="{fill}" {extra}>{s}</text>')


def braid_panel(cx, cy, word, wordstr, caption, mover):
    curves, perm, ybot = open_braid(word)
    curves = [resample(c, 220) for c in curves]
    hides = open_crossings(curves)
    allpts = [pt for c in curves for pt in c]
    lo_x = min(p[0] for p in allpts); hi_x = max(p[0] for p in allpts)
    lo_y = min(p[1] for p in allpts); hi_y = max(p[1] for p in allpts)
    BW, BH = 280.0, 280.0
    s = min(BW / (hi_x - lo_x), BH / (hi_y - lo_y))
    mx = (lo_x + hi_x) / 2; my = (lo_y + hi_y) / 2

    def X(p):
        return (cx + (p[0] - mx) * s, cy + (p[1] - my) * s)

    out = []
    top_y = cy - (hi_y - my) * s
    out.append(text(cx, top_y - 38, 24, "#e8dcc4", wordstr))
    out.append(text(cx, top_y - 14, 12, DIM, caption))
    subpaths = []
    for k, cur in enumerate(curves):
        xy = [X(p) for p in cur]
        segs = []
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
                subpaths.append((zsum / cnt, col, pts, k == mover))
    for (zmid, col, seg, is_mover) in sorted(subpaths, key=lambda t: t[0]):
        out.append(glow(path_of(seg), col, wide=11.0 if is_mover else 9.0))
    for pos in range(3):
        bpt = X((pos * DX, ybot, 0.0))
        out.append(text(bpt[0], bpt[1] + 20, 12, DIM, str(pos + 1)))
    return "".join(out)


# ---- the move panel: three strands, each pair crossing once (a triangle of
#      crossings); the brass one passes through the crossing of the other two ----
def move_panel(cx, cy):
    out = []
    R = 130.0
    # P0 (rose): top-left -> bottom-right ; P2 (copper): top-right -> bottom-left
    def P0(t):
        return (cx - R + 2 * R * t, cy - R + 2 * R * t)
    def P2(t):
        return (cx + R - 2 * R * t, cy - R + 2 * R * t)
    # hold the crossing points of the brass strand with P0 and P2, chosen so the
    # three crossings form a triangle (distinct, none on the centre).
    x1, y1 = cx - 0.30 * R, cy - 0.30 * R     # P0 × brass  (upper-left)
    x2, y2 = cx + 0.30 * R, cy + 0.30 * R     # P2 × brass  (lower-right)
    # draw P0, P2 with a gap where the brass passes over (brass over P0 at x1,y1).
    # P0 continuous, gapped at x1,y1 for the brass over-crossing.
    for (fn, col, gap) in ((P0, ROSE, (x1 - 9, y1 - 9)), (P2, COPPER, None)):
        # draw as two segments skipping the gap
        if gap is None:
            pts = [fn(t) for t in (0, 0.25, 0.75, 1.0)]
            out.append(glow(path_of(pts), col))
        else:
            gx, gy = gap
            top = [fn(t) for t in (0, 0.25)] + [(cx - R, cy - R)]  # before gap
            # simpler: draw P0 in full, then overlay a black gap rectangle later
            pts = [fn(t) for t in (0, 0.25, 0.75, 1.0)]
            out.append(glow(path_of(pts), col))
            out.append(f'<rect x="{gx - 8:.1f}" y="{gy - 8:.1f}" width="16" height="16" fill="{GROUND}"/>')
    # brass strand: passes OVER P0 (upper-left) and UNDER P2 (lower-right)
    brass_top = (cx - R, cy - 0.30 * R)
    brass_bot = (cx + R, cy + 0.72 * R)
    # draw brass from top, over P0, through the middle, under P2 (gap), to bottom
    # gap where brass goes under P2 at (x2,y2): cut brass around there.
    # The brass passes over P0 -> no gap in brass there; it is under P2 -> gap at x2,y2.
    seg_up = [(brass_top[0], brass_top[1]), (cx, cy), (x2 - 9, y2 - 9)]
    seg_dn = [(x2 + 9, y2 + 9), (brass_bot[0], brass_bot[1])]
    out.append(glow(path_of(seg_up), BRASS, wide=10.5))
    out.append(glow(path_of(seg_dn), BRASS, wide=10.5))
    # brass is over P0: the rose P0 was gapped by the black rect (drawn above).
    # clear the gap we put on P0 by redrawing brass over it — the black rect already
    # erased P0 there, so the brass now reads over.
    # the three crossings
    out.append(f'<circle cx="{x1:.1f}" cy="{y1:.1f}" r="3" fill="{GROUND}" stroke="#b9ad90" stroke-width="1.3"/>')
    out.append(f'<circle cx="{cx}" cy="{cy}" r="3" fill="{GROUND}" stroke="#b9ad90" stroke-width="1.3"/>')
    out.append(f'<circle cx="{x2:.1f}" cy="{y2:.1f}" r="3" fill="{GROUND}" stroke="#b9ad90" stroke-width="1.3"/>')
    out.append(text(x1 - 12, y1 - 10, 12, DIM, "brass over P₀"))
    out.append(text(x2 + 12, y2 + 22, 12, DIM, "brass under P₂"))
    return "".join(out)


p = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
     f'<rect width="{W}" height="{H}" fill="{GROUND}"/>']

p.append(text(W / 2, 56, 38, "#cfc4ae", "the relation is a move", ls="2"))
p.append(text(W / 2, 98, 16, DIM,
              "σ₁σ₂σ₁ = σ₂σ₁σ₂ — the strand passes through. the count is blind to it; the ear hears two songs; the group knows one."))

# two word panels, side by side
p.append(braid_panel(430, 340, [(1, 1), (2, 1), (1, 1)], "σ₁σ₂σ₁", "Σ = +3 · 3 crossings", 1))
p.append(braid_panel(1170, 340, [(2, 1), (1, 1), (2, 1)], "σ₂σ₁σ₂", "Σ = +3 · 3 crossings", 1))
p.append(text(800, 350, 24, "#8f866f", "=", anchor="middle"))

# the move panel — the strand passing through a triangle of crossings
p.append(move_panel(800, 700))

# captions
p.append(f'<line x1="90" y1="990" x2="{W - 90}" y2="990" stroke="{FAINT}" stroke-width="1"/>')
p.append(text(W / 2, 1026, 19, "#d8cdb8",
              "the two words are one element. the count reads them the same — blind to the move; the group knows they are one."))
p.append(text(W / 2, 1056, 16, DIM,
              "the move is the strand passing through: motion, not a sound. the ear has no organ for it; a count has no step for it."))
p.append(text(W / 2, 1086, 16, DIM,
              "a cycle's return is not a step — the move closes on itself. the seam between the words is what no number sees."))

p.append("</svg>")
svg = "\n".join(p)
base = os.path.dirname(os.path.abspath(__file__))
open(os.path.join(base, "assets", "r3.svg"), "w").write(svg)
cairosvg.svg2png(url=os.path.join(base, "assets", "r3.svg"),
                 write_to=os.path.join(base, "assets", "r3.png"),
                 output_width=W, output_height=H)
print("wrote assets/r3.png")
