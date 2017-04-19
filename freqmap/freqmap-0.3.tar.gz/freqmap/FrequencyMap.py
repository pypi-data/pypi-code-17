from collections import Counter     # Used for the inner map
from random import randrange        # Used for random probalistic retrieval


class FrequencyMap:
    """A structure designed for mapping hashable types to other hashable types,
    to be used for implementing n-grams, Markov chains, and other similiar,
    frequency based patterns."""

    def __init__(self):
        self.map = dict()

    def add(self, key, value):
        """Increment the count of the key-value pair,
        inserting a new pair if it does not exist"""
        try:
            self.map[key].update([value])
        except KeyError:
            self.map.update({key: Counter()})
            self.map[key].update([value])

    def subtract(self, key, value):
        """Decrement the count of the key-value pair if it exists.
        Does not allow negative values."""
        try:
            if self.map[key][value] > 0:
                self.map[key].subtract([value])
        except KeyError:
            pass

    def common_from(self, key):
        """Returns the most common answer for a given key.
        Raises KeyError if the key does not exist."""
        return self.map[key].most_common(1)[0][0]

    def random_from(self, key):
        """Randomly returns a value of the given key based on the probability
        that the value follows the key. Raises KeyError if the key does not
        exist."""
        rand = randrange(sum(self.map[key].values()))
        # Decrement by each count in the inner Counter until the random number
        # is less than zero, then return that inner key
        for value in self.map[key]:
            rand -= self.map[key][value]
            if rand < 0:
                return value

    def __str__(self):
        string = ''
        for key in self.map:
            string += str(key) + ' -->'
            for value in self.map[key].most_common():
                string += ' ' + str(value)
            string += '\n'
        return string
