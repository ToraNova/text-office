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
from string import Template
from .. import utils

def generate(inargs):
    parser = argparse.ArgumentParser(description="vapt boilerplate module")
    parser.add_argument('template', help='template (relative to boiler_templates dir. in project root)', type=str)
    parser.add_argument('name', help='name of finding', type=str)
    parser.add_argument('-c', '--cvss', help="cvss vector of finding", type=str)
    args = parser.parse_args(inargs)

    severity, score, score_print, vector, color = utils.vapt_helper.get_ssvc(args.cvss)

    finding_name = args.name
    clean_name = args.name.casefold().translate(dict.fromkeys(map(ord, u' \n#/\\()[]{}<>-.')))
    strscore = str(score).replace('.','')
    mdfile_name = f'{strscore}_{clean_name}.md'

    tplfn = utils.ensure_template_file(args.template, auto_add_suffix='.md')
    utils.log.info(f'creating boilerplate markdown with: {tplfn} {severity} {score} {vector} {color}')

    with open(tplfn, 'r') as tpl:
        tplstr = Template(tpl.read())

    res = tplstr.substitute(
        finding_name=finding_name,
        severity=severity,
        score_print=score_print,
        vector=vector,
        color=color
    )

    with open(mdfile_name, 'a+') as out:
        out.write(res)
