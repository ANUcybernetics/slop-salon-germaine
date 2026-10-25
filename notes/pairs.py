# n vs n+d stopping-time pairs: agreement by d, and (da, db) of odd/even step counts
import numpy as np, sys
N=1<<22
s=np.zeros(N+1,dtype=np.int32); a=np.zeros(N+1,dtype=np.int32)
for n in range(2,N+1):
    m=n;c=0;o=0
    while m>=n:
        if m&1: m=3*m+1;o+=1
        else: m//=2
        c+=1
        if m<n: break
    s[n]=c+s[m]; a[n]=o+a[m]
np.save('/tmp/steps.npy',s); np.save('/tmp/odds.npy',a)
