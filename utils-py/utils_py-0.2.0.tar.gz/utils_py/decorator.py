#!/usr/bin/python
# -*- coding: utf-8 -*-

# Authors: Yitian Jia <ytjia.zju@gmail.com>


import sys


def class_check_para(**kw):
    """
    force check accept and return,
    decorator, @class_check_para(accept=, returns=, mail=)
    :param kw:
    :return:
    """
    try:
        def decorator(f):
            def new_f(*args):
                if "accepts" in kw:
                    assert len(args) == len(kw["accepts"]) + 1
                    arg_types = tuple(map(type, args[1:]))
                    if arg_types != kw["accepts"]:
                        msg = decorator_info(f.__name__, kw["accepts"],
                                             arg_types, 0)
                        print >> sys.stderr, 'TypeWarning: ', msg
                        if "mail" in kw:
                            kw["mail"].do_warn(msg)
                        raise TypeError, msg
                result = f(*args)
                if "returns" in kw:
                    res_type = type(result)
                    if res_type != kw["returns"]:
                        msg = decorator_info(f.__name__, (kw["returns"],),
                                             (res_type,), 1)
                        print >> sys.stderr, 'TypeWarning: ', msg
                        if "mail" in kw:
                            kw["mail"].do_warn(msg)
                        raise TypeError, msg
                return result

            new_f.__name__ = f.__name__
            return new_f

        return decorator
    except KeyError, key:
        raise KeyError, str(key) + "is not a valid keyword argument"
    except TypeError, msg:
        raise TypeError, msg


def decorator_info(f_name, expected, actual, flag):
    """
    Convenience function returns nicely formatted error/warning msg.
    :param f_name:
    :param expected:
    :param actual:
    :param flag:
    :return:
    """
    format = lambda types: ', '.join([str(t).split("'")[1] for t in types])
    expected, actual = format(expected), format(actual)
    msg = "'{}' method ".format(f_name) \
          + ("accepts", "returns")[flag] + " ({}), but ".format(expected) \
          + ("was given", "result is")[flag] + " ({})".format(actual)

    return msg
