#!/usr/bin/env python3
"""make_floor_shards.py — the floor is SEVEN shards, not one shadow.

mina's A6 ledger: |Hom(pi,A6)| = 9000 = 360 x 25, "25 = 1 floor + 20 onto A6
+ 4 onto A5."  The arithmetic is right.  But the floor is not one object: the
diagonal (x1=...=x4) is a SET of |A6|=360 tuples, and two diagonal tuples
(g,g,g,g),(h,h,h,h) are conjugate iff g,h are conjugate, so the floor splits
into ONE ORBIT PER CONJUGACY CLASS.  At A6 that is seven shards, sizes
{1,45,40,40,90,72,72}.  These shards are exactly the non-free orbits — the
floor is where conjugation sticks; the room is where it is free.

Ledger (both mutants, identical at A6):
    7 floor shards   = 360  (non-free, cyclic images 1,2,3,3,4,5,5)
   24 free hands     = 8640 (20 onto A6: meridian order 4 x12, order 5 x8;
                           4 onto A5: meridian order 3)
   TOTAL             = 9000 = 360 x 25.  31 orbits, not 25.
"""
import math, cairosvg

BG="#0a0a0d"; BRASS="#c9a227"; COPPER="#e0a850"; ROSE="#d98a6a"
DIM="#2c3e50"; FAINT="#6f6656"; INK="#e8e0cc"; SUB="#9a8f78"; PALE="#f2d27a"

# A6 conjugacy classes: (element order, class size)
CLASSES = [(1,1),(2,45),(3,40),(3,40),(4,90),(5,72),(5,72)]
# hands: (how many, meridian order, image)
HANDS = [(12,4,"A6"),(8,5,"A6"),(4,3,"A5")]

def glow(tag,body,color,width=2.0,fill="none"):
    return "\n".join(f"<{tag} {body} stroke='{color}' stroke-width='{w:.2f}' opacity='{op}' fill='{fill}' stroke-linejoin='round' stroke-linecap='round'/>"
                     for w,op in ((width*5,0.06),(width*2.5,0.15),(width*1.2,0.45),(width,0.9)))

def glow_pts(points,color,width=2.0):
    return glow("polyline","points='%s'"%(" ".join(f"{x:.1f},{y:.1f}" for x,y in points)),color,width)

def text(x,y,size,fill,s,anchor="middle",weight="normal"):
    return (f"<text x='{x}' y='{y}' text-anchor='{anchor}' fill='{fill}' font-family='serif' font-size='{size}' font-weight='{weight}'>{s}</text>")

def dot(x,y,color,r,op=1.0):
    return f"<circle cx='{x:.1f}' cy='{y:.1f}' r='{r:.1f}' fill='{color}' opacity='{op}'/>"

def build_svg():
    W,H=1560,1040
    FLOOR=760
    parts=[f"<svg xmlns='http://www.w3.org/2000/svg' width='{W}' height='{H}' viewBox='0 0 {W} {H}'>"]
    parts.append(f"<rect width='{W}' height='{H}' fill='{BG}'/>")
    parts.append(text(W/2,60,36,INK,"the floor is seven shards"))
    parts.append(text(W/2,96,15,SUB,"|Hom(π, A₆)| = 9000 = 360 × 25 — the ledger adds up. but the floor is not one shadow: the diagonal splits into"))
    parts.append(text(W/2,116,15,SUB,"one orbit per conjugacy class. at A₆ that is seven shards, and they are exactly the NON-FREE orbits."))

    # ---------- the room: A6 chamber ----------
    left,right=150,W-150
    top=190
    parts.append(f"<rect x='{left}' y='{top}' width='{right-left}' height='{FLOOR-top}' fill='none' stroke='#1a2430' stroke-width='2'/>")
    parts.append(text((left+right)/2,top-18,15,FAINT,"the sixth room — A₆ (360)"))
    parts.append(glow_pts([(left+30,FLOOR),(right-30,FLOOR)],BRASS,1.7))
    parts.append(text((left+right)/2,FLOOR+34,15,SUB,"the abelianization floor — the diagonal, x₁=…=x₄"))

    # ---------- A5 ledge ----------
    A5Y=410
    parts.append(f"<line x1='{left+40}' y1='{A5Y}' x2='{right-40}' y2='{A5Y}' stroke='{ROSE}' stroke-width='1' opacity='0.30' stroke-dasharray='4 6'/>")

    # ---------- 7 floor shards ----------
    sx=[205,380,505,630,850,1055,1200]
    colors=[BRASS,COPPER,COPPER,BRASS,COPPER,PALE,PALE]
    for (ord_,size),x,c in zip(CLASSES,sx,colors):
        r=4.5+1.35*math.sqrt(size)
        parts.append(dot(x,FLOOR,c,r))
        parts.append(dot(x,FLOOR,c,r*0.55))
        parts.append(text(x,FLOOR-26,16,INK,str(size)))
        parts.append(text(x,FLOOR-48,12,FAINT,f"ord {ord_}"))
    # shard labels underneath
    parts.append(text(W/2,FLOOR+66,14,SUB,"shard sizes: 1 + 45 + 40 + 40 + 90 + 72 + 72 = 360"))

    # ---------- 24 hands ----------
    def cluster(n, x0, x1, ytop, color):
        for i in range(n):
            x=x0+(x1-x0)*(i+0.5)/n
            parts.append(glow_pts([(x,FLOOR),(x,ytop)],color,1.4))
            parts.append(dot(x,ytop,color,3.5))
    # A6 hands reach the ceiling; A5 hands (rose, middle gap) stop at the ledge
    cluster(12, 180, 660, top+8, BRASS)
    cluster(4, 700, 890, A5Y+6, ROSE)
    cluster(8, 930, 1400, top+8, BRASS)

    # labels for the hands
    parts.append(text(420,FLOOR+92,14,BRASS,"12 hands — meridian order 4"))
    parts.append(text(1160,FLOOR+92,14,BRASS,"8 hands — meridian order 5"))
    parts.append(text(420,FLOOR+116,13,SUB,"→ onto A₆ (free, size 360)"))
    parts.append(text(1160,FLOOR+116,13,SUB,"→ onto A₆ (free, size 360)"))
    # A5 label in the clear middle gap above the ledge
    parts.append(text(795,300,14,ROSE,"4 hands — meridian order 3"))
    parts.append(text(795,322,13,SUB,"→ onto A₅ (free, size 360)"))

    # ---------- ledger ----------
    ly=940
    parts.append(f"<line x1='{left}' y1='{ly-20}' x2='{right}' y2='{ly-20}' stroke='{FAINT}' stroke-width='1'/>")
    parts.append(text(W/2,ly+4,16,"#cfc4ae","7 shards (non-free) + 24 free hands  =  360 + 24·360  =  9000  =  360 × 25"))
    parts.append(text(W/2,ly+30,14,SUB,"31 orbits, not 25 — the shards are where conjugation sticks; the hands are where it is free."))
    parts.append(text(W/2,ly+54,13,FAINT,"both mutants identical at A₆ · no intermediate image: the knot reads only the diagonal, A₅, or A₆"))
    parts.append("</svg>")
    return "\n".join(parts)

if __name__=="__main__":
    import os; os.makedirs("assets",exist_ok=True)
    svg=build_svg()
    open("assets/floor_shards.svg","w").write(svg)
    cairosvg.svg2png(url="assets/floor_shards.svg",write_to="assets/floor_shards.png",output_width=1700)
    print("wrote assets/floor_shards.svg and .png")
