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
import io
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

def render_file(infile, **kwargs):
    """
    Converts markdown input to the output supported by the given renderer.
    If no renderer is supplied, ``HTMLRenderer`` is used.
    Note that extra token types supported by the given renderer
    are automatically (and temporarily) added to the parsing process.
    """
    with DocxRenderer(**kwargs) as rdr:
        outfile = rdr.render(block_token.Document(infile))
        return outfile

def docx_generate(mdarg, encoding='utf-8', pre_merge=True, **kwargs):
    outf = None

    if pre_merge and isinstance(mdarg, list) and len(mdarg) > 0:
        try:
            mdbuf = io.StringIO()
            for md in mdarg:
                with open(md, 'r', encoding=encoding) as infile:
                    mdbuf.write(infile.read())
            mdbuf.seek(0)
            outf = render_file(mdbuf, **kwargs)
        except Exception as e:
            utils.log.exception(f'error on input "{md}" - {e}')

    elif isinstance(mdarg, list) and len(mdarg) > 0:
        try:
            md = mdarg[0]
            with open(md, 'r', encoding=encoding) as infile:
                main_doc = render_file(infile, **kwargs)
                main_comp = Composer(main_doc)

            for md in mdarg[1:]:
                with open(md, 'r', encoding=encoding) as infile:
                    app_doc = render_file(infile, **kwargs)
                    main_comp.append(app_doc)

            outf = main_comp.doc
        except Exception as e:
            # if something messes up here, we must raise
            # this is a fatal error
            #utils.log.error(f'error on input "{md}" - {e}')
            utils.log.exception(f'error on input "{md}" - {e}')

    else:
        with open(mdarg, 'r', encoding=encoding) as infile:
            outf = render_file(infile, **kwargs)

    #utils.docx_helper.set_updatefields(outf, 'true')
    return outf
