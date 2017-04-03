def _():
    pass


class caseClass(object):
    def __gt__(self, other):
        return lambda: other


def iter_match(to_match, t):
    equal = True
    a = t.__iter__()
    b = to_match.__iter__()

    while True:
        try:
            aa = a.next()
        except StopIteration:
            aa = None
        try:
            bb = b.next()
        except StopIteration:
            bb = None

        if aa == _:
            continue

        if aa != bb and not (aa is type(bb) or aa == type(bb)):
            equal = False
            break

        if not aa and not bb:
            return equal

    return equal


def is_seq(obj):
    return type(obj) in [str, unicode, list, tuple, buffer, xrange]


def is_instance(to_match, val):
    try:
        return isinstance(to_match, val)
    except TypeError:
        return False


def match_f(to_match, *t):
    i = 0
    stop = len(t)
    while i < stop:
        val = t[i]()
        if val == _ or val == to_match or val is to_match or (
                        is_seq(to_match) and is_seq(val) and iter_match(to_match, val)) \
                or type(to_match) == val or is_instance(to_match, val):
            if hasattr(t[i + 1], '__call__'):
                return t[i + 1](to_match)
            else:
                return t[i + 1]
        i += 2
    raise Exception("No match found for: {}.".format(to_match))


def f_match_f(to_match, *t):
    i = 0
    stop = len(t)
    while i < stop:
        val = t[i]()
        if val == _ or val == to_match or val is to_match or (
                        is_seq(to_match) and is_seq(val) and iter_match(to_match, val)) \
                or type(to_match) == val or is_instance(to_match, val):
            return t[i + 1]
        i += 2
    raise Exception("No match found for: {}.".format(to_match))


class CatchContainer(object):
    __slots__ = ["val"]

    def __rrshift__(self, other):
        self.val = other
        return self

    def __rshift__(self, other):
        return match_f(self.val, *other)

case = caseClass()
match = CatchContainer()
