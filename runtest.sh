#!/bin/bash

. bin/activate

arr=(dual toc headfoot figures lists tables)

mkdir -p testout

for s in ${arr[@]}; do
    python ./docxtool.py samples/$s.md -o testout/$s.docx
    [ ! -f "testout/$s.docx" ] && { echo "error creating file from samples/$s.md"; continue; }
    unzip -qq testrefs/$s.docx -d testout/$s-ref
    unzip -qq testout/$s.docx -d testout/$s
    diff -qr testout/$s-ref testout/$s
done;

rm -rf testout
