from mistletoe.block_token import Document

from .docx import Renderer as DocxRenderer

def file_generate(in_path, out_path, renderer=DocxRenderer, encoding='utf-8', **kwargs):
    """
    Converts markdown input to the output supported by the given renderer.
    If no renderer is supplied, ``HTMLRenderer`` is used.
    Note that extra token types supported by the given renderer
    are automatically (and temporarily) added to the parsing process.
    """
    with open(in_path, 'r', encoding=encoding) as infile:
        with renderer(out_path, **kwargs) as renderer:
            return renderer.render(Document(infile))
