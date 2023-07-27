#!/bin/bash

. bin/activate

arr=(dual toc headfoot figures lists tables sections)

mkdir -p testout

for s in ${arr[@]}; do
    python ./text-office.py samples/$s.md -o testout/$s.docx
    [ ! -f "testout/$s.docx" ] && { echo "error creating file from samples/$s.md"; continue; }
    unzip -qq testrefs/$s.docx -d testout/$s-ref
    unzip -qq testout/$s.docx -d testout/$s
    diff -qr testout/$s-ref testout/$s
done;

# special cases with dxopt
s='auto_indent'
python ./text-office.py samples/$s.md -o testout/$s.docx -dxopt auto_left_indent=0.4in
if [ -f "testout/$s.docx" ]; then unzip -qq testrefs/$s.docx -d testout/$s-ref; unzip -qq testout/$s.docx -d testout/$s; diff -qr testout/$s-ref testout/$s; else echo "error creating file from samples/$s.md"; fi;

s='def_figtab_opts'
python ./text-office.py samples/$s.md -o testout/$s.docx -dxopt default_figure_width=3in -dxopt default_figure_border_width=1pt -dxopt 'default_table_style=Table Grid'
if [ -f "testout/$s.docx" ]; then unzip -qq testrefs/$s.docx -d testout/$s-ref; unzip -qq testout/$s.docx -d testout/$s; diff -qr testout/$s-ref testout/$s; else echo "error creating file from samples/$s.md"; fi;

rm -rf testout
