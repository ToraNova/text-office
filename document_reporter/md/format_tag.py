# special formatting tokens to ease report writing to md

# https://github.com/miyuchina/mistletoe/blob/master/mistletoe/html_renderer.py

import re
from ..utils import parse_kv_pairs, show_error
from mistletoe.span_token import SpanToken, RawText
from mistletoe.block_token import BlockToken, tokenize

def _build_regex_ftag_uni_pattern(tag):
    return f'<{tag}\\s*(\\S.*?)?>'

def _build_regex_ftag_pattern(tag):
    return f'<{tag}\\s*(\\S.*?)?>(.*?)</{tag}>'

def _build_regex_ftag_noattr_pattern(tag):
    return f'<{tag}>(.*?)</{tag}>'

def _build_regex_ftag_start_pattern(tag):
    return f'<{tag}\\s*(\\S.*?)?[>\n]'
    #return f'<{tag}\\s*(\\S.*?)?>\n'

class KeyValueMixin:
    def parse_format(self):
        self.format = parse_kv_pairs(self.format_value_raw, item_sep=' \n\t')
        #fkv_list = self.format_value_raw.split(',')
        #self.format = {}
        #for kv_pair in fkv_list:
        #    _wl = kv_pair.strip().split('=')
        #    if len(_wl) < 2:
        #        continue
        #    self.format[_wl[0].strip().casefold()] = _wl[1].strip()

class FormatTag(SpanToken):
    parse_group = 2

    def __init__(self, match):
        self.format_value = None
        self.format_value_raw = match.group(1)
        if self.format_value_raw is not None:
            self.format_value = self.format_value_raw.casefold()
        # do not define children ourselves, allow for nested formats
        #self.children = (RawText(match.group(2) if match.group(2) is not None else match.group(4)),)

class NoAttrFormatTag(SpanToken):
    parse_group = 1

class KeyValueFormatTag(KeyValueMixin, FormatTag):
    def __init__(self, match):
        super().__init__(match)
        self.parse_format()

class BoldTag(NoAttrFormatTag):
    pattern = re.compile(_build_regex_ftag_noattr_pattern('b'), re.DOTALL)

class ItalicTag(NoAttrFormatTag):
    pattern = re.compile(_build_regex_ftag_noattr_pattern('i'), re.DOTALL)

class UnderlineTag(NoAttrFormatTag):
    pattern = re.compile(_build_regex_ftag_noattr_pattern('u'), re.DOTALL)

class StrongTag(NoAttrFormatTag):
    pattern = re.compile(_build_regex_ftag_noattr_pattern('strong'), re.DOTALL)

class EmphasisTag(NoAttrFormatTag):
    pattern = re.compile(_build_regex_ftag_noattr_pattern('emphasis'), re.DOTALL)

class StrikethroughTag(NoAttrFormatTag):
    pattern = re.compile(_build_regex_ftag_noattr_pattern('strike'), re.DOTALL)

class FontTag(KeyValueFormatTag):
    pattern = re.compile(_build_regex_ftag_pattern('font'), re.DOTALL)

class ImageTag(KeyValueFormatTag):
    pattern = re.compile(_build_regex_ftag_pattern('img'), re.DOTALL)

class CellTag(KeyValueFormatTag):
    pattern = re.compile(_build_regex_ftag_pattern('cell'), re.DOTALL)

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
        start_token = re.search(_build_regex_ftag_start_pattern(self.tag), lines[0], re.DOTALL)
        self.format_value_raw = start_token.group(1)
        if self.format_value_raw is not None:
            self.format_value = self.format_value_raw.casefold()
        lines[0] = lines[0][start_token.span()[1]:]
        if len(lines[-1].strip()) < 1:
            raise Exception(f'Invalid block tag "{self.tag}": can\'t find end tag, did you include a newline after the start tag?')
        end_token =re.search(f'</{self.tag}>', lines[-1])
        lines[-1] = lines[-1][:end_token.span()[0]]
        super().__init__(lines, tokenize)

    @classmethod
    def start(cls, line):
        stripped = line.lstrip()
        if len(line) - len(stripped) >= 4:
            return False

        # rule 1: <pre>, <script> or <style> tags, allow newlines in block
        match_obj = re.match(_build_regex_ftag_start_pattern(cls.tag), stripped, re.DOTALL)
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

class FormatKeyValueBlockTag(KeyValueMixin, FormatBlockTag):
    def __init__(self, lines):
        super().__init__(lines)
        self.parse_format()

# comment block
class CommentBlockTag(FormatBlockTag):
    tag = 'comment'

# stuff that require multiple lines with breaks in between (e.g., align multiple paragraphs, styling a multi-line table)
class AlignBlockTag(FormatBlockTag):
    tag = 'align'

class TableBlockTag(FormatKeyValueBlockTag):
    tag = 'table'

class ParagraphBlockTag(FormatKeyValueBlockTag):
    tag = 'para'
