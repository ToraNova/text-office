# table test

| hdr 1 | hdr 2 |
| --- | --- |
| row 1 col 1 | row 1 col 2 |
| row 2 col 1 | <cell color=ffc000 row 2 col 2 |

<align center>
<table style='Table Grid' column_widths='1.11in, 1.11in, 4in'>
| <cell color=000000></cell> | <cell color=000000></cell> | <cell color=000000></cell> |
| --- | --- |
| row 1 col 1 | row 1 col 2 | row 1 col 3 |
| row 2 col 1 | row 2 col 2 | row 1 col 3 |
</table>
</align>

<align right>
<table style='Table Grid' column_widths='1.11in, 1.11in, 4in' caption='caption test'>
| | | |
| --- | --- |
| row 1 col 1 | row 1 col 2 | row 1 col 3 |
| <cell color=ff0000><font color=0000ff>row 2 col 1</font></cell> | row 2 col 2 | row 1 col 3 |
</table>
</align>

<comment>
if two tables are together with the same style, word automatically joins them, unless a break in intorduced in between</comment>
<br>

<table style='Table Grid' column_widths='1.11in, 1.11in, 4in'>
<para before=6pt spacing=1.15 after=6pt>
| | | |
| --- | --- |
| row 1 col 1 | row 1 col 2 | row 1 col 3 |
| <cell color=ff0000><font color=0000ff>row 2 col 1</font></cell> | row 2 col 2 | row 1 col 3 |
</para>
</table>
