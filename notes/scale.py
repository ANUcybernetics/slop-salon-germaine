# Rank-size of Truchet curve lengths on coin flips, many N; usage: python notes/scale.py OUT
import sys, numpy as np
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
def lengths(N, seed):
    rng = np.random.default_rng(seed)
    o = rng.random((N, N)) < .5
    # nodes: h(x,y) y in 0..N, x in 0..N-1 ; v(x,y) x in 0..N, y in 0..N-1
    H = N*(N+1); idx_h = lambda x,y: y*N+x; idx_v = lambda x,y: H + y*(N+1)+x
    par = np.arange(H + N*(N+1)); 
    def find(a):
        while par[a]!=a: par[a]=par[par[a]]; a=par[a]
        return a
    def un(a,b):
        a,b=find(a),find(b)
        if a!=b: par[a]=b
    for y in range(N):
        for x in range(N):
            n,s,w,e = idx_h(x,y), idx_h(x,y+1), idx_v(x,y), idx_v(x+1,y)
            if o[y,x]: un(n,w); un(s,e)
            else: un(n,e); un(s,w)
    roots = np.array([find(a) for a in range(len(par))])
    _, c = np.unique(roots, return_counts=True)
    return np.sort(c)[::-1]
out = sys.argv[1]
fig, ax = plt.subplots(figsize=(7,7), facecolor='#0e0e12'); ax.set_facecolor('#0e0e12')
cols = {32:'#6a7fb0',64:'#7fb0a0',128:'#d6c27a',256:'#ffecaa'}
for N in (32,64,128,256):
    reps = max(1,(256//N)**2)
    L = np.sort(np.concatenate([lengths(N, s) for s in range(reps)]))[::-1]
    r = np.arange(1,len(L)+1)/(reps*N*N)
    ax.loglog(L, r, '.', ms=3, color=cols[N], label=f'{N}x{N}')
    sel = (L>=16)&(L<N*N**.25)
    sl = np.polyfit(np.log(L[sel]), np.log(r[sel]), 1)[0]
    print(N, 'longest', L[0], 'slope', round(sl,3))
ax.set_xlabel('curve length', color='#aaa'); ax.set_ylabel('curves at least this long, per tile', color='#aaa')
ax.tick_params(colors='#888')
for s in ax.spines.values(): s.set_color('#444')
ax.legend(facecolor='#0e0e12', labelcolor='#ccc', edgecolor='#444')
plt.savefig(out, dpi=130, facecolor=fig.get_facecolor())
