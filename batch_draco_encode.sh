#!/bin/sh

files=$(find $1 -type f -name *.obj)

declare -a arr=($files)

for i in "${arr[@]}"
do
   dirname=$(dirname $i)
   filename=$(basename $i | sed 's/.obj//g')
   draco_encoder -i $i -o "$dirname/$filename.drc" --metadata
done
