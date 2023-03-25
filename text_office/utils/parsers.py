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

import webcolors
import re
from shlex import shlex
from docx.shared import Pt, Inches, Cm, Mm, RGBColor, Length
from docx.enum.section import WD_SECTION, WD_ORIENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_TAB_ALIGNMENT
from docx.enum.table import WD_TABLE_ALIGNMENT
from .errx_helper import ensure_valid_value

def parse_color(color):
    if color is None:
        return None

    if color.startswith('#') and len(color) > 6:
        try:
            return RGBColor.from_string(color[1:])
        except Exception as e:
            pass

    try:
        return RGBColor.from_string(webcolors.name_to_hex(color)[1:])
    except Exception as e:
        pass

    try:
        return RGBColor.from_string(color)
    except Exception as e:
        pass

    raise ValueError(f'unable to parse color: {color}')


def parse_sizespec(sizespec):
    if sizespec is None:
        return None

    try:
        match = re.search('([0-9.]+)([a-z]*)', sizespec)
        rsval = float(match.group(1))
        rstyp = match.group(2)

        if rstyp == 'mm':
            return Mm(rsval)
        elif rstyp == 'pt':
            return Pt(rsval)
        elif rstyp == 'in':
            return Inches(rsval)
        elif rstyp == 'cm':
            return Cm(rsval)
        else:
            return rsval
    except Exception as e:
        raise ValueError(f'unable to parse size spec: {sizespec}')


def parse_sec_orientation(orientation):
    vmap = {
        'landscape': WD_ORIENT.LANDSCAPE,
        'portrait': WD_ORIENT.PORTRAIT,
        None: None,
    }
    ensure_valid_value('orientation', vmap, orientation)
    return vmap[orientation]


def parse_para_align(align):
    vmap = {
        'center': WD_ALIGN_PARAGRAPH.CENTER,
        'left': WD_ALIGN_PARAGRAPH.LEFT,
        'right': WD_ALIGN_PARAGRAPH.RIGHT,
        'justify': WD_ALIGN_PARAGRAPH.JUSTIFY,
        None: None
    }
    ensure_valid_value('align', vmap, align)
    return vmap[align]


def parse_table_align(align):
    vmap = {
            'center': WD_TABLE_ALIGNMENT.CENTER,
            'left': WD_TABLE_ALIGNMENT.LEFT,
            'right': WD_TABLE_ALIGNMENT.RIGHT,
            None: None
            }
    ensure_valid_value('align', vmap, align)
    return vmap[align]


def parse_kv_pairs(text, item_sep=", ", value_sep="="):
    """Parse key-value pairs from a shell-like text"""
    # initialize a lexer, in POSIX mode (to properly handle escaping)
    lexer = shlex(text, posix=True)
    # set ',' as whitespace for the lexer
    # (the lexer will use this character to separate words)
    lexer.whitespace = item_sep
    # include '=' as a word character
    # (this is done so that the lexer returns a list of key-value pairs)
    # (if your option key or value contains any unquoted special character, you will need to add it here)
    lexer.wordchars += value_sep
    lexer.wordchars += '!@#$%^&*()[];:.<>?/+-' # allow dot, slahes, round and square brackets
    # then we separate option keys and values to build the resulting dictionary
    # (maxsplit is required to make sure that '=' in value will not be a problem)

    try:
        od = dict(word.split(value_sep, maxsplit=1) for word in lexer)
        return od
    except Exception as e:
        raise ValueError(f'attribute error: {text}: {e}')


def parse_bool(val):
    if isinstance(val, str):
        val = val.casefold()
    if val in [1, True, '1', 'yes', 'true']:
        return True
    return False
