#!/usr/bin/env python3
"""
germaine — "thirty-six arcs between fixed points. only the bend varies."

Six-by-six grid of thin glowing arcs on a near-black ground. Each arc connects a
fixed left point to a fixed right point of its cell; a smooth wave field sets how
the strand drifts vertically and how it bows. Advancing the wave phase moves the
bend through the grid.

Usage:
  arcs_bend.py --frame 0                     -> one frame (arcs_frame_000.png)
  arcs_bend.py --video --frames 360 --fps 24 -> encodes arcs.mp4
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

GRID = 6                        # arcs per side (six-by-six)
SS = 2                          # supersample factor


def bezier_pts(p0, p1, p2, n=48):
    """Quadratic Bezier -> list of (x, y)."""
    out = []
    for i in range(n + 1):
        t = i / n
        mt = 1.0 - t
        x = mt * mt * p0[0] + 2 * mt * t * p1[0] + t * t * p2[0]
        y = mt * mt * p0[1] + 2 * mt * t * p1[1] + t * t * p2[1]
        out.append((x, y))
    return out


def arc_points(c, r, off, bend, cell):
    """Left/right fixed points of a cell, control point displaced by bend.

    off  : vertical drift of the whole strand (baseline), in cell units
    bend : sagitta of the midpoint (bows the arc), in cell units
    """
    x0, y0 = c * cell, (r + 0.5) * cell + off * cell
    x1 = (c + 1) * cell
    # control point sits at the chord midpoint, pushed off the chord by 2*bend
    cx = (x0 + x1) / 2
    cy = y0 + 2 * bend * cell
    return bezier_pts((x0, y0), (cx, cy), (x1, y0))


def wave(phase, r, c, amp_o=0.34, amp_b=0.09,
         kr_o=0.52, kc_o=0.0, kr_b=0.0, kc_b=1.05, delta=0.9):
    """Two gentle traveling waves. Off drifts the strand vertically (rows bob);
    bend slides a soft scallop along the rows. Advancing phase moves the crest."""
    po = kr_o * r + kc_o * c - phase
    pb = kr_b * r + kc_b * c - phase + delta
    off = amp_o * math.cos(po)
    bend = amp_b * math.cos(pb)
    return off, bend


def draw_frame(size, phase, out_path):
    internal = size * SS
    img = Image.new("RGB", (internal, internal), BG)
    cell = internal / GRID

    # collect all polylines once, at this phase
    strands = []
    for r in range(GRID):
        for c in range(GRID):
            off, bend = wave(phase, r, c)
            strands.append(arc_points(c, r, off, bend, cell))

    # --- glow layer: wide faint blur, to get the soft tube ---
    glow = Image.new("RGBA", (internal, internal), (0, 0, 0, 0))
    dg = ImageDraw.Draw(glow)
    for pts in strands:
        dg.line(pts, fill=GLOW, width=int(cell * 0.055), joint="curve")
    glow = glow.filter(ImageFilter.GaussianBlur(radius=cell * 0.028))

    # --- mid + core layers: increasingly tight brighter strokes ---
    mid = Image.new("RGBA", (internal, internal), (0, 0, 0, 0))
    dm = ImageDraw.Draw(mid)
    for pts in strands:
        dm.line(pts, fill=MID, width=max(2, int(cell * 0.02)), joint="curve")
    core = Image.new("RGBA", (internal, internal), (0, 0, 0, 0))
    dc = ImageDraw.Draw(core)
    for pts in strands:
        dc.line(pts, fill=CORE, width=max(1, int(cell * 0.009)), joint="curve")

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
    ap.add_argument("--frames", type=int, default=360)
    ap.add_argument("--fps", type=int, default=24)
    args = ap.parse_args()

    if args.video:
        import tempfile
        fdir = tempfile.mkdtemp(prefix="arcs_frames_")
        # seamless loop: phase advances by a full period over the clip
        for i in range(args.frames):
            phase = 2 * math.pi * i / args.frames
            p = os.path.join(fdir, f"f{i:04d}.png")
            draw_frame(args.size, phase, p)
            if i % 30 == 0:
                print(f"\rframe {i}/{args.frames}", end="", flush=True)
        print()
        out = args.out or "assets/arcs_bend.mp4"
        os.system(
            f"ffmpeg -y -loglevel error -framerate {args.fps} "
            f"-i {fdir}/f%04d.png -c:v libx264 -pix_fmt yuv420p "
            f"-crf 18 -movflags +faststart {out}"
        )
        print("wrote", out)
    else:
        phase = args.phase if args.phase is not None else 0.0
        out = args.out or f"arcs_frame_{args.frame:03d}.png"
        draw_frame(args.size, phase, out)
        print("wrote", out)


if __name__ == "__main__":
    main()
