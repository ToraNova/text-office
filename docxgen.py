#!bin/python

import argparse
from document_reporter.md import file_generate, docx_generate, basetpl_generate

parser = argparse.ArgumentParser()
# single
parser.add_argument('input', help='name of input markdown', type=str)
parser.add_argument('-o', '--output', help='output docx path', type=str, default='output.docx')
parser.add_argument('-t', '--template', help='template docx path', type=str)
args = parser.parse_args()

if args.template is None:
    docx = docx_generate(args.input)
else:
    docx = docx_generate(args.input, docx_template=args.template)
docx.save(args.output)
