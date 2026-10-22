# Rank-size of the Sierpinski rule vs coins on a torus. usage: python notes/sierp_plot.py OUT
import sys, numpy as np
exec("import numpy as np\nfrom scipy.sparse import coo_matrix\nfrom scipy.sparse.csgraph import connected_components\ndef lengths" + open('notes/rules.py').read().split("def lengths")[1].split("def popc")[0])
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(7,5), facecolor='#0e0e12'); ax.set_facecolor('#0e0e12')
for N, c in ((256, '#7a3b8f'), (512, '#d65f7a'), (1024, '#ffd98a')):
    I, J = np.meshgrid(np.arange(N), np.arange(N)); L = lengths((I & J) == 0)
    ax.loglog(np.arange(1, len(L)+1)[::7], L[::7]/N, color=c, label=f'(i&j)==0, side {N}')
N = 1024; L = lengths(np.random.default_rng(1).random((N, N)) < .5)
ax.loglog(np.arange(1, 20001), L[:20000]/N, color='#8899aa', label='coins, side 1024')
ax.set_xlabel('rank (longest first)', color='#aaa'); ax.set_ylabel('curve length / side', color='#aaa'); ax.tick_params(colors='#888')
for s in ax.spines.values(): s.set_color('#444')
ax.legend(facecolor='#0e0e12', labelcolor='#ccc', edgecolor='#444', fontsize=8)
plt.savefig(sys.argv[1], dpi=130, facecolor=fig.get_facecolor())
