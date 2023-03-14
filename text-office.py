#!/usr/bin/env python
'''
Copyright (C) 2023 ToraNova

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published
    by the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
'''

import argparse
import datetime
from os import listdir
from natsort import natsorted
from os.path import isfile, isdir, join
from docx import Document
from docx.document import Document as _DOCX
from text_office import (
        version,
        md,
        utils,
        )

JOIN_OP = ['join', 'concat']
LIST_OP = ['listonly', 'nogen']
LSTY_OP = ['show_default_styles']
MKTP_OP = ['mktpl']

parser = argparse.ArgumentParser()
# single
parser.add_argument('inputs', help='input files', type=str, nargs='*')
parser.add_argument('-f', '--manifest', help='processing manifest', type=str)
parser.add_argument('--ascending', help='sort in ascending order (if sorting)', action='store_true')
parser.add_argument('--nosort', help='do not sort input naturally', action='store_true')
parser.add_argument('-op', '--operation', help=f'type of operation to do: ({md.OPNAME}), {JOIN_OP}, {LIST_OP}, {MKTP_OP}, {LSTY_OP}', type=str, default='mdgen')
parser.add_argument('-o', '--output', help='output docx path', type=str, default='output.docx')
parser.add_argument('-t', '--template', help='template docx path', type=str)
parser.add_argument('-dxopt', '--docx_opts', help='key-value pair of docx options (e.g., caption_prefix_heading=1, prompt_updatefield=no)', type=str)
parser.add_argument('--rel_root', help='relative root (for images, attachments)', type=str)
parser.add_argument('--version', help='show version number', action='store_true')
args = parser.parse_args()

if args.version:
    # show version then exit
    print('text-office', version)
    exit(0)

docx = None

# TODO: allow diff modules (e.g., substitute)
_module = md

inlist = []

if args.manifest is not None:
    # using a manifest file
    if not isfile(args.manifest):
        utils.log.critical('cannot open manifest for processing')
        exit(1)

    with open(args.manifest, 'r') as mfile:
        for line in mfile:
            line = line.strip()
            if line.startswith('#'):
                # ignore comments
                continue

            if line.isspace() or len(line) < 1:
                # ignore whitelines
                continue

            if not isfile(line):
                # raise error
                utils.log.error(f'cannot open specified file in manifest "{args.manifest}" for processing: {line}')
                continue

            inlist.append(line)
else:
    # specifying directly from args
    for inp in args.inputs:
        if isfile(inp):
            # is a file
            inlist.append(inp)
        else:
            for _file in listdir(inp):
                _filepath = join(inp, _file)
                if isfile(_filepath) and _module.can_process(_filepath):
                    inlist.append(_filepath)

if args.nosort:
    # don't sort
    pass
else:
    # sort
    inlist = natsorted(inlist, reverse=not args.ascending)


if args.operation in LIST_OP:
    # list target files to process without processing
    utils.log.info("the following markdown will be processed in order:")
    for i in inlist:
        utils.log.info(i)

elif args.operation in JOIN_OP:
    # concatenate docx
    docx = utils.docx_helper.concat_docx(inlist)

elif args.operation in MKTP_OP:
    # create template docx
    docx = Document()

elif args.operation in LSTY_OP:

    _docx = Document()
    for s in _docx.styles:
        print(s)
    docx = None

else:
    if len(inlist) < 1:
        utils.log.critical('no inputs')
        exit(1)

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
    utils.log.info(f'docx generated at {args.output}')
    docx.save(args.output)
