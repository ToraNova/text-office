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
from cvss import CVSS2, CVSS3

import sys
import importlib

from text_office.utils import log

parser = argparse.ArgumentParser()
parser.add_argument('module', help='boilerplate generator module to use (e.g., vapt)', type=str)
args = parser.parse_args(sys.argv[1:2])

try:
    importstr = f'text_office.boilers.{args.module}'
    boiler = importlib.import_module(importstr)
    boiler.generate(sys.argv[2:])
except ImportError:
    log.exception(f'boilerplate module \'{args.module}\' not found.')
except Exception as e:
    log.exception('exception occured')
