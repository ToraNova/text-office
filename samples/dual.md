# A Heading

Some text below heading. block types (e.g., headings, paragraphs) ought to be separated by newlines.

## A Smaller Heading - Text Formatting 1

<font color=red>You should see this text in red in microsoft docx, but they will appear normally in a markdown display. This is because markdown renderers typically ignore xml tags, which is what the document-reporter's extended syntax uses for formatting.</font> This text will be in normal. <b>This is a special case, it will appear bold in both docx and markdown renders</b>. This is because markdown recognizes `<b></b>` tags.

<i>Same goes for italics, </i><u>underlines</u> and </strike>strikethrough</strike>. You can nest them together <b><i>like this</i></b>.

Of course, normal markdown notations such as **bold** and *italic* works as well. You can also do ***emphasis*** and ~~strikethrough~~ like this.

<font name=Consolas>The font tag also allow you to customize certain font styles. This is in Consolas.</font><font name=Arial size=20pt>This is also in Arial, but larger.</font><font size=20pt>This is the default font, but larger.</font>

## Text Formatting 2

You may align texts, although this won't be visible in markdown. For instance, the following paragraph is center aligned.

<align center>
This is aligned in the center in docx, but you can't see this via markdown.
</align>

<align right>
This is aligned to the right.
</align>
