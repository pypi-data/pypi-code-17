__all__ = ["_nil", "_if", "_get", "_try", "_times"]


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


def _get(func):
    try:
        return func()
    except:
        return _nil


class SugarTry:
    def __enter__(self):
        pass

    def __exit__(self, *args):
        return True

    def __rmatmul__(self, left_opnd):
        return self

_try = SugarTry()


class _times:
    def __init__(self, func):
        self.func = func

    def __rmatmul__(self, left_opnd):
        return (self.func() for x in range(left_opnd))


if __name__ == "__main__":
    if "test _if":
        x = 42
        x @= 24 @_if([1, 2, 3])
        assert x == 24
        x @= 42 @_if({})
        assert x == 24

    if "test _try & _get":
        del x
        with _try:
            x = 3 / 0
        x = _get(lambda: x)
        assert x is _nil
        with "successful code" @_try:
            y = -9
        x = _get(lambda: abs(y))
        assert x == 9

    if "test _times":
        n = []
        foo = lambda x: x.append(0) or str(len(x))
        assert ''.join(5 @_times(lambda: foo(n))) == '12345'

