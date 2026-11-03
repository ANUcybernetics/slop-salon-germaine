#!/usr/bin/env python3
"""Convergent melody: python cfmelody.py SECONDS OUT_PREFIX
Four numbers (phi, sqrt2, e, pi), each a voice. Convergent n of x sounds at time ln(q_n)*scale,
pitch 220*2^(frac(p/q)) ... Rows show the convergent's offset from x on a log scale.
Writes OUT.wav and OUT_frames/%05d.png (12 fps)."""
import sys, os, numpy as np, wave
from math import isqrt, log, log10
from fractions import Fraction
from PIL import Image, ImageDraw, ImageFont
T, OUT = float(sys.argv[1]), sys.argv[2]
def cf_of(num, den, n):
    a = []
    for _ in range(n):
        if den == 0: break
        q = num // den; a.append(q); num, den = den, num - q*den
    return a
D = 10**400
phi = cf_of(D + isqrt(5*D*D), 2*D, 120)
s2 = cf_of(isqrt(2*D*D), D, 120)
e_a = [2]
for k in range(1, 60): e_a += [1, 2*k, 1]
def arctan_inv(x, P):
    s = t = P//x; x2 = x*x; n = 1; sign = 1
    while t:
        t //= x2; n += 2; sign = -sign; s += sign*(t//n)
    return s
P = 10**420
pi = cf_of(4*(4*arctan_inv(5, P) - arctan_inv(239, P)), P, 100)
def conv(a):
    out = []; p0, q0, p1, q1 = 1, 0, a[0], 1
    out.append((p1, q1))
    for x in a[1:]:
        p0, q0, p1, q1 = p1, q1, x*p1+p0, x*q1+q0
        out.append((p1, q1))
    return out
voices = [("phi", phi), ("sqrt 2", s2), ("e", e_a), ("pi", pi)]
cv = [(n, conv(a)) for n, a in voices]
lnq_max = 22.0
scale = T/lnq_max
SR = 22050
buf = np.zeros(int((T+4)*SR))
base = [220, 220, 220, 220]
for vi, (name, c) in enumerate(cv):
    for n, (p, q) in enumerate(c):
        lq = log(q) if q > 1 else 0.0
        t0 = lq*scale
        if t0 > T: break
        fr = float(Fraction(p, q) % 1)
        f = 220*2**fr*(0.5 if vi < 2 else 1)
        m = int(1.6*SR); t = np.arange(m)/SR
        w = np.sin(2*np.pi*f*t)+0.4*np.sin(2*np.pi*2*f*t)
        env = np.exp(-t*3.0)*(1-np.exp(-t*300))
        i = int(t0*SR); buf[i:i+m] += w*env*0.5
buf /= np.abs(buf).max()*1.05
with wave.open(OUT+'.wav', 'wb') as wf:
    wf.setnchannels(1); wf.setsampwidth(2); wf.setframerate(SR)
    wf.writeframes((buf*32767).astype('<i2').tobytes())
# frames: x = ln q (time), y = -log10|x - p/q| per convergent, one row per voice
W, H, FPS = 1200, 720, 12
os.makedirs(OUT+'_frames', exist_ok=True)
exact = [phi, s2, e_a, pi]
def val(a):  # high-precision value as Fraction from long CF
    return conv(a)[-1]
def log10x(fr):
    return -(log10(fr.numerator) - log10(fr.denominator)) if fr.numerator < 10**300 and fr.denominator < 10**300 else -(len(str(fr.numerator))-len(str(fr.denominator)))
pts = []
for vi, (name, c) in enumerate(cv):
    pf = Fraction(*val(voices[vi][1]))
    row = []
    for p, q in c:
        if q < 2 and p == 0: continue
        err = abs(Fraction(p, q) - pf)
        if err == 0: continue
        row.append((log(q) if q > 1 else 0.0, log10x(err*q*q)))
    pts.append(row)
font = ImageFont.load_default()
cols = [(240, 200, 120), (130, 220, 180), (150, 170, 250), (250, 140, 160)]
rowh = H//4
for k in range(int((T+3)*FPS)):
    tt = k/FPS
    im = Image.new('RGB', (W, H), (14, 14, 22)); d = ImageDraw.Draw(im, 'RGBA')
    for vi, row in enumerate(pts):
        y0 = vi*rowh + 14; y1 = (vi+1)*rowh - 14
        d.line([(60, y1), (W-30, y1)], fill=(60, 60, 80), width=1)
        d.text((12, y0), voices[vi][0], fill=cols[vi], font=font)
        prev = None
        for lq, ye in row:
            ts = lq*scale
            if ts > T: break
            x = 60 + lq/lnq_max*(W-90)
            y = y1 - (ye+0.6)/3.4*(y1-y0-10)
            age = tt-ts
            if age < 0: break
            g = np.exp(-age*2.2)
            c = cols[vi]
            if prev: d.line([prev, (x, y)], fill=c+(90,), width=1)
            r = 3+6*g
            d.ellipse([x-r, y-r, x+r, y+r], fill=c+(int(110+140*g),))
            prev = (x, y)
    d.text((W-300, H-14), "x: ln q (= time)    y: digits gained over 1/q^2", fill=(130, 130, 150), font=font)
    im.save(f'{OUT}_frames/{k:05d}.png')
