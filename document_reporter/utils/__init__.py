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

import os
import sys
import traceback
from shlex import shlex
from .errx_helper import (
        ensure_valid_opts,
        ensure_valid_value,
        ensure_template_file,
        )

from .log_helper import log

from .path_helper import (
        boiler_template_path_pip,
        boiler_template_path,
        )

def parse_kv_pairs(text, item_sep=",", value_sep="="):
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
    lexer.wordchars += '.' # allow dot
    # then we separate option keys and values to build the resulting dictionary
    # (maxsplit is required to make sure that '=' in value will not be a problem)

    try:
        od = dict(word.split(value_sep, maxsplit=1) for word in lexer)
        return od
    except Exception as e:
        raise ValueError(f'attribute error: {text}')


def parse_bool(val):
    if isinstance(val, str):
        val = val.casefold()
    if val in [1, True, '1', 'yes', 'true']:
        return True
    return False
