import traceback
from mistletoe import block_token

from .. import utils
from .documentx import Renderer as DocxRenderer
from docxcompose.composer import Composer

def file_generate(in_path, renderer, encoding='utf-8', **kwargs):
    """
    Converts markdown input to the output supported by the given renderer.
    If no renderer is supplied, ``HTMLRenderer`` is used.
    Note that extra token types supported by the given renderer
    are automatically (and temporarily) added to the parsing process.
    """
    with open(in_path, 'r', encoding=encoding) as infile:
        with renderer(tag=in_path, **kwargs) as renderer:
            docx = renderer.render(block_token.Document(infile))
            return docx

def docx_generate(mdarg, encoding='utf-8', **kwargs):
    if isinstance(mdarg, list) and len(mdarg) > 0:
        try:
            main_doc = file_generate(mdarg[0], DocxRenderer, encoding, **kwargs)
            main_comp = Composer(main_doc)

            for md in mdarg[1:]:
                try:
                    app_doc = file_generate(md, DocxRenderer, encoding, **kwargs)
                    main_comp.append(app_doc)
                except Exception as e:
                    utils.show_error(md, e)

            return main_comp.doc
        except Exception as e:
            utils.show_error(mdarg[0], e)

    else:
        return file_generate(mdarg, DocxRenderer, encoding, **kwargs)
