#!/usr/bin/env python3
"""make_doubling_a6.py — the doubling is |Out(A_n)|, not 2.

A₆ is the one room where Out(A₆)=Z/2×Z/2, so the '2×' the salon reads
(the outer automorphism doubling every lock into mirror hands) becomes 4×.
The A₆ onto set (11n34, class 4·2): 12 hands = 3 kernels × 4 (2 from the
odd-permutation mirror, 2 from the exotic outer automorphism).
"""
import math, os

# palette: glowing stroke-work on near-black (brass / copper / rose)
BG = "#0b0b10"
BRASS = "#d4af37"; BRASS_G = "#f6e39a"
COPPER = "#c87533"; COPPER_G = "#f0b07a"
ROSE  = "#d98a94"; ROSE_G  = "#f6c8d0"
DIM = "#3a3a46"

W, H = 1400, 920
svg = []
svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
           f'viewBox="0 0 {W} {H}">')
# defs: glow filter + radial background
svg.append('''<defs>
 <radialGradient id="bg" cx="50%" cy="45%" r="75%">
   <stop offset="0%" stop-color="#15151f"/><stop offset="100%" stop-color="#0b0b10"/>
 </radialGradient>
 <filter id="glow" x="-40%" y="-40%" width="180%" height="180%">
   <feGaussianBlur stdDeviation="6" result="b"/>
   <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
 </filter>
 <filter id="glow2" x="-60%" y="-60%" width="220%" height="220%">
   <feGaussianBlur stdDeviation="12" result="b"/>
   <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
 </filter>
</defs>''')
svg.append(f'<rect width="{W}" height="{H}" fill="url(#bg)"/>')

# ---------- LEFT: the A₆ flower (3 kernels x 4 hands) ----------
cx, cy = 430, 470
R = 300
# 12 hands = 3 kernels x 4. angles per kernel offset by 120deg, hands by 30deg.
def pt(r, ang):  # ang degrees
    a = math.radians(ang)
    return cx + r * math.cos(a), cy + r * math.sin(a)

kern_colors = [BRASS, COPPER, ROSE]
kern_glow   = [BRASS_G, COPPER_G, ROSE_G]
# concentric faint guides
for rr in (110, 190, 300):
    svg.append(f'<circle cx="{cx}" cy="{cy}" r="{rr}" fill="none" stroke="{DIM}" stroke-width="1" opacity="0.25"/>')

# 12 petals, 4 per kernel (2 mirror-pairs)
for k in range(3):
    base = k * 120
    col = kern_colors[k]; gl = kern_glow[k]
    for h in range(4):
        ang = base + h * 30
        # petal = tapered leaf from inner r=150 to outer r=300
        a0 = math.radians(ang - 9); a1 = math.radians(ang + 9)
        p_in  = (cx + 150*math.cos(a0), cy + 150*math.sin(a0))
        p_in2 = (cx + 150*math.cos(a1), cy + 150*math.sin(a1))
        p_out = (cx + 300*math.cos(a1), cy + 300*math.sin(a1))
        p_out2= (cx + 300*math.cos(a0), cy + 300*math.sin(a0))
        # 2 mirror-pairs within the kernel: shade the two hands of a pair slightly differently
        pairshade = h // 2
        stroke = col if pairshade == 0 else col
        op = 0.95 if pairshade == 0 else 0.75
        svg.append(f'<path d="M {p_in[0]:.1f} {p_in[1]:.1f} '
                   f'A 150 150 0 0 0 {p_in2[0]:.1f} {p_in2[1]:.1f} '
                   f'L {p_out[0]:.1f} {p_out[1]:.1f} '
                   f'A 300 300 0 0 1 {p_out2[0]:.1f} {p_out2[1]:.1f} Z" '
                   f'fill="none" stroke="{stroke}" stroke-width="3.5" opacity="{op}" '
                   f'filter="url(#glow)"/>')
        # node at petal tip
        tx, ty = pt(300, ang)
        svg.append(f'<circle cx="{tx:.1f}" cy="{ty:.1f}" r="5" fill="{gl}" filter="url(#glow2)"/>')
    # kernel ring arc (connects the 4 hands of this kernel)
    arc = f'M {pt(190, base)[0]:.1f} {pt(190, base)[1]:.1f} A 190 190 0 0 0 {pt(190, base+120)[0]:.1f} {pt(190, base+120)[1]:.1f}'
    svg.append(f'<path d="{arc}" fill="none" stroke="{col}" stroke-width="2" opacity="0.5" filter="url(#glow)"/>')
    # label the kernel
    lx, ly = pt(255, base + 60)
    svg.append(f'<text x="{lx:.1f}" y="{ly:.1f}" font-family="monospace" font-size="20" '
               f'fill="{gl}" text-anchor="middle" opacity="0.9">kern {k+1}</text>')

# center label
svg.append(f'<text x="{cx}" y="{cy-14}" font-family="monospace" font-size="26" '
           f'fill="#e8e8f0" text-anchor="middle">A₆  onto set</text>')
svg.append(f'<text x="{cx}" y="{cy+16}" font-family="monospace" font-size="18" '
           f'fill="#b8b8c4" text-anchor="middle">12 hands = 3 kernels × 4</text>')
svg.append(f'<text x="{cx}" y="{cy+40}" font-family="monospace" font-size="15" '
           f'fill="#8a8a96" text-anchor="middle">odd-perm mirror × exotic mirror</text>')

# ---------- RIGHT: the doubling ladder A₅..A₉ ----------
lx = 1050
svg.append(f'<text x="{lx}" y="120" font-family="monospace" font-size="24" '
           f'fill="#e8e8f0" text-anchor="middle">the doubling is |Out(Aₙ)|</text>')
rooms = ["A₅","A₆","A₇","A₈","A₉"]
out   = [2, 4, 2, 2, 2]
y0 = 210; step = 130
for i, r in enumerate(rooms):
    y = y0 + i * step
    fac = out[i]
    hot = (fac == 4)
    col = ROSE if hot else BRASS
    gl  = ROSE_G if hot else BRASS_G
    # rung line
    half = 60 + fac * 28
    svg.append(f'<line x1="{lx-half}" y1="{y}" x2="{lx+half}" y2="{y}" '
               f'stroke="{col}" stroke-width="{6 if hot else 3}" filter="url(#glow)"/>')
    # node
    svg.append(f'<circle cx="{lx}" cy="{y}" r="{10 if hot else 6}" fill="{gl}" filter="url(#glow2)"/>')
    svg.append(f'<text x="{lx-half-18}" y="{y+6}" font-family="monospace" font-size="22" '
               f'fill="{gl}" text-anchor="end">{r}</text>')
    svg.append(f'<text x="{lx+half+18}" y="{y+6}" font-family="monospace" font-size="22" '
               f'fill="{gl}" text-anchor="start">×{fac}</text>')
    svg.append(f'<text x="{lx}" y="{y-14}" font-family="monospace" font-size="14" '
               f'fill="#8a8a96" text-anchor="middle">{"Out = Z/2 × Z/2" if hot else "Out = Z/2"}</text>')
# caption
svg.append(f'<text x="{lx}" y="{y0+5*step+20}" font-family="monospace" font-size="15" '
           f'fill="#b8b8c4" text-anchor="middle">A₆ is the one room the "×2" breaks.</text>')

svg.append('</svg>')
os.makedirs("assets", exist_ok=True)
open("assets/a6_doubling.svg","w").write("\n".join(svg))
import cairosvg
cairosvg.svg2png(url="assets/a6_doubling.svg", write_to="assets/a6_doubling.png",
                 output_width=1400, output_height=920)
print("wrote assets/a6_doubling.png")
