import random
from PIL import Image, ImageDraw
N=48
def A(i,j): return int(((i&j)==0) ^ (((i+j)//7)%2==0))
cloth=[[A(i,j) for i in range(N)] for j in range(N)]  # [pick][warp]
def err_for_k(cols,k,iters=30,seed=0):
    # cols: list of warp-column tuples; cluster into k shafts, error = cells differing from cluster majority
    r=random.Random(seed); best=10**9
    for rs in range(12):
        cent=[list(c) for c in r.sample(cols,k)]
        for _ in range(iters):
            groups=[[] for _ in range(k)]
            for c in cols:
                g=min(range(k),key=lambda q:sum(a!=b for a,b in zip(c,cent[q])))
                groups[g].append(c)
            for q,gr in enumerate(groups):
                if gr: cent[q]=[int(sum(c[t] for c in gr)*2>len(gr)) for t in range(len(gr[0]))]
        e=sum(min(sum(a!=b for a,b in zip(c,cent[q])) for q in range(k)) for c in cols)
        best=min(best,e)
    return best
def curve(M,ks):
    cols=[tuple(M[j][i] for j in range(len(M))) for i in range(len(M[0]))]
    return [err_for_k(cols,k) for k in ks]
ks=[1,2,3,4,6,8,12,16,24,32,48]
cols=[tuple(cloth[j][i] for j in range(N)) for i in range(N)]
print("distinct columns",len(set(cols)),"distinct rows",len(set(tuple(r) for r in cloth)))
mine=curve(cloth,ks)
rnd=random.Random(5); coin=[[rnd.randint(0,1) for _ in range(N)] for _ in range(N)]
cc=curve(coin,ks)
print(ks);print(mine);print(cc)
# draw
W,H=620,400;img=Image.new("RGB",(W,H),(22,20,26));d=ImageDraw.Draw(img)
x0,y0,x1,y1=60,30,590,340;mx=max(cc)
def P(k,e): return (x0+(x1-x0)*ks.index(k)/(len(ks)-1), y1-(y1-y0)*e/mx)
for series,col in((cc,(110,100,110)),(mine,(224,128,84))):
    pts=[P(k,e) for k,e in zip(ks,series)]
    d.line(pts,fill=col,width=3)
    for p in pts: d.ellipse([p[0]-4,p[1]-4,p[0]+4,p[1]+4],fill=col)
for k in ks:
    x,_=P(k,0);d.line([(x,y1),(x,y1+5)],fill=(235,225,215));d.text((x-6,y1+9),str(k),fill=(235,225,215))
d.text((x0,y1+30),"shafts available",fill=(235,225,215));d.text((8,8),"cells wrong",fill=(235,225,215))
d.text((x0+260,y0+10),"coin flips",fill=(150,140,150));d.text((x0+260,y0+60),"my first cloth",fill=(224,128,84))
img.save("assets/curve.png")
