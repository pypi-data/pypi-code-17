

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
    assert len(mesh.edges) == 12
    assert len(mesh.corners) == 4
    assert len(mesh.vertices) == 4
    assert mesh.vertices == mesh.corners
    added = mesh.add('object', 50, 50)
    assert mesh.vertices != mesh.corners
    assert len(mesh.vertices) == 5
    assert added in mesh.vertices
    assert added not in mesh.corners
    added = mesh.remove(added)
    assert len(mesh.edges) == 12
    assert len(mesh.corners) == 4
    assert len(mesh.vertices) == 4


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
        assert nb_nei == 3
        assert nb_nei == len(set(vertex.direct_neighbors))


def test_neighbors_more(mesh):
    added_vertex = mesh.add('object', 50, 50)
    assert len(tuple(added_vertex.direct_neighbors)) == 4
    for vertex in mesh.vertices:
        nb_nei = len(tuple(vertex.direct_neighbors))
        assert nb_nei in {3, 4}
        assert nb_nei == len(set(vertex.direct_neighbors))
