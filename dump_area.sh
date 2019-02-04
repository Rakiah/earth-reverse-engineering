#!/bin/sh

GEO_DATA="$(python find_overlaps.py $1 $3 $2 $4 | tr -d '\n' | tr -d '\r')"
node.exe objs_dump.js "$GEO_DATA" "$1,$2-$3,$4" "$5"
