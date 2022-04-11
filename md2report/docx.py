# https://mistletoe-ebp.readthedocs.io/en/latest/using/develop.html?highlight=renderer#a-new-renderer
# https://github.com/miyuchina/mistletoe/blob/master/mistletoe/html_renderer.py
from itertools import chain
from mistletoe import block_token, span_token
from mistletoe.base_renderer import BaseRenderer

from docx import Document

class Renderer(BaseRenderer):
    def __init__(self, out_path, docx_template=None, *extras):
        self._suppress_ptag_stack = [False]
        super().__init__(*chain((block_token.HTMLBlock, span_token.HTMLSpan), extras))
        self.out_path = out_path
        self.docx_template = docx_template

    def render_document(self, token):
        if self.docx_template is None:
            self.docx = Document()
        else:
            self.docx = Document(self.docx_template)
        self.render_inner(token)
        self.docx.save(self.out_path)

    def render_inner(self, token):
        # render child tokens
        for c in token.children:
            self.render(c)

    def render_heading(self, token):
        self.docx.add_heading(token.content)
        self.render_inner(token)
