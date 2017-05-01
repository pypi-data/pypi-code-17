from dictknife import deepmerge
from zenmai.utils import quote


def concat(ds, override=False):
    """
    $concat:
      - name: foo
      - age: 10
    """
    return quote(deepmerge(*ds, override=override))
