#!/usr/bin/env python3
"""make_entangled.py — the weave is a fingerprint: same route, same framing,
the conjugators differ.

The fixed-point equations for a hom pi_1(K) -> A_9 are

    beta_hat(x_j) = gamma_j x_{pi(j)} gamma_j^-1 = x_j

The Artin automorphism beta_hat routes the generators by the braid permutation.
For BOTH mutants that route is the SAME 4-cycle  x1 -> x3 -> x4 -> x2 -> x1
(braid perm (0 2 3 1)).  The writhe is the same (-1).  The only thing that can
differ is the CONJUGATOR gamma_j — the weave, the conjugation sequence along the
braid.  This piece draws that cycle for each word, with each arrow carrying its
gamma_j (the generators it conjugates by, net count).

The generators are ENTANGLED: gamma_3 and gamma_4 contain x_4, so x_3 and x_4
feed back into each other's conjugators.  That is why the fixed points cannot be
solved one at a time — for a fixed (x1,x2) exactly one (x3,x4) is beta_hat-fixed,
but finding it needs the whole coupled system, not a conjugation chain.
"""
import math
import os
import cairosvg

import make_perm_map as mp

BG = "#0b0b10"
BRASS = "#c9a24b"
COPPER = "#c6703b"
ROSE = "#c65a72"
GOLD = "#e0c27a"
SERIF = "DejaVu Serif, serif"
MUTE = "#7d7868"
DIM = "#5c574b"

CONWAY = [(1, -1), (2, 1), (1, -1), (2, 1), (1, -1), (3, 1),
          (2, -1), (2, -1), (1, -1), (3, 1), (3, 1)]
KT = [(1, -1), (2, 1), (2, 1), (3, -1), (3, -1), (2, 1), (1, 1),
      (2, -1), (2, -1), (3, 1), (2, -1), (3, 1), (2, -1)]


def text(x, y, size, fill, s, extra=""):
    return (f'<text x="{x}" y="{y}" font-family="{SERIF}" font-size="{size}" '
            f'fill="{fill}" {extra}>{s}</text>')


def sub2(n):
    return "₀₁₂₃₄₅₆₇₈₉"[n]


def netstr(net):
    if not net:
        return "γ = 1"
    parts = []
    for x in sorted(net):
        v = net[x]
        if v == 1:
            parts.append(f"x{sub2(x)}")
        elif v == -1:
            parts.append(f"x{sub2(x)}⁻¹")
        else:
            parts.append(f"x{sub2(x)}{'^%d' % v if v != 2 else '²'}")
    return "γ = " + " ".join(parts)


def cycle_panel(cx, cy, R, color, nets):
    """Draw the 4-cycle x1->x3->x4->x2->x1 with gamma_j on each arrow."""
    out = []
    # nodes around the circle in cycle order: x1, x3, x4, x2 (positions of the cycle)
    nodes = [(1, (0, 1)), (3, (2, 1)), (4, (3, 1)), (2, (1, 1))]
    # place at angles starting from top, going clockwise
    angs = [-90, 0, 90, 180]
    pts = {}
    for (x, _), ang in zip(nodes, angs):
        a = math.radians(ang)
        pts[x] = (cx + R * math.cos(a), cy + R * math.sin(a))
    # cycle arrows: x_j -> x_{pi(j)};  the cycle is 1->3->4->2->1
    # arrow from x1 to x3 carries gamma1, x3->x4 carries gamma3,
    # x4->x2 carries gamma4, x2->x1 carries gamma2.
    seq = [(1, 3), (3, 4), (4, 2), (2, 1)]
    gmap = {1: "γ₁", 3: "γ₃", 4: "γ₄", 2: "γ₂"}
    for (a_, b_) in seq:
        x0, y0 = pts[a_]; x1_, y1_ = pts[b_]
        # curve the arrow outward (arc through the circle)
        mx, my = (x0 + x1_) / 2, (y0 + y1_) / 2
        # push outward from centre
        vx, vy = mx - cx, my - cy
        L = math.hypot(vx, vy) or 1
        mx, my = mx + vx / L * 26, my + vy / L * 26
        d = f'M {x0:.1f},{y0:.1f} Q {mx:.1f},{my:.1f} {x1_:.1f},{y1_:.1f}'
        out.append(f'<path d="{d}" fill="none" stroke="{color}" stroke-width="2" '
                   f'opacity="0.7" marker-end="url(#arr)"/>')
        # gamma label just outside the arc
        lx = cx + (mx - cx) * 1.32
        ly = cy + (my - cy) * 1.32
        out.append(text(lx, ly, 15, color, gmap[a_], 'text-anchor="middle"'))
        # net content just inside
        nx = cx + (mx - cx) * 0.78
        ny = cy + (my - cy) * 0.78
        out.append(text(nx, ny, 12, "#cfc4ae", netstr(nets[a_]), 'text-anchor="middle"'))
    # node dots + labels
    for x in pts:
        px, py = pts[x]
        out.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="7" fill="{color}" opacity="0.95"/>')
        lx, ly = pts[x]
        out.append(text(px, py - 13, 16, "#f0e6d0", f"x{sub2(x)}", 'text-anchor="middle"'))
    out.append(text(cx, cy, 13, DIM, "β̂(x_j) = γ_j x_{π(j)} γ_j⁻¹", 'text-anchor="middle"'))
    return out


def build():
    W, H = 1760, 1240
    p = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
         f'viewBox="0 0 {W} {H}">']
    p.append(f'<defs><marker id="arr" markerWidth="9" markerHeight="9" refX="7" '
             f'refY="3" orient="auto"><path d="M0,0 L7,3 L0,6 z" fill="#8f8872"/>'
             f'</marker></defs>')
    p.append(f'<rect width="{W}" height="{H}" fill="{BG}"/>')
    p.append(text(W / 2, 58, 32, "#cfc4ae",
                  "the weave is a fingerprint: same route, same framing, the γ differ",
                  'text-anchor="middle" letter-spacing="1"'))
    p.append(text(W / 2, 92, 16, DIM,
                  "both words: braid perm (0 2 3 1)  ·  writhe −1  ·  base flow "
                  "x₁→x₃→x₄→x₂→x₁", 'text-anchor="middle"'))
    p.append(text(W / 2, 116, 16, DIM,
                  "the conjugators γⱼ (the weave) are the only thing that differs — "
                  "and they entangle x₃, x₄", 'text-anchor="middle"'))

    cxL, cxR = 460, 1300
    # braid closures (same route) — reuse the perm-map renderer
    for cx, (key, word, col) in ((cxL, ("Conway", CONWAY, BRASS)),
                                 (cxR, ("KT", KT, ROSE))):
        p.extend(mp.render_panel(f"{key}  11n34" if key == "Conway" else "KT  11n42",
                                 word, cx, 340, f"{key}  11n34" if key == "Conway" else "KT  11n42",
                                 "perm (0 2 3 1)", labelx=cx - 60))

    # the cycle panels
    conway_nets = {1: {4: -1}, 2: {3: -1}, 3: {2: 2, 3: -1}, 4: {3: -1, 4: 1}}
    kt_nets = {1: {1: 2, 2: 1, 4: -1}, 2: {2: -1, 3: 1}, 3: {3: -1}, 4: {1: -1, 4: -1}}
    p.append(text(cxL, 520, 18, BRASS, "Conway", 'text-anchor="middle"'))
    p.extend(cycle_panel(cxL, 800, 250, BRASS, conway_nets))
    p.append(text(cxR, 520, 18, ROSE, "KT", 'text-anchor="middle"'))
    p.extend(cycle_panel(cxR, 800, 250, ROSE, kt_nets))

    # footnotes
    p.append(text(W / 2, 1150, 17, "#cfc4ae",
                  "the cycle of conjugations is the same on both; the γ on each arrow is the weave.",
                  'text-anchor="middle"'))
    p.append(text(W / 2, 1180, 15, DIM,
                  "γ₃ carries x₃ and γ₄ carries x₄ — the x₃, x₄ equations are self-referential, "
                  "so the weave couples them (a fixed (x₁,x₂) fixes exactly one (x₃,x₄), but not as a chain).",
                  'text-anchor="middle"'))
    p.append(text(W / 2, 1212, 14, MUTE,
                  "A₉ by class: 3³ open for KT (181440), closed for Conway; 3²·1³ open for both; "
                  "3·1⁶ closed for both.",
                  'text-anchor="middle"'))

    p.append("</svg>")
    return "\n".join(p)


def main():
    svg = build()
    base = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(base, "assets", "entangled.svg"), "w") as f:
        f.write(svg)
    png = os.path.join(base, "assets", "entangled.png")
    cairosvg.svg2png(url=os.path.join(base, "assets", "entangled.svg"),
                     write_to=png, output_width=1760, output_height=1240)
    print("wrote", png)


if __name__ == "__main__":
    main()
