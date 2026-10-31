# trace Stern-parity Truchet curves without building the page. usage: sterntrace.py N Y X0 X1 [CAP]
# starts from top-edge nodes (x, Y) for x in X0..X1, reports closed loops (node counts) found.
import sys
N,Y,X0,X1=map(int,sys.argv[1:5]); CAP=int(sys.argv[5]) if len(sys.argv)>5 else 10**6
o=lambda x,y:((x^y)%3==0)
def partner(node,tile):
    k,x,y=node; tx,ty=tile
    N_,S_,W_,E_=('h',tx,ty),('h',tx,ty+1),('v',tx,ty),('v',tx+1,ty)
    pr={N_:W_,W_:N_,S_:E_,E_:S_} if o(tx,ty) else {N_:E_,E_:N_,S_:W_,W_:S_}
    return pr[node]
def other(node,tile):
    k,x,y=node; a,b=((x,y-1),(x,y)) if k=='h' else ((x-1,y),(x,y))
    return b if tile==a else a
def trace(start):
    # go into the tile below/right of start
    k,x,y=start; tile=(x,y); node=start; n=1
    while n<CAP:
        nxt=partner(node,tile); n+=1
        if nxt==start: return n-1 if False else n-1+0, True
        k2,x2,y2=nxt
        t2=other(nxt,tile)
        if not(0<=t2[0]<N and 0<=t2[1]<N): return n,False
        node,tile=nxt,t2
    return n,False
seen=set(); res={}
for x in range(X0,X1+1):
    s=('h',x,Y)
    if s in seen: continue
    L,closed=trace(s)
    if closed: res[L]=res.get(L,0)+1
print(sorted(res.items())[-6:])
