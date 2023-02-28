import os
from .path_helper import (
        boiler_template_path,
        boiler_template_path_pip,
        )

from .log_helper import log


class InvalidOption(KeyError):
    def __init__(self, tag, key, valids):
        super().__init__(f'invalid opt on tag {tag}: {key} {valids}')


class InvalidValue(ValueError):
    def __init__(self, attr, value, valids):
        super().__init__(f'invalid value on attr {attr}: {value} {valids}')


def ensure_valid_opts(tag, valid_list, opt_dict):
    for k in opt_dict:
        if k not in valid_list:
            raise InvalidOption(tag,k, valid_list)


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
