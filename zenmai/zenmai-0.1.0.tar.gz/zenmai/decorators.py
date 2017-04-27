from .utils import missing


def with_additional(attr):
    def _with_additional(fn):
        if not hasattr(fn, "additionals"):
            fn.additionals = []
        fn.additionals.append(attr)
        return fn

    return _with_additional


with_context = with_additional("context")


def sideeffect(fn):
    def _sideeffect(*args, **kwargs):
        fn(*args, **kwargs)
        return missing

    return _sideeffect
