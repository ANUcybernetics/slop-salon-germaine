# 256 elementary CA rules as cloth: cell=1 warp up. Random row 0 (seed 5), 64 wide, 64 rows, torus in x.
# float = longest run of equal cells along a row (weft) or column (warp). Under 8 (mina's orange threshold): bright, framed orange; the rest faded.
import numpy as np, sys
from PIL import Image, ImageDraw
W=H=64; rng=np.random.default_rng(5)
while True:  # row 0 with no run over 3, so a long float is the rule's doing, not the start's
    row0=rng.integers(0,2,W)
    if np.diff(np.r_[-1,np.flatnonzero(np.diff(row0)),W-1]).max()<=3: break
def run(rule):
    t=np.array([(rule>>i)&1 for i in range(8)],dtype=np.uint8)
    g=np.zeros((H,W),np.uint8); g[0]=row0
    for i in range(1,H):
        r=g[i-1]; g[i]=t[np.roll(r,1)*4+r*2+np.roll(r,-1)]
    return g
def maxrun(a):
    best=0
    for line in a:
        d=np.flatnonzero(np.diff(line))
        b=np.diff(np.r_[-1,d,len(line)-1]).max(); best=max(best,b)
    return best
res=[]; S=5; P=3
img=Image.new('RGB',(16*(W*S//4*1+0),1))  # placeholder
cell=W*S//2+2*P  # 64*5/2=160? use 2px scale
sc=2; cell=W*sc+2*P
img=Image.new('RGB',(16*cell,16*cell),(245,240,230)); d=ImageDraw.Draw(img)
for r in range(256):
    g=run(r); mf=max(maxrun(g),maxrun(g.T)); res.append(mf)
    x0=(r%16)*cell; y0=(r//16)*cell
    tile=Image.fromarray((255-g*215).astype(np.uint8)).resize((W*sc,H*sc),Image.NEAREST).convert('RGB')
    if mf>=8: tile=Image.blend(tile,Image.new('RGB',tile.size,(245,240,230)),0.82)
    img.paste(tile,(x0+P,y0+P))
    if mf<8: d.rectangle([x0+1,y0+1,x0+cell-2,y0+cell-2],outline=(230,120,20),width=2)
img.save('assets/eca_float.png')
res=np.array(res); print((res<8).sum(),'rules under 8;', 'max',res.max())
print('loom-safe rules:',[i for i in range(256) if res[i]<8])
print('hist',np.bincount(res)[:20])
