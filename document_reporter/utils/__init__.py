import os
import sys
from shlex import shlex

_path_ = os.path.realpath(__file__)
_base_, _file_ = os.path.split(_path_)
_lib_ = _base_[:-_base_[::-1].find(os.path.sep)-1]
prj_root_path = _lib_[:-_lib_[::-1].find(os.path.sep)]
boiler_template_path = os.path.join(prj_root_path, 'boiler_templates')

_mainmod_path_ = os.path.abspath(sys.modules['__main__'].__file__)
_mainmod_base_, _mainmod_file_ = os.path.split(_mainmod_path_)
_local_path_ = _mainmod_base_[:-_mainmod_base_[::-1].find(os.path.sep)-1]
boiler_template_path_pip = os.path.join(_local_path_, 'boiler_templates')

def parse_kv_pairs(text, item_sep=",", value_sep="="):
    """Parse key-value pairs from a shell-like text."""
    # initialize a lexer, in POSIX mode (to properly handle escaping)
    lexer = shlex(text, posix=True)
    # set ',' as whitespace for the lexer
    # (the lexer will use this character to separate words)
    lexer.whitespace = item_sep
    # include '=' as a word character
    # (this is done so that the lexer returns a list of key-value pairs)
    # (if your option key or value contains any unquoted special character, you will need to add it here)
    lexer.wordchars += value_sep
    lexer.wordchars += '.' # allow dot
    # then we separate option keys and values to build the resulting dictionary
    # (maxsplit is required to make sure that '=' in value will not be a problem)

    try:
        od = dict(word.split(value_sep, maxsplit=1) for word in lexer)
        return od
    except Exception as e:
        raise ValueError(f'attribute error: {text}')

def warn_invalid_opts(tag, valid_list, opt_dict):
    for k in opt_dict:
        if k not in valid_list:
            print(f'Warning for "{tag}", invalid opt; {k}')

def show_error(tag, errmsg):
    print(f'Exception for "{tag}", {errmsg};')
