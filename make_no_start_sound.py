#!/usr/bin/env python3
"""make_no_start_sound.py — the same loop, two songs, two cuts.

The trefoil's word σ₁σ₂σ₁σ₂ is a cycle in one sense (it reads the same around
its closure) but a line in the ear's sense (it has a first note).  Play it cut
at σ₁ and you get A E A E; cut at σ₂ and you get E A E A — the same cyclic
melody, the same knot, two songs.  The ear can't hear that they are one loop;
it only ever takes a line, and which note comes first is the cut, not the knot.

Each generator is a note: σ₁ = 440 (brass), σ₂ = 660 (copper).  Same mapping as
make_sound_word.py.

Builds assets/_work/*.wav, concatenates into assets/no-start.wav via sox.
"""

import os
import subprocess

BASE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(BASE, "assets", "_work")
os.makedirs(WORK, exist_ok=True)

SR = "44100"
NOTE = 0.62
GAP = 0.16
BETWEEN = 1.6
LEAD = 0.5
TAIL = 1.1

A = 440.0
E = 660.0


def sox(*args):
    subprocess.run(["sox", *args], check=True, stdout=subprocess.DEVNULL)


def silence(path, dur):
    sox("-n", "-r", SR, path, "synth", f"{dur:.3f}", "sine", "0")


def note(path, freq, dur=NOTE, decay=0.34):
    cmd = ["-n", "-r", SR, path, "synth", f"{dur:.3f}", "sine", f"{freq:.1f}",
           "fade", "0.02", "0", f"{decay:.2f}"]
    sox(*cmd)


def voice(freqs, name):
    parts = []
    for i, f in enumerate(freqs):
        nf = os.path.join(WORK, f"{name}_{i}.wav")
        note(nf, f)
        parts.append(nf)
        if i != len(freqs) - 1:
            sf = os.path.join(WORK, f"{name}_gap{i}.wav")
            silence(sf, GAP)
            parts.append(sf)
    out = os.path.join(WORK, f"{name}.wav")
    sox(*parts, out)
    return out


def cat(*files, out):
    sox(*files, out)
    return out


# two loops of the word, from each cut
cut1 = voice([A, E, A, E, A, E, A, E], "cut_s1")     # σ₁σ₂σ₁σ₂ σ₁σ₂σ₁σ₂
cut2 = voice([E, A, E, A, E, A, E, A], "cut_s2")     # σ₂σ₁σ₂σ₁ σ₂σ₁σ₂σ₁

lead = os.path.join(WORK, "lead.wav"); silence(lead, LEAD)
tail = os.path.join(WORK, "tail.wav"); silence(tail, TAIL)
gap = os.path.join(WORK, "gap.wav"); silence(gap, BETWEEN)

track = cat(lead, cut1, gap, cut2, tail, out=os.path.join(WORK, "track_raw.wav"))

# a low drone bed, faint, for body
dur = float(subprocess.run(["soxi", "-D", track], capture_output=True, text=True).stdout)
drone_raw = os.path.join(WORK, "drone_raw.wav")
sox("-n", "-r", SR, drone_raw, "synth", f"{dur:.3f}", "sine", "110", "fade", "0.6", "0", "0.8")
drone = os.path.join(WORK, "drone.wav")
sox(drone_raw, drone, "vol", "0.06")

final_raw = os.path.join(WORK, "final_raw.wav")
subprocess.run(["sox", "-m", track, drone, final_raw], check=True, stdout=subprocess.DEVNULL)
final = os.path.join(BASE, "assets", "no-start.wav")
sox(final_raw, final, "norm")
print(f"wrote assets/no-start.wav  ({dur:.2f}s)")
