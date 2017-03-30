"""
API: Official recipes
---------------------
"""
# Licensed under PSF license - see licenses/LICENSE_PYTHON.rst

# Built-ins
from __future__ import absolute_import, division, print_function
from collections import deque
from copy import copy
from itertools import islice, chain, repeat, starmap, tee, combinations
from random import choice, sample, randrange

# This module
from .. import EQ_PY2

# Replace list-generating functions by generator functions
if EQ_PY2:
    from itertools import (ifilter as filter,
                           ifilterfalse as filterfalse)
    range = xrange
else:
    from itertools import filterfalse


__all__ = ['consume',
           'flatten',
           'ipartition',
           'ncycles',
           'powerset',
           'random_combination', 'random_product', 'random_permutation',
           'repeatfunc',
           'tail', 'tee_lookahead']


def tail(iterable, n):
    """Return an iterator over the last `n` items.

    Parameters
    ----------
    iterable : iterable
        The `iterable` from which to take the last items.

    n : int
        How many elements.

    Returns
    -------
    iterator : iterator
        The last `n` items of `iterable` as iterator.

    Examples
    --------
    >>> from iteration_utilities import tail
    >>> list(tail('ABCDEFG', 3))
    ['E', 'F', 'G']
    """
    # tail(3, 'ABCDEFG') --> E F G
    return iter(deque(iterable, maxlen=n))


def consume(iterator, n):
    """Advance the `iterator` `n`-steps ahead. If `n` is ``None``, consume \
        entirely.

    Parameters
    ----------
    iterator : iterator
        Any `iterator` from which to consume the items.

    n : int, None
        Number of items to consume from the `iterator`. If ``None`` consume it
        entirely.

    Examples
    --------
    >>> from iteration_utilities import consume
    >>> g = (x**2 for x in range(10))
    >>> consume(g, 2)
    >>> list(g)
    [4, 9, 16, 25, 36, 49, 64, 81]

    >>> g = (x**2 for x in range(10))
    >>> consume(g, None)
    >>> list(g)
    []
    """
    # Use functions that consume iterators at C speed.
    if n is None:
        # feed the entire iterator into a zero-length deque
        deque(iterator, maxlen=0)
    else:
        # advance to the empty slice starting at position n
        next(islice(iterator, n, n), None)


def ncycles(iterable, n):
    """Returns the sequence elements n times.

    Parameters
    ----------
    iterable : iterable
        Any `iterable` to repeat.

    n : int
        Number of repeatitions.

    Returns
    -------
    repeated_iterable : generator
        The `iterable` repeated `n` times.

    Examples
    --------
    >>> from iteration_utilities import ncycles
    >>> list(ncycles([1,2,3], 3))
    [1, 2, 3, 1, 2, 3, 1, 2, 3]
    """
    return chain.from_iterable(repeat(tuple(iterable), n))


def flatten(iterable):
    """Flatten one level of nesting.

    Parameters
    ----------
    iterable : iterable
        Any `iterable` to flatten.

    Returns
    -------
    flattened_iterable : generator
        The `iterable` with the first level of nesting flattened.

    Examples
    --------
    >>> from iteration_utilities import flatten
    >>> list(flatten([[1,2,3,4], [4,3,2,1]]))
    [1, 2, 3, 4, 4, 3, 2, 1]
    """
    return chain.from_iterable(iterable)


def repeatfunc(func, *args, **times):
    """Repeat calls to `func` with specified arguments.

    Parameters
    ----------
    func : callable
        The function that will be called.

    args :
        optional arguments for the `func`.

    times : int, None, optional
        The number of `times` the function is called. If ``None`` there will be
        no limit.
        Default is ``None``.

    Returns
    -------
    iterable : generator
        The result of the repeatedly called function.

    Examples
    --------
    >>> from iteration_utilities import repeatfunc, getitem
    >>> import random

    >>> random.seed(5)
    >>> list(getitem(repeatfunc(random.random), stop=5))
    {0}

    >>> random.seed(2)
    >>> list(repeatfunc(random.random, times=3))
    [0.9560342718892494, 0.9478274870593494, 0.05655136772680869]
    >>> random.seed(None)

    .. warning::
        This will return an infinitly long generator if you don't specify
        ``times``.
    """
    times = times.get('times', None)
    if times is None:
        return starmap(func, repeat(args))
    return starmap(func, repeat(args, times))


def ipartition(iterable, pred):
    """Use a predicate to partition entries into ``False`` entries and ``True``
    entries.

    Parameters
    ----------
    iterable : iterable
        `Iterable` to partition.

    pred : callable
        The predicate which determines the group in which the value of the
        `iterable` belongs.

    Returns
    -------
    false_values : generator
        An iterable containing the values for which the predicate was False.

    true_values : generator
        An iterable containing the values for which the predicate was True.

    Examples
    --------
    >>> from iteration_utilities import ipartition
    >>> def is_odd(val): return val % 2
    >>> [list(i) for i in ipartition(range(10), is_odd)]
    [[0, 2, 4, 6, 8], [1, 3, 5, 7, 9]]
    """
    t1, t2 = tee(iterable)
    return filterfalse(pred, t1), filter(pred, t2)


def powerset(iterable):
    """Create all possible sets of values from an `iterable`.

    Parameters
    ----------
    iterable : iterable
        `Iterable` for which to create a powerset.

    Returns
    -------
    powerset : generator
        An iterable containing all powersets as tuple.

    Examples
    --------
    >>> from iteration_utilities import powerset
    >>> list(powerset([1,2,3]))
    [(), (1,), (2,), (3,), (1, 2), (1, 3), (2, 3), (1, 2, 3)]
    """
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))


def random_product(*iterables, **repeat):
    """Random selection from :py:func:`itertools.product`.

    Parameters
    ----------
    iterables : iterable
        Any amount of `iterables` from to pass to
        :py:func:`itertools.product`.

    repeat : int, optional
        The number of random samples.
        Default is ``1``.

    Returns
    -------
    sample : tuple
        A tuple containing the random samples.

    Raises
    ------
    IndexError
        If any `iterable` is empty.

    Examples
    --------
    Take one random sample::

        >>> from iteration_utilities import random_product
        >>> import random
        >>> random.seed(70)

        >>> random_product(['a', 'b'], [1, 2], [0.5, 0.25])
        {0}

    Or take multiple samples::

        >>> random.seed(10)
        >>> random_product(['a', 'b'], [1, 2], [0.5, 0.25], repeat=5)
        {1}
        >>> random.seed(None)
    """
    pools = [tuple(pool) for pool in iterables] * repeat.get('repeat', 1)
    return tuple(choice(pool) for pool in pools)


def random_permutation(iterable, r=None):
    """Random selection from :py:func:`itertools.permutations`.

    Parameters
    ----------
    iterable : iterable
        The `iterable` to permutate with :py:func:`itertools.permutations`.

    r : int, None, optional
        The number of elements to permutate. If ``None`` use all elements from
        the iterable.
        Default is ``None``.

    Returns
    -------
    random_permutation : tuple
        The randomly chosen permutation.

    Examples
    --------
    One random permutation::

        >>> from iteration_utilities import random_permutation
        >>> import random
        >>> random.seed(20)
        >>> random_permutation([1,2,3,4,5,6])
        {0}

    One random permutation using a subset of the `iterable` (here 3 elements)::

        >>> random.seed(5)
        >>> random_permutation([1,2,3,4,5,6], r=3)
        {1}
        >>> random.seed(None)
    """
    pool = tuple(iterable)
    r = len(pool) if r is None else r
    return tuple(sample(pool, r))


def random_combination(iterable, r, replacement=False):
    """Random selection from :py:func:`itertools.combinations`.

    Parameters
    ----------
    iterable : iterable
        The `iterable` to combine with :py:func:`itertools.combinations`.

    r : int
        The number of elements to combine.

    replacement : bool
        If ``True`` then replace already included values (uses
        :py:func:``itertools.combinations_with_replacement`).
        Default is ``False``.

    Returns
    -------
    random_combination : tuple
        The randomly chosen combination.

    Examples
    --------
    >>> from iteration_utilities import random_combination
    >>> import random
    >>> random.seed(5)

    >>> random_combination([1,2,3,4,5,6], r=4)
    (3, 4, 5, 6)

    >>> random.seed(100)

    >>> random_combination([1,2,3,4,5,6], r=4, replacement=True)
    {0}

    >>> random.seed(None)

    >>> random.seed(None)
    """
    pool = tuple(iterable)
    n = len(pool)
    if replacement:
        indices = sorted(randrange(n) for _ in range(r))
    else:
        indices = sorted(sample(range(n), r))
    return tuple(pool[i] for i in indices)


def tee_lookahead(tee, i):
    """Inspect the `i`-th upcomping value from a tee object while leaving the
    tee object at its current position.

    Parameters
    ----------
    tee : :py:func:`itertools.tee`
        The tee object in which to look ahead.

    i : int
        The index counting from the current position which should be peeked.

    Returns
    -------
    peek : any type
        The element at the `i`-th upcoming index in the tee object.

    Raises
    ------
    IndexError
        If the underlying iterator doesn't have enough values.

    Examples
    --------
    >>> from iteration_utilities import tee_lookahead
    >>> from itertools import tee
    >>> t1, t2 = tee([1,2,3,4,5,6])
    >>> tee_lookahead(t1, 0)
    1
    >>> tee_lookahead(t1, 1)
    2
    >>> tee_lookahead(t1, 0)
    1
    """
    for value in islice(copy(tee), i, None):
        return value
    raise IndexError(i)


# Due to a change in random.choice the results are not reproducible between
# python < 3.2 and afterwards.


def _replace_docs(func, *args, **kwargs):
    func.__doc__ = func.__doc__.format(*args, **kwargs)

if EQ_PY2:
    _replace_repeatfunc = ('[0.6229016948897019, 0.7417869892607294, '
                           '0.7951935655656966, 0.9424502837770503, '
                           '0.7398985747399307]')
    _replace_docs(repeatfunc, _replace_repeatfunc)
    _replace_docs(random_combination, '(1, 3, 5, 5)')
    _replace_docs(random_permutation, '(6, 4, 5, 3, 1, 2)', '(4, 6, 5)')
    _replace_docs(random_product, "('b', 1, 0.5)",
                  "('b', 1, 0.25, 'a', 2, 0.25, 'b', 1, 0.25, "
                  "'a', 1, 0.25, 'b', 1, 0.25)")

else:
    _replace_repeatfunc = ('[0.6229016948897019, 0.7417869892607294, '
                           '0.7951935655656966, 0.9424502837770503, '
                           '0.7398985747399307]')
    _replace_docs(repeatfunc, _replace_repeatfunc)
    _replace_docs(random_combination, '(2, 2, 4, 4)')
    _replace_docs(random_permutation, '(6, 2, 3, 4, 1, 5)', '(5, 3, 6)')
    _replace_docs(random_product, "('a', 2, 0.25)",
                  "('a', 2, 0.25, 'a', 1, 0.25, 'b', 2, 0.5, "
                  "'a', 2, 0.25, 'a', 1, 0.25)")
