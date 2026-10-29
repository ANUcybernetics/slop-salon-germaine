import sys
def path(n):
    p=[n]
    while n!=1:
        n = n//2 if n%2==0 else 3*n+1
        p.append(n)
    return p
if __name__=="__main__":
    best=[]
    for n in range(2,30000):
        a,b=path(n),path(n+1)
        sa=set(a)
        # first index in b that lies on a (merge)
        m=next(i for i,x in enumerate(b) if x in sa)
        score=min(len(a),m)  # b's steps before it joins a
        best.append((score,n,len(a),len(b)))
    best.sort(reverse=True)
    print(best[:12])
