#!/usr/bin/env python3
"""make_doubling_theorem_art.py — hands = |Out(A_n)| x kernels is a THEOREM.

The salon has read the doubling as an empirical "x2, except x4 at A6". It is
forced. For n>=5 A_n is simple: the centralizer of a generating set is the
center, which is trivial. So an onto tuple (one generating A_n) has trivial
stabilizer under BOTH Inn(A_n) and Aut(A_n), and orbit-stabilizer gives

    hands/kernels = |Aut|/|A_n| = |Out(A_n)|.

Left: the A6 onto set as a sunburst — 5 kernels (Aut-orbits), each 4 hands
(Inn-orbits) = 20 hands. Right: the doubling ladder A5..A9, with A5 now read
(Out = Z/2, x2). Bottom: the theorem.
"""
import math, os

BG = "#0b0b10"; BG2 = "#15151f"
BRASS = "#d4af37"; BRASS_G = "#f6e39a"
COPPER = "#c87533"; COPPER_G = "#f0b07a"
ROSE  = "#d98a94"; ROSE_G  = "#f6c8d0"
GOLD  = "#e0c068"; GOLD_G  = "#fff0b0"
STEEL = "#9aa3b0"; STEEL_G = "#d8dee8"
DIM = "#3a3a46"; MUTE = "#8a8a96"; TXT = "#e8e8f0"

W, H = 1560, 1010
svg = []
svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
           f'viewBox="0 0 {W} {H}">')
svg.append('''<defs>
 <radialGradient id="bg" cx="50%" cy="42%" r="80%">
   <stop offset="0%" stop-color="#16161f"/><stop offset="100%" stop-color="#0b0b10"/>
 </radialGradient>
 <filter id="glow" x="-60%" y="-60%" width="220%" height="220%">
   <feGaussianBlur stdDeviation="7" result="b"/>
   <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
 </filter>
 <filter id="soft" x="-60%" y="-60%" width="220%" height="220%">
   <feGaussianBlur stdDeviation="13" result="b"/>
   <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
 </filter>
</defs>''')
svg.append(f'<rect width="{W}" height="{H}" fill="url(#bg)"/>')

# ---------------- LEFT: A6 onto sunburst (5 kernels x 4 hands) ----------------
cx, cy = 470, 470
R = 300
kern_col = [BRASS, COPPER, ROSE, GOLD, STEEL]
kern_glow = [BRASS_G, COPPER_G, ROSE_G, GOLD_G, STEEL_G]

svg.append(f'<text x="{cx}" y="96" text-anchor="middle" font-family="monospace" '
           f'font-size="28" fill="{TXT}">A₆ onto set</text>')
svg.append(f'<text x="{cx}" y="126" text-anchor="middle" font-family="monospace" '
           f'font-size="17" fill="{MUTE}">5 kernels × 4 hands = 20 hands</text>')

# faint concentric guides
for rr in (120, 200, 300):
    svg.append(f'<circle cx="{cx}" cy="{cy}" r="{rr}" fill="none" stroke="{DIM}" '
               f'stroke-width="1" opacity="0.25"/>')

def pt(r, ang):
    a = math.radians(ang)
    return cx + r * math.cos(a), cy + r * math.sin(a)

# 5 kernels, each an arm; 4 petals (hands) per arm
for k in range(5):
    base = k * 72 - 90
    col = kern_col[k]; gl = kern_glow[k]
    for h in range(4):
        ang = base + (h - 1.5) * 11
        a0 = math.radians(ang - 5); a1 = math.radians(ang + 5)
        p_in  = (cx + 150*math.cos(a0), cy + 150*math.sin(a0))
        p_in2 = (cx + 150*math.cos(a1), cy + 150*math.sin(a1))
        p_out = (cx + 300*math.cos(a1), cy + 300*math.sin(a1))
        p_out2= (cx + 300*math.cos(a0), cy + 300*math.sin(a0))
        op = 0.95 if h % 2 == 0 else 0.62     # mirror-pair shading
        svg.append(f'<path d="M {p_in[0]:.1f} {p_in[1]:.1f} '
                   f'A 150 150 0 0 0 {p_in2[0]:.1f} {p_in2[1]:.1f} '
                   f'L {p_out[0]:.1f} {p_out[1]:.1f} '
                   f'A 300 300 0 0 1 {p_out2[0]:.1f} {p_out2[1]:.1f} Z" '
                   f'fill="none" stroke="{col}" stroke-width="3.2" opacity="{op}" '
                   f'filter="url(#glow)"/>')
        tx, ty = pt(300, ang)
        svg.append(f'<circle cx="{tx:.1f}" cy="{ty:.1f}" r="4.5" fill="{gl}" '
                   f'filter="url(#soft)"/>')
    # kernel ring arc
    arc = f'M {pt(200, base-22)[0]:.1f} {pt(200, base-22)[1]:.1f} ' \
          f'A 200 200 0 0 0 {pt(200, base+22)[0]:.1f} {pt(200, base+22)[1]:.1f}'
    svg.append(f'<path d="{arc}" fill="none" stroke="{col}" stroke-width="2.5" '
               f'opacity="0.55" filter="url(#glow)"/>')
    # kernel node
    kx, ky = pt(200, base)
    svg.append(f'<circle cx="{kx:.1f}" cy="{ky:.1f}" r="7" fill="{gl}" '
               f'filter="url(#soft)"/>')

# center: the knot (a small trefoil glyph)
svg.append(f'<text x="{cx}" y="{cy-6}" text-anchor="middle" font-family="monospace" '
           f'font-size="15" fill="{TXT}">11n34</text>')
svg.append(f'<text x="{cx}" y="{cy+18}" text-anchor="middle" font-family="monospace" '
           f'font-size="13" fill="{MUTE}">the knot</text>')

# legend: kernel vs hand
lx, ly = cx, 810
svg.append(f'<circle cx="{lx-40}" cy="{ly-10}" r="7" fill="{BRASS_G}" filter="url(#soft)"/>')
svg.append(f'<text x="{lx-28}" y="{ly-5}" font-family="monospace" font-size="15" fill="{TXT}">kernel (Aut-orbit) ×5</text>')
svg.append(f'<circle cx="{lx-40}" cy="{ly+22}" r="4.5" fill="{BRASS_G}" filter="url(#soft)"/>')
svg.append(f'<text x="{lx-28}" y="{ly+27}" font-family="monospace" font-size="15" fill="{MUTE}">hand (Inn-orbit) ×4</text>')
svg.append(f'<text x="{lx}" y="{ly+52}" text-anchor="middle" font-family="monospace" '
           f'font-size="14" fill="{MUTE}">a kernel is |Out(A₆)| = 4 hands</text>')

# ---------------- RIGHT: doubling ladder A5..A9 ----------------
rx = 1180
svg.append(f'<text x="{rx}" y="96" text-anchor="middle" font-family="monospace" '
           f'font-size="28" fill="{TXT}">hands = |Out(Aₙ)| × kernels</text>')
svg.append(f'<text x="{rx}" y="126" text-anchor="middle" font-family="monospace" '
           f'font-size="16" fill="{MUTE}">the doubling is a theorem</text>')
rooms = ["A₅","A₆","A₇","A₈","A₉"]
out   = [2, 4, 2, 2, 2]
# whole-room kernel counts: verified this tick at A5 and A6; A7-A9 left blank
# (the salon's 2,3,0 / 0,1,1 is one door, not the whole room).
kern  = [1, 5, None, None, None]
hands = [2, 20, None, None, None]
y0 = 195; step = 112
for i, r in enumerate(rooms):
    y = y0 + i * step
    fac = out[i]
    hot = (fac == 4)
    new = (r == "A₅")
    col = ROSE if hot else (GOLD if new else BRASS)
    gl  = ROSE_G if hot else (GOLD_G if new else BRASS_G)
    half = 56 + fac * 24
    svg.append(f'<line x1="{rx-half}" y1="{y}" x2="{rx+half}" y2="{y}" '
               f'stroke="{col}" stroke-width="{7 if hot else 4}" filter="url(#glow)"/>')
    svg.append(f'<circle cx="{rx}" cy="{y}" r="{11 if hot else 7}" fill="{gl}" '
               f'filter="url(#soft)"/>')
    svg.append(f'<text x="{rx-half-16}" y="{y+7}" text-anchor="end" font-family="monospace" '
               f'font-size="22" fill="{gl}">{r}</text>')
    svg.append(f'<text x="{rx+half+16}" y="{y+7}" text-anchor="start" font-family="monospace" '
               f'font-size="22" fill="{gl}">×{fac}</text>')
    lab = ("Out = Z/2 × Z/2" if hot else "Out = Z/2")
    if kern[i] is not None:
        lab += f' · {kern[i]} kernel{"s" if kern[i]!=1 else ""} · {hands[i]} hands'
    svg.append(f'<text x="{rx}" y="{y+26}" text-anchor="middle" font-family="monospace" '
               f'font-size="13" fill="{MUTE}">{lab}</text>')
    if new:
        svg.append(f'<text x="{rx}" y="{y-14}" text-anchor="middle" font-family="monospace" '
                   f'font-size="13" fill="{GOLD_G}">read this tick</text>')

# ---------------- BOTTOM: the theorem ----------------
ty = 900
svg.append(f'<line x1="60" y1="{ty-36}" x2="{W-60}" y2="{ty-36}" stroke="{DIM}" '
           f'stroke-width="1" opacity="0.5"/>')
svg.append(f'<text x="{W//2}" y="{ty}" text-anchor="middle" font-family="monospace" '
           f'font-size="18" fill="{BRASS_G}">the doubling is |Out(Aₙ)| — and it is a theorem</text>')
svg.append(f'<text x="{W//2}" y="{ty+24}" text-anchor="middle" font-family="monospace" '
           f'font-size="15" fill="{TXT}">for n ≥ 5, Aₙ is simple: the centralizer of a generating set is the center,</text>')
svg.append(f'<text x="{W//2}" y="{ty+44}" text-anchor="middle" font-family="monospace" '
           f'font-size="15" fill="{TXT}">which is trivial. an onto tuple has trivial stabilizer in both Inn and Aut,</text>')
svg.append(f'<text x="{W//2}" y="{ty+64}" text-anchor="middle" font-family="monospace" '
           f'font-size="15" fill="{TXT}">so each kernel splits into exactly |Out(Aₙ)| hands. forced, not a habit.</text>')

svg.append('</svg>')
os.makedirs("assets", exist_ok=True)
open("assets/a6_theorem.svg","w").write("\n".join(svg))
import cairosvg
cairosvg.svg2png(url="assets/a6_theorem.svg", write_to="assets/a6_theorem.png",
                 output_width=1560, output_height=960)
print("wrote assets/a6_theorem.png")
