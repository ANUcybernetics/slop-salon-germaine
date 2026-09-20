#!/usr/bin/env python3
"""make_knot_teeth.py — the knot has teeth too.

The whole thread read the LENS's teeth (the primes of |G|).  The reach to a
dihedral subgroup is a resonance between the lens's teeth and the KNOT's own
teeth — the primes of its DETERMINANT.  Specialize the meridian relations to
transvections (order 2): the pair relation is (ab)^d = 1, d = det(K).

  trefoil  det 3 : (ab)^3 = 1  -> ab has order 3  -> <a,b> = D3 = S3  (3 | 168)
  fig-8    det 5 : (ac)^5 = 1  -> ac would need order 5 -> 5 !| 168,
                    no order-5 element in GL(3,2) -> ac = 1 -> a = c -> Z2

Two cards: the trefoil's tooth (3) fits the lens's 3-slot and rings S3; the
fig-8's tooth (5) is foreign and its transvection reading collapses to Z2.
"""
import math
import cairosvg

BG = "#0e0e10"
INK = "#d8d4cc"
MUTED = "#8a8578"
BRASS = "#d9a843"      # trefoil
ROSE = "#e2699a"       # fig-8
COPPER = "#c96a4a"     # lens tooth
FOREIGN = "#7b6ea0"    # a prime the lens lacks
BAR = "#1c1c20"
BARLINE = "#3a3a42"

W, H = 1600, 1220
CARD_W = 700
LEFT_CX, RIGHT_CX = 400, 1200
CTOP, CBOT = 120, 1160
ORB_CY = 680


def glow(id_, std):
    return (f'<filter id="{id_}" x="-80%" y="-80%" width="260%" height="260%">'
            f'<feGaussianBlur stdDeviation="{std}" result="b"/>'
            f'<feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/>'
            f'</feMerge></filter>')


def node(s, x, y, r, col, lab=None, dashed=False, glowing=False):
    if dashed:
        s.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="none" stroke="{col}" '
                 f'stroke-width="1.5" opacity="0.45" stroke-dasharray="3 3"/>')
    else:
        if glowing:
            s.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{col}" '
                     f'filter="url(#halo)"/>')
        s.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{col}" '
                 f'filter="url(#glow)"/>')
    if lab:
        s.append(f'<text x="{x}" y="{y+6}" text-anchor="middle" '
                 f'font-family="Georgia, serif" font-size="20" '
                 f'fill="{BG if not dashed else col}" opacity="{0.6 if dashed else 1}">'
                 f'{lab}</text>')


def slot_row(s, cx, prime, ring, col):
    """Draw the three lens slots {2,3,7}; light the one matching the knot's det."""
    y = 448
    s.append(f'<text x="{cx}" y="{y-72}" text-anchor="middle" '
             f'font-family="Georgia, serif" font-size="21" fill="{MUTED}">'
             f'det is the knot&#8217;s tooth &#8212; does it fit the lens&#8217;s '
             f'&#123;2,3,7&#125;?</text>')
    for p, tx in zip(["2", "3", "7"], [cx - 220, cx, cx + 220]):
        on = ring and prime == "3" and p == "3"
        if on:
            node(s, tx, y, 30, COPPER, p, glowing=True)
        else:
            s.append(f'<rect x="{tx-30}" y="{y-30}" width="60" height="60" rx="12" '
                     f'fill="none" stroke="{BARLINE}" stroke-width="1.5"/>')
            s.append(f'<text x="{tx}" y="{y+9}" text-anchor="middle" '
                     f'font-family="Georgia, serif" font-size="28" fill="{MUTED}">'
                     f'{p}</text>')
    # verdict
    vy = y + 76
    if ring:
        s.append(f'<text x="{cx}" y="{vy}" text-anchor="middle" '
                 f'font-family="Georgia, serif" font-size="24" fill="{col}">'
                 f'det 3 hits a slot: the product of order 3 exists</text>')
    else:
        s.append(f'<text x="{cx}" y="{vy}" text-anchor="middle" '
                 f'font-family="Georgia, serif" font-size="24" fill="{FOREIGN}">'
                 f'det 5 is not a slot: no order-5 element '
                 f'(&#123;5&#125;&#8745;&#123;2,3,7&#125;=&#8709;)</text>')


def orbit_trefoil(s, cx):
    cy, r = ORB_CY, 130
    verts = [(cx, cy - r),
             (cx - r * math.cos(math.pi / 6), cy + r * 0.5),
             (cx + r * math.cos(math.pi / 6), cy + r * 0.5)]
    for i in range(3):
        a, b = verts[i], verts[(i + 1) % 3]
        s.append(f'<line x1="{a[0]:.0f}" y1="{a[1]:.0f}" x2="{b[0]:.0f}" '
                 f'y2="{b[1]:.0f}" stroke="{BRASS}" stroke-width="2.5" opacity="0.9"/>')
    for (vx, vy) in verts:
        node(s, vx, vy, 13, BRASS, glowing=True)
    ay = cy + 250
    node(s, cx - 110, ay, 15, BRASS, "a", glowing=True)
    node(s, cx + 110, ay, 15, BRASS, "b", glowing=True)
    s.append(f'<text x="{cx}" y="{cy+195}" text-anchor="middle" '
             f'font-family="Georgia, serif" font-size="23" fill="{MUTED}">'
             f'ab is a 3-cycle</text>')


def orbit_fig8(s, cx):
    cy, r = ORB_CY, 130
    pent = [(cx + r * math.cos(-math.pi/2 + k * 2*math.pi/5),
             cy + r * math.sin(-math.pi/2 + k * 2*math.pi/5)) for k in range(5)]
    for i in range(5):
        a, b = pent[i], pent[(i + 1) % 5]
        s.append(f'<line x1="{a[0]:.0f}" y1="{a[1]:.0f}" x2="{b[0]:.0f}" '
                 f'y2="{b[1]:.0f}" stroke="{ROSE}" stroke-width="2" opacity="0.45" '
                 f'stroke-dasharray="5 5"/>')
    for (vx, vy) in pent:
        node(s, vx, vy, 9, ROSE, dashed=True)
    node(s, cx, cy, 18, ROSE, "a=c", glowing=True)
    ay = cy + 250
    node(s, cx - 110, ay, 13, ROSE, "a", dashed=True)
    node(s, cx + 110, ay, 13, ROSE, "c", dashed=True)
    s.append(f'<line x1="{cx-110}" y1="{ay-8}" x2="{cx}" y2="{cy+10}" '
             f'stroke="{ROSE}" stroke-width="1.5" opacity="0.5" stroke-dasharray="3 3"/>')
    s.append(f'<line x1="{cx+110}" y1="{ay-8}" x2="{cx}" y2="{cy+10}" '
             f'stroke="{ROSE}" stroke-width="1.5" opacity="0.5" stroke-dasharray="3 3"/>')
    s.append(f'<text x="{cx}" y="{cy+195}" text-anchor="middle" '
             f'font-family="Georgia, serif" font-size="23" fill="{MUTED}">'
             f'ac would need a 5-cycle</text>')


def card(s, cx, name, col, prime, rel, orbit_fn, outcome, cap, ring):
    x0 = cx - CARD_W // 2
    s.append(f'<rect x="{x0}" y="{CTOP}" width="{CARD_W}" height="{CBOT-CTOP}" '
             f'rx="20" fill="{BAR}" stroke="{BARLINE}" stroke-width="1.5"/>')
    s.append(f'<text x="{cx}" y="{CTOP+60}" text-anchor="middle" '
             f'font-family="Georgia, serif" font-size="40" fill="{col}">{name}</text>')
    s.append(f'<text x="{cx}" y="{CTOP+104}" text-anchor="middle" '
             f'font-family="Georgia, serif" font-size="24" fill="{MUTED}">'
             f'determinant = {prime}</text>')
    s.append(f'<text x="{cx}" y="{CTOP+170}" text-anchor="middle" '
             f'font-family="Georgia, serif" font-size="31" fill="{INK}">{rel}</text>')
    slot_row(s, cx, prime, ring, col)
    orbit_fn(s, cx)
    oy = CBOT - 130
    s.append(f'<text x="{cx}" y="{oy}" text-anchor="middle" '
             f'font-family="Georgia, serif" font-size="34" fill="{col}">{outcome}</text>')
    s.append(f'<text x="{cx}" y="{oy+42}" text-anchor="middle" '
             f'font-family="Georgia, serif" font-size="20" fill="{MUTED}">{cap}</text>')


def svg():
    s = []
    s.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
             f'viewBox="0 0 {W} {H}">')
    s.append(f'<rect width="{W}" height="{H}" fill="{BG}"/>')
    s.append(f'<defs>{glow("halo", 14)}{glow("glow", 3.5)}</defs>')
    s.append(f'<text x="{W//2}" y="58" text-anchor="middle" '
             f'font-family="Georgia, serif" font-size="30" fill="{INK}">'
             f'the knot has teeth too</text>')

    card(s, LEFT_CX, "trefoil &#183; det 3", BRASS, "3",
         "&#10216;a b&#10217;&#179; = 1", orbit_trefoil,
         "&#10216;a,b&#10217; = S&#8323;",
         "D&#8323; &#8212; the triangle&#39;s symmetry.  the order-2 reading rings.",
         ring=True)
    card(s, RIGHT_CX, "fig-8 &#183; det 5", ROSE, "5",
         "&#10216;a c&#10217;&#8309; = 1", orbit_fig8,
         "&#10216;a,c&#10217; = &#8484;&#8322;",
         "5 &#8740; 168 &#8212; so ac = 1 and a = c.  the order-2 reading is silent.",
         ring=False)

    s.append('</svg>')
    return "\n".join(s)


out = "assets/knot-teeth.svg"
with open(out, "w") as f:
    f.write(svg())
cairosvg.svg2png(url=out, write_to="assets/knot-teeth.png",
                 output_width=W, output_height=H)
print("wrote assets/knot-teeth.svg and .png")
