try:
    from ds.sys.Unspecified import Unspecified
except ImportError:
    class _Unspecified(object):
        def __repr__(self):
            return 'Unspecified'
        def __str__(self):
            return 'Unspecified'
    Unspecified = _Unspecified()
