#!/usr/bin/env python3
"""make_meridian_lock.py — the trefoil climbs two rungs; the lock is the meridian's
height.

Single trefoil in A_7 (|Hom| = 40320 = 16 x 2520):
  reaches A_5 (7560) and PSL(2,7) (10080), blind to A_6 and A_7.
  The A_5-doors always sit at meridian order 5; the PSL(2,7)-doors at meridian
  order 7 — they never share a meridian, so even though <A_5,PSL(2,7)> = A_7,
  the trefoil cannot reach A_7 that way.

Amalgamated trefoil#trefoil (join of meridian-sharing images):
  <A_5,A_5> -> A_6 (1008) and A_7 (504);  <PSL(2,7),PSL(2,7)> -> A_7 (720).
  The self-sum climbs TWO rungs: A_5 -> A_6 -> A_7.

A triptych: the meridian is a vertical axis, its ORDER the height. A lit room is
reached; a dark one is blind.  PSL(2,7) (the Fano plane, order 168) sits inside
A_7 (order 2520) — the star inside the dark heptagon.
"""
import math

W, H = 1500, 940
BG = "#08080d"
BRASS = "#d9a84f"
COPPER = "#c47b5a"
ROSE = "#c86b86"
DARK = "#2c2430"
MUTE = "#4a3f4a"

# height -> y (higher order = higher up)
H5, H6, H7 = 762, 600, 438
def Y(h): return {5: H5, 6: H6, 7: H7}[h]

def poly(cx, cy, rad, n, rot=-90.0):
    pts = []
    for k in range(n):
        a = math.radians(rot + k * 360.0 / n)
        pts.append((cx + rad * math.cos(a), cy + rad * math.sin(a)))
    return " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)

def star(cx, cy, rad, n=7, rot=-90.0):
    pts = []
    for k in range(2 * n):
        a = math.radians(rot + k * 180.0 / n)
        r = rad if k % 2 == 0 else rad * 0.42
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)

def glow(points, color, on=True, width=3.5, fill=0.06):
    if on:
        return (f'<polygon points="{points}" fill="none" stroke="{color}" stroke-width="{width*3}" '
                f'stroke-linejoin="round" opacity="0.18" filter="url(#soft)"/>\n'
                f'<polygon points="{points}" fill="none" stroke="{color}" stroke-width="{width}" '
                f'stroke-linejoin="round"/>\n'
                f'<polygon points="{points}" fill="{color}" opacity="{fill}"/>\n')
    return (f'<polygon points="{points}" fill="none" stroke="{DARK}" stroke-width="{width*3}" '
            f'stroke-linejoin="round" opacity="0.30" filter="url(#soft)"/>\n'
            f'<polygon points="{points}" fill="none" stroke="{DARK}" stroke-width="{width}" '
            f'stroke-linejoin="round" opacity="0.8"/>\n')

def axis(x, color):
    return (f'<line x1="{x}" y1="200" x2="{x}" y2="790" stroke="{MUTE}" stroke-width="2" opacity="0.7"/>\n'
            f'<line x1="{x-10}" y1="{H5}" x2="{x+10}" y2="{H5}" stroke="{MUTE}" stroke-width="1.5" opacity="0.6"/>\n'
            f'<line x1="{x-10}" y1="{H6}" x2="{x+10}" y2="{H6}" stroke="{MUTE}" stroke-width="1.5" opacity="0.6"/>\n'
            f'<line x1="{x-10}" y1="{H7}" x2="{x+10}" y2="{H7}" stroke="{MUTE}" stroke-width="1.5" opacity="0.6"/>\n'
            f'<text x="{x-92}" y="{H5+5}" text-anchor="end" font-family="monospace" font-size="14" fill="{MUTE}">5</text>\n'
            f'<text x="{x-92}" y="{H6+5}" text-anchor="end" font-family="monospace" font-size="14" fill="{MUTE}">6</text>\n'
            f'<text x="{x-92}" y="{H7+5}" text-anchor="end" font-family="monospace" font-size="14" fill="{MUTE}">7</text>\n')

def header(x, title, sub, color):
    return (f'<text x="{x}" y="150" text-anchor="middle" font-family="monospace" font-size="23" fill="{color}">{title}</text>\n'
            f'<text x="{x}" y="176" text-anchor="middle" font-family="monospace" font-size="14" fill="{MUTE}">{sub}</text>\n')

def room(x, h, n, rad, color, on, label, labcolor=None):
    s = glow(poly(x, Y(h), rad, n), color, on)
    s += f'<text x="{x}" y="{Y(h)+rad+18}" text-anchor="middle" font-family="monospace" font-size="15" fill="{labcolor or (color if on else MUTE)}">{label}</text>\n'
    return s

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<defs><filter id="soft" x="-40%" y="-40%" width="180%" height="180%"><feGaussianBlur stdDeviation="5"/></filter></defs>
<rect width="{W}" height="{H}" fill="{BG}"/>
<text x="750" y="46" text-anchor="middle" font-family="monospace" font-size="28" fill="{ROSE}">the lock is the meridian's height</text>
<text x="750" y="78" text-anchor="middle" font-family="monospace" font-size="16" fill="{MUTE}">the trefoil's A₅-doors sit at order 5, its PSL(2,7)-doors at order 7 — and the sum climbs two rungs</text>
'''

# ---- Panel 1: the trefoil alone ----
x = 250
svg += header(x, "trefoil alone", "16× = 40320 in A₇", BRASS)
svg += axis(x, BRASS)
svg += room(x, 5, 5, 46, BRASS, True, "A₅")                       # pentagon, reached
svg += room(x, 6, 6, 50, BRASS, False, "A₆")                      # hexagon, blind
svg += room(x, 7, 7, 54, BRASS, False, "A₇")                      # heptagon, blind
# star (PSL(2,7)) glowing inside the dark A_7
svg += glow(star(x, Y(7), 26), BRASS, True, 3, 0.08)
svg += f'<text x="{x+62}" y="{Y(7)+4}" font-family="monospace" font-size="13" fill="{BRASS}">PSL(2,7)</text>\n'

# ---- Panel 2: the lock ----
x = 750
svg += header(x, "the lock", "⟨A₅, PSL(2,7)⟩ = A₇, but no shared meridian", COPPER)
svg += axis(x, COPPER)
svg += room(x, 5, 5, 46, COPPER, True, "A₅")
svg += room(x, 6, 6, 50, COPPER, False, "A₆")
svg += room(x, 7, 7, 54, COPPER, True, "A₇")                       # A_7 reached by the join
svg += glow(star(x, Y(7), 26), COPPER, True, 3, 0.08)
svg += f'<text x="{x+62}" y="{Y(7)+4}" font-family="monospace" font-size="13" fill="{COPPER}">PSL(2,7)</text>\n'
# a lock bar between height 5 and 7: the doors never share a meridian
svg += (f'<line x1="{x-58}" y1="694" x2="{x+58}" y2="694" stroke="{DARK}" stroke-width="8" opacity="0.85"/>\n'
        f'<line x1="{x-58}" y1="712" x2="{x+58}" y2="712" stroke="{DARK}" stroke-width="8" opacity="0.85"/>\n'
        f'<text x="{x}" y="678" text-anchor="middle" font-family="monospace" font-size="13" fill="{COPPER}">meridian order 5 ≠ 7</text>\n')

# ---- Panel 3: the climb ----
x = 1250
svg += header(x, "the climb", "trefoil#trefoil → A₆ and A₇", ROSE)
svg += axis(x, ROSE)
# two A5 pentagons at height 5 joining to A6
svg += glow(poly(x-46, Y(5), 34, 5), ROSE, True, 3, 0.08)
svg += glow(poly(x+46, Y(5), 34, 5), ROSE, True, 3, 0.08)
svg += room(x, 6, 6, 50, ROSE, True, "A₆")
svg += room(x, 7, 7, 54, ROSE, True, "A₇")
svg += glow(star(x, Y(7), 26), ROSE, True, 3, 0.08)
# arcs: two A5 -> A6 ; two PSL -> A7
svg += (f'<path d="M {x-46} {Y(5)} C {x-80} {(H5+H6)//2} {x-46} {(H5+H6)//2} {x} {Y(6)}" fill="none" stroke="{ROSE}" stroke-width="2" opacity="0.5"/>\n'
        f'<path d="M {x+46} {Y(5)} C {x+80} {(H5+H6)//2} {x+46} {(H5+H6)//2} {x} {Y(6)}" fill="none" stroke="{ROSE}" stroke-width="2" opacity="0.5"/>\n'
        f'<path d="M {x-30} {Y(7)} C {x-70} {Y(7)-20} {x+70} {Y(7)-20} {x+30} {Y(7)}" fill="none" stroke="{ROSE}" stroke-width="2" opacity="0.4"/>\n')

svg += '</svg>'

with open("assets/meridian_lock.svg", "w") as f:
    f.write(svg)
print("wrote assets/meridian_lock.svg")
