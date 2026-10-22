# More deterministic tile rules on a torus, N=1024: slope and residual of curves>=L per tile. usage: python notes/rules2.py OUT
import sys, numpy as np
sys.argv_save = sys.argv
exec(open('notes/rules.py').read().split("def rules(N):")[0].split("def field")[0])
def ctz(a):
    a = a.copy(); c = np.zeros_like(a); a[a == 0] = 1 << 30
    while ((a & 1) == 0).any():
        m = (a & 1) == 0; c[m] += 1; a[m] >>= 1
    return c
def rules(N):
    I, J = np.meshgrid(np.arange(N), np.arange(N)); I = I.astype(np.int64); J = J.astype(np.int64)
    R = {}
    R['coin'] = np.random.default_rng(1).random((N, N)) < .5
    R['sierp (i&j)==0'] = (I & J) == 0
    R['pop(i&j)%3==0'] = popc(I & J) % 3 == 0
    R['pop(i&j)>=2'] = popc(I & J) >= 2
    R['ctz(i)+ctz(j) odd'] = ((ctz(I + 1) + ctz(J + 1)) & 1) == 1
    R['ctz(i+j+1) odd'] = (ctz(I + J + 1) & 1) == 1
    R['ctz(i^j) odd'] = (ctz(I ^ J) & 1) == 1
    R['ctz(i*j+1)'] = (ctz(I * J + 1) & 1) == 1
    R['pop(i^j)%3==0'] = popc(I ^ J) % 3 == 0
    R['(i&j)>(i^j)'] = (I & J) > (I ^ J)
    R['i*j>>10 odd'] = (((I * J) >> 10) & 1) == 1
    R['pop(i&(j<<1))odd'] = popc(I & (J << 1)) & 1 == 1
    R['pop(i&~j)odd'] = popc(I & ~J & (N - 1)) & 1 == 1
    return R
N = 1024
edges = np.unique(np.round(np.logspace(np.log10(12), np.log10(N*N/3), 20)).astype(int))
fig, ax = plt.subplots(figsize=(7,5), facecolor='#0e0e12'); ax.set_facecolor('#0e0e12')
for name, o in rules(N).items():
    L = lengths(o); T = N*N
    ge = np.array([(L >= e).sum() for e in edges]) / T
    ok = ge*T >= 5
    ls, lg = np.log(edges[ok]), np.log(ge[ok]); sel = (edges[ok] >= 30)
    if sel.sum() < 3: print(f'{name:20s} curves {len(L)} longest {L[0]} (short)'); continue
    p = np.polyfit(ls[sel], lg[sel], 1); res = np.std(lg[sel] - np.polyval(p, ls[sel]))
    print(f'{name:20s} curves {len(L):7d} longest {L[0]:8d} slope {p[0]:.2f} resid {res:.2f}')
    ax.loglog(edges[ok], ge[ok], 'o-', ms=3, label=f'{name} ({p[0]:.2f})')
ax.set_xlabel('curve length L', color='#aaa'); ax.set_ylabel('curves >= L per tile', color='#aaa'); ax.tick_params(colors='#888')
for s in ax.spines.values(): s.set_color('#444')
ax.legend(facecolor='#0e0e12', labelcolor='#ccc', edgecolor='#444', fontsize=6)
plt.savefig(sys.argv[1], dpi=130, facecolor=fig.get_facecolor())
