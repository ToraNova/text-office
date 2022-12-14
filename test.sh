#!/bin/sh

# testing on figure generation
#docxtool.py samples/figures.md -o ~/vmshare/figures.docx --docx_opts caption_prefix_heading=1

# testing on tables generation
#docxtool.py samples/tables.md -o ~/vmshare/tables.docx

# testing on basic1 (pretty much most test cases)
#docxtool.py samples/basic1.md -o ~/vmshare/basic1.docx

# append test
docxtool.py samples/tables.md samples/figures.md -o ~/vmshare/append.docx
