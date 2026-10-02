"""fastkernel.py — a C kernel for the braid automorphism on a batch of PSL(2,p) tuples.

The braid moves preserve the coset {A,-A}, so the kernel works on raw 2x2 reps
mod p (no intermediate canonicalisation) and the caller checks output == +/-input
to detect a beta-hat-fixed tuple.
"""
import cffi

_ffi = cffi.FFI()
_ffi.cdef("""
void apply_auto_kernel(long long* X, int n, int* moves, int nmoves, int p);
""")
_src = r"""
void apply_auto_kernel(long long* X, int n, int* moves, int nmoves, int p) {
    for (int m = 0; m < nmoves; m++) {
        int i = moves[2*m];
        int eps = moves[2*m+1];
        for (int r = 0; r < n; r++) {
            long long* a = &X[((r*4 + i) * 4)];
            long long* b = &X[((r*4 + i + 1) * 4)];
            long long a0=a[0], a1=a[1], a2=a[2], a3=a[3];
            long long b0=b[0], b1=b[1], b2=b[2], b3=b[3];
            if (eps > 0) {
                /* na = a b a^-1 ; nb = a */
                long long ab0=(a0*b0+a1*b2)%p, ab1=(a0*b1+a1*b3)%p;
                long long ab2=(a2*b0+a3*b2)%p, ab3=(a2*b1+a3*b3)%p;
                long long ai0=a3, ai1=(-a1)%p, ai2=(-a2)%p, ai3=a0;
                long long na0=(ab0*ai0+ab1*ai2)%p, na1=(ab0*ai1+ab1*ai3)%p;
                long long na2=(ab2*ai0+ab3*ai2)%p, na3=(ab2*ai1+ab3*ai3)%p;
                a[0]=na0; a[1]=na1; a[2]=na2; a[3]=na3;
                b[0]=a0; b[1]=a1; b[2]=a2; b[3]=a3;
            } else {
                /* na = b ; nb = b^-1 a b */
                a[0]=b0; a[1]=b1; a[2]=b2; a[3]=b3;
                long long bi0=b3, bi1=(-b1)%p, bi2=(-b2)%p, bi3=b0;
                long long bia0=(bi0*a0+bi1*a2)%p, bia1=(bi0*a1+bi1*a3)%p;
                long long bia2=(bi2*a0+bi3*a2)%p, bia3=(bi2*a1+bi3*a3)%p;
                long long nb0=(bia0*b0+bia1*b2)%p, nb1=(bia0*b1+bia1*b3)%p;
                long long nb2=(bia2*b0+bia3*b2)%p, nb3=(bia2*b1+bia3*b3)%p;
                b[0]=nb0; b[1]=nb1; b[2]=nb2; b[3]=nb3;
            }
        }
    }
}
"""
_lib = _ffi.verify(_src)


def apply_auto_fast(X, moves, p):
    """X: (n,4,4) int64 array (canonical reps) -> in-place braid automorphism (coset reps)."""
    n = X.shape[0]
    moves_flat = []
    for (i, eps) in moves:
        moves_flat.extend([i, eps])
    mv = _ffi.new("int[]", moves_flat)
    ptr = _ffi.cast("long long*", X.ctypes.data)
    _lib.apply_auto_kernel(ptr, n, mv, len(moves), p)
    return X
