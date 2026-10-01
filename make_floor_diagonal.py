#!/usr/bin/env python3
"""make_floor_diagonal.py — the floor is the diagonal, not "Klein four is normal".

A hom of the knot group is ON the floor iff its image is abelian, and for the
braid-closure presentation every abelian image is the DIAGONAL x1=...=x4 — the
hom factors through H1=Z. There are always exactly |G| of them.

  A4: the fixed set of b-hat is EXACTLY the diagonal (x1=...=x4), so every image
      is cyclic. No non-abelian hom, no door. |Hom|=12 = |A4|, all on the floor.
  A5: the fixed set breaks the diagonal. 180 = 60 (diagonal/floor) + 120 (onto).
      The onto key is FOUR 3-CYCLES rising off the floor into the room.

rahel read the floor as "A4 is not simple (Klein four is normal), so no door."
It is not that. A4 is the first rung the knot cannot see NON-ABELIAN-ly: the
braid's automorphism has only diagonal fixed points there.

Renders the floor as a glowing line; the diagonal sits on it; at A5 four
3-cycles lift off the line into a pentagon room.
"""
import math, cairosvg

BG="#0a0a0d"; BRASS="#c9a227"; COPPER="#e0a850"; ROSE="#d98a6a"
DIM="#2c3e50"; FAINT="#6f6656"; INK="#e8e0cc"; SUB="#9a8f78"; PALE="#f2d27a"

def pentagon(cx,cy,r,rot=-90):
    return [(cx+r*math.cos(math.radians(rot+72*i)), cy+r*math.sin(math.radians(rot+72*i))) for i in range(5)]

def glow(tag,body,color,width=2.0,fill="none"):
    return "\n".join(f"<{tag} {body} stroke='{color}' stroke-width='{w:.2f}' opacity='{op}' fill='{fill}' stroke-linejoin='round' stroke-linecap='round'/>"
                     for w,op in ((width*5,0.06),(width*2.5,0.15),(width*1.2,0.45),(width,0.9)))

def glow_poly(pts,color,width=2.0,closed=True,fill="none"):
    body=f"{'points' if True else 'points'}='{' '.join(f'{x:.1f},{y:.1f}' for x,y in pts)}'"
    return glow("polygon" if closed else "polyline", body, color, width, fill)

def glow_pts(points,color,width=2.0):
    return glow("polyline", "points='%s'"%(" ".join(f"{x:.1f},{y:.1f}" for x,y in points)), color, width)

def text(x,y,size,fill,s,anchor="middle",weight="normal"):
    return (f"<text x='{x}' y='{y}' text-anchor='{anchor}' fill='{fill}' font-family='serif' font-size='{size}' font-weight='{weight}'>{s}</text>")

def dot(x,y,color,r=5):
    return f"<circle cx='{x:.1f}' cy='{y:.1f}' r='{r}' fill='{color}'/>"

def knot_glyph(cx,cy,r,color):
    """A small closed-braid icon: a ring with four strands weaving (schematic)."""
    s=[]
    # ring
    s.append(glow_poly([(cx+r*math.cos(t), cy+r*math.sin(t)) for t in [i*2*math.pi/48 for i in range(48)]], color, 1.6, closed=True))
    # four strands crossing the ring vertically (schematic closure)
    for dx in (-r*0.55, -r*0.18, r*0.18, r*0.55):
        s.append(glow_pts([(cx+dx, cy-r*0.95),(cx-dx*0.4, cy),(cx+dx*0.9, cy+r*0.95)], color, 1.5))
    return "\n".join(s)

def build_svg():
    W,H=1560,980
    FLOOR=590
    parts=[f"<svg xmlns='http://www.w3.org/2000/svg' width='{W}' height='{H}' viewBox='0 0 {W} {H}'>"]
    parts.append(f"<rect width='{W}' height='{H}' fill='{BG}'/>")
    parts.append(text(W/2,56,34,INK,"the floor is the diagonal"))
    parts.append(text(W/2,90,15,SUB,"a hom is on the floor iff its image is abelian — for a knot's braid closure that is x₁=x₂=x₃=x₄, factoring through H₁=Z, always exactly |G| of them"))
    # floor
    parts.append(f"<line x1='90' y1='{FLOOR}' x2='{W-90}' y2='{FLOOR}' stroke='#1a2430' stroke-width='3'/>")
    parts.append(glow_pts([(110,FLOOR),(W-110,FLOOR)],BRASS,1.6))
    parts.append(text(W/2,FLOOR+36,15,SUB,"the abelianization floor — the diagonal, every image cyclic, count = |G|   (both knots, both mutants)"))

    # ---------------- A4 ----------------
    cx4=430
    parts.append(text(cx4,150,26,INK,"A₄"))
    parts.append(text(cx4,176,13,SUB,"|Hom| = 12 — all on the floor"))
    parts.append(knot_glyph(cx4,250,44,COPPER))
    # the room: dim pentagon, and the diagonal = one point on the floor
    room=pentagon(cx4,FLOOR-160,72)
    parts.append(glow_poly(room,DIM,1.5,closed=True))
    parts.append(text(cx4,FLOOR-160,15,FAINT,"no room"))
    # four faint strands converging to one floor point (the diagonal)
    for dx in (-56,-19,19,56):
        parts.append(glow_pts([(cx4+dx,FLOOR-160),(cx4,FLOOR)],COPPER,1.2))
    parts.append(dot(cx4,FLOOR,COPPER,7.5))
    parts.append(text(cx4,FLOOR+86,16,INK,"floor 12"))
    parts.append(text(cx4,FLOOR+108,13,SUB,"x₁=x₂=x₃=x₄ — every image cyclic"))
    parts.append(text(cx4,FLOOR+136,13,FAINT,"every hom is diagonal — onto = 0"))

    # ---------------- A5 ----------------
    cx5=1120
    parts.append(text(cx5,150,26,INK,"A₅"))
    parts.append(text(cx5,176,13,SUB,"|Hom| = 180 = 60 floor + 120 rise"))
    parts.append(knot_glyph(cx5,250,44,BRASS))
    # the room rises above the floor
    pcx,pcy,pr=cx5,FLOOR-170,74
    room5=pentagon(pcx,pcy,pr)
    parts.append(glow_poly(room5,BRASS,2.2,closed=True))
    star=[room5[0],room5[2],room5[4],room5[1],room5[3],room5[0]]
    parts.append(glow_pts(star,BRASS,1.7))
    for (x,y) in room5: parts.append(dot(x,y,BRASS,4))
    parts.append(text(pcx,pcy-pr-16,15,BRASS,"the room — 120 onto"))
    # four floor points, and four 3-cycles rising into the room
    floor_xs=[cx5-108,cx5-36,cx5+36,cx5+108]
    verts=[room5[1],room5[2],room5[3],room5[4]]
    for (fx,(vx,vy)) in zip(floor_xs,verts):
        parts.append(glow_pts([(fx,FLOOR),(vx,vy)],ROSE,1.6))
        parts.append(dot(fx,FLOOR,ROSE,4.5))
        parts.append(text(cx5,FLOOR+86,16,INK,"floor 60 + rise 120"))
    parts.append(text(cx5,FLOOR+108,13,SUB,"the diagonal breaks — four 3-cycles"))
    parts.append(text(cx5,FLOOR+136,13,FAINT,"the key rises off the floor into the room"))

    # ---------------- strip ----------------
    vy=900
    parts.append(f"<line x1='90' y1='{vy-30}' x2='{W-90}' y2='{vy-30}' stroke='{FAINT}' stroke-width='1'/>")
    parts.append(text(W/2,vy-4,17,"#cfc4ae","A₄: the fixed set of β̂ is exactly the diagonal — every image is cyclic, onto = 0"))
    parts.append(text(W/2,vy+22,15,SUB,"A₅: 180 = 60 (diagonal) + 120 (onto) — the onto key is four 3-cycles, both mutants agree"))
    parts.append("</svg>")
    return "\n".join(parts)

if __name__=="__main__":
    import os; os.makedirs("assets",exist_ok=True)
    svg=build_svg()
    open("assets/floor_diagonal.svg","w").write(svg)
    cairosvg.svg2png(url="assets/floor_diagonal.svg",write_to="assets/floor_diagonal.png",output_width=1700)
    print("wrote assets/floor_diagonal.svg and .png")
