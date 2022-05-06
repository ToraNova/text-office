# renders a docx from markdown
# using mistletoe for markdown parsing and python-docx for docx rendering

import os
import re
from urllib.parse import urlparse

from itertools import chain
from mistletoe import block_token, span_token
from mistletoe.base_renderer import BaseRenderer

from docx import Document
from docx.shared import Pt, Inches, Cm, Mm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.style import WD_STYLE_TYPE

from ..util.docx_helper import format_paragraph, format_run, format_table, insert_hrule, insert_hyperlink, parse_sizespec, assign_numbering
from .format_tag import HorizontalRuleTag, LineBreakTag, PageBreakTag, ColorTag, BoldTag, ItalicTag, UnderlineTag, StrikethroughTag, FontNameTag, FontSizeTag, ImageWidthTag, AlignBlockTag, TableStyleBlockTag, TableWidthBlockTag, ParagraphStyleBlockTag

class Renderer(BaseRenderer):
    def __init__(self, docx_template=None, rel_root=None, *extras):
        '''
        renders a .docx using docx_template as the template file
        rel_root determine the path to include relative path resources (e.g., images)
        '''
        self._suppress_ptag_stack = [False]
        super().__init__(*chain(([
            HorizontalRuleTag, LineBreakTag, PageBreakTag,
            ColorTag, BoldTag, ItalicTag, UnderlineTag, StrikethroughTag, FontNameTag, FontSizeTag, ImageWidthTag,
            AlignBlockTag, TableStyleBlockTag, TableWidthBlockTag, ParagraphStyleBlockTag,
        ]), extras))
        self.rel_root = os.getcwd() if rel_root is None else rel_root
        self.docx_template = docx_template

    def render_inner(self, token):
        # inner rendering not supported on DocxRenderer
        # raise NotImplementedError('unsupported render_inner function called')
        for c in token.children:
            self.render(c)

    def render_list(self, token):
        # https://github.com/miyuchina/mistletoe/blob/94022647cd9d80e242db5c93a6567e3155b468bc/mistletoe/block_token.py#L447
        ordered = token.start is not None
        level = self.list_level
        self.list_level += 1

        # TODO: fix this abstract_numId map with a more robust implementation
        anid_map = {
                0: 7, # numId 5, absnumId 7
                1: 3, # numId 6, absnumId 3
                2: 2, # numId 7, absnumId 2
        }

        if ordered:
            stpl = 'List Number '
        else:
            stpl = 'List Bullet '

        if level > 0:
            stpl += str(level+1)
        style = stpl.strip()

        for idx, c in enumerate(token.children):
            number = token.start + idx if ordered else None
            # if mistletoe changed the way leader/prepend is computed, this must changed as well

            tos = len(self.paras)
            for ic in c.children:
                ic.docx_style = style
                self.render(ic)
            #self.populate_and_format_paras(c, style=style)

            added = len(self.paras) - tos
            #if added > 0 and ordered:
            if added > 0 and ordered and idx == 0:
                assign_numbering(self.docx, self.paras[tos], anid_map[level], number)

        self.list_level -= 1

    def render_list_item(self, token):
        # handled by list
        #self.render_inner(token)
        raise NotImplementedError("list_item is handled by list rendering")

    def render_line_break(self, token):
        self.runs[-1].add_break()

    def render_link(self, token):
        # TODO: allow alt-txt in links, see mistletoe docs on parser issues (token.title is empty!)
        insert_hyperlink(self.paras[-1], token.target, token.target)

    def render_image(self, token):
        if token.src.startswith('/'):
            img_path = token.src
        else:
            img_path = os.path.join(self.rel_root, token.src)

        self.runs.append(self.paras[-1].add_run())
        self.inline_shapes.append(self.runs[-1].add_picture(img_path))

    def render_image_tag(self, token):
        up = urlparse(token.format_value_raw)

    def render_raw_text(self, token):
        # add run to last added paragraph
        self.runs.append(self.paras[-1].add_run())
        self.runs[-1].add_text(token.content)

    def render_document(self, token):
        # create document from template
        if self.docx_template is None:
            self.docx = Document()
        else:
            self.docx = Document(self.docx_template)

        # paragraph and run stack
        self.list_level = 0 # default root level
        self.runs = []
        self.paras = self.docx.paragraphs.copy()
        self.tables = self.docx.tables.copy()
        self.inline_shapes = []
        self.render_inner(token)

        # save document
        #self.docx.save(self.out_path)
        return self.docx

    def populate_and_format_runs(self, token, **kwargs):
        # format_tag allows nested formatting <b><i>test</i></b>, italic and bold
        tos = len(self.runs) # top of stack
        self.render_inner(token)
        added = len(self.runs) - tos # new top of stack
        # apply format to all added elements during inner render
        for i in range(added):
            format_run(self.runs[-(i+1)], **kwargs)

    def populate_and_format_paras(self, token, **kwargs):
        tos = len(self.paras)
        self.render_inner(token)
        added = len(self.paras) - tos
        # apply format to all added elements during inner render
        for i in range(added):
            format_paragraph(self.paras[-(i+1)], **kwargs)

    def populate_and_format_tables(self, token, **kwargs):
        tos = len(self.tables) # top of stack
        self.render_inner(token)
        added = len(self.tables) - tos # new top of stack
        # add style to all added table within this block
        for i in range(added):
            format_table(self.tables[-(i+1)], **kwargs)

    def populate_and_resize_image(self, token, width, height=None):
        tos = len(self.inline_shapes)
        self.render_inner(token)
        added = len(self.inline_shapes) - tos
        for i in range(added):
            target = self.inline_shapes[-(i+1)]
            if height is not None:
                target.height = height
            else:
                # maintain aspect ratio
                sf = float(width) / float(target.width)
                target.height = round(target.height * sf)

            target.width = width


    def render_color_tag(self, token):
        self.populate_and_format_runs(token, color=RGBColor.from_string(token.format_value))

    def render_bold_tag(self, token):
        self.populate_and_format_runs(token, bold=True)

    def render_strong(self, token):
        self.populate_and_format_runs(token, bold=True)

    def render_italic_tag(self, token):
        self.populate_and_format_runs(token, italic=True)

    def render_emphasis(self, token):
        self.populate_and_format_runs(token, italic=True)

    def render_underline_tag(self, token):
        self.populate_and_format_runs(token, underline=True)

    def render_strikethrough_tag(self, token):
        self.populate_and_format_runs(token, strike=True)

    def render_strikethrough(self, token):
        self.populate_and_format_runs(token, strike=True)

    def render_font_name_tag(self, token):
        self.populate_and_format_runs(token, name=token.format_value)

    def render_font_size_tag(self, token):
        size = parse_sizespec(token.format_value)
        self.populate_and_format_runs(token, size=size)

    def render_heading(self, token):
        # assume that heading has no additional child
        self.paras.append(self.docx.add_heading(level=token.level).clear())
        self.render_inner(token)

    def render_paragraph(self, token):
        # for all span tokens
        if hasattr(token, 'docx_style') and isinstance(token.docx_style, str):
            self.paras.append(self.docx.add_paragraph(style=token.docx_style).clear())
        else:
            self.paras.append(self.docx.add_paragraph().clear())
        self.render_inner(token)

    def render_align_block_tag(self, token):
        map = {
            'center': WD_ALIGN_PARAGRAPH.CENTER,
            'left': WD_ALIGN_PARAGRAPH.LEFT,
            'right': WD_ALIGN_PARAGRAPH.RIGHT,
            'justify': WD_ALIGN_PARAGRAPH.JUSTIFY,
        }
        if token.format_value not in map:
            raise KeyError(f'no such alignment type: {token.format_value} (center, left, right, justify)')
        self.populate_and_format_paras(token, align=map[token.format_value])

    def render_horizontal_rule_tag(self, token):
        insert_hrule(self.paras[-1], token.format_value)

    def render_thematic_break(self, token):
        insert_hrule(self.paras[-1])

    def render_page_break_tag(self, token):
        self.docx.add_page_break()

    def render_line_break_tag(self, token):
        #self.runs[-1].text += '\n'
        if len(self.runs) < 1:
            self.runs.append(self.paras[-1].add_run())
        self.runs[-1].add_break()

    def populate_table(self, token, **kwargs):
        if len(token.children) < 1:
            return
        ncol = len(token.children[0].children)
        self.tables.append(self.docx.add_table(0, ncol))

        if hasattr(token, 'header') and token.header is not None:
            token.header.is_header = True
            self.render(token.header)

        for row in token.children:
            row.is_header = False
            self.render(row)

    def populate_row(self, token, **kwargs):
        row = self.tables[-1].add_row()
        for cidx, col in enumerate(token.children):
            col.docx_cell = row.cells[cidx]
            self.render(col)

    def render_table(self, token):
        self.populate_table(token)

    def render_table_row(self, token):
        self.populate_row(token)

    def render_table_cell(self, token):
        self.paras.append(token.docx_cell.paragraphs[0])
        self.render_inner(token)

    def render_table_style_block_tag(self, token):
        self.populate_and_format_tables(token, style=token.format_value_raw)

    def render_paragraph_style_block_tag(self, token):
        self.populate_and_format_paras(token, style=token.format_value_raw)

    def render_image_width_tag(self, token):
        width = parse_sizespec(token.format_value)
        self.populate_and_resize_image(token, width=width)

    def render_table_width_block_tag(self, token):
        colw_raw = token.format_value.split(',')
        colw = []
        for cr in colw_raw:
            colw.append(parse_sizespec(cr.strip()))
        self.populate_and_format_tables(token, colwidths=colw)
