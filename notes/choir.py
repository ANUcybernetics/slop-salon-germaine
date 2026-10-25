# hailstone choir: voices n=1..N, one Collatz step per STEP seconds, pitch = F0*2^(log2 v / DIV)
# python notes/choir.py N STEP OUT   -> assets/OUT.wav + frames assets/choir_frames/
import sys, numpy as np, wave, os
from PIL import Image, ImageDraw
N=int(sys.argv[1]); STEP=float(sys.argv[2]); OUT=sys.argv[3]
SR=22050; F0=110.0; DIV=4.0; FPS=25
def stops(n):
    s=0
    while n!=1: n=n//2 if n%2==0 else 3*n+1; s+=1
    return s
T=max(stops(n) for n in range(1,N+1))+6   # steps, then a few turns of 4-2-1
L=np.zeros((N,T+1))
for n in range(1,N+1):
    v=n
    for t in range(T+1):
        L[n-1,t]=np.log2(v); v=v//2 if v%2==0 else 3*v+1
nS=int(T*STEP*SR); tt=np.arange(nS)/SR/STEP
i0=np.minimum(tt.astype(int),T-1); fr=tt-i0
mix=np.zeros(nS)
rng=np.random.default_rng(1)
for n in range(N):
    lg=L[n,i0]*(1-fr)+L[n,i0+1]*fr
    f=F0*2**(lg/DIV)
    ph=2*np.pi*np.cumsum(f)/SR+rng.uniform(0,2*np.pi)
    mix+=np.sin(ph)
mix/=np.abs(mix).max()
fade=np.minimum(1,np.minimum(np.arange(nS),nS-1-np.arange(nS))/(0.3*SR))
mix*=fade*0.8
w=wave.open(f"assets/{OUT}.wav","wb"); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
w.writeframes((mix*32767).astype(np.int16).tobytes()); w.close()
os.makedirs("assets/choir_frames",exist_ok=True)
W,H=1000,600; ymax=L.max()+0.5
nF=int(nS/SR*FPS)
for k in range(nF):
    t=k/FPS/STEP; a=min(int(t),T-1); f=t-a
    lg=L[:,a]*(1-f)+L[:,a+1]*f
    im=Image.new("RGB",(W,H),(14,12,20)); d=ImageDraw.Draw(im)
    xs=40+np.arange(N)/N*(W-80); ys=H-30-lg/ymax*(H-60)
    for x,y in zip(xs,ys): d.rectangle([x,y,x+1.2,y+1.2],fill=(240,200,120))
    im.save(f"assets/choir_frames/f{k:04d}.png")
print(T,nF,L.max())
