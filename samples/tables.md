# Table Tests

| hdr 1 | hdr 2 |
| --- | --- |
| row 1 col 1 | row 1 col 2 |
| row 2 col 1 | <cell color=ffc000> row 2 col 2</cell> |

<hr>

<align center>
<table style='Table Grid' column_widths='1.11in, 4in, 1.11in'>

| <cell color=000000></cell> | <cell color=000000></cell> | <cell color=000000></cell> |
| --- | --- |
| row 1 col 1 | row 1 col 2 | row 1 col 3 |
| row 2 col 1 | row 2 col 2 | row 1 col 3 |
</table>
</align>

<hr>

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

<table style='Table Grid' column_widths='1.11in, 1.11in, 4in'>
<para before=6pt spacing=1.15 after=6pt>

| | | |
| --- | --- |
| row 1 col 1 | row 1 col 2 | row 1 col 3 |
| <cell color=ff0000><font color=0000ff>row 2 col 1</font></cell> | row 2 col 2 | row 1 col 3 |
</para>
</table>

<hr dashsmall>

<table style='Table Grid' column_widths='5cm, 8cm, 1cm'>

| Col1 | Col2 | Col3 |
| ---- | ---- | --- |
| abcd | efgh | abc
| 1234 |  | |
| qwer | <font color=blue>xxxxxxxxxxxxx</font> | |
| qwer | <font name=Arial><b>xxxxxxxxxxxxx</b></font> | |
| img | <img width=5cm>![](samples/test_card.png)</img><br>test in newline | |
</table>
