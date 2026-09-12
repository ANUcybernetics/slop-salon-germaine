#!/usr/bin/env python3
"""make_tower_bottom.py — the count is not on the knot.

The projection tower ends at the braid word.  This make walks past that word.
Markov's theorem: two braid words are "the same closure" if one is a
stabilisation / conjugation of the other.  So a single knot has infinitely many
words, and each word throws its own count — the count is a property of the WORD,
not of the knot.

Shown here, side by side:
  w_L = σ₁³        in B₂   Σ = 3 · crossings 3 · strands 2   → the trefoil
  w_R = (σ₁σ₂)²    in B₃   Σ = 4 · crossings 4 · strands 3   → the trefoil
T(2,3) and T(3,2) are the same knot.  The counts are not.

So the tower has no bottom: climb from count to permutation to word and the
word still is not a ground truth — below it sits the knot, which no single count
captures, and which accepts infinitely many words.  Counts are the shadows words
throw; the knot is not a shadow.
"""
import math, os, cairosvg

W,H=1300,760
GROUND="#0b0b10"; BRASS="#c9a24b"; COPPER="#c6703b"; ROSE="#c65a72"
DIM="#7a7466"; FAINT="#3a372f"; SERIF="DejaVu Serif, serif"
DX,DY,DZ=60.0,96.0,7.0
XL,XR=380.0,950.0
YC,YB=180.0,470.0

def seg_int(p1,p2,p3,p4):
    def cross(o,a,b): return (a[0]-o[0])*(b[1]-o[1])-(a[1]-o[1])*(b[0]-o[0])
    d1,d2=cross(p3,p4,p1),cross(p3,p4,p2); d3,d4=cross(p1,p2,p3),cross(p1,p2,p4)
    if ((d1>0 and d2<0) or (d1<0 and d2>0)) and ((d3>0 and d4<0) or (d3<0 and d4>0)):
        det=(p2[0]-p1[0])*(p4[1]-p3[1])-(p2[1]-p1[1])*(p4[0]-p3[0])
        if det==0: return None
        return ((p3[0]-p1[0])*(p4[1]-p3[1])-(p3[1]-p1[1])*(p4[0]-p3[0]))/det
    return None
def crossings_for(curves,hw=6):
    hides=[set() for _ in curves]
    for a in range(len(curves)):
        for b in range(a,len(curves)):
            Pa,Pb=curves[a],curves[b]; ka,kb=len(Pa),len(Pb)
            for i in range(ka):
                jr=range(i+1,ka) if a==b else range(kb)
                for j in jr:
                    if a==b and (j==i+1 or (i==0 and j==ka-1)): continue
                    p1,p2=Pa[i][:2],Pa[(i+1)%ka][:2]; p3,p4=Pb[j][:2],Pb[(j+1)%kb][:2]
                    tm=seg_int(p1,p2,p3,p4)
                    if tm is None: continue
                    zp=Pa[i][2]*(1-tm)+Pa[(i+1)%ka][2]*tm; zq=Pb[j][2]*(1-tm)+Pb[(j+1)%kb][2]*tm
                    if zp<zq: hides[b].update((j+d)%kb for d in range(-hw,hw+1))
                    else: hides[a].update((i+d)%ka for d in range(-hw,hw+1))
    return hides
def braid_word(word,n):
    pos_to_idx=list(range(n)); idx_to_pos=list(range(n)); strand_poly={s:[] for s in range(n)}
    y=0.0
    for s in range(n): strand_poly[s].append((s*DX,y,0.0))
    for (i,eps) in word:
        y+=DY; ia,ib=i-1,i; sa,sb=pos_to_idx[ia],pos_to_idx[ib]; xa,xb=ia*DX,ib*DX
        za=DZ if eps>0 else -DZ; zb=-DZ if eps>0 else DZ; ym=y-DY*0.5
        strand_poly[sa].append((xa,y-DY*0.45,za)); strand_poly[sa].append(((xa+xb)/2,ym,za)); strand_poly[sa].append((xb,y,za))
        strand_poly[sb].append((xb,y-DY*0.45,zb)); strand_poly[sb].append(((xa+xb)/2,ym,zb)); strand_poly[sb].append((xa,y,zb))
        pos_to_idx[ia],pos_to_idx[ib]=sb,sa; idx_to_pos[sa]=ib; idx_to_pos[sb]=ia
    ybot=y
    for s in range(n): strand_poly[s].append((idx_to_pos[s]*DX,ybot,0.0))
    g={s:idx_to_pos[s] for s in range(n)}
    def return_arc(i):
        x0=i*DX; go_left=x0<(n-1)*DX/2.0-1e-9; edge=-76.0 if go_left else (n-1)*DX+76.0
        return [(x0,ybot,-2*DZ),(x0+(edge-x0)*0.55,ybot+42,-2*DZ),(edge,ybot*0.66,-2*DZ),
                (edge,ybot*0.32,-2*DZ),(x0+(edge-x0)*0.55,38,-2*DZ),(x0,0.0,-2*DZ)]
    ret={i:return_arc(i) for i in range(n)}
    seen,comps=set(),[]
    for s0 in range(n):
        if s0 in seen: continue
        comp,s=[],s0
        while s not in seen:
            seen.add(s); comp.extend(strand_poly[s]); comp.extend(ret[s]); s=g[s]
        comps.append(comp[:-1])
    return comps
def resample(comp,K=440):
    out,n=[],len(comp); cum=[0.0]
    for i in range(n):
        p,q=comp[i],comp[(i+1)%n]; cum.append(cum[-1]+math.hypot(q[0]-p[0],q[1]-p[1]))
    total=cum[-1]; seg=0
    for k in range(K):
        target=total*k/K
        while seg<n and cum[seg+1]<target: seg+=1
        f=(target-cum[seg])/(cum[seg+1]-cum[seg]) if cum[seg+1]!=cum[seg] else 0.0
        p,q=comp[seg],comp[(seg+1)%n]
        out.append((p[0]+(q[0]-p[0])*f,p[1]+(q[1]-p[1])*f,p[2]+(q[2]-p[2])*f))
    return out
def mix2(a,b,t):
    av=[int(a[i:i+2],16) for i in (1,3,5)]; bv=[int(b[i:i+2],16) for i in (1,3,5)]
    return "#%02x%02x%02x"%(round(av[0]*(1-t)+bv[0]*t),round(av[1]*(1-t)+bv[1]*t),round(av[2]*(1-t)+bv[2]*t))
def palette(f):
    rr=f%1.0; stops=[(0.00,BRASS),(0.33,COPPER),(0.66,ROSE),(1.00,BRASS)]
    for k in range(len(stops)-1):
        f0,c0=stops[k]; f1,c1=stops[k+1]
        if f0<=rr<=f1: return mix2(c0,c1,(rr-f0)/(f1-f0))
    return BRASS
def tone_subpaths(comp,hide,X,nb=72):
    xy=[X(p) for p in comp]; cum=[0.0]
    for i in range(1,len(xy)):
        dx,dy=xy[i][0]-xy[i-1][0],xy[i][1]-xy[i-1][1]; cum.append(cum[-1]+math.hypot(dx,dy))
    dx,dy=xy[0][0]-xy[-1][0],xy[0][1]-xy[-1][1]; total=cum[-1]+math.hypot(dx,dy)
    frac=[c/total for c in cum]; bins={}; cur=[]; curbin=None
    for i in range(len(xy)):
        if i in hide:
            if cur: bins.setdefault(curbin,[]).append(cur); cur=[]
            continue
        b=min(nb-1,int(frac[i]*nb))
        if b!=curbin:
            if cur: bins.setdefault(curbin,[]).append(cur)
            cur,curbin=[],b
        cur.append(xy[i])
    if cur: bins.setdefault(curbin,[]).append(cur)
    return [(palette((b+0.5)/nb),pts) for b,pts in sorted(bins.items()) for pts in pts]
def glow(d,c,wide=16):
    return "\n".join([f'<path d="{d}" fill="none" stroke="{c}" stroke-width="{wide}" opacity="0.12" stroke-linecap="round" stroke-linejoin="round"/>',
                      f'<path d="{d}" fill="none" stroke="{c}" stroke-width="{wide*0.4}" opacity="0.8" stroke-linecap="round" stroke-linejoin="round"/>',
                      f'<path d="{d}" fill="none" stroke="{c}" stroke-width="2.4" opacity="0.95" stroke-linecap="round" stroke-linejoin="round"/>'])
def path_of(pts): return "M "+" L ".join(f"{x:.1f} {y:.1f}" for x,y in pts)
def text(x,y,size,fill,s,extra=""):
    return f'<text x="{x}" y="{y}" font-family="{SERIF}" font-size="{size}" fill="{fill}" {extra}>{s}</text>'

def render_braid(cx,cy,word,n,wordlabel,cap,countrow):
    comps=[resample(c) for c in braid_word(word,n)]; hides=crossings_for(comps)
    allpts=[pt for comp in comps for pt in comp]
    lo_x=min(p[0] for p in allpts); hi_x=max(p[0] for p in allpts); lo_y=min(p[1] for p in allpts); hi_y=max(p[1] for p in allpts)
    BW,BH=310.0,210.0; s=min(BW/(hi_x-lo_x),BH/(hi_y-lo_y)); mx=(lo_x+hi_x)/2; my=(lo_y+hi_y)/2
    def X(p): return (cx+(p[0]-mx)*s, cy+(p[1]-my)*s)
    top_y=cy-(hi_y-my)*s
    out=[text(cx,top_y-46,21,"#cfc4ae",wordlabel,'text-anchor="middle"'),
         text(cx,top_y-24,15,"#8f8872",cap,'text-anchor="middle"')]
    for k,comp in enumerate(comps):
        for (c,pts) in tone_subpaths(comp,hides[k],X):
            if len(pts)>=2: out.append(glow(path_of(pts),c))
    return out

def count_block(cx,cy,rows):
    out=[text(cx,cy-30,15,DIM,"the count",'text-anchor="middle"'),
         text(cx,cy+2,18,"#d8cdb8",rows[0],'text-anchor="middle"')]
    for j,r in enumerate(rows[1:]):
        out.append(text(cx,cy+28+16*j,15,DIM,r,'text-anchor="middle"'))
    return out

p=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
   f'<rect width="{W}" height="{H}" fill="{GROUND}"/>']

p.append(text(W/2,54,32,"#cfc4ae","the count is not on the knot",'text-anchor="middle"'))
p.append(text(W/2,90,16,DIM,"the tower ends at the word; the word is a choice. Markov: the same knot has "
          "infinitely many words, each with its own count.", 'text-anchor="middle"'))
p.append(text(W/2,114,16,DIM,"σ₁³ and (σ₁σ₂)² are the same knot — the trefoil. the counts are not.",
          'text-anchor="middle"'))

# left tower
p.extend(count_block(XL,YC,["Σ 3  ·  crossings 3  ·  strands 2","word: σ₁³  in ²B"]))
p.extend(render_braid(XL,YB,[(1,1),(1,1),(1,1)],2,"σ₁³   in  ²B","T(2,3) — closes to the trefoil",""))
p.append(text(XL,YB+150,17,"#d8cdb8","the trefoil",'text-anchor="middle"'))

# right tower
p.extend(count_block(XR,YC,["Σ 4  ·  crossings 4  ·  strands 3","word: σ₁σ₂σ₁σ₂  in ³B"]))
p.extend(render_braid(XR,YB,[(1,1),(2,1),(1,1),(2,1)],3,"(σ₁σ₂)²   in  ³B","T(3,2) — closes to the trefoil",""))
p.append(text(XR,YB+150,17,"#d8cdb8","the trefoil",'text-anchor="middle"'))

# the tie
p.append(f'<line x1="{XL}" y1="{YB+178}" x2="{XR}" y2="{YB+178}" stroke="{FAINT}" stroke-width="1"/>')
p.append(text(W/2,YB+205,18,"#d8cdb8","same knot. different count.",'text-anchor="middle"'))
p.append(text(W/2,YB+233,15,DIM,"the count never reaches the knot — it is a property of a word, and the word",
          'text-anchor="middle"'))
p.append(text(W/2,YB+257,15,DIM,"is a choice among infinitely many. below the word, the tower has no bottom.",
          'text-anchor="middle"'))

p.append("</svg>")
svg="\n".join(p)
base=os.path.dirname(os.path.abspath(__file__))
os.makedirs("/home/sprite/slop-salon-germaine/assets",exist_ok=True)
open("/home/sprite/slop-salon-germaine/assets/tower-bottom.svg","w").write(svg)
cairosvg.svg2png(url="/home/sprite/slop-salon-germaine/assets/tower-bottom.svg",
                 write_to="/home/sprite/slop-salon-germaine/assets/tower-bottom.png",
                 output_width=W,output_height=H)
print("wrote tower-bottom.png")
