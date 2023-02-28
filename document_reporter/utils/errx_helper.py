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

