#!/usr/bin/env python

import argparse
from os import listdir
from natsort import natsorted
from os.path import isfile, isdir, join
from document_reporter.md import file_generate, docx_generate, basetpl_generate

parser = argparse.ArgumentParser()
# single
parser.add_argument('inputs', help='input files', type=str, nargs='*')
parser.add_argument('--ascending', help='sort in ascending order (if sorting)', action='store_true')
parser.add_argument('--nosort', help='do not sort input naturally', action='store_true')
parser.add_argument('-op', '--operation', help='type of operation to do: (generate), join/concat, mktpl', type=str, default='generate')
parser.add_argument('-o', '--output', help='output docx path', type=str, default='output.docx')
parser.add_argument('-t', '--template', help='template docx path', type=str)
args = parser.parse_args()

inlist = []
for inp in args.inputs:
    if isfile(inp):
        # is a file
        inlist.append(inp)
    else:
        for _file in listdir(inp):
            _filepath = join(inp, _file)
            if isfile(_filepath):
                inlist.append(_filepath)

#print(inlist)

if args.nosort:
    # don't sort
    pass
else:
    # sort
    inlist = natsorted(inlist, reverse=not args.ascending)

if args.operation in ['concat', 'join']:
    pass

elif args.operation in ['mktpl']:
    # create template docx
    docx = basetpl_generate()

else:
    if len(args.inputs) < 1:
        exit()

    # generate
    if args.template is None:
        docx = docx_generate(inlist)
    else:
        docx = docx_generate(inlist, docx_template=args.template)

if docx is not None:
    print('docx generated at', args.output)
    docx.save(args.output)
