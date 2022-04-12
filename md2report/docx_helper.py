from docx.oxml.shared import OxmlElement
from docx.oxml.ns import qn, nsdecls
from docx.oxml import parse_xml, CT_P
from docx.opc.constants import RELATIONSHIP_TYPE
from docx.oxml.numbering import CT_Num, CT_Numbering
from docx.enum.section import WD_SECTION, WD_ORIENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.dml import MSO_THEME_COLOR_INDEX
from docx.shared import Pt, Inches, Cm, RGBColor
from docx import Document

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

def delete_paragraph(paragraph):
    p = paragraph._element
    p.getparent().remove(p)
    p._p = p._element = None

def format_run(run, bold=None, italic=None, underline=None, color=None, size=None, name=None):
    if bold is not None:
        run.bold = bold
    if italic is not None:
        run.italic = italic
    if underline is not None:
        run.underline = underline
    if color is not None:
        run.font.color.rgb = color
    if size is not None:
        run.font.size = size
    if name is not None:
        run.font.name = name
    return run

def add_text_run(para, text, bold=None, italic=None, underline=None, color=None, size=None, name=None):
    run = para.add_run()
    run.text = text
    return format_run(run, bold, italic, underline, color, size, name)

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


def restart_numbering(doc, para, abstract_numId):
    '''
    how to find abstract_numId, open the .docx and find nav to word/document.xml
    search the relevant keyword in the list that we want to restart (i.e. ListBullet)
    open word/styles.xml and search for the style (ListBullet), look for numId value
    open word/numbering.xml and search the numId="x" value, get abstractNumId value
    '''
    ctn = doc.part.numbering_part.numbering_definitions._numbering
    nxtnid = ctn._next_numId
    num = CT_Num.new(nxtnid, abstract_numId)
    num.add_lvlOverride(ilvl=0).add_startOverride(1)
    ctn._insert_num(num)
    para._p.get_or_add_pPr().get_or_add_numPr().get_or_add_numId().val = nxtnid
    return num


def add_hyperlink(paragraph, text, url):
    # This gets access to the document.xml.rels file and gets a new relation id value
    part = paragraph.part
    r_id = part.relate_to(url, RELATIONSHIP_TYPE.HYPERLINK, is_external=True)

    # Create the w:hyperlink tag and add needed values
    hyperlink = OxmlElement('w:hyperlink')
    hyperlink.set(qn('r:id'), r_id, )

    # Create a w:r element and a new w:rPr element
    new_run = OxmlElement('w:r')
    rPr = OxmlElement('w:rPr')

    # Join all the xml elements together add add the required text to the w:r element
    new_run.append(rPr)
    new_run.text = text
    hyperlink.append(new_run)

    # Create a new Run object and add the hyperlink into it
    r = paragraph.add_run()
    r._r.append(hyperlink)

    # A workaround for the lack of a hyperlink style (doesn't go purple after using the link)
    # Delete this if using a template that has the hyperlink style in it
    #r.font.color.theme_color = MSO_THEME_COLOR_INDEX.HYPERLINK
    r.font.color.rgb = RGBColor(0x06, 0x45, 0xad)
    r.font.underline = True

    return hyperlink


def shade_cell(cell, rgbhex='111111'):
    sh_elem = parse_xml(r'<w:shd {} w:fill="{}"/>'.format(nsdecls('w'), rgbhex))
    cell._tc.get_or_add_tcPr().append(sh_elem)


def insert_hrule(paragraph, linestyle='single'):
    p = paragraph._p  # p is the <w:p> XML element
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
    if linestyle == 'dashSmallGap':
        bottom.set(qn('w:val'), 'dashSmallGap')
    else:
        bottom.set(qn('w:val'), 'single')
    bottom.set(qn('w:sz'), '6')
    bottom.set(qn('w:space'), '1')
    bottom.set(qn('w:color'), 'auto')
    pBdr.append(bottom)


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
