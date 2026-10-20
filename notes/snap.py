from PIL import Image, ImageDraw
N=48;S=8;ROW=27
thr=[(i^(i>>1))%S for i in range(N)]
trd=[(((j+1)&-(j+1)).bit_length()-1)%S for j in range(N)]
rows=[".#.#.###","#.#.#.##","#...##.#","#...#...",".#####..","#.......",".##.....","#..#...."]
T=[[1 if c=="#" else 0 for c in r] for r in rows]
G=[[T[thr[i]][trd[j]] for i in range(N)] for j in range(N)]
def wruns(row,skip):
    cells=[(i,v) for i,v in enumerate(row) if i!=skip]
    best=0;run=0;prev=None;span=None;start=0
    for k,(i,v) in enumerate(cells):
        if v==prev: run+=1
        else: run=1;start=i
        prev=v
        if run>best: best=run;span=(start,i)
    return best,span
res=[]
for s in range(N):
    m=0;where=None
    for j in range(ROW,N):
        b,sp=wruns(G[j],s)
        if b>m: m,where=b,(j,sp)
    res.append((m,s,where))
base=max(wruns(G[j],None)[0] for j in range(N))
print("base",base)
for m,s,w in sorted(res,reverse=True)[:6]: print("thread",s,"float",m,w)
print("safest",sorted(res)[:3])
worst=sorted(res,reverse=True)[0]; snap=worst[1]
C=14;M=C*2
img=Image.new("RGB",(N*C+2*M,N*C+2*M+C*5),(22,20,26));d=ImageDraw.Draw(img)
for j in range(N):
    for i in range(N):
        x=M+i*C;y=M+j*C
        if i==snap and j>=ROW:
            d.rectangle([x+C//2-1,y,x+C//2,y+C],fill=(70,60,66));continue
        d.rectangle([x,y,x+C-2,y+C-2],fill=(224,128,84) if G[j][i] else (40,56,92))
# snapped row marker and merged floats in white outline
d.line([(M-8,M+ROW*C-1),(M+N*C+8,M+ROW*C-1)],fill=(235,225,215),width=1)
for j in range(ROW,N):
    b,sp=wruns(G[j],snap)
    if b>=5 and sp:
        d.rectangle([M+sp[0]*C-1,M+j*C-1,M+(sp[1]+1)*C-1,M+j*C+C-1],outline=(255,240,200))
res_sorted=sorted(res,key=lambda r:r[1])
# per-thread fragility strip under cloth
y0=M+N*C+C
for m,s,w in res_sorted:
    h=int(m*C*0.4)
    d.rectangle([M+s*C,y0+C*4-h,M+s*C+C-2,y0+C*4],fill=(235,225,215) if s==snap else (110,100,110))
img.save("snap.png");print(img.size,"snap thread",snap)
