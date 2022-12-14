#!/usr/bin/env python

import argparse
from os import listdir
from natsort import natsorted
from os.path import isfile, isdir, join
from docx import Document
from docx.document import Document as _DOCX
from document_reporter import (
        md,
        utils,
        )

parser = argparse.ArgumentParser()
# single
parser.add_argument('inputs', help='input files', type=str, nargs='*')
parser.add_argument('--ascending', help='sort in ascending order (if sorting)', action='store_true')
parser.add_argument('--nosort', help='do not sort input naturally', action='store_true')
parser.add_argument('-op', '--operation', help='type of operation to do: (generate), join/concat, mktpl, substitute', type=str, default='generate')
parser.add_argument('-o', '--output', help='output docx path', type=str, default='output.docx')
parser.add_argument('-t', '--template', help='template docx path', type=str)
parser.add_argument('-D', '--docx_opts', help='key-value pair of docx options (e.g., caption_prefix_heading=1)', type=str)
parser.add_argument('--rel_root', help='relative root (for images, attachments)', type=str)
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

if args.nosort:
    # don't sort
    pass
else:
    # sort
    inlist = natsorted(inlist, reverse=not args.ascending)

docx = None
_module = md

if args.operation in ['stats', 'analysis']:
    fltlist = []
    for fn in inlist:
        if fn.endswith('.docx'):
            fltlist.append(fn)

    res = stats.analyse(fltlist)
    exit('work-in-progress.')

if args.operation in ['substitute', 'sub']:
    _module = sub


if args.operation in ['concat', 'join']:
    docx = utils.docx_helper.concat_docx(inlist)

elif args.operation in ['mktpl']:
    # create template docx
    docx = Document()

else:
    if len(args.inputs) < 1:
        exit('no inputs. use -h for help.')

    docx_opts = {}
    if args.docx_opts is not None:
        docx_opts = utils.parse_kv_pairs(args.docx_opts)

    # generate
    docx = _module.docx_generate(
            inlist,
            docx_template=args.template,
            rel_root=args.rel_root,
            docx_opts=docx_opts,
            )

if isinstance(docx, _DOCX):
    print('docx generated at', args.output)
    docx.save(args.output)
