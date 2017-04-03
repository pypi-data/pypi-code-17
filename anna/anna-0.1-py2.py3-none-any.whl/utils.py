# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import json
import re

import numpy
import scipy.constants as constants
from scipy.constants import physical_constants


def convert_camel_case_to_snake_case(camel_case):
    """
    Convert a string in CamelCaseFormat to snake_case_format.

    Parameters
    ----------
    camel_case : unicode
        The string to be converted.

    Returns
    -------
    snake_case : unicode
        The string converted to snake case.
    """
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', camel_case)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


def safe_math_eval(string, unsafe_error=ValueError, locals_dict=None):
    """
    Evaluate the given mathematical expression after having verified its innocence.

    .. warning::
    This functions uses :py:function:`eval` internally. While it restricts all access to
    ``globals``, ``locals`` and `__builtins__`` one should be careful in using the
    ``locals_dict`` argument.

    Parameters
    ----------
    string : unicode
        The mathematical expression.
    unsafe_error : Exception, optional
        The exception to be raised if evaluating the string is found to be unsafe.
    locals_dict : dict, optional
        A dict which will be used as the ``locals`` argument to ``eval``;
        use with care in order to prevent malicious injections.

    Returns
    -------
    value : float
        The value of the mathematical expression.

    Raises
    ------
    ValueError
        If execution of the given expression is found to be unsafe; the type of
        the exception being raised can be controlled with the `unsafe_error` argument.
    """
    if any(map(
            lambda x: x in string,
            ('__', '()', '[]', '{}', 'lambda', ',', ';', ':', '"', "'")
    )):
        raise unsafe_error('Refusing to evaluate "%s"' % string)
    # Allow a-z for numpy or math functions.
    if re.match(r'^[.*/+\-0-9a-z\s()]+$', string) is None:
        raise unsafe_error('Refusing to evaluate "%s"' % string)
    if locals_dict is None:
        locals_dict = {}
    return eval(string, {'__builtins__': None}, locals_dict)


def supply_with_constants(text):
    """
    Supply the given string with constants values from either ``scipy.constants``
    or ``scipy.constants.physical_constants``. Placeholders for constants should be
    marked via string interpolation format keys: ``'%(name)e'`` (other possible types are
    ``%s`` and ``%f``), where ``name`` is the name of the constant that is either
    an attribute of ``scipy.constants`` or a key in ``scipy.constants.physical_constants``
    (``scipy.constants`` is checked first). Matched keys are replaced with
    their corresponding values using ``%.18e`` format (in order to prevent precision loss).

    Parameters
    ----------
    text : unicode
        The string to be interpolated containing string formatter as constant placeholders.

    Returns
    -------
    supplied_text : unicode
        The string where placeholders have been replaced with their corresponding values.

    Raises
    ------
    ValueError
        If an unmatched placeholder name is encountered.

    Examples
    --------
    >>> supply_with_constants('%(pi)e')
    '3.14159265358979311600e+00'
    >>> supply_with_constants('%(electron mass)f')
    '9.10938355999999975160e-31'
    >>> supply_with_constants('%(proton mass energy equivalent in MeV)s * %(elementary charge)e')
    '9.38272081299999967996e+02 * 1.60217662080000009264e-19'
    """
    if re.match(r'%([defs])', text) is not None:
        raise ValueError('String interpolation is only supported for named placeholders')
    supply = {}
    for key, representation in re.findall(r'%\((?P<key>[0-9a-zA-Z\s\-/{}()_,.]+)\)([efs])', text):
        try:
            supply[key] = getattr(constants, key)
        except AttributeError:
            try:
                supply[key] = physical_constants[key][0]
            except KeyError:
                raise ValueError('Invalid specifier for a (physical) constant: %s' % key)
        text = text.replace('%({0}){1}'.format(key, representation), '%({0}).18e'.format(key))
    return text % supply


def use_docs_from(cls):
    """
    Use the specified class as a source for the decorated method. The decorated method
    will receive the doc string from a method with a similar name of the specified class.

    Parameters
    ----------
    cls : type
        The class which holds the method that serves as doc string source.

    Returns
    -------
    callable
        Decorator which sets the doc string of the decorated method.
    """
    def decorator(method):
        method.__doc__ = getattr(cls, method.__name__).__doc__
        return method
    return decorator


def convert_to_json_serializable_object(obj):
    """
    Convert the given object which is not necessarily JSON serializable to a JSON serializable
    version. If this is not possible then raise a TypeError.

    Parameters
    ----------
    obj

    Raises
    ------
    TypeError
        If the given object cannot be converted
    """
    if isinstance(obj, numpy.ndarray):
        return obj.tolist()
    if hasattr(obj, 'as_json'):
        return obj.as_json()
    try:
        json.dumps(obj)
    except ValueError:
        raise TypeError(
            'Cannot convert object of type %s to a JSON serializable version'
            % type(obj)
        )
    return obj


def to_json_string(json_obj):
    """
    Convert the given JSON serializable object to a JSON string.

    Parameters
    ----------
    json_obj : JSON serializable object

    Returns
    -------
    json_str : unicode
        The JSON string corresponding to the given object.
    """
    return json.dumps(json_obj, indent=4)
