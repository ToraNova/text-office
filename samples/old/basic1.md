# heading1

blablabla, these are some text, i would like them to be in my .docx

newpara test, margins should apply

## heading2

paragraph test **bold** *italic* (TM)
***italic and bold?***
~~strikethrough~~

### heading3

md2report special tokens:
<font color=red>this is in red</font>
<b>this is in bold</b>
<i>this is in italic</i>
<u>this is underlined</u>
<strike>strikethrough</strike>
<font color=blue><b><i><u>blue text in bold, underlined and italic</u></i></b></font>
<font name=Arial>testing a different font</font>
<font size=20pt>testing a bigger font</font>
<font name=Arial size=20pt>Bigger and different</font>

<align center>
all block/spans here should be aligned in the <strike>left</strike> center

multiple paragraphs **works** as <font name=Consolas>well</font>

### EVEN HEADINGS!

TEST URL
[hahah](https://google.com)

</align>

<para style='No Spacing'>
testing a paragraph style format, 'No Spacing' is a default style, let's now try a very long line blablabalabaaaaalalalalaallaalalalaaaaaaaaaaaaaaaaaaaaasdkajsdasddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddwkajwhdkajwhdkddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddakwdhawkdawd

newline, note that this has no margin coz 'no spacing'? incoming pagebreak
</para>

<pgbr>

## numbering test

1. one
2. two
3. three
4. four
5. five
6. six
7. seven
8. eight
9. nine
    1. one
    2. two
        1. one
        2. two
10. ten
    - test
    - test2
11. eleven
    1. one
    2. two
        1. one
        2. two
12. twelve

another list, numbering should restart

<align center>
1. one
2. two
3. three
  1. one
  2. two
</align>

## unordered list

- the first
- the second
- the third
- the fourth
  - another
  - another 2

ul don't reset, duh

- the first
- the second
  - another

## image test

absolute path image, default image width
![altxt](../../Pictures/fun/chad.jpg "TODO: caption for this image")

these images has fixed width 10cm, with aspect ratio maintained
<img width=10cm>
![](../../Pictures/fun/chad.jpg "TODO: caption for this image")
</img>

<align center>
<img width=10cm>![](../../Pictures/fun/doomer.jpg "TODO: caption for this image")</img>
</align>

<align center>
1. <img width=5cm>![](../../Pictures/fun/golden_ticket.png "TODO: caption for this image")</img>
2. <img width=5cm>![](samples/teh_tarik.png)</img>
</align>


<pgbr>

## some horizontal rule

<hr>
<hr dashsmall>

<pgbr>

## basic table (no formatting)

| Col1 | Col2 |
| ---- | ---- |
| abcd | efgh<br>newline? |
| 1234 |  |
| qwer | <font color=green>xxxxxxxxxxxxx</font> |
| qwer | <font name=Arial><b>xxxxxxxxxxxxx</b></font> |
| img | <img width=50mm>![](../../Pictures/fun/wojak.jpg)</img><br>test in newline |

## table with style (Table Grid)

<table style='Table Grid'>

| Col1 | Col2 |
| ---- | ---- |
| abcd | efgh |
| 1234 |  |
| qwer | <font color=green>xxxxxxxxxxxxx</font> |
| qwer | <font name=Arial><b>xxxxxxxxxxxxx</b></font> |
| img | <img width=5cm>![](../../Pictures/fun/wojak.jpg)</img><br>test in newline |

</table>

## table with style and custom column width

<table style='Table Grid' column_widths='5cm, 8cm, 1cm'>

| Col1 | Col2 | Col3 |
| ---- | ---- | --- |
| abcd | efgh | abc
| 1234 |  | |
| qwer | <font color=blue>xxxxxxxxxxxxx</font> | |
| qwer | <font name=Arial><b>xxxxxxxxxxxxx</b></font> | |
| img | <img width=5cm>![](../../Pictures/fun/wojak.jpg)</img><br>test in newline | |

</table>
