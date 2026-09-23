#!/usr/bin/env python3
"""build_An.py — build A_n (even permutations of n, order n!/2) as tables in the
same (size, mul, inv, conj, order) format as build_GL32 / build_A5."""
import itertools
import numpy as np

def perm_mul(p, q):
    return tuple(p[q[i]] for i in range(len(p)))

def perm_inv(p):
    r = [0]*len(p)
    for i in range(len(p)):
        r[p[i]] = i
    return tuple(r)

def perm_order(p):
    n = len(p); seen=[False]*n; o=1
    for i in range(n):
        if not seen[i]:
            j=i; l=0
            while not seen[j]:
                seen[j]=True; j=p[j]; l+=1
            o = o*l//__import__("math").gcd(o,l)
    return o

def perm_sign(p):
    n=len(p); seen=[False]*n; s=1
    for i in range(n):
        if not seen[i]:
            j=i; l=0
            while not seen[j]:
                seen[j]=True; j=p[j]; l+=1
            s *= (-1)**(l-1)
    return s

def build_An(n):
    elems=[p for p in itertools.permutations(range(n)) if perm_sign(p)==1]
    idx={e:i for i,e in enumerate(elems)}
    size=len(elems)
    ident=idx[tuple(range(n))]
    mul=np.zeros((size,size),dtype=np.int64)
    for a in range(size):
        for b in range(size):
            mul[a,b]=idx[perm_mul(elems[a],elems[b])]
    inv=np.zeros(size,dtype=np.int64)
    for a in range(size):
        for b in range(size):
            if mul[a,b]==ident:
                inv[a]=b
    conj=np.zeros((size,size),dtype=np.int64)
    for a in range(size):
        for b in range(size):
            conj[a,b]=mul[mul[a,b],inv[a]]
    order=np.zeros(size,dtype=np.int64)
    for a in range(size):
        order[a]=perm_order(elems[a])
    return size,mul,inv,conj,order

if __name__=="__main__":
    import sys
    n=int(sys.argv[1]) if len(sys.argv)>1 else 6
    size,mul,inv,conj,order=build_An(n)
    print(f"|A_{n}| = {size}")
