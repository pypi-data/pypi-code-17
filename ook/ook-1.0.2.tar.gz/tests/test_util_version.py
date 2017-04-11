"""Tests for `ook.util.Version`."""

from operator import eq
from operator import ge
from operator import gt
from operator import le
from operator import lt
from operator import ne

import pytest

from ook.util import Version

from tests import VERSION_ARGS


@pytest.mark.parametrize('version', map(Version, VERSION_ARGS))
def test_repr(version):
    """`Version` instance has a sensible `repr` value"""
    assert repr(version) == "Version(%r)" % str(version)


def params_mmm():
    """yield `Version` instances and `major`|`minor`|`micro` attributes"""
    attrs = ("major", "minor", "micro")
    for version in map(Version, VERSION_ARGS):
        for index, attr in enumerate(getattr(version, a) for a in attrs):
            yield version, index, attr


@pytest.mark.parametrize('version,index,attr', params_mmm())
def test_mmm(version, index, attr):
    """`Version` instance has sensible `major`|`minor`|`micro` attributes"""
    # pylint: disable=redefined-variable-type
    try:
        expected_value = int(str(version).split(".")[index])
    except IndexError:
        expected_value = None
    except ValueError:
        expected_value = float("inf")
    assert attr == expected_value


def params_compare():
    """yield `Version` comparisons"""
    for ver1 in map(Version, VERSION_ARGS):
        for ver2 in map(Version, VERSION_ARGS):
            for oper in (eq, ge, gt, le, lt, ne):
                yield oper, ver1, ver2


@pytest.mark.parametrize('oper,ver1,ver2', params_compare())
def test_compare(oper, ver1, ver2):
    """`Version` instances compare as expected"""
    assert oper(ver1, ver2) == oper(ver1.truncate(ver2), ver2.truncate(ver1))


def params_cmp_unorderable():
    """yield `Version`, non-`Version` comparisons"""
    for nonversion in VERSION_ARGS:
        if isinstance(nonversion, Version):
            continue
        for version in map(Version, VERSION_ARGS):
            for oper in (ge, gt, le, lt):
                yield oper, version, nonversion


@pytest.mark.parametrize('oper,version,nonversion', params_cmp_unorderable())
def test_cmp_unorderable(oper, version, nonversion):
    """Comparing `Version` instance against non-`Version` fails"""
    with pytest.raises(TypeError):
        oper(version, nonversion)
