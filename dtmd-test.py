#!bin/python
from document_reporter.md import file_generate, docx_generate, basetpl_generate

#basetpl_generate('/home/cjason/vmshare/sample_template.docx')

#file_generate('samples/basic1.md', 'test.docx', DocxRenderer)
#docx = docx_generate('samples/basic1.md')
#docx.save('/home/cjason/vmshare/test.docx')

#docx = docx_generate(['samples/basic1.md', 'samples/append_test.md'])
#docx.save('/home/cjason/vmshare/test2.docx')

#docx = docx_generate(['samples/basic1.md'], docx_template='samples/sample_template.docx')
#docx.save('/home/cjason/vmshare/test3.docx')

#docx = docx_generate('samples/figures.md')
#docx.save('/home/cjason/vmshare/figures.docx')

#docx = docx_generate(['/media/dtpt/644026ae-40ab-4bc2-ae0d-e28acae3f1a9/home/cjason/work/nparks/2022-may/mobile/findings/rootok.md', '/media/dtpt/644026ae-40ab-4bc2-ae0d-e28acae3f1a9/home/cjason/softdev/document-reporter/samples/basic1.md'])
docx = docx_generate(['/media/dtpt/644026ae-40ab-4bc2-ae0d-e28acae3f1a9/home/cjason/work/nparks/2022-may/mobile/findings/rootok.md'])
docx.save('/home/dtpt/shares/vmshare/rootok.docx')
