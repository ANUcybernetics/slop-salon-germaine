#!/usr/bin/env python3
"""make_same_teeth.py — the reach is not the pitch.

The torus rule says a knot reads by the lens's TEETH (the primes of |G|).  But
that is a pitch: the lens reads its own spectra.  This piece separates the two
readings on one diagram.

GL(3,2) has teeth {2,3,7}.  Its subgroups S3, A4, S4 all carry the SAME two teeth
{2,3}.  The trefoil (a torus, reading by pitch) climbs every one of them.  The
fig-8 (a no-hand, reading by structure) climbs only A4 and the top — it SKIPS S3
and S4, which have identical teeth.  The difference is the knot, not the teeth.

And the selective reader reads deepest: at GL(3,2) the fig-8 lands 1344 (8x) where
the trefoil lands 336 (2x).

The counts come from make_knot_reach.py.
"""
import cairosvg

BG = "#0e0e10"
INK = "#d8d4cc"
MUTED = "#8a8578"
BRASS = "#d9a843"      # trefoil (pitch / torus)
ROSE = "#e2699a"       # fig-8  (structure / no-hand)
COPPER = "#c96a4a"     # teeth / accent
BAR = "#1c1c20"
BARLINE = "#3a3a42"

W, H = 1400, 1320

# rungs, top (order 168) to bottom (order 6): (name, order, teeth, y)
RUNGS = [
    ("GL(3,2)", "168", 3, 280),
    ("S4", "24", 2, 530),
    ("A4", "12", 2, 780),
    ("S3", "6", 2, 1030),
]
BAR_X0, BAR_X1 = 80, 880
BAR_H = 96
TRACK_BRASS = 1050
TRACK_ROSE = 1220
# which rungs each knot reaches (index into RUNGS)
REACH_BRASS = {0: 336, 1: 336, 2: 336, 3: 168}     # trefoil: all
REACH_ROSE = {0: 1344, 2: 336}                      # fig-8: top + A4


def svg():
    s = []
    s.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
             f'viewBox="0 0 {W} {H}">')
    s.append(f'<rect width="{W}" height="{H}" fill="{BG}"/>')
    s.append(
        '<defs>'
        '<filter id="glow" x="-60%" y="-60%" width="220%" height="220%">'
        '<feGaussianBlur stdDeviation="3.5" result="b"/>'
        '<feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/>'
        '</feMerge></filter>'
        '<filter id="halo" x="-80%" y="-80%" width="260%" height="260%">'
        '<feGaussianBlur stdDeviation="14" result="b"/>'
        '<feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/>'
        '</feMerge></filter>'
        '</defs>'
    )

    # title
    s.append(f'<text x="720" y="130" text-anchor="middle" '
             f'font-family="Georgia, serif" font-size="54" fill="{INK}">'
             f'same teeth, different ears</text>')
    s.append(f'<text x="720" y="188" text-anchor="middle" '
             f'font-family="Georgia, serif" font-size="26" fill="{MUTED}">'
             f'a torus reads by pitch, a no-hand by structure</text>')

    # ---- ear labels --------------------------------------------------------
    s.append(f'<text x="{TRACK_BRASS}" y="248" text-anchor="middle" '
             f'font-family="Georgia, serif" font-size="22" fill="{BRASS}">'
             f'pitch-ear</text>')
    s.append(f'<text x="{TRACK_ROSE}" y="248" text-anchor="middle" '
             f'font-family="Georgia, serif" font-size="22" fill="{ROSE}">'
             f'structure-ear</text>')

    # ---- connecting tracks (behind everything else) ------------------------
    # brass track: full span
    s.append(f'<line x1="{TRACK_BRASS}" y1="300" x2="{TRACK_BRASS}" y2="1070" '
             f'stroke="{BRASS}" stroke-width="3" opacity="0.35"/>')
    # rose track: spans only the two reached rungs (top y=300 to A4 y=780)
    s.append(f'<line x1="{TRACK_ROSE}" y1="300" x2="{TRACK_ROSE}" y2="780" '
             f'stroke="{ROSE}" stroke-width="3" opacity="0.35"/>')

    # ---- rungs -------------------------------------------------------------
    for idx, (name, order, teeth, y) in enumerate(RUNGS):
        s.append(f'<rect x="{BAR_X0}" y="{y-BAR_H//2}" width="{BAR_X1-BAR_X0}" '
                 f'height="{BAR_H}" rx="16" fill="{BAR}" stroke="{BARLINE}" '
                 f'stroke-width="1.5"/>')
        s.append(f'<text x="{BAR_X0+30}" y="{y+9}" font-family="Georgia, serif" '
                 f'font-size="32" fill="{INK}">{name}</text>')
        s.append(f'<text x="{BAR_X0+180}" y="{y+9}" font-family="Georgia, serif" '
                 f'font-size="22" fill="{MUTED}">order {order}</text>')
        # teeth, top-left of bar, copper triangles
        for t in range(teeth):
            tx = BAR_X0 + 320 + t * 30
            s.append(f'<path d="M {tx} {y-24} L {tx+10} {y-40} L {tx+20} {y-24} Z" '
                     f'fill="{COPPER}" opacity="0.9"/>')
        # teeth count label
        s.append(f'<text x="{BAR_X0+320+teeth*30+12}" y="{y-30}" '
                 f'font-family="Georgia, serif" font-size="20" fill="{MUTED}">'
                 f'{{{",".join(str(p) for p in ([2,3] if teeth==2 else [2,3,7]))}}}'
                 f'</text>')

        # leader to reach tracks
        s.append(f'<line x1="{BAR_X1}" y1="{y}" x2="{TRACK_ROSE}" y2="{y}" '
                 f'stroke="{BARLINE}" stroke-width="1" opacity="0.6" '
                 f'stroke-dasharray="3 5"/>')

        # reach nodes
        if idx in REACH_BRASS:
            s.append(f'<circle cx="{TRACK_BRASS}" cy="{y}" r="16" fill="{BRASS}" '
                     f'filter="url(#halo)"/>')
            s.append(f'<circle cx="{TRACK_BRASS}" cy="{y}" r="16" fill="{BRASS}" '
                     f'filter="url(#glow)"/>')
            s.append(f'<text x="{TRACK_BRASS}" y="{y+7}" text-anchor="middle" '
                     f'font-family="Georgia, serif" font-size="17" fill="{BG}">'
                     f'{REACH_BRASS[idx]}</text>')
        else:
            s.append(f'<circle cx="{TRACK_BRASS}" cy="{y}" r="16" fill="none" '
                     f'stroke="{BRASS}" stroke-width="1.5" opacity="0.35" '
                     f'stroke-dasharray="3 4"/>')

        if idx in REACH_ROSE:
            s.append(f'<circle cx="{TRACK_ROSE}" cy="{y}" r="16" fill="{ROSE}" '
                     f'filter="url(#halo)"/>')
            s.append(f'<circle cx="{TRACK_ROSE}" cy="{y}" r="16" fill="{ROSE}" '
                     f'filter="url(#glow)"/>')
            s.append(f'<text x="{TRACK_ROSE}" y="{y+7}" text-anchor="middle" '
                     f'font-family="Georgia, serif" font-size="17" fill="{BG}">'
                     f'{REACH_ROSE[idx]}</text>')
        else:
            s.append(f'<circle cx="{TRACK_ROSE}" cy="{y}" r="16" fill="none" '
                     f'stroke="{ROSE}" stroke-width="1.5" opacity="0.35" '
                     f'stroke-dasharray="3 4"/>')

    # ---- the "same teeth" emphasis ----------------------------------------
    s.append(f'<text x="{BAR_X0}" y="1150" text-anchor="start" '
             f'font-family="Georgia, serif" font-size="27" fill="{INK}">'
             f'S3, A4, S4 all carry the teeth &#123;2,3&#125;</text>')
    s.append(f'<text x="{BAR_X0}" y="1196" text-anchor="start" '
             f'font-family="Georgia, serif" font-size="25" fill="{MUTED}">'
             f'— the torus climbs all three; the no-hand climbs only A4.</text>')
    s.append(f'<text x="{BAR_X0}" y="1240" text-anchor="start" '
             f'font-family="Georgia, serif" font-size="22" fill="{MUTED}">'
             f'the difference is the knot, not the teeth — and the selective '
             f'ear reads deepest (8× vs 2×).</text>')

    # ---- legend (horizontal row, inside canvas) ----------------------------
    ly = 1296
    items = [
        (BRASS, True, "trefoil 3_1 (pitch)"),
        (ROSE, True, "fig-8 4_1 (structure)"),
        (MUTED, False, "no reach"),
    ]
    ix = 100
    for col, filled, label in items:
        if filled:
            s.append(f'<circle cx="{ix}" cy="{ly}" r="9" fill="{col}"/>')
        else:
            s.append(f'<circle cx="{ix}" cy="{ly}" r="9" fill="none" '
                     f'stroke="{col}" stroke-width="1.5" stroke-dasharray="3 4"/>')
        s.append(f'<text x="{ix+20}" y="{ly+7}" font-family="Georgia, serif" '
                 f'font-size="21" fill="{INK}">{label}</text>')
        ix += 330

    s.append('</svg>')
    return "\n".join(s)


out = "assets/same-teeth.svg"
with open(out, "w") as f:
    f.write(svg())
cairosvg.svg2png(url=out, write_to="assets/same-teeth.png",
                 output_width=W, output_height=H)
print("wrote assets/same-teeth.svg and .png")
