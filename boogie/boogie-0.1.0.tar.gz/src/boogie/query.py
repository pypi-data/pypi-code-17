"""
=============================
Django managers and querysets
=============================

Django ORM is nice, but it is not awesome.


Problems
=========

QuerySet vs. Managers
---------------------

Django Managers and QuerySets have a huge overlap. Most of the time, Django's
Manager classes are created from querysets, such as Django's own Manager class:

.. code-block:: python
    class Manager(BaseManager.from_queryset(QuerySet)):
        pass

``BaseManager`` provides a few methods such as ``deconstruct``,
``contribute_to_class`` that are necessary for migrations and for model
introspection. Most user-facing methods, however, are just wrapped QuerySet
methods.

To the user, Managers and QuerySets seems to be the same thing: you can
``.filter()``, ``.get()``, and use basically the same methods.


Code organization
-----------------

In Django, row-level logic belongs in the model and table-level logic
belongs in the Managers/QuerySets.

"""
import collections

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Model
from django.db.models.manager import Manager
from lazyutils import lazy, delegate_to

from boogie.types.attrlist import AttrList


class QueryMeta(type):
    """
    Metaclass that override a few behaviors:
    """


def queryset_value_method(name, rettype=None):
    """
    Return a wrapped version of a QuerySet method that returns a regular value.
    """

    docstring = 'see also: :cls:`django.db.models.query.QuerySet.%s`'
    docstring = docstring % name

    def method(self, *args, **kwargs) -> rettype:
        method = getattr(self._queryset, name)
        return method(*args, **kwargs)

    method.__name__ = name
    method.__doc__ = docstring
    return method


def queryset_to_queryset_method(name):
    """
    Return a wrapped version of a QuerySet method that returns a regular value.
    """

    docstring = 'see also: :cls:`django.db.models.query.QuerySet.%s`'
    docstring = docstring % name

    def method(self, *args, **kwargs):
        method = getattr(self._queryset, name)
        qs = method(*args, **kwargs)
        return self._new(queryset=qs)

    method.__name__ = name
    method.__doc__ = docstring
    return method


class Location:
    def __init__(self, table, queryset):
        self._owner = table
        self._queryset = queryset


class QuerySet(Manager, metaclass=QueryMeta):
    """
    A QuerySet class that unifies Django's QuerySets and Managers.

    You can replace the default manager of your model by a QuerySet instance.
    """

    @lazy
    def _queryset(self):
        if self._manager is None:
            qs = super().get_queryset()
        else:
            qs = self._manager.get_queryset()
        return qs

    def __init__(self, manager=None, queryset=None, model=None, using=None,
                 hints=None):
        super().__init__()
        self._manager = manager
        if queryset is not None:
            self._queryset = queryset
        self.model = model or getattr(queryset, 'model', None)
        self._db = using
        self._hints = hints

    def _new(self, *args, **kwargs):
        """
        Return a new instance.

        It is useful for sub
        """
        return type(self)(*args, **kwargs)

    #
    # Public attributes and introspection
    #
    ordered = delegate_to('_queryset')
    db = delegate_to('_queryset')

    #
    # Python magic methods.
    #
    def __iter__(self):
        return iter(self._queryset)

    def __len__(self):
        return self._queryset.count()

    def __bool__(self):
        return self._queryset.exists()

    def __getitem__(self, idx):
        # Handle 2D indexes
        if isinstance(idx, tuple):
            try:
                i, j = idx
            except ValueError:
                raise IndexError('QuerySets support only 1D and 2D indexes')
            return self._getitem_2d(i, j)
        elif isinstance(idx, slice):
            return self._getitem_slice(idx)
        elif isinstance(idx, (int, str)):
            return self._getitem_pk(idx)
        else:
            return self._getitem_seq(idx)

    def __setitem__(self, idx, value):
        raise NotImplementedError

    def __eq__(self, other):
        if isinstance(other, collections.Sequence):
            if len(self) != len(other):
                return False
            return all(x == y for x, y in zip(self, other))
        return NotImplemented

    #
    # List and Set methods.
    #
    # Django querysets exposes a set-sh and list-sh API.
    # We want to explicitly support all frozenset functions and a few immutable
    # idioms for the set interface.
    #
    # The list interface is supported by the .loc attribute that is reminiscent
    # of the same attribute in Pandas.
    #
    @lazy
    def loc(self):
        return Location(self, queryset=self._queryset)

    #
    # Frozendict methods
    #
    # TODO: check those: difference, intersection, union

    def copy(self):
        """
        Return a copy.

        The copy flushes any cached objects.
        """
        return self.all()

    def symmetric_difference(self, other):
        """
        Return the symmetric difference of two sets as a new set.

        (i.e. all elements that are in exactly one of the sets.)
        """
        raise NotImplementedError

    def isdisjoint(self, other):
        """
        Return True if two sets have a null intersection.
        """
        raise NotImplementedError

    def issubset(self, other):
        """
        Report whether another set contains this set.
        """
        raise NotImplementedError

    def issuperset(self, other):
        """
        Report whether this set contains another set.
        """
        raise NotImplementedError

    #
    # Methods that perform queries and return regular Python types.
    # We just delegate the implemetation to the ._queryset attribute.
    #
    iterator = queryset_value_method('iterator', iter)
    aggregate = queryset_value_method('aggregate', dict)
    count = queryset_value_method('count', int)
    get = queryset_value_method('get', Model)
    create = queryset_value_method('create', Model)
    bulk_create = queryset_value_method('bulk_create', list)
    get_or_create = queryset_value_method('get_or_create', (Model, bool))
    update_or_create = queryset_value_method('update_or_create', (Model, bool))
    earliest = queryset_value_method('earliest', Model)
    latest = queryset_value_method('latest', Model)
    first = queryset_value_method('first', Model)
    last = queryset_value_method('last', Model)
    in_bulk = queryset_value_method('in_bulk', dict)
    delete = queryset_value_method('delete', (list, int))
    update = queryset_value_method('delete', int)
    exists = queryset_value_method('exists', bool)

    #
    # Methods that perform queries and return a queryset.
    # Those methods require us to wrap the result on a QuerySet.
    #

    # Queryset subclasses
    raw = queryset_to_queryset_method('raw')
    values = queryset_to_queryset_method('values')
    values_list = queryset_to_queryset_method('values_list')
    dates = queryset_to_queryset_method('dates')
    datetimes = queryset_to_queryset_method('datetimes')
    none = queryset_to_queryset_method('none')

    # Queryset to regular querysets
    filter = queryset_to_queryset_method('filter')
    exclude = queryset_to_queryset_method('exclude')
    complex_filter = queryset_to_queryset_method('complex_filter')
    union = queryset_to_queryset_method('union')
    intersection = queryset_to_queryset_method('intersection')
    difference = queryset_to_queryset_method('difference')
    select_for_update = queryset_to_queryset_method('select_for_update')
    select_related = queryset_to_queryset_method('select_related')
    prefetch_related = queryset_to_queryset_method('prefetch_related')
    annotate = queryset_to_queryset_method('annotate')
    order_by = queryset_to_queryset_method('order_by')
    distinct = queryset_to_queryset_method('distinct')
    extra = queryset_to_queryset_method('extra')
    reverse = queryset_to_queryset_method('reverse')
    defer = queryset_to_queryset_method('defer')
    using = queryset_to_queryset_method('using')

    def all(self):
        """
        Returns all objects.

        This should never be necessary. It is here just for compatibility with
        Django's API.
        """
        if self._manager:
            return self
        else:
            return self._new(queryset=self._queryset.all())

    #
    # Auxiliary private methods
    #
    def _pk_set(self):
        """
        Return a set of all pk's in the current queryset.
        """
        return set(self.values_list('pk', flat=True))

    # Item getters
    _pk_types = (int, str)
    _slice_err = IndexError('slicing is not supported: use QuerySet.loc '
                            'attribute.')

    def _getitem_2d(self, i, j):
        # Check if first index is a slice and move to column fetch instead
        if isinstance(i, slice):
            if not i == slice(None, None, None):
                raise self._slice_err
            return self._getitem_col(j)

        # Assume first index is selecting a single element by pk
        if isinstance(i, self._pk_types):
            is_j_str = isinstance(j, str)
            fields = [j] if is_j_str else j
            data = list(
                self._queryset.filter(pk=i).values_list(*fields, flat=True))
            if not data:
                raise IndexError('no element found with pk: %r' % i)
            if is_j_str:
                return data[0]
            return AttrList(data, fields)

        # First index is a list
        if isinstance(i, list):
            raise NotImplementedError

        raise IndexError('invalid index: %r' % [i, j])

    def _getitem_col(self, col):
        pass

    def _getitem_pk(self, pk):
        try:
            return self.get(pk=pk)
        except ObjectDoesNotExist:
            raise IndexError(pk)

    def _getitem_slice(self, idx):
        if idx == slice(None, None, None):
            return self.all()
        raise self._slice_err

    def _getitem_seq(self, seq):
        data = self.in_bulk(seq)
        return [data[pk] for pk in seq]
