

import itertools
import pytest
from pydelaunator import Mesh, Edge, Face, Vertex


@pytest.fixture
def mesh():
    return Mesh(100, 100)


def test_object_corvering(mesh):
    face = mesh.object_covering(10, 10)
    assert isinstance(face, Face)

    edge = mesh.object_covering(50, 50)
    assert isinstance(edge, Edge)

    vrtx = mesh.object_covering(0, 0)
    assert isinstance(vrtx, Vertex)


def test_mesh_dim(mesh):
    assert mesh.corrected_position(0, 100) == (1, 99)
    assert mesh.corrected_position(50, 50) == (50, 50)

def test_mesh_add(mesh):
    mesh.add('one', 10, 10)
    with pytest.raises(ValueError):
        mesh.add('another at the same place', 10, 10)


def test_mesh(mesh):
    assert len(mesh.edges) == 10
    assert len(mesh.corners) == 4
    assert len(mesh.vertices) == 0
    assert set(mesh) == mesh.vertices
    added = mesh.add('object', 50, 50)
    assert mesh.vertices != mesh.corners
    assert len(mesh.edges) == 16
    assert len(mesh.corners) == 4
    assert len(mesh.vertices) == 1
    assert set(mesh) == mesh.vertices
    assert added in mesh.vertices
    assert added not in mesh.corners
    added = mesh.remove(added)
    assert len(mesh.edges) == 10
    assert len(mesh.corners) == 4
    assert len(mesh.vertices) == 0
    assert set(mesh) == mesh.vertices


def test_remove():
    # reproduction of a weird case encountered while playing
    mesh = Mesh(600, 600)
    points = (75, 381), (133, 192), (320, 107), (503, 488), (528, 209), (465, 325)
    for point in points:
        mesh.add(str(point), *point)
    todel = (251, 574)
    vertex = mesh.add(str(todel), *todel)
    mesh.move(vertex, 271, 540)  # just change the position
    mesh.move(vertex, 271, 539)  # delete and replace it


def test_neighbors(mesh):
    for vertex in mesh.vertices:
        nb_nei = len(tuple(vertex.direct_neighbors))
        assert nb_nei in {3, 4}
        assert nb_nei == len(set(vertex.direct_neighbors))


def test_neighbors_more(mesh):
    added_vertex = mesh.add('object', 50, 50)
    assert len(tuple(added_vertex.direct_neighbors)) == 4
    for vertex in mesh.vertices:
        nb_nei = len(tuple(vertex.direct_neighbors))
        assert nb_nei in {3, 4}
        assert nb_nei == len(set(vertex.direct_neighbors))


@pytest.fixture
def buggy_mesh_1():
    dt = Mesh(600, 600)
    uid = itertools.count()
    moving_one = dt.add(next(uid), 536, 206)
    dt.add(next(uid), 528, 209)
    dt.add(next(uid), 465, 325)
    dt.add(next(uid), 503, 488)  # commented: bug1 var 1 raises errors
    return dt, moving_one


def test_bug_1(buggy_mesh_1):
    # living bug that needs to be fixed
    dt, tgt = buggy_mesh_1
    dt.move(tgt, -4, 0)
    with pytest.raises(AssertionError) as excinfo:
        dt.move(tgt, -2, -1)
    # thing is: this is the one or the other, probably depending of which vertex
    #  is tested first.
    assert str(excinfo.value).startswith(('EV12', 'EV21', 'EV3'))

def test_bug_1_variation_1(buggy_mesh_1):
    # in this case, there is no problem
    dt, tgt = buggy_mesh_1
    dt.move(tgt, -5, 0)
    dt.move(tgt, -1, -1)

def test_bug_1_variation_2(buggy_mesh_1):
    dt, tgt = buggy_mesh_1
    with pytest.raises(AssertionError) as excinfo:
        dt.move(tgt, -6, -1)
    # thing is: this is the one or the other, probably depending of which vertex
    #  is tested first.
    assert str(excinfo.value).startswith(('EV12', 'EV21', 'EV3'))


def test_bug_2(buggy_mesh_1):
    # this is basically a proof that removing is not working properly
    dt = Mesh(600, 600)
    added = [
        dt.add('point', 75, 381),   # 0
        dt.add('point', 133, 192),  # 1
        dt.add('point', 249, 574),  # 2
        dt.add('point', 320, 107),  # 3
        dt.add('point', 503, 488),  # 4
        dt.add('point', 528, 209),  # 5
        dt.add('point', 465, 325),  # 6
    ]

    dt.remove(added[2])
    dt.remove(added[4])
    dt.remove(added[6])
    dt.remove(added[5])
    try:  # this is not always. Just, sometimes, it fails.
        dt.remove(added[0])
    except AssertionError as excinfo:
        assert str(excinfo).startswith(('EV3', 'EV12'))
    else:  # the mesh was good
        dt.remove(added[3])
        # with pytest.raises(AssertionError) as excinfo:
        dt.remove(added[1])
        # assert str(excinfo.value).startswith('EC2')


def test_bug_3():
    # fixed by adding a root vertex
    dt = Mesh(600, 600)
    one = dt.add(1, 400, 300)
    two = dt.add(2, 400, 400)
    tee = dt.add(3, 400, 500)
    foo = dt.add(4, 300, 400)
    dt.remove(two)
    dt.remove(tee)
    dt.remove(foo)
    dt.remove(one)
