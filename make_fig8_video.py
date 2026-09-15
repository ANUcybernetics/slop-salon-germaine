#!/usr/bin/env python3
"""make_fig8_video.py — animate the ear reporting a hand where there is none.

The static score (fig8-hand.png) is the argument.  This adds the ear: each note
disc lights up as its note plays, so the two songs unfold in time.  Frames are
drawn with PIL over the PNG, joined with the audio into assets/fig8-hand.mp4.

Timing mirrors make_fig8_sound.py exactly: lead 0.6, NOTE 0.70, GAP 0.18,
BETWEEN 2.0, tail 1.2.
"""

import os
import subprocess
from PIL import Image, ImageDraw

BASE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(BASE, "assets", "_work")
ASSETS = os.path.join(BASE, "assets")
os.makedirs(WORK, exist_ok=True)

SRC = os.path.join(ASSETS, "fig8-hand.png")
AUDIO = os.path.join(ASSETS, "fig8-hand.wav")
OUT = os.path.join(ASSETS, "fig8-hand.mp4")

NOTE, GAP, LEAD, BETWEEN, TAIL = 0.70, 0.18, 0.6, 2.0, 1.2

BRASS = (201, 162, 75)
COPPER = (198, 112, 59)
HALO = (245, 236, 200)

# note-disc positions (pixel coords in the 1300x1040 score) and their colour
# word staff (y=738): A E⁻ A E⁻   |  mirror staff (y=872): A⁻ E A⁻ E
word_mirror = [
    # (x, y, (r,g,b), start_time)
]
wx = [500, 652, 804, 956]
wy = 738
word_mirror += [(wx[0], wy + 34, BRASS, LEAD),
                (wx[1], wy - 34, COPPER, LEAD + NOTE + GAP),
                (wx[2], wy + 34, BRASS, LEAD + 2 * (NOTE + GAP)),
                (wx[3], wy - 34, COPPER, LEAD + 3 * (NOTE + GAP))]
mstart = LEAD + 4 * NOTE + 3 * GAP + BETWEEN
mwx = wx
my = 872
word_mirror += [(mwx[0], my + 34, BRASS, mstart),
                (mwx[1], my - 34, COPPER, mstart + NOTE + GAP),
                (mwx[2], my + 34, BRASS, mstart + 2 * (NOTE + GAP)),
                (mwx[3], my - 34, COPPER, mstart + 3 * (NOTE + GAP))]

TOTAL = LEAD + 2 * (4 * NOTE + 3 * GAP) + BETWEEN + TAIL
FPS = 20


def glow(draw, cx, cy, color, radius, a):
    # layered translucent rings -> a soft halo on top of the disc
    for rr, am in ((radius * 3.4, 0.18), (radius * 2.2, 0.35), (radius * 1.3, 0.75)):
        alpha = int(min(1.0, a) * am * 255)
        draw.ellipse([cx - rr, cy - rr, cx + rr, cy + rr],
                     outline=(color[0], color[1], color[2], alpha),
                     width=max(2, int(rr * 0.28)))


def frame(t):
    im = Image.open(SRC).convert("RGBA")
    layer = Image.new("RGBA", im.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    active = []
    for (x, y, c, start) in word_mirror:
        if start <= t < start + NOTE + 0.10:
            active.append((x, y))
            # fade in over the first ~0.12s of the note
            a = min(1.0, (t - start) / 0.12 + 0.4)
            glow(d, x, y, c, 15, a)
    out = Image.alpha_composite(im, layer).convert("RGB")
    return out


def main():
    frames = []
    n = int(round(TOTAL * FPS))
    for k in range(n):
        t = k / FPS
        im = frame(t)
        p = os.path.join(WORK, f"f_{k:04d}.png")
        im.save(p)
        frames.append(p)
    ffmpeg = ["ffmpeg", "-y", "-framerate", str(FPS), "-i", os.path.join(WORK, "f_%04d.png"),
              "-i", AUDIO, "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "24",
              "-c:a", "aac", "-b:a", "160k", "-shortest", "-movflags", "+faststart", OUT]
    subprocess.run(ffmpeg, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    dur = subprocess.run(["soxi", "-D", AUDIO], capture_output=True, text=True).stdout.strip()
    sz = os.path.getsize(OUT)
    print(f"wrote assets/fig8-hand.mp4  ({dur}s, {sz/1e6:.1f} MB)")


if __name__ == "__main__":
    main()
