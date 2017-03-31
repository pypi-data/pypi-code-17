from collections import namedtuple
from itertools import tee


MatchSummary = namedtuple("MatchSummary", ["is_match", "explanation"])
# Make explanation optional
MatchSummary.__new__.__defaults__ = (None,)


def pairwise(iterable):
    """
    [a, b, c] -> [(a, b), (b, c)]
    """
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)


def make_fluent_func(cls):
    def func(*args, **kwargs):
        return cls(*args, **kwargs)
    return func


def explain_none(f):
    """
    Wrap f to accept an explain argument and add an explanation of `None`.
    """
    def ret(*args, **kwargs):
        kwargs.pop('explain')
        matched = f(*args, **kwargs)
        return MatchSummary(matched)
    return ret
