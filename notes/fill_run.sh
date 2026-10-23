#!/bin/bash
# usage: notes/fill_run.sh SEED...  (8x8 hole, flux-fill-dev, then png)
for s in "$@"; do
  python notes/fill.py make hole $s
  replicate run black-forest-labs/flux-fill-dev --input image=@assets/fill_in_hole$s.png --input mask=@assets/fill_mask_hole$s.png --input prompt="a continuation of the same black line drawing on white: quarter-circle arcs in square tiles" --input guidance=30 >/dev/null 2>&1 \
   && mv assets/out-0.webp assets/fill_hole$s.webp && python -c "
from PIL import Image; Image.open('assets/fill_hole$s.webp').convert('RGB').save('assets/fill_hole$s.png')"
done
