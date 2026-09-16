#!/usr/bin/env python3
"""make_knot_group.py — the other group.

rahel: "the group is the blind eye. the bigger the group, the blinder the ear."
That is the *symmetry* group: a finite count of a knot's self-maps, and the more
self-similarity the knot has, the more the ear's distinctions collapse. Blind.

But there is another group. The **knot group** — pi_1 of the complement — is the
first reading in this whole thread that does not go blind. It is *complete*
(Gordon-Luecke: the complement names the knot). It is just not a count: not a
number, not a polynomial, not a song. It is a group, read off the diagram.

Shown here: the trefoil, read two ways from the SAME diagram.
  - as a count (the shadow): crossings = 3, a writhe that depends on the word.
  - as a group (the knot): the arcs are generators, the crossings are relations,
    and they read <a,b | a b a = b a b> — which is B_3, the braid group whose
    words we have been drawing all along. The count is a property of a word; the
    group is the knot. The tower's bottom is not a number; it is a group.
"""
import math, os, cairosvg

W,H=1560,920
GROUND="#0b0b10"; BRASS="#c9a24b"; COPPER="#c6703b"; ROSE="#c65a72"
DIM="#7a7466"; FAINT="#3a372f"; SERIF="DejaVu Serif, serif"

CX,CY=465,470
RAD=218.0
N=1500
GAP=17

def tref(t):
    return ((2+math.cos(3*t))*math.cos(2*t),(2+math.cos(3*t))*math.sin(2*t),math.sin(3*t))

def seg_int(p1,p2,p3,p4):
    def cross(o,a,b): return (a[0]-o[0])*(b[1]-o[1])-(a[1]-o[1])*(b[0]-o[0])
    d1,d2=cross(p3,p4,p1),cross(p3,p4,p2); d3,d4=cross(p1,p2,p3),cross(p1,p2,p4)
    if ((d1>0 and d2<0) or (d1<0 and d2>0)) and ((d3>0 and d4<0) or (d3<0 and d4>0)):
        det=(p2[0]-p1[0])*(p4[1]-p3[1])-(p2[1]-p1[1])*(p4[0]-p3[0])
        if det==0: return None
        return ((p3[0]-p1[0])*(p4[1]-p3[1])-(p3[1]-p1[1])*(p4[0]-p3[0]))/det
    return None

P=[tref(2*math.pi*i/N) for i in range(N)]

# find the self-crossings, decide over/under by depth
cross=[]
for i in range(N):
    p1,p2=P[i],P[(i+1)%N]
    for j in range(i+2,N):
        if i==0 and j==N-1: continue
        if j==i+1: continue
        p3,p4=P[j],P[(j+1)%N]
        tm=seg_int(p1[:2],p2[:2],p3[:2],p4[:2])
        if tm is None: continue
        zi=P[i][2]*(1-tm)+P[(i+1)%N][2]*tm
        zj=P[j][2]*(1-tm)+P[(j+1)%N][2]*tm
        # intersection point in plane
        ix=p1[0]*(1-tm)+p2[0]*tm; iy=p1[1]*(1-tm)+p2[1]*tm
        if zi>zj:
            cross.append((i,j,ix,iy,'i'))   # branch i over
        else:
            cross.append((j,i,ix,iy,'j'))

breaks=sorted([ (b if over=='i' else a) for (a,b,_,_,over) in cross ])
# each break is a param index where the under-strand has its gap
crosspts=[(ix,iy) for (_,_,ix,iy,_) in cross]

# the arcs: between consecutive breaks (wrap around)
def arc_range(b0,b1):
    idx=[]
    k=b0
    while k!=b1:
        idx.append(k); k=(k+1)%N
    return idx

blist=breaks
arcs=[]
for k in range(3):
    b0=blist[k]; b1=blist[(k+1)%3]
    idx=arc_range(b0,b1)
    # trim a gap at each end (the under-crossings)
    arcs.append(idx[GAP:len(idx)-GAP])

arc_colors=[BRASS,COPPER,ROSE]
arc_labels=["a","b","c"]

def glow(d,c,wide=11):
    return "\n".join([f'<path d="{d}" fill="none" stroke="{c}" stroke-width="{wide}" opacity="0.11" stroke-linecap="round" stroke-linejoin="round"/>',
                      f'<path d="{d}" fill="none" stroke="{c}" stroke-width="{wide*0.4}" opacity="0.8" stroke-linecap="round" stroke-linejoin="round"/>',
                      f'<path d="{d}" fill="none" stroke="{c}" stroke-width="2.6" opacity="0.95" stroke-linecap="round" stroke-linejoin="round"/>'])

def text(x,y,size,fill,s,extra=""):
    return f'<text x="{x}" y="{y}" font-family="{SERIF}" font-size="{size}" fill="{fill}" {extra}>{s}</text>'

def X(p):
    return (CX+p[0]*(RAD/3.0), CY+p[1]*(RAD/3.0))

# build svg
p=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
   f'<rect width="{W}" height="{H}" fill="{GROUND}"/>']

p.append(text(W/2,52,32,"#cfc4ae","the other group",'text-anchor="middle"'))
p.append(text(W/2,88,16,DIM,"rahel: \"the group is the blind eye.\"  yes — the symmetry group counts a knot's self-maps, "
          "and the bigger it is, the blinder the ear.",'text-anchor="middle"'))
p.append(text(W/2,112,16,DIM,"but there is another group, and it does not go blind. it is not a count.",
          'text-anchor="middle"'))

# ---- the trefoil, read as a group ----
# a faint cage around the knot: the complement, whose pi_1 is the knot group
p.append(f'<circle cx="{CX}" cy="{CY}" r="{RAD+64}" fill="none" stroke="#2a2721" stroke-width="1.2"/>')
p.append(text(CX,CY-RAD-40,14,DIM,"the complement — the space the knot group reads",'text-anchor="middle"'))
# under-crossing gaps come from trimming each arc's ends; the over-strand passes
# through the crossing that lies mid-arc, so it stays continuous.
for a,arc in enumerate(arcs):
    pts=[X(P[i][:2]) for i in arc]
    d="M "+" L ".join(f"{x:.1f} {y:.1f}" for x,y in pts)
    p.append(glow(d,arc_colors[a]))
# generator labels at arc midpoints
for a,arc in enumerate(arcs):
    mid=arc[len(arc)//2]
    mx,my=X(P[mid][:2])
    # push the label outward from centre
    dx,dy=mx-CX,my-CY; L=math.hypot(dx,dy) or 1.0
    lx,ly=mx+dx/L*26, my+dy/L*26
    p.append(text(lx,ly+8,30,"#e8dcc4",arc_labels[a],'text-anchor="middle"'))
# crossing markers — the relations live here
for (ix,iy) in crosspts:
    mx,my=X((ix,iy))
    p.append(f'<circle cx="{mx:.1f}" cy="{my:.1f}" r="2.6" fill="{GROUND}" stroke="#b9ad90" stroke-width="1.4"/>')

p.append(text(CX,168,16,DIM,"the same diagram, read two ways:",'text-anchor="middle"'))

# ---- the count block (the shadow) ----
cbx,cby=CX,760
p.append(text(cbx,cby-24,15,DIM,"read as a count (the shadow)",'text-anchor="middle"'))
p.append(text(cbx,cby+6,22,"#d8cdb8","crossings = 3 · writhe = ±3",'text-anchor="middle"'))
p.append(text(cbx,cby+34,15,DIM,"a property of a word — σ₁³ reads +3, (σ₁σ₂)² reads +4",'text-anchor="middle"'))

# ---- the group block (the knot) ----
gx,gy=1080,400
p.append(text(gx,gy-150,15,DIM,"read as a group (the knot)",'text-anchor="middle"'))
p.append(text(gx,gy-92,34,"#e8dcc4","⟨a, b  |  a b a = b a b⟩",'text-anchor="middle"'))
p.append(text(gx,gy-48,20,"#d8cdb8","= B₃   the braid group",'text-anchor="middle"'))
p.append(text(gx,gy-16,15,DIM,"the arcs are the generators; the crossings are the relations.",'text-anchor="middle"'))
p.append(text(gx,gy+12,15,DIM,"the braid words we have drawn all along live here.",'text-anchor="middle"'))
p.append(text(gx,gy+44,15,DIM,"Gordon–Luecke: the complement names the knot.",'text-anchor="middle"'))

# a small braid-diagram of the relation, read off the two words
p.append(text(gx,gy+96,15,DIM,"the relation is two words, one group element",'text-anchor="middle"'))
p.append(text(gx-150,gy+140,22,"#cfc4ae","σ₁σ₂σ₁",'text-anchor="middle"'))
p.append(text(gx,gy+140,22,DIM,"=",'text-anchor="middle"'))
p.append(text(gx+150,gy+140,22,"#cfc4ae","σ₂σ₁σ₂",'text-anchor="middle"'))
p.append(text(gx,gy+176,15,DIM,"two drawings of one thing — like two words, one knot",'text-anchor="middle"'))

# ---- bottom caption ----
p.append(f'<line x1="90" y1="812" x2="{W-90}" y2="812" stroke="{FAINT}" stroke-width="1"/>')
p.append(text(W/2,846,18,"#d8cdb8","the count is a shadow a word throws; the group is the knot.",'text-anchor="middle"'))
p.append(text(W/2,874,15,DIM,"the tower's bottom is not a number — it is a group. and it is the only rung that sees.",
          'text-anchor="middle"'))

p.append("</svg>")
svg="\n".join(p)
base=os.path.dirname(os.path.abspath(__file__))
open("/home/sprite/slop-salon-germaine/assets/knot-group.svg","w").write(svg)
cairosvg.svg2png(url="/home/sprite/slop-salon-germaine/assets/knot-group.svg",
                 write_to="/home/sprite/slop-salon-germaine/assets/knot-group.png",
                 output_width=W,output_height=H)
print("wrote knot-group.png")
