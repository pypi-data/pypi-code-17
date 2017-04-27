from dictknife import deepmerge
from functools import reduce
from collections import OrderedDict


def concat(ds):
    """
    $concat:
      - name: foo
      - age: 10
    """
    return reduce(deepmerge, ds, OrderedDict())
