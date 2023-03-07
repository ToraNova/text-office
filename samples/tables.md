# Table Tests

## Normal Table

| hdr 1 | hdr 2 |
| --- | --- |
| row 1 col 1 | row 1 col 2 |
| row 2 col 1 | <cell color=ffc000> row 2 col 2</cell> |

## Aligned Table with adjusted column widths

Notice that the table itself does not align centrally, only the text does.

<align center>
<table style='Table Grid' column_widths='1.11in, 4in, 1.11in'>

| <cell color=000000></cell> | <cell color=000000></cell> | <cell color=000000></cell> |
| --- | --- |
| row 1 col 1 | row 1 col 2 | row 1 col 3 |
| row 2 col 1 | row 2 col 2 | row 1 col 3 |
</table>
</align>

## Aligned Table with adjust column widths and captions

<align right>
<table style='Table Grid' column_widths='1.11in, 1.11in, 4in' caption='caption test'>

| | | |
| --- | --- |
| row 1 col 1 | row 1 col 2 | row 1 col 3 |
| <cell color=ff0000><font color=0000ff>row 2 col 1</font></cell> | row 2 col 2 | row 1 col 3 |
</table>
</align>

<comment>
if two tables are together with the same style, word automatically joins them, unless a break in introduced in between</comment>
<br>

<table style='Table Grid' column_widths='1.11in, 1.11in, 4in' caption='center caption' caption_align=center>
<para before=6pt spacing=1.15 after=6pt>

| | | |
| --- | --- |
| row 1 col 1 | row 1 col 2 | row 1 col 3 |
| <cell color=ff0000><font color=0000ff>row 2 col 1</font></cell> | row 2 col 2 | row 1 col 3 |
</para>
</table>

## Center Aligned Table, with texts aligned to the right

Notice the table is centrally aligned, but the text remains left aligned. There is a difference between aligning the text in the table and the table itself.

<table style='Table Grid' column_widths='5cm, 8cm, 1cm' align=center>

| Col1 | Col2 | Col3 |
| ---- | ---- | --- |
| abcd | efgh | abc
| 1234 |  | |
| qwer | <font color=blue>xxxxxxxxxxxxx</font> | |
| qwer | <font name=Arial><b>xxxxxxxxxxxxx</b></font> | |
| img | <img width=5cm>![](samples/test_card.png)</img><br>test in newline | |
</table>

## Aligned Table with adjusted paragraphs

Basic table

| <cell color=a9a9a9>foo</cell> | <cell color=b9b9b9>bar</cell> |
| --- | --- |
| <cell color=c9c9c9>fu</cell>  | <cell color=d9d9d9>baz</cell> |

Spacing adjusted

<para before=0pt after=0pt spacing=1>

| <cell color=a9a9a9>foo</cell> | <cell color=b9b9b9>bar</cell> |
| --- | --- |
| <cell color=c9c9c9>fu</cell>  | <cell color=d9d9d9>baz</cell> |
</para>

## Table with border shading

<border top_width=3 bottom_width=1 bottom_color=00ff00 bottom_line=double left_space=5 left_line=dashed right_shadow=true>

| <cell color=a9a9a9>foo</cell> | <cell color=b9b9b9>bar</cell> |
| --- | --- |
| <cell color=c9c9c9>fu</cell>  | <cell color=d9d9d9>baz</cell> |
| <cell color=c7c7c7>f8</cell>  | <cell color=d7d7d7>b2z</cell> |
</border>

Specifying border attributes in cell tags overrides the table border settings

<border top_width=3 bottom_width=1 bottom_color=00ff00 bottom_line=double left_space=5 left_line=dashed right_shadow=true>

| <cell color=a9a9a9>foo</cell> | <cell color=b9b9b9>bar</cell> |
| --- | --- |
| <cell color=c9c9c9 left_space=0 left_line=wave left_color=ff0000>fu</cell>  | <cell color=d9d9d9>baz</cell> |
| <cell color=c7c7c7>f8</cell>  | <cell color=d7d7d7>b2z</cell> |
</border>

# Table with merged cells

<table style='Table Grid'>

| <cell align=center>1</cell> | 2 | 3  |
| --- | --- | --- |
| a | b | c |
| d | e | f |
</table>
<merge from_row=0 from_col=0 to_row=0 to_col=2><br>

<table style='Table Grid'>

| <cell align=center>1</cell> | 2 | 3  |
| --- | --- | --- |
| a | b | c |
| d | e | f |
</table>
<merge from_row=0 from_col=1 to_row=0 to_col=2><br>

<table style='Table Grid'>

| <cell align=center>1</cell> | 2 | 3  |
| --- | --- | --- |
| a | b | c |
| d | e | f |
</table>
<merge from_row=0 from_col=0 to_row=2 to_col=0><br>

<table style='Table Grid'>

| <cell align=center>1</cell> | 2 | 3  |
| --- | --- | --- |
| a | b | c |
| d | e | f |
</table>
<merge from_row=1 from_col=0 to_row=2 to_col=0><br>

<table style='Table Grid'>

| 1 | 2 | 3 | 4 | 5 |
| --- | --- | --- | --- | --- |
| a | b | c | d | e |
| f | g | h | i | j |
| a | b | c | d | e |
| f | g | h | i | j |
</table>
<merge from_row=2 from_col=0 to_row=3 to_col=0>
<merge from_row=0 from_col=0 to_row=0 to_col=4><br>

<table style='Table Grid'>

| 1 | 2 | 3 | 4 | 5 |
| --- | --- | --- | --- | --- |
| a | b | c | d | e |
| f | g | h | i | j |
| a | b | c | d | e |
| f | g | h | i | j |
</table>
<merge from_row=0 from_col=0 to_row=1 to_col=1>
<merge from_row=0 from_col=3 to_row=0 to_col=4>
