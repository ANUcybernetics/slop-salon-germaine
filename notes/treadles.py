# joint shafts x treadles cost: best k x k tie-up, alternating row/column assignment. usage: python notes/treadles.py
import random
from PIL import Image, ImageDraw
N=48
def A(i,j): return int(((i&j)==0) ^ (((i+j)//7)%2==0))
cloth=[[A(i,j) for i in range(N)] for j in range(N)]  # [pick j][warp i]
def ff(vs,k,r):
    # farthest-first prototypes, then nearest assignment
    P=[r.randrange(N)]
    while len(P)<k:
        P.append(max(range(N),key=lambda v:(min(sum(a!=b for a,b in zip(vs[v],vs[p])) for p in P),r.random())))
    return [min(range(k),key=lambda q:sum(a!=b for a,b in zip(vs[v],vs[P[q]]))) for v in range(N)]
def fit(M,k,restarts=12,seed=0):
    r=random.Random(seed);best=10**9
    for _ in range(restarts):
        sh=ff([[M[j][i] for j in range(N)] for i in range(N)],k,r); tr=ff(M,k,r)
        prev=None
        for _ in range(40):
            # tie-up majority given assignments
            cnt=[[[0,0] for _ in range(k)] for _ in range(k)]
            for j in range(N):
                for i in range(N): cnt[tr[j]][sh[i]][M[j][i]]+=1
            T=[[int(cnt[a][b][1]>cnt[a][b][0]) for b in range(k)] for a in range(k)]
            # reassign warps then picks
            for i in range(N):
                sh[i]=min(range(k),key=lambda b:sum(T[tr[j]][b]!=M[j][i] for j in range(N)))
            for j in range(N):
                tr[j]=min(range(k),key=lambda a:sum(T[a][sh[i]]!=M[j][i] for i in range(N)))
            e=sum(T[tr[j]][sh[i]]!=M[j][i] for j in range(N) for i in range(N))
            if e==prev: break
            prev=e
        best=min(best,e)
    return best
ks=[1,2,4,8,12,16,24,32,48]
rnd=random.Random(5);coin=[[rnd.randint(0,1) for _ in range(N)] for _ in range(N)]
mine=[fit(cloth,k) for k in ks];cc=[fit(coin,k) for k in ks]
print(ks);print("mine",mine);print("coin",cc)
print("pct wrong mine",[round(100*e/N/N,1) for e in mine]);print("pct wrong coin",[round(100*e/N/N,1) for e in cc])
