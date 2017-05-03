from dictknife import deepmerge
from zenmai.utils import quote


def concat(ds, override=False, sep="\n"):
    """
    $concat:
      - name: foo
      - age: 10
    """
    if not ds:
        return {}
    elif hasattr(ds[0], "keys"):
        return quote(deepmerge(*ds, override=override))
    else:
        return sep.join(ds)
