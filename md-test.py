#!bin/python
from document_reporter.md import file_generate, docx_generate

#file_generate('samples/basic1.md', 'test.docx', DocxRenderer)
docx_generate('samples/basic1.md', '/home/cjason/vmshare/test.docx')
