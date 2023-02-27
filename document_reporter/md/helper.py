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

from ..utils import check_valid_value
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_TAB_ALIGNMENT
from docx.shared import Pt, Inches, Cm, Mm

def set_attr_recursively(token, instance_type, attr, value):
    if isinstance(token, instance_type):
        setattr(token, attr, value)

    if hasattr(token, 'children'):
        if isinstance(token.children, list):
            for c in token.children:
                set_attr_recursively(c, instance_type, attr, value)

def ensure_tabstop(token, cs):
    lmar = Inches(cs.left_margin.inches)
    cmar = Inches(cs.page_width.inches/2 - cs.left_margin.inches)
    rmar = Inches(cs.page_width.inches - (cs.left_margin.inches + cs.right_margin.inches))
    vmap = {
        'left': (lmar, WD_TAB_ALIGNMENT.LEFT),
        'center': (cmar, WD_TAB_ALIGNMENT.CENTER),
        'right': (rmar, WD_TAB_ALIGNMENT.RIGHT),
    }
    if 'tabstops' in token.format:
        out = []
        for t in token.format['tabstops'].split(','):
            check_valid_value('tabstops', vmap, t)
            out.append(vmap[t])
        return out
    return None


def ensure_align(token):
    if 'align' in token.format:
        vmap = {
            'center': WD_ALIGN_PARAGRAPH.CENTER,
            'left': WD_ALIGN_PARAGRAPH.LEFT,
            'right': WD_ALIGN_PARAGRAPH.RIGHT,
            'justify': WD_ALIGN_PARAGRAPH.JUSTIFY,
        }
        check_valid_value('align', vmap, token.format['align'])
        return vmap[token.format['align']]
    return None
