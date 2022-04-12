# special formatting tokens to ease report writing to md

import re
import webcolors
from mistletoe.span_token import SpanToken, RawText

def _build_regex_string(tag):
    return f'<{tag}\\s*([#0-9a-zA-Z]+)?>(.*?)</{tag}>'

class FormatSpan(SpanToken):
    parse_group = 2

    def __init__(self, match):
        self.format_value = match.group(1)
        # do not define children ourselves, allow for nested formats
        #self.children = (RawText(match.group(2) if match.group(2) is not None else match.group(4)),)

class ColorSpan(FormatSpan):
    pattern = re.compile(_build_regex_string('c'), re.DOTALL)

    def __init__(self, match):
        super().__init__(match)
        if not self.format_value.startswith('#'):
            self.format_value = webcolors.name_to_hex(self.format_value)[1:]

class BoldSpan(FormatSpan):
    pattern = re.compile(_build_regex_string('b'), re.DOTALL)

class ItalicSpan(FormatSpan):
    pattern = re.compile(_build_regex_string('i'), re.DOTALL)
