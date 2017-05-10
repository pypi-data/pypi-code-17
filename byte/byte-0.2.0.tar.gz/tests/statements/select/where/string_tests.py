from __future__ import absolute_import, division, print_function

from byte.collection import Collection
from byte.expressions import Equal, LessThan, NotEqual, Or
from tests.base.models.dynamic.user import User

from hamcrest import *

users = Collection(User)


def test_or():
    """Test select() statement can be created with an OR operator inside a string expression."""
    query = users.select().where(
        'id < 35 or username == "alpha"'
    )

    assert_that(query, has_properties({
        'state': has_entries({
            'where': [
                Or(
                    LessThan(User.Properties.id, 35),
                    Equal(User.Properties.username, 'alpha')
                )
            ]
        })
    }))


def test_or_brackets():
    """Test select() statement can be created with an OR operator and brackets inside a string expression."""
    query = users.select().where(
        'id < 35 AND (username != "alpha" or password == "beta") AND password ne "alpha"'
    )

    assert_that(query, has_properties({
        'state': has_entries({
            'where': [
                LessThan(User.Properties.id, 35),
                Or(
                    NotEqual(User.Properties.username, 'alpha'),
                    Equal(User.Properties.password, 'beta')
                ),
                NotEqual(User.Properties.password, 'alpha')
            ]
        })
    }))


def test_parameters():
    """Test select() statement can be created with parameters inside a string expression."""
    query = users.select().where(
        'id < ? AND username != ?',
        (35, 'alpha')
    )

    assert_that(query, has_properties({
        'state': has_entries({
            'where': [
                LessThan(User.Properties.id, 35),
                NotEqual(User.Properties.username, 'alpha')
            ]
        })
    }))
