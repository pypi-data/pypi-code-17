"""Functions helping for navigation in the Mesh.

"""

import itertools
from math import inf
from operator import itemgetter
from collections import deque
from pydelaunator import Vertex
from pydelaunator.geometry import distance_between_points


def neighbors(vertex:Vertex, max_dist:float=inf, min_dist:float=0.) -> iter:
    assert vertex
    assert min_dist <= max_dist
    reference = vertex
    cur_edge = vertex.edge
    assert cur_edge
    found_neighbors = {vertex}  # set of found neighbors
    queue = deque([vertex])

    def found(v:Vertex) -> (Vertex) or ():
        if v not in found_neighbors:
            found_neighbors.add(v)
            dist = distance_between_points(*reference, *v)
            if min_dist <= dist <= max_dist:
                queue.append(v)
                yield v

    while queue:
        vertex = queue.popleft()
        for nei in vertex.direct_neighbors:
            yield from found(nei)


def nearests(vertex) -> iter:
    distance = lambda v: distance_between_points(*vertex, *v)
    distance_to_one_neighbor = distance(vertex.edge.target_vertex)
    all_neighbors = neighbors(vertex, max_dist=distance_to_one_neighbor)
    candidates = {neighbor: distance(neighbor) for neighbor in all_neighbors}
    # now extract the best of them (minimal distance)
    best_score = min(candidates.values())
    yield from (nei for nei, score in candidates.items() if score == best_score)
