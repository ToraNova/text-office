# Sample L1 Heading

Some text below heading. block types (e.g., headings, paragraphs) ought to be separated by newlines.

## Text Formatting 1 - Fonts

<font color=red>You should see this text in red in microsoft docx, but they will appear normally in a markdown display. This is because markdown renderers typically ignore xml tags, which is what the document-reporter's extended syntax uses for formatting.</font> This text will be in normal. <b>This is a special case, it will appear bold in both docx and markdown renders</b>. This is because markdown recognizes `<b></b>` tags.

<i>Same goes for italics, </i><u>underlines</u> and </strike>strikethrough</strike>. You can nest them together <b><i>like this</i></b>.

Of course, normal markdown notations such as **bold** and *italic* works as well. You can also do ***emphasis*** and ~~strikethrough~~ like this.

<font name=Consolas>The font tag also allow you to customize certain font styles. This is in Consolas.</font><font name=Arial size=20pt>This is also in Arial, but larger.</font><font size=20pt>This is the default font, but larger.</font>

## Text Formatting 2 - Alignments

You may align texts, although this won't be visible in markdown. For instance, the following paragraph is center aligned. You must include a new-line after the align tag as it is a 'block' tag, meaning it applies to multiple blocks.

<align center>
This is aligned in the center in docx, but you can't see this via markdown.
</align>

<align right>
This is aligned to the right.

### Headings can also be aligned.

text under heading
</align>

## Text Formatting 3 - Lists

A list will appear normally in both markdown renders and the resulting docx

1. one
2. two
    1. satu
        1. yi
        2. er
    2. dua
    3. tiga
3. three
    - foo
        - fu
        - fubar
    - bar
        - baz
        - bazinga

Here is another list, the numbering should restart

1. another one
    1. ali
        1. ah chong
    2. muthu
2. another two
    - unordered list has no numbering

- unordered list item 1
- unordered list item 2
  - child item 1
    - grandchild item
  - child item 2

Unordered list has no numbering, so it does not reset.

- another UL item
- another UL item again
  - yet another UL item again

Set new page with the following. This does not appear in markdown rendering because markdown renders has no notion of "pages".
<pgbr>

## Figures and Captions

A figure and a caption.

![](samples/test_card.png "A caption")

A figure fixed at 10cm width.

<img width=10cm>![](samples/test_card.png "10 cm fixed width")</img>

A figure fixed at 4inch, aligned center.

<align center>
<img width=10cm>![](samples/test_card.png "10 cm fixed width, center-aligned")</img>
</align>
<pgbr>

## Tables

A table with no styling. Use `<br>` tags in cells to set a newline. Each newline character defines a new row.

| Col1 | Col2 |
| ---- | ---- |
| abcd | efgh<br>newline? |
| 1234 |  |
| qwer | <font color=green>xxxxxxxxxxxxx</font> |
| qwer | <font name=Arial><b>xxxxxxxxxxxxx</b></font> |
| img | <img width=50mm>![](samples/test_card.png)</img><br>test in newline |

<pgbr>

A table with table style 'Table Grid'. Leave an empty line after the table tag so markdown can render it properly.

<table style='Table Grid'>

| Col1 | Col2 |
| ---- | ---- |
| abcd | efgh<br>newline? |
| 1234 |  |
| qwer | <font color=green>xxxxxxxxxxxxx</font> |
| qwer | <font name=Arial><b>xxxxxxxxxxxxx</b></font> |
| img | <img width=50mm>![](samples/test_card.png)</img><br>test in newline |
</table>

<pgbr>

A table with table style 'Table Grid' and preset column widths. Likewise, leave an empty space so markdown can render it properly.

<table style='Table Grid' column_widths='5cm, 8cm, 1cm'>

| Col1 | Col2 | Col3 |
| ---- | ---- | --- |
| abcd | efgh | abc
| 1234 |  | |
| qwer | <font color=blue>xxxxxxxxxxxxx</font> | |
| qwer | <font name=Arial><b>xxxxxxxxxxxxx</b></font> | |
| img | <img width=5cm>![](samples/test_card.png)</img><br>test in newline | |
</table>

<pgbr>

## Extras

### Horizontal Lines

Here is a horizontal rule
<hr>

Here is a horizontal rule with small dashed lines
<hr dashsmall>

### Block quotes

Block quotes may be shown in monospace fonts on markdowns, but the tool will display them as normal text in the docx document. Same goes for inline `like this`.

```
monospace font in markdown renders, normal styling in microsoft docx.
```

### Paragraph Spacing (DOCX only)

<para spacing=1 before=6pt>
This text in this paragraph is formatted to have spacing = 1, before 6pt. Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
</para>

<comment>
This line break is required for markdown renderers to split the 2 paragraphs when we enclosed them with xml tags.</comment>
<br>

<para spacing=1.5 before=2pt>
This text in this paragraph is formatted to have spacing = 1.5, before 2pt. Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
</para>
