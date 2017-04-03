"""Regular expression in regular expression"""

import re

__version__ = '1.1.1'
__author__ = 'Meme Kagurazaka'
__license__ = 'Public Domain'


def rer(re_string, re_group=0,
        item_continuation=lambda _: _, list_continuation=lambda _: _,
        re_continuation=None):
    """rer atom

    This function use regular expression string `re_string' and the group
    `re_group' (default 0) to match the `data'. This will evaluates a list,
    a function `re_continuation' will apply to every match of the list,
    a function `list_continuation' will apply to the list. `list_continuation'
    does nothing by default.

    `re_continuation' applies `item_continuation' to `re_group' by default.

    Return value is a function which can be apply to the `data'.
    Return value can also be used as a `item_continuation' or
    `list_continuation' of another rer recursively.
    """

    if re_continuation is None:
        re_continuation = lambda _: item_continuation(_.group(re_group))

    return lambda x: list_continuation(
        [re_continuation(_) for _ in re.compile(re_string).finditer(x)])
