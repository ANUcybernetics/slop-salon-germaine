#!/usr/bin/env python3
"""make_fold_inverse.py — a fold is an inversion, not a coincidence.

The weave is beta_hat(x_j) = c_j x_{b_j} c_j^-1 with bases [3,1,4,2], so all
four meridians are mutually conjugate.  If two of them x_i, x_j lie in a common
torus T (their centralizer), then the weave word w carrying x_i to x_j sends T
to itself, so w in N(T) = D_{2m}.  N(T) acts on T by identity (w in T -> x_j =
x_i, a collapse) or inversion (w in N(T)\\T -> x_j = x_i^-1).  The meridians are
distinct, so the fold is ALWAYS an inversion.

So a fold is not two strangers meeting in a torus — it is ONE axis traversed
both ways.  x and x^-1 have the same two fixed points (the same chord on P^1),
opposite directions.  Verified (verify_fold_inverse.py, p=7,11,13,17,19): every
fold pair is an inverse pair, on a weave-adjacent pair, ZERO counterexamples —
even at m=5 where non-inverse commuting pairs are structurally available.
"""
import cairosvg
import math

BG = "#0b0907"
BRASS = "#d4a017"
BRASS_EDGE = "#f0c75e"
BRASS_DIM = "#8a6a12"
COPPER = "#c07a5a"
COPPER_EDGE = "#e0a37f"
ROSE = "#c05a7a"
TXT = "#d8c9a8"
DIM = "#8a7d63"
MUTED = "#5f5748"
DARK_EDGE = "#3a332c"

W, H = 1600, 920


def pt(k, p, cx, cy, R):
    ang = -math.pi / 2 + 2 * math.pi * k / (p + 1)
    return (cx + R * math.cos(ang), cy + R * math.sin(ang))


def arrow(x1, y1, x2, y2, color, w=2.4, head=9, op=1.0):
    """line with an arrowhead at (x2,y2)."""
    dx, dy = x2 - x1, y2 - y1
    L = math.hypot(dx, dy) or 1
    ux, uy = dx / L, dy / L
    hx, hy = x2 - ux * head, y2 - uy * head
    px, py = -uy, ux
    ah = head * 0.62
    a1 = (hx + px * ah, hy + py * ah)
    a2 = (hx - px * ah, hy - py * ah)
    return (
        f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{hx:.1f}" y2="{hy:.1f}" '
        f'stroke="{color}" stroke-width="{w}" stroke-opacity="{op}" stroke-linecap="round"/>'
        f'<polygon points="{x2:.1f},{y2:.1f} {a1[0]:.1f},{a1[1]:.1f} {a2[0]:.1f},{a2[1]:.1f}" '
        f'fill="{color}" fill-opacity="{op}"/>'
    )


def fold_chord(k1, k2, p, cx, cy, R):
    """one axis, traversed both ways: x and x^-1 share the chord, opposite arrows."""
    x1, y1 = pt(k1, p, cx, cy, R)
    x2, y2 = pt(k2, p, cx, cy, R)
    # perpendicular offset so the two counter-arrows both read
    dx, dy = x2 - x1, y2 - y1
    L = math.hypot(dx, dy) or 1
    px, py = -dy / L, dx / L
    off = 4.0
    # under-glow beam
    beam = (f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
            f'stroke="{BRASS}" stroke-width="13" stroke-opacity="0.16" stroke-linecap="round"/>'
            f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
            f'stroke="{BRASS}" stroke-width="3.6" stroke-opacity="0.5" stroke-linecap="round"/>')
    # counter arrows: x_j (k1->k2), x_i (k2->k1)
    a1 = arrow(x1 + px * off, y1 + py * off, x2 + px * off, y2 + py * off,
               BRASS_EDGE, w=2.2, head=10)
    a2 = arrow(x2 - px * off, y2 - py * off, x1 - px * off, y1 - py * off,
               ROSE, w=2.2, head=10)
    return beam + a1 + a2


def chord(k1, k2, p, cx, cy, R):
    x1, y1 = pt(k1, p, cx, cy, R)
    x2, y2 = pt(k2, p, cx, cy, R)
    return (f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
            f'stroke="{COPPER}" stroke-width="2" stroke-opacity="0.8" stroke-linecap="round"/>'
            f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
            f'stroke="{COPPER_EDGE}" stroke-width="0.6" stroke-opacity="0.5"/>')


def node(x, y, label, color, edge, r=15):
    return (f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{color}" '
            f'stroke="{edge}" stroke-width="1.6" fill-opacity="0.16"/>'
            f'<text x="{x:.1f}" y="{y+5:.1f}" text-anchor="middle" '
            f'font-family="DejaVu Sans Mono" font-size="15" fill="{TXT}">{label}</text>')


def weave_cycle(cx, cy, fold_edge):
    """the 4-cycle x1->x3->x4->x2->x1; fold_edge is the (from,to) highlighted."""
    R = 150
    # positions: x1 top, x3 right, x4 bottom, x2 left
    pos = {1: (cx, cy - R), 3: (cx + R, cy), 4: (cx, cy + R), 2: (cx - R, cy)}
    edges = [(1, 3), (3, 4), (4, 2), (2, 1)]
    out = []
    # faint cycle
    for (a, b) in edges:
        x1, y1 = pos[a]
        x2, y2 = pos[b]
        if (a, b) == fold_edge or (b, a) == fold_edge:
            continue
        out.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{DARK_EDGE}" '
                   f'stroke-width="2" stroke-opacity="0.8"/>')
    # the fold edge: strong brass beam with the inversion
    a, b = fold_edge
    x1, y1 = pos[a]
    x2, y2 = pos[b]
    out.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{BRASS}" '
               f'stroke-width="9" stroke-opacity="0.22" stroke-linecap="round"/>')
    out.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{BRASS_EDGE}" '
               f'stroke-width="2.6" stroke-linecap="round"/>')
    # the conjugator label along the fold edge
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2
    out.append(f'<text x="{mx}" y="{my-10}" text-anchor="middle" font-family="DejaVu Sans Mono" '
               f'font-size="12" fill="{BRASS_EDGE}">c∈N(T)</text>')
    # nodes
    for k in (1, 2, 3, 4):
        col = BRASS if k in (a, b) else COPPER
        edge = BRASS_EDGE if k in (a, b) else COPPER_EDGE
        out.append(node(pos[k][0], pos[k][1], f"x{k}", col, edge))
    # arrowheads on the cycle
    for (aa, bb) in edges:
        x1, y1 = pos[aa]
        x2, y2 = pos[bb]
        ux, uy = (x2 - x1), (y2 - y1)
        L = math.hypot(ux, uy) or 1
        ux, uy = ux / L, uy / L
        tip = (x1 + ux * (L - 10), y1 + uy * (L - 10))
        out.append(arrow(x1 + ux * 18, y1 + uy * 18, tip[0], tip[1],
                         BRASS if (aa, bb) == fold_edge else DIM, w=2, head=8,
                         op=0.95 if (aa, bb) == fold_edge else 0.6))
    return "".join(out)


def svg():
    p = 11
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">']
    out.append(f'<rect width="{W}" height="{H}" fill="{BG}"/>')
    out.append(f'<text x="40" y="52" font-family="DejaVu Sans Mono" font-size="26" fill="{TXT}">a fold is an inversion — not a coincidence</text>')
    out.append(f'<text x="40" y="80" font-family="DejaVu Sans Mono" font-size="13" fill="{DIM}">the weave conjugates the meridians (bases 3,1,4,2). when two land in one torus the conjugator must normalize it,</text>')
    out.append(f'<text x="40" y="98" font-family="DejaVu Sans Mono" font-size="13" fill="{DIM}">and N(T) acts by identity or inversion. distinct meridians, so the fold is ALWAYS an inversion — one axis traversed both ways.</text>')

    # LEFT: the P^1(F_11) with the fold chord doubled, counter-directed
    cx, cy, R = 360, 440, 175
    out.append(f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="none" stroke="{DARK_EDGE}" stroke-width="1.4"/>')
    out.append(f'<text x="{cx}" y="{cy-R-38}" text-anchor="middle" font-family="DejaVu Sans Mono" '
               f'font-size="15" fill="{BRASS_EDGE}">p=11 · m=5 · conway</text>')
    out.append(f'<text x="{cx}" y="{cy-R-16}" text-anchor="middle" font-family="DejaVu Sans Mono" '
               f'font-size="11" fill="{MUTED}">the fold pair x1·x3 — one chord, both ways</text>')
    # spread chords
    out.append(chord(1, 4, p, cx, cy, R))
    out.append(chord(5, 6, p, cx, cy, R))
    # fold chord (5,9) doubled, counter-directed
    out.append(fold_chord(5, 9, p, cx, cy, R))
    # fixed points
    for k in range(p + 1):
        x, y = pt(k, p, cx, cy, R)
        out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="2.4" fill="{TXT}" fill-opacity="0.55"/>')
        out.append(f'<text x="{x:.1f}" y="{y-7:.1f}" text-anchor="middle" font-family="DejaVu Sans Mono" '
                   f'font-size="9" fill="{MUTED}">{k}</text>')
    # labels for the fold chord ends
    x5, y5 = pt(5, p, cx, cy, R)
    x9, y9 = pt(9, p, cx, cy, R)
    out.append(f'<text x="{x5-22:.1f}" y="{y5+4:.1f}" font-family="DejaVu Sans Mono" font-size="13" fill="{BRASS_EDGE}">x1</text>')
    out.append(f'<text x="{x9+12:.1f}" y="{y9+4:.1f}" font-family="DejaVu Sans Mono" font-size="13" fill="{ROSE}">x3</text>')
    out.append(f'<text x="{cx}" y="{cy+R+36}" text-anchor="middle" font-family="DejaVu Sans Mono" '
               f'font-size="12" fill="{DIM}">x1 and x3 share the axis (5,9)</text>')
    out.append(f'<text x="{cx}" y="{cy+R+54}" text-anchor="middle" font-family="DejaVu Sans Mono" '
               f'font-size="12" fill="{MUTED}">same two fixed points, opposite arrows: x3 = x1^-1</text>')

    # RIGHT: the weave cycle with the fold edge
    wcx, wcy = 1080, 430
    out.append(weave_cycle(wcx, wcy, (1, 3)))
    out.append(f'<text x="{wcx}" y="{wcy-224}" text-anchor="middle" font-family="DejaVu Sans Mono" '
               f'font-size="15" fill="{BRASS_EDGE}">the weave: x1→x3→x4→x2→x1</text>')
    out.append(f'<text x="{wcx}" y="{wcy-208}" text-anchor="middle" font-family="DejaVu Sans Mono" '
               f'font-size="11" fill="{MUTED}">every edge is a conjugator c_j</text>')
    # mechanism note
    out.append(f'<text x="{wcx}" y="{wcy+186}" text-anchor="middle" font-family="DejaVu Sans Mono" '
               f'font-size="12" fill="{DIM}">fixed point: x1 = c1 · x3 · c1⁻¹</text>')
    out.append(f'<text x="{wcx}" y="{wcy+204}" text-anchor="middle" font-family="DejaVu Sans Mono" '
               f'font-size="12" fill="{DIM}">x1, x3 in one torus T  ⇒  c1 ∈ N(T) = D₂ₘ</text>')
    out.append(f'<text x="{wcx}" y="{wcy+222}" text-anchor="middle" font-family="DejaVu Sans Mono" '
               f'font-size="12" fill="{BRASS_EDGE}">N(T) acts by inversion  ⇒  x3 = x1⁻¹</text>')

    # BOTTOM: the data strip
    y0 = 720
    out.append(f'<line x1="40" y1="{y0}" x2="{W-40}" y2="{y0}" stroke="{DARK_EDGE}" stroke-width="1"/>')
    out.append(f'<text x="40" y="{y0+30}" font-family="DejaVu Sans Mono" font-size="14" fill="{TXT}">fold count per rung — word-blind, and always an inversion</text>')
    out.append(f'<rect x="700" y="{y0+20}" width="13" height="10" fill="{BRASS}" stroke="{BRASS_EDGE}" stroke-width="1"/>')
    out.append(f'<text x="719" y="{y0+30}" font-family="DejaVu Sans Mono" font-size="11" fill="{DIM}">conway fold</text>')
    out.append(f'<rect x="846" y="{y0+20}" width="13" height="10" fill="{COPPER}" stroke="{COPPER_EDGE}" stroke-width="1"/>')
    out.append(f'<text x="865" y="{y0+30}" font-family="DejaVu Sans Mono" font-size="11" fill="{DIM}">kt fold</text>')
    rows = [
        (7,  3, 6,  6,  "x1·x3 / x3·x4 — both inverse"),
        (11, 5, 10, 10, "x1·x3 / x3·x4 — both inverse"),
        (13, 6, 0,  0,  "no fold; kt reaches nothing"),
        (17, 8, 0,  0,  "no fold; both spread"),
        (19, 9, 0,  0,  "no fold; both spread"),
    ]
    x = 40
    bw = 130
    for (pp, m, cf, kf, note) in rows:
        out.append(f'<text x="{x}" y="{y0+66}" font-family="DejaVu Sans Mono" font-size="14" fill="{TXT}">p={pp}</text>')
        out.append(f'<text x="{x}" y="{y0+84}" font-family="DejaVu Sans Mono" font-size="11" fill="{DIM}">m={m}</text>')
        bx = x + 52
        if cf or kf:
            out.append(f'<rect x="{bx}" y="{y0+52}" width="{bw*cf/10:.0f}" height="12" fill="{BRASS}" '
                       f'stroke="{BRASS_EDGE}" stroke-width="1" fill-opacity="0.85"/>')
            out.append(f'<rect x="{bx}" y="{y0+68}" width="{bw*kf/10:.0f}" height="12" fill="{COPPER}" '
                       f'stroke="{COPPER_EDGE}" stroke-width="1" fill-opacity="0.85"/>')
        else:
            out.append(f'<text x="{bx}" y="{y0+72}" font-family="DejaVu Sans Mono" font-size="11" fill="{MUTED}">—</text>')
        out.append(f'<text x="{bx}" y="{y0+98}" font-family="DejaVu Sans Mono" font-size="11" fill="{MUTED}">{note}</text>')
        x += 305
    out.append(f'<text x="40" y="{H-16}" font-family="DejaVu Sans Mono" font-size="12" fill="{MUTED}">verified: every fold pair is an inverse pair, on a weave-adjacent pair — 0 counterexamples at p=7,11,13,17,19.</text>')
    out.append('</svg>')
    return "\n".join(out)


if __name__ == "__main__":
    s = svg()
    open("assets/fold_inverse.svg", "w").write(s)
    cairosvg.svg2png(bytestring=s.encode(), write_to="assets/fold_inverse.png",
                     output_width=1600)
    print("wrote assets/fold_inverse.svg / .png")
