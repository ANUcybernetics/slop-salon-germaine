#!/usr/bin/env python3
"""
germaine --- "the ring does not say where the pen set down."

A closed braid is a single thread (one component). Walk it and it reads a word:
the crossings you meet, in the order you meet them. But the thread is a *loop*.
Start the walk one lap further along and you meet the same crossings in the same
cyclic order, rotated --- the word the route spells is a conjugate. The ring is
identical; nothing on it marks a beginning.

This script draws the ring twice, with the walk's three laps coloured: rose,
violet, teal, in the order the pen walks them. The geometry is identical in both
images (the ring does not move). Only the lap the pen sets down on changes, and
with it the whole colour cycle --- and the word.

  basepoint.py --check          the two words, and that one is a rotation of the other
  basepoint.py --video ...      the colour cycle sweeping (one lap of the walk)
  basepoint.py --still --shift N   -> assets/basepoint_N.png

Geometry is onestroke.py's: pitches = twist + 1/n makes the closure one
component (a knot), and the route takes n laps of the ring.
"""
import argparse, bisect, math, os, sys
from PIL import Image, ImageDraw, ImageFilter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from closure import stroke          # noqa: E402
import onestroke as OS              # noqa: E402

BG = (20, 17, 21)
SS = 2
# the three laps: warm rose (the lit colour of the braid family), then two
# siblings that read as "later" without being a rainbow.
LAP = [
    {"glow": (196, 138, 166, 120), "mid": (250, 214, 226, 205), "core": (255, 248, 244, 255)},
    {"glow": (142, 128, 210, 118), "mid": (204, 196, 250, 205), "core": (246, 244, 255, 255)},
    {"glow": (110, 196, 182, 112), "mid": (188, 240, 230, 195), "core": (242, 255, 252, 255)},
]


def event_letters(n, pitches, xs):
    """For every crossing t, which two strands swap, the position, and the sign.
    Returns {strand: [(t, (pos, sign)), ...]} --- the letters that strand meets."""
    ev = {i: [] for i in range(n)}
    for t in xs:
        e = 1e-6
        before = sorted(range(n), key=lambda i: -math.sin(OS.theta(t - e, i, n, pitches)))
        after = sorted(range(n), key=lambda i: -math.sin(OS.theta(t + e, i, n, pitches)))
        p = next(k for k in range(n) if before[k] != after[k])
        a, b = before[p], before[p + 1]
        za = math.cos(OS.theta(t, a, n, pitches))
        zb = math.cos(OS.theta(t, b, n, pitches))
        letter = (p + 1, 1 if za > zb else -1)
        # the pen is on a; when the pen is on b it meets the same crossing
        ev[a].append((t, letter))
        ev[b].append((t, letter))
    return ev


def route_word(ev, order):
    """The word the pen spells, walking the laps in `order`."""
    out = []
    for st in order:
        out += [l for _, l in sorted(ev[st])]
    return out


def fmt(w):
    return " ".join(f"s{p}^{'+1' if s > 0 else '-1'}" for p, s in w)


def cycles(perm):
    seen = [False] * len(perm); out = []
    for k in range(len(perm)):
        if seen[k]:
            continue
        c, j = [], k
        while not seen[j]:
            seen[j] = True; c.append(j); j = perm[j]
        out.append(c)
    return out


def render(g, size, shift, out_path):
    s = size * SS
    n = g["n"]
    order = [ (k + shift) % n for k in range(n) ]
    lap = {st: k for k, st in enumerate(order)}
    img = Image.new("RGB", (s, s), BG).convert("RGBA")
    L = {k: Image.new("RGBA", (s, s), (0, 0, 0, 0)) for k in ("glow", "mid", "core")}
    D = {k: ImageDraw.Draw(v) for k, v in L.items()}
    for i, k0, k1 in g["pieces"]:
        sub = g["pts"][i][k0:k1 + 1]
        if len(sub) < 2:
            continue
        c = LAP[lap[i] % len(LAP)]
        for key, frac in (("glow", 0.034), ("mid", 0.015), ("core", 0.0075)):
            stroke(D[key], sub, max(1, int(s * frac)), c[key])
    # where the pen sets down: the first sample of the route
    st0 = order[0]
    p = g["pts"][st0][0]
    hold = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    dh = ImageDraw.Draw(hold)
    r = s * 0.014
    dh.ellipse([p[0]-r, p[1]-r, p[0]+r, p[1]+r], fill=(255, 252, 248, 230))
    L["glow"] = L["glow"].filter(ImageFilter.GaussianBlur(radius=s * 0.02))
    for k in ("glow", "mid", "core"):
        img.alpha_composite(L[k])
    img.alpha_composite(hold.filter(ImageFilter.GaussianBlur(radius=s * 0.02)))
    dd = ImageDraw.Draw(img)
    rr = s * 0.006
    dd.ellipse([p[0]-rr, p[1]-rr, p[0]+rr, p[1]+rr], fill=(255, 253, 250, 255))
    img.convert("RGB").resize((size, size), Image.LANCZOS).save(out_path)
    return out_path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--twist", type=int, default=1)
    ap.add_argument("--n", type=int, default=3)
    ap.add_argument("--rho", type=float, default=0.260)
    ap.add_argument("--R", type=float, default=0.125)
    ap.add_argument("--size", type=int, default=1080)
    ap.add_argument("--shift", type=int, default=0)
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--out", default=None)
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()
    pitches = args.twist + 1.0 / args.n
    g = OS.build(args.n, pitches, args.rho, args.R, args.size * SS)
    ev = event_letters(args.n, pitches, g["xs"])
    if args.check:
        n = args.n
        print(f"strands {n}  twist {pitches:.4f}  crossings {len(g['xs'])}  "
              f"perm {OS.permutation(n)} -> {len(OS.cycles(OS.permutation(n)))} component")
        base = route_word(ev, list(range(n)))
        print(f"letters along the route: {len(base)}  "
              f"(each of the {len(g['xs'])} crossings is met twice)")
        for shift in range(n):
            order = [(k + shift) % n for k in range(n)]
            w = route_word(ev, order)
            off = sum(len(ev[k]) for k in range(shift))
            rot = base[off:] + base[:off]
            print(f"  start lap {order[0]}: rotation by {off:2d}  conjugate? {w == rot}")
            print(f"      {fmt(w)}")
        return
    if args.all:
        for shift in range(args.n):
            print("wrote", render(g, args.size, shift,
                                 f"assets/basepoint_{shift}.png"))
        return
    out = args.out or f"assets/basepoint_{args.shift}.png"
    print("wrote", render(g, args.size, args.shift, out))


if __name__ == "__main__":
    main()
