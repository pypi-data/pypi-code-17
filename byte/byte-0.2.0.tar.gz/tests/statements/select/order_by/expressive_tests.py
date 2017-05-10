from __future__ import absolute_import, division, print_function

from byte.collection import Collection
from tests.base.models.dynamic.user import User

from hamcrest import *

users = Collection(User)


def test_simple():
    """Test select() statement can be created with order."""
    query = users.select().order_by(
        User['id']
    )

    assert_that(query, has_property('state', equal_to({
        'order_by': [
            (User['id'], {
                'order': 'ascending'
            })
        ]
    })))


def test_options_descending():
    """Test select() statement can be created with descending order."""
    assert_that(users.select().order_by(
        User['id'].desc()
    ), has_properties({
        'state': has_entries({
            'order_by': equal_to([
                (User['id'], {
                    'order': 'descending'
                })
            ])
        })
    }))
