#!bin/python
from document_reporter.md import file_generate, docx_generate, basetpl_generate

#basetpl_generate('/home/cjason/vmshare/sample_template.docx')

#file_generate('samples/basic1.md', 'test.docx', DocxRenderer)
docx = docx_generate('samples/basic1.md')
docx.save('/home/cjason/vmshare/test.docx')

#docx = docx_generate(['samples/basic1.md', 'samples/append_test.md'])
#docx.save('/home/cjason/vmshare/test2.docx')

#docx = docx_generate(['samples/basic1.md'], docx_template='samples/sample_template.docx')
#docx.save('/home/cjason/vmshare/test3.docx')

#docx = docx_generate('samples/figures.md')
#docx.save('/home/cjason/vmshare/figures.docx')

docx = docx_generate('samples/tables.md')
docx.save('/home/cjason/vmshare/tables.docx')
