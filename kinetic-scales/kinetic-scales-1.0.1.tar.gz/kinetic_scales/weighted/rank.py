# Copyright 2017 Real Kinetic, LLC. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
# either express or implied. See the License for the specific
# language governing permissions and limitations under the License.

import abc
import collections
import six

from fuzzywuzzy import process


class WeightedBase(six.with_metaclass(abc.ABCMeta, collections.Iterable)):
    """Provides a simple iterable that takes a weight and applies it to the items
    in the iterator.  Items are given a score based on place in the iterator
    multiplied by the weight.  This is essentially a simple weighted sum
    model mixed with a Nauru count.
    """
    @abc.abstractproperty
    def weight(self):
        """Return a weight for this iterator.  This weight is applied to all
        items in the iterator.

        :return: weight of these items
        :rtype: number
        """
        pass


class WeightedFuzzyStringBase(WeightedBase):
    """Like WeightedBase but operates on strings and in a fuzzy manner.
    """
    @abc.abstractmethod
    def to_string(self, obj):
        """Return the string representation of the obj.  Similar to sorted's
        key argument.

        :param obj: object to stringify
        :type obj: object
        :return: string representation
        :rtype: str
        """
        pass


class WeightedIterable(WeightedBase):
    """A very simple default implementation of WeightedBase.
    """
    def __init__(self, weight, iterable):
        """Accepts a weight and any iterable which will be used to hydrate
        this iterable.

        :param weight: weight to apply to the items
        :type weight: number
        :param iterable: any iterable
        :type iterable: collections.Iterable
        """
        self._weight = weight
        self._iterable = iterable

    def __iter__(self):
        """Returns an iterator from the underlying iterable.

        :return: iterator
        :rtype: collections.Iterator
        """
        return iter(self._iterable)

    @property
    def weight(self):
        """The weight to apply to items from the iterator.

        :return: weight
        :rtype: number
        """
        return self._weight


def sort(*args):
    """Takes a list of WeightedBase and returns a sorted list of items by rank
    descending.  Items should all be of the same type.

    :return: sorted list of weighted items
    :rtype: list(object)
    """
    items = {}
    for ib in args:
        for i, item in enumerate(ib):
            if item not in items:
                items[item] = 0.0

            items[item] += 1.0/(i + 1) * ib.weight

    weighted = [(score, value) for value, score in items.iteritems()]
    weighted = sorted(weighted, key=lambda x: x[0], reverse=True)
    return map(lambda x: x[1], weighted)


class WeightedFuzzyStringIterable(WeightedFuzzyStringBase):
    """An implementation for use with fuzzy string matching.
    """
    def __init__(self, weight, key, iterable):
        """Accepts a weight and any iterable which will be used to hydrate
        this iterable.

        :param weight: weight to apply to the items
        :type weight: number
        :param key: lambda or function used to retrieve the string key of an item
        :type key: lambda x -> str
        :param iterable: any iterable
        :type iterable: collections.Iterable
        """
        self._weight = weight
        self._iterable = iterable
        self._key = key

    def __iter__(self):
        """Returns an iterator from the underlying iterable.

        :return: iterator
        :rtype: collections.Iterator
        """
        return iter(self._iterable)

    @property
    def weight(self):
        """The weight to apply to items from the iterator.

        :return: weight
        :rtype: number
        """
        return self._weight

    def to_string(self, obj):
        """Returns the string representation of the provided object.

        :param obj: object to stringify
        :type obj: object
        :return: string representation
        :rtype: str
        """
        return self._key(obj)


def fuzzy_string_sort(min_levenshtein_distance, *args):
    """Does a sorting of the provided iterables represented by args by also
    employs a fuzzy string matching algorithm to match similar strings from
    the iterables.  Strings are determined to be identical using a
    levenshtein distance, or minimum edit distance.  If that number is above
    the threshold provided, the strings are considered to be identical.  If
    identical strings are found in the different iterables, the returned list
    takes the value of the previous-major or highest precedent iterable.

    Unfortunately, this is an O(n^2) operation.

    :param min_levenshtein_distance: minimum edit distance for strings to be
        considered identical
    :type min_levenshtein_distance: int or long
    :param args: list of iterables to merge for the weighted sort
    :type args: list(WeightedFuzzyStringBase)
    :return: sorted list of weighted items, descending
    :rtype: list(obj)
    """
    # first thing we're going to do is collapse all the iterables to lists
    ibs = [dict((ib.to_string(item), item) for item in ib) for ib in args]

    # reduce identical strings
    reduced = set()  # going to keep track of strings that have been reduced
    for i, ib in enumerate(ibs[:len(ibs)-1]):
        local_reduced = set()
        for next_ib in ibs[i+1:]:
            for str_, item in ib.iteritems():
                if str_ in reduced:
                    continue

                result = process.extractOne(
                    str_,
                    next_ib.keys(),
                    score_cutoff=min_levenshtein_distance,
                )

                if result is None:  # can get ''
                    continue

                result_str = result[0]
                local_reduced.add(str_)
                next_item = next_ib[result_str]
                del next_ib[result_str]
                next_ib[str_] = next_item

        reduced |= local_reduced

    # now what we have left is a list of dicts where all the keys have been
    # reduced.  We need to convert these dicts into WeightedBase

    wbs = [
        WeightedIterable(args[i].weight, ibs[i].keys())
        for i in xrange(0, len(ibs))
    ]

    all_items = {}
    for ib in reversed(ibs):
        all_items.update(ib)

    result = sort(*wbs)
    return map(lambda x: all_items.get(x), result)
