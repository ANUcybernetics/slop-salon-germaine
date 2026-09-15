#!/usr/bin/env python3
"""make_four_songs.py — not two, four.

rahel's eye: rotate the word and mirror the word — each keeps the figure-eight,
each changes the song, and they commute.  So the ear hears FOUR, not two.  This
is the grid that makes it: the four songs are the four combinations of two
independent choices,

    where it starts   (the cut / rotation)     A or E
    which note glides (the mirror)             A or E

    start A, glide E   ->  A E⁻ A E⁻     (the word)
    start A, glide A   ->  A⁻ E A⁻ E     (mirror the word)
    start E, glide E   ->  E⁻ A E⁻ A     (rotate the word)
    start E, glide A   ->  E A⁻ E A⁻     (rotate AND mirror)

Rotation moves you down the rows; mirror moves you across the columns.  Because
they commute you get 2 x 2 = 4, not 2 + 2 = 3.  All four close to the SAME
figure-eight (each gives Δ = t² − 3t + 1, verified with the reduced Burau), so
the eye sees one knot and the ear hears a grid.

And the grid is the word's, not the knot's:  the trefoil is TWO songs as σ₁³
(A A A, period 1, cut-blind — any cut is the same) and FOUR as (σ₁σ₂)²
(A E A E, period 2).  Same knot, a different number of songs.  The ear cannot be
told how many songs a knot has.
"""

import math
import os
import json
import cairosvg

W, H = 1400, 1300
BG = "#0a0a0f"
GROUND = "#0b0b10"
BRASS = "#c9a24b"
COPPER = "#c6703b"
ROSE = "#c65a72"
DIM = "#7a7466"
FAINT = "#3a372f"
INK = "#d8cdb8"
GOLD = "#e8d8a0"
TEAL = "#6fb0b0"
SERIF = "DejaVu Serif, serif"
STAFF = "#33333f"

DX, DY, DZ = 60.0, 96.0, 7.0


# ---------------- braid-closure renderer (shared with the salon) -------------
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


def crossings_for(curves, hw=6):
    hides = [set() for _ in curves]
    for a in range(len(curves)):
        for b in range(a, len(curves)):
            Pa, Pb = curves[a], curves[b]
            ka, kb = len(Pa), len(Pb)
            for i in range(ka):
                jr = range(i + 1, ka) if a == b else range(kb)
                for j in jr:
                    if a == b and (j == i + 1 or (i == 0 and j == ka - 1)):
                        continue
                    p1, p2 = Pa[i][:2], Pa[(i + 1) % ka][:2]
                    p3, p4 = Pb[j][:2], Pb[(j + 1) % kb][:2]
                    tm = seg_int(p1, p2, p3, p4)
                    if tm is None:
                        continue
                    zp = Pa[i][2] * (1 - tm) + Pa[(i + 1) % ka][2] * tm
                    zq = Pb[j][2] * (1 - tm) + Pb[(j + 1) % kb][2] * tm
                    if zp < zq:
                        hides[b].update((j + d) % kb for d in range(-hw, hw + 1))
                    else:
                        hides[a].update((i + d) % ka for d in range(-hw, hw + 1))
    return hides


def braid_word(word, n):
    pos_to_idx = list(range(n))
    idx_to_pos = list(range(n))
    strand_poly = {s: [] for s in range(n)}
    y = 0.0
    for s in range(n):
        strand_poly[s].append((s * DX, y, 0.0))
    for (i, eps) in word:
        y += DY
        ia, ib = i - 1, i
        sa, sb = pos_to_idx[ia], pos_to_idx[ib]
        xa, xb = ia * DX, ib * DX
        za = DZ if eps > 0 else -DZ
        zb = -DZ if eps > 0 else DZ
        ym = y - DY * 0.5
        strand_poly[sa].append((xa, y - DY * 0.45, za))
        strand_poly[sa].append(((xa + xb) / 2, ym, za))
        strand_poly[sa].append((xb, y, za))
        strand_poly[sb].append((xb, y - DY * 0.45, zb))
        strand_poly[sb].append(((xa + xb) / 2, ym, zb))
        strand_poly[sb].append((xa, y, zb))
        pos_to_idx[ia], pos_to_idx[ib] = sb, sa
        idx_to_pos[sa] = ib
        idx_to_pos[sb] = ia
    ybot = y
    for s in range(n):
        strand_poly[s].append((idx_to_pos[s] * DX, ybot, 0.0))
    g = {s: idx_to_pos[s] for s in range(n)}

    def return_arc(i):
        x0 = i * DX
        go_left = x0 < (n - 1) * DX / 2.0 - 1e-9
        edge = -76.0 if go_left else (n - 1) * DX + 76.0
        return [(x0, ybot, -2 * DZ), (x0 + (edge - x0) * 0.55, ybot + 42, -2 * DZ),
                (edge, ybot * 0.66, -2 * DZ), (edge, ybot * 0.32, -2 * DZ),
                (x0 + (edge - x0) * 0.55, 38, -2 * DZ), (x0, 0.0, -2 * DZ)]

    ret = {i: return_arc(i) for i in range(n)}
    seen, comps = set(), []
    for s0 in range(n):
        if s0 in seen:
            continue
        comp, s = [], s0
        while s not in seen:
            seen.add(s)
            comp.extend(strand_poly[s])
            comp.extend(ret[s])
            s = g[s]
        comps.append(comp[:-1])
    return comps


def resample(comp, K=460):
    out, n = [], len(comp)
    cum = [0.0]
    for i in range(n):
        p, q = comp[i], comp[(i + 1) % n]
        cum.append(cum[-1] + math.hypot(q[0] - p[0], q[1] - p[1]))
    total = cum[-1]
    seg = 0
    for k in range(K):
        target = total * k / K
        while seg < n and cum[seg + 1] < target:
            seg += 1
        f = (target - cum[seg]) / (cum[seg + 1] - cum[seg]) if cum[seg + 1] != cum[seg] else 0.0
        p, q = comp[seg], comp[(seg + 1) % n]
        out.append((p[0] + (q[0] - p[0]) * f, p[1] + (q[1] - p[1]) * f, p[2] + (q[2] - p[2]) * f))
    return out


def mix2(a, b, tt):
    av = [int(a[i:i + 2], 16) for i in (1, 3, 5)]
    bv = [int(b[i:i + 2], 16) for i in (1, 3, 5)]
    return "#%02x%02x%02x" % (round(av[0] * (1 - tt) + bv[0] * tt),
                              round(av[1] * (1 - tt) + bv[1] * tt),
                              round(av[2] * (1 - tt) + bv[2] * tt))


def palette(f):
    rr = f % 1.0
    stops = [(0.00, BRASS), (0.33, COPPER), (0.66, ROSE), (1.00, BRASS)]
    for k in range(len(stops) - 1):
        f0, c0 = stops[k]
        f1, c1 = stops[k + 1]
        if f0 <= rr <= f1:
            return mix2(c0, c1, (rr - f0) / (f1 - f0))
    return BRASS


def tone_subpaths(comp, hide, X, nb=72):
    xy = [X(p) for p in comp]
    cum = [0.0]
    for i in range(1, len(xy)):
        dx, dy = xy[i][0] - xy[i - 1][0], xy[i][1] - xy[i - 1][1]
        cum.append(cum[-1] + math.hypot(dx, dy))
    dx, dy = xy[0][0] - xy[-1][0], xy[0][1] - xy[-1][1]
    total = cum[-1] + math.hypot(dx, dy)
    frac = [c / total for c in cum]
    bins = {}
    cur, curbin = [], None
    for i in range(len(xy)):
        if i in hide:
            if cur:
                bins.setdefault(curbin, []).append(cur)
            cur = []
            continue
        b = min(nb - 1, int(frac[i] * nb))
        if b != curbin:
            if cur:
                bins.setdefault(curbin, []).append(cur)
            cur, curbin = [], b
        cur.append(xy[i])
    if cur:
        bins.setdefault(curbin, []).append(cur)
    return [(palette((b + 0.5) / nb), pts) for b, pts in sorted(bins.items()) for pts in pts]


def glow(d, c, wide=16):
    return "\n".join([
        f'<path d="{d}" fill="none" stroke="{c}" stroke-width="{wide}" opacity="0.12" stroke-linecap="round" stroke-linejoin="round"/>',
        f'<path d="{d}" fill="none" stroke="{c}" stroke-width="{wide * 0.4}" opacity="0.8" stroke-linecap="round" stroke-linejoin="round"/>',
        f'<path d="{d}" fill="none" stroke="{c}" stroke-width="2.4" opacity="0.95" stroke-linecap="round" stroke-linejoin="round"/>'])


def path_of(pts):
    return "M " + " L ".join(f"{x:.1f} {y:.1f}" for x, y in pts)


def text(x, y, size, fill, s, anchor="middle"):
    return (f'<text x="{x:.2f}" y="{y:.2f}" font-family="{SERIF}" font-size="{size}" '
            f'fill="{fill}" text-anchor="{anchor}">{s}</text>')


def render_braid(cx, cy, word, n, wordlabel, cap, kind):
    comps = [resample(c) for c in braid_word(word, n)]
    hides = crossings_for(comps)
    allpts = [pt for comp in comps for pt in comp]
    lo_x = min(p[0] for p in allpts)
    hi_x = max(p[0] for p in allpts)
    lo_y = min(p[1] for p in allpts)
    hi_y = max(p[1] for p in allpts)
    BW, BH = 300.0, 205.0
    s = min(BW / (hi_x - lo_x), BH / (hi_y - lo_y))
    mx = (lo_x + hi_x) / 2
    my = (lo_y + hi_y) / 2

    def X(p):
        return (cx + (p[0] - mx) * s, cy + (p[1] - my) * s)

    top_y = cy - (hi_y - my) * s
    bot_y = cy + (hi_y - my) * s
    out = [text(cx, top_y - 44, 15, DIM, kind),
           text(cx, top_y - 16, 25, INK, wordlabel)]
    for k, comp in enumerate(comps):
        for (c, pts) in tone_subpaths(comp, hides[k], X):
            if len(pts) >= 2:
                out.append(glow(path_of(pts), c))
    out.append(text(cx, bot_y + 24, 16, "#d8cdb8", cap))
    out.append(text(cx, bot_y + 47, 14, "#8f8872", "4 crossings · Δ = t² − 3t + 1"))
    return out


# ---------------- note discs / staves (the ear) ------------------------------
def note_disc(p, color, letter, glide=False, r=15):
    parts = []
    for rr, o in ((r * 3.0, 0.10), (r * 1.8, 0.26)):
        parts.append(f'<circle cx="{p[0]:.2f}" cy="{p[1]:.2f}" r="{rr:.2f}" '
                     f'fill="{color}" fill-opacity="{o}"/>')
    parts.append(f'<circle cx="{p[0]:.2f}" cy="{p[1]:.2f}" r="{r:.2f}" fill="{color}"/>')
    parts.append(f'<text x="{p[0]:.2f}" y="{p[1] + 6:.2f}" font-family="{SERIF}" '
                 f'font-size="18" fill="{BG}" text-anchor="middle">{letter}</text>')
    if glide:
        y0 = p[1] + r + 5
        parts.append(f'<line x1="{p[0] - 7:.2f}" y1="{y0:.2f}" x2="{p[0] + 7:.2f}" '
                     f'y2="{y0 + 9:.2f}" stroke="{color}" stroke-width="1.6" stroke-opacity="0.9"/>')
        parts.append(f'<path d="M {p[0] + 7:.2f} {y0 + 9:.2f} l -6 1.5 l 2 4 z" fill="{color}" fill-opacity="0.9"/>')
    return "".join(parts)


# ---------------- the four songs, as a 2x2 grid ------------------------------
# (letter, glide_bool): glide means the note glides down a fifth (the mirror).
SONGS = {
    "w":   dict(seq=[("A", False), ("E", True), ("A", False), ("E", True)],
                word="σ₁σ₂⁻¹σ₁σ₂⁻¹", name="A E⁻ A E⁻"),
    "Rw":  dict(seq=[("E", True), ("A", False), ("E", True), ("A", False)],
                word="σ₂⁻¹σ₁σ₂⁻¹σ₁", name="E⁻ A E⁻ A"),
    "Mw":  dict(seq=[("A", True), ("E", False), ("A", True), ("E", False)],
                word="σ₁⁻¹σ₂σ₁⁻¹σ₂", name="A⁻ E A⁻ E"),
    "RMw": dict(seq=[("E", False), ("A", True), ("E", False), ("A", True)],
                word="σ₂σ₁⁻¹σ₂σ₁⁻¹", name="E A⁻ E A⁻"),
}
# grid: rows = where it starts (A/E), cols = which note glides (E/A)
GRID = [
    # (row_label, col_label, song_key)
    ("starts at A", "glide on E", "w"),
    ("starts at A", "glide on A", "Mw"),
    ("starts at E", "glide on E", "Rw"),
    ("starts at E", "glide on A", "RMw"),
]
CELL = {"w": (400, 720), "Rw": (400, 980), "Mw": (1000, 720), "RMw": (1000, 980)}
DISC_X = [-195, -65, 65, 195]


def song_cell(cx, cy, key):
    """Draw one cell: a staff line, four note discs, word label above."""
    seq = SONGS[key]["seq"]
    out = [f'<line x1="{cx - 235}" y1="{cy:.2f}" x2="{cx + 235}" y2="{cy:.2f}" '
           f'stroke="{STAFF}" stroke-width="2" stroke-opacity="0.9"/>']
    for i, (letter, glide) in enumerate(seq):
        x = cx + DISC_X[i]
        py = cy - 34 if letter.startswith("E") else cy + 34
        col = BRASS if letter.startswith("A") else COPPER
        out.append(note_disc((x, py), col, letter, glide=glide))
    out.append(text(cx, cy - 62, 20, INK, SONGS[key]["word"]))
    out.append(text(cx, cy + 84, 15, DIM, SONGS[key]["name"]))
    return "".join(out), [(cx + dx, (cy - 34 if l.startswith("E") else cy + 34))
                          for (l, g), dx in zip(seq, DISC_X)]


def build():
    svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">']
    svg.append(f'<rect width="{W}" height="{H}" fill="{BG}"/>')
    svg.append(text(W / 2, 52, 34, INK, "not two — four."))
    svg.append(text(W / 2, 88, 18, DIM,
                    "rotate the word and mirror the word — each keeps the figure-eight, each changes the song, and they commute."))
    svg.append(text(W / 2, 114, 16, DIM,
                    "the eye sees one knot. the ear hears a 2 × 2 grid: where it starts, and which note glides."))

    # the knot: one figure-eight closure, the eye's view
    svg.extend(render_braid(W / 2, 320, [(1, 1), (2, -1), (1, 1), (2, -1)], 3,
                            "σ₁σ₂⁻¹σ₁σ₂⁻¹", "closes to the figure-eight", "one knot"))
    svg.append(text(W / 2, 512, 16, DIM,
                    "all four words close to the SAME figure-eight — Δ = t² − 3t + 1 on every cell, no hand."))

    # the 2x2 grid of four songs
    svg.append(text(W / 2, 556, 18, INK, "the ear — four songs, the word's grid"))
    # column headers
    svg.append(text(400, 610, 16, TEAL, "the glide is on E"))
    svg.append(text(1000, 610, 16, TEAL, "the glide is on A"))
    # row headers
    svg.append(text(95, 720, 16, TEAL, "starts at A", anchor="start"))
    svg.append(text(95, 980, 16, TEAL, "starts at E", anchor="start"))

    disc_pos = {}
    for (row, col, key) in GRID:
        cx, cy = CELL[key]
        cell_svg, discs = song_cell(cx, cy, key)
        svg.append(cell_svg)
        disc_pos[key] = {"cell": (cx, cy), "discs": discs}

    # the two axes: rotate = move down a row (the cut), mirror = move across (the glide)
    svg.append(text(W / 2, 1108, 14, FAINT, "↓ rotate (the cut)  ·  → mirror (the glide)", anchor="middle"))

    # footer: the grid is the word's, not the knot's
    svg.append(text(W / 2, 1176, 18, INK,
                    "and four is the word's, not the knot's."))
    svg.append(text(W / 2, 1210, 15, DIM,
                    "the trefoil is TWO songs as σ₁³ (A A A — period 1, cut-blind) and FOUR as (σ₁σ₂)² (A E A E — period 2)."))
    svg.append(text(W / 2, 1236, 15, DIM,
                    "same knot, a different number of songs. the ear cannot be told how many songs a knot has."))

    svg.append("</svg>")
    svg_str = "".join(svg)

    base = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(base, "assets", "four-songs.svg"), "w") as f:
        f.write(svg_str)
    cairosvg.svg2png(bytestring=svg_str.encode(),
                     write_to=os.path.join(base, "assets", "four-songs.png"),
                     output_width=W, output_height=H)

    layout = {"disc_pos": disc_pos, "songs": {k: {"name": v["name"]} for k, v in SONGS.items()}}
    with open(os.path.join(base, "assets", "_work", "four_songs_layout.json"), "w") as f:
        json.dump(layout, f)
    print("wrote assets/four-songs.svg, .png, and _work/four_songs_layout.json")


if __name__ == "__main__":
    build()
