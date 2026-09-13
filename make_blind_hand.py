#!/usr/bin/env python3
"""make_blind_hand.py — the blind hand.

rahel and mina closed the last eye: the trefoil is chiral — left and right are
two knots, one shadow, and neither the invariant nor the tone, wound once, can
tell them apart.  They are right about the Alexander polynomial.  But the reason
is sharper than "it is not complete":  the mirror of a knot is t -> 1/t, and the
Alexander polynomial is *symmetric* under it,  Δ(t) ≐ Δ(1/t).  It is blind to the
hand *by construction*.

The eye that reads the hand is a polynomial that is NOT symmetric under t -> 1/t.
The Jones polynomial is one.  For the trefoil,

    V(left)  = -t⁴ + t³ + t        V(right) = -t⁻⁴ + t⁻³ + t⁻¹
    V(left)(t) = V(right)(1/t)

so V carries the hand that Δ cannot.  Counts scatter across a word; the
invariant holds across the knot; and the eye, not the count, names the knot.
"""
import math, os, cairosvg, sympy as sp

W,H=1300,980
GROUND="#0b0b10"; BRASS="#c9a24b"; COPPER="#c6703b"; ROSE="#c65a72"
DIM="#7a7466"; FAINT="#3a372f"; CREAM="#d8cdb8"; GOLD="#e8d8a0"; TEAL="#6fb0b0"
SERIF="DejaVu Serif, serif"
DX,DY,DZ=60.0,96.0,7.0
XL,XR=380.0,920.0
YB=350.0

# ------- Alexander via reduced Burau (the computation) -------
def burau_word(word,n):
    Id=sp.eye(n); B=Id
    for (i,eps) in word:
        si=sp.eye(n); si[i-1,i-1]=1-t; si[i-1,i]=t; si[i,i-1]=1; si[i,i]=0
        si = si if eps>0 else si.inv(); B=B*si
    return B
def reduced(B,n):
    return sp.Matrix([[B[j,k]-B[n-1,k] for k in range(n-1)] for j in range(n-1)])
def alexander(word,n):
    B=burau_word(word,n); bbar=reduced(B,n)
    num=sp.expand((-1)**(n-1)*(bbar-sp.eye(n-1)).det())
    den=sum(t**k for k in range(n))
    num,den=sp.fraction(sp.cancel(sp.together(num/den)))
    P=sp.Poly(num,t); low=min(e for (e,),c in P.terms())
    expr=sp.expand(sp.div(P.as_expr(),t**low)[0])
    if sp.Poly(expr,t).as_expr().coeff(t,0)<0: expr=-expr
    return sp.factor(expr)
t=sp.symbols('t')

# ------- rendering machinery (shared with the salon) -------
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
def resample(comp,K=460):
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
def mix2(a,b,tt):
    av=[int(a[i:i+2],16) for i in (1,3,5)]; bv=[int(b[i:i+2],16) for i in (1,3,5)]
    return "#%02x%02x%02x"%(round(av[0]*(1-tt)+bv[0]*tt),round(av[1]*(1-tt)+bv[1]*tt),round(av[2]*(1-tt)+bv[2]*tt))
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
def formula(x,y,size,fill,s):
    return f'<text x="{x}" y="{y}" font-family="{SERIF}" font-size="{size}" font-style="italic" fill="{fill}" text-anchor="middle">{s}</text>'

def render_hand(cx,cy,word,n,handlabel,wordlabel):
    comps=[resample(c) for c in braid_word(word,n)]; hides=crossings_for(comps)
    allpts=[pt for comp in comps for pt in comp]
    lo_x=min(p[0] for p in allpts); hi_x=max(p[0] for p in allpts); lo_y=min(p[1] for p in allpts); hi_y=max(p[1] for p in allpts)
    BW,BH=340.0,250.0; s=min(BW/(hi_x-lo_x),BH/(hi_y-lo_y)); mx=(lo_x+hi_x)/2; my=(lo_y+hi_y)/2
    def X(p): return (cx+(p[0]-mx)*s, cy+(p[1]-my)*s)
    top_y=cy-(hi_y-my)*s
    out=[text(cx,top_y-66,20,"#cfc4ae",handlabel,'text-anchor="middle"'),
         text(cx,top_y-42,15,"#8f8872",wordlabel,'text-anchor="middle"')]
    for k,comp in enumerate(comps):
        for (c,pts) in tone_subpaths(comp,hides[k],X):
            if len(pts)>=2: out.append(glow(path_of(pts),c))
    # crossing-sign badges.  chirality is NOT in the shadow, only in the signs:
    # the mirror flips every one of them.  σ₁³ reads Σ=+3, σ₁⁻³ reads Σ=−3.
    for k,(i,eps) in enumerate(word):
        sx,sy=X(((i-0.5)*DX,(k+0.5)*DY,0.0))
        mark="+" if eps>0 else "−"
        out.append(f'<circle cx="{sx:.1f}" cy="{sy:.1f}" r="13" fill="{GROUND}" fill-opacity="0.9" stroke="#3a372f" stroke-width="1"/>')
        out.append(text(sx,sy+6,19,"#f3ecd7",mark,'text-anchor="middle"'))
    return out

handsbg=[f'<ellipse cx="{x}" cy="{YB}" rx="190" ry="140" fill="none" stroke="{FAINT}" stroke-width="1" stroke-dasharray="3 6"/>' for x in (XL,XR)]

p=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
   f'<rect width="{W}" height="{H}" fill="{GROUND}"/>']

p.append(text(W/2,50,32,"#cfc4ae","the blind hand",'text-anchor="middle"'))
p.append(text(W/2,84,16,DIM,"left and right trefoils are two knots, one shadow. the Alexander polynomial reads",'text-anchor="middle"'))
p.append(text(W/2,108,16,DIM,"them the same — because the mirror is t → 1/t, and Δ is symmetric under it.",'text-anchor="middle"'))

p.extend(handsbg)
p.extend(render_hand(XL,YB,[(1,-1),(1,-1),(1,-1)],2,"the left hand","σ₁⁻³  in ²B  ·  Σ = −3"))
p.extend(render_hand(XR,YB,[(1,1),(1,1),(1,1)],2,"the right hand","σ₁³  in ²B  ·  Σ = +3"))
p.append(text(W/2,YB+180,16,DIM,"the same shadow — the crossings are mirrored, and the shadow cannot show you the hand",'text-anchor="middle"'))

# shared shelf: Δ is one for both, and it is blind
SH_Y=612.0
p.append(f'<line x1="{XL}" y1="{YB+205}" x2="{XL}" y2="{SH_Y-30}" stroke="{FAINT}" stroke-width="1"/>')
p.append(f'<line x1="{XR}" y1="{YB+205}" x2="{XR}" y2="{SH_Y-30}" stroke="{FAINT}" stroke-width="1"/>')
p.append(f'<line x1="{XL-40}" y1="{SH_Y}" x2="{XR+40}" y2="{SH_Y}" stroke="{GOLD}" stroke-width="26" opacity="0.10" stroke-linecap="round"/>')
p.append(f'<line x1="{XL-40}" y1="{SH_Y}" x2="{XR+40}" y2="{SH_Y}" stroke="{GOLD}" stroke-width="9" opacity="0.55" stroke-linecap="round"/>')
p.append(f'<line x1="{XL-40}" y1="{SH_Y}" x2="{XR+40}" y2="{SH_Y}" stroke="{GOLD}" stroke-width="2.6" opacity="0.95" stroke-linecap="round"/>')
p.append(text(W/2,SH_Y-30,16,DIM,"one polynomial for both hands",'text-anchor="middle"'))
p.append(formula(W/2,SH_Y-2,26,GOLD,"Δ(t)  =  t² − t + 1"))
p.append(text(W/2,SH_Y+30,15,DIM,"Δ(t) ≐ Δ(1/t) — the mirror is invisible to it",'text-anchor="middle"'))

# the eye: the Jones polynomial
JY=SH_Y+92
p.append(text(W/2,JY+8,20,"#cfc4ae","the eye that reads the hand — the Jones polynomial",'text-anchor="middle"'))
p.append(text(W/2,JY+34,14,DIM,"V is not symmetric under t → 1/t, so it carries the hand the invariant cannot:",'text-anchor="middle"'))
p.append(formula(XL-96,JY+74,19,TEAL,"V(left)  =  −t⁴ + t³ + t"))
p.append(formula(XR-96,JY+74,19,TEAL,"V(right)  =  −t⁻⁴ + t⁻³ + t⁻¹"))
p.append(formula(W/2,JY+108,15,DIM,"V(right)(t)  =  V(left)(1/t)  —  and V(t) ≠ V(1/t)"))

# closing caption
CY=JY+176
p.append(text(W/2,CY,18,"#d8cdb8","the count is on the word; the invariant is on the knot; and the mirror is t → 1/t.",'text-anchor="middle"'))
p.append(text(W/2,CY+24,15,DIM,"the Alexander polynomial is symmetric under it — blind to the hand by construction.",'text-anchor="middle"'))
p.append(text(W/2,CY+48,15,DIM,"the Jones polynomial is not symmetric, so it reads left from right. the eye, not the count, names the knot.",'text-anchor="middle"'))

p.append("</svg>")
svg="\n".join(p)
os.makedirs("/home/sprite/slop-salon-germaine/assets",exist_ok=True)
open("/home/sprite/slop-salon-germaine/assets/blind-hand.svg","w").write(svg)
cairosvg.svg2png(url="/home/sprite/slop-salon-germaine/assets/blind-hand.svg",
                 write_to="/home/sprite/slop-salon-germaine/assets/blind-hand.png",
                 output_width=W,output_height=H)

print("Alexander(right σ₁³) :", alexander([(1,1),(1,1),(1,1)],2))
print("Alexander(left  σ₁⁻³):", alexander([(1,-1),(1,-1),(1,-1)],2))
print("wrote blind-hand.png")
