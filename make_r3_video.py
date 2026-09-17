#!/usr/bin/env python3
"""make_r3_video.py — the strand passes through (the move, as motion).

rahel: "the seam is motion, not a sound — the ear can't hear it."
mina:  "the relation is a strand passing a crossing — motion, not a sound."

The move, made: three strands, each pair crossing once — a triangle of
crossings. The brass strand passes through the crossing of the other two,
arching over it as it slides from one side to the other.  The crossings of the
brass with the rose and copper slide with it; the middle crossing stays; the
three crossings never collide (no triple point) — the brass goes OVER the
crossing, in depth, where a count has no organ.

The two ends are the two words sigma_1 sigma_2 sigma_1 and sigma_2 sigma_1
sigma_2.  The count reads them the same (Sigma = +3, 3 crossings); the ear
hears two songs; the group knows they are one element.
"""
import math, os, subprocess, cairosvg

GROUND = "#0b0b10"; BRASS = "#c9a24b"; COPPER = "#c6703b"; ROSE = "#c65a72"
DIM = "#7a7466"; INK = "#d8cdb8"
SERIF = "DejaVu Serif, serif"
W, H = 900, 720
CX, CY = 450, 430
SC = 250.0          # scale from normalized coords
WORK = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "_work", "r3")


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


def resample(curve, K=360):
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


def to_px(p):
    return (CX + p[0] * SC, CY + p[1] * SC)


def open_crossings(curves, hw=7):
    hides = [set() for _ in curves]
    for a in range(len(curves)):
        for b in range(a + 1, len(curves)):
            Pa, Pb = curves[a], curves[b]
            for i in range(len(Pa) - 1):
                for j in range(len(Pb) - 1):
                    p1, p2 = to_px(Pa[i][:2]), to_px(Pa[i + 1][:2])
                    p3, p4 = to_px(Pb[j][:2]), to_px(Pb[j + 1][:2])
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


def glow(d, c, wide=8.0):
    return "\n".join([
        f'<path d="{d}" fill="none" stroke="{c}" stroke-width="{wide}" opacity="0.12" stroke-linecap="round" stroke-linejoin="round"/>',
        f'<path d="{d}" fill="none" stroke="{c}" stroke-width="{wide * 0.42}" opacity="0.8" stroke-linecap="round" stroke-linejoin="round"/>',
        f'<path d="{d}" fill="none" stroke="{c}" stroke-width="2.6" opacity="0.95" stroke-linecap="round" stroke-linejoin="round"/>'])


def path_of(pts):
    return "M " + " L ".join(f"{x:.1f} {y:.1f}" for x, y in pts)


def text(x, y, size, fill, s, anchor="middle"):
    return f'<text x="{x:.1f}" y="{y:.1f}" font-family="{SERIF}" font-size="{size}" fill="{fill}" text-anchor="{anchor}">{s}</text>'


def frame_state(t):
    """Return the three curves (rose P0, copper P2, brass) for time t in [0,1].
    Brass slides from above (+yc) to below (-yc), arching over the centre."""
    yc = 0.40 * (1 - 2 * t)
    A = 0.52 * math.exp(-(yc / 0.32) ** 2)
    n = 360
    xs = [-1.35 + 2.7 * i / (n - 1) for i in range(n)]
    # z: brass passes OVER the centre crossing (its z is high near the centre).
    # Away from the centre the brass flips over/under the P0/P2 by the slide side.
    brass = []
    for x in xs:
        y = yc - A * math.exp(-(x * x) / (2 * 0.3 * 0.3))
        # over/under: t<0.5 brass over P0 (z +1), under P2 ; t>0.5 flips. Centre always over.
        zc = 3.0 * math.exp(-(x * x) / (2 * 0.3 * 0.3))   # arch clearance >0 always
        flip = (0.5 - t)                                 # + on before side
        z = zc + flip * 1.2
        brass.append((x, y, z))
    P0 = [(x, x, 0.0) for x in xs]                       # y = x
    P2 = [(x, -x, -1.0) for x in xs]                     # y = -x, P0 over P2
    # brass must pass over the P0xP2 centre crossing: at x=0 brass z = 3 + flip*1.2, P0 z=0,P2 z=-1 -> brass over. good.
    return [P0, P2, brass]


def render(t):
    out = []
    curves = frame_state(t)
    hides = open_crossings(curves)
    colours = [ROSE, COPPER, BRASS]
    subpaths = []
    for k, cur in enumerate(curves):
        xy = [to_px(p[:2]) for p in cur]
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
        for pts, zsum, cnt in segs:
            if len(pts) >= 2:
                subpaths.append((zsum / cnt, colours[k], pts, k == 2))
    # draw back-to-front by mean z so over strands land on top
    for (zmid, col, seg, is_brass) in sorted(subpaths, key=lambda t: t[0]):
        out.append(glow(path_of(seg), col, wide=11.0 if is_brass else 8.0))
    # crossing markers
    for (x, y) in [(0.0, 0.0)]:
        px, py = to_px((x, y))
        out.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="3" fill="{GROUND}" stroke="#b9ad90" stroke-width="1.3"/>')
    # top / side captions (static)
    return "".join(out)


def main():
    os.makedirs(WORK, exist_ok=True)
    NF = 60
    for f in range(NF):
        t = f / (NF - 1)
        svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
               f'<rect width="{W}" height="{H}" fill="{GROUND}"/>']
        svg.append(text(W / 2, 46, 34, "#cfc4ae", "the strand passes through"))
        svg.append(text(W / 2, 76, 14, DIM, "the relation is a move — σ₁σ₂σ₁ = σ₂σ₁σ₂"))
        svg.append(render(t))
        # side labels: the two words at the two ends of the slide
        label = "σ₁σ₂σ₁" if t < 0.5 else "σ₂σ₁σ₂"
        lx = 85 if t < 0.5 else W - 85
        la = "start" if t < 0.5 else "end"
        svg.append(text(lx, CY + 150, 22, "#e8dcc4", label))
        svg.append(text(lx, CY + 176, 12, DIM, la))
        svg.append(text(W / 2, H - 40, 14, DIM,
                        "the count reads both words the same (Σ = +3, 3 crossings); the group knows they are one element.",
                        anchor="middle"))
        svg.append("</svg>")
        fn = os.path.join(WORK, f"f{f:03d}.svg")
        open(fn, "w").write("\n".join(svg))
        cairosvg.svg2png(url=fn, write_to=fn.replace(".svg", ".png"), output_width=W, output_height=H)
    # assemble
    subprocess.run(["ffmpeg", "-y", "-framerate", "24", "-i", os.path.join(WORK, "f%03d.png"),
                    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-movflags", "+faststart",
                    os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "r3.mp4")],
                   check=True, capture_output=True)
    print("wrote assets/r3.mp4")


main()
