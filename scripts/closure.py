#!/usr/bin/env python3
"""
germaine --- "the route, and its closure."

One braid, two states.

  --mode open    three rows of rope braids running left to right, ends
                 off-frame: a route you can follow from one edge to the other.
  --mode closed  the same three rows sewn end to end and bent into concentric
                 rings. Same crossings, same strands --- but no edge, so no
                 thread has a place to begin.

The geometry is shared: every strand is sampled at a parameter t, placed by
`place()`, and given a depth z = cos(theta). Over/under is the same painter's
algorithm as braid.py --- depth order only flips where two strands exchange
their wave offset, so the width is split into bands at those t and each band's
strands are painted back-to-front (ascending z). The only difference between
the modes is the map from (t, offset) to the plane:

  open    (x, y) = (t*S, cy + R*sin(theta))
  closed  (x, y) = C + (rho + R*sin(theta)) * (cos 2pi t, sin 2pi t)

Because sin/cos of theta is periodic in 2*pi and the strand completes an
integer number of pitches over t in [0,1], the closed ring meets itself exactly:
place(0) == place(1) for every strand. The closure is not a seam that was
hidden --- there is no seam to hide.

Usage:
  closure.py --mode open   --size 1400 -> assets/closure_open.png
  closure.py --mode closed --size 1400 -> assets/closure_closed.png
  closure.py --check                    -> print the closure/seam numbers
"""
import argparse
import math

from PIL import Image, ImageDraw, ImageFilter

# ---- palette (sampled from assets/arcs-01.png) --------------------------------
BG = (20, 17, 21)               # near-black, faint magenta
GLOW = (150, 148, 158, 90)      # dim magenta-gray halo
MID = (205, 202, 210, 190)      # mid tube
CORE = (245, 243, 247)          # near-white heart

SS = 2                          # supersample factor
THIN = 1                        # draw stride; stroke() has no junctions, so dense
                                # is free
N = 3                           # strands per braid (odd -> a weave, not a rope)
PITCHES = 2                     # full turns of the strand about the braid axis
ROW_PHASE = (0.0, 0.35, 0.7)    # each row/ring at its own phase, so none mirror

OPEN = dict(rows=3, row_gap=0.28, R=0.085, rho_top=0.0, ring_gap=0.0)
CLOSED = dict(rows=3, row_gap=0.0, R=0.048, rho_top=0.42, ring_gap=0.13)


def theta(t, i, base):
    """Phase of strand i at parameter t."""
    return PITCHES * 2.0 * math.pi * t + base + 2.0 * math.pi * i / N


def place(mode, S, row, t, off, g):
    """Map (t, offset) to the plane. `off` is already in pixels."""
    if mode == "open":
        cy = S * (0.5 + (row - (g["rows"] - 1) / 2.0) * g["row_gap"])
        return (t * S, cy + off)
    C = S / 2.0
    rho = (g["rho_top"] - row * g["ring_gap"]) * S
    phi = 2.0 * math.pi * t
    r = rho + off
    return (C + r * math.cos(phi), C + r * math.sin(phi))


def wave(t, i, base):
    """(offset in units of R, depth toward viewer)."""
    a = theta(t, i, base)
    return math.sin(a), math.cos(a)


def crossings(base, grid=4000):
    """t values where two strands exchange their wave offset (sin order flips)."""
    out = []
    for i in range(N):
        for j in range(i + 1, N):
            prev = None
            for m in range(grid + 1):
                t = m / grid
                si = math.sin(theta(t, i, base))
                sj = math.sin(theta(t, j, base))
                cur = si - sj
                if prev is not None and prev != 0.0 and (prev > 0) != (cur > 0):
                    tp = (m - 1) / grid
                    frac = prev / (prev - cur)
                    out.append(tp + frac / grid)
                prev = cur
    out.sort()
    # dedupe crossings that land on top of each other
    ded = []
    for x in out:
        if not ded or x - ded[-1] > 1e-4:
            ded.append(x)
    return ded


def stroke(d, pts, w, col):
    """Paint a constant-width tube along a polyline as one filled polygon.

    ImageDraw.line() rasterizes each segment separately, so a dense polyline
    leaves a junction artifact at every vertex --- a comb of ticks along the
    tube at small strides, a step at the apex at large ones. Offsetting the
    polyline by its local normal and filling the ring has no junctions at all,
    so the stride is free to be as dense as the curve wants.
    """
    n = len(pts)
    if n < 2:
        return
    h = w / 2.0
    left, right = [], []
    for k in range(n):
        if k == 0:
            dx, dy = pts[1][0] - pts[0][0], pts[1][1] - pts[0][1]
        elif k == n - 1:
            dx, dy = pts[-1][0] - pts[-2][0], pts[-1][1] - pts[-2][1]
        else:
            dx, dy = pts[k + 1][0] - pts[k - 1][0], pts[k + 1][1] - pts[k - 1][1]
        L = math.hypot(dx, dy)
        if L == 0.0:
            dx, dy, L = 1.0, 0.0, 1.0
        nx, ny = -dy / L, dx / L
        left.append((pts[k][0] + nx * h, pts[k][1] + ny * h))
        right.append((pts[k][0] - nx * h, pts[k][1] - ny * h))
    d.polygon(left + right[::-1], fill=col)
    for e in (pts[0], pts[-1]):          # round caps
        d.ellipse([e[0] - h, e[1] - h, e[0] + h, e[1] + h], fill=col)


def bands_for(xs, closed):
    """Bands of t bounded by crossings. In closed mode the last wraps to the first."""
    if not xs:
        return [(0.0, 1.0)]
    if not closed:
        return [(0.0, xs[0])] + [(xs[k], xs[k + 1]) for k in range(len(xs) - 1)] + [(xs[-1], 1.0)]
    return [(xs[k], xs[k + 1] if k + 1 < len(xs) else xs[0] + 1.0) for k in range(len(xs))]


def draw_frame(mode, size, out_path, over=None, thin=None):
    global THIN
    if thin is not None:
        THIN = thin
    g = dict(OPEN if mode == "open" else CLOSED)
    if over:
        g.update(over)
    closed = mode == "closed"
    internal = size * SS
    S = internal
    img = Image.new("RGB", (internal, internal), BG)
    R = g["R"] * S

    glow = Image.new("RGBA", (internal, internal), (0, 0, 0, 0))
    mid = Image.new("RGBA", (internal, internal), (0, 0, 0, 0))
    core = Image.new("RGBA", (internal, internal), (0, 0, 0, 0))
    dg, dm, dc = ImageDraw.Draw(glow), ImageDraw.Draw(mid), ImageDraw.Draw(core)

    for row in range(g["rows"]):
        base = ROW_PHASE[row % len(ROW_PHASE)]
        xs = crossings(base)
        for lo, hi in bands_for(xs, closed):
            tm = 0.5 * (lo + hi)
            order = sorted(range(N), key=lambda i: wave(tm, i, base)[1])  # far -> near
            K = 96
            for i in order:
                pts = []
                for k in range(K + 1):
                    t = lo + (hi - lo) * k / K
                    off, z = wave(t, i, base)
                    pts.append(place(mode, S, row, t, R * off, g))
                sp = pts[::THIN]
                if sp[-1] != pts[-1]:
                    sp.append(pts[-1])
                if len(sp) < 2:
                    continue
                # three tube passes: wide halo, mid stroke, near-white core
                for dr, col, frac in ((dg, GLOW, 0.05), (dm, MID, 0.02), (dc, CORE, 0.009)):
                    stroke(dr, sp, max(1, int(S * frac)), col)

    glow = glow.filter(ImageFilter.GaussianBlur(radius=S * 0.02))
    img = img.convert("RGBA")
    img.alpha_composite(glow)
    img.alpha_composite(mid)
    img.alpha_composite(core)
    out = img.convert("RGB").resize((size, size), Image.LANCZOS)
    out.save(out_path)
    return out_path


def check():
    """Report what the closure actually does, numerically."""
    S = 1000.0
    for row in range(OPEN["rows"]):
        base = ROW_PHASE[row]
        for i in range(N):
            o0, z0 = wave(0.0, i, base)
            o1, z1 = wave(1.0, i, base)
            p0 = place("closed", S, row, 0.0, CLOSED["R"] * S * o0, CLOSED)
            p1 = place("closed", S, row, 1.0, CLOSED["R"] * S * o1, CLOSED)
            d = math.dist(p0, p1)
            print(f"ring {row} strand {i}: offset d={o1-o0:+.2e}  z d={z1-z0:+.2e}  "
                  f"seam gap={d:.3e}px (of {S:.0f})")
        xs = crossings(base)
        print(f"  ring {row}: {len(xs)} crossings, "
              f"first at t={xs[0]:.4f}, last at t={xs[-1]:.4f}")
    print("\neach strand returns to its own slot -> closure keeps N components; "
          "the crossings are unchanged, only the basepoint is spent.")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=("open", "closed"), default="open")
    ap.add_argument("--size", type=int, default=1400)
    ap.add_argument("--out", default=None)
    ap.add_argument("--rows", type=int, default=None)
    ap.add_argument("--R", type=float, default=None)
    ap.add_argument("--rho-top", type=float, default=None)
    ap.add_argument("--ring-gap", type=float, default=None)
    ap.add_argument("--row-gap", type=float, default=None)
    ap.add_argument("--thin", type=int, default=None)
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()

    if args.check:
        check()
        return
    over = {}
    if args.rows is not None:
        over["rows"] = args.rows
    if args.R is not None:
        over["R"] = args.R
    if args.rho_top is not None:
        over["rho_top"] = args.rho_top
    if args.ring_gap is not None:
        over["ring_gap"] = args.ring_gap
    if args.row_gap is not None:
        over["row_gap"] = args.row_gap
    out = args.out or f"assets/closure_{args.mode}.png"
    print("wrote", draw_frame(args.mode, args.size, out, over, args.thin))


if __name__ == "__main__":
    main()
