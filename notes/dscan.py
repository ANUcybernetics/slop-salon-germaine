# n vs n+d, d=2^k: residual r = de - log2(3)*do (de = evens diff, do = odds diff), spread and lattice points
import numpy as np
s=np.load('/tmp/steps.npy').astype(np.int64); o=np.load('/tmp/odds.npy').astype(np.int64)
e=s-o; L=np.log2(3); N=len(s)-1
lo=1<<10
for k in range(0,15):
    d=1<<k; n=np.arange(lo,N-d+1)
    de=e[n+d]-e[n]; do=o[n+d]-o[n]; r=de-L*do
    tot=(de+do)
    z=(do==0)&(de==0)
    ok=np.abs(r)<0.3
    nz=~z
    from collections import Counter
    c=Counter(np.abs(do[nz & ok]).tolist()).most_common(5)
    print(f"d=2^{k:2d} same {z.mean():.3f} |r|<.3 {ok.mean():.3f} median|do|(nonzero) {np.median(np.abs(do[nz])):.0f} rms r {np.sqrt((r**2).mean()):.2f} top|do| {c}")
