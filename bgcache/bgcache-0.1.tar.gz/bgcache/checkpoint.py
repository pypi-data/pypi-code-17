import gzip
import inspect

import dill

from os import makedirs
from os.path import exists, join, dirname


def bgcheckpoint(*variables):
    """

    Create a checkpoint of the given variables.

    Usage example:

    a, b, c = bgcheckpoint(vars(), 'a', 'b', 'c')

    :param namespace:
    :param variables:
    :return:
    """

    frame = inspect.currentframe()
    namespace = frame.f_back.f_locals

    result = []
    for variable in variables:
        if type(variable) != str:
            continue

        value = None
        file_key = join(".bgcheckpoint", "{}.gz".format(variable))
        if variable in namespace:

            value = namespace[variable]

            # Store it
            makedirs(dirname(file_key), exist_ok=True)
            with gzip.open(file_key, "wb") as fd:
                dill.dump(value, fd)

        else:

            if exists(file_key):
                with gzip.open(file_key, "rb") as fd:
                    value = dill.load(fd)

        result.append(value)

    return tuple(result)