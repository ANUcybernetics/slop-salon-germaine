#!/usr/bin/env python3
"""sweep_big_a8.py — the three big A₈ meridian classes (the one concrete block).

Classes 4·2·1², 6·2, 7·1 were never swept: the m² grid is 6.3–11.3 M rows ×
300–570 x₂-orbits, ~11 s per orbit for m=2520 (measured), so ~2–6 h per (class,
word).  That is too long for one tick — but the sprite's filesystem persists
between ticks.  This script is RESUMABLE and meant to be launched DETACHED:

    nohup python3 sweep_big_a8.py > notes/a8_big_sweep.log 2>&1 &

State in notes/a8_big_state.json: which (class, word) pairs are done, and the
x₂-orbit index within the in-progress pair.  Re-running resumes.

Reports, per (class, word): β̂-fixed count, transitive count, max image order,
surject-A₈ (20160) and a witness.

Run: python3 sweep_big_a8.py            (resumes; safe to re-launch)
"""
import itertools, json, os, signal, sys, time
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
STATE = os.path.join(HERE, "notes", "a8_big_state.json")
N = 8
WANT = 20160
CONWAY = [-1, 2, -1, 2, -1, 3, -2, -2, -1, 3, 3]
KT = [-1, 2, 2, -3, -3, 2, 1, -2, -2, 3, -2, 3, -2]

CLASSES = {
    "4 2 1^2": (1, 2, 3, 0, 5, 4, 6, 7),
    "6 2":     (1, 2, 3, 4, 5, 0, 7, 6),
    "7 1":     (1, 2, 3, 4, 5, 6, 0, 7),
}


def pmul(p, q): return tuple(p[q[i]] for i in range(len(p)))
def pinv(p):
    r = [0] * len(p)
    for i in range(len(p)): r[p[i]] = i
    return tuple(r)
def psign(p):
    n = len(p); seen = [False] * n; s = 1
    for i in range(n):
        if not seen[i]:
            j = i; l = 0
            while not seen[j]:
                seen[j] = True; j = p[j]; l += 1
            s *= (-1)**(l - 1)
    return s
def cyc(p):
    n = len(p); seen = [False] * n; parts = []
    for i in range(n):
        if not seen[i]:
            c = []; j = i
            while not seen[j]:
                seen[j] = True; c.append(j); j = p[j]
            if len(c) > 1:
                parts.append("(" + " ".join(str(x) for x in c) + ")")
    return "".join(parts) if parts else "()"


def compose3(P, Q, R):
    return np.take_along_axis(np.take_along_axis(P, Q, axis=1), R, axis=1)


def apply_opt(X, moves):
    for (i, eps) in moves:
        aa = X[:, i]; bb = X[:, i + 1]
        if eps > 0:
            na = compose3(aa, bb, np.argsort(aa, axis=1))
            X[:, i + 1] = aa; X[:, i] = na
        else:
            nb = compose3(np.argsort(bb, axis=1), aa, bb)
            X[:, i] = bb; X[:, i + 1] = nb
    return X


def transitive(gen):
    n = len(gen[0]); adj = [set() for _ in range(n)]
    for g in gen:
        for i in range(n):
            adj[i].add(g[i]); adj[g[i]].add(i)
    seen = {0}; front = [0]
    while front:
        a = front.pop()
        for b in adj[a]:
            if b not in seen:
                seen.add(b); front.append(b)
    return len(seen) == n


def closure_order(gen, cap=30000):
    gen = list(set(gen)); n = len(gen[0])
    H = set(gen); H.add(tuple(range(n)))
    front = list(H)
    while front:
        a = front.pop()
        for b in gen:
            for c in (pmul(a, b), pmul(b, a), pinv(b)):
                if c not in H:
                    H.add(c); front.append(c)
                    if len(H) > cap:
                        return -1
    return len(H)


def class_of(a, G): return set(pmul(pmul(g, a), pinv(g)) for g in G)
def centralizer(a, G): return set(g for g in G if pmul(pmul(g, a), pinv(g)) == a)
def orbit_reps(a, cls, G):
    C = centralizer(a, G); seen = set(); reps = []
    for x in sorted(cls):
        if x in seen: continue
        reps.append(x)
        seen |= set(pmul(pmul(h, x), pinv(h)) for h in C)
    return reps


def log(msg):
    print(f"[{time.strftime('%H:%M:%S')}] {msg}", flush=True)


def load_state():
    if os.path.exists(STATE):
        with open(STATE) as f:
            return json.load(f)
    return {"done": {}, "progress": {}}


def save_state(st):
    tmp = STATE + ".tmp"
    with open(tmp, "w") as f:
        json.dump(st, f, indent=1)
    os.replace(tmp, STATE)


def run_pair(key, word, a, cls, moves, st):
    """Sweep one (class, word).  st['progress'][key] holds done orbit count."""
    reps = orbit_reps(a, cls, A8)
    mem = sorted(cls); m = len(mem)
    mem_arr = np.array(mem, dtype=np.int64)
    g3 = np.repeat(np.arange(m, dtype=np.int64), m)
    g4 = np.tile(np.arange(m, dtype=np.int64), m)

    prog = st["progress"].get(key, {})
    start = prog.get("orbit", 0)
    acc = {k: prog.get(k, d) for k, d in
           (("fixed", 0), ("trans", 0), ("maxord", 0), ("surj", False))}
    X = np.zeros((m * m, 4, N), dtype=np.int8)
    X[:, 2] = mem_arr[g3]; X[:, 3] = mem_arr[g4]
    X0 = np.zeros_like(X)
    X0[:, 2] = mem_arr[g3]; X0[:, 3] = mem_arr[g4]
    a_arr = np.array(a, dtype=np.int8)

    log(f"start {key}: m={m} orbits={len(reps)} from orbit {start}")
    for oi in range(start, len(reps)):
        x2 = reps[oi]
        X[:, 0] = a_arr; X[:, 1] = np.array(x2, dtype=np.int8)
        X0[:, 0] = X[:, 0]; X0[:, 1] = X[:, 1]
        apply_opt(X, moves)
        mask = np.all(X == X0, axis=(1, 2))
        idxs = np.nonzero(mask)[0]
        acc["fixed"] += len(idxs)
        for r in idxs:
            tup = (a, x2, mem[g3[r]], mem[g4[r]])
            if not transitive(tup):
                continue
            acc["trans"] += 1
            o = closure_order(list(tup))
            if o > acc["maxord"]:
                acc["maxord"] = o
            if o == WANT:
                acc["surj"] = True
                log(f"  *** {key} SURJECTS A₈: x1={cyc(a)} x2={cyc(x2)} "
                    f"x3={cyc(tup[2])} x4={cyc(tup[3])}")
        st["progress"][key] = {"orbit": oi + 1, **acc}
        if oi % 5 == 0 or oi == len(reps) - 1:
            save_state(st)
            log(f"  {key} orbit {oi+1}/{len(reps)}: fixed={acc['fixed']} "
                f"trans={acc['trans']} max={acc['maxord']} surj={acc['surj']}")
        if acc["surj"]:
            break
    st["progress"].pop(key, None)
    st["done"][key] = acc
    save_state(st)
    log(f"DONE {key}: fixed={acc['fixed']} trans={acc['trans']} "
        f"max={acc['maxord']} surj={acc['surj']}")


def main():
    global A8
    A8 = [p for p in itertools.permutations(range(N)) if psign(p) == 1]
    st = load_state()
    for cname, a in CLASSES.items():
        cls = class_of(a, A8)
        for wname, word in (("Conway", CONWAY), ("KT", KT)):
            key = f"{cname}|{wname}"
            if key in st["done"]:
                log(f"skip {key} (done: {st['done'][key]})")
                continue
            moves = [(abs(g) - 1, 1 if g > 0 else -1) for g in word]
            run_pair(key, word, a, cls, moves, st)
    log("ALL DONE")


if __name__ == "__main__":
    main()
