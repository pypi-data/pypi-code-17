"""Static model tests."""
from __future__ import absolute_import, division, print_function

from byte.model import Model
from byte.property import Property
from tests.base.models.static.user import User

from datetime import datetime
from dateutil.tz import tzutc


def test_create():
    """Test static model generation and the creation of static items."""
    class User(Model):
        class Options:
            slots = True

        id = Property(int, primary_key=True)

        username = Property(str)
        password = Property(str)

        created_at = Property(datetime, default=lambda: datetime.now())
        updated_at = Property(datetime, default=lambda: datetime.now())

    user = User(
        id=1,

        username='one',
        password='hunter12'
    )

    assert user.id == 1

    assert user.username == 'one'
    assert user.password == 'hunter12'

    assert user.created_at
    assert user.updated_at


def test_create_child():
    """Test static model generation with properties defined in a child class."""
    class User(Model):
        class Options:
            slots = True

        class Properties:
            id = Property(int, primary_key=True)

            username = Property(str)
            password = Property(str)

            created_at = Property(datetime, default=lambda: datetime.now())
            updated_at = Property(datetime, default=lambda: datetime.now())

    user = User(
        id=1,

        username='one',
        password='hunter12'
    )

    assert user.id == 1

    assert user.username == 'one'
    assert user.password == 'hunter12'

    assert user.created_at
    assert user.updated_at


def test_encode():
    """Test static model encoding."""
    user = User(
        id=1,

        username='one',
        password='hunter12',

        created_at=datetime(2017, 1, 1, 13, 24, 35),
        updated_at=datetime(2017, 1, 1, 16, 24, 35)
    )

    assert user.to_plain() == {
        'id': 1,

        'username': 'one',
        'password': 'hunter12',

        'created_at': datetime(2017, 1, 1, 13, 24, 35),
        'updated_at': datetime(2017, 1, 1, 16, 24, 35)
    }


def test_encode_translate():
    """Test static model encoding with property value translation."""
    user = User(
        id=1,

        username='one',
        password='hunter12',

        created_at=datetime(2017, 1, 1, 13, 24, 35),
        updated_at=datetime(2017, 1, 1, 16, 24, 35)
    )

    assert user.to_plain(translate=True) == {
        'id': 1,

        'username': 'one',
        'password': 'hunter12',

        'created_at': '2017-01-01T13:24:35+00:00',
        'updated_at': '2017-01-01T16:24:35+00:00'
    }


def test_decode():
    """Test static model decoding."""
    user = User.from_plain({
        'id': 1,

        'username': 'one',
        'password': 'hunter12',

        'created_at': datetime(2017, 1, 1, 13, 24, 35),
        'updated_at': datetime(2017, 1, 1, 16, 24, 35)
    })

    assert user.id == 1

    assert user.username == 'one'
    assert user.password == 'hunter12'

    assert user.created_at == datetime(2017, 1, 1, 13, 24, 35)
    assert user.updated_at == datetime(2017, 1, 1, 16, 24, 35)


def test_decode_translate():
    """Test static model decoding with property value translation."""
    user = User.from_plain(
        {
            'id': 1,

            'username': 'one',
            'password': 'hunter12',

            'created_at': '2017-01-01T13:24:35+00:00',
            'updated_at': '2017-01-01T16:24:35+00:00'
        },
        translate=True
    )

    assert user.id == 1

    assert user.username == 'one'
    assert user.password == 'hunter12'

    assert user.created_at == datetime(2017, 1, 1, 13, 24, 35, tzinfo=tzutc())
    assert user.updated_at == datetime(2017, 1, 1, 16, 24, 35, tzinfo=tzutc())
