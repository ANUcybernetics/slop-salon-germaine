# bars: share of edges per curve-length decade. usage: python notes/mass_fig.py
import numpy as np, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
exec(open('notes/mass.py').read().split("for k, g in")[0])
sel = ['coin', 'cascade q.2', 'q.02 r.6']
cols = ['#8a8a8a', '#c8962a', '#2a6f9a']
fig, ax = plt.subplots(figsize=(7, 4), dpi=150)
w = .27
for i, (k, c) in enumerate(zip(sel, cols)):
    m = mass(1024, rules[k]); ax.bar(np.arange(7) + (i-1)*w, m, w, color=c, label=k)
ax.set_xticks(range(7)); ax.set_xticklabels(['1-9', '10', '100', '1e3', '1e4', '1e5', '1e6'])
ax.set_xlabel('curve length (tiles), by decade'); ax.set_ylabel('share of all edges')
ax.legend(frameon=False); ax.spines[['top', 'right']].set_visible(False)
ax.set_title('slope -1 = equal mass per decade; flatter must climb, and the page runs out', fontsize=9, loc='left')
fig.tight_layout(); fig.savefig('assets/mass.png')
