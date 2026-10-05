#!/bin/sh
# Renders every product image with Cycles (several hours on 4 CPU cores).
cd "$(dirname "$0")"
for p in gear-board crag-ring rock-ring double-ring sport-board approach-bar pocket-bar; do
  python3 photoreal.py "$p" --views gear,dark --samples 32 || echo "FAILED $p gear"
  python3 photoreal.py "$p" --views hero,front,edge --samples 16 || echo "FAILED $p views"
  echo "DONE $p"
done
echo "ALL DONE"
