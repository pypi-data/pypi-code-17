

from math import inf
from pydelaunator import navigation
from pydelaunator import Mesh, Vertex
from pydelaunator.commons import logger


class Placer:
    """High level interface for the Mesh class.

    End-user can be totally abstracted from the Mesh and Vertex concepts.

    """

    def __init__(self, width:int, height:int):
        self.mesh = Mesh(width, height)
        self._objects = {}  # client object: vertex in mesh

    def add(self, obj:object, x:int, y:int) -> object:
        assert obj not in self._objects
        if obj in self._objects:
            i, j = self._objects[obj]
            logger.warning("Placer can't add object '{}' because it is already "
                           "placed (at ({};{}). It will be moved instead."
                           "".format(obj, i, j))
            self.move(obj, x - i, y - j)
        else:  # object is new
            added = self.mesh.add(obj, x, y)
            self._objects[obj] = added
            return obj

    def move(self, obj:object, dx:int, dy:int):
        self.mesh.move(self._objects[obj], dx, dy)

    def nearests(self, obj:object) -> iter:
        """Yield the nearests objects."""
        vertices = navigation.nearests(self._objects[obj])
        yield from (vertex.payload for vertex in vertices
                    if vertex not in self.mesh.corners)

    def neighbors(self, obj:object, max_dist:float=inf, min_dist:float=0.) -> iter:
        vertices = navigation.neighbors(self._objects[obj], max_dist, min_dist)
        yield from (vertex.payload for vertex in vertices
                    if vertex not in self.mesh.corners)

    def __iter__(self) -> object:
        """Yield objects in mesh"""
        yield from self.mesh
