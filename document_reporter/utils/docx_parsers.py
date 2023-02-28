import webcolors
import re
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

