#!/usr/bin/env python

import argparse
from cvss import CVSS2, CVSS3

import sys
import importlib

parser = argparse.ArgumentParser()
parser.add_argument('module', help='boilerplate generator module to use (e.g., vapt)', type=str)
args = parser.parse_args(sys.argv[1:2])

try:
    importstr = f'document_reporter.boilers.{args.module}'
    boiler = importlib.import_module(importstr)
    boiler.generate(sys.argv[2:])
except ImportError:
    print(f'boilerplate module \'{args.module}\' not found.')
except Exception as e:
    print('exception occured:', e)
