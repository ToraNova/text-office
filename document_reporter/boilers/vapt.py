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
from ..utils import boiler_template_path, boiler_template_path_pip, log
from ..utils.vapt_helper import get_ssvc

def generate(inargs):
    parser = argparse.ArgumentParser(description="vapt boilerplate module")
    parser.add_argument('template', help='template (relative to boiler_templates dir. in project root)', type=str)
    parser.add_argument('name', help='name of finding', type=str)
    parser.add_argument('-c', '--cvss', help="cvss vector of finding", type=str)
    args = parser.parse_args(inargs)

    severity, score, score_print, vector, color = get_ssvc(args.cvss)

    finding_name = args.name
    clean_name = args.name.casefold().translate(dict.fromkeys(map(ord, u' \n#/\\()[]{}<>-.')))
    strscore = str(score).replace('.','')
    mdfile_name = f'{strscore}_{clean_name}.md'

    tplfn = args.template
    if not tplfn.endswith('.md'):
        tplfn += '.md'

    btplfn = tplfn

    if not os.path.isfile(tplfn):
        log.warn(f"cannot find boiler template '{tplfn}' in current working directory, defaulting to built-ins")
        tplfn = os.path.join(boiler_template_path, btplfn)

    if not os.path.isfile(tplfn):
        tplfn = os.path.join(boiler_template_path_pip, btplfn)

    if not os.path.isfile(tplfn):
        raise FileExistsError(f"cannot find boiler template in built-in templates dir")

    log.info(f'creating boilerplate markdown with: {tplfn} {severity} {score} {vector} {color}')

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
