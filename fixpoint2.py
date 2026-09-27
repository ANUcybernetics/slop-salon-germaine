#!/usr/bin/env python3
"""fixpoint2.py — iterate y -> gamma3(y)^-1 x3 gamma3(y) on the CORRECT equation.

beta_hat(x3) = gamma3 x4 gamma3^-1 = x3  =>  x4 = gamma3^-1 x3 gamma3.
gamma3 is the conjugator for beta_hat(x3), a word in x1,x2,x3,x4.
Track gamma3 as a word, evaluate it at (x1,x2,x3,y), and iterate.
Does it converge to the witness x4?
"""
import itertools
CONWAY = [-1, 2, -1, 2, -1, 3, -2, -2, -1, 3, 3]
KT = [-1, 2, 2, -3, -3, 2, 1, -2, -2, 3, -2, 3, -2]

def pmul(p,q): return tuple(p[q[i]] for i in range(len(p)))
def pinv(p):
    r=[0]*len(p)
    for i in range(len(p)): r[p[i]]=i
    return tuple(r)
def psign(p):
    n=len(p); seen=[False]*n; s=1
    for i in range(n):
        if not seen[i]:
            j=i; l=0
            while not seen[j]: seen[j]=True; j=p[j]; l+=1
            s*=(-1)**(l-1)
    return s
def cyc(p):
    n=len(p); seen=[False]*n; parts=[]
    for i in range(n):
        if not seen[i]:
            c=[]; j=i
            while not seen[j]: seen[j]=True; c.append(j); j=p[j]
            if len(c)>1: parts.append("("+" ".join(str(x) for x in c)+")")
    return "".join(parts) if parts else "()"
def from_cycles(cycles, n=9):
    p=list(range(n))
    for c in cycles:
        for k in range(len(c)): p[c[k]]=c[(k+1)%len(c)]
    return tuple(p)

# ---- track conjugator words for each position --------------------------------
def track_word(word):
    pos=[([],1),([],2),([],3),([],4)]
    for g in word:
        i=abs(g)-1
        (c1,b1)=pos[i]; (c2,b2)=pos[i+1]
        if g>0:
            pos[i]=(list(c1)+[(b1,1)]+[(x,-s) for (x,s) in reversed(c1)]+list(c2), b2)
            pos[i+1]=(list(c1), b1)
        else:
            pos[i]=(list(c2), b2)
            pos[i+1]=(list(c2)+[(b2,-1)]+[(x,-s) for (x,s) in reversed(c2)]+list(c1), b1)
    return pos

def eval_word(word_atoms, vals):
    """word_atoms = [(base,sign)], vals = {base: permutation}.  Evaluate."""
    r=tuple(range(9))
    for (b,s) in word_atoms:
        v=vals[b]
        if s<0: v=pinv(v)
        r=pmul(r,v)
    return r

def beta_hat(tup, word):
    X=list(tup)
    for g in word:
        i=abs(g)-1
        a,b=X[i],X[i+1]
        if g>0:
            X[i]=pmul(pmul(a,b),pinv(a)); X[i+1]=a
        else:
            X[i]=b; X[i+1]=pmul(pinv(b),pmul(a,b))
    return tuple(X)

def main():
    w=(from_cycles([(0,1,2),(3,4,5),(6,7,8)]),
       from_cycles([(0,1,3),(2,6,5),(4,8,7)]),
       from_cycles([(0,4,1),(2,5,6),(3,8,7)]),
       from_cycles([(0,2,6),(1,7,8),(3,4,5)]))
    x1,x2,x3,x4=w
    for wname,word in [("KT",KT),("CONWAY",CONWAY)]:
        pos=track_word(word)
        # gamma3 = pos[2] conjugator, base = pos[2][1] (=4 => x4)
        g3word,b3=pos[2]
        print(f"=== {wname}: beta_hat(x3) = gamma x{b3} gamma^-1, |gamma|={len(g3word)} ===")
        # iterate y -> gamma3(y)^-1 x3 gamma3(y)
        for seedname,seed in [("x2",x2),("x3",x3),("x4",x4),("x1",x1)]:
            y=seed
            path=[]
            for it in range(6):
                vals={1:x1,2:x2,3:x3,4:y}
                g=eval_word(g3word, vals)       # gamma3(y)
                gy=pmul(pinv(g), pmul(x3, g))    # gamma3^-1 x3 gamma3
                path.append((cyc(y), cyc(gy)))
                if gy==y:
                    break
                y=gy
            print(f"  seed {seedname}: " + " -> ".join(f"{a}=>{b}" for (a,b) in path))
        print("  target x4 =", cyc(x4))
        print("  beta_hat fixed at witness?", beta_hat(w, word)==w)

if __name__=="__main__":
    main()
