# usage: blurdiff.py IMG -- polar unwrap, blur by s px, mean abs diff under rolls (45 should beat 22.5 and 60 if C8)
import sys, numpy as np
from PIL import Image
from scipy.ndimage import map_coordinates, gaussian_filter
a=np.asarray(Image.open(sys.argv[1]).convert('L'),float); W=a.shape[0]; c=(W-1)/2
NA=1440; NR=480
th=np.linspace(0,2*np.pi,NA,endpoint=False); r=np.linspace(0,0.49*W,NR)
u=map_coordinates(a,[c+r[:,None]*np.sin(th)[None],c+r[:,None]*np.cos(th)[None]],order=1)
for s in (0,4,10,20):
    v=gaussian_filter(u,s,mode=('nearest','wrap')) if s else u
    row=[]
    for d in (360,180,120,90,60,45,30,22.5):
        row.append(f'{d}:{np.abs(v-np.roll(v,int(NA*d/360),axis=1)).mean():.1f}'.replace('.0:',':'))
    print('blur',s,' '.join(row))
