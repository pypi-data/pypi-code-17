from __future__ import absolute_import, division, print_function

from byte.collection import Collection
from byte.statements import SelectStatement
from tests.base.models.dynamic.user import User

from hamcrest import *

users = Collection(User)


def test_all():
    """Test all() statement can be created."""
    assert_that(users.all(), all_of(
        instance_of(SelectStatement),
        has_properties({
            'collection': users,
            'model': User,

            'properties': ()
        })
    ))


def test_select():
    """Test select() statement can be created."""
    assert_that(users.select(), all_of(
        instance_of(SelectStatement),
        has_properties({
            'collection': users,
            'model': User,

            'properties': ()
        })
    ))


def test_select_properties():
    """Test select() statement can be created with specific properties."""
    assert_that(users.select(
        User['id'],
        User['username']
    ), all_of(
        instance_of(SelectStatement),
        has_properties({
            'collection': users,
            'model': User,

            'properties': ('id', 'username')
        })
    ))


def test_select_names():
    """Test select() statement can be created with specific property names."""
    assert_that(users.select(
        'id',
        'username'
    ), all_of(
        instance_of(SelectStatement),
        has_properties({
            'collection': users,
            'model': User,

            'properties': ('id', 'username')
        })
    ))
