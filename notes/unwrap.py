# usage: unwrap.py IMG OUT -- polar unwrap (angle across, radius up) and its self-difference under 45 and 22.5 deg rolls
import sys, numpy as np
from PIL import Image, ImageDraw
from scipy.ndimage import map_coordinates
a = np.asarray(Image.open(sys.argv[1]).convert('RGB'), float); H,W,_=a.shape
c=(W-1)/2; NA=1440; NR=480
th=np.linspace(0,2*np.pi,NA,endpoint=False); r=np.linspace(0,0.49*W,NR)[::-1]
Y=c+r[:,None]*np.sin(th)[None]; X=c+r[:,None]*np.cos(th)[None]
u=np.stack([map_coordinates(a[...,k],[Y,X],order=1) for k in range(3)],-1)
def diff(s): return np.abs(u-np.roll(u,s,axis=1)).mean(-1)
for name,s in (('45',NA//8),('22.5',NA//16),('90',NA//4),('60',NA//6)):
    d=diff(s); print(name,'deg: mean abs diff',round(d.mean(),1))
def tile(d): return Image.fromarray(np.clip(255-d*2.5,0,255).astype(np.uint8)).convert('RGB')
top=Image.fromarray(u.astype(np.uint8))
panels=[top,tile(diff(NA//8)),tile(diff(NA//16))]
out=Image.new('RGB',(NA,NR*3+8),(20,20,40))
for i,p in enumerate(panels): out.paste(p,(0,i*(NR+4)))
dr=ImageDraw.Draw(out)
for k in range(9):
    x=k*NA//8
    dr.line([(x,0),(x,NR-1)],fill=(255,255,255),width=1)
out.save(sys.argv[2])
