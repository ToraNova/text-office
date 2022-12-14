import argparse
import os
from string import Template
from ..utils import boiler_template_path, boiler_template_path_pip
from ..utils.vapt_helper import get_ssvc

def generate(inargs):
    parser = argparse.ArgumentParser(description="static boilerplate module")
    parser.add_argument('template', help='template (relative to boiler_templates dir. in project root)', type=str)
    args = parser.parse_args(inargs)

    tplfn = args.template
    if not tplfn.endswith('.md'):
        tplfn += '.md'

    btplfn = tplfn

    if not os.path.isfile(tplfn):
        print(f"cannot find boiler template '{tplfn}' in current working directory, defaulting to built-ins.")
        tplfn = os.path.join(boiler_template_path, btplfn)

    if not os.path.isfile(tplfn):
        tplfn = os.path.join(boiler_template_path_pip, btplfn)

    if not os.path.isfile(tplfn):
        raise FileExistsError(f"cannot find boiler template in built-in templates dir.")

    print('copying static boiler to directory.')
    buf = []
    with open(tplfn, 'r') as tpl:
        buf = tpl.read()

    with open('images.md', 'a+') as out:
        out.write(buf)
