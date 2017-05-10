"""Relation tests for dynamic models."""
from __future__ import absolute_import, division, print_function

from tests.base.models.dynamic.album import Album
from tests.base.models.dynamic.artist import Artist
from tests.base.models.dynamic.track import Track


def test_simple():
    """Test simple dynamic model relations."""
    # Artist
    artist = Artist.create(
        id=1,
        title='Daft Punk'
    )

    assert artist.id == 1
    assert artist.title == 'Daft Punk'

    # Album
    album = Album.create(
        id=1,
        artist=artist,

        title='Discovery'
    )

    assert album.id == 1
    assert album.artist_id == 1

    assert album.artist is artist

    assert album.title == 'Discovery'

    # Track
    track = Track.create(
        id=1,
        artist=artist,
        album=album,

        title='One More Time'
    )

    assert track.id == 1
    assert track.artist_id == 1
    assert track.album_id == 1

    assert track.artist is artist
    assert track.album is album

    assert track.title == 'One More Time'
