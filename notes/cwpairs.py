import numpy as np, sys
from PIL import Image
# Calkin-Wilf pairs (f(n),f(n+1)): every coprime pair once. colour = bit length of n (depth)
K=int(sys.argv[1]); R=int(sys.argv[2]); out=sys.argv[3]
M=1<<K
f=np.zeros(M+2,dtype=np.int64); f[1]=1
for n in range(2,M+2):
    f[n]=f[n//2] if n%2==0 else f[n//2]+f[n//2+1]
n=np.arange(1,M); a=f[n]; b=f[n+1]
depth=np.floor(np.log2(n)).astype(int)
img=np.zeros((R,R,3),dtype=np.float64)
m=(a<R)&(b<R)
cm=np.array([[255,200,60],[240,90,40],[170,40,120],[60,60,170],[40,160,190],[90,200,120],[230,230,230]],float)
c=cm[depth[m]%7]
np.add.at(img,(b[m],a[m]),c)
img=np.clip(img,0,255).astype(np.uint8)
Image.fromarray(img[::-1]).save(out)
print(m.sum(), "points in window; coprime pairs in window ~", int(R*R*6/np.pi**2))
