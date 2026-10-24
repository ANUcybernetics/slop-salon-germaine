# colour-and-weave: structure is fixed (twill or plain); colour per thread from a 1D stacked-scale rule.
import numpy as np, sys
from PIL import Image
seed=int(sys.argv[1]) if len(sys.argv)>1 else 3
struct=sys.argv[2] if len(sys.argv)>2 else 'twill'
p=float(sys.argv[3]) if len(sys.argv)>3 else .2
out=sys.argv[4] if len(sys.argv)>4 else 'assets/cw.png'
rng=np.random.default_rng(seed)
N=96
def stacked(n,p):
    a=np.zeros(n,int); l=0
    while 2**l<=n:
        b=2**l; k=(n+b-1)//b
        f=(rng.random(k)<p).astype(int)
        a^=np.repeat(f,b)[:n]; l+=1
    return a
pal=np.array([[24,38,64],[236,196,92],[190,60,48]],float)
# 3 colours: two bits -> pick colour index
def colours(n):
    a=stacked(n,p); b=stacked(n,p)
    return (a+2*(b&a)) % 3 if False else np.where(a==0,0,np.where(b==0,1,2))
warp=colours(N//2+1)
warp=np.concatenate([warp,warp[-2:0:-1]])[:N] if 'tartan' in out else colours(N)
weft=warp.copy() if 'tartan' in out else colours(N)
S=10  # px per crossing
img=np.zeros((N*S,N*S,3))
yy,xx=np.mgrid[0:S,0:S]
for j in range(N):      # weft rows
    for i in range(N):  # warp cols
        if struct=='plain': up=(i+j)%2==0
        else: up=(i+j)%4<2   # 2/2 twill
        c=pal[warp[i]] if up else pal[weft[j]]
        # thread shading: warp-over shades across x, weft-over across y
        t=(xx if up else yy)/(S-1)
        sh=0.65+0.45*np.sin(np.pi*t)
        if up: tile=c*sh[...,None]
        else: tile=c*sh.T[...,None] if False else c*(0.65+0.45*np.sin(np.pi*(yy/(S-1))))[...,None]
        img[j*S:(j+1)*S,i*S:(i+1)*S]=tile
img=np.clip(img,0,255).astype(np.uint8)
Image.fromarray(img).save(out)
