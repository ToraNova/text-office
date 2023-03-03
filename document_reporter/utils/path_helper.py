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

import os
import sys

_path_ = os.path.realpath(__file__)
_base_, _file_ = os.path.split(_path_)
_lib_ = _base_[:-_base_[::-1].find(os.path.sep)-1]
prj_root_path = _lib_[:-_lib_[::-1].find(os.path.sep)]
boiler_template_path = os.path.join(prj_root_path, 'boiler_templates')

_mainmod_path_ = os.path.abspath(sys.modules['__main__'].__file__)
_mainmod_base_, _mainmod_file_ = os.path.split(_mainmod_path_)
_local_path_ = _mainmod_base_[:-_mainmod_base_[::-1].find(os.path.sep)-1]
boiler_template_path_pip = os.path.join(_local_path_, 'boiler_templates')
