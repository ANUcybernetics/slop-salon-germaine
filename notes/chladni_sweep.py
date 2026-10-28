# usage: python notes/chladni_sweep.py M N OUTDIR  -> frames of persistent sand while theta sweeps 0..pi (A -> B -> -A)
import sys, os, numpy as np
from PIL import Image
M,N,OUT=int(sys.argv[1]),int(sys.argv[2]),sys.argv[3]
os.makedirs(OUT,exist_ok=True)
S=540; P=400000; BURN=500; F=150; SPF=40
rng=np.random.default_rng(5)
x=rng.random(P); y=rng.random(P)
def step(th):
    global x,y
    A=np.cos(M*np.pi*x)*np.cos(N*np.pi*y); B=np.cos(N*np.pi*x)*np.cos(M*np.pi*y)
    s=0.02*np.abs(np.cos(th)*A+np.sin(th)*B)
    x=x+rng.normal(size=P)*s; y=y+rng.normal(size=P)*s
    x=1-np.abs(1-np.abs(x)); y=1-np.abs(1-np.abs(y))
for i in range(BURN): step(0.0)
for f in range(F):
    th=np.pi*f/F
    for i in range(SPF): step(th+np.pi/F*i/SPF)
    h,_,_=np.histogram2d(y,x,bins=S,range=[[0,1],[0,1]])
    h=np.clip(h/np.percentile(h[h>0],97),0,1)
    Image.fromarray((255*(1-h**0.7)).astype(np.uint8)).save(f"{OUT}/f{f:04d}.png")
