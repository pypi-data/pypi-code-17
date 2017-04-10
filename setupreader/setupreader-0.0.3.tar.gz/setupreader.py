import inspect
import imp
import json
import functools
import argparse

import mock

class BrokenSetupException(Exception):
    """
    setupreader can not find a setup function in your setup.py.

    please make sure your setup.py contains the call to setup.
    If you have placed a guard around the call to setup like this::
    
        def main():
            setup(
                ...
            )

        if __name__ == '__main__':
            main()
    
    make sure the guarding function takes no parameters.
    """
    def __init__(self):
        super(BrokenSetupException, self).__init__(self.__doc__)


def _setup(target, *args, **kwargs):
    target.result = dict(*args, **kwargs)


def load(path):
    setupdict = argparse.Namespace(result=None)

    with mock.patch('setuptools.setup', functools.partial(_setup, setupdict)):
        setup_module = imp.load_source('packagesetup', path)

    if setupdict.result is None:
        # this can happen if the call to setup is inside a guard:
        # if __name__ == '__main__'

        # let's try to find a function that looks like it guards setup.
        functions_found_in_setup_module = inspect.getmembers(
            setup_module, inspect.isfunction)
        for name, candidate in functions_found_in_setup_module:
            argspec = inspect.getargspec(candidate)
            # if the function is named 'main' and it receives no arguments, we
            # declare it found.
            # Also if this package was made by peopls without any knowledge or
            # feeling for python idioms, they might have named it
            # something else as main. We will declare any function that is
            # defined inside the setup_module that received no arguments as a
            # find.
            if (name == 'main' or inspect.getmodule(candidate) == setup_module) and \
                len(argspec.args) == 0:
                candidate()
                break
        else: # we couldn't find anything resembling a guarded setup function.
            raise BrokenSetupException()
                
    return setupdict.result


def main():
    p = argparse.ArgumentParser(description="Read data from setup.py.")
    p.add_argument('path', help="path to setup.py")
    args = p.parse_args()

    print json.dumps(load(args.path), indent=4)


if __name__ == '__main__':
    main()
