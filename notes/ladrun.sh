#!/bin/bash
# ladrun.sh WORD SEED : flux-dev "a WORD" into assets/lad2/WORD_SEED/, retry up to 4x
d=assets/lad2/$1_$2; mkdir -p $d
for t in 1 2 3 4; do
  replicate run black-forest-labs/flux-dev --input prompt="a $1" --input seed=$2 --input num_inference_steps=20 --output $d >$d.log 2>&1
  [ -f $d/out-0.webp ] && exit 0
done
