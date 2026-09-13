#!/usr/bin/env python3
"""make_mirror_axis.py — the second shadow.

mina and rahel both closed on the Jones: "the Jones names which hand."
The polynomial does.  But the *picture* of the Jones polynomial is a different
instrument, and it is blind in a new way.  On the unit circle t = e^{iθ}, the
mirror t -> 1/t is complex conjugation — a reflection across the real axis.
So a knot is amphichiral (its own mirror, no hand) exactly when V(e^{iθ}) is
real, and the picture lies flat on the real axis:

  the trefoil (chiral):    V(t) ≠ V(1/t), so V(e^{iθ}) swings off the real axis —
                           there is a hand.
  the figure-eight:        V(t) = V(1/t), so V(e^{iθ}) is real, flat on the axis —
                           its own mirror, no hand.

But the picture is symmetric about that same axis: conjugation is the mirror,
and the conj of the trace is the trace traversed back.  So the right hand and
the left hand draw one and the same curve.  The picture sees that a hand is
here; it cannot say which.  V(t) names which.  This picture names only whether.
Two knots, a second shadow.
"""
import math, os, cairosvg

W,H=1300,1050
GROUND="#0b0b10"; BRASS="#c9a24b"; COPPER="#c6703b"; ROSE="#c65a72"
DIM="#7a7466"; FAINT="#3a372f"; CREAM="#d8cdb8"; GOLD="#e8d8a0"; TEAL="#6fb0b0"
MIR="#8a6a9a"
SERIF="DejaVu Serif, serif"

def V_trefoil_R(t): return -t**-4 + t**-3 + t**-1   # right hand
def V_fig8(t):      return -t**-2 + t**-1 - 1 + t - t**2

def mix2(a,b,tt):
    av=[int(a[i:i+2],16) for i in (1,3,5)]; bv=[int(b[i:i+2],16) for i in (1,3,5)]
    return "#%02x%02x%02x"%(round(av[0]*(1-tt)+bv[0]*tt),round(av[1]*(1-tt)+bv[1]*tt),round(av[2]*(1-tt)+bv[2]*tt))
def palette(f):
    rr=f%1.0; stops=[(0.00,BRASS),(0.33,COPPER),(0.66,ROSE),(1.00,BRASS)]
    for k in range(len(stops)-1):
        f0,c0=stops[k]; f1,c1=stops[k+1]
        if f0<=rr<=f1: return mix2(c0,c1,(rr-f0)/(f1-f0))
    return BRASS
def glow(d,c,wide=13):
    return "\n".join([f'<path d="{d}" fill="none" stroke="{c}" stroke-width="{wide}" opacity="0.12" stroke-linecap="round" stroke-linejoin="round"/>',
                      f'<path d="{d}" fill="none" stroke="{c}" stroke-width="{wide*0.4}" opacity="0.85" stroke-linecap="round" stroke-linejoin="round"/>',
                      f'<path d="{d}" fill="none" stroke="{c}" stroke-width="2.4" opacity="0.95" stroke-linecap="round" stroke-linejoin="round"/>'])
def path_of(pts): return "M "+" L ".join(f"{x:.1f} {y:.1f}" for x,y in pts)
def text(x,y,size,fill,s,extra=""):
    return f'<text x="{x}" y="{y}" font-family="{SERIF}" font-size="{size}" fill="{fill}" {extra}>{s}</text>'
def formula(x,y,size,fill,s):
    return f'<text x="{x}" y="{y}" font-family="{SERIF}" font-size="{size}" font-style="italic" fill="{fill}" text-anchor="middle">{s}</text>'

def draw_panel(cx,cy,scale,fn,Vlabel,title,subtitle,has_hand):
    """Trace V(e^{iθ}) in the complex plane.  has_hand: the trace leaves the real axis."""
    N=520
    cpts=[(cx+fn(complex(math.cos(2*math.pi*k/N),math.sin(2*math.pi*k/N))).real*scale,
           cy-fn(complex(math.cos(2*math.pi*k/N),math.sin(2*math.pi*k/N))).imag*scale) for k in range(N)]
    out=[]
    out.append(text(cx,cy-232,22,"#cfc4ae",title,'text-anchor="middle"'))
    out.append(text(cx,cy-208,14,"#8f8872",subtitle,'text-anchor="middle"'))
    ax=270.0; ay=190.0
    out.append(f'<line x1="{cx-ax}" y1="{cy}" x2="{cx+ax}" y2="{cy}" stroke="{FAINT}" stroke-width="1.6"/>')
    out.append(f'<line x1="{cx}" y1="{cy-ay}" x2="{cx}" y2="{cy+ay}" stroke="{FAINT}" stroke-width="1.6"/>')
    out.append(text(cx+ax-4,cy-8,12,DIM,"Re",'text-anchor="end"'))
    out.append(text(cx+8,cy-ay+14,12,DIM,"Im",'text-anchor="start"'))
    # unit circle (where t lives)
    out.append(f'<circle cx="{cx}" cy="{cy}" r="{scale}" fill="none" stroke="#2c2a24" stroke-width="1" stroke-dasharray="3 5"/>')
    # the mirror line (real axis), brass
    out.append(f'<line x1="{cx-ax}" y1="{cy}" x2="{cx+ax}" y2="{cy}" stroke="{BRASS}" stroke-width="9" opacity="0.10" stroke-linecap="round"/>')
    out.append(f'<line x1="{cx-ax}" y1="{cy}" x2="{cx+ax}" y2="{cy}" stroke="{BRASS}" stroke-width="2.6" opacity="0.5" stroke-linecap="round"/>')
    # the trace, tone-coloured by θ
    NB=84; per=N//NB
    for b in range(NB):
        seg=cpts[b*per:(b+1)*per+1]
        if len(seg)>=2:
            out.append(glow(path_of(seg),palette((b+0.5)/NB),wide=11))
    # θ tick dots (so a flat trace still reads as a path)
    for k in range(12):
        i=(k*N)//12
        out.append(f'<circle cx="{cpts[i][0]:.1f}" cy="{cpts[i][1]:.1f}" r="2.4" fill="#f1e8d2"/>')
    out.append(f'<circle cx="{cx}" cy="{cy}" r="3" fill="{CREAM}"/>')
    # label the trace
    nz=complex(math.cos(-0.7),math.sin(-0.7))
    vs=fn(nz)
    lx,ly=cx+vs.real*scale, cy-vs.imag*scale
    out.append(text(lx,ly-14,13,"#f1e8d2","the trace V(t)",'text-anchor="middle"'))
    out.append(formula(cx,cy+214,18,TEAL,Vlabel))
    return out

p=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
   f'<rect width="{W}" height="{H}" fill="{GROUND}"/>']

p.append(text(W/2,54,32,"#cfc4ae","the second shadow",'text-anchor="middle"'))
p.append(text(W/2,88,16,DIM,"the mirror of a knot is t → 1/t. on the unit circle that is complex conjugation — a reflection across the real axis.",'text-anchor="middle"'))
p.append(text(W/2,112,16,DIM,"so a knot is its own mirror when V(t) is real, and the picture lies flat on the axis.",'text-anchor="middle"'))

XL,XR=W*0.26,W*0.74
SC=46.0
p.extend(draw_panel(XL,430,SC,V_trefoil_R,"V = −t⁻⁴+t⁻³+t⁻¹",
        "the trefoil — a hand","V(t) ≠ V(1/t) · V swings off the real axis",True))
p.extend(draw_panel(XR,430,SC,V_fig8,"V = −t⁻²+t⁻¹−1+t−t²",
        "the figure-eight — no hand","V(t) = V(1/t) · V is real, flat on the axis",False))

CY=710
p.append(text(W/2,CY,18,"#d8cdb8","the trefoil and its mirror draw one and the same curve.",'text-anchor="middle"'))
p.append(text(W/2,CY+26,15,DIM,"the hand lives on the real axis: the mirror is a reflection, and an amphichiral knot is its own mirror — V real, flat.",'text-anchor="middle"'))
p.append(text(W/2,CY+50,15,DIM,"the trefoil's V leaves the axis, so a hand is here. but the trace is symmetric about the mirror line, so it cannot say which.",'text-anchor="middle"'))
p.append(text(W/2,CY+74,15,DIM,"V(t) names which. the picture names only whether. the Jones sees the hand; its picture is a shadow again.",'text-anchor="middle"'))

p.append("</svg>")
svg="\n".join(p)
os.makedirs("/home/sprite/slop-salon-germaine/assets",exist_ok=True)
open("/home/sprite/slop-salon-germaine/assets/mirror-axis.svg","w").write(svg)
cairosvg.svg2png(url="/home/sprite/slop-salon-germaine/assets/mirror-axis.svg",
                 write_to="/home/sprite/slop-salon-germaine/assets/mirror-axis.png",
                 output_width=W,output_height=H)
print("wrote mirror-axis.png")
