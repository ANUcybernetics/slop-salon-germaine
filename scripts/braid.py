#!/usr/bin/env python3
"""
germaine — "the arcs learn to cross."

A field of rows, each row a rope braid: N helical strands wound around the row's
axis, projected to the plane. In projection they weave up/down and cross; the
strand nearest the viewer (max Z) passes over, so the over/under is the
physically-correct projection of a rope braid rather than a faked weave. Same
palette and soft-neon-tube treatment as the arcs field, so the rows read as the
arcs grid finally crossing.

A painter's algorithm renders it right: depth-order only flips at an x-crossing,
so the width is split into bands at crossing x's and each band's strands are
painted back-to-front (ascending z). The over strand draws last and covers the
under strand where they overlap.

Usage:
  braid.py --frame 0                     -> one frame (braid_frame_000.png)
  braid.py --video --frames 288 --fps 24 -> encodes assets/braid.mp4
"""
import argparse
import math
import os
import sys

from PIL import Image, ImageDraw, ImageFilter

# ---- palette (sampled from assets/arcs-01.png) --------------------------------
BG = (20, 17, 21)               # near-black, faint magenta
GLOW = (150, 148, 158, 90)      # dim magenta-gray halo
MID = (205, 202, 210, 190)      # mid tube
CORE = (245, 243, 247)          # near-white heart

SS = 2                          # supersample factor


def strand_pos(theta, i, n):
    """Helical strand i at angle theta: horizontal offset and depth.

    Returns (x_offset, z) in units of the braid radius R. x_offset oscillates
    left-right as theta advances; z is the depth toward/away from the viewer.
    """
    ang = theta + 2.0 * math.pi * i / n
    return math.sin(ang), math.cos(ang)


def draw_frame(size, phase, out_path, n=3, R=0.085, pitches=2, rows=3,
               row_gap=0.28, row_phase=(0.0, 0.35, 0.7)):
    internal = size * SS
    img = Image.new("RGB", (internal, internal), BG)
    M = 600                     # samples along the horizontal axis
    THIN = 12                   # draw stride: PIL wide lines zipper on sub-px segs

    # Build one painter pass per row so each braid weaves independently. Rows sit
    # at cy_i spaced by row_gap; each gets its own phase so they never mirror.
    # The whole row set slides left by one pitch over the clip (seamless).
    R_px = R * internal
    rows_cy = [internal * (0.5 + (r - (rows - 1) / 2.0) * row_gap) for r in range(rows)]
    row_off = list(row_phase) + [row_phase[-1]] * (rows - len(row_phase))

    def row_strands(row, phase):
        """Strandi as list of (x, y, z) for one horizontal braid row."""
        cy = rows_cy[row]
        out = []
        for i in range(n):
            pts = []
            for m in range(M + 1):
                t = m / M
                x = t * internal
                theta = pitches * 2.0 * math.pi * t + phase + row_off[row]
                yo, z = strand_pos(theta, i, n)
                pts.append((x, cy + R_px * yo, z))
            out.append(pts)
        return out

    def interp(strand, x):
        """(y, z) of a strand at horizontal position x, linear interpolation."""
        lo, hi = 0, M
        while lo < hi:
            mid = (lo + hi) // 2
            if strand[mid][0] < x:
                lo = mid + 1
            else:
                hi = mid
        i = max(1, min(M, lo))
        x0, y0, z0 = strand[i - 1]
        x1, y1, z1 = strand[i]
        f = (x - x0) / (x1 - x0) if x1 != x0 else 0.0
        return y0 + f * (y1 - y0), z0 + f * (z1 - z0)

    def crossings_for(strands):
        """(x, over, under) where a pair exchanges y-order."""
        out = []
        for i in range(n):
            for j in range(i + 1, n):
                prev = strands[i][0][1] - strands[j][0][1]
                for m in range(1, M + 1):
                    cur = strands[i][m][1] - strands[j][m][1]
                    if prev == 0.0 or (prev > 0) != (cur > 0):
                        x0, x1 = strands[i][m - 1][0], strands[i][m][0]
                        frac = prev / (prev - cur) if (prev - cur) != 0 else 0.5
                        xc = x0 + frac * (x1 - x0)
                        zi, zj = strands[i][m][2], strands[j][m][2]
                        out.append((xc, i, j) if zi >= zj else (xc, j, i))
                    prev = cur
        return out

    # ---- collect painted slices for every row, in painter order --------------
    # Within a row, depth-order only flips at an x-crossing, so split the width
    # into bands at crossing x's and paint each band's strands back-to-front
    # (ascending z). The over strand draws last and covers the under strand where
    # they overlap — a real rope braid, not a cut-out.
    glow = Image.new("RGBA", (internal, internal), (0, 0, 0, 0))
    dg = ImageDraw.Draw(glow)
    mid = Image.new("RGBA", (internal, internal), (0, 0, 0, 0))
    dm = ImageDraw.Draw(mid)
    core = Image.new("RGBA", (internal, internal), (0, 0, 0, 0))
    dc = ImageDraw.Draw(core)

    for row in range(rows):
        strands = row_strands(row, phase)
        xs = sorted({xc for xc, _, _ in crossings_for(strands)})
        bounds = [0.0] + xs + [internal]
        if len(bounds) < 3:
            # no crossings (flat row) — draw each strand once
            for i in range(n):
                sp = [(p[0], p[1]) for p in strands[i]][::THIN]
                dg.line(sp, fill=GLOW, width=int(internal * 0.05), joint="curve")
                dm.line(sp, fill=MID, width=max(2, int(internal * 0.02)), joint="curve")
                dc.line(sp, fill=CORE, width=max(1, int(internal * 0.009)), joint="curve")
            continue
        for b in range(len(bounds) - 1):
            lo, hi = bounds[b], bounds[b + 1]
            mctx = (lo + hi) / 2.0
            order = sorted(
                range(n), key=lambda k: interp(strands[k], mctx)[1]
            )                       # ascending z -> far first, near last
            for i in range(n):
                pts = strands[i]
                start, end = -1, -1
                for m in range(M + 1):
                    x = pts[m][0]
                    if x >= lo and start < 0:
                        start = max(0, m - 1)
                    if x <= hi:
                        end = m + 1
                if start < 0 or end <= start:
                    continue
                raw = pts[max(0, start): min(M + 1, end)]
                sp = [(p[0], p[1]) for p in raw]
                if len(sp) > 2:
                    sp = sp[::THIN]
                    if sp[-1] != (raw[-1][0], raw[-1][1]):
                        sp.append((raw[-1][0], raw[-1][1]))
                if len(sp) >= 2:
                    dg.line(sp, fill=GLOW, width=int(internal * 0.05), joint="curve")
                    dm.line(sp, fill=MID, width=max(2, int(internal * 0.02)), joint="curve")
                    dc.line(sp, fill=CORE, width=max(1, int(internal * 0.009)), joint="curve")

    glow = glow.filter(ImageFilter.GaussianBlur(radius=internal * 0.02))
    img = img.convert("RGBA")
    img.alpha_composite(glow)
    img.alpha_composite(mid)
    img.alpha_composite(core)

    out = img.convert("RGB").resize((size, size), Image.LANCZOS)
    out.save(out_path)
    return out_path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--frame", type=int, default=0)
    ap.add_argument("--size", type=int, default=1080)
    ap.add_argument("--phase", type=float, default=None)
    ap.add_argument("--out", default=None)
    ap.add_argument("--video", action="store_true")
    ap.add_argument("--frames", type=int, default=288)
    ap.add_argument("--fps", type=int, default=24)
    args = ap.parse_args()

    if args.video:
        import tempfile
        fdir = tempfile.mkdtemp(prefix="braid_frames_")
        for i in range(args.frames):
            phase = 2 * math.pi * i / args.frames
            p = os.path.join(fdir, f"f{i:04d}.png")
            draw_frame(args.size, phase, p)
            if i % 30 == 0:
                print(f"\rframe {i}/{args.frames}", end="", flush=True)
        print()
        out = args.out or "assets/braid.mp4"
        os.system(
            f"ffmpeg -y -loglevel error -framerate {args.fps} "
            f"-i {fdir}/f%04d.png -c:v libx264 -pix_fmt yuv420p "
            f"-crf 18 -movflags +faststart {out}"
        )
        print("wrote", out)
    else:
        phase = args.phase if args.phase is not None else 0.0
        out = args.out or f"braid_frame_{args.frame:03d}.png"
        draw_frame(args.size, phase, out)
        print("wrote", out)


if __name__ == "__main__":
    main()
