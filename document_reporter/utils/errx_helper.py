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
from .path_helper import (
        boiler_template_path,
        boiler_template_path_pip,
        )

from .log_helper import log


class InvalidAttr(KeyError):
    def __init__(self, attr, valids):
        super().__init__(f'invalid attr: {attr} {valids}')

class MissingAttr(KeyError):
    def __init__(self, attr, required):
        super().__init__(f'missing attr: {attr} {required}')

class InvalidValue(ValueError):
    def __init__(self, attr, value, valids):
        super().__init__(f'invalid value on attr "{attr}": {value} {valids}')

class InvalidType(TypeError):
    def __init__(self, used, desired):
        super().__init__(f'invalid type used "{used}", requires "{desired}"')

def ensure_and_set(vkey, vtype, v, obj, objkey=None, parser=None):
    if objkey is None:
        objkey = vkey

    if isinstance(v, dict):
        v = v.get(vkey)

    if callable(parser):
        v = parser(v)

    if isinstance(vtype, list):
        # allow OR types
        for vtype_or in vtype:
            if isinstance(v, vtype_or):
                # if any meets, sets and exit
                setattr(obj, objkey, v)
                return
    else:
        # singular type
        if isinstance(v, vtype):
            # meets, sets and exists
            setattr(obj, objkey, v)
            return

    if v is not None:
        # v is specified, but invalid type, dev error
        raise InvalidType(type(v), vtype)

def ensure_all_attr(required, opt_dict):
    for k in required.keys():
        if k not in opt_dict:
            raise MissingAttr(k, required)
        parser, valids = required[k]
        v = opt_dict.get(k)
        try:
            opt_dict[k] = parser(v)
        except Exception as e:
            raise InvalidValue(k, v, valids)

def ensure_valid_attr(valid_list, opt_dict):
    for k in opt_dict:
        if k not in valid_list:
            raise InvalidAttr(k, valid_list)


def ensure_valid_value(attr, vmap, v):
    if v not in vmap:
        raise InvalidValue(attr, v, list(vmap.keys()))


def ensure_template_file(t, auto_add_suffix=None):

    tplfn = t
    if isinstance(auto_add_suffix, str):
        if not tplfn.endswith(auto_add_suffix):
            tplfn += auto_add_suffix

    btplfn = tplfn

    if not os.path.isfile(tplfn):
        log.warn(f"cannot find boiler template '{tplfn}' in current working directory, defaulting to built-ins")
        tplfn = os.path.join(boiler_template_path, btplfn)

    if not os.path.isfile(tplfn):
        tplfn = os.path.join(boiler_template_path_pip, btplfn)

    if not os.path.isfile(tplfn):
        raise FileExistsError(f"cannot find boiler template '{btplfn}' in built-in templates dir")

    return tplfn
