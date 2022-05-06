import re
from docx.oxml.shared import OxmlElement
from docx.oxml.ns import qn, nsdecls
from docx.oxml import parse_xml, CT_P
from docx.opc.constants import RELATIONSHIP_TYPE
from docx.oxml.numbering import CT_Num, CT_Numbering
from docx.enum.section import WD_SECTION, WD_ORIENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.base import XmlMappedEnumMember
from docx.enum.dml import MSO_THEME_COLOR_INDEX
from docx.shared import Pt, Inches, Cm, Mm, RGBColor
from docx.styles.styles import Styles

def format_run(run, bold=None, italic=None, underline=None, strike=None, color=None, size=None, name=None):
    if bold is not None:
        run.font.bold = bold
    if italic is not None:
        run.font.italic = italic
    if underline is not None:
        run.font.underline = underline
    if strike is not None:
        run.font.strike = strike
    if color is not None:
        run.font.color.rgb = color
    if size is not None:
        run.font.size = size
    if name is not None:
        run.font.name = name
    return run

def format_paragraph(para, style=None, align=None, spacing=None, before=None, after=None):
    if style is not None:
        para.style = style
    if align is not None:
        para.paragraph_format.alignment = align
    if spacing is not None:
        para.paragraph_format.line_spacing = spacing
    if before is not None:
        para.paragraph_format.space_before = before
    if after is not None:
        para.paragraph_format.space_after = after
    return para

def format_table(table, style=None, align=None, autofit=None, colwidths=None):
    if style is not None:
        table.style = style
    if autofit is not None:
        table.autofit = autofit
    if align is not None:
        table.alignment = align
    if colwidths is not None:
        table.autofit = False
        for r in table.rows:
            for idx, cell in enumerate(r.cells):
                if idx < len(colwidths):
                    cell.width = colwidths[idx]

    return table

def insert_hrule(para, linestyle='single'):
    p = para._p  # p is the <w:p> XML element
    pPr = p.get_or_add_pPr()
    pBdr = OxmlElement('w:pBdr')
    pPr.insert_element_before(pBdr,
            'w:shd', 'w:tabs', 'w:suppressAutoHyphens', 'w:kinsoku', 'w:wordWrap',
            'w:overflowPunct', 'w:topLinePunct', 'w:autoSpaceDE', 'w:autoSpaceDN',
            'w:bidi', 'w:adjustRightInd', 'w:snapToGrid', 'w:spacing', 'w:ind',
            'w:contextualSpacing', 'w:mirrorIndents', 'w:suppressOverlap', 'w:jc',
            'w:textDirection', 'w:textAlignment', 'w:textboxTightWrap',
            'w:outlineLvl', 'w:divId', 'w:cnfStyle', 'w:rPr', 'w:sectPr',
            'w:pPrChange'
            )
    bottom = OxmlElement('w:bottom')
    if linestyle == 'dashsmall':
        bottom.set(qn('w:val'), 'dashSmallGap')
    else:
        bottom.set(qn('w:val'), 'single')
    bottom.set(qn('w:sz'), '6')
    bottom.set(qn('w:space'), '1')
    bottom.set(qn('w:color'), 'auto')
    pBdr.append(bottom)
    return pBdr

def parse_sizespec(sizespec):
    try:
        match = re.search('([0-9]+)([a-z]*)', sizespec)
        rsval = float(match.group(1))
        rstyp = match.group(2)

        if rstyp == 'mm':
            return Mm(rsval)
        elif rstyp == 'pt':
            return Pt(rsval)
        elif rstyp == 'in':
            return Inches(rsval)
        else:
            return Cm(rsval)
    except Exception as e:
        raise ValueError(f'unable to parse size spec: {sizespec}')

def insert_hyperlink(para, txt, url):
    # This gets access to the document.xml.rels file and gets a new relation id value
    part = para.part
    r_id = part.relate_to(url, RELATIONSHIP_TYPE.HYPERLINK, is_external=True)

    # Create the w:hyperlink tag and add needed values
    hyperlink = OxmlElement('w:hyperlink')
    hyperlink.set(qn('r:id'), r_id, )

    # Create a w:r element and a new w:rPr element
    new_run = OxmlElement('w:r')
    rPr = OxmlElement('w:rPr')

    # Join all the xml elements together add add the required text to the w:r element
    new_run.append(rPr)
    new_run.text = txt
    hyperlink.append(new_run)

    # Create a new Run object and add the hyperlink into it
    r = para.add_run()
    r._r.append(hyperlink)

    # A workaround for the lack of a hyperlink style (doesn't go purple after using the link)
    # Delete this if using a template that has the hyperlink style in it
    r.font.color.theme_color = MSO_THEME_COLOR_INDEX.HYPERLINK
    #r.font.color.rgb = RGBColor(0x06, 0x45, 0xad)
    r.font.underline = True
    return hyperlink

def assign_numbering(doc, para, anid, start=1, tierlvl=0):
    '''
    how to find abstract_numId (anid), open the .docx and find nav to word/document.xml
    search the relevant keyword in the list that we want to restart (i.e. ListBullet)
    open word/styles.xml and search for the style (ListBullet), look for numId value
    open word/numbering.xml and search the numId="x" value, get abstractNumId value
    '''
    ctn = doc.part.numbering_part.numbering_definitions._numbering
    nxtnid = ctn._next_numId
    num = CT_Num.new(nxtnid, anid)
    num.add_lvlOverride(ilvl=tierlvl).add_startOverride(start)
    ctn._insert_num(num)
    para._p.get_or_add_pPr().get_or_add_numPr().get_or_add_numId().val = nxtnid
    return nxtnid

def delete_paragraph(para):
    p = para._element
    p.getparent().remove(p)
    p._p = p._element = None

def shade_cell(cell, rgbhex='111111'):
    sh_elem = parse_xml(r'<w:shd {} w:fill="{}"/>'.format(nsdecls('w'), rgbhex))
    cell._tc.get_or_add_tcPr().append(sh_elem)

# NOT INCORPORATED INTO CORE YET-------------------------------------------------

def change_orientation(doc, orient='portrait'):
    current_section = doc.sections[-1]
    new_width, new_height = current_section.page_height, current_section.page_width
    new_section = doc.add_section(WD_SECTION.NEW_PAGE)
    if orient == 'landscape':
        new_section.orientation = WD_ORIENT.LANDSCAPE
    else:
        new_section.orientation = WD_ORIENT.PORTRAIT
    new_section.page_width = new_width
    new_section.page_height = new_height
    return new_section

def set_border(cell, **kwargs):
    """
    Set cell`s border
    Usage:

    set_cell_border(
        cell,
        top={"sz": 12, "val": "single", "color": "#FF0000", "space": "0"},
        bottom={"sz": 12, "color": "#00FF00", "val": "single"},
        left={"sz": 24, "val": "dashed", "shadow": "true"},
        right={"sz": 12, "val": "dashed"},
    )
    """
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()

    # check for tag existnace, if none found, then create one
    tcBorders = tcPr.first_child_found_in("w:tblBorders")
    if tcBorders is None:
        tcBorders = OxmlElement('w:tblBorders')
        tcPr.append(tcBorders)

    # list over all available tags
    for edge in ('top', 'bottom', 'left', 'right', 'insideH', 'insideV'):
        edge_data = kwargs.get(edge)
        if edge_data:
            tag = 'w:{}'.format(edge)

            # check for tag existnace, if none found, then create one
            element = tcBorders.find(qn(tag))
            if element is None:
                element = OxmlElement(tag)
                tcBorders.append(element)

            # looks like order of attributes is important
            for key in ["sz", "val", "color", "space", "shadow"]:
                if key in edge_data:
                    element.set(qn('w:{}'.format(key)), str(edge_data[key]))
