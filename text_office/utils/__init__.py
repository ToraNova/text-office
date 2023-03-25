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
from .errx_helper import (
        ensure_valid_value,
        ensure_template_file,
        )

from .log_helper import log

from .path_helper import (
        boiler_template_path_pip,
        boiler_template_path,
        )

from .parsers import (
        parse_bool,
        parse_kv_pairs,
        parse_sizespec as parse_docx_sizespec,
        )

def set_attr_recursively(token, instance_type, attr, value):
    if isinstance(token, instance_type):
        setattr(token, attr, value)

    if hasattr(token, 'children'):
        if isinstance(token.children, list):
            for c in token.children:
                set_attr_recursively(c, instance_type, attr, value)

default_encoding = 'utf-8'
