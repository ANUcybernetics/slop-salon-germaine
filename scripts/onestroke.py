#!/usr/bin/env python3
"""
germaine --- "the still says three, the stroke says one."

One braid, closed into a ring --- and whether the closure is three loops or one
knot is a single number in the twist.

Every strand is sampled at a parameter t and placed at
    r = rho + R*sin(theta),   theta = 2*pi*pitches*t + 2*pi*i/N,
    (x, y) = C + r*(cos 2*pi t, sin 2*pi t)
so the ring is automatic: angle 2*pi*t and angle 0 are the same place.

The closure has one component per cycle of the permutation the strands suffer
over one lap. Strand i ends at radius rate sin(2*pi*pitches + 2*pi*i/N). If
`pitches` is a whole number that is sin(2*pi*i/N) --- every strand lands in its
own slot, and the closure is N separate loops. But put one N-th of a turn more
into the twist and it is sin(2*pi*(i+1)/N): strand i lands exactly where strand
i+1 began. The slots are shifted by one, the permutation is a single N-cycle,
and the closure is ONE stroke --- a knot --- which takes N laps of the ring
before the pen comes back to where it started.

Nothing in the still can tell you which of those two you are looking at. At
every angle there are N strands either way. Only the route can.

The over/under is the same painter's algorithm as braid.py and closure.py:
depth is z = cos(theta), the width is split into bands at the angles where two
strands swap their radial order, and each band is painted back-to-front.

Usage:
  onestroke.py --check                       permutation, components, the word
  onestroke.py --still --q 1                 -> assets/onestroke.png
  onestroke.py --video --frames 288          -> assets/onestroke.mp4
"""

import argparse
import bisect
import math
import os
import sys

from PIL import Image, ImageDraw, ImageFilter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from closure import stroke  # noqa: E402  (fills a polygon; no junction artifacts)

# ---- palette (sampled from assets/arcs-01.png) --------------------------------
BG = (20, 17, 21)               # near-black, faint magenta

# unread: cold, dim --- present but not lit
COLD = {"glow": (150, 148, 158, 34),
        "mid": (205, 202, 210, 72),
        "core": (245, 243, 247, 92)}
# read: the route, warmed a step toward rose so the lit part is a different thing
WARM = {"glow": (196, 142, 168, 120),
        "mid": (246, 220, 230, 205),
        "core": (255, 250, 244, 255)}

SS = 2                          # supersample factor
K = 1400                        # samples per strand (one lap)
N = 3
TWIST = 2                       # whole turns of the rope; the closure gets +1/N


def theta(t, i, n, pitches):
    return 2.0 * math.pi * pitches * t + 2.0 * math.pi * i / n


def radius(t, i, n, pitches, rho, R):
    return rho + R * math.sin(theta(t, i, n, pitches))


def place(t, i, n, pitches, rho, R, s):
    phi = 2.0 * math.pi * t
    r = radius(t, i, n, pitches, rho, R) * s
    return (s / 2.0 + r * math.cos(phi), s / 2.0 + r * math.sin(phi))


def crossings(n, pitches, grid=24000):
    """Angles where two strands swap radial order. The whole closed curve has
    every strand present at every t, so one lap of t carries all of them."""
    out = []
    for i in range(n):
        for j in range(i + 1, n):
            prev = None
            for m in range(grid + 1):
                t = m / grid
                cur = math.sin(theta(t, i, n, pitches)) - math.sin(theta(t, j, n, pitches))
                if prev is not None and prev != 0.0 and (prev > 0) != (cur > 0):
                    frac = prev / (prev - cur)
                    out.append((m - 1 + frac) / grid)
                prev = cur
    out.sort()
    ded = []
    for x in out:
        if not ded or x - ded[-1] > 1e-6:
            ded.append(x)
    return ded


def permutation(n):
    """Strand i ends where strand (i + 1) % n began iff pitches = whole + 1/n."""
    return [(i + 1) % n for i in range(n)]


def read_word(n, pitches, xs):
    """The braid word the drawing spells, read off the crossings in order.

    Position 1 is the outermost strand (largest sin). sigma_k is the strand in
    position k passing over the one in position k+1, or under, by the sign."""
    word = []
    for t in xs:
        eps = 1e-6
        before = sorted(range(n),
                        key=lambda i: -math.sin(theta(t - eps, i, n, pitches)))
        after = sorted(range(n),
                       key=lambda i: -math.sin(theta(t + eps, i, n, pitches)))
        # the first index where the order differs is the pair that swapped
        p = next(p for p in range(n) if before[p] != after[p])
        a, b = before[p], before[p + 1]
        za = math.cos(theta(t, a, n, pitches))
        zb = math.cos(theta(t, b, n, pitches))
        word.append((p + 1, 1 if za > zb else -1))
    return word


def build(n, pitches, rho, R, s):
    xs = crossings(n, pitches)
    pts, cums = [], []
    for i in range(n):
        P, C = [], [0.0]
        for k in range(K + 1):
            t = k / K
            P.append(place(t, i, n, pitches, rho, R, s))
            if k:
                C.append(C[-1] + math.dist(P[-1], P[-2]))
        pts.append(P)
        cums.append(C)

    order = list(range(n))               # strand i hands off to strand i+1
    off, acc = {}, 0.0
    for i in order:
        off[i] = acc
        acc += cums[i][-1]
    total = acc

    bands, prev = [], 0.0
    for x in xs:
        if x > prev:
            bands.append((prev, x))
        prev = x
    if prev < 1.0:
        bands.append((prev, 1.0))

    pieces = []
    for lo, hi in bands:
        ka, kb = int(round(lo * K)), int(round(hi * K))
        if kb <= ka:
            continue
        tm = 0.5 * (lo + hi)
        for i in sorted(range(n), key=lambda i: math.cos(theta(tm, i, n, pitches))):
            pieces.append((i, ka, kb))   # far (small z) first

    return dict(xs=xs, pts=pts, cums=cums, off=off, total=total,
                order=order, pieces=pieces, n=n, pitches=pitches)


# ---- painting ----------------------------------------------------------------

def paint(draws, pieces, pts, colors, s, upto=None):
    """Draw pieces in paint order. `upto` (strand -> sample index) draws only the
    head of each piece --- that is the trail's leading edge."""
    for i, k0, k1 in pieces:
        if upto is not None:
            if i not in upto or upto[i] <= k0:
                continue
            k1 = min(k1, upto[i])
        sub = pts[i][k0:k1 + 1]
        if len(sub) < 2:
            continue
        for key, frac in (("glow", 0.034), ("mid", 0.015), ("core", 0.0075)):
            stroke(draws[key], sub, max(1, int(s * frac)), colors[key])


def soft_glow(layer, radius, factor=3):
    """Blur at reduced resolution --- a wide halo has no fine detail to lose, and
    this is the only expensive step per frame."""
    w, h = layer.size
    small = layer.resize((max(1, w // factor), max(1, h // factor)), Image.BILINEAR)
    small = small.filter(ImageFilter.GaussianBlur(radius / factor))
    return small.resize((w, h), Image.BILINEAR)


def point_at(g, q):
    target = q * g["total"]
    i = g["order"][-1]
    for cand in g["order"]:
        if target <= g["off"][cand] + g["cums"][cand][-1]:
            i = cand
            break
    u = max(0.0, min(target - g["off"][i], g["cums"][i][-1]))
    c = g["cums"][i]
    k = min(bisect.bisect_left(c, u), len(c) - 1)
    if k == 0:
        return g["pts"][i][0]
    span = c[k] - c[k - 1]
    f = 0.0 if span == 0 else (u - c[k - 1]) / span
    p0, p1 = g["pts"][i][k - 1], g["pts"][i][k]
    return (p0[0] + (p1[0] - p0[0]) * f, p0[1] + (p1[1] - p0[1]) * f)


def frame(g, size, q, dot_alpha, s, base=None):
    if base is None:                       # the dim layer never changes
        img = Image.new("RGB", (s, s), BG).convert("RGBA")
        drew = {k: Image.new("RGBA", (s, s), (0, 0, 0, 0)) for k in COLD}
        paint({k: ImageDraw.Draw(v) for k, v in drew.items()},
              g["pieces"], g["pts"], COLD, s)
        img.alpha_composite(soft_glow(drew["glow"], s * 0.02))
        img.alpha_composite(drew["mid"])
        img.alpha_composite(drew["core"])
        base = img

    out = base.copy()
    if q > 0.0:
        lit = q * g["total"]
        upto = {}
        for i in g["order"]:
            u = lit - g["off"][i]
            if u <= 0:
                continue
            upto[i] = bisect.bisect_right(g["cums"][i], min(u, g["cums"][i][-1]))
        drew = {k: Image.new("RGBA", (s, s), (0, 0, 0, 0)) for k in WARM}
        paint({k: ImageDraw.Draw(v) for k, v in drew.items()},
              g["pieces"], g["pts"], WARM, s, upto=upto)
        out.alpha_composite(soft_glow(drew["glow"], s * 0.02))
        out.alpha_composite(drew["mid"])
        out.alpha_composite(drew["core"])

    if dot_alpha > 0.0:                    # at q = 1 it sits on the start, fading
        p = point_at(g, q)
        hold = Image.new("RGBA", (s, s), (0, 0, 0, 0))
        dh = ImageDraw.Draw(hold)
        r = s * 0.015
        dh.ellipse([p[0] - r, p[1] - r, p[0] + r, p[1] + r],
                   fill=(255, 250, 244, int(dot_alpha)))
        out.alpha_composite(soft_glow(hold, s * 0.03))
        dd = ImageDraw.Draw(out)
        rr = s * 0.006
        dd.ellipse([p[0] - rr, p[1] - rr, p[0] + rr, p[1] + rr],
                   fill=(255, 252, 248, int(dot_alpha)))

    return out.convert("RGB").resize((size, size), Image.LANCZOS), base


def cycles(perm):
    seen = [False] * len(perm)
    out = []
    for k in range(len(perm)):
        if seen[k]:
            continue
        cyc, j = [], k
        while not seen[j]:
            seen[j] = True
            cyc.append(j)
            j = perm[j]
        out.append(cyc)
    return out


def check(g):
    n, pitches = g["n"], g["pitches"]
    perm = permutation(n)
    print(f"strands   {n}   twist  {pitches:.6g} turns  (= {TWIST} + 1/{n})")
    print(f"perm      {perm}  ->  {len(cycles(perm))} component(s)")
    print(f"laps      {len(g['order'])} before the stroke closes")
    print(f"length    {g['total']:.1f}px")
    for i in range(n):
        print(f"  strand {i}: lands in slot {perm[i]}   len {g['cums'][i][-1]:.1f}px")
    print(f"crossings {len(g['xs'])} at t = "
          + ", ".join(f"{x:.4f}" for x in g["xs"]))
    w = read_word(n, pitches, g["xs"])
    print("word      " + " ".join(f"s{k}^{'+1' if s > 0 else '-1'}" for k, s in w))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--twist", type=int, default=TWIST)
    ap.add_argument("--n", type=int, default=N)
    ap.add_argument("--rho", type=float, default=0.260)
    ap.add_argument("--R", type=float, default=0.125)
    ap.add_argument("--size", type=int, default=1080)
    ap.add_argument("--q", type=float, default=1.0)
    ap.add_argument("--out", default=None)
    ap.add_argument("--still", action="store_true")
    ap.add_argument("--video", action="store_true")
    ap.add_argument("--frames", type=int, default=288)
    ap.add_argument("--fps", type=int, default=24)
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()

    pitches = args.twist + 1.0 / args.n
    g = build(args.n, pitches, args.rho, args.R, args.size * SS)

    if args.check:
        check(g)
        return

    if args.video:
        import tempfile
        fdir = tempfile.mkdtemp(prefix="onestroke_frames_")
        trace = int(args.frames * 0.62)
        fade = int(args.frames * 0.14)
        base = None
        for f in range(args.frames):
            if f < trace:
                q, dot = f / (trace - 1), 255.0
            else:
                q = 1.0
                dot = 255.0 * max(0.0, 1.0 - (f - trace) / max(1, fade))
            img, base = frame(g, args.size, q, dot, args.size * SS, base)
            img.save(os.path.join(fdir, f"f{f:04d}.png"))
            if f % 12 == 0:
                print(f"\rframe {f}/{args.frames}", end="", flush=True)
        print()
        out = args.out or "assets/onestroke.mp4"
        os.system(
            f"ffmpeg -y -loglevel error -framerate {args.fps} -i {fdir}/f%04d.png "
            f"-c:v libx264 -pix_fmt yuv420p -crf 18 -movflags +faststart {out}"
        )
        print("wrote", out)
        return

    out = args.out or "assets/onestroke.png"
    img, _ = frame(g, args.size, args.q, 0.0 if args.q >= 1.0 else 255.0,
                   args.size * SS)
    img.save(out)
    print("wrote", out)


if __name__ == "__main__":
    main()
