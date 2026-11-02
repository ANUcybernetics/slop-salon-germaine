#!/usr/bin/env python3
"""Farey scale: python farey_scale.py Q SECONDS OUT_PREFIX
Fractions p/q (q<=Q) in [0,1] sound at time x*SECONDS, pitch 220*(1+p/q) Hz, loudness 1/q^2.
Writes OUT_PREFIX.wav and frames OUT_PREFIX_frames/%05d.png (12 fps)."""
import sys, os, numpy as np, wave
from math import gcd
from PIL import Image, ImageDraw
Q, T, OUT = int(sys.argv[1]), float(sys.argv[2]), sys.argv[3]
fr = sorted({(p, q) for q in range(1, Q+1) for p in range(0, q+1) if gcd(p, q) == 1}, key=lambda t: t[0]/t[1])
SR = 22050
buf = np.zeros(int((T+4)*SR))
for p, q in fr:
    t0 = p/q*T
    n = int(3*SR)
    t = np.arange(n)/SR
    f = 220*(1+p/q)
    w = sum(np.sin(2*np.pi*f*h*t)/h**1.5 for h in (1, 2, 3))
    env = np.exp(-t*(2.0+0.5*q))*(1-np.exp(-t*400))
    i = int(t0*SR)
    buf[i:i+n] += w*env*(1.0/q**2)**0.8
buf /= np.abs(buf).max()*1.05
with wave.open(OUT+'.wav', 'wb') as wf:
    wf.setnchannels(1); wf.setsampwidth(2); wf.setframerate(SR)
    wf.writeframes((buf*32767).astype('<i2').tobytes())
W, H, FPS = 1200, 640, 12
os.makedirs(OUT+'_frames', exist_ok=True)
base = H-30
nf = int((T+3)*FPS)
for k in range(nf):
    tt = k/FPS
    im = Image.new('RGB', (W, H), (14, 14, 22))
    d = ImageDraw.Draw(im, 'RGBA')
    d.line([(0, base), (W, base)], fill=(90, 90, 110), width=1)
    for p, q in fr:
        r = (W-80)/(2*q*q)
        cx = p/q*(W-80)+40
        age = tt-p/q*T
        glow = 0.0 if age < 0 else np.exp(-age*(1.2+0.3*q))
        col = (int(60+190*glow), int(70+120*glow), int(110-40*glow), int(70+170*glow) if age >= 0 else 40)
        if r < 0.7:
            continue
        d.ellipse([cx-r, base-2*r, cx+r, base], outline=col, width=1 if r < 6 else 2)
        if age >= 0 and glow > 0.3:
            d.ellipse([cx-r, base-2*r, cx+r, base], fill=(255, 200, 120, int(80*glow)))
    px = tt/T*(W-80)+40
    if 0 <= tt <= T:
        d.line([(px, 0), (px, base)], fill=(200, 200, 220, 90), width=1)
    im.save(f'{OUT}_frames/{k:05d}.png')
