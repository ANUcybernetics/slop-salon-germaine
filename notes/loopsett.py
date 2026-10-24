# loop as sett: smoothed unwrapped heading of the coin giant loop -> thread colour; mirrored tartan; weave arg plain|twill|satin
import numpy as np, sys
sys.path.insert(0,'notes')
import walk
from PIL import Image
seed=int(sys.argv[1]); weave=sys.argv[2]; out=sys.argv[3]
W=int(sys.argv[4]) if len(sys.argv)>4 else 10   # smoothing window
N=96
o=np.random.default_rng(seed).random((256,256))<.5
nd,L=walk.longest_start(o); t,_=walk.walk(o,nd)
h=np.cumsum(t).astype(float)
sm=np.convolve(h,np.ones(W)/W,'valid')
start=int(sys.argv[5]) if len(sys.argv)>5 else 0
seg=sm[start:start+N//2+1]
q=np.floor(seg/ (seg.max()-seg.min()+1e-9)*4.0 - seg.min()/(seg.max()-seg.min()+1e-9)*4.0).astype(int).clip(0,3)
warp=np.concatenate([q,q[-2:0:-1]])[:N]
pal=np.array([[24,38,64],[236,196,92],[190,60,48],[226,222,210]],float)
def up(i,j):
    if weave=='plain': return (i+j)%2==0
    if weave=='twill': return (i+j)%4<2
    return (j*2 - i)%5==0 if False else ((i-2*j)%5)!=0   # satin: warp up except 1 in 5
S=10; yy,xx=np.mgrid[0:S,0:S]
img=np.zeros((N*S,N*S,3))
for j in range(N):
    for i in range(N):
        u=up(i,j)
        c=pal[warp[i]] if u else pal[warp[j]]
        t_=(xx if u else yy)/(S-1)
        img[j*S:(j+1)*S,i*S:(i+1)*S]=c*(0.65+0.45*np.sin(np.pi*t_))[...,None]
Image.fromarray(np.clip(img,0,255).astype(np.uint8)).save(out)
runs=np.diff(np.flatnonzero(np.diff(np.concatenate([[-1],q,[-1]]))!=0))
print(L,len(t),'range',seg.min(),seg.max(),'q',np.bincount(q,minlength=4),'runs',sorted(runs)[::-1][:12],len(runs))
