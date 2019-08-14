#!/bin/sh

filename="$1,$3-$2,$4-L-$5.json"
if [ ! -f "$filename" ]; then
    echo "Cache not found -> redownloading cache..."
    python find_overlaps.py $1 $3 $2 $4 $5 > "$filename"
fi

node.exe objs_dump.js "$filename" "world-2" "$5"
