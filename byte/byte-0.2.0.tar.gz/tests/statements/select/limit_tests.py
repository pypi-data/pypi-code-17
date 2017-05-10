from __future__ import absolute_import, division, print_function

from byte.collection import Collection
from tests.base.models.dynamic.user import User

from hamcrest import *

users = Collection(User)


def test_simple():
    """Test select() statement can be created with limit."""
    assert_that(users.select().limit(12), has_properties({
        'state': has_entries({
            'limit': 12
        })
    }))


def test_offset():
    """Test select() statement can be created with offset."""
    assert_that(users.select().offset(12), has_properties({
        'state': has_entries({
            'offset': 12
        })
    }))
