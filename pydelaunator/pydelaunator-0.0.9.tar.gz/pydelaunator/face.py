

from pydelaunator import geometry


class Face:
    """Triangle in Mesh space, surrounded by there Edge and three Vertex."""
    __slots__ = ['_edge']

    def __init__(self, edge=None):
        self._edge = edge

    @property
    def edge(self):
        return self._edge
    @edge.setter
    def edge(self, edge):
        edge._left_face = self
        self._edge = edge

    @property
    def surrounding_edges(self) -> tuple:
        """Return the 3 edges that surround self"""
        ret = (
            self.edge,
            self.edge.next_left_edge,
            self.edge.next_left_edge.next_left_edge,
        )
        assert all(edge.left_face is self for edge in ret)
        return ret

    @property
    def surrounding_vertices(self) -> tuple:
        """Return the 3 vertices that surround self"""
        return tuple(edge.target_vertex for edge in self.surrounding_edges)


    def circumcircle_contain_position(self, position:tuple) -> bool:
        """True if given position is in the circumcircle of the triangle
        formed by the 3 vertices of this face.

        """
        return geometry.point_in_circumcircle_of(*self.surrounding_vertices, position)

    def __str__(self):
        return "FACE({}->{}->{})".format(self._edge.origin_vertex, self._edge.next_left_edge.origin_vertex, self._edge.next_left_edge.next_left_edge.origin_vertex)



class OutsideFace(Face):

    def circumcircle_contain_position(self, _) -> False:
        """An outside face never contains anything."""
        return False

    def __str__(self):
        return "FACE!({}->{}->{})".format(self._edge.origin_vertex, self._edge.next_left_edge.origin_vertex, self._edge.next_left_edge.next_left_edge.origin_vertex)
