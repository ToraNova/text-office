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
import os
import sys
from string import Template
from .. import utils

def generate(inargs):
    parser = argparse.ArgumentParser(description="static boilerplate module")
    parser.add_argument('template', help='template (relative to boiler_templates dir. in project root)', type=str)
    parser.add_argument('-d', '--data', help='key-value pair of substitutions options (e.g., foo=bar, count=3)', type=str)
    parser.add_argument('-o', '--output', help='output md filename', type=str, default='output.md')
    parser.add_argument('-stdout', '--stdout', help='output to stdout', action="store_true")
    parser.add_argument('--overwrite', help='overwrite output instead of append', action='store_true')
    args = parser.parse_args(inargs)

    kvd = {}
    if args.data is not None:
        kvd = utils.parse_kv_pairs(args.data)

    tplfn = utils.ensure_template_file(args.template, auto_add_suffix='.md')

    buf = []
    with open(tplfn, 'r') as tpl:
        buf = tpl.read()

    t = Template(buf)
    buf = t.substitute(**kvd)

    if args.stdout:
        sys.stdout.write(buf)
    else:
        utils.log.info(f'creating boilerplate markdown from "{tplfn}" with values: {kvd}')
        mode = 'w' if args.overwrite else 'a+'
        with open(args.output, mode) as out:
            out.write(buf)
