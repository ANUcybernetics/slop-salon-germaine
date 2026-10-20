# Truchet quarter-arc tiles; every edge midpoint has exactly one arc end, so curves close or leave the border.
# usage: python notes/truchet.py RULE N OUT
import sys, random, colorsys
from PIL import Image, ImageDraw
rule, N, out = sys.argv[1], int(sys.argv[2]), sys.argv[3]
def orient(x, y):
    if rule == 'rand': return random.Random(x*977+y*31+5).random() < .5
    if rule == 'and': return bin(x & y).count('1') & 1
    if rule == 'sq': return ((x*x + 3*y*y) >> 3) & 1
    if rule == 'xor': return ((x ^ y) >> 1) & 1
# nodes: ('h',x,y) = top edge midpoint of tile (x,y) ; ('v',x,y) = left edge midpoint
def N_(x,y): return ('h',x,y)
def S_(x,y): return ('h',x,y+1)
def W_(x,y): return ('v',x,y)
def E_(x,y): return ('v',x+1,y)
adj = {}
arcs = []
for y in range(N):
    for x in range(N):
        o = orient(x,y)
        pr = [(N_(x,y),W_(x,y)),(S_(x,y),E_(x,y))] if o else [(N_(x,y),E_(x,y)),(S_(x,y),W_(x,y))]
        for a,b in pr:
            adj.setdefault(a,[]).append(b); adj.setdefault(b,[]).append(a)
            arcs.append((x,y,o,a,b))
comp = {}; sizes = []
for n in adj:
    if n in comp: continue
    st=[n]; comp[n]=len(sizes); c=0
    while st:
        u=st.pop(); c+=1
        for v in adj[u]:
            if v not in comp: comp[v]=len(sizes); st.append(v)
    sizes.append(c)
S=24; W=N*S
img = Image.new('RGB',(W*2,W*2),(14,14,18)); d = ImageDraw.Draw(img)
mx = max(sizes)
def col(c):
    t = (c/mx)**.5
    if c==mx: return (255,236,170)
    r,g,b = colorsys.hsv_to_rgb(.62-.5*t, .55+.3*t, .35+.6*t)
    return (int(r*255),int(g*255),int(b*255))
k=2
for x,y,o,a,b in arcs:
    cx,cy = (x*S, y*S) if (a[0]=='h' and a[2]==y and b[0]=='v' and b[1]==x) else None, None
for x,y,o,a,b in arcs:
    # corner the arc is centred on
    if o: corners = {'N-W':(0,0),'S-E':(1,1)}
    else: corners = {'N-E':(1,0),'S-W':(0,1)}
    # determine corner from the two endpoints
    pts = {a,b}
    if N_(x,y) in pts and W_(x,y) in pts: c=(0,0)
    elif S_(x,y) in pts and E_(x,y) in pts: c=(1,1)
    elif N_(x,y) in pts and E_(x,y) in pts: c=(1,0)
    else: c=(0,1)
    cx,cy = (x+c[0])*S*k, (y+c[1])*S*k
    r = S*k/2
    start = {(0,0):0,(1,0):90,(1,1):180,(0,1):270}[c]
    d.arc([cx-r,cy-r,cx+r,cy+r], start, start+90, fill=col(sizes[comp[a]]), width=5)
img = img.resize((W*2,W*2))
img.save(out)
print(rule, 'curves', len(sizes), 'longest', mx, 'of', sum(sizes))
