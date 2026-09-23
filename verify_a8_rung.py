"""verify_a8_rung.py — two point-stabilizers of A_8 generate A_8 (permutation
closure, no table).  This is the rung the seam climbs: seam reaches A_7 (rahel),
A_7 is a point-stabilizer of A_8, so seam#seam -> A_8."""
import itertools

def mul(p,q): return tuple(p[q[i]] for i in range(len(p)))
def inv(p):
    r=[0]*len(p)
    for i in range(len(p)): r[p[i]]=i
    return tuple(r)
def sign(p):
    n=len(p); seen=[False]*n; s=1
    for i in range(n):
        if not seen[i]:
            j=i; l=0
            while not seen[j]:
                seen[j]=True; j=p[j]; l+=1
            s*=(-1)**(l-1)
    return s

def closure(gen):
    gen=list(set(gen)); H=set(gen); H.add(tuple(range(len(gen[0]))))
    frontier=list(H)
    while frontier:
        a=frontier.pop()
        for b in gen:
            for c in (mul(a,b), mul(b,a), inv(b)):
                if c not in H:
                    H.add(c); frontier.append(c)
    return H

def stab(n,i):
    return [p for p in itertools.permutations(range(n)) if sign(p)==1 and p[i]==i]

for n in (6,7,8):
    S0=stab(n,0); S1=stab(n,1)
    J=closure(S0+S1)
    # verify J is all of A_n
    order = len([p for p in itertools.permutations(range(n)) if sign(p)==1])
    print(f"A_{n}: <stab(0),stab(1)> = |{len(J)}|   |A_{n}| = {order}   -> "
          f"{'GENERATES A_%d'%n if len(J)==order else 'NO'}")
