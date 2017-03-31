from itertools import repeat
__all__ = ["_if", "_try", "_times"]


class SugarNil:
    pass


_nil = SugarNil()


class SugarIf:
    def __init__(self, is_true):
        self.is_true = is_true
        self.value = _nil

    def __rmatmul__(self, left_opnd):
        if self.value is _nil:
            self.value = left_opnd
            return self
        else:
            return self.value if self.is_true else left_opnd


def _if(is_true):
    return SugarIf(is_true)


class SugarTry:
    def __enter__(self):
        pass

    def __exit__(self, *args):
        return True

    def __rmatmul__(self, left_opnd):
        return self

_try = SugarTry()


class SugarTimes:
    def __rmatmul__(self, left_opnd):
        return repeat(None, left_opnd)


_times = SugarTimes()


if __name__ == "__main__":
    if "test _if":
        x = 42
        x @= 24 @_if([1, 2, 3])
        assert x == 24
        x @= 42 @_if({})
        assert x == 24

    if "test _try":
        x = None
        with _try:
            x = 3 / 0
        assert x is None
        with "successful code" @_try:
            y = -9
        assert y == -9

    if "test _times":
        n = []
        m = list(n.append(0) or len(n) for _ in 5 @_times)
        assert m == [1, 2, 3, 4, 5]
        for _ in 3 @_times:
            m.pop()
            n.pop()

        assert m == [1, 2] and n == [0, 0]
