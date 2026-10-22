# Sierpinski tile rule (i&j)==0 on a torus: exact curve-length ladder per side. usage: python notes/sierp.py
import numpy as np, collections
exec(open('notes/rules.py').read().split("def popc")[0].split("import matplotlib")[0])
exec("def lengths" + open('notes/rules.py').read().split("def lengths")[1].split("def popc")[0])
for N in (16, 32, 64, 128, 256, 512, 1024):
    I, J = np.meshgrid(np.arange(N), np.arange(N))
    L = lengths((I & J) == 0)
    c = sorted(collections.Counter(L.tolist()).items(), reverse=True)
    print(N, len(L), c[:8])
print('count >= L, absolute, vs L/N')
for N in (128, 256, 512, 1024):
    I, J = np.meshgrid(np.arange(N), np.arange(N)); L = lengths((I & J) == 0)
    print(N, [int((L >= f*N).sum()) for f in (.01,.03,.1,.25,.5,1,1.5,2)])
