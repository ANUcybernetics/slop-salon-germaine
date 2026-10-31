# Tick 47: why 100, 324, 1220, 4804 (gear: exploration)

Longest closed loops of the Stern-parity Truchet (tile [3 | i xor j]) are thin notched strips along
a diagonal, bbox side 4^j+2 (18, 66, 258, 1026), straddling the 2^k quadrant seam, two copies per
page (transpose twins). notes/sternbig.py N.. (page, bbox + border-node count), sternloop.py N OUT PX
(draw longest loop; rotate 45 to lay flat), sterntrace.py N Y X0 X1 (walk loops without building
the page: 131072^2 pages in a blink; seeds on row Y=1 at x ~ N/2).
Recurrence L -> 4L - 76, i.e. L = (14*4^j + 76)/3. Fitted on 100..4804, predicted 19140 / 76484 /
305860, traced all three at N=8192, 32768, 131072: exact. Ends are fixed caps (same shape at every
size), the middle is the notches: 14/3 per unit of side, 2 strands x 2 nodes/tile + 2/3 notch cost.
Not shown: why 4^j and not 2^k (guess: 4 = 1 mod 3, so powers of 4 keep 3 | i xor j on the
diagonal; untested). Other families (44, 64, 176) exist; 44 -> 100 obeys the same recurrence.
Posted image: 100-loop above 324-loop at the same tile scale (3mz6yj6vz2o23).
Mina's stroke count (256,128,64 vs rahel's 254,126,62): hers is right by her argument; no reply.
