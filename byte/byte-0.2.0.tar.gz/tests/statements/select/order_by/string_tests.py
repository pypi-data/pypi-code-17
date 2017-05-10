from __future__ import absolute_import, division, print_function

from byte.collection import Collection
from tests.base.models.dynamic.user import User

from hamcrest import *

users = Collection(User)


def test_simple():
    """Test select() statement can be created with order defined by property name."""
    assert_that(users.select().order_by('id'), has_properties({
        'state': has_entries({
            'order_by': equal_to([
                (User['id'], {
                    'order': 'ascending'
                })
            ])
        })
    }))
