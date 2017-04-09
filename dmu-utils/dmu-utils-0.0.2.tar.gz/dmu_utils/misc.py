import itertools

DEFAULT = object()
"Sometimes `None` has its own meaning other than a default, so `DEFAULT` constant can be handy"


def get_call_repr(func_or_meth, args=(), kwargs=None):
    kwargs = kwargs or {}
    return '{}({})'.format(
        func_or_meth.__name__,
        ', '.join(itertools.chain((repr(arg) for arg in args),
                                  ('{}={!r}'.format(k, v) for k, v in kwargs.iteritems())))
    )
