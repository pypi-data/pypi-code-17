from pydelaunator import geometry


class Edge:
    __slots__ = ['_next_left_edge', '_origin_vertex', '_target_vertex',
                 '_left_face', '_opposite_edge', '_constrained']

    def __init__(self, origin_vertex, target_vertex, left_face=None,
                 next_left_edge=None, opposite_edge=None, constrained:bool=False):
        self._next_left_edge = next_left_edge
        self._origin_vertex = origin_vertex
        self._target_vertex = target_vertex
        self._left_face = left_face
        self._opposite_edge = opposite_edge
        self._constrained = bool(constrained)


    def nullify(self):
        """Remove all references to other objects. This is useful to ensure
        an error if this object is used after this call.
        """
        self._next_left_edge = None
        self._origin_vertex = None
        self._target_vertex = None
        self._left_face = None
        self._opposite_edge = None


    def squareDistanceTo(self, px, py) -> float:
        """Return square of distance between the edge and given coordinates."""
        return geometry.square_distance_between_segment_and_point(
            *self._origin_vertex.pos,
            *self._target_vertex.pos,
            px, py
        )

    def dot_product(self, pos) -> float:
        """Return dot product of given edge and point defined by given coordinates."""
        tx, ty = self._target_vertex.pos
        ox, oy = self._origin_vertex.pos
        px, py = pos
        return ((ty - oy) * (px - ox) + (ox - tx) * (py - oy))


    def coordOnTheRight(self, c) -> bool:
        """True if given coordinates are on the right of this Edge."""
        return self.dot_product(c) <= 0.
    def coordOnTheStrictRight(self, c) -> bool:
        """True if given coordinates are on the right of this Edge, but not on the Edge itself."""
        return self.dot_product(c) < 0.
    def coordOnTheLeft(self, c) -> bool:
        """True if given coordinates are on the left of this Edge."""
        return self.dot_product(c) >= 0.
    def coordOnTheStrictLeft(self, c) -> bool:
        """True if given coordinates are on the left of this Edge, but not on the Edge itself."""
        return self.dot_product(c) > 0.

    @property
    def origin_vertex(self):
        return self._origin_vertex
    @property
    def target_vertex(self):
        return self._target_vertex

    @property
    def next_left_edge(self):
        return self._next_left_edge
    @next_left_edge.setter
    def next_left_edge(self, next_left_edge):
        self._next_left_edge = next_left_edge
    @property
    def prev_left_edge(self):
        raise self._next_left_edge._next_left_edge

    @property
    def next_right_edge(self):
        return self.opposite_edge._next_left_edge._next_left_edge.opposite_edge
    @property
    def prev_right_edge(self):
        return self.opposite_edge._next_left_edge.opposite_edge

    @property
    def rot_right_edge(self):
        return self._opposite_edge._next_left_edge
    @property
    def rot_left_edge(self):
        return self._next_left_edge._next_left_edge.opposite_edge

    @property
    def left_face(self):
        return self._left_face
    @left_face.setter
    def left_face(self, left_face):
        self._left_face = left_face
    @property
    def right_face(self):
        return self.opposite_edge._left_face

    @property
    def opposite_edge(self):
        return self._opposite_edge
    @opposite_edge.setter
    def opposite_edge(self, opposite_edge):
        opposite_edge._opposite_edge = self
        self._opposite_edge = opposite_edge

    @property
    def constrained(self) -> bool:
        return self._constrained

    def __str__(self):
        return "EDGE{}({}->{})".format(('!' if self.constrained else ''),
                                       self.origin_vertex, self.target_vertex)
