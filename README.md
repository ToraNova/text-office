# Python Text Office 'text-office'
A python tool to convert text-based formats (i.e., md) to documents (e.g., docx, pdf). It is built to be simple to use and integrate with your other workflows. This tool is written using [python-docx](https://python-docx.readthedocs.io/en/latest/) and [mistletoe](https://github.com/miyuchina/mistletoe).

## Why did I made this?
I find editing text-based files much quicker and consistent compared to using Microsoft Word. Nevertheless, I need to create reports in .docx format when I do reporting. While tools like pandoc already exists to convert text files to .docx, it does not _easily_ support exact formatting (e.g., font type, table widths).

Another benefit of this is that because I mainly work on a Linux distro, so it make sense to be able to create .docx documents that are required for my work without use of Microsoft Word.

This is NOT a replacement for Microsoft Word. You will still need that. It is just a tool to help you create report more easily if you have a similar workflow like mine.

## Installation
Installation is very easy with pip. Just do `pip install text-office`

### Pitfalls
If `/home/<your-username>/.local/bin` is not on your PATH, which is the default installation directory for python scripts, you will need to add it to your PATH first.

Temporarily add it to your PATH by `export PATH="$PATH:$HOME/.local/bin"`. For a more persistent solution, do:

Bash
```
echo 'export PATH="$PATH:$HOME/.local/bin"' >> $HOME/.profile
```

Zsh
```
echo 'export PATH="$PATH:$HOME/.local/bin"' >> $HOME/.zshrc
```

Alternatively, you can install the tool globally to /usr/ with `sudo pip install text-office`. This is not recommended!

## Getting Started
Checkout the walkthrough for a use-case creating a penetration testing report using .md files.

1. [Penetration Testing Report Example](getting_started/vapt/README.md)

## Markdown Samples
Here are some markdown samples.

1. [markdown + docx](samples/dual.md)
2. [tables](samples/tables.md)
3. [figures](samples/figures.md)
4. [lists](samples/lists.md)
5. [table-of-contents](samples/toc.md)
6. [headers/footers](samples/headfoot.md)
7. [boiler generation](samples/kvboil.md)
8. [sections](samples/sections.md)

## How is this different from pandoc?
This tool supports use of formatting styles, image width adjustments, fonts etc.

## License
```
Copyright (c) the respective contributors, as shown by the AUTHORS.txt file.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
```
