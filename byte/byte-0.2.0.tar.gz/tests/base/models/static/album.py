from __future__ import absolute_import, division, print_function

from byte.model import Model
from byte.property import Property
from tests.base.models.dynamic.artist import Artist


class Album(Model):
    class Options:
        slots = True

    id = Property(int, primary_key=True)
    artist = Property(Artist)

    title = Property(str)
