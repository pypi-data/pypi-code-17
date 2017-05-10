from collections import defaultdict
from itertools import islice
import random

def sample(lst, size):
    if len(lst) <= size:
        return lst

    return random.sample(lst, size)


def chunk(it, size):
    it = iter(it)
    return iter(lambda: tuple(islice(it, size)), ())

flatten = lambda l: [item for sublist in l for item in sublist]

def group_by(key, l):
    d = defaultdict(list)
    for item in l:
        d[key(item)].append(item)
    return d.items()