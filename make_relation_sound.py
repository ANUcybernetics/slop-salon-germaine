#!/usr/bin/env python3
"""make_relation_sound.py — the relation, heard.

The static piece shows the words; this plays them.  Two words, one element:
sigma_1 sigma_2 sigma_1 (A·E·A) then sigma_2 sigma_1 sigma_2 (E·A·E).  The ear
hears two tunes; the group knows they are one.  Same note/glide map as
make_sound_word.py.  Builds assets/_work/*.wav, concatenates into
assets/relation.wav via sox.
"""

import os
import subprocess

BASE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(BASE, "assets", "_work")
os.makedirs(WORK, exist_ok=True)

SR = "44100"
NOTE = 0.70
GAP = 0.18
BETWEEN = 1.4
LEAD = 0.5
TAIL = 1.2

A = 440.0
E = 660.0
A_GLIDE = A * 2 / 3   # -> 293.3
E_GLIDE = E * 2 / 3   # -> 440.0


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


# the two words of the relation
w1 = voice([(A, None), (E, None), (A, None)], "rel_w1")     # sigma_1 sigma_2 sigma_1
w2 = voice([(E, None), (A, None), (E, None)], "rel_w2")     # sigma_2 sigma_1 sigma_2

lead = os.path.join(WORK, "rel_lead.wav"); silence(lead, LEAD)
tail = os.path.join(WORK, "rel_tail.wav"); silence(tail, TAIL)
between = os.path.join(WORK, "rel_between.wav"); silence(between, BETWEEN)

track = cat(lead, w1, between, w2, tail, out=os.path.join(WORK, "rel_track_raw.wav"))

# a low drone bed, mixed faintly, for body
dur = float(subprocess.run(["soxi", "-D", track], capture_output=True, text=True).stdout)
drone_raw = os.path.join(WORK, "rel_drone_raw.wav")
sox("-n", "-r", SR, drone_raw, "synth", f"{dur:.3f}", "sine", "110", "fade", "0.6", "0", "0.9")
drone = os.path.join(WORK, "rel_drone.wav")
sox(drone_raw, drone, "vol", "0.06")

final_raw = os.path.join(WORK, "rel_final_raw.wav")
subprocess.run(["sox", "-m", track, drone, final_raw], check=True, stdout=subprocess.DEVNULL)
final = os.path.join(BASE, "assets", "relation.wav")
sox(final_raw, final, "norm")
print(f"wrote assets/relation.wav  ({dur:.2f}s)")
