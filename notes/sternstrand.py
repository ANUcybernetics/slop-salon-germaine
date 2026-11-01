# print o-tile map of bbox of the longest closed loop. usage: sternstrand.py N Y X0 X1 LEN
import sys
N,Y,X0,X1,LEN=map(int,sys.argv[1:6])
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
    k,x,y=start; tile=(x,y); node=start; tiles=[tile]
    while len(tiles)<10**6:
        nxt=partner(node,tile)
        if nxt==start: return tiles,True
        t2=other(nxt,tile)
        if not(0<=t2[0]<N and 0<=t2[1]<N): return tiles,False
        node,tile=nxt,t2; tiles.append(tile)
    return tiles,False
for x in range(X0,X1+1):
    t,c=trace(('h',x,Y))
    if c and len(t)+1==LEN or c and len(t)==LEN:
        xs=[a for a,b in t]; ys=[b for a,b in t]
        x0,x1,y0,y1=min(xs),max(xs),min(ys),max(ys)
        S=set(t)
        print(x,len(t),(x0,y0),(x1,y1))
        for y in range(y0,y1+1):
            print(''.join(('#' if o(a,y) else '+') if (a,y) in S else ('o' if o(a,y) else '.') for a in range(x0,x1+1)))
        break
