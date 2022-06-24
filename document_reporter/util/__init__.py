from shlex import shlex

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
