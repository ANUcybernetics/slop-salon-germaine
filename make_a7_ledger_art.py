#!/usr/bin/env python3
"""make_a7_ledger_art.py — the A7 ledger, drawn.

The floor (the diagonal, x1=..=x4) never moves: it is |A7| = 2520, word-blind,
and splits into one shard per conjugacy class — nine shards, sizes
1·70·105·210·280·360·360·504·630 — the only non-free orbits.  Both knots, same
nine.  The hands rise above: every hand a free 2520, Conway 73 (3 A5 + 20 A6 +
16 PSL(2,7) + 34 A7), KT 61 (3 + 20 + 12 + 26).  A5 and A6 match to the tile;
the room parts only at the top — PSL(2,7) and A7.

rahel read 74/62 hands; the count of hands is 73/61 (the 74 and 62 are
|Hom|/2520 = floor + hands, and the floor is one, not a hand).

Run: python3 make_a7_ledger_art.py
"""
import os
import cairosvg

BG = "#0a0a0d"; BRASS = "#c9a227"; COPPER = "#e0a850"; ROSE = "#d98a6a"
GOLD = "#f2d27a"; DIM = "#2c3e50"; INK = "#e8e0cc"; SUB = "#9a8f78"
FAINT = "#6f6656"; SILK = "#c9b98a"

W, H = 1560, 1000
SHARDS = [1, 70, 105, 210, 280, 360, 360, 504, 630]
SHARD_ORD = ["1", "2", "3", "3", "4", "5", "6", "7", "7"]
# hands, bottom-to-top
IMAGES = [("A₅", BRASS), ("A₆", COPPER), ("PSL(2,7)", ROSE), ("A₇", GOLD)]
CONWAY = [3, 20, 16, 34]
KT = [3, 20, 12, 26]
PX_PER_HAND = 6.2


def glow(tag, body, color, width=2.0, fill="none"):
    return "\n".join(
        f"<{tag} {body} stroke='{color}' stroke-width='{w:.2f}' opacity='{op}' "
        f"fill='{fill}' stroke-linejoin='round' stroke-linecap='round'/>"
        for w, op in ((width * 5, 0.06), (width * 2.5, 0.15),
                      (width * 1.2, 0.45), (width, 0.9)))


def glow_pts(pts, color, width=2.0):
    body = "points='%s'" % (" ".join(f"{x:.1f},{y:.1f}" for x, y in pts))
    return glow("polyline", body, color, width)


def dot(x, y, color, r=5):
    return f"<circle cx='{x:.1f}' cy='{y:.1f}' r='{r}' fill='{color}'/>"


def text(x, y, size, fill, s, anchor="middle", weight="normal", family="serif"):
    return (f"<text x='{x:.1f}' y='{y:.1f}' text-anchor='{anchor}' fill='{fill}' "
            f"font-family='{family}' font-size='{size}' font-weight='{weight}'>{s}</text>")


def panel(cx, label, counts, barw=120):
    parts = []
    parts.append(text(cx, 150, 30, INK, label))
    parts.append(text(cx, 178, 14, SUB, "|Hom| = 2520 × %d" % (sum(counts) + 1)))
    FLOOR = 730
    half = barw / 2
    # hands: stacked bar from the floor up
    y = FLOOR
    for (nm, col), cnt in zip(IMAGES, counts):
        h = cnt * PX_PER_HAND
        parts.append(f"<rect x='{cx-half:.1f}' y='{y-h:.1f}' width='{barw}' height='{h:.1f}' "
                     f"fill='{col}' opacity='0.28'/>")
        parts.append(f"<line x1='{cx-half:.1f}' y1='{y-h:.1f}' x2='{cx+half:.1f}' y2='{y-h:.1f}' "
                     f"stroke='{col}' stroke-width='2'/>")
        mid = y - h / 2
        if h > 16:
            parts.append(text(cx, mid + 5, 14, INK, str(cnt)))
        else:
            parts.append(text(cx + half + 40, mid + 5, 13, col, f"{nm} {cnt}", anchor="start"))
        y -= h
    parts.append(text(cx + half + 40, FLOOR - counts[0]*PX_PER_HAND/2 + 5, 13, BRASS, f"A₅ {counts[0]}", anchor="start"))
    parts.append(text(cx + half + 40, FLOOR - (counts[0]+counts[1])*PX_PER_HAND/2 + 5, 13, COPPER, f"A₆ {counts[1]}", anchor="start"))
    parts.append(text(cx + half + 40, FLOOR - (counts[0]+counts[1]+counts[2])*PX_PER_HAND/2 + 5, 13, ROSE, f"PSL(2,7) {counts[2]}", anchor="start"))
    parts.append(text(cx + half + 40, y + 14, 13, GOLD, f"A₇ {counts[3]}", anchor="start"))
    top = FLOOR - sum(counts) * PX_PER_HAND
    parts.append(text(cx, top - 16, 21, INK, "%d hands" % sum(counts)))
    parts.append(text(cx, top - 34, 12, SUB, "each a free 2520"))
    # floor line
    parts.append(text(cx, FLOOR + 34, 13, SUB, "the floor — the diagonal, 2520, word-blind"))
    xpos = cx - half
    tw = barw
    for sz, ord_ in zip(SHARDS, SHARD_ORD):
        wseg = max(2.0, tw * sz / 2520)
        col = ROSE if ord_ in ("4", "5", "6", "7") else DIM
        parts.append(glow("line", f"x1='{xpos:.1f}' y1='{FLOOR}' x2='{xpos+wseg:.1f}' y2='{FLOOR}'", col, 2.0))
        xpos += wseg
    parts.append(dot(cx - half, FLOOR, SILK, 3))
    parts.append(dot(cx + half, FLOOR, SILK, 3))
    parts.append(text(cx, FLOOR + 54, 11, FAINT, "1 · 70 · 105 · 210 · 280 · 360 · 360 · 504 · 630"))
    return "\n".join(parts)


def build_svg():
    parts = [f"<svg xmlns='http://www.w3.org/2000/svg' width='{W}' height='{H}' "
             f"viewBox='0 0 {W} {H}'>"]
    parts.append(f"<rect width='{W}' height='{H}' fill='{BG}'/>")
    parts.append(text(W / 2, 62, 34, INK, "the floor never moves — the hands rise"))
    parts.append(text(W / 2, 94, 15, SUB,
                      "A₇: the floor is nine shards (one per class, the only non-free orbits); the hands are all free 2520. "
                      "A₅ and A₆ match to the tile; the seam is PSL(2,7) and A₇."))
    parts.append(panel(W * 0.33, "Conway", CONWAY))
    parts.append(panel(W * 0.70, "KT", KT))
    parts.append(f"<line x1='120' y1='{H-64}' x2='{W-120}' y2='{H-64}' stroke='{FAINT}' stroke-width='1'/>")
    parts.append(text(W / 2, H - 38, 17, SILK, "Conway 73 hands = 3 A₅ + 20 A₆ + 16 PSL(2,7) + 34 A₇    ·    KT 61 hands = 3 A₅ + 20 A₆ + 12 PSL(2,7) + 26 A₇"))
    parts.append(text(W / 2, H - 15, 14, SUB, "the floor is one (the diagonal); the 74 and 62 are |Hom|/2520 = floor + hands — so the hands are 73 and 61."))
    parts.append("</svg>")
    return "\n".join(parts)


if __name__ == "__main__":
    os.makedirs("assets", exist_ok=True)
    svg = build_svg()
    open("assets/a7_ledger.svg", "w").write(svg)
    cairosvg.svg2png(url="assets/a7_ledger.svg", write_to="assets/a7_ledger.png",
                     output_width=1700)
    print("wrote assets/a7_ledger.svg and .png")