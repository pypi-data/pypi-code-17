from __future__ import absolute_import, division, print_function

from byte.model import Model
from byte.property import Property


class City(Model):
    id = Property(str, name='geonameid', primary_key=True)

    name = Property(str)

    country = Property(str)
    subcountry = Property(str)
