#!/usr/bin/env python3
"""make_fig8_sound.py — the ear reports a hand where there is none.

Two mirror words of the figure-eight knot, played as two songs:

    w  = σ₁σ₂⁻¹σ₁σ₂⁻¹   ->  A  E⁻  A  E⁻      (E⁻ glides down a fifth)
    w̄  = σ₁⁻¹σ₂σ₁⁻¹σ₂   ->  A⁻ E  A⁻ E        (A⁻ glides down a fifth)

They close to the SAME knot — the figure-eight is amphichiral, its mirror is a
no-op — yet the ear hears two different melodies, and a listener who trusts the
ear would say there are two hands.  For a chiral knot that guess is right (the
two mirror words ARE the two trefoils).  For the figure-eight it is a lie: two
songs, one knot, no hand to be lost.

Same mapping as make_sound_word.py / make_no_start_sound.py.
Builds assets/_work/*.wav, concatenates into assets/fig8-hand.wav via sox.
"""

import os
import subprocess

BASE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(BASE, "assets", "_work")
os.makedirs(WORK, exist_ok=True)

SR = "44100"
NOTE = 0.70
GAP = 0.18
BETWEEN = 2.0
LEAD = 0.6
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


# the two mirror words of the figure-eight
word_vo = voice([(A, None), (E, E_GLIDE), (A, None), (E, E_GLIDE)], "v_word")     # A E⁻ A E⁻
mirr_vo = voice([(A, A_GLIDE), (E, None), (A, A_GLIDE), (E, None)], "v_mirror")   # A⁻ E A⁻ E

lead = os.path.join(WORK, "lead.wav"); silence(lead, LEAD)
tail = os.path.join(WORK, "tail.wav"); silence(tail, TAIL)
sep = os.path.join(WORK, "sep.wav"); silence(sep, BETWEEN)

track = cat(lead, word_vo, sep, mirr_vo, tail, out=os.path.join(WORK, "track_raw.wav"))

# a low drone bed, mixed in faintly, to give the sparse notes body
dur = float(subprocess.run(["soxi", "-D", track], capture_output=True, text=True).stdout)
drone_raw = os.path.join(WORK, "drone_raw.wav")
sox("-n", "-r", SR, drone_raw, "synth", f"{dur:.3f}", "sine", "110", "fade", "0.6", "0", "0.8")
drone = os.path.join(WORK, "drone.wav")
sox(drone_raw, drone, "vol", "0.06")

final_raw = os.path.join(WORK, "final_raw.wav")
subprocess.run(["sox", "-m", track, drone, final_raw], check=True, stdout=subprocess.DEVNULL)
final = os.path.join(BASE, "assets", "fig8-hand.wav")
sox(final_raw, final, "norm")
print(f"wrote assets/fig8-hand.wav  ({dur:.2f}s)")
