# Python Document Reporter 'document-reporter'
A python tool to convert text-based formats (i.e., md) to documents (e.g., docx, pdf). It is built to be simple to use and integrate with your other workflows. This tool is written using [python-docx](https://python-docx.readthedocs.io/en/latest/) and [mistletoe](https://github.com/miyuchina/mistletoe).

## Why did I made this?
I find editing text-based files much quicker and consistent compared to using Microsoft Word. Nevertheless, I need to create reports in .docx format when I do reporting. While tools like pandoc already exists to convert text files to .docx, it does not _easily_ support exact formatting (e.g., font type, table widths).

Another benefit of this is that because I mainly work on a Linux distro, so it make sense to be able to create .docx documents that are required for my work without use of Microsoft Word.

This is NOT a replacement for Microsoft Word. You will still need that. It is just a tool to help you create report more easily if you have a similar workflow like mine.

## Installation
Installation is very easy with pip. Just do `pip install document-reporter`

### Pitfalls
If /home/<your-username>/.local/bin is not on your PATH, which is the default installation directory for python scripts, you will need to add it to your PATH first.

Temporarily add it to your PATH by `export PATH="$PATH:$HOME/.local/bin"`. For a more persistent solution, do:

Bash
```
echo 'export PATH="$PATH:$HOME/.local/bin"' >> $HOME/.profile
```

Zsh
```
echo 'export PATH="$PATH:$HOME/.local/bin"' >> $HOME/.zshrc
```

Alternatively, you can install the tool globally to /usr/ with `sudo pip install document-reporter`. This is not recommended!

## Getting Started
Checkout the walkthrough for a use-case creating a penetration testing report using .md files.

1. [Penetration Testing Report Example](getting_started/vapt/README.md)

## Markdown Samples
Here are some markdown samples.

1. [messy-all](samples/basic1.md)
2. [tables](samples/tables.md)
3. [figures](samples/figures.md)
4. [lists](samples/lists.md)

## How is this different from pandoc?
This tool supports use of formatting styles, image width adjustments, fonts etc.
