"""Definition of the Mesh object

"""

import math
import random
import itertools

from pydelaunator import geometry, commons
from pydelaunator import Vertex, Edge, Face
from pydelaunator.commons import logger


INTEGRITY_TESTS = True


class Mesh:
    """Representation of a trianguled 2D space where points are Vertex linked
    by Edge and filled between by Face.

    """
    __slots__ = ['width', 'height', '_outside_objects', '_corners', '_vertices',
                 '_edges', '_root_vertex']


    def __init__(self, width:int, height:int):
        self.width, self.height = width, height
        self._outside_objects = frozenset()
        self._corners = frozenset()
        self._root_vertex = None  # vertex linked to all corners.
        self._vertices = set()
        self._edges = set()

        self._init_space()
        self._integrity_tests()

    def collide_at(self, x, y) -> bool:
        """True if given position is valid"""
        return 0 <= x <= self.width and 0 <= y <= self.height

    def corrected_position(self, x, y) -> tuple:
        """Return given position if is valid, else another one which is"""
        i = max(0+1, min(x, self.width-1))
        j = max(0+1, min(y, self.height-1))
        logger.info("Position ({};{}) corrected to ({};{}).".format(x, y, i, j))
        return i, j

    def _init_space(self):
        # create the four corners and the root vertex
        a, b, d, c = Vertex(0, 0), Vertex(self.width, 0), Vertex(0, self.height), Vertex(self.width, self.height)
        self._corners = frozenset((a, b, c, d))
        self._vertices = set(self.corners)
        r = self._root_vertex = Vertex(math.nan, math.nan)
        edges = dict()

        outside_triangles = {(r, d, a), (r, a, b), (r, b, c), (r, c, d)}
        triangles = {(b, a, d), (d, c, b), *outside_triangles}

        # Create the two internal triangles and the four outsiders
        from pydelaunator.face import OutsideFace
        for vertices in triangles:
            vone, vtwo, vtee = vertices
            face_builder = OutsideFace if vertices in outside_triangles else Face
            assert isinstance(vone, Vertex)
            assert isinstance(vtwo, Vertex)
            assert isinstance(vtee, Vertex)
            pone, ptwo, ptee = (vone, vtwo), (vtwo, vtee), (vtee, vone)
            one = edges[pone] = Edge(*pone, constrained=True)
            two = edges[ptwo] = Edge(*ptwo, constrained=True)
            tee = edges[ptee] = Edge(*ptee, constrained=True)
            one.next_left_edge = two
            two.next_left_edge = tee
            tee.next_left_edge = one
            one.left_face = two.left_face = tee.left_face = face_builder(one)
            assert one.left_face is two.left_face
            assert two.left_face is tee.left_face

        # Remove constrains on BD and DB
        edges[b, d].constrained = False
        edges[d, b].constrained = False

        # Set oppositions
        for one, eone in edges.items():
            for two, etwo in edges.items():
                if two == tuple(reversed(one)):
                    eone.opposite_edge = etwo

        # Merge Edge and Vertex Models
        a.edge = edges[a, b]
        b.edge = edges[b, c]
        c.edge = edges[c, d]
        d.edge = edges[d, a]
        r.edge = edges[r, a]

        self._outside_objects = frozenset((
            edges[r, a], edges[a, r], edges[r, a].left_face,
            edges[r, b], edges[b, r], edges[r, b].left_face,
            edges[r, c], edges[c, r], edges[r, c].left_face,
            edges[r, d], edges[d, r], edges[r, d].left_face,
            self._root_vertex
        ))

        # Verifications
        assert edges[b, d].rot_right_edge == edges[b, a]
        assert edges[b, d].rot_left_edge == edges[b, c]
        assert edges[b, d].left_face == edges[d, b].right_face
        print(tuple((edge.left_face for edge in edges.values())))
        assert 6 == len(set(edge.left_face for edge in edges.values()))  # exactly 6 faces in whole structure
        # Keep track of all edges, except the ones related to vertex root.
        self._edges = set(edges.values()) - self._outside_objects
        logger.info("Mesh initiated.")


    def _integrity_tests(self, aggressive=True):
        """Raise AssertionError on any inconsistency in the graph"""
        if not INTEGRITY_TESTS:  return

        # count number of constrained edges between corners
        nb_constrained = sum(1 for edge in self._edges if
                             edge.origin_vertex in self._corners and
                             edge.target_vertex in self._corners and
                             edge.constrained)
        assert nb_constrained == 8

        if len(self._vertices) == len(self._corners) and True:
            for corner in self._corners:
                found = frozenset(corner.direct_neighbors)
                assert len(found) >= 2, (
                    "EC2: Corner vertex {} is not linked to at least 2 others."
                    " The following {} are linked: {}"
                    "".format(corner, len(found), found)
                )

        for edge in self.edges:
            opps = edge.opposite_edge
            # print('\nFKCTZV:')
            # print('E,O:', edge, opps)
            # print('N  :', edge.next_left_edge)
            # print('NN :', edge.next_left_edge.next_left_edge)
            # print('NNN:', edge.next_left_edge.next_left_edge.next_left_edge)
            assert edge is not edge.next_left_edge
            assert edge.opposite_edge is not edge.next_left_edge
            assert edge.next_left_edge.next_left_edge.next_left_edge == edge
            assert opps.next_left_edge.next_left_edge.next_left_edge == opps
            assert edge.next_right_edge.next_right_edge.next_right_edge == edge
            face = edge.left_face
            assert face == edge.next_left_edge.left_face
            assert face == edge.next_left_edge.next_left_edge.left_face

        for vertex in self.vertices:
            assert vertex.edge is not None, ("EV0: Vertex {} does not references"
                                             "any edge.".format(vertex))
            out_edge = tuple(vertex.outgoing_edges)
            dir_neis = tuple(vertex.direct_neighbors)
            assert len(out_edge) == len(set(out_edge)), (
                "EV11: Vertex {} referencies the same edge multiple times in {}"
                .format(vertex, ';'.join(map(str, out_edge)))
            )
            assert len(dir_neis) == len(set(dir_neis)), (
                "EV12: Vertex {} referencies the same neighbor multiple times in {}"
                "".format(vertex, ';'.join(map(str, dir_neis)))
            )
            assert len(out_edge) == len(dir_neis), (
                "EV21: Number of outgoing edge ({}) is not the same as direct neighbors ({})."
                "".format(len(out_edge), len(dir_neis))
            )
            assert len(set(out_edge)) == len(set(dir_neis)), (
                "EV22: Number of unique outgoing edge ({}) is not the same as "
                "unique direct neighbors ({})."
                "".format(len(set(out_edge)), len(set(dir_neis)))
            )
            assert len(set(dir_neis)) > 2, (
                "EV3: Vertex {} have not enough neighbors ({}, minimum is 3)"
                "".format(vertex, len(dir_neis))
            )
            assert vertex.edge.origin_vertex == vertex, (
                "EV4: Vertex {} references edge {} that has vertex {} as origin."
                "".format(vertex, vertex.edge, vertex.edge.origin_vertex)
            )
            if vertex not in self._corners:
                for edge in vertex.surrounding_edges:
                    args = *vertex, *edge.origin_vertex, *edge.target_vertex
                    assert not geometry.point_collide_segment(*args), (
                        "EV5: Vertex {} collides with its surrounding edge {}. "
                        "geometry.point_collide_segment({}) returned True"
                        "".format(vertex, edge, ', '.join(map(str, args)))
                    )

        if not aggressive:
            logger.info("Mesh integrity test ran with success.")
            return  # do not performe the costly treatments that follow

        # Build intermediary data structure
        #  it will allow more powerful integrity_tests
        edge_map = {}  # {position origin, position target: edge}
        for edge in self.edges:
            ori, tar = edge.origin_vertex.pos, edge.target_vertex.pos
            assert (ori, tar) not in edge_map, (
                "EE1: Edge {} linking vertices {} and {} is not the first"
                " to do so. Edge {} is already doing that."
                "".format(edge, edge.origin_vertex, edge.target_vertex, edge_map[ori, tar])
            )
            edge_map[ori, tar] = edge

        # edge_map = {}  # {position origin, position target: edge}
        # for edge in self.edges:
            # print()
            # ori, tar = edge.origin_vertex.pos, edge.target_vertex.pos
            # if (ori, tar) not in edge_map:
                # edge_map[ori, tar] = edge
            # else:
                # print('NTNEWN:', ori, tar, str(edge))
                # print("There is multiple {}->{} edges.".format(ori, tar))
                # edge_map[ori, tar] = (edge_map[ori, tar], edge)
        # from pprint import pprint
        # pprint({k: str(v) for k, v in edge_map.items()})
        # return  # next tests are not yet opened to public ; needs a proper edge_map (only one edge by node combination)
        for ori in self.vertices:
            ori = ori.pos
            for tar in self.vertices:
                tar = tar.pos
                if (ori, tar) in edge_map:
                    assert (tar, ori) in edge_map
                    one, two = edge_map[ori, tar], edge_map[tar, ori]
                    assert one.opposite_edge == two
        logger.info("Mesh aggressive integrity test ran with success.")


    def add(self, obj:object or Vertex, x:int, y:int, search_start:Edge=None):
        """Add given object at given position.

        obj -- the object to associate with the given position
        x, y -- position of the object in the mesh
        search_start -- optional edge in the mesh to use as start point

        If obj is a Vertex instance, it will use it instead of
        creating a new Vertex.
        This parameter is used in very particular cases, like `Mesh.move`.

        Raise a ValueError if given position is already dominated by an existing
        vertice.

        """
        x, y = self.corrected_position(x, y)
        obj = obj if isinstance(obj, Vertex) else Vertex(x, y, payload=obj)
        obj.position = (x, y)
        assert isinstance(obj, Vertex)
        logger.info("Mesh will add a new Vertex at ({};{}) containing {}.".format(x, y, obj.payload))

        face_or_edge_or_vertex = self.object_covering(x, y, starting_edge=search_start)
        if isinstance(face_or_edge_or_vertex, Face):
            logger.info("({};{}) is on face {}.".format(x, y, face_or_edge_or_vertex))
            face = face_or_edge_or_vertex
            # A B and C are the three surrounding vertices.
            # I is the one to be added.
            ba = face.edge
            ac = ba.next_left_edge
            cb = ba.next_left_edge.next_left_edge
            # get the three surrounding points
            a = ba.target_vertex
            b = cb.target_vertex
            c = ac.target_vertex
            # get the 6 new edges
            ai, bi, ci = Edge(a, obj), Edge(b, obj), Edge(c, obj)
            ia, ib, ic = Edge(obj, a), Edge(obj, b), Edge(obj, c)
            ai.next_left_edge, ib.next_left_edge, ba.next_left_edge = ib, ba, ai
            ia.next_left_edge, ac.next_left_edge, ci.next_left_edge = ac, ci, ia
            ic.next_left_edge, cb.next_left_edge, bi.next_left_edge = cb, bi, ic
            ai.opposite_edge = ia
            bi.opposite_edge = ib
            ci.opposite_edge = ic
            # Create the two new faces
            ac.left_face = ci.left_face = ia.left_face = Face(ac)
            cb.left_face = bi.left_face = ic.left_face = Face(cb)
            ai.left_face = ib.left_face = ba.left_face
            self._edges |= {ic, ci, ia, ai, ib, bi}
            # Manage the new vertex
            obj.edge = ia
            self._vertices.add(obj)
            self._apply_delaunay_condition(ac.left_face)
            self._apply_delaunay_condition(cb.left_face)
            self._apply_delaunay_condition(ai.left_face)

        elif isinstance(face_or_edge_or_vertex, Edge):
            logger.info("({};{}) is on edge {}.".format(x, y, face_or_edge_or_vertex))
            # A B C and D are the four surrounding vertices.
            # I is the one to be added.
            ca = face_or_edge_or_vertex
            ac = ca.opposite_edge
            ab = ca.next_left_edge
            bc = ca.next_left_edge.next_left_edge
            cd = ac.next_left_edge
            da = cd.next_left_edge
            assert bc.next_left_edge == ca

            # get the four surrounding points
            a = ca.target_vertex
            b = ab.target_vertex
            c = bc.target_vertex
            d = cd.target_vertex
            assert a == ab.origin_vertex
            assert b == bc.origin_vertex
            assert c == cd.origin_vertex
            assert d == da.origin_vertex

            # modify the AC and CA edges to become the AI and CI edges.
            ai, ia = ac, ca
            del ac, ca
            ai.origin_vertex, ai.target_vertex = a, obj
            ia.origin_vertex, ia.target_vertex = obj, a
            # get the 8 new edges
            bi, ci, di = Edge(b, obj), Edge(c, obj), Edge(d, obj)
            ib, ic, id = Edge(obj, b), Edge(obj, c), Edge(obj, d)
            self._edges |= {ic, ci, ib, bi, id, di}
            assert ai in self._edges
            assert ia in self._edges

            ai.opposite_edge = ia
            bi.opposite_edge = ib
            ci.opposite_edge = ic
            di.opposite_edge = id

            # form the four triangles
            triangles = (
                (id, da, ai),
                (ia, ab, bi),
                (ib, bc, ci),
                (ic, cd, di),
            )
            for one, two, tee in triangles:
                one.next_left_edge, two.next_left_edge, tee.next_left_edge = two, tee, one
                one.left_face = two.left_face = tee.left_face = Face(one)

            # Manage the new vertex
            obj.edge = ia
            self._vertices.add(obj)
            self._apply_delaunay_condition(ab.left_face)
            # self._apply_delaunay_condition(bc.left_face)
            self._apply_delaunay_condition(cd.left_face)
            # self._apply_delaunay_condition(da.left_face)

        elif isinstance(face_or_edge_or_vertex, Vertex):
            logger.info("({};{}) is on vertex {}.".format(x, y, face_or_edge_or_vertex))
            vertex = face_or_edge_or_vertex
            raise ValueError("Can't add a vertex on a vertex.")
        else:
            raise TypeError("Mesh.object_covering returned an unexpected value"
                            " {}.".format(face_or_edge_or_vertex))
        self._integrity_tests(aggressive=True)
        logger.info("Object {} added with success.".format(obj))
        return obj


    def object_covering(self, x, y, starting_edge:Edge=None) -> Face or Edge or Vertex:
        """Return the object describing the best given position.

        If position is one of a vertex, the vertex is returned.
        If position is on an edge, the edge is returned.
        Else, position is expected to be on a face, which is returned.

        starting_edge -- optional edge to use as starting point for the search

        Delaunator: Triangulation::findContainerOf
        https://github.com/Aluriak/Delaunator/blob/master/delaunator/libdelaunator_src/triangulation.cpp#L905

        """
        assert self.collide_at(x, y)
        logger.info("Search for cover of ({};{}).".format(x, y))
        counter_left = 0  # when hit 3, it's because we are turning around it
        current_edge = starting_edge or random.choice(tuple(self.edges))
        while current_edge in self.outside_objects:
            current_edge = random.choice(tuple(self.edges))
        # current_edge = next(iter(self.edges))  # could probably be choosen more efficiently
        logger.info("Starting edge : {}.".format(current_edge))
        target = x, y


        def non_outside(edge, access='rot_left_edge'):
            """Avoid using an outside object"""
            while edge in self.outside_objects:
                edge = getattr(edge, access)
            return edge

        while True:
            # print()
            assert current_edge not in self.outside_objects
            if current_edge.coordOnTheLeft(target):
                # print(*target, *current_edge.origin_vertex.pos, *current_edge.target_vertex.pos)
                if geometry.point_collide_segment(*target, *current_edge.origin_vertex.pos, *current_edge.target_vertex.pos):
                    if geometry.point_collide_point(*target, *current_edge.origin_vertex.pos):
                        return current_edge.origin_vertex
                    if geometry.point_collide_point(*target, *current_edge.target_vertex.pos):
                        return current_edge.target_vertex
                    return current_edge
                counter_left += 1
                # churn until be on the left of target,
                current_edge = current_edge.rot_left_edge
                while current_edge.coordOnTheStrictLeft(target):
                    current_edge = non_outside(current_edge.rot_left_edge)
                # Churn to right for keep target to the left.
                current_edge = non_outside(current_edge.rot_right_edge, 'rot_right_edge')
            else:  # target is on the right
                counter_left = 0
                while current_edge.coordOnTheStrictRight(target) and current_edge not in self.outside_objects:
                    current_edge = non_outside(current_edge.rot_right_edge, 'rot_right_edge')
                # Churn to left for keep target to the left.
                current_edge = non_outside(current_edge.rot_left_edge)

            current_edge = non_outside(current_edge.next_left_edge)
            if counter_left >= 3:  # we are turning around it
                return current_edge.left_face


    def vertices_at(self, position:tuple, max_square_dist:float) -> iter:
        """Yield vertices with position in given range"""
        for vertex in self.vertices:
            dist = geometry.square_distance_between_points(*position, *vertex.position)
            if dist <= max_square_dist:
                yield vertex


    def _apply_delaunay_condition(self, face:Face, *, processed:set=None) -> set:
        """Modify self internals to respect the delaunay condition.

        Return all the faces that have been treated.
        Delaunator: Triangulation::applyDelaunayCondition

        """
        assert face is not None and face.edge is not None
        processed = processed or set()
        if face in processed or face in self.outside_objects:
            processed.add(face)
            return processed
        processed.add(face)
        # INITIALIZATION
        illegal_edge = None;  # illegal edge that relie the illegal vertex and the face's vertex.
        # to restore the delaunay condition, flip the illegal edge
        logger.info("Delaunay condition will be apply on {}.".format(face))

        # CONDITION: we care
        if face in self.outside_objects:
            return processed
        # Get a neighbor that breaks the delaunay condition
        for edge in face.surrounding_edges:
            if edge.constrained:  continue
            if face.circumcircle_contain_position(edge.next_right_edge.target_vertex):
                illegal_edge = edge
                break
        else:  # no illegal edge found
            return processed

        # MODIFICATION OF FACES
        # restore delaunay condition and verify those that are around
        self._flip_edge(illegal_edge)
        processed |= self._apply_delaunay_condition(illegal_edge.right_face,
                                                    processed=processed)
        processed |= self._apply_delaunay_condition(illegal_edge.left_face,
                                                    processed=processed)
        return processed


    def _flip_edge(self, illegal_edge1) -> bool:
        """Flip given edge inside its two triangles structure.

        Return True if flipping has been performed.

        Delaunator: Triangulation::operateFlip

        """
        if illegal_edge1 in self.outside_objects:
            print('EVQWSD: TRIED TO FLIP AN OUTSIDE EDGE — abort !')
            input('<ok>')
            return False
        if illegal_edge1.constrained:
            assert not illegal_edge1.opposite_edge.constrained
            assert illegal_edge1.opposite_edge.constrained
            logger.info("Constraigned Edge {} was not flipped.".format(illegal_edge1))
            return False
        assert illegal_edge1 not in self.outside_objects
        # SHORTCUTS
        illegal_edge2 = illegal_edge1.opposite_edge
        illegal_vertex1 = illegal_edge1.next_left_edge.target_vertex
        illegal_vertex2 = illegal_edge2.next_left_edge.target_vertex
        face1 = illegal_edge1.left_face
        face2 = illegal_edge2.left_face
        # Previous and next edge in the cycle that form the faces.
        edge1_prev = illegal_edge1.next_left_edge
        edge1_next = illegal_edge1.next_right_edge.opposite_edge
        edge2_prev = illegal_edge2.next_left_edge
        edge2_next = illegal_edge2.next_right_edge.opposite_edge


        # TESTS
        assert illegal_edge2.opposite_edge == illegal_edge1
        assert illegal_vertex2 == illegal_edge1.next_right_edge.target_vertex
        assert illegal_edge1.left_face == illegal_edge2.right_face
        assert illegal_edge2.left_face == illegal_edge1.right_face
        assert face1 == illegal_edge2.right_face
        assert face2 == illegal_edge1.right_face
        assert edge1_prev.next_left_edge == edge2_next
        assert edge2_prev.next_left_edge == edge1_next
        assert edge1_next.target_vertex == illegal_edge1.target_vertex
        assert edge2_next.target_vertex == illegal_edge2.target_vertex
        assert illegal_edge1.origin_vertex != illegal_vertex1
        assert illegal_edge2.origin_vertex != illegal_vertex1
        assert illegal_edge1.origin_vertex != illegal_vertex2
        assert illegal_edge2.origin_vertex != illegal_vertex2

        # MODIFICATIONS
        # Origin vertex of illegal edges can't reference illegal edges anymore
        illegal_edge1.origin_vertex.edge = edge2_prev
        illegal_edge2.origin_vertex.edge = edge1_prev

        # Modify next left and right edges of non-illegal edges
        edge1_prev.next_left_edge = illegal_edge1
        edge2_prev.next_left_edge = illegal_edge2

        edge1_next.next_left_edge = edge1_prev
        edge2_next.next_left_edge = edge2_prev

        illegal_edge1.next_left_edge = edge1_next  # Close the cycle
        illegal_edge2.next_left_edge = edge2_next

        # assign origin vertex
        illegal_edge1._origin_vertex = illegal_vertex1
        illegal_edge1._target_vertex = illegal_vertex2
        illegal_edge2._origin_vertex = illegal_vertex2
        illegal_edge2._target_vertex = illegal_vertex1

        # update faces
        face1.edge = illegal_edge1
        edge1_next.left_face = face1
        edge1_prev.left_face = face1
        face2.edge = illegal_edge2
        edge2_next.left_face = face2
        edge2_prev.left_face = face2

        # TESTS
        assert illegal_edge1.origin_vertex is illegal_vertex1
        assert illegal_edge1.origin_vertex.edge.origin_vertex is illegal_edge1.origin_vertex
        assert illegal_edge1.next_left_edge is illegal_edge2.next_right_edge.next_right_edge.opposite_edge
        assert illegal_edge1.next_left_edge.next_left_edge.next_left_edge is illegal_edge1
        assert illegal_edge1.left_face is face1
        assert illegal_edge1.next_left_edge.left_face is face1
        assert illegal_edge1.next_left_edge.next_left_edge.left_face is face1

        assert illegal_edge2.target_vertex is illegal_vertex1
        assert illegal_edge2.next_left_edge.next_left_edge.next_left_edge is illegal_edge2
        assert illegal_edge2.left_face is face2
        assert illegal_edge2.next_left_edge.left_face is face2
        assert illegal_edge2.next_left_edge.next_left_edge.left_face is face2
        logger.info("Edge {} was flipped. Run integrity tests.".format(str(illegal_edge1)))
        self._integrity_tests()
        return True



    @property
    def edges(self) -> frozenset:  return frozenset(self._edges)
    @property
    def corners(self) -> frozenset:  return frozenset(self._corners)
    @property
    def vertices(self) -> frozenset:  return frozenset(self._vertices)
    @property
    def outside_objects(self) -> frozenset:  return frozenset(self._outside_objects)

    def __iter__(self) -> iter:
        return iter(self.vertices)

    def print(self, do_layout:bool=True) -> object:
        edges = []
        for edge in self.edges:
            if edge in self.outside_objects:  continue
            o = str(edge.origin_vertex.position)
            t = str(edge.target_vertex.position)
            edges.append((o, t))
        if do_layout:
            layout = {str(vertex.pos): vertex.pos for vertex in self.vertices}
        else:
            layout = None
        commons.draw_digraph(edges, layout)


    def remove(self, del_vertex:Vertex) -> object:
        """Return the payload of the given vertex, once it has been removed
        from graph.

        Raise a ValueError if given vertex is not in the graph.

        """
        if del_vertex not in self.vertices:
            raise ValueError("Given vertex '{}' is not in this graph.".format(del_vertex))
        if del_vertex in self.corners:
            raise ValueError("Given vertex is one of the corners.".format(del_vertex))
        # Creat some container
        modified_faces = set()  # faces that can break Delaunay condition
        assert del_vertex.edge
        assert self.collide_at(*del_vertex.position)
        logger.info("Mesh will remove {} ({} neighbors).".format(del_vertex, len(tuple(del_vertex.direct_neighbors))))

        # Collect references to neighbors (both edge and vertex)

    # SIMPLIFY LOCAL TRIANGULATION
        # Recipes for 3 and 4 neighbors are not the general cases, but all
        #  the others (5 or more) can be modified to a non-delaunay triangulation
        #  where del_vrtx reach exactly 3 or 4 neighbors.
        # Applying this modification, delaunay condition is broken,
        #  so we need to track the faces to verify after the removal. (modified_faces)
        nei_edge = tuple(del_vertex.outgoing_edges)
        while len(nei_edge) > 4:
            logger.info("Vertex {} expose the following {} neighbors: {}."
                        "".format(del_vertex, len(nei_edge),
                                  ', '.join(map(str, del_vertex.direct_neighbors))))
            # For each triplet of neighbor, try to lost the middle one
            for eone, etwo, etee in commons.sliding(itertools.cycle(tuple(nei_edge)), size=3):
                if etwo.constrained:  continue  # this one can't be flipped
                one, two, tee = eone.target_vertex, etwo.target_vertex, etee.target_vertex
                if geometry.segment_crosses_segment(one.pos, tee.pos, del_vertex.pos, two.pos):
                    # del_vertex will lose neighbor two if we flip etwo.
                    if not self._flip_edge(etwo):
                        logger.warning("Edge {} should have been flipped, "
                                       "but didn't. That's weird.".format(etwo))
                    modified_faces |= {etwo.left_face, etwo.right_face}
                    # update the sets of neighbors
                    nei_edge = tuple(del_vertex.outgoing_edges)
                    logger.info("Mesh discards vertex {} by flipping edge {} ({} neighbors).".format(two, etwo, len(nei_edge)))
                    break
        assert len(nei_edge) in {3, 4}


    # DELETE POINT FROM TRIANGLE CONTAINER
        logger.info("Mesh start removing {} ({} neighbors).".format(del_vertex, len(nei_edge)))
        if len(nei_edge) == 3:
            # edges to delete
            ia = del_vertex.edge
            ib = ia.rot_right_edge
            ic = ib.rot_right_edge
            assert ia.rot_left_edge is ic
            ai, bi, ci = ia.opposite_edge, ib.opposite_edge, ic.opposite_edge

            # edges to modify
            ac = ia.next_left_edge
            cb = ic.next_left_edge
            ba = ib.next_left_edge

            # 2 faces must be deleted, f1 remain
            f1, f2, f3 = ia.left_face, ib.left_face, ic.left_face
            modified_faces.add(f1)
            modified_faces -= {f2, f3}

            assert len(set((ia, ib, ic))) == 3  # uniques
            assert len(set((f1, f2, f3))) == 3  # uniques
            assert len(set((ia.target_vertex, ib.target_vertex, ic.target_vertex))) == 3 # uniques

            # update the vertices
            ia.target_vertex.edge = ac
            ib.target_vertex.edge = ba
            ic.target_vertex.edge = cb

            # update the triangle
            ac.next_left_edge = cb
            cb.next_left_edge = ba
            ba.next_left_edge = ac
            ac.left_face, cb.left_face, ba.left_face = [f1] * 3

            # delete the edges, update the Mesh
            todel = {ia, ib, ic, ai, bi, ci}
            logger.info("Edges {} are removed and nullified.".format(';'.join(map(str, todel))))
            self._edges -= todel
            assert all(not e.constrained for e in todel)
            map(Edge.nullify, todel)
            self._vertices.remove(del_vertex)


    # DELETE POINT FROM SQUARE CONTAINER
        elif len(nei_edge) == 4:
            # edges to be deleted
            ia = del_vertex.edge
            ib = ia.rot_right_edge
            ic = ib.rot_right_edge
            id = ia.rot_left_edge
            # and their opposite
            ai = ia.opposite_edge
            bi = ib.opposite_edge
            ci = ic.opposite_edge
            di = id.opposite_edge

            # faces to delete
            f1, f2 = ia.left_face, ia.right_face
            modified_faces -= {f1, f2}
            # faces to keep
            f3, f4 = ic.left_face, ic.right_face
            modified_faces |= {f3, f4}

            # edges to modify
            ad = ia.next_left_edge
            dc = id.next_left_edge
            cb = ic.next_left_edge
            ba = ib.next_left_edge

            a = ia.target_vertex
            b = ib.target_vertex
            c = ic.target_vertex
            d = id.target_vertex

            # tests
            assert a is not del_vertex
            assert b is not del_vertex
            assert c is not del_vertex
            assert d is not del_vertex
            assert f1 is id.right_face
            assert f2 is ib.left_face
            assert f3 is bi.left_face
            assert f4 is ci.left_face
            assert ic is id.rot_left_edge
            assert cb.next_left_edge is bi
            assert ba.next_left_edge is ai
            assert ib.next_left_edge is ba

            # update vertices
            for vx, e in zip((a, b, c, d), (ad, ba, cb, dc)):
                assert e.origin_vertex == vx
                vx.edge = e

            # update CI => CA and IC => AC
            ca, ac = ci, ic
            ca._target_vertex, ac._target_vertex = a, c
            ca._origin_vertex, ac._origin_vertex = c, a
            ca.next_left_edge, ac.next_left_edge = ad, cb
            del ci, ic

            # set triangles
            triangles = ((ca, ad, dc, f3), (ac, cb, ba, f4))
            for one, two, tee, face in triangles:
                one.next_left_edge = two
                two.next_left_edge = tee
                tee.next_left_edge = one
                one.left_face = face
                two.left_face = face
                tee.left_face = face
                face.edge = one

            # update the Mesh itself
            todel = {ia, ai, ib, bi, id, di}
            self._edges -= todel
            assert all(not e.constrained for e in todel)
            map(Edge.nullify, todel)
            self._vertices.remove(del_vertex)

    # RESTORE DELAUNAY CONDITION
        # Delaunay condition was break. It's time to restore it.
        logger.info("Mesh will restaure the delaunay condition for {} candidate faces.".format(len(modified_faces)))
        for face in modified_faces:
            self._apply_delaunay_condition(face)
        self._integrity_tests(aggressive=True)
        return del_vertex.payload


    def move(self, mov_vertex, dx, dy):
        """Move given given vertex in graph of given delta position.

        Raise a ValueError if given vertex is not in the graph.

        """
        if mov_vertex not in self.vertices:
            raise ValueError("Given vertex '{}' is not in this graph.".format(mov_vertex))
        if mov_vertex in self.corners:
            raise ValueError("Given vertex is one of the corners.".format(mov_vertex))

        target = self.corrected_position(mov_vertex.pos[0] + dx,
                                         mov_vertex.pos[1] + dy)
        logger.info("Mesh will move Vertex {} to position ({},{}).".format(mov_vertex, *target))
        # search for problems
        for edge in mov_vertex.surrounding_edges:
            right_vertex = edge.origin_vertex
            left_vertex = edge.target_vertex
            assert right_vertex is not left_vertex
            assert mov_vertex is not right_vertex
            assert mov_vertex is not left_vertex
            if geometry.segment_collides_segment(mov_vertex, target, left_vertex, right_vertex):
                # collision with neighbors highly probable : delete and add the vertice
                logger.info("Mesh will delete Vertex {} and add it to target "
                            "position, because segment vertex/target [{} {}] "
                            "collides with segment of neighbors [{} {}] (edge {})."
                            "".format(mov_vertex, mov_vertex, target,
                                      left_vertex, right_vertex, edge))
                # search for new emplacement by beginning around the old position
                starting_point = mov_vertex.edge.next_left_edge
                self.remove(mov_vertex)
                mov_vertex.edge = None
                mov_vertex.position = None
                self.add(mov_vertex, *target, search_start=starting_point)
                assert mov_vertex.edge
                break
        else:  # no collision with neighbors
            logger.info("Mesh will change Vertex {} position".format(mov_vertex))
            mov_vertex.position = target
            faces = set()
            for face in tuple(mov_vertex.surrounding_faces):
                faces |= self._apply_delaunay_condition(face, processed=faces)
            assert mov_vertex.edge
            self._integrity_tests()
        logger.info("Vertex {} is now at position ({};{})".format(mov_vertex, *target))


    def term_print(self):
        """DEBUG"""
        print('\n######################################################')
        print('VERTICES:')
        for v in self.vertices:
            print('\t', v, v.edge, v.edge.next_left_edge)
            if v.edge:
                print('\t\t', *tuple(map(str, v.surrounding_faces)))
        print('EDGES:')
        for e in self.edges:
            print(e, e.next_left_edge, e.left_face)
        print('######################################################\n')


    def do_thing(self):
        """DEBUG"""
        edge_map = {}
        for edge in self.edges:
            # print()
            ori, tar = edge.origin_vertex, edge.target_vertex
            # print(ori, tar, str(edge))
            # assert (ori.pos, tar.pos) not in edge_map
            if (ori.pos, tar.pos) not in edge_map:
                edge_map[ori.pos, tar.pos] = edge
            else:
                print("There is multiple {}->{} edges.".format(ori, tar))
                edge_map[ori.pos, tar.pos] = (edge_map[ori.pos, tar.pos], edge)
        return edge_map


if __name__ == "__main__":
    mesh = Mesh(100, 100)
    mesh.print()
    mesh.add('Michel', 40, 40)
    mesh.print()
    print(mesh.do_thing())
    mesh.print()
    mesh.add('Gérard', 80, 10)
    mesh.print()
    mesh.add('Micheline', 40, 60)
    mesh.print()
