'''
Copyright (C) 2023 ToraNova

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published
    by the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
'''

import traceback
from mistletoe import block_token

from .. import utils
from .documentx import Renderer as DocxRenderer
from docxcompose.composer import Composer

OPNAME = [
        'mdgen',
        'markdown',
        ]

def can_process(fn):
    return fn.endswith('.md')

def file_generate(in_path, renderer, encoding='utf-8', **kwargs):
    """
    Converts markdown input to the output supported by the given renderer.
    If no renderer is supplied, ``HTMLRenderer`` is used.
    Note that extra token types supported by the given renderer
    are automatically (and temporarily) added to the parsing process.
    """
    with open(in_path, 'r', encoding=encoding) as infile:
        with renderer(tag=in_path, **kwargs) as rdr:
            outfile = rdr.render(block_token.Document(infile))
            return outfile

def docx_generate(mdarg, encoding='utf-8', **kwargs):
    outf = None

    if isinstance(mdarg, list) and len(mdarg) > 0:
        try:
            md = mdarg[0]
            main_doc = file_generate(md, DocxRenderer, encoding, **kwargs)
            main_comp = Composer(main_doc)

            for md in mdarg[1:]:
                app_doc = file_generate(md, DocxRenderer, encoding, **kwargs)
                main_comp.append(app_doc)

            outf = main_comp.doc
        except Exception as e:
            # if something messes up here, we must raise
            # this is a fatal error
            #utils.log.error(f'error on input "{md}" - {e}')
            utils.log.exception(f'error on input "{md}" - {e}')

    else:
        outf = file_generate(mdarg, DocxRenderer, encoding, **kwargs)

    #utils.docx_helper.set_updatefields(outf, 'true')
    return outf
