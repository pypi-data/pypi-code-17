"""A module containing functions that can be used to partition lists."""
import random

def pseudorandom_function(index):
    """A function that just wraps ``random.random()`` and ensures it received a non-negative
    index."""
    assert index >= 0, "Index must be non-negative! Got {} instead.".format(index)
    return random.random()

class LinearFakeRandomFunction():
    """A "random" function that always returns the index divided by the total number of elements. In
    other words, this fake random function linearly increases with the index."""

    def __init__(self, n_of_elements):
        assert n_of_elements > 0, "Number of elements must be greater than 0!"
        self.n_of_elements = n_of_elements

    def __call__(self, index):
        assert index >= 0, "Index must be non-negative! Got {} instead.".format(index)
        assert index < self.n_of_elements, (
            "You sent an index ({}) that's larger than the supposed numer of elements ({})!".format(
                index,
                self.n_of_elements,
            )
        )
        return index / self.n_of_elements

def partitioner(n_of_elements, weights, rand=pseudorandom_function):
    """
    Partitions elements ``0..n-1`` into ``len(weights)`` buckets. The probability that an
    element is in bucket ``i`` is given by ``weights[i] / sum(weights)``.
    """
    assert n_of_elements > 0, "The number of elements needs to be larger than 0."
    assert all(map(lambda x: x >= 0, weights)), "All elements of weights must be non negative."
    sum_weights = sum(weights)
    assert sum_weights > 0, "The sum of all weights must be larger than 0."
    n_of_buckets = len(weights)
    buckets = [0]
    for i in range(n_of_buckets):
        buckets.append(buckets[i] + weights[i] / sum_weights)
    for i in range(n_of_elements):
        value = rand(i)
        for j in range(n_of_buckets+1):
            if buckets[j] > value:
                yield j-1
                break
        else:
            yield n_of_buckets-1
