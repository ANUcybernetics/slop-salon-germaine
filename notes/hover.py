# heading (unwrapped, quarter-turns) along the coin's giant loop vs an iid +-1 walk of equal length. plot + two-track audio. usage: python notes/hover.py
import numpy as np, sys, wave
sys.path.insert(0, 'notes')
from walk import longest_start, walk
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
o = np.random.default_rng(7).random((192, 192)) < .5
nd, L = longest_start(o); t, _ = walk(o, nd); n = len(t)
h = np.cumsum(t); r = np.cumsum(np.random.default_rng(3).choice([-1, 1], n))
print(n, 'loop range', h.min(), h.max(), 'iid range', r.min(), r.max(), 'iid rms', np.sqrt((r**2).mean()), 'loop rms', np.sqrt((h**2).mean()))
fig, ax = plt.subplots(figsize=(10, 4.2), facecolor='#0e0e12'); ax.set_facecolor('#0e0e12')
x = np.arange(n)
ax.plot(x, r, color='#555566', lw=.7, label='coin-flip walk, same length')
ax.plot(x, h, color='#ee8a3a', lw=.9, label='heading along the giant loop')
ax.set_xlabel('steps along the curve', color='#aaa'); ax.set_ylabel('turning so far (quarter-turns)', color='#aaa')
ax.tick_params(colors='#888'); [s.set_color('#444') for s in ax.spines.values()]
ax.legend(facecolor='#0e0e12', labelcolor='#ccc', edgecolor='#444', fontsize=8, loc='lower left')
plt.tight_layout(); plt.savefig('assets/hover.png', dpi=130, facecolor=fig.get_facecolor())
# audio: pitch = heading, 60 steps/s; loop then walk, walk clipped to loop's own range
sr = 22050; spp = sr // 240
def render(hh, lo, hi):
    f = np.clip(330 * 2 ** (hh / 6.0), 40, 8000)
    fr = np.repeat(f, spp); ph = np.cumsum(2*np.pi*fr/sr)
    s = np.sin(ph) + .3*np.sin(2*ph); return s / np.abs(s).max()
a = render(h, 0, 0); b = render(r, 0, 0)
sil = np.zeros(sr//2)
y = np.concatenate([a, sil, b]); y = (y * 0.5 * 32767).astype(np.int16)
w = wave.open('assets/hover.wav', 'wb'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr); w.writeframes(y.tobytes()); w.close()
print('dur', len(y)/sr, 'loop frac clipped walk', (np.abs(r) > 20).mean())
