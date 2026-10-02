"""Reduce the composite conjugator Gamma = gamma1 gamma3 gamma4 gamma2 for each word.
Fixed-point chain: x1 = g1 x3 g1^-1, x3 = g3 x4 g3^-1, x4 = g4 x2 g4^-1, x2 = g2 x1 g2^-1
=> x1 = Gamma x1 Gamma^-1 with Gamma = g1 g3 g4 g2.  So a fixed point needs m to commute
with Gamma(m).  Compare the reduced Gamma word for Conway vs KT."""
CONWAY = [-1, 2, -1, 2, -1, 3, -2, -2, -1, 3, 3]
KT = [-1, 2, 2, -3, -3, 2, 1, -2, -2, 3, -2, 3, -2]

def trace(word):
    # pos = (conjugator list of (base,sign), base)
    pos = [([], 1), ([], 2), ([], 3), ([], 4)]
    for g in word:
        i = abs(g) - 1
        (c1, b1) = pos[i]; (c2, b2) = pos[i + 1]
        if g > 0:
            pos[i] = (list(c1) + [(b1, 1)] + [(x, -s) for (x, s) in reversed(c1)] + list(c2), b2)
            pos[i + 1] = (list(c1), b1)
        else:
            pos[i] = (list(c2), b2)
            pos[i + 1] = (list(c2) + [(b2, -1)] + [(x, -s) for (x, s) in reversed(c2)] + list(c1), b1)
    return [pos[k][0] for k in range(4)]

def reduce(w):
    # free reduction: cancel adjacent (x,+s) (x,-s)
    st = []
    for atom in w:
        if st and st[-1][0] == atom[0] and st[-1][1] == -atom[1]:
            st.pop()
        else:
            st.append(atom)
    return st

def show(w):
    return " ".join(("x%d" % x if s > 0 else "x%d^-1" % x) for (x, s) in w)

for name, w in [("Conway", CONWAY), ("KT", KT)]:
    g = trace(w)
    G = list(g[0]) + list(g[2]) + list(g[3]) + list(g[1])  # gamma1 gamma3 gamma4 gamma2
    rG = reduce(G)
    print(f"=== {name} ===")
    for k in range(4):
        r = reduce(g[k])
        print(f"  gamma{k+1}: |{len(g[k])}| -> reduced |{len(r)}| : {show(r)}")
    print(f"  Gamma = g1 g3 g4 g2 : |{len(G)}| -> reduced |{len(rG)}| : {show(rG)}")
    print()
