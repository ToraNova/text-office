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
