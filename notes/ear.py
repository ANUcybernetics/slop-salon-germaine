# usage: ear.py N OUT  -> OUT.wav (stereo: path of N left, N+1 right) and OUT.png
import sys, numpy as np, wave
from pairs_ear import path
N=int(sys.argv[1]); out=sys.argv[2]
SR=22050; STEP=0.12; P=0.2
paths=[path(N),path(N+1)]
L=max(len(p) for p in paths)+8
chans=[]
for p in paths:
    p=p+[1]*(L-len(p))
    f=np.array([110*x**P for x in p])
    t=np.arange(int(L*STEP*SR))/SR
    idx=np.minimum((t/STEP).astype(int),L-1)
    fr=f[idx]
    # glide: smooth over ~40 ms
    k=int(0.04*SR); fr=np.convolve(fr,np.ones(k)/k,mode='same')
    ph=2*np.pi*np.cumsum(fr)/SR
    x=np.sin(ph)+0.3*np.sin(2*ph)
    env=0.6+0.4*np.exp(-((t%STEP))/0.04)
    chans.append(x*env)
y=np.stack(chans,1); y/=np.abs(y).max()*1.1
w=wave.open(out+'.wav','wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
w.writeframes((y*32767).astype('<i2').tobytes()); w.close()
# picture: log2 n of both
import PIL.Image as I, PIL.ImageDraw as D
W,H=1280,720; im=I.new('RGB',(W,H),(14,14,18)); d=D.Draw(im)
top=max(max(np.log2(paths[0])),max(np.log2(paths[1])))
for p,c in zip(paths,[(240,170,70),(90,200,220)]):
    pts=[(40+i*(W-80)/(L-1), H-40-(np.log2(x))/top*(H-80)) for i,x in enumerate(p)]
    d.line(pts,fill=c,width=3)
im.save(out+'.png')
print(L, top)
