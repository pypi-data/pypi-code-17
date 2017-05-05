import re


def to_re_in(tpl):
    return '^'+re.sub(r'\{(\w+)\}', r'(?P<\1>.+)', tpl)+'$'


def to_re_out(tpl):
    return re.sub(r'\{(\w+)\}', r'\\g<\1>', tpl)


def new_name(filename, tpl_in, tpl_out):
    re_in = to_re_in(tpl_in)
    re_out = to_re_out(tpl_out)

    if not re.match(re_in, filename):
        return None
    try:
        return re.sub(re_in, re_out, filename)
    except IndexError:
        return None