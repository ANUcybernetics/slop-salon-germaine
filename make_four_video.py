#!/usr/bin/env python3
"""make_four_video.py — animate the 2x2 grid of songs.

The static score (four-songs.png) is the argument.  This adds the ear: in the
sequence each cell's discs light as its song plays (top-left, bottom-left,
top-right, bottom-right); at the overlay ALL sixteen light at once, because the
four songs have become the two note-classes.  Frames are PIL over the PNG, joined
with the audio into assets/four-songs.mp4.

Timing mirrors make_four_sound.py exactly.
"""

import os
import subprocess
import json
from PIL import Image, ImageDraw

BASE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(BASE, "assets", "_work")
ASSETS = os.path.join(BASE, "assets")
os.makedirs(WORK, exist_ok=True)

SRC = os.path.join(ASSETS, "four-songs.png")
AUDIO = os.path.join(ASSETS, "four-songs.wav")
OUT = os.path.join(ASSETS, "four-songs.mp4")
LAYOUT = os.path.join(WORK, "four_songs_layout.json")
TIMING = os.path.join(WORK, "four_songs_timing.json")

NOTE, GAP = 0.70, 0.18
FPS = 20

BRASS = (201, 162, 75)
COPPER = (198, 112, 59)

with open(LAYOUT) as f:
    layout = json.load(f)
with open(TIMING) as f:
    timing = json.load(f)

LEAD = timing["lead"]
BETWEEN = timing["between"]
OVL = timing["overlay_start"]
SONG_LEN = timing["song_len"]

# the four songs in playback order and their cells
ORDER_KEYS = ["w", "Rw", "Mw", "RMw"]
SONG = layout["disc_pos"]

# (letter) -> colour, so the overlay lights the right ones
CELL_META = {
    "w":    ["A", "E", "A", "E"],
    "Rw":   ["E", "A", "E", "A"],
    "Mw":   ["A", "E", "A", "E"],
    "RMw":  ["E", "A", "E", "A"],
}


def song_start(seq_idx):
    return LEAD + seq_idx * (SONG_LEN + BETWEEN)


def glow(d, cx, cy, color, radius, a):
    for rr, am in ((radius * 3.4, 0.18), (radius * 2.2, 0.35), (radius * 1.3, 0.75)):
        alpha = int(min(1.0, a) * am * 255)
        d.ellipse([cx - rr, cy - rr, cx + rr, cy + rr],
                  outline=(color[0], color[1], color[2], alpha),
                  width=max(2, int(rr * 0.28)))


def frame(t):
    im = Image.open(SRC).convert("RGBA")
    layer = Image.new("RGBA", im.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    events = []
    # the sequence: one song at a time, note i starts at song_start + i*(NOTE+GAP)
    for si, key in enumerate(ORDER_KEYS):
        st = song_start(si)
        for i, (x, y) in enumerate(SONG[key]["discs"]):
            nstart = st + i * (NOTE + GAP)
            if nstart <= t < nstart + NOTE + 0.10:
                col = BRASS if CELL_META[key][i] == "A" else COPPER
                events.append((x, y, col, (t - nstart) / 0.12 + 0.4))
    # the overlay: all sixteen at once, the four collapsed
    if OVL <= t < OVL + SONG_LEN + 0.10:
        for key in ORDER_KEYS:
            for i, (x, y) in enumerate(SONG[key]["discs"]):
                col = BRASS if CELL_META[key][i] == "A" else COPPER
                a = min(1.0, (t - OVL) / 0.25 + 0.5)
                events.append((x, y, col, a))
    for (x, y, col, a) in events:
        glow(d, x, y, col, 15, a)
    out = Image.alpha_composite(im, layer).convert("RGB")
    return out


def main():
    dur = float(subprocess.run(["soxi", "-D", AUDIO], capture_output=True, text=True).stdout)
    frames = []
    n = int(round(dur * FPS))
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
    sz = os.path.getsize(OUT)
    print(f"wrote assets/four-songs.mp4  ({dur:.2f}s, {sz/1e6:.2f} MB)")


if __name__ == "__main__":
    main()
