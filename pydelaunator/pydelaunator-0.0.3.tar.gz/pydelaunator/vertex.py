

class Vertex:
    """Point in Mesh space, linked together by Edge instances"""
    __slots__ = ['_pos', '_edge', 'payload']

    def __init__(self, x, y, edge=None, payload=None):
        self._pos = x, y
        self._edge = edge
        self.payload = payload

    @property
    def direct_neighbors(self) -> iter:
        """Yield neighbors directly linked by an Edge"""
        yield from (edge.target_vertex for edge in self.outgoing_edges)
    @property
    def surrounding_faces(self) -> iter:
        """Yield Face with self as vertex"""
        yield from (edge.left_face for edge in self.outgoing_edges)
    @property
    def surrounding_edges(self) -> iter:
        """Yield edges that surround self (but do not collide with)"""
        yield from (edge.next_left_edge for edge in self.outgoing_edges)



    @property
    def pos(self):
        return tuple(self._pos)
    @property
    def position(self):
        return tuple(self._pos)
    @position.setter
    def position(self, new_pos:tuple):
        self._pos = None if new_pos is None else tuple(new_pos)
    @property
    def edge(self):
        return self._edge
    @edge.setter
    def edge(self, edge):
        self._edge = edge
        assert self._edge.origin_vertex == self

    @property
    def outgoing_edges(self):
        cur_edge = self._edge
        yield cur_edge
        cur_edge = cur_edge.rot_left_edge
        while cur_edge != self._edge:
            yield cur_edge
            cur_edge = cur_edge.rot_left_edge

    @property
    def x(self): return self.pos[0]
    @property
    def y(self): return self.pos[1]

    def __iter__(self):
        return iter(self._pos)

    def __str__(self):
        TRAD = {
            (0, 0): 'A',
            (100, 0): 'D',
            (0, 100): 'B',
            (100, 100): 'C',
        }
        return str(TRAD.get(self.pos, self.pos))
