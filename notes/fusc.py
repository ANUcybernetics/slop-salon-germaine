import numpy as np, sys
from PIL import Image
# fusc(n): f(0)=0,f(1)=1,f(2n)=f(n),f(2n+1)=f(n)+f(n+1)
M=int(sys.argv[1]); W=int(sys.argv[2]); mod=int(sys.argv[3]); out=sys.argv[4]
f=np.zeros(M+2,dtype=np.int64); f[1]=1
for n in range(2,M+2):
    f[n]=f[n//2] if n%2==0 else f[n//2]+f[n//2+1]
a=f[:M-M%W].reshape(-1,W)
img=(a%mod)
pal=np.array([[20,20,30],[230,120,40],[240,230,200],[60,120,160],[160,40,80],[90,160,90],[200,200,60]]+[[i*9%255,i*37%255,i*17%255] for i in range(40)],dtype=np.uint8)
im=Image.fromarray(pal[img]).resize((W*2,a.shape[0]*2),Image.NEAREST)
im.save(out)
print(a.shape, f[:M].max())
