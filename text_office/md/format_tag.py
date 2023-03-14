'''
Copyright (C) 2023 ToraNova

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published
    by the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
'''

# special formatting tokens to ease report writing to md

# https://github.com/miyuchina/mistletoe/blob/master/mistletoe/html_renderer.py

import re
from ..utils import parse_kv_pairs
from mistletoe.span_token import SpanToken, RawText
from mistletoe.block_token import BlockToken, tokenize

_attr_matcher = r'([^\<\>\n]+)'

def _build_regex_ftag_uni_pattern(tag):
    return f'<{tag}\\s*{_attr_matcher}?>'

def _build_regex_ftag_pattern(tag):
    return f'<{tag}\\s*{_attr_matcher}?>(.*?)</{tag}>'

def _build_regex_ftag_noattr_pattern(tag):
    return f'<{tag}>(.*?)</{tag}>'

def _build_regex_ftag_start_pattern(tag):
    return f'<{tag}\\s*{_attr_matcher}?[>\n]'
    #return f'<{tag}\\s*(\\S.*?)?>\n'

class KeyValueMixin:
    def parse_format(self):
        self.format = {}
        if self.format_value_raw == '>':
            # edge case 1, KeyValueFormatTag without attributes
            pass
        elif self.format_value_raw is None:
            # edge case 2, ditto
            pass
        else:
            self.format = parse_kv_pairs(self.format_value_raw, item_sep=' \n\t')


class NoAttrFormatTag(SpanToken):
    parse_group = 1


class FormatTag(SpanToken):
    parse_group = 2

    def __init__(self, match):
        self.format_value = None
        self.format_value_raw = match.group(1)
        if self.format_value_raw is not None:
            self.format_value = self.format_value_raw.casefold()
        # do not define children ourselves, allow for nested formats
        #self.children = (RawText(match.group(2) if match.group(2) is not None else match.group(4)),)


class NoBodyFormatTag(FormatTag):
    parse_group = 0
    parse_inner = False


class KeyValueFormatTag(KeyValueMixin, FormatTag):
    def __init__(self, match):
        super().__init__(match)
        self.parse_format()

class KeyValueNoBodyFormatTag(KeyValueMixin, NoBodyFormatTag):
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

class HorizontalRuleTag(NoBodyFormatTag):
    pattern = re.compile(_build_regex_ftag_uni_pattern('hr'))

class LineBreakTag(NoBodyFormatTag):
    pattern = re.compile(_build_regex_ftag_uni_pattern('br'))

class SectionBreakTag(NoBodyFormatTag):
    pattern = re.compile(_build_regex_ftag_uni_pattern('secbr'))

class InsertTabTag(NoBodyFormatTag):
    pattern = re.compile(_build_regex_ftag_uni_pattern('tab'))

class PageBreakTag(NoBodyFormatTag):
    pattern = re.compile(_build_regex_ftag_uni_pattern('pgbr'))

class TOCTag(NoBodyFormatTag):
    pattern = re.compile(_build_regex_ftag_uni_pattern('toc'))

class LOTTag(NoBodyFormatTag):
    pattern = re.compile(_build_regex_ftag_uni_pattern('lot'))

class LOFTag(NoBodyFormatTag):
    pattern = re.compile(_build_regex_ftag_uni_pattern('lof'))

class MergeTag(KeyValueNoBodyFormatTag):
    pattern = re.compile(_build_regex_ftag_uni_pattern('merge'))

class InsertPageNumTag(KeyValueNoBodyFormatTag):
    pattern = re.compile(_build_regex_ftag_uni_pattern('pgnum'))

class SectionControlTag(KeyValueNoBodyFormatTag):
    pattern = re.compile(_build_regex_ftag_uni_pattern('section'))

class NoNewLineException(Exception):

    def __init__(self, tagname):
        super().__init__(f'invalid block tag "{tagname}": can\'t find end tag, did you include a newline after the start tag/before the end tag (at least 2 lines required)?')

class FormatBlockTag(BlockToken):

    _end_cond = None

    def __init__(self, lines):
        start_token = re.search(_build_regex_ftag_start_pattern(self.tag), lines[0], re.DOTALL)
        self.format_value_raw = start_token.group(1)
        if self.format_value_raw is not None:
            self.format_value = self.format_value_raw.casefold()
        lines[0] = lines[0][start_token.span()[1]:]
        if len(lines[-1].strip()) < 1:
            raise NoNewLineException(self.tag)
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

class BorderBlockTag(FormatKeyValueBlockTag):
    tag = 'border'

class ParagraphBlockTag(FormatKeyValueBlockTag):
    tag = 'para'

class HeaderBlockTag(FormatKeyValueBlockTag):
    tag = 'header'

class FooterBlockTag(FormatKeyValueBlockTag):
    tag = 'footer'
