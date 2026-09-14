#!/usr/bin/env python3
"""make_sound_word.py — the same song, different scores.

The trefoil is one knot in infinitely many words (a Markov class).  The eye can
see a whole knot diagram at once; the ear is bound to time and can only hear a
word, one crossing after another.  Play two of the trefoil's words and they
sound nothing alike.

Each braid generator is a note:  sigma_i is a steady tone at a pitch that
names the strand pair; sigma_i^{-1} is the same note gliding down a fifth —
the mirror, t -> 1/t, heard as a reflection.  A braid word is a sequence of
crossings, so it plays as a sequence of notes.

Four voices:
  1  sigma_1^3 (B_2)          -> trefoil.          A A A
  2  (sigma_1 sigma_2)^2 (B_3)-> trefoil.          A E A E
  3  sigma_1^2 sigma_2^2 (B_3)-> three loose loops. A A E E
  4  sigma_1^{-3} (B_2)       -> trefoil, the other hand.  A A A, falling.

Voices 1 and 2 are the same knot in different words; voices 2 and 3 have the
same note count (4) and the same exponent sum, but close to different things.
The ear that counts notes cannot tell a knot from a tangle.

Builds assets/_work/*.wav, concatenates into assets/same-song.wav via sox.
"""

import os
import subprocess

BASE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(BASE, "assets", "_work")
os.makedirs(WORK, exist_ok=True)

SR = "44100"
NOTE = 0.62   # seconds per crossing (tone)
GAP = 0.16    # silence between crossings
BETWEEN = 1.5  # silence between voices
LEAD = 0.5     # silence at the start
TAIL = 0.8     # silence at the end

# pitches (Hz): generator -> note
A = 440.0    # sigma_1 (strand pair 1-2)
E = 660.0    # sigma_2 (strand pair 2-3)
# inverse = glide down a fifth (the mirror, reflected)
A_GLIDE = A * 2 / 3   # -> 293.3
E_GLIDE = E * 2 / 3   # -> 440.0


def sox(*args):
    subprocess.run(["sox", *args], check=True, stdout=subprocess.DEVNULL)


def silence(path, dur):
    sox("-n", "-r", SR, path, "synth", f"{dur:.3f}", "sine", "0")


def note(path, freq, dur=NOTE, glide=None, decay=0.34):
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


# ---- the four voices -------------------------------------------------------
v1 = voice([(A, None), (A, None), (A, None)], "v1_s1cubed")            # sigma_1^3
v2 = voice([(A, None), (E, None), (A, None), (E, None)], "v2_alt")      # (s1 s2)^2
v3 = voice([(A, None), (A, None), (E, None), (E, None)], "v3_group")    # s1^2 s2^2
v4 = voice([(A, A_GLIDE), (A, A_GLIDE), (A, A_GLIDE)], "v4_mirror")     # s1^{-3}

# ---- assemble --------------------------------------------------------------
lead = os.path.join(WORK, "lead.wav"); silence(lead, LEAD)
tail = os.path.join(WORK, "tail.wav"); silence(tail, TAIL)
sep = os.path.join(WORK, "sep.wav"); silence(sep, BETWEEN)

track = cat(lead, v1, sep, v2, sep, v3, sep, v4, tail,
            out=os.path.join(WORK, "track_raw.wav"))

# ---- a low drone bed, mixed in faintly, to give the sparse notes body ------
dur = float(subprocess.run(["soxi", "-D", track], capture_output=True, text=True).stdout)
drone_raw = os.path.join(WORK, "drone_raw.wav")
sox("-n", "-r", SR, drone_raw, "synth", f"{dur:.3f}", "sine", "110", "fade", "0.6", "0", "0.8")
drone = os.path.join(WORK, "drone.wav")
sox(drone_raw, drone, "vol", "0.07")

final_raw = os.path.join(WORK, "final_raw.wav")
subprocess.run(["sox", "-m", track, drone, final_raw], check=True, stdout=subprocess.DEVNULL)
final = os.path.join(BASE, "assets", "same-song.wav")
sox(final_raw, final, "norm")
print(f"wrote assets/same-song.wav  ({dur:.2f}s)")
