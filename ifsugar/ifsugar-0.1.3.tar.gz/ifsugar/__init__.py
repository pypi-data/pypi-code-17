"""usage:
    from ifsugar import _if, _try, _times
or
    from ifsugar.ifsugar import *

x @= A @_if(B) <==> if B: x = A
with _try: ...code... <==> try: ... code... except: pass
n @_times <==> itertools.repeat(None, n)

example:
>>> x = 42
>>> x @= 24 @_if([1, 2, 3])
>>> assert x == 24

>>> with "I am comment" @_try:
...     y = -9
>>> assert y == -9

>>> n = []
>>> assert list(n.append(0) or len(n) for _ in 5 @_times) == [1, 2, 3, 4, 5]
"""

from . import ifsugar
from .ifsugar import *
