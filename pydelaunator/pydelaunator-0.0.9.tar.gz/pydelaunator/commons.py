

from itertools import zip_longest, islice
from collections import deque
from pydelaunator.setup_logging import logger


def grouped(iterable:iter, by:int, fillvalue=None) -> iter:
    """Collect data into fixed-length chunks or blocks

    >>> tuple(grouped('ABCDEFG', 3, 'x'))
    (('A', 'B', 'C'), ('D', 'E', 'F'), ('G', 'x', 'x'))

    """
    args = [iter(iterable)] * by
    return zip_longest(*args, fillvalue=fillvalue)


def sliding(iterable:iter, size:int) -> iter:
    """Sliding window of given size of given iterable.

    >>> tuple(map(''.join, sliding('ABCD', 2)))
    ('AB', 'BC', 'CD')

    """
    iterable = iter(iterable)
    acc = deque(islice(iterable, 0, size), maxlen=size)
    yield tuple(acc)
    for elem in iterable:
        acc.append(elem)
        yield tuple(acc)


def draw_digraph(graph:iter, layout:dict=None):
    """Print given iterable of 2-uplet understood as edges"""
    import networkx as nx
    import matplotlib
    matplotlib.use("TkAgg")
    import matplotlib.pyplot as plt
    from matplotlib.lines import Line2D

    G = nx.DiGraph()
    G.add_edges_from(graph)
    graph_pos = layout or nx.shell_layout(G)
    nx.draw_networkx_nodes(G, graph_pos, node_size=1000, node_color='blue', alpha=0.3)
    nx.draw_networkx_edges(G, graph_pos, width=2, alpha=0.3, edge_color='green')
    nx.draw_networkx_labels(G, graph_pos, font_size=12, font_family='sans-serif')
    # matplotlib.pyplot.xkcd()
    plt.show()
