from __future__ import absolute_import, division, print_function

from byte.model import Model
from byte.property import Property


class Artist(Model):
    class Options:
        slots = True

    id = Property(int, primary_key=True)

    title = Property(str)
