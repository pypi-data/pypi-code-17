import re


class NoMatchException(Exception):
    pass


class IdentifiersNotFound(Exception):
    def __init__(self, identifiers=None):
        self.identifiers = identifiers


def get_identifiers(pattern_string):
    m = re.findall(r'\{(\w+)\}', pattern_string, )
    if not m:
        return []
    return m


def validate_patterns(pattern_in, pattern_out):
    ids_in = set(get_identifiers(pattern_in))
    ids_out = set(get_identifiers(pattern_out))
    ids_not_found = [s for s in ids_out if s not in ids_in]
    if ids_not_found:
        raise IdentifiersNotFound(ids_not_found)


def to_re_in(tpl):
    return '^'+re.sub(r'\{(\w+)\}', r'(?P<\1>.+)', tpl)+'$'


def to_re_out(tpl):
    return re.sub(r'\{(\w+)\}', r'\\g<\1>', tpl)


def new_name(filename, tpl_in, tpl_out):
    re_in = to_re_in(tpl_in.replace('.', '\.'))
    re_out = to_re_out(tpl_out)

    if not re.match(re_in, filename):
        raise NoMatchException()

    return re.sub(re_in, re_out, filename)
