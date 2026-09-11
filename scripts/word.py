#!/usr/bin/env python3
"""
germaine --- issue a braid word and draw it.

Every other braid script here *reads* its word off a sine field, so the word is
always a pure twist (sigma1 sigma2 repeated) and every closure is the same kind
of thing. This one takes the word as input instead: `--word 1212` is sigma1
sigma2 sigma1 sigma2. Strands swap lanes at each crossing, so the word is
legible in the drawing, and the closure's component count is the number of
cycles of the permutation.

The lane geometry works on a STRIP (the excursion is vertical, perpendicular to
the sweep) and cogs on a RING (the excursion is radial --- see TOOLS.md). Open
mode is the legible one; closed mode is here because sometimes you want to see
the sewing anyway.

Strands are coloured by the closure component they belong to, so a braid whose
closure is one thread is one colour, and a braid that closes to three loops is
three --- which is the whole content of rahel's "the sum is blind to which":

    word.py --word 1212 --check   ->  perm (0 1 2), 1 component, sum +4, 4 crossings
    word.py --word 1122 --check   ->  perm identity, 3 components, sum +4, 4 crossings

Usage:
  word.py --word 1212 --check
  word.py --word 1212 --mode open   -> assets/word_1212.png
  word.py --word 1212 --mode closed -> assets/word_1212_closed.png
"""
import argparse, math, os, sys
from PIL import Image, ImageDraw, ImageFilter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from closure import stroke  # noqa: E402

BG = (20, 17, 21)
SS = 2
COMP = [  # one tint per closure component
    {"glow": (196, 142, 168, 120), "mid": (246, 220, 230, 205), "core": (255, 250, 244, 255)},
    {"glow": (146, 120, 204, 110), "mid": (206, 188, 240, 195), "core": (244, 240, 255, 250)},
    {"glow": (112, 188, 176, 104), "mid": (182, 236, 226, 185), "core": (240, 255, 252, 250)},
]


def build(word, n, K=700, wfrac=0.35):
    """word: list of 1-based lane indices, each a positive crossing."""
    m = len(word)
    w = wfrac / m                      # half-width of the lane-change window
    ev = {s: [] for s in range(n)}
    occ, lane, zorder = list(range(n)), list(range(n)), list(range(n))
    bnd, orders = [0.0], []
    for k in word:
        k -= 1
        t = (len(orders) + 0.5) / m
        orders.append(list(zorder))
        bnd.append(t)
        a, b = occ[k], occ[k + 1]
        zorder.remove(a)               # a crosses over b: a moves to the front
        zorder.insert(zorder.index(b) + 1, a)
        ev[a].append((t, lane[a], lane[a] + 1))
        ev[b].append((t, lane[b], lane[b] - 1))
        occ[k], occ[k + 1] = b, a
        lane[a], lane[b] = lane[b], lane[a]
    orders.append(list(zorder))
    bnd.append(1.0)
    perm = [0] * n
    for lane_i, s in enumerate(occ):
        perm[s] = lane_i

    def lane_at(s, t):
        L = s
        for tm, before, after in ev[s]:
            if t >= tm + w:
                L = after
            elif t >= tm - w:
                u = (t - (tm - w)) / (2 * w)
                return before + (after - before) * u * u * (3 - 2 * u)
            else:
                return L
        return L

    return dict(n=n, K=K, word=word, bnd=bnd, orders=orders, lane_at=lane_at,
                perm=perm, cyc=cycles(perm))


def cycles(perm):
    n = len(perm)
    seen, out = [False] * n, []
    for k in range(n):
        if seen[k]:
            continue
        c, j = [], k
        while not seen[j]:
            seen[j] = True
            c.append(j)
            j = perm[j]
        out.append(c)
    return out


def place(mode, S, g, s, t, rho=0.30, gap=0.052):
    off = g["lane_at"](s, t) - (g["n"] - 1) / 2.0
    if mode == "open":
        return (t * S, S * (0.5 + off * 0.085))
    C = S / 2.0
    r = (rho + off * gap) * S
    phi = 2 * math.pi * t
    return (C + r * math.cos(phi), C + r * math.sin(phi))


def render(word, mode, size, out_path, n=3, K=700):
    S = size * SS
    g = build(word, n, K)
    cid = {s: j for j, c in enumerate(g["cyc"]) for s in c}
    img = Image.new("RGB", (S, S), BG).convert("RGBA")
    L = {k: Image.new("RGBA", (S, S), (0, 0, 0, 0)) for k in ("glow", "mid", "core")}
    D = {k: ImageDraw.Draw(v) for k, v in L.items()}
    for i in range(len(g["bnd"]) - 1):
        lo, hi = g["bnd"][i], g["bnd"][i + 1]
        if hi <= lo:
            continue
        for s in g["orders"][i]:                       # far -> near
            pts = [place(mode, S, g, s, lo + (hi - lo) * k / K) for k in range(K + 1)]
            c = COMP[cid[s] % len(COMP)]
            for key, frac in (("glow", 0.05), ("mid", 0.02), ("core", 0.009)):
                stroke(D[key], pts, max(1, int(S * frac)), c[key])
    L["glow"] = L["glow"].filter(ImageFilter.GaussianBlur(radius=S * 0.02))
    for k in ("glow", "mid", "core"):
        img.alpha_composite(L[k])
    img.convert("RGB").resize((size, size), Image.LANCZOS).save(out_path)
    return g, out_path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--word", default="1212", help="lane indices, e.g. 1212 = s1 s2 s1 s2")
    ap.add_argument("--n", type=int, default=3)
    ap.add_argument("--mode", choices=("open", "closed"), default="open")
    ap.add_argument("--size", type=int, default=900)
    ap.add_argument("--out", default=None)
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()
    word = [int(c) for c in args.word]
    g = build(word, args.n)
    if args.check:
        w = " ".join(f"s{k}+1" for k in word)
        print(f"word       {w}   n={args.n}   crossings {len(word)}   sum +{len(word)}")
        print(f"perm       {g['perm']}  ->  {len(g['cyc'])} component(s)  {g['cyc']}")
        return
    out = args.out or f"assets/word_{args.word}{'_closed' if args.mode == 'closed' else ''}.png"
    g, out = render(word, args.mode, args.size, out, args.n)
    print(f"wrote {out}   {len(g['cyc'])} component(s)")


if __name__ == "__main__":
    main()
