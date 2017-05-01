from collections import OrderedDict


def _format(d, kwargs, factory):
    if hasattr(d, "items"):
        for k, v in d.items():
            return factory((_format(k, kwargs, factory), _format(v, kwargs, factory)) for k, v in d.items())
    elif isinstance(d, (list, tuple)):
        return [_format(x, kwargs, factory) for x in d]
    elif isinstance(d, (str, bytes)):
        return d.format(**kwargs)
    else:
        return d


def format(d, **kwargs):
    return _format(d, kwargs, factory=OrderedDict)
