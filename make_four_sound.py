#!/usr/bin/env python3
"""make_four_sound.py — not two, four, and then the collapse.

The four songs of the figure-eight, as a 2x2 grid would have it: they are the
four combinations of (where it starts) x (which note glides).  Played in
sequence, the ear hears four distinct songs.  Played SIMULTANEOUSLY, the ordering
(grid row and column) cancels — you are left with the two note-classes A and E,
each plain and gliding.  All four were the same two notes all along.

Same note/glide map as make_sound_word.py / make_fig8_sound.py.  Builds
assets/_work/*.wav, concatenates/mixes into assets/four-songs.wav via sox.
"""

import os
import subprocess
import json

BASE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(BASE, "assets", "_work")
os.makedirs(WORK, exist_ok=True)

SR = "44100"
NOTE = 0.70
GAP = 0.18
BETWEEN = 0.7
LEAD = 0.5
TAIL = 1.0

A = 440.0
E = 660.0
A_GLIDE = A * 2 / 3     # -> 293.3
E_GLIDE = E * 2 / 3     # -> 440.0


def sox(*args):
    subprocess.run(["sox", *args], check=True, stdout=subprocess.DEVNULL)


def silence(path, dur):
    sox("-n", "-r", SR, path, "synth", f"{dur:.3f}", "sine", "0")


def note(path, freq, glide=None, dur=NOTE, decay=0.34):
    cmd = ["-n", "-r", SR, path, "synth", f"{dur:.3f}", "sine"]
    if glide is None:
        cmd.append(f"{freq:.1f}")
    else:
        cmd.append(f"{freq:.1f}:{glide:.1f}")
    cmd += ["fade", "0.02", "0", f"{decay:.2f}"]
    sox(*cmd)


def voice(seq, name):
    """seq: list of (freq, glide_or_None).  Build the wav for one braid word."""
    parts = []
    for i, (freq, glide) in enumerate(seq):
        nf = os.path.join(WORK, f"{name}_{i}.wav")
        note(nf, freq, glide=glide)
        parts.append(nf)
        if i != len(seq) - 1:
            sf = os.path.join(WORK, f"{name}_gap{i}.wav")
            silence(sf, GAP)
            parts.append(sf)
    out = os.path.join(WORK, f"{name}.wav")
    sox(*parts, out)
    return out


def cat(*files, out):
    sox(*files, out)
    return out


# the four songs: (where it starts) x (which note glides)
songs = {
    "w":    [(A, None),      (E, E_GLIDE),  (A, None),      (E, E_GLIDE)],   # A  E⁻ A  E⁻
    "Rw":   [(E, E_GLIDE),   (A, None),     (E, E_GLIDE),   (A, None)],      # E⁻ A  E⁻ A
    "Mw":   [(A, A_GLIDE),   (E, None),     (A, A_GLIDE),   (E, None)],      # A⁻ E  A⁻ E
    "RMw":  [(E, None),      (A, A_GLIDE),  (E, None),      (A, A_GLIDE)],   # E  A⁻ E  A⁻
}
voices = {k: voice(seq, "v_" + k) for k, seq in songs.items()}

lead = os.path.join(WORK, "lead.wav"); silence(lead, LEAD)
tail = os.path.join(WORK, "tail.wav"); silence(tail, TAIL)

parts = [lead]
for i, k in enumerate(["w", "Rw", "Mw", "RMw"]):
    parts.append(voices[k])
    if i < 3:
        g = os.path.join(WORK, f"songgap{i}.wav")
        silence(g, BETWEEN)
        parts.append(g)
seq_out = os.path.join(WORK, "track_seq.wav")
cat(*parts, out=seq_out)

dur = float(subprocess.run(["soxi", "-D", seq_out], capture_output=True, text=True).stdout)

# the overlay: all four songs mixed, simultaneous.  the ordering cancels.
mix_parts = [voices[k] for k in songs]
overlay_raw = os.path.join(WORK, "overlay_raw.wav")
subprocess.run(["sox", "-m", *mix_parts, overlay_raw], check=True, stdout=subprocess.DEVNULL)
overlay = os.path.join(WORK, "overlay.wav")
sox(overlay_raw, overlay, "vol", "0.5")
soxi = subprocess.run(["soxi", "-D", overlay], capture_output=True, text=True).stdout
olat = float(soxi)

# assemble: sequence, then a short beat, then the overlay, then tail
beat = os.path.join(WORK, "beat.wav"); silence(beat, 1.0)
final_raw = os.path.join(WORK, "final_raw.wav")
cat(seq_out, beat, overlay, tail, out=final_raw)
final = os.path.join(BASE, "assets", "four-songs.wav")
sox(final_raw, final, "norm")

with open(os.path.join(WORK, "four_songs_timing.json"), "w") as f:
    json.dump({"lead": LEAD, "note": NOTE, "gap": GAP, "between": BETWEEN,
               "overlay_start": LEAD + 4 * (4 * NOTE + 3 * GAP) + 3 * BETWEEN + 1.0,
               "tail": TAIL, "song_len": 4 * NOTE + 3 * GAP}, f)
print(f"wrote assets/four-songs.wav  (seq {dur:.2f}s + beat + overlay {olat:.2f}s)")
