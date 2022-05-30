# special formatting tokens to ease report writing to md

# https://github.com/miyuchina/mistletoe/blob/master/mistletoe/html_renderer.py

import re
import webcolors
from mistletoe.span_token import SpanToken, RawText
from mistletoe.block_token import BlockToken, tokenize

def _build_regex_ftag_uni_pattern(tag):
    return f'<{tag}\\s*((?:[\\-\\=?_.,/:#0-9a-zA-Z]+ ?)+)?>'

def _build_regex_ftag_pattern(tag):
    return f'<{tag}\\s*((?:[\\-\\=?_.,/:#0-9a-zA-Z]+ ?)+)?>(.*?)</{tag}>'

def _build_regex_ftag_start_pattern(tag):
    return f'<{tag}\\s*((?:[\\-\\=?_.,/:#0-9a-zA-Z]+ ?)+)?[ >\n]'

class FormatTag(SpanToken):
    parse_group = 2

    def __init__(self, match):
        self.format_value = None
        self.format_value_raw = match.group(1)
        if self.format_value_raw is not None:
            self.format_value = self.format_value_raw.casefold()
        # do not define children ourselves, allow for nested formats
        #self.children = (RawText(match.group(2) if match.group(2) is not None else match.group(4)),)

class ColorTag(FormatTag):
    pattern = re.compile(_build_regex_ftag_pattern('c'), re.DOTALL)

    def __init__(self, match):
        super().__init__(match)
        if not self.format_value.startswith('#'):
            self.format_value = webcolors.name_to_hex(self.format_value)[1:]

class BoldTag(FormatTag):
    pattern = re.compile(_build_regex_ftag_pattern('b'), re.DOTALL)

class ItalicTag(FormatTag):
    pattern = re.compile(_build_regex_ftag_pattern('i'), re.DOTALL)

class UnderlineTag(FormatTag):
    pattern = re.compile(_build_regex_ftag_pattern('u'), re.DOTALL)

class StrikethroughTag(FormatTag):
    pattern = re.compile(_build_regex_ftag_pattern('strike'), re.DOTALL)

class FontNameTag(FormatTag):
    pattern = re.compile(_build_regex_ftag_pattern('name@font'), re.DOTALL)

class FontSizeTag(FormatTag):
    pattern = re.compile(_build_regex_ftag_pattern('size@font'), re.DOTALL)

class ImageWidthTag(FormatTag):
    pattern = re.compile(_build_regex_ftag_pattern('width@img'), re.DOTALL)

class TableCellColorTag(FormatTag):
    pattern = re.compile(_build_regex_ftag_pattern('color@cell'), re.DOTALL)

class HorizontalRuleTag(FormatTag):
    parse_group = 0
    parse_inner = False
    pattern = re.compile(_build_regex_ftag_uni_pattern('hr'))

class LineBreakTag(FormatTag):
    parse_group = 0
    parse_inner = False
    pattern = re.compile(_build_regex_ftag_uni_pattern('br'))

class PageBreakTag(FormatTag):
    parse_group = 0
    parse_inner = False
    pattern = re.compile(_build_regex_ftag_uni_pattern('pgbr'))

class FormatBlockTag(BlockToken):

    _end_cond = None

    def __init__(self, lines):
        start_token = re.search(_build_regex_ftag_start_pattern(self.tag), lines[0])
        self.format_value_raw = start_token.group(1)
        if self.format_value_raw is not None:
            self.format_value = self.format_value_raw.casefold()
        lines[0] = lines[0][start_token.span()[1]:]
        end_token =re.search(f'</{self.tag}>', lines[-1])
        lines[-1] = lines[-1][:end_token.span()[0]]
        super().__init__(lines, tokenize)

    @classmethod
    def start(cls, line):
        stripped = line.lstrip()
        if len(line) - len(stripped) >= 4:
            return False

        # rule 1: <pre>, <script> or <style> tags, allow newlines in block
        match_obj = re.match(_build_regex_ftag_start_pattern(cls.tag), stripped)
        cls._end_cond = f'</{cls.tag}>'
        if match_obj is not None:
            return 1
        return False

    @classmethod
    def read(cls, lines):
        # note: stop condition can trigger on the starting line
        line_buffer = []
        for line in lines:
            line_buffer.append(line)
            if cls._end_cond is not None:
                if cls._end_cond in line.casefold():
                    break
            elif line.strip() == '':
                line_buffer.pop()
                break
        return line_buffer

class FormatKeyValueBlockTag(FormatBlockTag):
    def __init__(self, lines):
        super().__init__(lines)
        fkv_list = self.format_value_raw.split(',')
        self.format = {}
        for kv_pair in fkv_list:
            _wl = kv_pair.strip().split('=')
            if len(_wl) < 2:
                continue
            self.format[_wl[0].strip().casefold()] = _wl[1].strip()

# comment block
class CommentBlockTag(FormatBlockTag):
    tag = 'comment'

# stuff that require multiple lines with breaks in between (e.g., align multiple paragraphs, styling a multi-line table)
class AlignBlockTag(FormatBlockTag):
    tag = 'align'

class TableStyleBlockTag(FormatBlockTag):
    tag = 'style@table'

class ParagraphStyleBlockTag(FormatBlockTag):
    tag = 'style@para'

class TableWidthBlockTag(FormatBlockTag):
    tag = 'width@table'

class ParagraphFormatBlockTag(FormatKeyValueBlockTag):
    tag = 'format@para'
