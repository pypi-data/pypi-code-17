"""TODO DOCSTRING."""

import tiles


class Map(object):
    """A class representation of a map logic."""

    def __init__(self, size_x, size_y, size_z):
        """Construct a map of given sizes."""
        if not isinstance(size_x, int) or\
           not isinstance(size_y, int) or\
           not isinstance(size_z, int):
            raise TypeError('The map dimensions must be positive integers.')

        if size_x <= 0 or size_y <= 0 or size_z <= 0:
            raise AttributeError('The map dimensions must be POSITIVE ints.')

        self.dimensions = (size_x, size_y, size_z)
        self.tiles = []


class MapGenerators(object):
    """A set of methods for generating maps."""

    def flat_map(self, size_x, size_y, mode=0):
        """Generate a flat map."""
        tile = tiles.Tile(0, 0, 0)
        return [[tile for x in range(size_x)] for y in range(size_y)]
