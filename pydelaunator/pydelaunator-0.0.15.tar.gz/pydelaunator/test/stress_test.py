

import itertools
from random import randint

from pydelaunator import Mesh, Edge, Face, Vertex


def run():
    size = 1000
    uid = itertools.count(1)
    mesh = Mesh(size, size)


    for _ in range(1000):
        mesh.add(next(uid), randint(0, size), randint(0, size))

    while True:
        for vertex in mesh.vertices:
            mesh.move(vertex, randint(-1, 1), randint(-1, 1))
