#!/bin/sh

#python find_overlaps.py $1 $3 $2 $4 $5 > cache.json
node.exe objs_dump.js "cache.json" "$1,$2-$3,$4" "$5"
