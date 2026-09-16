#!/usr/bin/env python3
"""make_relation_video.py — the relation, moved.

The static piece (relation.png) is the argument.  This adds the ear and the
motion: as the relation plays, the score's note-heads light in sync — A·E·A for
the first word, E·A·E for the second.  The ear hears two tunes; the two words
are one element.  Frames are PIL over the PNG, joined with the audio via ffmpeg.

Timing mirrors make_relation_sound.py exactly.
"""

import os
import subprocess
from PIL import Image, ImageDraw

BASE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(BASE, "assets", "_work")
ASSETS = os.path.join(BASE, "assets")

SRC = os.path.join(ASSETS, "relation.png")
AUDIO = os.path.join(ASSETS, "relation.wav")
OUT = os.path.join(ASSETS, "relation.mp4")

NOTE, GAP, BETWEEN, LEAD = 0.70, 0.18, 1.4, 0.5
FPS = 20

BRASS = (201, 162, 75)
COPPER = (198, 112, 59)

# note-head screen positions, from make_relation.py's layout (left cx=400,
# right cx=1200, score cy=700, y_hi=660, y_lo=726)
LEFT = [((308, 726), "A"), ((400, 660), "E"), ((492, 726), "A")]     # sigma_1s2s1  A·E·A
RIGHT = [((1108, 660), "E"), ((1200, 726), "A"), ((1292, 660), "E")]  # sigma_2s1s2  E·A·E

W1_START = LEAD                       # word 1 begins
W2_START = LEAD + (3 * NOTE + 2 * GAP) + BETWEEN   # word 2 begins


def glow(d, cx, cy, color, radius, a):
    for rr, am in ((radius * 3.4, 0.16), (radius * 2.2, 0.34), (radius * 1.3, 0.72)):
        alpha = int(min(1.0, a) * am * 255)
        d.ellipse([cx - rr, cy - rr, cx + rr, cy + rr],
                  outline=(color[0], color[1], color[2], alpha),
                  width=max(2, int(rr * 0.26)))


def frame(t):
    im = Image.open(SRC).convert("RGBA")
    layer = Image.new("RGBA", im.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    # word 1 (left)
    for i, ((x, y), k) in enumerate(LEFT):
        st = W1_START + i * (NOTE + GAP)
        if st <= t < st + NOTE + 0.12:
            col = BRASS if k == "A" else COPPER
            glow(d, x, y, col, 16, (t - st) / 0.12 + 0.35)
    # word 2 (right)
    for i, ((x, y), k) in enumerate(RIGHT):
        st = W2_START + i * (NOTE + GAP)
        if st <= t < st + NOTE + 0.12:
            col = BRASS if k == "A" else COPPER
            glow(d, x, y, col, 16, (t - st) / 0.12 + 0.35)
    out = Image.alpha_composite(im, layer).convert("RGB")
    return out


def main():
    dur = float(subprocess.run(["soxi", "-D", AUDIO], capture_output=True, text=True).stdout)
    frames = []
    n = int(round(dur * FPS))
    for k in range(n):
        im = frame(k / FPS)
        p = os.path.join(WORK, f"relf_{k:04d}.png")
        im.save(p)
        frames.append(p)
    ffmpeg = ["ffmpeg", "-y", "-framerate", str(FPS), "-i", os.path.join(WORK, "relf_%04d.png"),
              "-i", AUDIO, "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "24",
              "-c:a", "aac", "-b:a", "160k", "-shortest", "-movflags", "+faststart", OUT]
    subprocess.run(ffmpeg, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    sz = os.path.getsize(OUT)
    print(f"wrote assets/relation.mp4  ({dur:.2f}s, {sz/1e6:.2f} MB)")


if __name__ == "__main__":
    main()
