from __future__ import absolute_import, division, print_function

from byte.model import Model
from byte.property import Property
from tests.base.models.dynamic.album import Album
from tests.base.models.dynamic.artist import Artist


class Track(Model):
    class Options:
        slots = True

    id = Property(int, primary_key=True)
    artist = Property(Artist)
    album = Property(Album)

    title = Property(str)
