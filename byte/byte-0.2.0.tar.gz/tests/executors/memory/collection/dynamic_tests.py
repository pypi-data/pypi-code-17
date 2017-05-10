"""Dynamic tests for memory collections."""
from __future__ import absolute_import, division, print_function

from byte.collection import Collection
from tests.base.models.dynamic.album import Album
from tests.base.models.dynamic.artist import Artist
from tests.base.models.dynamic.track import Track
import byte.compilers.operation
import byte.executors.memory


def test_basic():
    """Test collection with dynamic models."""
    artists = Collection(Artist, 'memory://', plugins=[
        byte.compilers.operation,
        byte.executors.memory
    ])

    # Update memory collection
    artists.executor.update({
        1: {
            'id': 1,
            'title': 'Daft Punk'
        }
    })

    # Fetch artist, and validate properties
    artist = artists.get(1)

    assert artist
    assert artist.id == 1
    assert artist.title == 'Daft Punk'


def test_relations():
    """Test collection relations with dynamic models."""
    # Artists
    artists = Collection(Artist, 'memory://', plugins=[
        byte.compilers.operation,
        byte.executors.memory
    ])

    # Albums
    albums = Collection(Album, 'memory://', plugins=[
        byte.compilers.operation,
        byte.executors.memory
    ])

    albums.connect(Album.Properties.artist, artists)

    # Tracks
    tracks = Collection(Track, 'memory://', plugins=[
        byte.compilers.operation,
        byte.executors.memory
    ])

    tracks.connect(Track.Properties.album, albums)
    tracks.connect(Track.Properties.artist, artists)

    # Create objects
    artists.create(
        id=1,
        title='Daft Punk'
    )

    albums.create(
        id=1,
        artist_id=1,

        title='Discovery'
    )

    tracks.create(
        id=1,
        artist_id=1,
        album_id=1,

        title='One More Time'
    )

    # Fetch track, and ensure relations can be resolved
    track = tracks.get(1)

    assert track.id == 1

    assert track.artist.id == 1

    assert track.album.id == 1
    assert track.album.artist.id == 1
