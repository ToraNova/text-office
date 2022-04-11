#!bin/python
from md2report import file_generate, DocxRenderer

file_generate('samples/header.md', 'test.docx', DocxRenderer)
