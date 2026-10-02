#!/usr/bin/env python3
"""make_floor_map_art.py — the floor is the group's own map.

The floor is the DIAGONAL {x1=...=xn}: every Artin generator acts on a pair as
(a,b)->(aba^-1,a), fixing (g,g), so the whole diagonal is beta-hat-fixed for ANY
word — word-blind by construction.  Its Inn-orbits are one per conjugacy class:
the ground IS the group's conjugacy-class partition, summing to |G|.  The knot
contributes only the hands — each a free orbit of |Inn|.

Verified ledgers (class-restricted beta-hat, both words):
     room        |G|   #classes   Conway hands   KT hands
     A6          360      7           24            24
     A7         2520      9           73            61   <- the seam
     SL(2,5)     120      9            4             4   (|Inn|=60 each)
     PSL(2,7)    168      6            8             6   <- the part
     PSL(2,11)   660      8           10            10   <- the crossing

Run: python3 make_floor_map_art.py
"""
import math
import cairosvg

BG = "#0a0a0d"; BRASS = "#c9a227"; COPPER = "#e0a850"; ROSE = "#d98a6a"
DIM = "#2c3e50"; FAINT = "#6f6656"; INK = "#e8e0cc"; SUB = "#9a8f78"; PALE = "#f2d27a"

# (label, |G|, shard sizes (the class map), conway hands, kt hands, note)
ROOMS = [
    ("A₆", 360, [1, 45, 40, 40, 90, 72, 72], 24, 24, "both strokes agree"),
    ("A₇", 2520, [1, 70, 105, 210, 280, 360, 360, 504, 630], 73, 61, "the seam"),
    ("SL(2,5)", 120, [1, 1, 12, 12, 12, 12, 20, 20, 30], 4, 4, "|Inn| = 60, centre splits"),
    ("PSL(2,7)", 168, [1, 21, 24, 24, 42, 56], 8, 6, "the part"),
    ("PSL(2,11)", 660, [1, 55, 60, 60, 110, 110, 132, 132], 10, 10, "the crossing"),
]


def glow_line(x1, y1, x2, y2, color, width=2.0):
    return "\n".join(
        f"<line x1='{x1:.1f}' y1='{y1:.1f}' x2='{x2:.1f}' y2='{y2:.1f}' stroke='{color}' "
        f"stroke-width='{w:.2f}' opacity='{op}' stroke-linecap='round'/>"
        for w, op in ((width * 5, 0.06), (width * 2.5, 0.15),
                      (width * 1.2, 0.45), (width, 0.9)))


def rect(x, y, w, h, color, op=1.0, rx=2):
    return f"<rect x='{x:.1f}' y='{y:.1f}' width='{max(w,0):.1f}' height='{h:.1f}' rx='{rx}' fill='{color}' opacity='{op}'/>"


def text(x, y, size, fill, s, anchor="middle", weight="normal"):
    return (f"<text x='{x:.1f}' y='{y:.1f}' text-anchor='{anchor}' fill='{fill}' "
            f"font-family='serif' font-size='{size}' font-weight='{weight}'>{s}</text>")


def build_svg():
    W, H = 1560, 1180
    left, right = 210, W - 210
    span = right - left
    parts = [f"<svg xmlns='http://www.w3.org/2000/svg' width='{W}' height='{H}' viewBox='0 0 {W} {H}'>"]
    parts.append(f"<rect width='{W}' height='{H}' fill='{BG}'/>")
    parts.append(text(W / 2, 58, 40, INK, "the floor is the group's own map"))
    parts.append(text(W / 2, 94, 16, SUB,
                      "the ground is the diagonal x₁=…=xₙ — every σᵢ fixes (g,g), so it is word-blind by construction."))
    parts.append(text(W / 2, 116, 16, SUB,
                      "its Inn-orbits are one per conjugacy class: the floor is the group's conjugacy-class partition, summing to |G|."))
    parts.append(text(W / 2, 138, 14, FAINT,
                      "the knot contributes only the hands — each a free orbit of |Inn|.  the ground is the room's; the rise is the word's."))

    y0 = 196
    rowh = 178
    for idx, (label, G, shards, hc, hk, note) in enumerate(ROOMS):
        y = y0 + idx * rowh
        gy = y + 66                      # ground line
        parts.append(text(left - 24, y + 6, 20, INK, label, anchor="end", weight="bold"))
        parts.append(text(left - 24, y + 28, 13, FAINT, f"|G| = {G}", anchor="end"))
        parts.append(text(left - 24, y + 46, 12, FAINT, f"{len(shards)} classes", anchor="end"))
        # --- the ground: the class partition, segmented, widths ∝ class size ---
        gap = 4
        x = left
        tot = sum(shards)
        for j, sh in enumerate(shards):
            wseg = span * sh / tot - gap
            col = COPPER if j % 2 else BRASS
            parts.append(rect(x, gy, wseg, 24, col, op=0.85))
            if wseg > 40:
                parts.append(text(x + wseg / 2, gy + 17, 13, BG, str(sh), weight="bold"))
            x += wseg + gap
        parts.append(text(left, gy + 40, 12, FAINT, "the floor — one shard per conjugacy class", anchor="start"))
        parts.append(text(right, gy + 40, 12, FAINT, f"sum = {sum(shards)} = |G|", anchor="end"))
        # --- the hands: two readings of the same ground, widths ∝ hand count ---
        hmax = max(hc, hk, 1)
        hw = span * 0.86
        hy = gy - 54
        # Conway (rose)
        parts.append(rect(left, hy, hw * hc / hmax, 12, ROSE, op=0.9))
        parts.append(text(left + hw * hc / hmax + 10, hy + 10, 13, ROSE, f"Conway · {hc} hands", anchor="start"))
        # KT (gold)
        parts.append(rect(left, hy + 20, hw * hk / hmax, 12, PALE, op=0.9))
        parts.append(text(left + hw * hk / hmax + 10, hy + 30, 13, PALE, f"KT · {hk} hands", anchor="start"))
        # the note
        parts.append(text(right, y - 4, 13, SUB, note, anchor="end"))

    # --- footer ---
    ly = y0 + len(ROOMS) * rowh + 6
    parts.append(f"<line x1='{left-120}' y1='{ly-16}' x2='{right+120}' y2='{ly-16}' stroke='{FAINT}' stroke-width='1'/>")
    parts.append(text(W / 2, ly + 12, 18, "#cfc4ae",
                      "floor = |G|  (one shard per class, non-free, word-blind)      hands = |Inn| each  (free, word-dependent)"))
    parts.append(text(W / 2, ly + 42, 15, SUB,
                      "the two strokes share the ground; the seam lives in the hands alone — A₇ parts 73/61, PSL(2,7) 8/6, PSL(2,11) crosses 10/10."))
    parts.append(text(W / 2, ly + 68, 13, FAINT,
                      "the split is exact while the image self-centralizes; the centre is the chisel — in SL(2,5), |Z|=2, the floor is 120 but each hand only 60."))
    parts.append("</svg>")
    return "\n".join(parts)


if __name__ == "__main__":
    import os
    os.makedirs("assets", exist_ok=True)
    svg = build_svg()
    open("assets/floor_map.svg", "w").write(svg)
    cairosvg.svg2png(url="assets/floor_map.svg", write_to="assets/floor_map.png", output_width=1800)
    print("wrote assets/floor_map.svg and .png")