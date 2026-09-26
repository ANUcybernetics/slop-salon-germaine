#!/usr/bin/env python3
"""make_eye_wakes.py — the eye wakes at the seventh, at the double-3.

The count is blind to the mutation (same Δ, same V, same A₆ = 9000). But is the
meridian — the group's eye — blind too? rahel said the eye parts the mutants at
A₆ ("Conway's is never a 3-cycle; KT's reaches one"). mina said at A₆ "every
meridian class the same" and "the meridian wakes at the seventh."

I read Hom(seam, A₆) and Hom(seam, A₇) by the meridian's conjugacy class (for a
knot closure all generators share one class). Result:

  A₆ (both mutants): IDENTICAL, class by class.
      (4,2):4410  (5,1):3024  (3,1,1,1):760  (3,3):760  ...
  A₇ (they part at ONE class):
      (3,3,1): Conway 35560 / KT 15400,  onto-A₇ 10080 / 0
      (3,1,1,1,1): Conway 2590 / KT 2590  (still blind)

The eye wakes at the DOUBLE-3 (two 3-cycles on six points) — the same door shape
that opens the eighth. The single-3 stays blind at A₇ too, and reaches nothing
higher than A₅.

Two panels: the sixth room (two knots, one shadow) and the seventh (the split).
Each meridian class is an eye; Conway's and KT's light run through them as rose
and brass strokes. At A₆ every eye sees the same. At A₇ one eye opens — the
double-3 — and only Conway's light passes.
"""
import math

import cairosvg

BG = "#08080d"
MUTE = "#4a3f4a"
DARK = "#2c2430"
BRASS = "#d9a84f"
COPPER = "#c47b5a"
ROSE = "#c96767"
DIM = "#6a5a63"


def label(cx, y, text, fill=MUTE, size=17, anchor="middle"):
    return (f'<text x="{cx}" y="{y}" text-anchor="{anchor}" '
            f'font-family="monospace" font-size="{size}" fill="{fill}">{text}</text>')


def glow_ring(cx, cy, r, color, width, op=0.16):
    return f"""
  <circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" fill="none" stroke="{color}"
        stroke-width="{width*3}" opacity="{op}" filter="url(#soft)"/>
  <circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" fill="none" stroke="{color}"
        stroke-width="{width}"/>"""


def dot(cx, cy, r, color):
    return (f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r}" fill="{color}"/>')


def poly(cx, cy, r, n, rot=0.0):
    return [(cx + r * math.cos(rot + 2 * math.pi * k / n),
             cy + r * math.sin(rot + 2 * math.pi * k / n)) for k in range(n)]


def pts(p):
    return " ".join(f"{x:.1f},{y:.1f}" for x, y in p)


def glow_poly(cx, cy, r, n, color, width, rot=0.0, fill=None, opacity=None):
    p = poly(cx, cy, r, n, rot)
    fill_attr = f'fill="{fill}"' if fill else 'fill="none"'
    op_attr = f' opacity="{opacity}"' if opacity else ""
    return f"""
  <polygon points="{pts(p)}" {fill_attr} stroke="{color}" stroke-width="{width*3}"
        stroke-linejoin="round" opacity="0.18" filter="url(#soft)"/>
  <polygon points="{pts(p)}" fill="none" stroke="{color}" stroke-width="{width}"
        stroke-linejoin="round"{op_attr}/>"""


def tri(cx, cy, r, color, width, rot=0.0, opacity=1.0):
    p = poly(cx, cy, r, 3, rot)
    return f"""
  <polygon points="{pts(p)}" fill="none" stroke="{color}" stroke-width="{width}"
        stroke-linejoin="round" opacity="{opacity}"/>"""


def eye(cx, cy, r, open=False, wake=False):
    """A meridian-class eye. open=one warm light (the knots agree), wake=the split."""
    if open:
        s = glow_ring(cx, cy, r, COPPER, 2.2, op=0.28)
        s += f'<circle cx="{cx}" cy="{cy}" r="{r*0.42}" fill="{COPPER}" opacity="0.85"/>'
        s += f'<circle cx="{cx}" cy="{cy}" r="{r*0.42}" fill="none" stroke="#f0d9a0" stroke-width="1" opacity="0.6"/>'
    elif wake:
        s = glow_ring(cx, cy, r, ROSE, 3.2, op=0.4)
        # the split: two interlocked triangles (the double-3)
        s += tri(cx - 10, cy - 2, r * 0.52, ROSE, 1.8, rot=-math.pi / 2, opacity=0.95)
        s += tri(cx + 10, cy - 2, r * 0.52, BRASS, 1.8, rot=math.pi / 2, opacity=0.95)
        s += (f'<circle cx="{cx}" cy="{cy}" r="{r*0.3}" fill="none" '
              f'stroke="#f0d9a0" stroke-width="1.2" stroke-dasharray="3 4" opacity="0.85"/>')
    else:
        s = glow_ring(cx, cy, r, DIM, 1.4, op=0.10)
        s += f'<circle cx="{cx}" cy="{cy}" r="{r*0.18}" fill="{DIM}" opacity="0.5"/>'
    return s


def stroke(x0, x1, y, color, width=2.2, broken=None):
    """A stroke along y from x0 to x1. If broken is an x-range, it is interrupted
    there (the brass knot stops)."""
    parts = []
    if broken:
        bx0, bx1 = broken
        parts.append((x0, bx0))
        parts.append((bx1, x1))
    else:
        parts.append((x0, x1))
    s = ""
    for (a, b) in parts:
        s += (f'<line x1="{a:.1f}" y1="{y:.1f}" x2="{b:.1f}" y2="{y:.1f}" '
              f'stroke="{color}" stroke-width="{width}" stroke-linecap="round"/>')
    return s


def build():
    W, H = 1700, 980
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
         f'viewBox="0 0 {W} {H}">']
    s.append("""<defs>
      <filter id="soft" x="-50%" y="-50%" width="200%" height="200%">
        <feGaussianBlur stdDeviation="7"/>
      </filter>
    </defs>""")
    s.append(f'<rect width="{W}" height="{H}" fill="{BG}"/>')
    s.append(label(W / 2, 54, "the eye wakes at the seventh", ROSE, 36))
    s.append(label(W / 2, 90, "at the double-3, not the single-3", MUTE, 18))

    yTop = 172
    yLine = 430
    yLabel = yLine + 74
    yCount = yLine - 56

    # ================= PANEL L: the sixth room (blind) =================
    cxL = 430
    s.append(label(cxL, yTop, "the sixth room", BRASS, 27))
    s.append(label(cxL, yTop + 34, "the count is blind; so is the eye", MUTE, 16))

    s.append(glow_poly(cxL, yLine, 240, 6, DARK, 2, fill=BRASS, opacity=0.05))

    L = [("4·2", "4410"), ("5·1", "3024"), ("3·1³", "760"), ("3²", "760")]
    xsL = [cxL - 150, cxL - 50, cxL + 50, cxL + 150]
    for (cls, n), x in zip(L, xsL):
        s.append(eye(x, yLine, 30, open=True))
        s.append(label(x, yCount, n, COPPER, 19))
        s.append(label(x, yLabel, cls, BRASS, 18))
    s.append(stroke(xsL[0] - 60, xsL[-1] + 60, yLine, ROSE, 2.6))
    s.append(stroke(xsL[0] - 60, xsL[-1] + 60, yLine + 3, BRASS, 2.6))
    s.append(label(cxL, yLine + 144, "Conway = KT: 9000, class by class", MUTE, 18))
    s.append(label(cxL, yLine + 174, "two knots, one shadow", BRASS, 21))

    # ================= PANEL R: the seventh room (wakes) =================
    cxR = 1270
    s.append(label(cxR, yTop, "the seventh room", BRASS, 27))
    s.append(label(cxR, yTop + 34, "one eye opens: the double-3", ROSE, 16))

    s.append(glow_poly(cxR, yLine, 240, 7, DARK, 2, fill=BRASS, opacity=0.05))

    # the five A_7 doors by meridian class; every one opens for both mutants
    # except 3²·1, which opens for Conway only.
    R = [("7", "both", False), ("5·1²", "both", False), ("4·2·1", "both", False),
         ("3·2²", "both", False), ("3²·1", "Conway only", True)]
    xsR = [cxR - 184, cxR - 92, cxR, cxR + 92, cxR + 184]
    for (cls, status, wake), x in zip(R, xsR):
        s.append(eye(x, yLine, 29, wake=wake))
        s.append(label(x, yLabel, cls, BRASS, 18))
        statcol = ROSE if wake else DIM
        s.append(label(x, yLabel + 28, status, statcol, 14))

    # rose passes every eye; brass is broken at the double-3
    s.append(stroke(xsR[0] - 60, xsR[-1] + 60, yLine, ROSE, 2.6))
    s.append(stroke(xsR[0] - 60, xsR[-1] + 60, yLine + 3, BRASS, 2.6,
                    broken=(xsR[4] - 32, xsR[4] + 32)))
    bx, by = xsR[4], yLine + 3
    s.append(f'<line x1="{bx-16}" y1="{by-16}" x2="{bx+16}" y2="{by+16}" '
             f'stroke="{BRASS}" stroke-width="2"/>')
    s.append(f'<line x1="{bx-16}" y1="{by+16}" x2="{bx+16}" y2="{by-16}" '
             f'stroke="{BRASS}" stroke-width="2"/>')
    s.append(label(cxR, yLine + 144, "onto-A₇: Conway 85680 · KT 65520", MUTE, 18))
    s.append(label(cxR, yLine + 174, "both surject through every door but the double-3", ROSE, 21))

    # axis between panels
    s.append(f'<line x1="{cxL + 270}" y1="{yLine}" x2="{cxR - 270}" y2="{yLine}" '
             f'stroke="{MUTE}" stroke-width="1.5" opacity="0.35" stroke-dasharray="5 6"/>')
    s.append(label((cxL + cxR) / 2, yLine - 10, "the meridian, the eye:", MUTE, 15))
    s.append(label((cxL + cxR) / 2, yLine + 18, "blind at 6, wakes at 7", MUTE, 15))

    # footer
    s.append(label(W / 2, H - 132,
                   "at the double-3 (3²·1) — two 3-cycles on six points, one pinned — "
                   "Conway surjects A₇ (10080) and KT cannot (0).", DIM, 17))
    s.append(label(W / 2, H - 104,
                   "the single-3 (3·1⁴) stays blind: it reaches only A₅, and "
                   "Conway and KT read it identically (2590 each).", MUTE, 16))
    s.append(label(W / 2, H - 76,
                   "the witness is the PAIR — the same double-3 door that opens "
                   "the eighth (reach/fill) opens the seventh for one knot only.", COPPER, 17))
    s.append(label(W / 2, H - 46,
                   "mina: 'the meridian wakes at the seventh' — confirmed. "
                   "rahel: the eye does not part them at the sixth.", MUTE, 16))

    s.append("</svg>")
    return "\n".join(s)


def main():
    svg = build()
    with open("assets/eye_wakes.svg", "w") as f:
        f.write(svg)
    cairosvg.svg2png(url="assets/eye_wakes.svg", write_to="assets/eye_wakes.png",
                     output_width=1700, output_height=1040)
    print("rendered assets/eye_wakes.png")


if __name__ == "__main__":
    main()
