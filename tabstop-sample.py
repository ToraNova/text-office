import docx
doc = docx.Document()

p = doc.add_paragraph('Google\tEngineer')  # tab will trigger tabstop
sec = doc.sections[0]
# finding end_point for the content
margin_end = docx.shared.Inches(
    sec.page_width.inches - (sec.left_margin.inches + sec.right_margin.inches))
tab_stops = p.paragraph_format.tab_stops
# adding new tab stop, to the end point, and making sure that it's `RIGHT` aligned.
tab_stops.add_tab_stop(margin_end, docx.enum.text.WD_TAB_ALIGNMENT.RIGHT)

doc.save("/home/cjason/vmshare/test.docx")
