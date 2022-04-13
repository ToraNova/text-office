#!bin/python
from document_reporter.markdown import file_generate, docx_generate

#file_generate('samples/basic1.md', 'test.docx', DocxRenderer)
docx_generate('samples/basic1.md', '/home/cjason/share/test.docx')
