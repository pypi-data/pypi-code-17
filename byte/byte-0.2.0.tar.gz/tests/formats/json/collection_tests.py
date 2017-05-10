"""Dynamic tests for memory collections."""
from __future__ import absolute_import, division, print_function

from byte.collection import Collection
from tests.base.core.fixtures import get_fixture_uri
from tests.base.models.dynamic.album import Album
from tests.base.models.dynamic.artist import Artist
from tests.base.models.dynamic.city import City
from tests.base.models.dynamic.track import Track
import byte.compilers.operation
import byte.executors.file
import byte.formats.json

from hamcrest import *


def test_all():
    """Test all items are returned from json-formatted collection."""
    with get_fixture_uri('collections/artists.json') as artists_uri:
        artists = Collection(Artist, artists_uri, plugins=[
            byte.compilers.operation,
            byte.executors.file,
            byte.formats.json
        ])

        # Fetch artists, and validate properties
        assert_that(list(artists.all().iterator()), all_of(
            has_length(5),

            has_items(
                has_properties({
                    'id': 1,
                    'title': 'Gorillaz'
                }),
                has_properties({
                    'id': 2,
                    'title': 'Daft Punk'
                }),
                has_properties({
                    'id': 3,
                    'title': 'Friendly Fires'
                }),
                has_properties({
                    'id': 4,
                    'title': 'Miike Snow'
                }),
                has_properties({
                    'id': 5,
                    'title': 'LCD Soundsystem'
                })
            )
        ))


def test_create():
    """Test items can be created on json-formatted collections."""
    with get_fixture_uri('collections/artists.json') as artists_uri:
        artists = Collection(Artist, artists_uri, plugins=[
            byte.compilers.operation,
            byte.executors.file,
            byte.formats.json
        ])

        # Create artist
        artists.create(id=123, title='Fenech-Soler')

        # Fetch artist, and validate properties
        assert_that(artists.get(123), has_properties({
            'id': 123,
            'title': 'Fenech-Soler'
        }))


def test_get_basic():
    """Test items can be retrieved from json-formatted collections."""
    with get_fixture_uri('collections/artists.json') as artists_uri:
        artists = Collection(Artist, artists_uri, plugins=[
            byte.compilers.operation,
            byte.executors.file,
            byte.formats.json
        ])

        # Fetch artist, and validate properties
        assert_that(artists.get(1), has_properties({
            'id': 1,
            'title': 'Gorillaz'
        }))


def test_get_relations():
    """Test relations can be resolved in json-formatted collections."""
    with get_fixture_uri((
        'collections/artists.json',
        'collections/albums.json',
        'collections/tracks.json'
    )) as (
        artists_uri,
        albums_uri,
        tracks_uri
    ):
        # Artists
        artists = Collection(Artist, artists_uri, plugins=[
            byte.compilers.operation,
            byte.executors.file,
            byte.formats.json
        ])

        # Albums
        albums = Collection(Album, albums_uri, plugins=[
            byte.compilers.operation,
            byte.executors.file,
            byte.formats.json
        ])

        albums.connect(Album.Properties.artist, artists)

        # Tracks
        tracks = Collection(Track, tracks_uri, plugins=[
            byte.compilers.operation,
            byte.executors.file,
            byte.formats.json
        ])

        tracks.connect(Track.Properties.album, albums)
        tracks.connect(Track.Properties.artist, artists)

        # Fetch track, and ensure relations can be resolved
        assert_that(tracks.get(1), has_properties({
            'id': 1,
            'title': 'Ascension (feat. Vince Staples)',

            'artist': has_properties({
                'id': 1,
                'title': 'Gorillaz'
            }),

            'album': has_properties({
                'id': 1,
                'title': 'Humanz',

                'artist': has_properties({
                    'id': 1,
                    'title': 'Gorillaz'
                })
            })
        }))


def test_where():
    """Test json-formatted collections can be filtered with expressions."""
    with get_fixture_uri('collections/cities.json') as cities_uri:
        cities = Collection(City, cities_uri, plugins=[
            byte.compilers.operation,
            byte.executors.file,
            byte.formats.json
        ])

        # Fetch cities, and validate properties
        items = list(cities.select().where(City['country'] == 'New Zealand').iterator())

        assert_that(items, all_of(
            has_length(35),

            has_items(
                has_properties({
                    'id': '2179537',
                    'name': 'Wellington',

                    'country': 'New Zealand',
                    'subcountry': 'Wellington'
                }),
                has_properties({
                    'id': '2179670',
                    'name': 'Wanganui',

                    'country': 'New Zealand',
                    'subcountry': 'Manawatu-Wanganui'
                }),
                has_properties({
                    'id': '2181133',
                    'name': 'Timaru',

                    'country': 'New Zealand',
                    'subcountry': 'Canterbury'
                }),
                has_properties({
                    'id': '2181742',
                    'name': 'Taupo',

                    'country': 'New Zealand',
                    'subcountry': 'Waikato'
                }),
                has_properties({
                    'id': '2184155',
                    'name': 'Pukekohe East',

                    'country': 'New Zealand',
                    'subcountry': 'Auckland'
                }),
            )
        ))
