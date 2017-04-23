# Copyright (C) 2017 by Kevin L. Mitchell <klmitch@mit.edu>
#
# Licensed under the Apache License, Version 2.0 (the "License"); you
# may not use this file except in compliance with the License. You may
# obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied. See the License for the specific language governing
# permissions and limitations under the License.

"""
Object-like access to ``setuptools``-style entrypoints.

This module provides a set of classes that allows an entrypoint to be
looked up easily.  It also caches those lookups efficiently, as
``pkg_resources.iter_entry_points()`` is known to be somewhat slow.

Most users will wish to use the special ``eps`` object to access an
endpoint group: simply access the group name as an attribute of the
``eps`` object.  For instance, to access the endpoints in the endpoint
group "example_app.example_group", use
``eps.example_app.example_group``.  If the group name contains
characters invalid in Python identifiers, use ``getattr()``; for
example, the endpoint group "example app.example group" can be
accessed using ``getattr(eps, "example app.example group")``.  The
only limitation on this is that no component of the group name may
begin with a leading underscore ("_").

The result of accessing the ``eps`` object in this way is an instance
of ``EndpointDict``.  (Note that instances of this class may be
directly instantiated if use of ``eps`` is undesirable or impossible;
simply pass the endpoint group name as the sole argument of the
constructor.)  An ``EndpointDict`` object acts like a read-only
dictionary keyed by endpoint names; the first loadable entrypoint of a
given name can be easily obtained through subscripting or by using the
``get()`` method.  If all the entrypoints of a given name are desired,
use the ``get_all()`` method, which returns a list-like object (an
instance of ``EndpointList``) with all the loadable entrypoints of
that name.

The ``EndpointDict`` and ``EndpointList`` classes are designed to do
as little work as possible to accomplish the requested tasks.  In
particular, if only the first entrypoint with a given name is
required, no other entrypoints will be explored.  However, if
``len()`` is used on either object, all the designated entrypoints
will be explored and all the loadable ones will be loaded, in order to
fully answer the question.  Keep this in mind while using this module.

It is safe to use this module with ``import *``.
"""

import collections

import pkg_resources
import six

__all__ = ['EntrypointList', 'EntrypointDict', 'eps']


class AttrGroup(object):
    """
    Allows attribute-type access to sub-groups.
    """

    def __init__(self, prefix):
        """
        Initialize an ``AttrGroup`` instance.

        :param str prefix: The group name prefix.  This will be
                           prepended to the group name provided to
                           subordinate ``EntrypointDict`` objects.
        """

        # Save the prefix
        self._prefix = prefix

        # Initialize the attribute cache
        self._attr_cache = {}

    def __getattr__(self, name):
        """
        Get a subordinate ``EntrypointDict`` object.

        :param str name: The name of the subordinate
                         ``EntrypointDict`` object.  This name may not
                         begin with '_', but any other characters,
                         including '.', are permitted.

        :returns: A subordinate ``EntrypointDict`` object.
        :rtype: ``EntrypointDict``

        :raises AttributeError:
            An attempt was made to access an internal attribute.
        """

        # Prohibit internal names
        if name.startswith('_'):
            raise AttributeError(
                "'%s' object has no attribute '%s'" %
                (self.__class__.__name__, name)
            )

        # If '.' is in the name, treat it specially
        if '.' in name:
            parts = name.split('.')
            obj = self
            for part in parts:
                obj = getattr(obj, part)
            return obj

        # Dynamically create an EntrypointDict as needed
        if name not in self._attr_cache:
            self._attr_cache[name] = EntrypointDict(self._prefix + name)

        return self._attr_cache[name]


@six.python_2_unicode_compatible
class EntrypointList(collections.Sequence):
    """
    A lazy list of entrypoints.  This ``list`` class is designed to
    only query as many entrypoints as are necessary to accomplish the
    required task.  For instance, asking for ``obj[0]`` will find and
    return only the first loadable entrypoint, without exploring any
    others, yet a subsequent ``obj[1]`` will load the rest of the
    entrypoints.
    """

    def __init__(self, group, name):
        """
        Initialize an ``EntrypointList`` instance.

        :param str group: The name of the entrypoint group.
        :param str name: The name of the entrypoint itself.
        """

        # Save the entrypoint group and name
        self._group = group
        self._name = name

        # List of all found entrypoints
        self._eps = []

        # Have we found 1?
        self._found = False

        # Have we found all of them?
        self._explored = False

        # Set of EntryPoint object IDs that we can skip
        self._entries = set()

    def __str__(self):
        """
        Return a string representation of this object.

        :returns: A string containing a representation of the object.
        :rtype: ``str``
        """

        return '[%s]' % ', '.join(str(item) for item in self)

    def __repr__(self):
        """
        Return a representation of this object.  This variant ensures that
        no entrypoints are explored.

        :returns: A string containing a representation of the object.
        :rtype: ``str``
        """

        return '<%s.%s object at 0x%x>' % (
            self.__class__.__module__, self.__class__.__name__, id(self)
        )

    def __len__(self):
        """
        Determine the number of entrypoints available.

        :returns: The number of loadable entrypoints.
        :rtype: ``int``
        """

        # Make sure we've fully explored the space
        self._find()

        return len(self._eps)

    def __getitem__(self, idx):
        """
        Obtain the specified entrypoint.

        :param idx: An integer or ``slice`` that specifies the
                    entrypoint or entrypoints to return.

        :returns: The designated entrypoint.

        :raises TypeError:
            The ``idx`` is not an integer or slice.

        :raises IndexError:
            The ``idx`` does not exist.
        """

        # Sanity-check the index value
        if not isinstance(idx, (six.integer_types, slice)):
            raise TypeError('list indices must be integers, not str')

        # If it's identically 0, only look for one entry
        if idx == 0:
            self._find(True)
            return self._eps[idx]  # will raise IndexError if empty

        # OK, have to make sure we have the full space
        self._find()
        return self._eps[idx]

    def __bool__(self):
        """
        Determine if the entrypoint list is empty.

        :returns: A ``False`` value if the entrypoint list is empty,
                  ``True`` otherwise.
        :rtype: ``bool``
        """

        # Only look for 1
        self._find(True)

        return bool(self._eps)

    # Alias for Python 2 functionality
    __nonzero__ = __bool__

    def _find(self, one=False):
        """
        Explore the entrypoint space.  This fills ``self._eps`` with the
        entrypoints that can be loaded.

        :param bool one: If ``True``, exploration stops after the
                         first loadable entrypoint is found.  Defaults
                         to ``False``.
        """

        # If we've found what's required, we're done
        if self._explored or (one and self._found):
            return

        # Look up entrypoints
        for ep in pkg_resources.iter_entry_points(self._group, self._name):
            # Skip entrypoints we know about
            if id(ep) in self._entries:
                continue

            # OK, we don't know about it; mark it so we don't try again
            self._entries.add(id(ep))

            # See if we can load it
            try:
                obj = ep.load()
            except (ImportError, AttributeError, pkg_resources.UnknownExtra):
                continue

            # OK, we can load it
            self._eps.append(obj)
            self._found = True

            # Was that all?
            if one:
                return

        # We've fully explored the entrypoint space
        self._found = True
        self._explored = True

    @property
    def group(self):
        """
        Retrieve the entrypoint group.
        """

        return self._group

    @property
    def name(self):
        """
        Retrieve the name of the entrypoint.
        """

        return self._name


@six.python_2_unicode_compatible
class EntrypointDict(AttrGroup, collections.Mapping):
    """
    A lazy dictionary of entrypoints.  This ``dict`` class is designed
    to only query as many entrypoints as are necessary to accomplish
    the required task.  For instance, asking for ``obj['name']`` will
    find and return only the first loadable entrypoint having the name
    ``'name'``, without exploring any others, yet a ``len(obj)`` will
    explore the entire entrypoint space and return the total number of
    unique entrypoint names within the entrypoint group.
    """

    def __init__(self, group):
        """
        Initialize an ``EntrypointDict`` instance.

        :param str group: The name of the entrypoint group.
        """

        # Save the group name
        self._group = group

        # Cache of the entrypoints we've found
        self._entries = {}

        # Have we explored the whole space?
        self._explored = False

        # Initialize the attribute group
        super(EntrypointDict, self).__init__(group + '.')

    def __str__(self):
        """
        Return a string representation of this object.

        :returns: A string containing a representation of the object.
        :rtype: ``str``
        """

        return '{%s}' % ', '.join('%r: %s' % (k, v)
                                  for k, v in self._entries.items())

    def __repr__(self):
        """
        Return a representation of this object.  This variant ensures that
        no entrypoints are explored.

        :returns: A string containing a representation of the object.
        :rtype: ``str``
        """

        return '<%s.%s object at 0x%x>' % (
            self.__class__.__module__, self.__class__.__name__, id(self)
        )

    def __getitem__(self, key):
        """
        Retrieve an entrypoint.

        :param str key: The name of the entrypoint.

        :returns: The requested entrypoint.

        :raises KeyError:
            The designated entrypoint does not exist.
        """

        # Skip if it's not a string
        if not isinstance(key, six.string_types):
            raise KeyError(key)

        # Look up the entrypoint if we don't have it in the cache
        if key not in self._entries:
            self._entries[key] = EntrypointList(self._group, key)

        # We've looked it up but couldn't find one
        if not self._entries[key]:
            raise KeyError(key)

        # Return the first entrypoint
        return self._entries[key][0]

    def __len__(self):
        """
        Determine the number of entrypoints in this entrypoint group.

        :returns: The number of unique entrypoint names in this
                  entrypoint group.
        :rtype: ``int``
        """

        # Make sure we've explored the entrypoint space
        self._find()

        # Subtract out the empty entries
        return len(self._entries) - sum(1 for v in self._entries.values() if v)

    def __iter__(self):
        """
        Iterate through all the entrypoints in this entrypoint group.

        :returns: An iterator that yields entrypoint names.
        """

        # Make sure we've explored the entrypoint space
        self._find()

        for key, value in self._entries.items():
            # Skip entries that weren't found
            if not value:
                continue

            yield key

    def _find(self):
        """
        Explore the entrypoint space.  This fills ``self._entries`` with
        the entrypoints that can be loaded.  Note that this will
        explore the whole space, and update the entrypoint lists to
        reflect this.
        """

        # If we've already explored the space, we're done
        if self._explored:
            return

        # Iterate through the entrypoints
        encountered = set()
        for ep in pkg_resources.iter_entry_points(self._group):
            # We'll want to set the caching attributes later
            encountered.add(ep.name)

            # Is it an entrypoint we've seen already?
            if (ep.name in self._entries and
                    id(ep) in self._entries[ep.name]._entries):
                continue

            # Mark it so we don't try again
            if ep.name not in self._entries:
                self._entries[ep.name] = EntrypointList(self._group, ep.name)
            self._entries[ep.name]._entries.add(id(ep))

            # See if we can load it
            try:
                obj = ep.load()
            except (ImportError, AttributeError, pkg_resources.UnknownExtra):
                continue

            # OK, we can load it
            self._entries[ep.name]._eps.append(obj)

        # Mark that we've fully explored the entrypoint space
        self._explored = True
        for epname in encountered:
            self._entries[epname]._found = True
            self._entries[epname]._explored = True

    # Alias keys_all() so it exists
    keys_all = __iter__

    def items_all(self):
        """
        Like ``items()``, but returns the full list of entrypoints instead
        of just the first entrypoint.

        :returns: An iterator yielding tuples of the entrypoint name
                  and the list of entrypoints with that name.
        """

        # Make sure we've explored the entrypoint space
        self._find()

        for key, value in self._entries.items():
            # Skip entries that weren't found
            if not value:
                continue

            yield (key, value)

    def values_all(self):
        """
        Like ``values()``, but returns the full list of entrypoints instead
        of just the first entrypoint.

        :returns: An iterator yielding the list of entrypoints with a
                  given name.
        """

        # Make sure we've explored the entrypoint space
        self._find()

        for key, value in self._entries.items():
            # Skip entries that weren't found
            if not value:
                continue

            yield value

    def get_all(self, key, default=None):
        """
        Like ``get()``, but returns the full list of entrypoints instead
        of just the first entrypoint.

        :param str key: The name of the entrypoint.
        :param default: A value to return if no entrypoints with the
                        specified name exist.  Defaults to ``None``.

        :returns: A list of entrypoints, or the specified ``default``.
        :rtype: ``EntrypointList``
        """

        # Skip if it's not a string
        if not isinstance(key, six.string_types):
            return default

        # Look up the entrypoint if we don't have it in the cache
        if key not in self._entries:
            self._entries[key] = EntrypointList(self._group, key)

        # We've looked it up but couldn't find one
        if not self._entries[key]:
            return default

        # Return all the entrypoints
        return self._entries[key]

    @property
    def group(self):
        """
        Retrieve the entrypoint group.
        """

        return self._group


# A place to get all the endpoints
eps = AttrGroup('')
